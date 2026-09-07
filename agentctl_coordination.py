from __future__ import annotations

import argparse
import json
import os
import signal
import sys
import tempfile
import time
import uuid
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from pathlib import Path

import acli
import acli.args


def identifier(value: str) -> str:
    try:
        return str(uuid.UUID(value))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected a UUID") from exc


@contextmanager
def file_lock(path: Path, *, blocking: bool = True) -> Iterator[None]:
    try:
        import fcntl
    except ImportError as exc:
        raise RuntimeError(
            "claim coordination requires POSIX flock (tested on Linux)"
        ) from exc
    with path.open("a") as handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | (0 if blocking else fcntl.LOCK_NB))
        except BlockingIOError as exc:
            raise RuntimeError("this wait already has a running observer") from exc
        try:
            yield
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


def atomic_json(path: Path, value: dict) -> None:
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", dir=path.parent, prefix=".tmp-", delete=False
        ) as out:
            temporary = Path(out.name)
            json.dump(value, out, sort_keys=True)
            out.write("\n")
            out.flush()
            os.fsync(out.fileno())
        temporary.replace(path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


class Coordination:
    def __init__(self, state: Path, stale_minutes: int = 70) -> None:
        self.root = state / "coordination"
        self.stale_seconds = stale_minutes * 60

    @contextmanager
    def locked(self) -> Iterator[None]:
        self.root.mkdir(parents=True, exist_ok=True)
        # Keep the lock inode outside directories that are archived.
        with file_lock(self.root / ".lock"):
            yield

    def path(self, wait_id: str) -> Path:
        return self.root / wait_id

    def read(self, wait_id: str) -> dict:
        path = self.path(wait_id)
        record = json.loads((path / "wait.json").read_text())
        if (path / "closed.json").exists():
            self.archive(wait_id, "done")
            raise FileNotFoundError(f"wait {wait_id} is closed")
        if time.time() - record["heartbeat"] > self.stale_seconds:
            self.archive(wait_id, "stale")
            raise FileNotFoundError(f"wait {wait_id} is stale")
        return record

    def archive(self, wait_id: str, destination: str) -> None:
        target = self.root / destination
        target.mkdir(exist_ok=True)
        self.path(wait_id).rename(target / wait_id)

    def close(self, wait_id: str, reason: str) -> None:
        atomic_json(
            self.path(wait_id) / "closed.json", {"reason": reason, "at": time.time()}
        )
        self.archive(wait_id, "done")

    def sweep(self, *, dry_run: bool = False) -> list[dict]:
        result = []
        for path in sorted(self.root.iterdir()):
            if not path.is_dir() or path.name in {"done", "stale"}:
                continue
            closed = (path / "closed.json").exists()
            record_path = path / "wait.json"
            # A crash during initial publication can leave an empty directory.
            heartbeat = (
                json.loads(record_path.read_text())["heartbeat"]
                if record_path.exists()
                else path.stat().st_mtime
            )
            if not closed and time.time() - heartbeat <= self.stale_seconds:
                continue
            destination = "done" if closed else "stale"
            result.append({"wait_id": path.name, "target": destination})
            if not dry_run:
                self.archive(path.name, destination)
        return result


def emit(value: dict, fmt: object) -> None:
    acli.emit(value, fmt)
    sys.stdout.flush()


def follow(
    store: Coordination,
    args: argparse.Namespace,
    session_id: str,
    check: Callable[[], tuple[int, dict]],
    refresh: Callable[[], None],
) -> int:
    fmt = acli.resolve_format(args)
    intent = {
        "session_id": session_id,
        "paths": args.paths,
        "carve": args.carve,
        "minutes": args.minutes,
        "note": args.note,
    }
    wait_id = args.wait_id or str(uuid.uuid4())
    with store.locked():
        if args.wait_id:
            record = store.read(wait_id)
            if any(record[key] != value for key, value in intent.items()):
                raise ValueError(
                    "--wait-id must belong to this session and match paths, --carve, --minutes and --note"
                )
        else:
            code, result = check()
            if code == 0:
                emit(result, fmt)
                return code
            store.sweep()
            path = store.path(wait_id)
            path.mkdir()
            (path / "notices").mkdir()
            record = {
                "version": 1,
                "wait_id": wait_id,
                **intent,
                "created_at": time.time(),
                "heartbeat": time.time(),
                "deaf": args.deaf,
            }
            atomic_json(path / "wait.json", record)
        observer = file_lock(store.path(wait_id) / ".observer.lock", blocking=False)
        observer.__enter__()

    def interrupted(signum: int, frame: object) -> None:
        raise KeyboardInterrupt

    previous = signal.signal(signal.SIGTERM, interrupted)
    seen: set[str] = set()
    last_conflicts = None
    deadline = time.monotonic() + args.timeout if args.timeout else None
    try:
        while True:
            with store.locked():
                record = store.read(wait_id)
                record.update(heartbeat=time.time(), deaf=args.deaf)
                atomic_json(store.path(wait_id) / "wait.json", record)
                refresh()
                notices = []
                if not args.deaf:
                    for path in sorted(
                        (store.path(wait_id) / "notices").glob("*.json")
                    ):
                        if path.stem not in seen:
                            notices.append(json.loads(path.read_text()))
                code, result = check()
                if code == 0:
                    store.close(wait_id, "claimed")
            for notice in notices:
                emit({"kind": "coordination_notice", **notice}, fmt)
                seen.add(notice["notice_id"])
            if code == 0:
                emit({**result, "wait_id": wait_id}, fmt)
                return code
            conflicts = [
                {key: row[key] for key in ("path", "id", "claim", "kind", "status")}
                for row in result["conflicts"]
            ]
            if conflicts != last_conflicts:
                emit(
                    {
                        **result,
                        "kind": "clear_wait",
                        "wait_id": wait_id,
                        "deaf": args.deaf,
                    },
                    fmt,
                )
                last_conflicts = conflicts
            if deadline is not None and time.monotonic() >= deadline:
                emit(
                    {"kind": "clear_paused", "wait_id": wait_id, "reason": "timeout"},
                    fmt,
                )
                return 1
            time.sleep(
                min(args.poll, max(0, deadline - time.monotonic()))
                if deadline
                else args.poll
            )
    except KeyboardInterrupt:
        emit({"kind": "clear_paused", "wait_id": wait_id, "reason": "interrupted"}, fmt)
        return 130
    finally:
        signal.signal(signal.SIGTERM, previous)
        observer.__exit__(None, None, None)


def command(
    store: Coordination, args: argparse.Namespace, session_id: str | None
) -> int:
    fmt = acli.resolve_format(args)
    with store.locked():
        if args.operation == "sweep":
            result = {
                "kind": "coordination_sweep",
                "entries": store.sweep(dry_run=args.dry_run),
                "dry_run": args.dry_run,
            }
        elif args.operation == "list":
            waits = []
            for path in sorted(store.root.iterdir()):
                if not path.is_dir() or path.name in {"done", "stale"}:
                    continue
                record_path = path / "wait.json"
                if record_path.exists():
                    record = json.loads(record_path.read_text())
                    waits.append(
                        {
                            **(
                                record
                                if args.full
                                else {
                                    key: record[key]
                                    for key in (
                                        "wait_id",
                                        "session_id",
                                        "paths",
                                        "deaf",
                                    )
                                }
                            ),
                            "stale": time.time() - record["heartbeat"]
                            > store.stale_seconds,
                            "closed": (path / "closed.json").exists(),
                        }
                    )
            result = {"kind": "coordination_waits", "waits": waits}
        else:
            if not session_id:
                raise ValueError("coordination notice/cancel requires a session id")
            if (
                args.operation == "cancel"
                and (store.root / "done" / args.wait_id / "wait.json").exists()
            ):
                record = json.loads(
                    (store.root / "done" / args.wait_id / "wait.json").read_text()
                )
                if record["session_id"] != session_id:
                    raise ValueError("only the waiter may cancel its wait")
                reason = json.loads(
                    (store.root / "done" / args.wait_id / "closed.json").read_text()
                )["reason"]
                result = {
                    "kind": "coordination_closed",
                    "wait_id": args.wait_id,
                    "reason": reason,
                }
            else:
                record = store.read(args.wait_id)
                if args.operation == "cancel":
                    if record["session_id"] != session_id:
                        raise ValueError("only the waiter may cancel its wait")
                    with file_lock(
                        store.path(args.wait_id) / ".observer.lock", blocking=False
                    ):
                        store.close(args.wait_id, "cancelled")
                    result = {
                        "kind": "coordination_closed",
                        "wait_id": args.wait_id,
                        "reason": "cancelled",
                    }
                else:
                    if record["deaf"]:
                        raise ValueError("wait uses --deaf and does not accept notices")
                    if not args.message.strip():
                        raise ValueError("--message must not be empty")
                    notice_id = args.notice_id or str(uuid.uuid4())
                    notice = {
                        "wait_id": args.wait_id,
                        "notice_id": notice_id,
                        "from": session_id,
                        "to": record["session_id"],
                        "message": args.message,
                    }
                    path = store.path(args.wait_id) / "notices" / (notice_id + ".json")
                    if path.exists():
                        old = json.loads(path.read_text())
                        if any(old[key] != value for key, value in notice.items()):
                            raise ValueError(
                                "--notice-id already identifies a different notice"
                            )
                    else:
                        atomic_json(path, {**notice, "created_at": time.time()})
                    result = {
                        "kind": "coordination_posted",
                        "wait_id": args.wait_id,
                        "notice_id": notice_id,
                        "status": "persisted",
                    }
    emit(result, fmt)
    return 0


def register(subparsers: object, callback: Callable) -> None:
    parser = subparsers.add_parser(
        "coordination",
        help="List claim waits, post notices, cancel or archive waits; instant, structured stdout.",
    )
    verbs = parser.add_subparsers(dest="operation", required=True)
    for name, help_text in (
        ("list", "List open claim waits and their IDs; instant, structured stdout."),
        (
            "notice",
            "Publish an immutable notice to a wait; instant, structured stdout. No wake or acknowledgment. Archived/deaf waits reject notices.",
        ),
        (
            "cancel",
            "Cancel your paused wait and archive it to coordination/done; stop its observer first. Instant, structured stdout.",
        ),
        (
            "sweep",
            "Archive closed waits to done and waits without a waiter heartbeat for 70 minutes to stale; no deletion. Instant, structured stdout.",
        ),
    ):
        child = verbs.add_parser(name, help=help_text, description=help_text)
        if name in {"notice", "cancel"}:
            child.add_argument(
                "wait_id",
                type=identifier,
                help="Wait UUID from clear output or coordination list.",
            )
        if name == "notice":
            child.add_argument(
                "--message",
                required=True,
                help="Peer coordination text; not user authorization or claim release.",
            )
            child.add_argument(
                "--notice-id",
                type=identifier,
                help="Stable UUID for idempotent retries; generated if omitted.",
            )
        if name == "sweep":
            child.add_argument(
                "--dry-run",
                action="store_true",
                help="Report proposed archives without moving them.",
            )
        acli.args.add_standard_args(child)
        child.set_defaults(func=callback)
