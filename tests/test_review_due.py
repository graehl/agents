#!/usr/bin/env python3
"""End-to-end tests for scripts/review-due."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "review-due"


def _run(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--repo", str(repo), *args],
        capture_output=True,
        text=True,
        check=False,
        env=dict(os.environ, ACLI_QUIET="1"),
    )


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t", *args],
        capture_output=True,
        text=True,
        check=True,
    ).stdout


def _commit(repo: Path, name: str, text: str, *, executable: bool = False) -> None:
    path = repo / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    if executable:
        path.chmod(0o755)
    _git(repo, "add", "--", name)
    _git(repo, "commit", "-qm", f"change {name}")


def _repo(root: Path) -> Path:
    repo = root / "project"
    repo.mkdir()
    _git(repo, "init", "-q")
    _commit(repo, "lib.py", "x = 1\n")
    return repo


def _mark(repo: Path) -> None:
    (repo / ".harsh-review").write_text(_git(repo, "rev-parse", "HEAD") + "context\n")


def test_no_marker_reports_nothing() -> None:
    with tempfile.TemporaryDirectory() as root:
        repo = _repo(Path(root))
        _commit(repo, "scripts/tool", "#!/bin/sh\n", executable=True)
        hook = _run(repo, "hook")
        assert hook.returncode == 0 and hook.stdout == "", hook.stderr
        # As the commit hook runs it: no launch banner on stderr either.
        env = {k: v for k, v in os.environ.items() if k != "ACLI_QUIET"}
        quiet = subprocess.run(
            [sys.executable, str(SCRIPT), "--repo", str(repo), "hook", "--acli-quiet"],
            capture_output=True,
            text=True,
            check=False,
            env=env,
        )
        assert (quiet.returncode, quiet.stdout, quiet.stderr) == (0, "", "")
        assert json.loads(_run(repo, "status", "--json").stdout)["reviewed"] is None


def test_new_code_file_makes_a_creation_review_due_and_prose_does_not() -> None:
    with tempfile.TemporaryDirectory() as root:
        repo = _repo(Path(root))
        _mark(repo)
        _commit(repo, "notes.md", "prose\n" * 900)
        _commit(repo, "node_modules/dep/index.js", "x\n" * 900)
        assert _run(repo, "hook").stdout == ""
        _commit(repo, "scripts/tool", "#!/bin/sh\necho hi\n", executable=True)
        hook = _run(repo, "hook").stdout
        assert (
            hook == "review-due: creation review due for new kept code: scripts/tool\n"
        )
        status = json.loads(_run(repo, "status", "--json").stdout)
        assert status["due"] == ["creation"] and status["changed_lines"] == 2
        _mark(repo)
        assert _run(repo, "hook").stdout == ""


def test_accumulated_edits_make_a_periodic_review_due() -> None:
    with tempfile.TemporaryDirectory() as root:
        repo = _repo(Path(root))
        _mark(repo)
        _commit(repo, "lib.py", "x = 2\n")
        assert _run(repo, "hook").stdout == ""
        over_lines = _run(repo, "--max-lines", "1", "hook").stdout
        assert "periodic review due: 2 changed code lines in 1 commits" in over_lines
        assert "creation" not in over_lines
        assert "periodic review due" in _run(repo, "--max-commits", "0", "hook").stdout


def test_marker_naming_an_unknown_commit_fails() -> None:
    with tempfile.TemporaryDirectory() as root:
        repo = _repo(Path(root))
        (repo / ".harsh-review").write_text("0" * 40 + "\n")
        assert _run(repo, "hook").returncode == 4


if __name__ == "__main__":
    tests = [
        value for name, value in sorted(globals().items()) if name.startswith("test_")
    ]
    for test in tests:
        test()
    print(f"ok: {len(tests)} tests")
