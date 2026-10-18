"""Filesystem rendezvous subscriptions and immutable delivered snapshots."""

from __future__ import annotations

import ctypes
import errno
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
import socket
import struct
import subprocess
import sys
import threading
import time
import uuid
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from pathlib import Path

from agentctl_coordination import atomic_json
from session_attachments import attachment_profile, prepare_attachment

MAX_ROUTES = 128
MAX_FILES = 10000
MAX_UPLOAD_BYTES = 64 * 1024 * 1024
CODE_ROOT = Path(__file__).resolve().parent
DEFAULT_WINDOW_MS = 1000
DEFAULT_MAX_PER_WINDOW = 10
LATEST_PASSES = 8
LOGGER = logging.getLogger(__name__)

# A delivery takes a record.json path and returns the updated record to emit,
# or None when it already emitted the delivery itself.
Delivery = Callable[[Path], "dict | None"]


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
        # Observers do not lock this file; a second concurrent observer can
        # only miscount arrivals, never duplicate or redirect a delivery.
        atomic_json(self.root / ".admission.json", self.state)
        return notice


class DeliveryWorker:
    """Observe arrivals independently of slow preparation and acceptance acks."""

    def __init__(
        self,
        root: Path,
        emit,
        delivery: Delivery,
        *,
        window_ms: int,
        maximum: int,
    ) -> None:
        self.root = root
        self.emit = emit
        self.delivery = delivery
        self.admission = BurstAdmission(root, window_ms, maximum)
        self.slots = threading.BoundedSemaphore(maximum)
        # Sends are bounded by the slots; receipt checks by the scan limit.
        self.queue = queue.Queue()
        self.error: Exception | None = None
        self.thread = threading.Thread(
            target=self.run, name="rendez-delivery", daemon=True
        )
        self.thread.start()

    def submit(self, record: dict, observed_ms: int) -> None:
        self.check()
        if record["state"] != "pending" or record.get("kind") == "overload":
            # Receipt checks and overload notices need no outstanding-send slot.
            self.queue.put_nowait((record, False))
            return
        capacity = self.slots.acquire(blocking=False)
        notice = self.admission.admit(record, observed_ms, capacity)
        if notice:
            self.queue.put_nowait((notice, False))
        if record["state"] == "held":
            if capacity:
                self.slots.release()
            return
        self.queue.put_nowait((record, True))

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
                    result = self.delivery(record_path(self.root, record))
                    if result is not None:
                        self.emit(result)
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


def record_path(root: Path, record: dict) -> Path:
    return root / "delivered" / record["route"] / record["id"] / "record.json"


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
    if not target["harness"] or not target["providerSessionId"]:
        raise ValueError("Rendezvous subscriptions require a harness and session")
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
    try:
        alias.symlink_to(Path("routes") / name / "inbox", target_is_directory=True)
    except FileExistsError:
        if not alias.is_symlink():
            raise ValueError("Rendezvous named destination already exists") from None
        if os.readlink(alias) != str(Path("routes") / name / "inbox"):
            raise ValueError(
                "Rendezvous named destination points to another directory"
            ) from None
    if latest:
        publish_latest(
            root,
            name,
            received_at if received_at is not None else time.time_ns() // 1_000_000,
        )
    return {**record, "path": str(inbox)}


def publish_latest(root: Path, route: str, received_at: int) -> None:
    """Point latest-session at the route with the newest recorded user turn.

    Writers never lock. Each records its turn as an entry, moves the pointer to
    the newest entry, and repeats until a listing shows no newer arrival, so
    the last writer to look leaves the pointer correct. Fixed-width names sort
    by time, then route, identically for every writer.
    """
    entries = root / "latest.d"
    entries.mkdir(exist_ok=True)
    (entries / f"{received_at:016d}-{route}").touch()
    link = root / "latest-session"
    newest = None
    for _ in range(LATEST_PASSES):
        names = sorted(p.name for p in entries.iterdir() if not p.name.startswith("."))
        if names[-1] == newest:
            for name in names[:-1]:
                (entries / name).unlink(missing_ok=True)
            return
        newest = names[-1]
        want = str(Path("routes") / newest[17:] / "inbox")
        if not link.is_symlink() or os.readlink(link) != want:
            temporary = root / f".latest-{uuid.uuid4()}"
            temporary.symlink_to(want, target_is_directory=True)
            temporary.replace(link)
    raise RuntimeError("Rendezvous latest-session kept changing; retry the turn")


def note_user_turn(
    project: Path, target: dict, origin: str, received_at: int | None = None
) -> None:
    if origin == "user" and (project / ".rendez").is_dir():
        subscribe(project, target, latest=True, received_at=received_at)


