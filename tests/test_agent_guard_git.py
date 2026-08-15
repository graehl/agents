#!/usr/bin/env python3
"""Fake-peer command matrix for scripts/agent-guard-git."""

from __future__ import annotations

import os
import shlex
import subprocess
import tempfile
import traceback
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GUARD = REPO_ROOT / "scripts" / "agent-guard-git"


def _assert(condition: bool, message: str = "assertion failed") -> None:
    if not condition:
        raise AssertionError(message)


def _fixture() -> tuple[Path, Path, dict[str, str]]:
    root = Path(tempfile.mkdtemp(prefix="agent-guard-git-test-"))
    active = root / ".agentctl" / "active"
    active.mkdir(parents=True)
    (active / "peer-session").write_text("Editing overlapping files\n")
    log = root / "git.log"
    fake = root / "git-real"
    fake.write_text(
        "#!/bin/sh\n"
        'if [ "$1" = rev-parse ] && [ "$2" = --show-toplevel ]; then\n'
        f"  printf '%s\\n' {shlex.quote(str(root))}\n"
        "  exit 0\n"
        "fi\n"
        f"printf '%s\\n' \"$*\" >> {shlex.quote(str(log))}\n"
    )
    fake.chmod(0o755)
    env = dict(
        os.environ,
        AGENT_GUARD="1",
        AGENT_GUARD_REAL_GIT=str(fake),
        AGENTCTL_SESSION_ID="own-session",
    )
    return root, log, env


def _run(root: Path, env: dict[str, str], argv: list[str]):
    return subprocess.run(
        [str(GUARD), *argv],
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def test_fake_peer_command_matrix() -> None:
    root, log, env = _fixture()
    blocked = [
        ["reset", "--hard"],
        ["reset", "--merge", "HEAD^"],
        ["clean", "-fd"],
        ["restore", "tracked"],
        ["restore", "--worktree", "tracked"],
        ["checkout", "--", "tracked"],
        ["checkout", "."],
        ["checkout", "-f", "topic"],
        ["stash"],
        ["stash", "push"],
        ["stash", "push", "--", "."],
        ["stash", "pop"],
        ["stash", "drop"],
        ["stash", "clear"],
        ["-C", str(root), "reset", "--hard"],
        ["-c", "user.name=Test", "clean", "-fd"],
    ]
    for argv in blocked:
        proc = _run(root, env, argv)
        _assert(proc.returncode == 1, f"should block {argv}: {proc.stderr}")
        _assert("peer-session" in proc.stderr, proc.stderr)

    allowed = [
        ["status", "--short"],
        ["reset", "--soft", "HEAD^"],
        ["restore", "--staged", "tracked"],
        ["checkout", "topic"],
        ["stash", "apply"],
        ["stash", "push", "--", "tracked"],
    ]
    for argv in allowed:
        proc = _run(root, env, argv)
        _assert(proc.returncode == 0, f"should allow {argv}: {proc.stderr}")

    calls = log.read_text().splitlines()
    _assert(len(calls) == len(allowed), calls)


def main() -> int:
    try:
        test_fake_peer_command_matrix()
    except Exception:
        traceback.print_exc()
        print("0 passed, 1 failed")
        return 1
    print("1 passed, 0 failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
