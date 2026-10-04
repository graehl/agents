#!/usr/bin/env python3
"""Tests for scripts/verify — the per-project check runner.

Every case drives the real CLI against a temporary project, so config
loading, process handling, logs, and output all go through the entry point.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
import traceback
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOL = REPO_ROOT / "scripts" / "verify"

CONFIG = """
[[check]]
name = "passes"
run = "echo fine"

[[check]]
name = "fails"
run = "echo context; echo broken >&2; exit 3"

[[check]]
name = "unavailable"
run = '''echo '{"ok":false,"exit_code":69,"error":{"code":"unavailable","message":"needs yaml"}}' >&2; exit 69'''

[[check]]
name = "needs-tool"
run = "true"
requires = ["no-such-executable-for-verify-tests"]

[[check]]
each = "t/test_*.sh"
run = "bash {path}"

[[check]]
name = "slow"
run = "sleep 30"
timeout = "0.5s"
tier = "deep"
"""


def _project(tmp: str, config: str = CONFIG) -> Path:
    root = Path(tmp) / "proj"
    (root / "t").mkdir(parents=True)
    (root / "t" / "test_a.sh").write_text("exit 0\n")
    (root / "t" / "test_b.sh").write_text("exit 0\n")
    (root / "verify.toml").write_text(config)
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    return root


def _run(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = {**os.environ, "ACLI_QUIET": "1"}
    return subprocess.run(
        [str(TOOL), "--project", str(root), "--json", *args],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


def _records(run: subprocess.CompletedProcess[str]) -> list[dict]:
    return [json.loads(line) for line in run.stdout.splitlines()]


def test_quick_tier_reports_only_attention() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = _project(tmp)
        run = _run(root)
        assert run.returncode == 1, (run.returncode, run.stderr)
        records = _records(run)
        summary = records[-1]
        assert summary["kind"] == "summary" and summary["ok"] is False, summary
        assert summary["tier"] == "quick"
        assert (summary["passed"], summary["failed"], summary["skipped"]) == (3, 1, 2)
        results = {r["name"]: r for r in records[:-1]}
        assert set(results) == {"fails", "unavailable", "needs-tool"}, results
        fail = results["fails"]
        assert fail["exit_code"] == 3
        assert fail["stdout_tail"] == "context" and fail["stderr_tail"] == "broken"
        assert Path(fail["stderr_log"]).read_text() == "broken\n"
        assert results["unavailable"]["reason"] == "needs yaml"
        assert results["needs-tool"]["reason"].startswith("missing ")
        exclude = (root / ".git" / "info" / "exclude").read_text()
        assert ".verify/" in exclude.splitlines(), exclude
        assert "verify.local.toml" in exclude.splitlines(), exclude
        status = subprocess.run(
            ["git", "-C", str(root), "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        assert ".verify" not in status, status


def test_full_lists_passes_and_each_expansion() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = _project(tmp)
        names = {r["name"] for r in _records(_run(root, "--full"))[:-1]}
        assert {"passes", "test_a", "test_b"} <= names, names


def test_deep_tier_times_out_and_kills() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = _project(tmp)
        start = time.monotonic()
        run = _run(root, "--deep", "--only", "slow")
        assert time.monotonic() - start < 10
        assert run.returncode == 1, run.stderr
        slow = _records(run)[0]
        assert slow["name"] == "slow" and slow["exit_code"] is None, slow
        assert slow["timed_out_after_s"] == 0.5, slow
        survivors = subprocess.run(
            ["pgrep", "-x", "sleep", "-a"], capture_output=True, text=True, check=False
        ).stdout
        assert "sleep 30" not in survivors, survivors


def test_local_config_wins_and_can_include() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = _project(tmp)
        local = root / "verify.local.toml"
        local.write_text('[[check]]\nname = "mine"\nrun = "true"\n')
        listed = [r["name"] for r in _records(_run(root, "--list"))]
        assert listed == ["mine"], listed  # replaces verify.toml entirely

        local.write_text(
            'include = ["verify.toml"]\n\n[[check]]\nname = "fails"\nrun = "true"\n'
        )
        listed = {r["name"]: r for r in _records(_run(root, "--list"))}
        assert listed["fails"]["source"] == "verify.local.toml", listed["fails"]
        assert listed["passes"]["source"] == "verify.toml", listed["passes"]
        assert "slow" not in listed, listed
        run = _run(root, "--only", "fails")
        assert run.returncode == 0, run.stdout
        assert _records(run)[-1]["passed"] == 1

        local.write_text('include = ["verify.local.toml"]\n')
        run = _run(root, "--list")
        assert run.returncode == 2 and "include cycle" in run.stderr, run.stderr


def test_program_config_includes_parent_checks() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = _project(
            tmp, '[[check]]\nname = "root-file"\nrun = "test -f t/test_a.sh"\n'
        )
        program = root / "research" / "prog"
        program.mkdir(parents=True)
        (program / "verify.toml").write_text(
            'include = ["../../verify.toml"]\n\n'
            '[[check]]\nname = "prog-file"\nrun = "test -f here"\n'
        )
        (program / "here").write_text("")
        run = _run(program)
        assert run.returncode == 0, run.stdout  # each check runs in its file's dir
        assert _records(run)[-1]["passed"] == 2


def test_exclusive_checks_never_overlap() -> None:
    body = "echo start >> order; sleep 0.3; echo end >> order"
    config = "".join(
        f'[[check]]\nname = "{name}"\nrun = "{body}"\nexclusive = true\n\n'
        for name in ("one", "two")
    )
    config += '[[check]]\nname = "shared"\nrun = "true"\n'
    with tempfile.TemporaryDirectory() as tmp:
        root = _project(tmp, config)
        run = _run(root, "--jobs", "4")
        assert run.returncode == 0, run.stdout
        order = (root / "order").read_text().split()
        assert order == ["start", "end", "start", "end"], order


def _passed(root: Path) -> list[str]:
    run = _run(root, "--passed")
    assert run.returncode == 0, run.stderr
    return _records(run)[0]["checks"]


def test_passed_tracks_the_exact_source_tree() -> None:
    config = (
        '[[check]]\nname = "ok"\nrun = "true"\n\n'
        '[[check]]\nname = "bad"\nrun = "false"\n\n'
        '[[check]]\nname = "later"\nrun = "true"\ntier = "deep"\n'
    )
    with tempfile.TemporaryDirectory() as tmp:
        root = _project(tmp, config)
        assert _passed(root) == []
        _run(root)
        assert _passed(root) == ["ok"]  # failures and unrun tiers are absent
        _run(root, "--only", "later")
        assert _passed(root) == ["ok", "later"]
        text = subprocess.run(
            [str(TOOL), "--project", str(root), "--passed", "--text"],
            capture_output=True,
            text=True,
            env={**os.environ, "ACLI_QUIET": "1"},
            check=True,
        ).stdout
        assert text == "ok,later\n", repr(text)
        (root / "new_file.txt").write_text("untracked edits count\n")
        assert _passed(root) == []
        (root / "new_file.txt").unlink()
        assert _passed(root) == ["ok", "later"]
        (root / "verify.toml").write_text(
            config.replace('"true"\n\n', '"true;"\n\n', 1)
        )
        assert "ok" not in _passed(root)


def _git(root: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-C", str(root), "-c", "user.name=t", "-c", "user.email=t@t", *args],
        check=True,
        capture_output=True,
    )


def test_uncommitted_pass_survives_committing_the_same_files() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = _project(tmp, '[[check]]\nname = "ok"\nrun = "true"\n')
        source = _records(_run(root))[-1]["source"]
        assert source["state"] == "uncommitted" and source["head"] is None, source
        assert source["recorded"] is True, source
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "verified files")
        assert _passed(root) == ["ok"]  # the commit's tree is the verified tree
        head = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        source = _records(_run(root))[-1]["source"]
        assert source["state"] == "committed" and source["head"] == head, source
        assert source["tree"] == _records(_run(root, "--passed"))[0]["tree"]

        outside = Path(tmp) / "plain"
        outside.mkdir()
        (outside / "verify.toml").write_text('[[check]]\nname = "ok"\nrun = "true"\n')
        run = _run(outside)
        source = _records(run)[-1]["source"]
        assert source == {"state": "not-git", "recorded": False}, source


def test_warn_pattern_reports_without_failing() -> None:
    config = (
        '[[check]]\nname = "noisy"\n'
        "run = \"echo fine; echo 'Warning: not wrapped in act(...)' >&2\"\n"
        'warn = "not wrapped in act"\n\n'
        '[[check]]\nname = "quiet"\nrun = "echo all good"\nwarn = "Warning"\n'
    )
    with tempfile.TemporaryDirectory() as tmp:
        root = _project(tmp, config)
        warnings_file = Path(tmp) / "warnings.txt"
        run = _run(root, "--warnings-file", str(warnings_file))
        assert run.returncode == 0, run.stdout
        records = _records(run)
        noisy, summary = records
        assert noisy["name"] == "noisy" and noisy["status"] == "passed", noisy
        assert noisy["warnings"] == ["Warning: not wrapped in act(...)"], noisy
        assert summary["warned_checks"] == ["noisy"], summary
        assert summary["ok"] is True and summary["failed"] == 0, summary
        assert warnings_file.read_text() == (
            "noisy: Warning: not wrapped in act(...)\n"
        )
        assert _passed(root) == ["noisy", "quiet"]
        text = subprocess.run(
            [str(TOOL), "--project", str(root), "--text"],
            capture_output=True,
            text=True,
            env={**os.environ, "ACLI_QUIET": "1"},
            check=True,
        ).stdout
        assert text.startswith("verify ok: 2 passed (1 with warnings)"), text
        assert "    Warning: not wrapped in act(...)" in text, text


def test_program_subdirectory_uses_its_own_config() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = _project(tmp, '[[check]]\nname = "root-check"\nrun = "true"\n')
        program = root / "research" / "prog"
        program.mkdir(parents=True)
        (program / "verify.toml").write_text(
            '[[check]]\nname = "prog-check"\nrun = "test -f here"\n'
        )
        (program / "here").write_text("")
        listed = _records(_run(program, "--list"))
        assert [c["name"] for c in listed] == ["prog-check"], listed
        run = _run(program)
        assert run.returncode == 0, run.stdout  # cwd is the program dir
        assert _records(run)[-1]["root"] == str(program)
        status = subprocess.run(
            ["git", "-C", str(root), "status", "--porcelain", "--untracked-files=all"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        assert ".verify" not in status, status


def test_text_summary_is_one_line_when_green() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = _project(tmp, '[[check]]\nname = "ok"\nrun = "true"\n')
        env = {**os.environ, "ACLI_QUIET": "1"}
        run = subprocess.run(
            [str(TOOL), "--project", str(root), "--text"],
            capture_output=True,
            text=True,
            env=env,
            check=False,
        )
        assert run.returncode == 0, run.stderr
        lines = run.stdout.splitlines()
        assert len(lines) == 1 and lines[0].startswith("verify ok: 1 passed"), lines


def test_stderr_announces_each_check_as_commentary() -> None:
    config = (
        '[[check]]\nname = "ok"\nrun = "echo `date`"\n'
        '[[check]]\nname = "multi"\nrun = """\ntrue\ntrue\n"""\n'
    )
    with tempfile.TemporaryDirectory() as tmp:
        root = _project(tmp, config)
        env = {k: v for k, v in os.environ.items() if k != "ACLI_QUIET"}

        def run(*args: str) -> subprocess.CompletedProcess[str]:
            return subprocess.run(
                [str(TOOL), "--project", str(root), "--json", *args],
                capture_output=True,
                text=True,
                env=env,
                check=False,
            )

        loud = run()
        assert loud.returncode == 0, loud.stderr
        lines = loud.stderr.splitlines()
        assert lines[0].startswith("# acli: 1 ") and "+commentary-lines" in lines[0]
        notes = sorted(
            line for line in lines if line.startswith("# _acli.commentary: ")
        )
        assert notes == [
            "# _acli.commentary: running `multi`: `true …`",
            "# _acli.commentary: running `ok`: `` echo `date` ``",
        ], notes
        assert _records(loud)[-1]["ok"] is True  # stdout stays pure JSONL
        quiet = run("--no-commentary")
        assert "_acli.commentary" not in quiet.stderr, quiet.stderr


def test_config_errors_and_missing_config() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = _project(tmp, '[[check]]\nname = "x"\nrun = "true"\ntier = "slow"\n')
        run = _run(root)
        assert run.returncode == 2, run.stderr
        envelope = json.loads(run.stderr.strip().splitlines()[-1])
        assert "tier" in envelope["error"]["message"], envelope
        empty = Path(tmp) / "empty"
        empty.mkdir()
        run = _run(empty)
        assert run.returncode == 4, run.stderr


def main(argv: list[str]) -> int:
    verbose = "-v" in argv
    tests = [
        (name, fn)
        for name, fn in sorted(globals().items())
        if name.startswith("test_") and callable(fn)
    ]
    passed = failed = 0
    failures: list[tuple[str, str]] = []
    start = time.time()
    for name, fn in tests:
        try:
            fn()
            passed += 1
            print(f"PASS  {name}" if verbose else ".", end="\n" if verbose else "")
        except Exception:
            failed += 1
            failures.append((name, traceback.format_exc()))
            print(f"FAIL  {name}" if verbose else "F", end="\n" if verbose else "")
    if not verbose:
        print()
    for name, tb in failures:
        print(f"\n--- {name} ---\n{tb}")
    print(f"\n{passed} passed, {failed} failed in {time.time() - start:.2f}s")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