def routes(root: Path, only: str | None = None) -> list[Path]:
    result = []
    for item in (root / "routes").iterdir():
        if (
            (only is None or item.name == only)
            and item.is_dir()
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
        # Renaming onto an existing, never-empty event directory fails, so
        # exactly one observer captures each upload without a lock.
        try:
            scratch.rename(destination)
        except OSError as exc:
            if exc.errno in {errno.EEXIST, errno.ENOTEMPTY}:
                return None
            raise
        return record
    finally:
        if scratch.exists():
            shutil.rmtree(scratch)


def claim(event: Path) -> bool:
    """Take the one-time right to send an event; a claim is never released."""
    try:
        with (event / "claim").open("x") as handle:
            json.dump(
                {"host": socket.gethostname(), "pid": os.getpid(), "at": time.time()},
                handle,
            )
    except FileExistsError:
        return False
    return True


def _start_time(pid: int) -> str | None:
    """Linux process start time, which tells a reused pid from its original."""
    try:
        stat = Path(f"/proc/{pid}/stat").read_text()
    except OSError:
        return None
    return stat[stat.rindex(")") + 2 :].split()[19]


def _alive(pid: int, start_time: str | None) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        pass
    return start_time is None or _start_time(pid) in {None, start_time}


@contextmanager
def project_observer(root: Path, owner: str) -> Iterator[None]:
    """Refuse to start a second project observer: YA or `watch --turns`.

    This is a startup conflict check, not a lock. A marker whose process is
    gone from this host is replaced; one from another host must be removed by
    hand, because its owner's liveness cannot be checked from here.
    """
    marker = root / ".observer.json"
    mine = {
        "owner": owner,
        "host": socket.gethostname(),
        "pid": os.getpid(),
        "startTime": _start_time(os.getpid()),
        "startedAt": time.time(),
    }
    temporary = root / f".observer-{uuid.uuid4()}"
    temporary.write_text(json.dumps(mine))
    try:
        for _ in range(2):
            try:
                os.link(temporary, marker)
                break
            except FileExistsError:
                try:
                    other = json.loads(marker.read_text())
                except (FileNotFoundError, ValueError):
                    other = {}
                if other.get("host") == mine["host"] and not _alive(
                    other.get("pid", 0), other.get("startTime")
                ):
                    marker.unlink(missing_ok=True)
                    continue
                raise RuntimeError(
                    f"Project {root.parent} is already observed by {other.get('owner', 'another observer')} "
                    f"(pid {other.get('pid')} on {other.get('host')}); stop it, or delete {marker} if it is gone"
                ) from None
        else:
            raise RuntimeError(f"Cannot create the rendezvous observer marker {marker}")
    finally:
        temporary.unlink()
    try:
        yield
    finally:
        try:
            if json.loads(marker.read_text()).get("pid") == mine["pid"]:
                marker.unlink()
        except (FileNotFoundError, ValueError):
            pass


def unhold(record_path: Path) -> dict:
    """Restore one held upload's snapshot so a delivery can send it."""
    record = json.loads(record_path.read_text())
    if record["state"] != "held":
        raise ValueError("Only held uploads can be explicitly unheld")
    if not claim(record_path.parent):
        raise ValueError("This held upload was already unheld")
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
    return record


def _admit(record_path: Path, claimed: bool) -> dict | None:
    """Return a pending record this caller may send, after preparing it."""
    record = json.loads(record_path.read_text())
    if record["state"] != "pending":
        return None
    if not claimed and not claim(record_path.parent):
        # A claimant that stopped before recording an outcome may or may not
        # have sent the upload; never send it a second time.
        record.update(
            state="uncertain",
            diagnostics="Another observer claimed this upload; inspect the target transcript before another upload",
        )
        atomic_json(record_path, record)
        return None
    if "prepared" not in record and record.get("kind") != "overload":
        api = runpy.run_path(str(CODE_ROOT / "scripts/session-turn"))
        try:
            profile = attachment_profile(record["target"], api)
            prepared = prepare_attachment(
                Path(record["path"]), record["mimeType"], profile
            )
        except (OSError, ValueError, RuntimeError) as exc:
            record.update(
                state="failed", diagnostics=f"Image preparation failed: {exc}"
            )
            atomic_json(record_path, record)
            return None
        record.update(prepared)
        record["prepared"] = True
        atomic_json(record_path, record)
    return record


def body(record: dict) -> str:
    if record.get("kind") == "overload":
        return record["text"]
    dimensions = f", {record['width']}x{record['height']}" if "width" in record else ""
    name = (
        record["originalName"]
        .replace("[", "\\[")
        .replace("]", "\\]")
        .replace("\n", " ")
    )
    return f"Please inspect the uploaded file.\n\nUser uploaded files:\n- [{name}](<{record['path']}>) ({record['size']} B, {record['mimeType']}{dimensions})"


def output_delivery(emit, *, claimed: bool = False) -> Delivery:
    """Deliver by printing to the observing session, which owns its route."""

    def deliver(record_path: Path) -> None:
        record = _admit(record_path, claimed)
        if record is None:
            record = json.loads(record_path.read_text())
            if record["state"] in {"failed", "uncertain"}:
                emit(record)
            return
        text = body(record)
        # Printing is the delivery; record acceptance only after it happened.
        emit({**record, "state": "accepted", "transport": "output", "text": text})
        record.update(state="accepted", transport="output")
        atomic_json(record_path, record)

    return deliver


def turn_delivery(*, native: bool = False, claimed: bool = False) -> Delivery:
    """Deliver each upload as a user turn to its subscribed session."""

    def deliver(record_path: Path) -> dict:
        record = json.loads(record_path.read_text())
        if record["state"] in {"uncertain", "attempting"}:
            return _reconcile(record_path, record)
        record = _admit(record_path, claimed)
        if record is None:
            return json.loads(record_path.read_text())
        return _send_turn(record_path, record, native)

    return deliver


def _reconcile(record_path: Path, record: dict) -> dict:
    if record.get("transport") in {"native", "ya", "output"}:
        record.update(
            state="uncertain",
            diagnostics="Acceptance is uncertain; inspect the target transcript before another upload",
        )
    else:
        api = runpy.run_path(str(CODE_ROOT / "scripts/session-turn"))
        try:
            descriptor, token = api["discover_provider_host"]()
            status = api["host_request"](
                descriptor,
                token,
                {"op": "sessionTurnStatus", "submissionId": record["id"]},
            )
            record.update(
                state="accepted" if status and status.get("accepted") else "uncertain",
                receipt=status,
            )
        except api["TransportFailure"] as exc:
            record.update(state="uncertain", diagnostics=str(exc))
    atomic_json(record_path, record)
    return record


def _send_turn(record_path: Path, record: dict, native: bool) -> dict:
    target = record["target"]
    if target["harness"] not in {"claude", "codex"}:
        record.update(
            state="failed",
            diagnostics="Rendezvous turn delivery supports Claude and Codex sessions",
        )
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
            input=body(record),
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


def discover_pending(root: Path, observed: list[Path]) -> Iterator[dict]:
    pending = []
    names = {route.name for route in observed}
    for route in (root / "delivered").iterdir():
        if route.name not in names or not route.is_dir() or route.is_symlink():
            continue
        for event in route.iterdir():
            if event.name.startswith("."):
                continue
            path = event / "record.json"
            if not path.is_file():
                continue
            record = json.loads(path.read_text())
            # Uncertain records stay so until someone inspects the transcript;
            # only a provider receipt can still settle one.
            if record["state"] in {"pending", "attempting"} or (
                record["state"] == "uncertain"
                and record.get("transport") == "provider-host"
            ):
                pending.append(record)
                if len(pending) > MAX_FILES:
                    raise RuntimeError(
                        "Rendezvous pending records exceed the scan limit"
                    )
    yield from pending
    count = 0
    for route in observed:
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
    emit,
    delivery: Delivery,
    *,
    only: str | None = None,
    window_ms: int = DEFAULT_WINDOW_MS,
    maximum: int = DEFAULT_MAX_PER_WINDOW,
) -> None:
    observed = time.time_ns() // 1_000_000
    worker = DeliveryWorker(root, emit, delivery, window_ms=window_ms, maximum=maximum)
    try:
        for record in discover_pending(root, routes(root, only)):
            worker.submit(record, observed)
    finally:
        worker.close()


