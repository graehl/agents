"""Filesystem rendezvous subscriptions and immutable delivered snapshots."""

from __future__ import annotations

import ctypes
import fcntl
import hashlib
import json
import logging
import mimetypes
import os
import queue
import runpy
import select
import shutil
import struct
import subprocess
import sys
import threading
import time
import uuid
from collections.abc import Iterator
from pathlib import Path

from agentctl_coordination import atomic_json, file_lock
from session_attachments import attachment_profile, prepare_attachment

MAX_ROUTES = 128
MAX_FILES = 10000
MAX_UPLOAD_BYTES = 64 * 1024 * 1024
CODE_ROOT = Path(__file__).resolve().parent
DEFAULT_WINDOW_MS = 1000
DEFAULT_MAX_PER_WINDOW = 10
LOGGER = logging.getLogger(__name__)


class BurstAdmission:
    """Rate-limit arrivals, holding an overloaded burst until a quiet window."""

    def __init__(self, root: Path, window_ms: int, maximum: int) -> None:
        if not 1 <= window_ms <= 60000 or not 1 <= maximum <= 1000:
            raise ValueError("Burst window must be 1..60000 ms and maximum 1..1000")
        self.root = root
        self.window_ms = window_ms
        self.maximum = maximum
        path = root / ".admission.json"
        self.state = json.loads(path.read_text()) if path.exists() else {}

    def admit(
        self, record: dict, observed_ms: int, capacity: bool = True
    ) -> dict | None:
        route = record["route"]
        previous = self.state.get(route)
        if previous is None or observed_ms - previous["last"] >= 4 * self.window_ms:
            previous = {
                "last": observed_ms,
                "arrivals": [],
                "burst": str(uuid.uuid4()),
                "overloaded": False,
            }
        previous["last"] = observed_ms
        previous["arrivals"] = [
            t for t in previous["arrivals"] if observed_ms - t < self.window_ms
        ]
        overflow = (
            not capacity
            or previous["overloaded"]
            or len(previous["arrivals"]) >= self.maximum
        )
        notice = None
        if overflow:
            record.update(state="held", burstId=previous["burst"])
            # Held files need no second full-size archive. Unhold verifies and
            # snapshots the still-present original before submitting anything.
            Path(record["path"]).unlink()
            atomic_json(Path(record["path"]).parent / "record.json", record)
            if not previous["overloaded"]:
                notice = {
                    "version": 1,
                    "id": previous["burst"],
                    "route": route,
                    "target": record["target"],
                    "state": "pending",
                    "kind": "overload",
                    "createdAt": time.time(),
                    "text": f"Many files were uploaded, potentially unintentionally. Excess uploads are held and will not be sent automatically. Inspect record.json files under {self.root / 'delivered' / route} with state 'held' and burstId '{previous['burst']}' to find their originalPath values. Do not unhold them without an explicit request.",
                }
                directory = self.root / "delivered" / route / notice["id"]
                directory.mkdir()
                atomic_json(directory / "record.json", notice)
            previous["overloaded"] = True
        else:
            previous["arrivals"].append(observed_ms)
        self.state[route] = previous
        atomic_json(self.root / ".admission.json", self.state)
        return notice


class DeliveryWorker:
    """Observe arrivals independently of slow preparation and acceptance acks."""

    def __init__(
        self,
        root: Path,
        emit,
        *,
        native: bool,
        ya_stdio: bool,
        window_ms: int,
        maximum: int,
    ) -> None:
        self.root = root
        self.emit = emit
        self.native = native
        self.ya_stdio = ya_stdio
        self.admission = BurstAdmission(root, window_ms, maximum)
        self.slots = threading.BoundedSemaphore(maximum)
        self.queue = queue.Queue(maxsize=maximum + MAX_ROUTES)
        self.error: Exception | None = None
        self.thread = threading.Thread(
            target=self.run, name="rendez-delivery", daemon=True
        )
        self.thread.start()

    def submit(self, record: dict, observed_ms: int) -> None:
        self.check()
        capacity = self.slots.acquire(blocking=False)
        if record["state"] == "pending" and record.get("kind") != "overload":
            notice = self.admission.admit(record, observed_ms, capacity)
            if record["state"] == "held":
                if capacity:
                    self.slots.release()
                if notice:
                    self.queue.put_nowait((notice, False))
                return
        if not capacity and record.get("kind") != "overload":
            raise RuntimeError(
                "Rendezvous reconciliation exceeds the outstanding-delivery limit"
            )
        self.queue.put_nowait((record, capacity))

    def check(self) -> None:
        if self.error:
            raise RuntimeError(
                f"Rendezvous delivery worker failed: {self.error}"
            ) from self.error

    def run(self) -> None:
        try:
            while True:
                item = self.queue.get()
                if item is None:
                    return
                record, reserved = item
                try:
                    path = (
                        self.root
                        / "delivered"
                        / record["route"]
                        / record["id"]
                        / "record.json"
                    )
                    self.emit(deliver(path, native=self.native, ya_stdio=self.ya_stdio))
                finally:
                    if reserved:
                        self.slots.release()
        except Exception as exc:
            LOGGER.exception("Rendezvous delivery worker failed")
            self.error = exc

    def close(self) -> None:
        self.check()
        self.queue.put(None)
        self.thread.join()
        self.check()


