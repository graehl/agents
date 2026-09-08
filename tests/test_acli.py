#!/usr/bin/env python3
"""Tests for the stdlib-only ACLI helper package."""

from __future__ import annotations

import argparse
import contextlib
import importlib
import io
import json
import queue
import subprocess
import sys
import threading
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


def test_duration_seconds():
    for raw, expected in (
        ("300", 300),
        ("0", 0),
        ("-1", -1),
        ("0.25", 0.25),
        ("1e2", 100),
        ("5m", 300),
        ("10h", 36000),
        ("2d", 172800),
        ("2d1s", 172801),
        ("0.01m", 0.6),
        ("1h30m", 5400),
        (" 2H ", 7200),
    ):
        actual = _acli.args.duration_seconds(raw)
        _assert(actual == expected, f"{raw}: {actual} != {expected}")
    for raw in (
        "",
        "10 m",
        "2 d 1 s",
        "5ms",
        "1h garbage",
        "1m2",
        "nan",
        "inf",
        "1e999",
    ):
        try:
            _acli.args.duration_seconds(raw)
        except argparse.ArgumentTypeError:
            pass
        else:
            raise AssertionError(f"invalid duration accepted: {raw!r}")


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


def test_text_preference_is_available_without_a_text_renderer():
    parser = _acli.argument_parser()
    sub = parser.add_subparsers(dest="verb")
    child = sub.add_parser("status")
    _acli.add_standard_args(child)
    for argv in (
        ["--text", "status"],
        ["status", "--text"],
        ["status", "--format", "text"],
    ):
        parsed = parser.parse_args(argv)
        fmt = resolve_format(parsed)
        _assert(fmt is Format.TEXT)
        out = io.StringIO()
        _acli.emit({"ok": True}, fmt, out)
        _assert(json.loads(out.getvalue()) == {"ok": True})
        out = io.StringIO()
        _acli.emit({"ok": True}, fmt, out, text="Ready")
        _assert(out.getvalue() == "Ready\n")
    parsed = parser.parse_args(["--text", "status", "--json"])
    _assert(resolve_format(parsed) is Format.COMPACT)


def test_empty_results_are_explicit_in_both_json_formats() -> None:
    for fmt in (Format.COMPACT, Format.PRETTY):
        for value in ([], ()):
            out = io.StringIO()
            _acli.emit(value, fmt, out)
            _assert(json.loads(out.getvalue()) == [])
            _assert(out.getvalue().endswith("\n"))


def test_commentary_round_trip_and_data_only_output():
    source = {"id": 1, "nested": {"ok": True}}
    attached = _acli.commentary("Checked this item.", value=source)
    rows = [attached, _acli.commentary("Finished.")]
    out = io.StringIO()
    _acli.emit(rows, Format.COMPACT, out)
    parsed = [json.loads(line) for line in out.getvalue().splitlines()]
    _assert(parsed == rows)
    _assert("_acli" not in source, "attaching commentary must not mutate data")
    out = io.StringIO()
    _acli.emit(rows, Format.COMPACT, out, commentary=False)
    _assert(json.loads(out.getvalue()) == source)


def test_json_rejects_non_finite_numbers_before_writing_the_value() -> None:
    for fmt in (Format.COMPACT, Format.PRETTY):
        for number in (float("nan"), float("inf"), float("-inf")):
            out = io.StringIO()
            try:
                _acli.emit({"first": "valid", "nested": [number]}, fmt, out)
            except ValueError:
                _assert(out.getvalue() == "", "invalid JSON must not be partly written")
            else:
                raise AssertionError(f"accepted non-finite number in {fmt}")
    out = io.StringIO()
    try:
        _acli.emit([{"ok": 1}, {"bad": float("nan")}], Format.COMPACT, out)
    except ValueError:
        _assert(out.getvalue() == '{"ok":1}\n', "retain completed prior records")
    else:
        raise AssertionError("accepted invalid trailing record")


