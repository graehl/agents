#!/usr/bin/env python3
"""Tests for the stdlib-only ACLI helper package."""

from __future__ import annotations

import io
import importlib
import json
import sys
import time
import traceback
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

_acli = importlib.import_module("acli")
_emit = importlib.import_module("acli.emit")
ExitCode = _acli.ExitCode
Format = _acli.Format
die = _acli.die
is_agent_session = _acli.is_agent_session
resolve_format = _acli.resolve_format
write_jsonl = _emit.write_jsonl
write_pretty = _emit.write_pretty
write_toon_table = _emit.write_toon_table


class FakeStdout:
    def __init__(self, tty: bool):
        self.tty = tty

    def isatty(self) -> bool:
        return self.tty


class Args:
    def __init__(self, fmt=None, allow_toon: bool = False):
        self.format = fmt
        self.acli_toon_allowed = allow_toon


def _assert(cond, msg="assertion failed"):
    if not cond:
        raise AssertionError(msg)


def test_is_agent_session_disjunction():
    _assert(not is_agent_session(FakeStdout(True), {}), "plain TTY should be human")
    _assert(is_agent_session(FakeStdout(False), {}), "non-TTY stdout should be agent")
    _assert(is_agent_session(FakeStdout(True), {"AGENT_GUARD": "1"}))
    _assert(is_agent_session(FakeStdout(True), {"CLAUDE_CODE_SESSION_ID": "s"}))
    _assert(is_agent_session(FakeStdout(True), {"CODEX_THREAD_ID": "t"}))
    _assert(is_agent_session(FakeStdout(True), {"PI_CODING_AGENT": "1"}))


def test_resolve_format_flags_override_detection():
    _assert(resolve_format(Args(), FakeStdout(False), {}) is Format.COMPACT)
    _assert(resolve_format(Args("pretty"), FakeStdout(False), {}) is Format.PRETTY)
    _assert(resolve_format(Args("compact"), FakeStdout(True), {}) is Format.COMPACT)
    _assert(resolve_format(Args("jsonl"), FakeStdout(True), {}) is Format.COMPACT)
    _assert(
        resolve_format(Args("toon", allow_toon=True), FakeStdout(False), {})
        is Format.TOON
    )
    try:
        resolve_format(Args("toon"), FakeStdout(False), {})
    except ValueError as exc:
        _assert("table-producing" in str(exc))
    else:
        raise AssertionError(
            "--toon should fail when the subcommand is not a table producer"
        )


def test_jsonl_and_pretty_emit_parseable_json():
    out = io.StringIO()
    write_jsonl([{"b": 2, "a": 1}, {"a": 3}], out)
    lines = out.getvalue().splitlines()
    _assert([json.loads(line) for line in lines] == [{"a": 1, "b": 2}, {"a": 3}])

    out = io.StringIO()
    write_pretty({"b": 2, "a": 1}, out)
    _assert(json.loads(out.getvalue()) == {"a": 1, "b": 2})
    _assert("\n  " in out.getvalue(), "pretty JSON should be indented")


def test_toon_table_quotes_scalars_and_preserves_inner_spaces():
    rows = [
        {"id": 1, "name": "Alice Smith", "note": "hello, world", "literal": "true"},
        {"id": 2, "name": "Bob", "note": " padded ", "literal": "05"},
    ]
    out = io.StringIO()
    write_toon_table(rows, out=out)
    _assert(
        out.getvalue()
        == (
            "items[2]{id,name,note,literal}:\n"
            '  1,Alice Smith,"hello, world","true"\n'
            '  2,Bob," padded ","05"\n'
        )
    )


def test_toon_table_rejects_non_uniform_or_nested_rows():
    for rows in (
        [{"id": 1}, {"name": "missing id"}],
        [{"id": 1, "nested": {"x": 2}}],
    ):
        try:
            write_toon_table(rows, out=io.StringIO())
        except (TypeError, ValueError):
            pass
        else:
            raise AssertionError(f"TOON table should reject {rows!r}")


def test_toon_table_rejects_lone_surrogate_strings():
    try:
        write_toon_table([{"bad": "\ud800"}], out=io.StringIO())
    except ValueError as exc:
        _assert("surrogates" in str(exc))
    else:
        raise AssertionError("TOON strings should reject lone surrogates")


