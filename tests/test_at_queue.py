#!/usr/bin/env python3
"""Behavior tests for scripts/at-queue."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
import traceback
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "at-queue"


def _assert(condition, message="assertion failed"):
    if not condition:
        raise AssertionError(message)


def _stamp(text: str) -> float:
    return datetime.fromisoformat(text.replace("Z", "+00:00")).timestamp()


def _job(root: Path, name: str, run_after: str | None) -> Path:
    queue = root / "at"
    queue.mkdir()
    path = queue / f"{name}.md"
    value = "null" if run_after is None else run_after
    path.write_text(f"---\nrun_after: {value}\n---\n\nRun {name}.\n")
    if run_after is not None:
        os.utime(path, (_stamp(run_after), _stamp(run_after)))
    return path


def _run(root: Path, *args: str):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args, "--root", str(root)],
        capture_output=True,
        text=True,
        check=False,
    )


def test_claim_repairs_future_mtime_without_claiming():
    root = Path(tempfile.mkdtemp(prefix="at-queue-test-"))
    future = "2030-01-02T03:04:05Z"
    job = _job(root, "future", future)
    os.utime(job, (time.time() - 5, time.time() - 5))

    result = _run(root, "claim", "--session", "session-a")
    _assert(result.returncode == 3, result.stderr)
    payload = json.loads(result.stdout)
    _assert(
        payload["status"] == "none" and payload["repaired"] == ["future.md"],
        payload,
    )
    _assert(job.stat().st_mtime_ns == int(_stamp(future) * 1_000_000_000))
    _assert(not (root / "at/.locks/future.lock").exists())


def test_claim_does_not_create_absent_queue():
    root = Path(tempfile.mkdtemp(prefix="at-queue-test-"))
    result = _run(root, "claim", "--session", "session-a")
    _assert(result.returncode == 3, result.stderr)
    _assert(json.loads(result.stdout)["reason"] == "no at directory")
    _assert(not (root / "at").exists())


def test_claim_is_single_winner_and_records_owner_identity():
    root = Path(tempfile.mkdtemp(prefix="at-queue-test-"))
    _job(root, "due", "2020-01-01T00:00:00Z")

    result = _run(
        root,
        "claim",
        "--session",
        "session-a",
        "--harness",
        "codex",
        "--owner-pid",
        str(os.getpid()),
    )
    _assert(result.returncode == 0, result.stderr)
    payload = json.loads(result.stdout)
    _assert(payload["status"] == "claimed" and payload["job"].endswith("due.md"))
    owner = (root / "at/.locks/due.lock/owner.md").read_text()
    _assert("session-a" in owner and "harness: codex" in owner, owner)
    _assert("process_start_ticks:" in owner, owner)

    second = _run(root, "claim", "--session", "session-b")
    _assert(second.returncode == 3, second.stderr)
    _assert(json.loads(second.stdout)["status"] == "none")


def test_claim_recovers_lock_after_verified_acknowledgement():
    root = Path(tempfile.mkdtemp(prefix="at-queue-test-"))
    job = _job(root, "once", "2020-01-01T00:00:00Z")
    claimed = _run(root, "claim", "--session", "session-a")
    _assert(claimed.returncode == 0, claimed.stderr)

    job.write_text("---\nrun_after: null\n---\n\nRun once.\n")
    parked = _stamp("2030-01-01T00:00:00Z")
    os.utime(job, (parked, parked))
    recovered = _run(root, "claim", "--session", "session-b")
    _assert(recovered.returncode == 3, recovered.stderr)
    _assert(json.loads(recovered.stdout)["recovered"] == ["once.md"])
    _assert(not (root / "at/.locks/once.lock").exists())


def test_due_ownerless_lock_remains_ambiguous():
    root = Path(tempfile.mkdtemp(prefix="at-queue-test-"))
    _job(root, "ambiguous", "2020-01-01T00:00:00Z")
    (root / "at/.locks/ambiguous.lock").mkdir(parents=True)

    result = _run(root, "claim", "--session", "session-a")
    _assert(result.returncode == 3, result.stderr)
    _assert((root / "at/.locks/ambiguous.lock").is_dir())


def test_finish_refuses_due_job_then_releases_verified_schedule():
    root = Path(tempfile.mkdtemp(prefix="at-queue-test-"))
    job = _job(root, "periodic", "2020-01-01T00:00:00Z")
    claimed = _run(root, "claim", "--session", "session-a")
    _assert(claimed.returncode == 0, claimed.stderr)

    blocked = _run(root, "finish", "--job", job.name)
    _assert(blocked.returncode == 70, blocked.stdout)
    _assert((root / "at/.locks/periodic.lock").is_dir())

    future = "2030-02-03T04:05:06Z"
    job.write_text(f"---\nrun_after: {future}\n---\n\nRun periodically.\n")
    os.utime(job, (_stamp(future), _stamp(future)))
    released = _run(root, "finish", "--job", job.name)
    _assert(released.returncode == 0, released.stdout)
    _assert(not (root / "at/.locks/periodic.lock").exists())


def _collect_tests():
    return [
        (name, fn)
        for name, fn in sorted(globals().items())
        if name.startswith("test_") and callable(fn)
    ]


def main() -> int:
    passed = failed = 0
    failures = []
    for name, fn in _collect_tests():
        try:
            fn()
            passed += 1
            print(".", end="", flush=True)
        except Exception:
            failed += 1
            failures.append((name, traceback.format_exc()))
            print("F", end="", flush=True)
    print("\n")
    for name, trace in failures:
        print(f"--- {name} ---\n{trace}")
    print(f"{passed} passed, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