def test_commentary_flag_survives_subcommands_and_repeated_parses():
    parser = _acli.argument_parser(capabilities=("complete", "+commentary"))
    _acli.add_standard_args(parser)
    child = parser.add_subparsers(dest="verb").add_parser("show")
    _acli.add_standard_args(child)
    for argv in (["--no-commentary", "show"], ["show", "--no-commentary"]):
        args = parser.parse_args(argv)
        _assert(args.no_commentary)
        out = io.StringIO()
        _acli.emit(
            _acli.commentary("Done.", value={"ok": True}),
            resolve_format(args),
            out,
            commentary=not args.no_commentary,
        )
        _assert(json.loads(out.getvalue()) == {"ok": True})
    _assert(not parser.parse_args(["show"]).no_commentary)
    _assert("--no-commentary" in parser.format_help())
    _assert("presentation" in child.format_help())
    rows = _complete_lines(importlib.import_module("acli.args"), parser, ["--no-c"])
    _assert([row["completion"] for row in rows] == ["--no-commentary"])


def test_nested_commentary_preserves_order_and_data_structure():
    value = {
        "z": _acli.commentary("Z checked.", value={"id": 1}),
        "a": [0, _acli.commentary("About zero."), {}],
        "commentary": "ordinary data",
        "literal": '{"_acli":{"commentary":[{"text":"literal"}]}}',
    }
    out = io.StringIO()
    _acli.emit(value, Format.PRETTY, out)
    parsed = json.loads(out.getvalue())
    _assert(list(parsed) == list(value), "commentary traversal preserves member order")
    _assert(parsed == value)
    out = io.StringIO()
    _acli.emit(value, Format.PRETTY, out, commentary=False)
    cleaned = json.loads(out.getvalue())
    _assert(cleaned["z"] == {"id": 1})
    _assert(cleaned["a"] == [0, {}, {}], "nested array positions remain intact")
    _assert(cleaned["commentary"] == value["commentary"])
    _assert(cleaned["literal"] == value["literal"])
    _assert("_acli" in value["z"], "suppression must not mutate the caller's data")


def test_commentary_preserves_markdown_exactly():
    prose = "  [report](./report.html)\n\n$x^2$ — café\n\n$$\\sum_i x_i$$\n"
    value = _acli.commentary(prose)
    for fmt in (Format.COMPACT, Format.PRETTY):
        out = io.StringIO()
        _acli.emit(value, fmt, out)
        _assert(json.loads(out.getvalue())["_acli"]["commentary"][0]["text"] == prose)


def test_commentary_rejects_malformed_reserved_metadata_before_writing():
    for metadata in (None, {}, {"commentary": []}, {"commentary": [{"text": 4}]}):
        out = io.StringIO()
        try:
            _acli.emit({"nested": {"_acli": metadata}}, Format.COMPACT, out)
        except ValueError:
            _assert(out.getvalue() == "")
        else:
            raise AssertionError(f"accepted malformed metadata: {metadata!r}")
    for texts in ((), ("",), (" ",), (None,)):
        try:
            _acli.commentary(*texts)
        except ValueError:
            pass
        else:
            raise AssertionError(f"accepted invalid commentary: {texts!r}")
    once = _acli.commentary("First.", value={"id": 1})
    twice = _acli.commentary("Second.", value=once)
    _assert(
        [item["text"] for item in twice["_acli"]["commentary"]] == ["First.", "Second."]
    )
    _assert(len(once["_acli"]["commentary"]) == 1)


def test_commentary_non_json_output_requires_explicit_suppression():
    value = _acli.commentary("Checked.", value={"id": 1})
    for fmt, data, text in (
        (Format.TEXT, value, "Ready"),
        (Format.TOON, [value], None),
    ):
        out = io.StringIO()
        try:
            _acli.emit(data, fmt, out, text=text)
        except ValueError as exc:
            _assert("--no-commentary" in str(exc))
            _assert(out.getvalue() == "")
        else:
            raise AssertionError("non-JSON output silently lost commentary")
        _acli.emit(data, fmt, out, text=text, commentary=False)
        _assert("_acli" not in out.getvalue())
    out = io.StringIO()
    _acli.emit(value, Format.TEXT, out)
    _assert(json.loads(out.getvalue()) == value, "text without renderer stays JSONL")


