#!/usr/bin/env python3
"""End-to-end tests for scripts/on_deck.py."""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "on_deck.py"


class Workspace:
    def __init__(self):
        self.root = Path(tempfile.mkdtemp(prefix="on-deck-test-"))

    def cleanup(self) -> None:
        shutil.rmtree(self.root, ignore_errors=True)

    def run(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=self.root,
            capture_output=True,
            text=True,
            timeout=10,
        )


def _assert(cond, msg="assertion failed"):
    if not cond:
        raise AssertionError(msg)


def add_args(slug: str, priority: str = "5", by: str = "director") -> list[str]:
    return [
        "add",
        slug,
        "--priority",
        priority,
        "--by",
        by,
        "--runtime-estimate",
        "20m",
        "--size-class",
        "small",
        "--cheap-reversible",
        "true",
        "--guard",
        "input file exists",
        "--skip-if",
        "output already exists",
        "--what",
        f"Run {slug}",
        "--why",
        "Exercise the on-deck helper.",
        "--provenance",
        "topics/on-deck.md",
        "--on-success",
        "Planner reviews the output.",
        "--check",
        "Confirm the output exists and quote one metric.",
        "--",
        "agentctl",
        "start",
        "--no-aim",
        slug,
        "--",
        "true",
    ]


def test_add_index_and_validate():
    ws = Workspace()
    try:
        res = ws.run(*add_args("pilot-a"))
        _assert(res.returncode == 0, res.stderr)
        entry = ws.root / "on-deck" / "pilot-a.md"
        index = ws.root / "on-deck" / "INDEX.md"
        _assert(entry.exists(), "entry was not created")
        _assert(index.exists(), "index was not created")
        text = entry.read_text()
        _assert("priority: 5" in text, "priority missing from frontmatter")
        _assert("## Launch" in text and "agentctl start" in text, "launch block missing")
        _assert("pilot-a" in index.read_text(), "index omitted entry")
        res = ws.run("validate")
        _assert(res.returncode == 0, res.stderr)
    finally:
        ws.cleanup()


def test_steward_priority_cap():
    ws = Workspace()
    try:
        res = ws.run(*add_args("too-high", priority="4", by="steward"))
        _assert(res.returncode != 0, "steward priority cap should fail")
        _assert("priority <= 3" in res.stderr, res.stderr)
    finally:
        ws.cleanup()


def test_index_sort_and_retire():
    ws = Workspace()
    try:
        _assert(ws.run(*add_args("low", priority="1")).returncode == 0)
        _assert(ws.run(*add_args("high", priority="8")).returncode == 0)
        index = (ws.root / "on-deck" / "INDEX.md").read_text()
        _assert(index.index("high") < index.index("low"), "index should sort by priority descending")
        res = ws.run("retire", "high", "--reason", "covered by newer run")
        _assert(res.returncode == 0, res.stderr)
        _assert(not (ws.root / "on-deck" / "high.md").exists(), "retired entry stayed live")
        _assert((ws.root / "on-deck" / "done" / "high.md").exists(), "retired entry was not moved")
        index = (ws.root / "on-deck" / "INDEX.md").read_text()
        _assert("high" not in index, "retired entry remained in live index")
    finally:
        ws.cleanup()


def test_log_updates_status_and_index():
    ws = Workspace()
    try:
        _assert(ws.run(*add_args("tracked", priority="3")).returncode == 0)
        res = ws.run("log", "tracked", "--status", "launched", "launched job=tracked run=abc123")
        _assert(res.returncode == 0, res.stderr)
        entry = (ws.root / "on-deck" / "tracked.md").read_text()
        _assert("status: \"launched\"" in entry, "status frontmatter was not updated")
        _assert("launched job=tracked run=abc123" in entry, "status log line missing")
        index = (ws.root / "on-deck" / "INDEX.md").read_text()
        _assert("| launched |" in index, "index did not pick up status change")
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
