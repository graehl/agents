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
        assert "/.verify/" in exclude.splitlines(), exclude
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


def test_local_config_overrides_and_list() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = _project(tmp)
        (root / "verify.local.toml").write_text(
            '[[check]]\nname = "fails"\nrun = "true"\n'
        )
        listed = {r["name"]: r for r in _records(_run(root, "--list"))}
        assert listed["fails"]["source"] == "verify.local.toml", listed["fails"]
        assert "slow" not in listed, listed
        run = _run(root, "--only", "fails")
        assert run.returncode == 0, run.stdout
        assert _records(run)[-1]["passed"] == 1


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
