#!/usr/bin/env python3
"""Tests for scripts/tool-surprises — session-log surprise mining.

Covers the two heuristics the report's grouping depends on (command
signature extraction, error classification) and the fail→fix pairing
over a synthetic transcript; no real session logs are read.
"""

from __future__ import annotations

import importlib.machinery
import importlib.util
import json
import sys
import tempfile
import time
import traceback
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOL = REPO_ROOT / "scripts" / "tool-surprises"

_loader = importlib.machinery.SourceFileLoader("tool_surprises", str(TOOL))
_spec = importlib.util.spec_from_loader("tool_surprises", _loader)
ts = importlib.util.module_from_spec(_spec)
sys.modules["tool_surprises"] = ts
_loader.exec_module(ts)


def test_bash_signature() -> None:
    cases = {
        "rg -n foo topics/": "rg",
        "cd sub/dir && rg -n foo .": "rg",
        "git commit -m 'x'": "git commit",
        "VAR=1 env FOO=2 ./agentctl others id": "agentctl others",
        "D=$(mktemp -d /x/y-XXXX 2>/dev/null || mktemp -d) && echo $D": "mktemp",
        "python3 - <<'EOF'\nprint(1)\nEOF": "python3 -",
        'python3 -c "print(1)"': "python3 -c",
        "python3 -m json.tool f.json": "python3 -m json.tool",
        "sudo systemctl restart foo": "systemctl restart",
        "/usr/bin/ls -la": "ls",
        "": "(empty)",
    }
    for command, want in cases.items():
        got = ts.bash_signature(command)
        assert got == want, f"{command!r}: {got!r} != {want!r}"


def test_classify_error() -> None:
    cases = {
        "Exit code 127\nbash: command not found: ruff": "command-not-found",
        "Error: Exit code 2\nrg: x.md: No such file or directory": "missing-path",
        "Error: String to replace not found in file.": "edit-anchor",
        "Error: File has not been read yet.": "edit-before-read",
        "Error: Blocked: sleep 45 ... use Monitor with an": "harness-blocked",
        "Error: Exit code 144": "nonzero-exit",
        "usage: frob [-h]": "usage",
        "The user doesn't want to proceed": "interrupted",
        "something novel": "other",
    }
    for text, want in cases.items():
        got = ts.classify_error(text)
        assert got == want, f"{text!r}: {got!r} != {want!r}"


def _record(kind: str, content: list, extra: dict | None = None) -> str:
    rec = {
        "type": kind,
        "timestamp": "2026-08-18T00:00:00Z",
        "message": {"content": content},
    }
    if kind == "assistant":
        rec["message"]["model"] = "claude-fable-5"
    rec.update(extra or {})
    return json.dumps(rec)


def test_scan_and_recovery() -> None:
    lines = [
        _record(
            "assistant",
            [
                {
                    "type": "tool_use",
                    "id": "a",
                    "name": "Bash",
                    "input": {"command": "rg -n foo missing/"},
                }
            ],
        ),
        _record(
            "user",
            [
                {
                    "type": "tool_result",
                    "tool_use_id": "a",
                    "is_error": True,
                    "content": "x",
                }
            ],
            {
                "toolUseResult": "Error: Exit code 2\nrg: missing/: No such file or directory"
            },
        ),
        _record(
            "assistant",
            [
                {
                    "type": "tool_use",
                    "id": "b",
                    "name": "Bash",
                    "input": {"command": "rg -n foo topics/"},
                }
            ],
        ),
        _record(
            "user",
            [{"type": "tool_result", "tool_use_id": "b", "content": "hit"}],
            {"toolUseResult": {"stdout": "hit"}},
        ),
    ]
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "s.jsonl"
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        events, calls = ts.scan_session(path)
    assert calls == 2, calls
    fails = [e for e in events if not e["ok"]]
    assert len(fails) == 1 and fails[0]["err_class"] == "missing-path", fails
    assert fails[0]["exit"] == 2, fails[0]
    recovery = ts.find_recovery(events, fails[0])
    assert recovery is not None and recovery["command"] == "rg -n foo topics/", recovery


def main(argv: list[str]) -> int:
    verbose = "-v" in argv
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_")]
    passed = failed = 0
    failures = []
    start = time.time()
    for name, fn in tests:
        try:
            fn()
            passed += 1
            print(
                f"PASS  {name}" if verbose else ".",
                end="" if not verbose else "\n",
                flush=True,
            )
        except Exception:
            failed += 1
            failures.append((name, traceback.format_exc()))
            print(
                f"FAIL  {name}" if verbose else "F",
                end="" if not verbose else "\n",
                flush=True,
            )
    if not verbose:
        print()
    for name, tb in failures:
        print(f"\n--- {name} ---\n{tb}")
    print(f"\n{passed} passed, {failed} failed in {time.time() - start:.2f}s")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
