#!/usr/bin/env python3
"""End-to-end tests for scripts/commit-msg-fmt."""

from __future__ import annotations

import os
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "commit-msg-fmt"
LINT = REPO_ROOT / "scripts" / "commit-msg-lint"


def run_fmt(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        timeout=10,
    )


def _assert(cond, msg="assertion failed"):
    if not cond:
        raise AssertionError(msg)


def test_literal_newline_escape_is_rejected():
    res = run_fmt("-m", "short subject", "-m", "body\\ntrailer")
    _assert(res.returncode == 1, "literal newline escape should fail")
    _assert("literal '\\n' in -m 2" in res.stderr, res.stderr)


def test_plain_prose_is_wrapped_and_lints_cleanly():
    body = "A decision-bearing body paragraph " * 6
    res = run_fmt("-m", "short subject", "-m", "", "-m", body)
    _assert(res.returncode == 0, res.stderr)
    lines = res.stdout.rstrip("\n").split("\n")
    _assert(lines[1] == "", "formatter must preserve the requested blank line")
    _assert(all(len(line) <= 71 for line in lines[2:]), res.stdout)
    lint = subprocess.run(
        [sys.executable, str(LINT)],
        input=res.stdout,
        capture_output=True,
        text=True,
        timeout=10,
    )
    _assert(lint.returncode == 0, lint.stderr)


def test_documented_process_substitution_commits_checked_bytes():
    with tempfile.TemporaryDirectory(prefix="commit-msg-fmt-test-") as temp:
        root = Path(temp)
        _assert(
            subprocess.run(
                ["git", "init"], cwd=root, capture_output=True, text=True
            ).returncode
            == 0
        )
        root.joinpath("tracked.txt").write_text("content\n")
        _assert(
            subprocess.run(
                ["git", "add", "tracked.txt"],
                cwd=root,
                capture_output=True,
                text=True,
            ).returncode
            == 0
        )
        body = "A reviewer-facing decision and outcome paragraph " * 5
        format_cmd = shlex.join(
            [
                str(SCRIPT),
                "-m",
                "short subject",
                "-m",
                "",
                "-m",
                body,
            ]
        )
        command = f"git commit -F <({format_cmd} | {shlex.quote(str(LINT))})"
        env = {
            **os.environ,
            "GIT_AUTHOR_NAME": "Tester",
            "GIT_AUTHOR_EMAIL": "tester@example.com",
            "GIT_COMMITTER_NAME": "Tester",
            "GIT_COMMITTER_EMAIL": "tester@example.com",
        }
        commit = subprocess.run(
            ["bash", "-c", command],
            cwd=root,
            env=env,
            capture_output=True,
            text=True,
            timeout=10,
        )
        _assert(commit.returncode == 0, commit.stderr)
        message = subprocess.run(
            ["git", "log", "-1", "--format=%B"],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=10,
        ).stdout
        _assert(message.startswith("short subject\n\n"), message)
        _assert(all(len(line) <= 71 for line in message.splitlines()[2:]), message)


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
