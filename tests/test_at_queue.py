#!/usr/bin/env python3
"""Behavior tests for scripts/at-queue."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "at-queue"

PAST = "2020-01-01T00:00:00Z"
FUTURE = "2030-01-02T03:04:05Z"


def _assert(condition, message="assertion failed"):
    if not condition:
        raise AssertionError(message)


def _project(*, git: bool = False) -> Path:
    root = Path(tempfile.mkdtemp(prefix="at-queue-test-"))
    if git:
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "t@t"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "t"], cwd=root, check=True)
    return root


def _source(root: Path, name: str, body: str = "Run it.") -> Path:
    queue = root / "at"
    queue.mkdir(exist_ok=True)
    path = queue / f"{name}.md"
    path.write_text(f"---\nname: {name}\n---\n\n{body}\n")
    return path


def _claim(root: Path, session: str, pid: int | None = None):
    return _run(
        root,
        "claim",
        "--session",
        session,
        "--owner-pid",
        str(os.getpid() if pid is None else pid),
    )


def _run(root: Path, *args: str):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args, "--root", str(root)],
        capture_output=True,
        text=True,
        check=False,
    )


def _json(proc):
    return json.loads(proc.stdout)


def _activation(root: Path) -> Path:
    return root / ".yep" / "at-activation.json"


def test_activation_is_separate_from_source():
    root = _project()
    source = _source(root, "review")
    before = source.read_text()
    proc = _run(root, "activate", "--job", "review", "--run-after", FUTURE)
    _assert(proc.returncode == 0, proc.stderr)

    _assert(source.read_text() == before, "activating must not rewrite the prompt")
    state = json.loads(_activation(root).read_text())
    _assert(state["jobs"]["review"]["run_after"] == FUTURE, state)
    _assert("run_after" not in before, "schedule never lives in the source file")


def test_claim_skips_future_and_takes_due():
    root = _project()
    _source(root, "later")
    _source(root, "now")
    _run(root, "activate", "--job", "later", "--run-after", FUTURE)
    _run(root, "activate", "--job", "now", "--run-after", PAST)

    proc = _claim(root, "session-a")
    _assert(proc.returncode == 0, proc.stderr)
    payload = _json(proc)
    _assert(payload["job"] == "now", payload)
    _assert(payload["skipped"]["later"] == "not due", payload)


def test_claim_is_single_winner_while_runner_is_alive():
    root = _project()
    _source(root, "solo")
    _run(root, "activate", "--job", "solo", "--run-after", PAST)

    first = _claim(root, "a")
    _assert(first.returncode == 0, first.stderr)
    second = _claim(root, "b")
    _assert(second.returncode == 3, second.stdout)
    _assert(_json(second)["skipped"]["solo"] == "already running", second.stdout)


def test_dead_runner_releases_the_job_without_a_heartbeat():
    root = _project()
    _source(root, "orphan")
    _run(root, "activate", "--job", "orphan", "--run-after", PAST)

    dead = subprocess.Popen([sys.executable, "-c", "pass"])
    dead.wait()
    claimed = _claim(root, "a", dead.pid)
    _assert(claimed.returncode == 0, claimed.stderr)

    again = _claim(root, "b")
    _assert(again.returncode == 0, "an exited runner must not hold the job forever")
    _assert(_json(again)["job"] == "orphan", again.stdout)


def test_done_reschedules_or_parks():
    root = _project()
    _source(root, "periodic")
    _run(root, "activate", "--job", "periodic", "--run-after", PAST)
    _claim(root, "a")

    proc = _run(root, "done", "--job", "periodic", "--run-after", FUTURE)
    _assert(
        proc.returncode == 0 and _json(proc)["status"] == "rescheduled", proc.stdout
    )
    _assert(_claim(root, "b").returncode == 3, "no longer due")

    _run(root, "activate", "--job", "periodic", "--run-after", PAST)
    _claim(root, "c")
    proc = _run(root, "done", "--job", "periodic", "--park")
    _assert(proc.returncode == 0 and _json(proc)["status"] == "parked", proc.stdout)
    entry = json.loads(_activation(root).read_text())["jobs"]["periodic"]
    _assert(entry["enabled"] is False and entry["run_after"] is None, entry)


def test_done_requires_an_explicit_disposition():
    root = _project()
    _source(root, "ambiguous")
    _run(root, "activate", "--job", "ambiguous", "--run-after", PAST)
    proc = _run(root, "done", "--job", "ambiguous")
    _assert(proc.returncode == 4, proc.stdout)
    _assert("--park" in _json(proc)["error"], proc.stdout)


def test_pause_blocks_claiming_without_forgetting_the_schedule():
    root = _project()
    _source(root, "sleepy")
    _run(root, "activate", "--job", "sleepy", "--run-after", PAST)
    _assert(_run(root, "pause", "--job", "sleepy").returncode == 0)

    proc = _claim(root, "a")
    _assert(proc.returncode == 3 and _json(proc)["skipped"]["sleepy"] == "paused")
    _assert(json.loads(_activation(root).read_text())["jobs"]["sleepy"]["run_after"])

    _assert(_run(root, "resume", "--job", "sleepy").returncode == 0)
    _assert(_claim(root, "a").returncode == 0)


def test_changed_prompt_blocks_the_claim_until_reactivated():
    root = _project()
    source = _source(root, "drifting")
    _run(root, "activate", "--job", "drifting", "--run-after", PAST)
    source.write_text("---\nname: drifting\n---\n\nSomething else entirely.\n")

    proc = _claim(root, "a")
    _assert(proc.returncode == 3, proc.stdout)
    _assert("re-activate" in _json(proc)["skipped"]["drifting"], proc.stdout)

    _run(root, "activate", "--job", "drifting", "--run-after", PAST)
    _assert(_claim(root, "a").returncode == 0)


def test_tracked_activation_is_refused():
    root = _project(git=True)
    _source(root, "tracked")
    _run(root, "activate", "--job", "tracked", "--run-after", PAST)
    subprocess.run(
        ["git", "add", "-f", ".yep/at-activation.json"], cwd=root, check=True
    )

    for verb in (
        ["list"],
        ["claim", "--session", "a", "--owner-pid", str(os.getpid())],
    ):
        proc = _run(root, *verb)
        _assert(proc.returncode == 4, f"{verb} must refuse tracked activation")
        _assert("clone-local" in _json(proc)["error"], proc.stdout)


def test_hand_edited_activation_is_reported():
    root = _project()
    _source(root, "edited")
    _run(root, "activate", "--job", "edited", "--run-after", PAST)
    path = _activation(root)
    path.write_text(json.dumps(json.loads(path.read_text())))  # compact, not canonical

    proc = _run(root, "list")
    _assert(proc.returncode == 0, proc.stderr)
    _assert("not written by at-queue" in _json(proc)["warnings"][0], proc.stdout)


def test_stale_lock_is_broken_but_a_live_one_is_not():
    root = _project()
    _source(root, "locked")
    lock = _activation(root).parent / "at-activation.json.lock"
    lock.mkdir(parents=True)

    proc = _run(root, "activate", "--job", "locked", "--run-after", PAST)
    _assert(proc.returncode == 4, "a fresh lock must not be stolen")

    os.utime(lock, (0, 0))
    proc = _run(root, "activate", "--job", "locked", "--run-after", PAST)
    _assert(proc.returncode == 0, "a lock older than the critical section is debris")


def test_missing_source_is_refused_and_never_claimed():
    root = _project()
    source = _source(root, "vanishing")
    _run(root, "activate", "--job", "vanishing", "--run-after", PAST)
    source.unlink()

    proc = _claim(root, "a")
    _assert(proc.returncode == 3, proc.stdout)
    _assert(_json(proc)["skipped"]["vanishing"] == "prompt source is missing")
    _assert(
        _run(root, "activate", "--job", "gone", "--run-after", PAST).returncode == 4
    )


def test_claim_demands_provable_liveness():
    root = _project()
    _source(root, "unproven")
    _run(root, "activate", "--job", "unproven", "--run-after", PAST)

    proc = _run(root, "claim", "--session", "a")
    _assert(proc.returncode == 2, "exclusion without an owner pid must not be silent")
    _assert("--owner-pid" in proc.stderr, proc.stderr)


def test_absent_queue_and_activation_are_not_created():
    root = _project()
    proc = _claim(root, "a")
    _assert(proc.returncode == 3, proc.stdout)
    _assert(not _activation(root).exists(), "claiming nothing writes no state")
    _assert(not (root / "at").exists(), "an absent at/ is never created")


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
