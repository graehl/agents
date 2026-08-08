#!/usr/bin/env python3
"""Behavior tests for scripts/perf-sweep."""

from __future__ import annotations

import os
import secrets
import signal
import subprocess
import sys
import traceback
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "perf-sweep"


def _assert(condition: bool, message: str = "assertion failed") -> None:
    if not condition:
        raise AssertionError(message)


def _marker(name: str) -> str:
    return f"perf-sweep-{name}-{os.getpid()}-{secrets.token_hex(4)}"


def _run_sweep(marker: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(SCRIPT), marker, *args],
        capture_output=True,
        text=True,
        check=False,
    )


def _stop_isolated_group(leader: subprocess.Popen[bytes]) -> None:
    if leader.poll() is not None:
        return
    try:
        os.killpg(leader.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    leader.wait(timeout=3)


def _group_safety_worker(marker: str) -> int:
    survivor = subprocess.Popen(
        [sys.executable, "-c", "import time; time.sleep(60)", marker]
    )
    groupmate = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
    try:
        sweep = _run_sweep(marker, "--kill", "--kill-group", "--grace", "0.1")
        survivor.wait(timeout=3)
        if (
            sweep.returncode != 10
            or "PROTECTED_GROUP:" not in sweep.stdout
            or groupmate.poll() is not None
        ):
            print(sweep.stdout, end="")
            print(sweep.stderr, end="", file=sys.stderr)
            return 1
        return 0
    finally:
        for child in (survivor, groupmate):
            if child.poll() is None:
                child.terminate()
                child.wait(timeout=3)


def test_clean_marker_returns_zero() -> None:
    sweep = _run_sweep(_marker("clean"))
    _assert(sweep.returncode == 0, sweep.stdout + sweep.stderr)
    _assert("CLEAN:" in sweep.stdout, sweep.stdout)


def test_report_finds_argv_survivor_and_groupmate() -> None:
    marker = _marker("report")
    leader = subprocess.Popen(
        [
            sys.executable,
            "-c",
            "import subprocess, time; subprocess.Popen(['sleep', '60']); time.sleep(60)",
            marker,
        ],
        start_new_session=True,
    )
    try:
        sweep = _run_sweep(marker)
        _assert(sweep.returncode == 10, sweep.stdout + sweep.stderr)
        _assert("SURVIVOR:" in sweep.stdout, sweep.stdout)
        _assert("src=argv" in sweep.stdout, sweep.stdout)
        _assert("GROUPMATE:" in sweep.stdout, sweep.stdout)
    finally:
        _stop_isolated_group(leader)


def test_report_finds_inherited_environment_marker() -> None:
    marker = _marker("environment")
    env = os.environ.copy()
    env["PERF_RUN_ID"] = marker
    leader = subprocess.Popen(
        [sys.executable, "-c", "import time; time.sleep(60)"],
        env=env,
        start_new_session=True,
    )
    try:
        sweep = _run_sweep(marker)
        _assert(sweep.returncode == 10, sweep.stdout + sweep.stderr)
        _assert("src=env" in sweep.stdout, sweep.stdout)
    finally:
        _stop_isolated_group(leader)


def test_kill_group_reaps_an_isolated_group() -> None:
    marker = _marker("reap")
    leader = subprocess.Popen(
        [
            sys.executable,
            "-c",
            "import subprocess, time; subprocess.Popen(['sleep', '60']); time.sleep(60)",
            marker,
        ],
        start_new_session=True,
    )
    try:
        sweep = _run_sweep(marker, "--kill", "--kill-group", "--grace", "0.1")
        _assert(sweep.returncode == 10, sweep.stdout + sweep.stderr)
        _assert("KILLED:" in sweep.stdout, sweep.stdout)
        _assert(_run_sweep(marker).returncode == 0, "marker survived group reap")
    finally:
        _stop_isolated_group(leader)


def test_kill_group_never_signals_the_callers_process_group() -> None:
    marker = _marker("protected")
    worker = subprocess.run(
        [sys.executable, __file__, "--group-safety-worker", marker],
        capture_output=True,
        text=True,
        check=False,
        start_new_session=True,
        timeout=8,
    )
    _assert(
        worker.returncode == 0,
        "--kill-group killed or failed its caller process group: "
        f"rc={worker.returncode} stdout={worker.stdout!r} stderr={worker.stderr!r}",
    )


def main() -> int:
    tests = [
        (name, function)
        for name, function in sorted(globals().items())
        if name.startswith("test_") and callable(function)
    ]
    failed = 0
    for name, function in tests:
        try:
            function()
            print(f"PASS  {name}")
        except Exception:
            failed += 1
            print(f"FAIL  {name}")
            traceback.print_exc()
    print(f"\n{len(tests) - failed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--group-safety-worker":
        sys.exit(_group_safety_worker(sys.argv[2]))
    sys.exit(main())
