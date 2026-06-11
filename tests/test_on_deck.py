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


def add_args(
    slug: str,
    priority: str = "5",
    by: str = "director",
    guard: str = "test -e .",
    skip_if: str = "false",
    size_class: str = "small",
    cheap_reversible: str = "true",
    status: str = "pending",
) -> list[str]:
    return [
        "add",
        slug,
        "--priority",
        priority,
        "--by",
        by,
        "--status",
        status,
        "--runtime-estimate",
        "20m",
        "--size-class",
        size_class,
        "--cheap-reversible",
        cheap_reversible,
        "--guard",
        guard,
        "--skip-if",
        skip_if,
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


def test_index_without_queue_is_noop():
    ws = Workspace()
    try:
        res = ws.run("index")
        _assert(res.returncode == 0, res.stderr)
        _assert("no on-deck directory" in res.stdout, res.stdout)
        _assert(not (ws.root / "on-deck").exists(), "index created an unopted queue")
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
        done = ws.root / "on-deck" / "done" / "high.md"
        _assert(done.exists(), "retired entry was not moved")
        _assert("status: \"retired\"" in done.read_text(), "retired status was not written to done entry")
        index = (ws.root / "on-deck" / "INDEX.md").read_text()
        _assert("high" not in index, "retired entry remained in live index")
    finally:
        ws.cleanup()


def test_retired_live_entry_is_not_indexed():
    ws = Workspace()
    try:
        _assert(ws.run(*add_args("stale-retired", priority="9")).returncode == 0)
        res = ws.run("log", "stale-retired", "--status", "retired", "left retired in live queue")
        _assert(res.returncode == 0, res.stderr)
        index = (ws.root / "on-deck" / "INDEX.md").read_text()
        _assert("stale-retired" not in index, "live retired entry remained in index")
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


def test_validate_reports_parse_error_directly():
    ws = Workspace()
    try:
        _assert(ws.run(*add_args("good")).returncode == 0)
        rogue = ws.root / "on-deck" / "rogue.md"
        rogue.write_text("# rogue\nno frontmatter here\n")
        res = ws.run("validate")
        _assert(res.returncode == 1, "corrupt entry should fail validation")
        _assert("missing frontmatter fence" in res.stderr, res.stderr)
        _assert("missing priority" not in res.stderr, "parse error should not cascade into field errors")
        ws.run("index")
        index = (ws.root / "on-deck" / "INDEX.md").read_text()
        _assert("invalid" in index and "missing frontmatter fence" in index, index)
    finally:
        ws.cleanup()


def test_log_status_without_status_line_fails():
    ws = Workspace()
    try:
        _assert(ws.run(*add_args("good")).returncode == 0)
        entry = ws.root / "on-deck" / "no-status.md"
        entry.write_text(
            "---\nslug: \"no-status\"\npriority: 5\nby: \"director\"\n"
            "runtime_estimate: \"5m\"\nsize_class: \"small\"\ncheap_reversible: true\n"
            "guard: \"true\"\nskip_if: \"false\"\n---\n\n# no-status\n\n"
            "## Launch\n```bash\ntrue\n```\n\n## Check\nc\n\n## Status Log\n- t\n"
        )
        res = ws.run("log", "no-status", "--status", "launched", "launched anyway")
        _assert(res.returncode != 0, "status update with no status: line must fail")
        _assert("no status:" in res.stderr, res.stderr)
    finally:
        ws.cleanup()


def test_log_and_retire_record_author():
    ws = Workspace()
    try:
        _assert(ws.run(*add_args("authored")).returncode == 0)
        res = ws.run("log", "authored", "--by", "director", "--status", "blocked", "needs new guard")
        _assert(res.returncode == 0, res.stderr)
        entry = (ws.root / "on-deck" / "authored.md").read_text()
        _assert("director: needs new guard" in entry, entry)
        res = ws.run("retire", "authored", "--by", "director", "--reason", "superseded")
        _assert(res.returncode == 0, res.stderr)
        done = (ws.root / "on-deck" / "done" / "authored.md").read_text()
        _assert("director: retired - superseded" in done, done)
    finally:
        ws.cleanup()


def test_size_class_vocabulary_enforced():
    ws = Workspace()
    try:
        res = ws.run(*add_args("huge", size_class="huge"))
        _assert(res.returncode != 0, "unknown size_class should be rejected")
        _assert("size_class" in res.stderr, res.stderr)
    finally:
        ws.cleanup()


def test_add_blocked_placeholder():
    ws = Workspace()
    try:
        res = ws.run(*add_args("not-yet", status="blocked"))
        _assert(res.returncode == 0, res.stderr)
        entry = (ws.root / "on-deck" / "not-yet.md").read_text()
        _assert('status: "blocked"' in entry, entry)
        _assert("created blocked entry" in entry, entry)
    finally:
        ws.cleanup()


def test_validate_warns_on_agentctl_launch_without_context_note():
    ws = Workspace()
    try:
        _assert(ws.run(*add_args("bare")).returncode == 0)
        res = ws.run("validate")
        _assert(res.returncode == 0, res.stderr)
        _assert("--context-note" in res.stderr, "expected a context-note warning")
    finally:
        ws.cleanup()


def test_eligible_runs_guard_and_skip_commands():
    ws = Workspace()
    try:
        _assert(ws.run(*add_args("ready", priority="2", guard="true")).returncode == 0)
        _assert(ws.run(*add_args("guard-fails", priority="9", guard="false")).returncode == 0)
        _assert(ws.run(*add_args("skips", priority="5", skip_if="true")).returncode == 0)
        res = ws.run("eligible")
        _assert(res.returncode == 0, res.stderr)
        out = res.stdout
        _assert("guard-fails: guard failed" in out, out)
        _assert("skips: skip_if fired" in out, out)
        _assert("eligible: ready" in out, out)
        res = ws.run("eligible", "guard-fails")
        _assert(res.returncode == 1, "single-slug guard failure should exit nonzero")
    finally:
        ws.cleanup()


def test_eligible_steward_excludes_gated_entries():
    ws = Workspace()
    try:
        _assert(ws.run(*add_args("gated", priority="9", cheap_reversible="false")).returncode == 0)
        res = ws.run("eligible", "--steward")
        _assert(res.returncode == 1, "gated entry should not be steward-eligible")
        _assert("no eligible entry" in res.stdout, res.stdout)
        res = ws.run("eligible")
        _assert(res.returncode == 0, "director eligibility should still see the entry")
    finally:
        ws.cleanup()


def test_index_truncates_long_cells():
    ws = Workspace()
    try:
        long_guard = "test -e " + "x" * 200
        _assert(ws.run(*add_args("long", guard=long_guard)).returncode == 0)
        index = (ws.root / "on-deck" / "INDEX.md").read_text()
        _assert("…" in index, "long guard cell should be truncated")
        _assert("x" * 100 not in index, "full guard text should not appear in index")
    finally:
        ws.cleanup()


def test_section_ignores_fenced_headings():
    import importlib.util

    spec = importlib.util.spec_from_file_location("on_deck", SCRIPT)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    body = (
        "## Launch\n```bash\necho one\n## Check\necho two\n```\n\n"
        "## Check\nreal check\n\n## Status Log\n- t\n"
    )
    launch = mod.section(body, "Launch")
    _assert("echo two" in launch, f"launch truncated at fenced heading: {launch!r}")
    _assert(mod.section(body, "Check") == "real check", mod.section(body, "Check"))


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