def _commentary_demo(argv):
    parser = _acli.argument_parser(capabilities=("complete", "+commentary"))
    _acli.add_standard_args(parser)
    parser.add_argument("--pause", action="store_true")
    _acli.maybe_complete(parser, ["demo", *argv])
    args = parser.parse_args(argv)
    fmt = resolve_format(args)
    _acli.emit(
        _acli.commentary("Checked item.", value={"id": 1}),
        fmt,
        commentary=not args.no_commentary,
    )
    if args.pause:
        input()
    _acli.emit(_acli.commentary("Finished."), fmt, commentary=not args.no_commentary)
    return 0


def test_commentary_real_cli_flag_and_completion():
    command = [sys.executable, str(Path(__file__).resolve()), "--commentary-demo"]
    enabled = subprocess.run(
        [*command, "--json"], capture_output=True, text=True, timeout=10, check=True
    )
    disabled = subprocess.run(
        [*command, "--json", "--no-commentary"],
        capture_output=True,
        text=True,
        timeout=10,
        check=True,
    )
    records = [json.loads(line) for line in enabled.stdout.splitlines()]
    _assert(
        [row["_acli"]["commentary"][0]["text"] for row in records]
        == ["Checked item.", "Finished."]
    )
    _assert(json.loads(disabled.stdout) == {"id": 1})
    completion = subprocess.run(
        [*command, "--acli-complete", "--no-c"],
        capture_output=True,
        text=True,
        timeout=10,
        check=True,
    )
    _assert(json.loads(completion.stdout)["completion"] == "--no-commentary")
    _assert(completion.stderr == "")


def test_real_cli_usage_errors_are_structured_and_help_uses_stdout() -> None:
    command = [sys.executable, str(Path(__file__).resolve()), "--commentary-demo"]
    for argv in (
        ["--unknown-acli-probe"],
        ["--format", "invalid"],
        ["--format"],
        ["--json", "--pretty"],
    ):
        result = subprocess.run(
            [*command, *argv], capture_output=True, text=True, timeout=10
        )
        _assert(result.returncode == 2 and result.stdout == "", result)
        failure = json.loads(result.stderr.splitlines()[-1])
        _assert(failure["exit_code"] == 2 and failure["ok"] is False)
        _assert(failure["error"]["code"] == "usage")
        _assert(failure["error"]["message"])
        _assert("usage:" in failure["error"]["detail"]["usage"])
    help_result = subprocess.run(
        [*command, "--help"], capture_output=True, text=True, timeout=10
    )
    _assert(help_result.returncode == 0 and help_result.stderr == "")
    _assert(help_result.stdout.rstrip().endswith("acli: 1 complete +commentary"))


def test_commentary_flushes_before_the_tool_finishes():
    command = [
        sys.executable,
        str(Path(__file__).resolve()),
        "--commentary-demo",
        "--json",
        "--pause",
    ]
    with subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ) as process:
        lines = queue.Queue()
        reader = threading.Thread(
            target=lambda: lines.put(process.stdout.readline()), daemon=True
        )
        reader.start()
        try:
            line = lines.get(timeout=5)
            reader.join(timeout=1)
            _assert(
                json.loads(line)["_acli"]["commentary"][0]["text"] == "Checked item."
            )
            _assert(process.poll() is None, "commentary arrives before process exit")
            tail, _ = process.communicate("\n", timeout=5)
            _assert(process.returncode == 0)
            _assert(json.loads(tail)["_acli"]["commentary"][0]["text"] == "Finished.")
        finally:
            if process.poll() is None:
                process.kill()
                process.communicate(timeout=5)
            reader.join(timeout=1)


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


def test_error_details_reject_non_finite_json_without_partial_output() -> None:
    out = io.StringIO()
    try:
        die("bad data", ExitCode.DATA, detail={"value": float("nan")}, out=out)
    except ValueError:
        _assert(out.getvalue() == "")
    except SystemExit as exc:
        raise AssertionError("invalid error detail was serialized") from exc
    else:
        raise AssertionError("non-finite error detail must fail serialization")