def test_die_emits_structured_error_envelope():
    out = io.StringIO()
    try:
        die("bad flag", ExitCode.USAGE, out=out)
    except SystemExit as exc:
        _assert(exc.code == int(ExitCode.USAGE))
    else:
        raise AssertionError("die should raise SystemExit")
    payload = json.loads(out.getvalue())
    _assert(payload["ok"] is False)
    _assert(payload["error"]["code"] == "usage")
    _assert(payload["error"]["message"] == "bad flag")


def _demo_name_completer(prefix, tokens):
    del tokens
    entries = ["alpha", "beta", {"completion": "gamma"}]
    return [
        entry
        for entry in entries
        if (entry["completion"] if isinstance(entry, dict) else entry).startswith(prefix)
    ]


def _completion_parser():
    args_mod = importlib.import_module("acli.args")
    parser = args_mod.argument_parser(prog="demo")
    args_mod.add_standard_args(parser)
    sub = parser.add_subparsers(dest="verb")
    show = sub.add_parser("show", help="Show one record.")
    name_arg = show.add_argument("name", help="Dataset name.")
    args_mod.set_completer(name_arg, _demo_name_completer)
    show.add_argument("--mode", choices=["brief", "wide"], help="Detail level.")
    sub.add_parser("list", help="List records.")
    return args_mod, parser


def _complete_lines(args_mod, parser, tokens):
    out = io.StringIO()
    args_mod.complete(parser, tokens, out)
    return [json.loads(line) for line in out.getvalue().splitlines()]


def test_complete_subcommands_flags_and_values():
    args_mod, parser = _completion_parser()
    rows = _complete_lines(args_mod, parser, [""])
    _assert([r["completion"] for r in rows] == ["list", "show"], rows)
    _assert(all(r["kind"] == "subcommand" for r in rows))

    rows = _complete_lines(args_mod, parser, ["--f"])
    _assert([r["completion"] for r in rows] == ["--format", "--full"], rows)

    rows = _complete_lines(args_mod, parser, ["show", "a"])
    _assert([r["completion"] for r in rows] == ["alpha"], rows)

    rows = _complete_lines(args_mod, parser, ["show", "alpha", "--mode", ""])
    _assert([r["completion"] for r in rows] == ["brief", "wide"], rows)

    rows = _complete_lines(args_mod, parser, ["show", "alpha", "--mode=w"])
    _assert([r["completion"] for r in rows] == ["--mode=wide"], rows)


def test_complete_empty_is_definitive():
    args_mod, parser = _completion_parser()
    _assert(_complete_lines(args_mod, parser, ["show", "zzz"]) == [])
    _assert(_complete_lines(args_mod, parser, ["nonsense", "x"]) == [])


def test_maybe_complete_only_fires_on_argv1():
    args_mod, parser = _completion_parser()
    out = io.StringIO()
    _assert(args_mod.maybe_complete(parser, ["demo", "list"], out) is None)
    _assert(out.getvalue() == "")
    try:
        args_mod.maybe_complete(parser, ["demo", "--acli-complete", "sh"], out)
    except SystemExit as exc:
        _assert(exc.code == 0)
    else:
        raise AssertionError("maybe_complete should exit 0 after completing")
    rows = [json.loads(line) for line in out.getvalue().splitlines()]
    _assert([r["completion"] for r in rows] == ["show"], rows)


def _collect_tests():
    return [
        (name, fn)
        for name, fn in sorted(globals().items())
        if name.startswith("test_") and callable(fn)
    ]


def main(argv):
    verbose = "-v" in argv
    tests = _collect_tests()
    if "-k" in argv:
        idx = argv.index("-k")
        if idx + 1 < len(argv):
            needle = argv[idx + 1]
            tests = [(name, fn) for name, fn in tests if needle in name]

    passed = failed = 0
    failures = []
    start_total = time.time()
    for name, fn in tests:
        t0 = time.time()
        try:
            fn()
            passed += 1
            if verbose:
                print(f"PASS  {name}  ({time.time() - t0:.2f}s)")
            else:
                print(".", end="", flush=True)
        except Exception:
            failed += 1
            tb = traceback.format_exc()
            failures.append((name, tb))
            if verbose:
                print(f"FAIL  {name}  ({time.time() - t0:.2f}s)")
                print(tb)
            else:
                print("F", end="", flush=True)
    if not verbose:
        print()
    print()
    if failures:
        print(f"{'=' * 60}")
        print(f"{len(failures)} FAILURE(S):")
        for name, tb in failures:
            print(f"\n--- {name} ---")
            print(tb)
    print(f"\n{passed} passed, {failed} failed in {time.time() - start_total:.2f}s")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
