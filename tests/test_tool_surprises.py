#!/usr/bin/env python3
"""Tests for scripts/tool-surprises — session-log surprise mining.

Covers classification, fail→fix pairing, both harness parsers, yielded
results, Codex project discovery, and coverage diagnostics over synthetic
transcripts; no real session logs are read.
"""

from __future__ import annotations

import importlib.machinery
import importlib.util
import json
import os
import sys
import tempfile
import time
import traceback
from pathlib import Path
from types import SimpleNamespace

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOL = REPO_ROOT / "scripts" / "tool-surprises"

_loader = importlib.machinery.SourceFileLoader("tool_surprises", str(TOOL))
_spec = importlib.util.spec_from_loader("tool_surprises", _loader)
assert _spec is not None
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
        "Script error: exec cell 88 not found": "stale-handle",
        "write_stdin failed: Unknown process id 2509": "stale-handle",
        "Error: Exit code 2\nrg: x.md: No such file or directory": "missing-path",
        "Error: String to replace not found in file.": "edit-anchor",
        "apply_patch verification failed: Failed to find expected lines": "edit-anchor",
        "Error: File has not been read yet.": "edit-before-read",
        "Error: Blocked: sleep 45 ... use Monitor with an": "harness-blocked",
        "Error: Exit code 144": "nonzero-exit",
        "Process exited with code 7": "nonzero-exit",
        "usage: frob [-h]": "usage",
        "The user doesn't want to proceed": "interrupted",
        "aborted by user after 4.2s": "interrupted",
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


def _codex_record(item_type: str, **payload: object) -> str:
    return json.dumps(
        {
            "type": "response_item",
            "timestamp": "2026-08-18T00:00:00Z",
            "payload": {"type": item_type, **payload},
        }
    )


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


def test_scan_codex_commands_and_yielded_processes() -> None:
    def call(call_id: str, name: str, args: dict) -> str:
        return _codex_record(
            "function_call",
            call_id=call_id,
            name=name,
            arguments=json.dumps(args),
        )

    def result(call_id: str, output: str) -> str:
        return _codex_record("function_call_output", call_id=call_id, output=output)

    lines = [
        json.dumps({"type": "turn_context", "payload": {"model": "gpt-5.6-sol"}}),
        call("a", "exec_command", {"cmd": "rg -n foo missing/"}),
        result("a", "Process exited with code 2\nOutput:\nmissing path"),
        call("b", "exec_command", {"cmd": "rg -n foo topics/"}),
        result("b", "Process exited with code 0\nOutput:\nhit"),
        call("c", "exec_command", {"cmd": "pnpm test"}),
        result("c", "Process running with session ID 42\nLive output:\n..."),
        call("d", "write_stdin", {"session_id": 42, "chars": ""}),
        result("d", "Process exited with code 1\nFinal output:\nfailed"),
        call("e", "exec_command", {"cmd": "pnpm test"}),
        result("e", "Process exited with code 0\nFinal output:\npassed"),
        call("f", "wait", {"cell_id": 88}),
        result("f", "Script failed\nScript error:\nexec cell 88 not found"),
        call("g", "wait", {"cell_id": 89}),
        result("g", "Script completed\nOutput:\ndone"),
        call("h", "exec_command", {"cmd": "pnpm dev"}),
        result("h", "Process running with session ID 43\nLive output:\n..."),
        call("i", "write_stdin", {"session_id": 43, "chars": ""}),
        result("i", "Script failed\nScript error:\nUnknown process id 43"),
        call("j", "write_stdin", {"session_id": 44, "chars": ""}),
        result("j", "Process exited with code 0\nOutput:\ndone"),
    ]
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "rollout.jsonl"
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        events, calls, diagnostics = ts.scan_codex_session(path)
    assert calls == 10, calls
    assert diagnostics["standard_exec_command_calls"] == 5, diagnostics
    assert diagnostics["terminal_events"] == 8, diagnostics
    failures = [event for event in events if not event["ok"]]
    assert [event["sig"] for event in failures] == [
        "rg",
        "pnpm test",
        "wait",
        "write_stdin",
    ], failures
    assert failures[-2]["err_class"] == "stale-handle", failures[-2]
    assert failures[-2]["targets"] == ["cell:88"], failures[-2]
    assert failures[-1]["err_class"] == "stale-handle", failures[-1]
    assert failures[-1]["targets"] == ["process:43"], failures[-1]
    assert all(event["model"] == "gpt-5.6-sol" for event in events), events
    assert ts.find_recovery(events, failures[0])["command"] == "rg -n foo topics/"
    assert ts.find_recovery(events, failures[1])["command"] == "pnpm test"
    assert ts.find_recovery(events, failures[2]) is None
    assert ts.find_recovery(events, failures[3]) is None


