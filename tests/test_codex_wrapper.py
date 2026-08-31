#!/usr/bin/env python3
"""End-to-end tests for the Codex shadow wrapper."""

from __future__ import annotations

import fcntl
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "codex"
WARNING = "WARNING: failed to clean up stale arg0 temp dirs:"


class Workspace:
    def __init__(self):
        codex_tmp = Path.home() / ".codex" / "tmp"
        codex_tmp.mkdir(parents=True, exist_ok=True)
        self.root = Path(tempfile.mkdtemp(prefix="codex-wrapper-test-", dir=codex_tmp))
        self.arg0 = self.root / "tmp" / "arg0"
        self.arg0.mkdir(parents=True)

    def cleanup(self) -> None:
        shutil.rmtree(self.root, ignore_errors=True)

    def alias_dir(self, name: str) -> Path:
        directory = self.arg0 / name
        directory.mkdir()
        (directory / ".lock").touch()
        (directory / "apply_patch").symlink_to("missing-target")
        return directory

    def run(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [str(SCRIPT), *args],
            env={**os.environ, "CODEX_HOME": str(self.root)},
            capture_output=True,
            text=True,
            timeout=10,
        )


def _assert(cond, msg="assertion failed"):
    if not cond:
        raise AssertionError(msg)


def test_stale_alias_directory_is_removed_without_a_warning():
    ws = Workspace()
    try:
        stale = ws.alias_dir("codex-arg0stale")
        live = ws.alias_dir("codex-arg0live")
        with (live / ".lock").open("r+") as live_lock:
            fcntl.flock(live_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            res = ws.run("--version")
            _assert(live.exists(), "live alias directory was removed")

        _assert(res.returncode == 0, res.stderr)
        _assert(WARNING not in res.stderr, res.stderr)
        _assert(not stale.exists(), "stale alias directory was not removed")
        _assert(res.stdout.startswith("codex-cli "), res.stdout)
    finally:
        ws.cleanup()


def test_codex_errors_still_reach_stderr():
    ws = Workspace()
    try:
        res = ws.run("--definitely-invalid")
        _assert(res.returncode == 2, res.stderr)
        _assert("unexpected argument '--definitely-invalid'" in res.stderr, res.stderr)
    finally:
        ws.cleanup()


def _collect_tests():
    return [
        (name, fn)
        for name, fn in sorted(globals().items())
        if name.startswith("test_") and callable(fn)
    ]


def main() -> int:
    failed = 0
    for name, fn in _collect_tests():
        try:
            fn()
            print(f"PASS  {name}")
        except Exception as exc:
            failed += 1
            print(f"FAIL  {name}: {exc}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
