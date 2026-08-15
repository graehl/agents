#!/usr/bin/env python3
"""Behavior tests for scripts/pre-push-no-attrib."""

from __future__ import annotations

import subprocess
import tempfile
import traceback
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
HOOK = REPO_ROOT / "scripts" / "pre-push-no-attrib"
COMMITS_TOPIC = REPO_ROOT / "topics" / "commits.md"
ZERO = "0" * 40


def _assert(condition: bool, message: str = "assertion failed") -> None:
    if not condition:
        raise AssertionError(message)


def _git(root: Path, *args: str, input_text: str | None = None):
    return subprocess.run(
        ["git", *args],
        cwd=root,
        input=input_text,
        capture_output=True,
        text=True,
        check=False,
    )


def _repo() -> Path:
    root = Path(tempfile.mkdtemp(prefix="pre-push-no-attrib-test-"))
    _assert(_git(root, "init", "-q").returncode == 0)
    _git(root, "config", "user.name", "Test")
    _git(root, "config", "user.email", "test@example.invalid")
    (root / "tracked").write_text("base\n")
    _git(root, "add", "tracked")
    _assert(_git(root, "commit", "-q", "-m", "base").returncode == 0)
    return root


def _commit(root: Path, message: str) -> str:
    path = root / "tracked"
    path.write_text(path.read_text() + "x\n")
    _git(root, "add", "tracked")
    proc = _git(root, "commit", "-q", "-F", "-", input_text=message)
    _assert(proc.returncode == 0, proc.stderr)
    return _git(root, "rev-parse", "HEAD").stdout.strip()


def _hook(root: Path, remote: str, tip: str, remote_tip: str = ZERO):
    line = f"refs/heads/topic {tip} refs/heads/topic {remote_tip}\n"
    return subprocess.run(
        [str(HOOK), remote, f"test://{remote}"],
        cwd=root,
        input=line,
        capture_output=True,
        text=True,
        check=False,
    )


def test_new_ref_excludes_only_the_destination_remote() -> None:
    root = _repo()
    marked = _commit(
        root,
        "marked\n\nCo-Authored-By: Example <example@example.invalid>\n",
    )
    _assert(
        _git(root, "update-ref", "refs/remotes/private/main", marked).returncode == 0
    )

    private = _hook(root, "private", marked)
    _assert(private.returncode == 0, private.stderr)
    public = _hook(root, "public", marked)
    _assert(public.returncode == 1, public.stderr)
    _assert("no-attrib:" in public.stderr, public.stderr)


def test_generated_banner_is_anchored_to_the_start_of_a_line() -> None:
    benign_root = _repo()
    benign = _commit(
        benign_root,
        "benign\n\nThis prose was generated with [a local fixture].\n",
    )
    _assert(_hook(benign_root, "public", benign).returncode == 0)

    marked_root = _repo()
    marked = _commit(marked_root, "marked\n\nGenerated with [a local fixture]\n")
    _assert(_hook(marked_root, "public", marked).returncode == 1)


def test_detected_space_free_trailer_strips_and_verifies_clean() -> None:
    root = _repo()
    marked = _commit(
        root,
        "marked\n\nCo-Authored-By:Name <name@example.invalid>\n",
    )
    _assert(_hook(root, "public", marked).returncode == 1)

    message = _git(root, "log", "-1", "--format=%B").stdout
    pattern = "^co-authored-by:[[:space:]]*"
    _assert(pattern in COMMITS_TOPIC.read_text(), "documented strip pattern drifted")
    stripped = subprocess.run(
        ["sed", f"/{pattern}/Id"],
        input=message,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    amended = _git(root, "commit", "--amend", "-q", "-F", "-", input_text=stripped)
    _assert(amended.returncode == 0, amended.stderr)
    clean_tip = _git(root, "rev-parse", "HEAD").stdout.strip()
    _assert(_hook(root, "public", clean_tip).returncode == 0)


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
    raise SystemExit(main())