def test_scan_codex_exec_and_patch_results() -> None:
    patch_program = (
        'const r = await tools.apply_patch("*** Begin Patch\\n'
        '*** Update File: /tmp/example.py\\n"); text(r);'
    )
    shell_program = (
        'const r = await tools.exec_command({"cmd":"rg -n foo topics/"}); '
        "text(r.output);"
    )

    def image_program(path: str) -> str:
        return f'const r = await tools.view_image({{path:"{path}"}}); image(r);'

    lines = [
        _codex_record(
            "custom_tool_call", call_id="a", name="exec", input=patch_program
        ),
        _codex_record(
            "custom_tool_call_output",
            call_id="a",
            output=(
                "Script failed\nOutput:\nScript error:\n"
                "apply_patch verification failed: Failed to find expected lines in "
                "/tmp/example.py:\nold line"
            ),
        ),
        _codex_record(
            "custom_tool_call",
            call_id="b",
            name="apply_patch",
            input="*** Begin Patch\n*** Update File: /tmp/example.py\n",
        ),
        _codex_record(
            "custom_tool_call_output",
            call_id="b",
            output="Exit code: 0\nOutput:\nSuccess. Updated file",
        ),
        _codex_record(
            "custom_tool_call", call_id="c", name="exec", input=shell_program
        ),
        _codex_record(
            "custom_tool_call_output",
            call_id="c",
            output="Script completed\nOutput:\nIf a command times out: report it",
        ),
        _codex_record(
            "custom_tool_call",
            call_id="d",
            name="exec",
            input=image_program("/tmp/missing.png"),
        ),
        _codex_record(
            "custom_tool_call_output",
            call_id="d",
            output=(
                "Script failed\nScript error:\nunable to locate image at "
                "`/tmp/missing.png`: No such file or directory"
            ),
        ),
        _codex_record(
            "custom_tool_call",
            call_id="e",
            name="exec",
            input=image_program("/tmp/other.png"),
        ),
        _codex_record(
            "custom_tool_call_output",
            call_id="e",
            output="Script completed\nOutput:\nimage",
        ),
        _codex_record(
            "custom_tool_call",
            call_id="f",
            name="exec",
            input=image_program("/tmp/missing.png"),
        ),
        _codex_record(
            "custom_tool_call_output",
            call_id="f",
            output="Script completed\nOutput:\nimage",
        ),
    ]
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "rollout.jsonl"
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        events, calls, diagnostics = ts.scan_codex_session(path)
    assert calls == 6, calls
    assert len(events) == 6, events
    failures = [event for event in events if not event["ok"]]
    patch_failure, image_failure = failures
    assert patch_failure["tool"] == "apply_patch", patch_failure
    assert patch_failure["targets"] == ["/tmp/example.py"], patch_failure
    assert patch_failure["err_class"] == "edit-anchor", patch_failure
    patch_recovery = ts.find_recovery(events, patch_failure)
    assert patch_recovery is not None and patch_recovery["tool"] == "apply_patch"
    assert image_failure["targets"] == ["/tmp/missing.png"], image_failure
    image_recovery = ts.find_recovery(events, image_failure)
    assert image_recovery is not None
    assert image_recovery["targets"] == ["/tmp/missing.png"], image_recovery
    assert diagnostics["custom_exec_scripts_with_opaque_command_status"] == 1
    assert events[2]["tool"] == "exec", events[2]


def test_codex_session_info() -> None:
    session_id = "019ff32e-d080-7753-b021-1bfc10996d96"
    line = json.dumps(
        {
            "type": "session_meta",
            "payload": {"id": session_id, "cwd": "/home/graehl/agents"},
        }
    )
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "rollout.jsonl"
        path.write_text(line + "\n", encoding="utf-8")
        got_id, cwd = ts.codex_session_info(path)
    assert got_id == session_id
    assert cwd == Path("/home/graehl/agents").resolve()


def test_build_codex_report() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        project = home / "project"
        other_project = home / "other"
        project.mkdir()
        other_project.mkdir()
        sessions = home / ".codex" / "sessions" / "2026" / "08" / "18"
        sessions.mkdir(parents=True)

        def write_rollout(path: Path, cwd: Path, failing: bool) -> None:
            lines = [
                json.dumps(
                    {
                        "type": "session_meta",
                        "payload": {"id": path.stem, "cwd": str(cwd)},
                    }
                ),
                _codex_record(
                    "function_call",
                    call_id="a",
                    name="exec_command",
                    arguments=json.dumps({"cmd": "rg -n foo missing/"}),
                ),
                _codex_record(
                    "function_call_output",
                    call_id="a",
                    output=(
                        "Process exited with code 2\nOutput:\nmissing path"
                        if failing
                        else "Process exited with code 0\nOutput:\nhit"
                    ),
                ),
                _codex_record(
                    "function_call",
                    call_id="b",
                    name="exec_command",
                    arguments=json.dumps({"cmd": "rg -n foo topics/"}),
                ),
                _codex_record(
                    "function_call_output",
                    call_id="b",
                    output="Process exited with code 0\nOutput:\nhit",
                ),
            ]
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")

        write_rollout(sessions / "wanted.jsonl", project, True)
        write_rollout(sessions / "other.jsonl", other_project, False)
        ns = SimpleNamespace(
            project=str(project),
            harness="codex",
            all_sessions=False,
            days=30,
            include_gated=False,
            min_fails=1,
            limit=20,
            full=False,
        )
        prior_home = os.environ.get("HOME")
        os.environ["HOME"] = str(home)
        try:
            summary, patterns, dropped = ts.build_report(ns)
        finally:
            if prior_home is None:
                del os.environ["HOME"]
            else:
                os.environ["HOME"] = prior_home

    assert summary["sessions_scanned"] == 1, summary
    assert summary["tool_calls"] == 2, summary
    assert summary["failures"] == 1, summary
    assert summary["coverage"]["standard_exec_command_calls"] == 2, summary
    assert len(patterns) == 1 and patterns[0]["recovered"] == 1, patterns
    assert dropped == 0


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