def watch(
    root: Path,
    emit,
    delivery: Delivery,
    *,
    only: str | None = None,
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
        # One control watch plus at most MAX_ROUTES input watches.
        control = libc.inotify_add_watch(fd, os.fsencode(root / "routes"), 0x100 | 0x80)
        if control < 0:
            raise OSError(ctypes.get_errno(), "Cannot watch rendezvous routes")
        emit({"state": "watching", "project": str(root.parent)})
        worker = DeliveryWorker(
            root, emit, delivery, window_ms=window_ms, maximum=maximum
        )
        initial_scan = True
        while True:
            worker.check()
            new_routes = []
            for route in routes(root, only):
                if route in watched.values():
                    continue
                wd = libc.inotify_add_watch(
                    fd, os.fsencode(route / "inbox"), 0x8 | 0x80
                )
                if wd < 0:
                    raise OSError(ctypes.get_errno(), "Cannot watch rendezvous inbox")
                watched[wd] = route
                new_routes.append(route)
            if initial_scan:
                observed = time.time_ns() // 1_000_000
                for record in discover_pending(root, new_routes):
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
                name = os.fsdecode(data[offset : offset + length].split(b"\0", 1)[0])
                offset += length
                if mask & 0x4000:
                    raise RuntimeError(
                        "Rendezvous watcher overflow; run scan after transfers complete"
                    )
                if mask & 0x8000:
                    watched.pop(wd, None)
                    continue
                if wd in watched and name and not mask & 0x40000000:
                    record = snapshot(root, watched[wd], watched[wd] / "inbox" / name)
                    if record:
                        worker.submit(record, observed)
    finally:
        os.close(fd)