def _demo_name_completer(prefix, tokens):
    del tokens
    entries = ["alpha", "beta", {"completion": "gamma"}]
    return [
        entry
        for entry in entries
        if (entry["completion"] if isinstance(entry, dict) else entry).startswith(
            prefix
        )
    ]


def test_standard_flag_arity_covers_every_flag_add_standard_args_adds():
    args_mod = importlib.import_module("acli.args")
    parser = args_mod.argument_parser(prog="arity", add_help=False)
    args_mod.add_standard_args(parser, allow_toon=True)
    declared = {
        option: 1 if action.nargs != 0 else 0
        for action in parser._actions
        for option in action.option_strings
    }
    _assert(
        args_mod.standard_flag_arity() == declared,
        f"a standard flag with no arity entry is invisible to launcher verb "
        f"dispatch: {declared} vs {args_mod.standard_flag_arity()}",
    )


def test_skip_standard_flags_consumes_values_in_both_spellings():
    skip = importlib.import_module("acli.args").skip_standard_flags
    _assert(skip(["--format", "pretty", "show", "x"]) == 2)
    _assert(skip(["--format=pretty", "show", "x"]) == 1)
    _assert(skip(["--json", "--pretty", "--full", "show", "x"]) == 3)
    _assert(skip(["show", "--pretty", "x"]) == 0, "only leading flags are skipped")
    _assert(skip([]) == 0)
    _assert(skip(["--format"]) == 2, "a dangling value slot leaves nothing behind")


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
    sub.add_parser("_internal", help=argparse.SUPPRESS)
    return args_mod, parser


def _complete_lines(args_mod, parser, tokens):
    out = io.StringIO()
    args_mod.complete(parser, tokens, out)
    return [json.loads(line) for line in out.getvalue().splitlines()]


def test_complete_subcommands_flags_and_values():
    args_mod, parser = _completion_parser()
    rows = _complete_lines(args_mod, parser, [""])
    # Declaration order, not alphabetical: emission order is the contract.
    _assert([r["completion"] for r in rows] == ["show", "list"], rows)
    _assert(all(r["kind"] == "subcommand" for r in rows))
    _assert(rows[0]["help"] == "Show one record.", rows)

    rows = _complete_lines(args_mod, parser, ["--f"])
    _assert([r["completion"] for r in rows] == ["--format", "--full"], rows)

    rows = _complete_lines(args_mod, parser, ["--j"])
    _assert([r["completion"] for r in rows] == ["--json"], rows)

    rows = _complete_lines(args_mod, parser, ["show", "a"])
    _assert([r["completion"] for r in rows] == ["alpha"], rows)

    rows = _complete_lines(args_mod, parser, ["show", "alpha", "--mode", ""])
    _assert([r["completion"] for r in rows] == ["brief", "wide"], rows)

    rows = _complete_lines(args_mod, parser, ["show", "alpha", "--mode=w"])
    _assert([r["completion"] for r in rows] == ["--mode=wide"], rows)


def test_complete_multi_value_option_tracks_argparse_cardinality():
    args_mod = importlib.import_module("acli.args")
    parser = args_mod.argument_parser(prog="multi")
    parser.add_argument("--pair", nargs=2, choices=["alpha", "beta"])
    parser.add_argument("--maybe", nargs="?", choices=["yes", "no"])
    parser.add_argument("--other", choices=["left", "right"])

    rows = _complete_lines(args_mod, parser, ["--pair", "alpha", ""])
    _assert(
        [row["completion"] for row in rows] == ["alpha", "beta"],
        "the second value of nargs=2 still belongs to --pair",
    )
    rows = _complete_lines(args_mod, parser, ["--maybe", "--other", ""])
    _assert(
        [row["completion"] for row in rows] == ["left", "right"],
        "a new option ends an optional-value slot",
    )


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


def test_complete_value_rows_do_not_inherit_action_help():
    args_mod, parser = _completion_parser()
    rows = _complete_lines(args_mod, parser, ["show", "alpha", "--mode", ""])
    _assert(all("help" not in r for r in rows), rows)


