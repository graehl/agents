#!/usr/bin/env python3
"""Tests for scripts/intervention-needles — first-pass correction needles.

Covers needle matching, both harness parsers, context capture, and the
real CLI over synthetic transcripts; no real session logs are read.
"""

from __future__ import annotations

import importlib.machinery
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import time
import traceback
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOL = REPO_ROOT / "scripts" / "intervention-needles"

_loader = importlib.machinery.SourceFileLoader("intervention_needles", str(TOOL))
_spec = importlib.util.spec_from_loader("intervention_needles", _loader)
assert _spec is not None
needles = importlib.util.module_from_spec(_spec)
sys.modules["intervention_needles"] = needles
_loader.exec_module(needles)


def test_match_needle() -> None:
    cases = {
        "bad": "bad",
        "Bad! wrong file": "bad",
        "bad idea to rebase": "bad",
        "🎤 Bad. that broke it": "bad",
        "[ASR] bad, revert that": "bad",
        "no": "no",
        "No.": "no",
        "no, the other branch": "no",
        "  'no!' lol": "no",
        "no\nuse the other flag": "no",
        "[ASR] No, keep it": "no",
        "no need to rerun": None,
        "nope": None,
        "know what": None,
        "badge colors": None,
        "it is bad": None,
        "[ASR] okay, now no": None,
        "": None,
    }
    for text, want in cases.items():
        got = needles.match_needle(text)
        assert got == want, f"{text!r}: {got!r} != {want!r}"


def _claude(kind: str, content: object, **extra: object) -> str:
    rec = {
        "type": kind,
        "timestamp": extra.pop("ts", "2026-10-03T00:00:00Z"),
        "message": {"content": content},
    }
    rec.update(extra)
    return json.dumps(rec)


def _claude_session() -> list[str]:
    return [
        _claude("user", "rename the flag"),
        _claude(
            "assistant",
            [{"type": "text", "text": "Should I also rename the env var?"}],
        ),
        _claude("user", "no, just the flag", ts="2026-10-03T00:01:00Z"),
        _claude(
            "assistant",
            [
                {"type": "text", "text": "Renaming only the flag."},
                {
                    "type": "tool_use",
                    "id": "t1",
                    "name": "Edit",
                    "input": {"file_path": "/repo/cli.py"},
                },
            ],
        ),
        _claude(
            "user",
            [{"type": "tool_result", "tool_use_id": "t1", "content": "no, failed"}],
        ),
        _claude("user", [{"type": "text", "text": "no. skill text"}], isMeta=True),
        _claude("user", "no, subagent prompt", isSidechain=True),
        json.dumps(
            {
                "type": "attachment",
                "timestamp": "2026-10-03T00:02:00Z",
                "attachment": {
                    "type": "queued_command",
                    "commandMode": "prompt",
                    "prompt": "Bad! that was the wrong file",
                },
            }
        ),
        _claude(
            "assistant",
            [
                {
                    "type": "tool_use",
                    "id": "t2",
                    "name": "Bash",
                    "input": {"command": "git restore -- cli.py"},
                }
            ],
        ),
    ]


def _write(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def test_scan_claude_context() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "s1.jsonl"
        _write(path, _claude_session())
        c = needles.scan_claude(path, "s1")
    assert c.user_turns == 3, c.user_turns
    assert [x["needle"] for x in c.candidates] == ["no", "bad"], c.candidates
    no, bad = c.candidates
    assert no["prior_asked"] is True, no
    assert no["next_reply"] == "Renaming only the flag.", no
    assert no["next_actions"] == ["Edit /repo/cli.py"], no
    assert bad["prior_asked"] is False, bad
    assert bad["next_actions"] == ["Bash git restore -- cli.py"], bad


def _codex(item_type: str, **payload: object) -> str:
    return json.dumps(
        {
            "type": "response_item",
            "timestamp": "2026-10-03T00:00:00Z",
            "payload": {"type": item_type, **payload},
        }
    )


def test_scan_codex_context() -> None:
    lines = [
        json.dumps({"type": "session_meta", "payload": {"id": "c1", "cwd": "/x"}}),
        _codex(
            "message",
            role="user",
            content=[{"type": "input_text", "text": "# AGENTS.md instructions"}],
        ),
        _codex(
            "message",
            role="assistant",
            content=[{"type": "output_text", "text": "Patched the parser."}],
        ),
        _codex(
            "message",
            role="user",
            content=[{"type": "input_text", "text": "bad: you edited the test"}],
        ),
        _codex(
            "function_call",
            name="exec_command",
            arguments=json.dumps({"cmd": "git diff"}),
        ),
    ]
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "rollout.jsonl"
        _write(path, lines)
        c = needles.scan_codex(path, "c1")
    assert c.user_turns == 2, c.user_turns
    assert len(c.candidates) == 1, c.candidates
    cand = c.candidates[0]
    assert cand["needle"] == "bad"
    assert cand["prior_assistant"] == "Patched the parser."
    assert cand["next_actions"] == ["exec_command git diff"], cand


def test_cli_scopes_project_and_skips_current_session() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        project = (home / "project").resolve()
        project.mkdir()
        tdir = home / ".claude" / "projects" / str(project).replace("/", "-")
        _write(tdir / "s1.jsonl", _claude_session())
        _write(tdir / "current.jsonl", [_claude("user", "no, ignore me")])
        other = home / ".claude" / "projects" / "-elsewhere"
        _write(other / "s9.jsonl", [_claude("user", "bad, other project")])
        env = {
            **os.environ,
            "HOME": str(home),
            "CLAUDE_CODE_SESSION_ID": "current",
            "ACLI_QUIET": "1",
        }
        env.pop("AGENTCTL_SESSION_ID", None)
        run = subprocess.run(
            [str(TOOL), "--project", str(project), "--harness", "claude", "--json"],
            capture_output=True,
            text=True,
            env=env,
            check=False,
        )
        assert run.returncode == 0, run.stderr
        rows = [json.loads(line) for line in run.stdout.splitlines()]
        summary, *cands = rows
        assert summary["sessions_scanned"] == {"claude": 1}, summary
        assert summary["candidates"] == {"bad": 1, "no": 1}, summary
        assert [c["needle"] for c in cands] == ["bad", "no"], cands  # newest first
        assert all(c["session"] == "s1" for c in cands), cands

        everywhere = subprocess.run(
            [str(TOOL), "--all-projects", "--harness", "all", "--needle", "bad"],
            capture_output=True,
            text=True,
            env=env,
            check=False,
        )
        assert everywhere.returncode == 0, everywhere.stderr
        summary = json.loads(everywhere.stdout.splitlines()[0])
        assert summary["candidates"] == {"bad": 2}, summary
        assert summary["harnesses_missing"] == {
            "codex": str(home / ".codex" / "sessions")
        }, summary


def test_cli_fails_when_no_harness_has_logs() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        env = {**os.environ, "HOME": tmp, "ACLI_QUIET": "1"}
        run = subprocess.run(
            [str(TOOL), "--all-projects"],
            capture_output=True,
            text=True,
            env=env,
            check=False,
        )
    assert run.returncode == 4, (run.returncode, run.stderr)
    envelope = json.loads(run.stderr.strip().splitlines()[-1])
    assert envelope["error"]["code"] == "not_found", envelope


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