def route_name(value: str) -> str:
    if (
        not value
        or value.startswith(".")
        or len(value) > 160
        or any(
            c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"
            for c in value
        )
    ):
        raise ValueError(
            "Rendezvous route must contain only letters, digits, underscores, or hyphens"
        )
    if value in {"latest-session", "delivered", "routes"}:
        raise ValueError("Rendezvous route name is reserved")
    return value


def initialize(project: Path) -> Path:
    project = project.resolve(strict=True)
    root = project / ".rendez"
    if root.is_symlink():
        raise ValueError("Rendezvous root must not be a symlink")
    if not root.exists():
        git = subprocess.run(
            ["git", "-C", str(project), "rev-parse", "--git-path", "info/exclude"],
            capture_output=True,
            text=True,
            check=False,
        )
        if git.returncode == 0:
            tracked = subprocess.run(
                ["git", "-C", str(project), "ls-files", "--", ".rendez"],
                capture_output=True,
                text=True,
                check=True,
            )
            if tracked.stdout:
                raise ValueError("Rendezvous root contains tracked files")
            exclude = Path(git.stdout.strip())
            if not exclude.is_absolute():
                exclude = project / exclude
            prefix = subprocess.run(
                ["git", "-C", str(project), "rev-parse", "--show-prefix"],
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip()
            pattern = f"/{prefix}.rendez/"
            exclude.parent.mkdir(parents=True, exist_ok=True)
            with exclude.open("a+") as handle:
                fcntl.flock(handle, fcntl.LOCK_EX)
                handle.seek(0)
                contents = handle.read()
                if pattern not in contents.splitlines():
                    handle.write(
                        ("\n" if contents and not contents.endswith("\n") else "")
                        + pattern
                        + "\n"
                    )
        elif "not a git repository" not in git.stderr.lower():
            raise RuntimeError(
                f"Cannot inspect rendezvous Git exclusion: {git.stderr.strip()}"
            )
        root.mkdir(mode=0o700, exist_ok=True)
        if root.is_symlink():
            raise ValueError("Rendezvous root must not be a symlink")
    for name in ("routes", "delivered"):
        child = root / name
        if child.is_symlink():
            raise ValueError(f"Rendezvous {name} must not be a symlink")
        child.mkdir(exist_ok=True)
    return root


def subscribe(
    project: Path,
    target: dict,
    route: str | None = None,
    *,
    latest: bool = False,
    received_at: int | None = None,
) -> dict:
    root = initialize(project)
    name = route_name(route or target.get("yaSessionId") or target["providerSessionId"])
    if target["harness"] not in {"claude", "codex"} or not target["providerSessionId"]:
        raise ValueError(
            "Rendezvous delivery currently supports Claude and Codex sessions"
        )
    with file_lock(root / ".lock"):
        directory = root / "routes" / name
        if directory.is_symlink():
            raise ValueError("Rendezvous route must not be a symlink")
        directory.mkdir(exist_ok=True)
        inbox = directory / "inbox"
        if inbox.is_symlink():
            raise ValueError("Rendezvous inbox must not be a symlink")
        inbox.mkdir(exist_ok=True)
        record = {
            "version": 1,
            "route": name,
            "project": str(project.resolve()),
            "target": target,
        }
        existing = directory / "subscription.json"
        if existing.exists():
            previous = json.loads(existing.read_text())["target"]
            if any(
                previous.get(key) != target.get(key)
                for key in ("harness", "providerSessionId", "yaSessionId")
            ):
                raise ValueError("Rendezvous route already belongs to another target")
        atomic_json(existing, record)
        alias = root / name
        if alias.is_symlink() and os.readlink(alias) != str(
            Path("routes") / name / "inbox"
        ):
            raise ValueError("Rendezvous named destination points to another directory")
        if not alias.is_symlink() and alias.exists():
            raise ValueError("Rendezvous named destination already exists")
        if not alias.is_symlink():
            alias.symlink_to(Path("routes") / name / "inbox", target_is_directory=True)
        if latest:
            timestamp = (
                received_at if received_at is not None else time.time_ns() // 1_000_000
            )
            latest_record = root / "latest.json"
            previous_time = (
                json.loads(latest_record.read_text())["receivedAt"]
                if latest_record.exists()
                else -1
            )
            if timestamp < previous_time:
                return {**record, "path": str(inbox)}
            link = root / f".latest-{uuid.uuid4()}"
            link.symlink_to(Path("routes") / name / "inbox", target_is_directory=True)
            link.replace(root / "latest-session")
            atomic_json(latest_record, {"route": name, "receivedAt": timestamp})
    return {**record, "path": str(inbox)}


def note_user_turn(
    project: Path, target: dict, origin: str, received_at: int | None = None
) -> None:
    if origin == "user" and (project / ".rendez").is_dir():
        subscribe(project, target, latest=True, received_at=received_at)


def routes(root: Path) -> list[Path]:
    result = []
    for item in (root / "routes").iterdir():
        if (
            item.is_dir()
            and not item.is_symlink()
            and (item / "subscription.json").is_file()
        ):
            result.append(item)
            if len(result) > MAX_ROUTES:
                raise RuntimeError(
                    f"Rendezvous exceeds the {MAX_ROUTES}-route observer limit"
                )
    return result


def snapshot(root: Path, route: Path, source: Path) -> dict | None:
    if source.name.startswith(".") or source.is_symlink() or not source.is_file():
        return None
    if source.stat().st_size > MAX_UPLOAD_BYTES:
        raise ValueError(
            f"Rendezvous upload exceeds {MAX_UPLOAD_BYTES} bytes: {source}"
        )
    target = json.loads((route / "subscription.json").read_text())["target"]
    directory = root / "delivered" / route.name
    if directory.is_symlink():
        raise ValueError("Rendezvous delivery directory must not be a symlink")
    directory.mkdir(exist_ok=True)
    scratch = directory / f".capture-{uuid.uuid4()}"
    scratch.mkdir()
    suffix = source.suffix if source.suffix[1:].isalnum() else ""
    copied = scratch / ("file" + suffix)
    try:
        digest = hashlib.sha256()
        with source.open("rb") as src, copied.open("xb") as dst:
            before = os.fstat(src.fileno())
            for chunk in iter(lambda: src.read(1024 * 1024), b""):
                if dst.tell() + len(chunk) > MAX_UPLOAD_BYTES:
                    raise ValueError("Rendezvous upload grew beyond the byte limit")
                digest.update(chunk)
                dst.write(chunk)
            after = os.fstat(src.fileno())
            dst.flush()
            os.fsync(dst.fileno())
        if (before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (
            after.st_size,
            after.st_mtime_ns,
            after.st_ctime_ns,
        ):
            return None
        sha = digest.hexdigest()
        event_id = str(
            uuid.uuid5(uuid.NAMESPACE_URL, f"{root}/{route.name}/{source.name}/{sha}")
        )
        destination = directory / event_id
        with file_lock(root / ".lock"):
            if destination.exists():
                return None
            record = {
                "version": 1,
                "id": event_id,
                "route": route.name,
                "target": target,
                "originalName": source.name,
                "originalPath": str(source),
                "sha256": sha,
                "path": str(destination / copied.name),
                "state": "pending",
                "createdAt": time.time(),
                "mimeType": mimetypes.guess_type(source.name)[0]
                or "application/octet-stream",
            }
            atomic_json(scratch / "record.json", record)
            scratch.rename(destination)
            return record
    finally:
        if scratch.exists():
            shutil.rmtree(scratch)


def deliver(
    record_path: Path,
    *,
    native: bool = False,
    ya_stdio: bool = False,
    unhold: bool = False,
) -> dict:
    with file_lock(record_path.parent / ".delivery.lock", blocking=False):
        record = json.loads(record_path.read_text())
        if unhold:
            if record["state"] != "held":
                raise ValueError("Only held uploads can be explicitly unheld")
            source = Path(record["originalPath"])
            destination = Path(record["path"])
            digest = hashlib.sha256()
            with source.open("rb") as handle, destination.open("wb") as output:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    if output.tell() + len(chunk) > MAX_UPLOAD_BYTES:
                        raise ValueError("Held original exceeds the upload byte limit")
                    output.write(chunk)
                    digest.update(chunk)
            if digest.hexdigest() != record["sha256"]:
                destination.unlink()
                raise ValueError(
                    "Held original was overwritten; upload it under a new name instead"
                )
            record["state"] = "pending"
            atomic_json(record_path, record)
        return _deliver(record_path, native=native, ya_stdio=ya_stdio)


def _deliver(record_path: Path, *, native: bool, ya_stdio: bool) -> dict:
    record = json.loads(record_path.read_text())
    if record["state"] in {"accepted", "held"}:
        return record
    api = runpy.run_path(str(CODE_ROOT / "scripts/session-turn"))
    if record["state"] in {"uncertain", "attempting"}:
        if record.get("transport") in {"native", "ya"}:
            record.update(
                state="uncertain",
                diagnostics="Acceptance is uncertain; inspect the target transcript before another upload",
            )
        else:
            try:
                descriptor, token = api["discover_provider_host"]()
                status = api["host_request"](
                    descriptor,
                    token,
                    {
                        "op": "sessionTurnStatus",
                        "submissionId": record["id"],
                    },
                )
                record.update(
                    state="accepted"
                    if status and status.get("accepted")
                    else "uncertain",
                    receipt=status,
                )
            except api["TransportFailure"] as exc:
                record.update(state="uncertain", diagnostics=str(exc))
        atomic_json(record_path, record)
        return record
    target = record["target"]
    if "prepared" not in record and record.get("kind") != "overload":
        try:
            profile = attachment_profile(target, api)
            prepared = prepare_attachment(
                Path(record["path"]), record["mimeType"], profile
            )
        except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
            record.update(
                state="failed", diagnostics=f"Image preparation failed: {exc}"
            )
            atomic_json(record_path, record)
            return record
        record.update(prepared)
        record["prepared"] = True
        atomic_json(record_path, record)
    if record.get("kind") == "overload":
        body = record["text"]
    else:
        size = record["size"]
        dimensions = (
            f", {record['width']}x{record['height']}" if "width" in record else ""
        )
        name = (
            record["originalName"]
            .replace("[", "\\[")
            .replace("]", "\\]")
            .replace("\n", " ")
        )
        body = f"Please inspect the uploaded file.\n\nUser uploaded files:\n- [{name}](<{record['path']}>) ({size} B, {record['mimeType']}{dimensions})"
    if ya_stdio:
        record.update(state="attempting", transport="ya")
        atomic_json(record_path, record)
        print(
            json.dumps({"type": "delivery-request", "record": record, "text": body}),
            flush=True,
        )
        try:
            if not select.select([sys.stdin], [], [], 30)[0]:
                raise RuntimeError(
                    "YA did not acknowledge the upload within 30 seconds"
                )
            reply = json.loads(sys.stdin.readline())
            if reply.get("id") != record["id"]:
                raise ValueError("YA upload acknowledgement has the wrong id")
            if reply.get("provider") is not True:
                record.update(
                    state="accepted" if reply.get("accepted") is True else "failed",
                    receipt=reply,
                )
                atomic_json(record_path, record)
                return record
        except (OSError, ValueError, RuntimeError) as exc:
            record.update(state="uncertain", diagnostics=str(exc))
            atomic_json(record_path, record)
            return record
    argv = [sys.executable, str(CODE_ROOT / "scripts/session-turn")]
    if not native:
        argv.append("send")
    argv += [
        target["harness"],
        target["providerSessionId"],
        "--origin",
        "rendezvous",
        "--submission-id",
        record["id"],
        "--cwd",
        str(record_path.parents[4]),
    ]
    if not native:
        argv.append("--eventual")
        if target.get("liveOnly"):
            argv.append("--live-only")
    elif target.get("liveOnly"):
        raise ValueError("Native delivery cannot enforce awake-only admission")
    if target.get("yaSessionId"):
        argv += ["--ya-session-id", target["yaSessionId"]]
    record["state"] = "attempting"
    record["transport"] = "native" if native else "provider-host"
    atomic_json(record_path, record)
    try:
        result = subprocess.run(
            argv,
            input=body,
            text=True,
            capture_output=True,
            timeout=1810 if native else 30,
            check=False,
        )
        rows = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
        accepted = any(row.get("type") == "accepted" for row in rows)
        record.update(
            state="accepted"
            if accepted or result.returncode == 0
            else "failed"
            if result.returncode == 11
            else "uncertain",
            diagnostics=result.stderr[-4000:],
            receipt=rows[-1] if rows else None,
        )
    except (OSError, subprocess.TimeoutExpired, ValueError) as exc:
        record.update(state="uncertain", diagnostics=str(exc))
    atomic_json(record_path, record)
    return record


def discover_pending(root: Path) -> Iterator[dict]:
    pending = []
    for route in (root / "delivered").iterdir():
        if not route.is_dir() or route.is_symlink():
            continue
        for event in route.iterdir():
            if event.name.startswith("."):
                continue
            path = event / "record.json"
            if not path.is_file():
                continue
            record = json.loads(path.read_text())
            if record["state"] in {
                "pending",
                "attempting",
                "uncertain",
            }:
                pending.append(record)
                if len(pending) > MAX_FILES:
                    raise RuntimeError(
                        "Rendezvous pending records exceed the scan limit"
                    )
    yield from pending
    count = 0
    for route in routes(root):
        for source in (route / "inbox").iterdir():
            count += 1
            if count > MAX_FILES:
                raise RuntimeError(
                    f"Rendezvous exceeds the {MAX_FILES}-file scan limit"
                )
            record = snapshot(root, route, source)
            if record:
                yield record


def scan(
    root: Path,
    *,
    native: bool = False,
    ya_stdio: bool = False,
    window_ms: int = DEFAULT_WINDOW_MS,
    maximum: int = DEFAULT_MAX_PER_WINDOW,
) -> list[dict]:
    results = []
    observed = time.time_ns() // 1_000_000
    worker = DeliveryWorker(
        root,
        results.append,
        native=native,
        ya_stdio=ya_stdio,
        window_ms=window_ms,
        maximum=maximum,
    )
    try:
        for record in discover_pending(root):
            worker.submit(record, observed)
    finally:
        worker.close()
    return results


def watch(
    root: Path,
    emit,
    *,
    native: bool = False,
    ya_stdio: bool = False,
    window_ms: int = DEFAULT_WINDOW_MS,
    maximum: int = DEFAULT_MAX_PER_WINDOW,
) -> None:
    if sys.platform != "linux":
        raise RuntimeError(
            "Rendezvous watching requires Linux inotify; use scan for completed transfers elsewhere"
        )
    libc = ctypes.CDLL(None, use_errno=True)
    fd = libc.inotify_init1(os.O_NONBLOCK | os.O_CLOEXEC)
    if fd < 0:
        raise OSError(ctypes.get_errno(), "Cannot initialize rendezvous inotify")
    watched: dict[int, Path] = {}
    try:
        with file_lock(root / ".observer.lock", blocking=False):
            # One control watch plus at most MAX_ROUTES input watches.
            control = libc.inotify_add_watch(
                fd, os.fsencode(root / "routes"), 0x100 | 0x80
            )
            if control < 0:
                raise OSError(ctypes.get_errno(), "Cannot watch rendezvous routes")
            emit({"state": "watching", "project": str(root.parent)})
            worker = DeliveryWorker(
                root,
                emit,
                native=native,
                ya_stdio=ya_stdio,
                window_ms=window_ms,
                maximum=maximum,
            )
            initial_scan = True
            while True:
                worker.check()
                new_routes = []
                for route in routes(root):
                    if route in watched.values():
                        continue
                    wd = libc.inotify_add_watch(
                        fd, os.fsencode(route / "inbox"), 0x8 | 0x80
                    )
                    if wd < 0:
                        raise OSError(
                            ctypes.get_errno(), "Cannot watch rendezvous inbox"
                        )
                    watched[wd] = route
                    new_routes.append(route)
                if initial_scan:
                    observed = time.time_ns() // 1_000_000
                    for record in discover_pending(root):
                        worker.submit(record, observed)
                    initial_scan = False
                else:
                    for route in new_routes:
                        observed = time.time_ns() // 1_000_000
                        for count, source in enumerate((route / "inbox").iterdir(), 1):
                            if count > MAX_FILES:
                                raise RuntimeError(
                                    "Rendezvous inbox exceeds the file scan limit"
                                )
                            record = snapshot(root, route, source)
                            if record:
                                worker.submit(record, observed)
                if not select.select([fd], [], [], 5)[0]:
                    continue
                data = os.read(fd, 65536)
                observed = time.time_ns() // 1_000_000
                offset = 0
                while offset < len(data):
                    wd, mask, _cookie, length = struct.unpack_from("iIII", data, offset)
                    offset += 16
                    name = os.fsdecode(
                        data[offset : offset + length].split(b"\0", 1)[0]
                    )
                    offset += length
                    if mask & 0x4000:
                        raise RuntimeError(
                            "Rendezvous watcher overflow; run scan after transfers complete"
                        )
                    if mask & 0x8000:
                        watched.pop(wd, None)
                        continue
                    if wd in watched and name and not mask & 0x40000000:
                        record = snapshot(
                            root, watched[wd], watched[wd] / "inbox" / name
                        )
                        if record:
                            worker.submit(record, observed)
    finally:
        os.close(fd)