def test_complete_hint_nospace_and_order():
    args_mod = importlib.import_module("acli.args")
    parser = args_mod.argument_parser(prog="demo2")
    sub = parser.add_subparsers(dest="verb")
    query = sub.add_parser("q")
    filters = query.add_argument("filters", nargs="*")

    def completer(prefix, tokens):
        del tokens
        rows = [args_mod.hint("FIELD=VALUE filters; bare words search")]
        for field in ("tier", "section"):  # declaration order, not alphabetical
            if field.startswith(prefix):
                rows.append({"completion": f"{field}=", "nospace": True})
        return rows

    args_mod.set_completer(filters, completer)
    rows = _complete_lines(args_mod, parser, ["q", ""])
    _assert(rows[0]["kind"] == "hint" and rows[0]["completion"] == "", rows)
    _assert([r["completion"] for r in rows[1:]] == ["tier=", "section="], rows)
    _assert(all(r.get("nospace") is True for r in rows[1:]), rows)
    _assert("help" not in rows[1], "value rows carry only completer-provided help")


def test_complete_preserves_completer_order_and_dedupes():
    args_mod = importlib.import_module("acli.args")
    parser = args_mod.argument_parser(prog="demo3")
    sub = parser.add_subparsers(dest="verb")
    show = sub.add_parser("s")
    name = show.add_argument("name")
    args_mod.set_completer(name, lambda prefix, tokens: ["beta", "alpha", "beta"])
    rows = _complete_lines(args_mod, parser, ["s", ""])
    _assert([r["completion"] for r in rows] == ["beta", "alpha"], rows)


def test_capability_line_and_exit_code_footer():
    args_mod = importlib.import_module("acli.args")
    parser = args_mod.argument_parser(
        prog="demo4",
        capabilities=("complete", "repl"),
        exit_codes={0: "success", 4: "no such record"},
    )
    sub = parser.add_subparsers(dest="verb")
    show = sub.add_parser("show", help="Show one record.")
    text = parser.format_help()
    _assert(text.rstrip().endswith("acli: 1 complete repl"), text)
    _assert("exit codes:" in text and "4  no such record" in text, text)
    _assert(
        "acli: 1 complete repl" in show.format_help(),
        "subcommand help repeats the parent capability line",
    )


def test_empty_capabilities_render_bare_baseline_line():
    args_mod = importlib.import_module("acli.args")
    parser = args_mod.argument_parser(prog="demo-bare", capabilities=())
    _assert(
        parser.format_help().rstrip().endswith("acli: 1"),
        "capabilities=() still claims the version baseline",
    )


def _parse_with_banner(args_mod, argv, env_quiet=None):
    import os

    args_mod._banner_emitted = False
    parser = args_mod.argument_parser(
        prog="demo-banner", capabilities=("complete", "+toon")
    )
    parser.add_argument("--x", action="store_true")
    saved = os.environ.get(args_mod.QUIET_ENV)
    try:
        if env_quiet is None:
            os.environ.pop(args_mod.QUIET_ENV, None)
        else:
            os.environ[args_mod.QUIET_ENV] = env_quiet
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            parser.parse_args(argv)
        return err.getvalue()
    finally:
        if saved is None:
            os.environ.pop(args_mod.QUIET_ENV, None)
        else:
            os.environ[args_mod.QUIET_ENV] = saved
        args_mod._banner_emitted = False


def test_parse_args_banners_once_on_stderr():
    args_mod = importlib.import_module("acli.args")
    _assert(
        _parse_with_banner(args_mod, ["--x"]) == "# acli: 1 complete +toon\n",
        "banner is the #-prefixed capability line on stderr",
    )
    args_mod._banner_emitted = False
    parser = args_mod.argument_parser(prog="demo-once", capabilities=())
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        parser.parse_args([])
        parser.parse_args([])
    _assert(err.getvalue() == "# acli: 1\n", "banner emits once per process")
    args_mod._banner_emitted = False


