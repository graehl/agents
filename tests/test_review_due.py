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


def _marker(repo: Path) -> str:
    return (repo / ".harsh-review").read_text().splitlines()[0]


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
        # A path Git would print quoted is still counted.
        _commit(repo, "na\u00efve [x].py", "y = 1\ny = 2\n")
        status = json.loads(_run(repo, "status", "--json").stdout)
        assert status["changed_lines"] == 4 and status["commits"] == 2, status
        assert status["new_files"] == ["na\u00efve [x].py"]
        over_lines = _run(repo, "--max-lines", "1", "hook").stdout
        assert "periodic review due: 4 changed code lines in 2 commits" in over_lines
        assert "periodic review due" in _run(repo, "--max-commits", "0", "hook").stdout


def test_an_oversized_backlog_replaces_the_due_reviews() -> None:
    with tempfile.TemporaryDirectory() as root:
        repo = _repo(Path(root))
        _mark(repo)
        _commit(repo, "legacy/old.py", "a = 1\nb = 2\nc = 3\n")
        hook = _run(repo, "--max-review-lines", "2", "hook").stdout
        assert "oversized backlog, start no review: 3 changed code lines" in hook
        assert "creation review" not in hook and "legacy 3" in hook


def test_an_approved_skip_is_recorded_and_no_longer_counted() -> None:
    with tempfile.TemporaryDirectory() as root:
        repo = _repo(Path(root))
        _mark(repo)
        _commit(repo, "legacy/old.py", "a = 1\nb = 2\nc = 3\n")
        _commit(repo, "lib.py", "x = 1\ny = 2\n")
        cut = _git(repo, "rev-parse", "HEAD").strip()
        _commit(repo, "feature.py", "f = 1\n")
        record = repo / "gaps" / "unreviewed-code.md"

        preview = _run(repo, "skip", "--dry-run", "--to", cut, "--reason", "legacy")
        assert json.loads(preview.stdout)["remaining"]["changed_lines"] == 1
        assert not record.exists()

        # One subtree only: the rest of that range is still to be reviewed.
        _run(repo, "skip", "--to", cut, "--path", "legacy/", "--reason", "legacy")
        status = json.loads(_run(repo, "status", "--json").stdout)
        assert status["changed_lines"] == 2 and status["commits"] == 2, status
        assert status["new_files"] == ["feature.py"]
        assert f"- `legacy` `{_marker(repo)}..{cut}` 3 lines, 1 commits" in (
            record.read_text()
        )

        # A later change under the skipped subtree is counted again.
        _commit(repo, "legacy/old.py", "a = 1\nb = 2\nc = 4\n")
        assert json.loads(_run(repo, "status", "--json").stdout)["changed_lines"] == 4

        # Extending the same path rewrites its one row instead of adding another.
        _run(repo, "skip", "--to", "HEAD", "--path", "legacy", "--reason", "more")
        assert record.read_text().count("- `legacy`") == 1
        assert _run(repo, "skip", "--to", cut, "--reason", "back").returncode == 0
        again = _run(repo, "skip", "--to", cut, "--reason", "twice")
        assert again.returncode == 5, again.stderr

        _run(repo, "unskip", "--path", "./legacy/")
        assert "`legacy`" not in record.read_text()
        _run(repo, "unskip", "--path", ".")
        assert not record.exists()


def test_skip_refuses_rows_it_could_not_honor() -> None:
    with tempfile.TemporaryDirectory() as root:
        repo = _repo(Path(root))
        _mark(repo)
        _commit(repo, "legacy/old.py", "a = 1\n")
        record = repo / "gaps" / "unreviewed-code.md"
        two_lines = _run(repo, "skip", "--to", "HEAD", "--reason", "a\n- `b` c")
        assert two_lines.returncode == 2, two_lines.stderr
        assert _run(repo, "skip", "--to", "nope", "--reason", "r").returncode == 4
        _git(repo, "branch", "side")
        _commit(repo, "lib.py", "x = 3\n")
        _git(repo, "checkout", "-q", "side")
        off_history = _run(repo, "skip", "--to", "master", "--reason", "r")
        if off_history.returncode == 4:  # default branch is named main here
            off_history = _run(repo, "skip", "--to", "main", "--reason", "r")
        assert off_history.returncode == 5, off_history.stderr
        assert not record.exists()

        # A path spelled differently, twice, makes one row that still matches.
        _run(
            repo,
            "skip",
            "--to",
            "HEAD",
            "--path",
            "./legacy",
            "--path",
            "legacy/",
            "--path",
            "docs",
            "--reason",
            "r",
        )
        assert record.read_text().count("- `legacy`") == 1
        assert "`docs`" not in record.read_text()
        assert json.loads(_run(repo, "status", "--json").stdout)["changed_lines"] == 0


def test_a_skip_row_whose_commit_is_gone_is_reported() -> None:
    with tempfile.TemporaryDirectory() as root:
        repo = _repo(Path(root))
        _mark(repo)
        gone = "1" * 40
        (repo / "gaps").mkdir()
        (repo / "gaps" / "unreviewed-code.md").write_text(
            f"- `legacy` `{_marker(repo)}..{gone}` 3 lines, 1 commits; "
            "skipped 2026-11-10: r\n"
        )
        assert "no longer has (111111111111)" in _run(repo, "hook").stdout


def test_a_malformed_skip_row_is_an_error() -> None:
    with tempfile.TemporaryDirectory() as root:
        repo = _repo(Path(root))
        _mark(repo)
        (repo / "gaps").mkdir()
        (repo / "gaps" / "unreviewed-code.md").write_text("- `legacy` oops\n")
        assert _run(repo, "hook").returncode == 3


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
