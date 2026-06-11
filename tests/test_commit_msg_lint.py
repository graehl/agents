#!/usr/bin/env python3
"""End-to-end tests for scripts/commit-msg-lint."""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "commit-msg-lint"


class Workspace:
    def __init__(self):
        self.root = Path(tempfile.mkdtemp(prefix="commit-msg-lint-test-"))

    def cleanup(self) -> None:
        shutil.rmtree(self.root, ignore_errors=True)

    def run(self, input_text: str | None = None) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(SCRIPT)],
            cwd=self.root,
            input=input_text,
            capture_output=True,
            text=True,
            timeout=10,
        )

    def git(self, *args: str) -> subprocess.CompletedProcess:
        env = {
            **os.environ,
            "GIT_AUTHOR_NAME": "Tester",
            "GIT_AUTHOR_EMAIL": "tester@example.com",
            "GIT_COMMITTER_NAME": "Tester",
            "GIT_COMMITTER_EMAIL": "tester@example.com",
        }
        return subprocess.run(
            ["git", *args],
            cwd=self.root,
            env=env,
            capture_output=True,
            text=True,
            timeout=10,
        )


def _assert(cond, msg="assertion failed"):
    if not cond:
        raise AssertionError(msg)


def test_stdin_message_is_linted():
    ws = Workspace()
    try:
        res = ws.run("short subject\n")
        _assert(res.returncode == 0, res.stderr)
        _assert(res.stdout == "short subject\n", "stdin message was not echoed")
    finally:
        ws.cleanup()


def test_no_stdin_lints_head_message():
    ws = Workspace()
    try:
        _assert(ws.git("init").returncode == 0)
        (ws.root / "tracked.txt").write_text("content\n")
        _assert(ws.git("add", "tracked.txt").returncode == 0)
        _assert(ws.git("commit", "-m", "short subject").returncode == 0)
        res = ws.run()
        _assert(res.returncode == 0, res.stderr)
        _assert(res.stdout == "short subject\n\n", "HEAD message was not echoed")
    finally:
        ws.cleanup()


def test_no_stdin_without_head_exits_2():
    ws = Workspace()
    try:
        res = ws.run()
        _assert(res.returncode == 2, "missing HEAD should exit 2")
        _assert("empty input and no HEAD" in res.stderr, res.stderr)
    finally:
        ws.cleanup()


def _collect_tests():
    return [(name, fn) for name, fn in sorted(globals().items()) if name.startswith("test_") and callable(fn)]


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