def test_banner_suppressed_by_flag_and_env():
    args_mod = importlib.import_module("acli.args")
    _assert(
        _parse_with_banner(args_mod, ["--acli-quiet"]) == "",
        "--acli-quiet suppresses the banner",
    )
    _assert(
        _parse_with_banner(args_mod, [], env_quiet="1") == "",
        "ACLI_QUIET suppresses the banner",
    )


def test_banner_quiet_flag_survives_subparser_namespace_copy():
    args_mod = importlib.import_module("acli.args")
    args_mod._banner_emitted = False
    parser = args_mod.argument_parser(prog="demo-sub-quiet", capabilities=())
    sub = parser.add_subparsers(dest="verb", required=True)
    sub.add_parser("list")
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        parser.parse_args(["--acli-quiet", "list"])
    _assert(
        err.getvalue() == "",
        "pre-verb --acli-quiet suppresses despite subparser defaults",
    )
    args_mod._banner_emitted = False


def test_completion_runs_never_banner():
    args_mod = importlib.import_module("acli.args")
    args_mod._banner_emitted = False
    parser = args_mod.argument_parser(prog="demo-complete-quiet")
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stderr(err):
        try:
            args_mod.maybe_complete(parser, ["demo", args_mod.COMPLETE_FLAG, "-"], out)
            _assert(False, "maybe_complete must exit")
        except SystemExit as exc:
            _assert(exc.code == 0, exc)
    _assert(err.getvalue() == "", "completion is banner-free")
    args_mod._banner_emitted = False


def _repl_parser(formats):
    args_mod = importlib.import_module("acli.args")
    parser = args_mod.argument_parser(prog="demo5")
    sub = parser.add_subparsers(dest="verb")
    runner = sub.add_parser("run")
    args_mod.add_standard_args(runner)

    def record(parsed):
        formats.append(parsed.format)
        return 0

    runner.set_defaults(func=record)
    boom = sub.add_parser("boom")

    def fail(parsed):
        del parsed
        raise SystemExit(4)

    boom.set_defaults(func=fail)
    return parser


def test_repl_executes_lines_with_pretty_default():
    shell = importlib.import_module("acli.shell")
    formats = []
    parser = _repl_parser(formats)
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        status = shell.run(
            parser,
            input_lines=["run", "run --compact", "bogus", "exit", "run"],
        )
    _assert(status == 0)
    _assert(formats == ["pretty", "compact"], formats)
    _assert("# exit 2" in err.getvalue(), err.getvalue())


def test_repl_catches_die_and_reports_status():
    shell = importlib.import_module("acli.shell")
    parser = _repl_parser([])
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        _assert(shell.run(parser, input_lines=["boom", "", "quit"]) == 0)
    _assert("# exit 4" in err.getvalue(), err.getvalue())


def test_repl_rewrite_binds_a_personality():
    shell = importlib.import_module("acli.shell")
    formats = []
    parser = _repl_parser(formats)

    def rewrite(tokens):
        if tokens and tokens[0] == "go":
            return ["run", *tokens[1:]]
        return tokens

    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        status = shell.run(parser, input_lines=["go", "exit"], rewrite=rewrite)
    _assert(status == 0)
    _assert(formats == ["pretty"], "rewritten line executes the bound verb")

    def prefix_run(tokens):
        if tokens and tokens[0] not in ("run", "boom"):
            return ["run", *tokens]
        return tokens

    rows = shell._completion_rows(parser, [""], prefix_run)
    _assert(
        [r["completion"] for r in rows] == ["run", "boom"],
        "bound completion falls back to the raw grammar's candidates",
    )


def test_repl_missing_dependency_advice_names_installer():
    shell = importlib.import_module("acli.shell")
    advice = shell.install_advice()
    _assert("pip install" in advice and "prompt_toolkit" in advice, advice)


def test_maybe_repl_only_fires_on_argv1():
    args_mod = importlib.import_module("acli.args")
    parser = args_mod.argument_parser(prog="demo7")
    _assert(args_mod.maybe_repl(parser, ["demo7", "list"]) is None)


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
    if sys.argv[1:2] == ["--commentary-demo"]:
        sys.exit(_commentary_demo(sys.argv[2:]))
    sys.exit(main(sys.argv[1:]))
