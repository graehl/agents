from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Callable, Iterable, TextIO


class ArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("formatter_class", argparse.RawTextHelpFormatter)
        super().__init__(*args, **kwargs)


def argument_parser(*args, **kwargs) -> ArgumentParser:
    return ArgumentParser(*args, **kwargs)


def add_standard_args(
    parser: argparse.ArgumentParser, *, allow_toon: bool = False
) -> None:
    """Add ACLI output flags to an argparse parser."""
    if getattr(parser, "_acli_standard_args", False):
        return
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--format",
        choices=["compact", "jsonl", "pretty", "toon"],
        dest="format",
        help="Output format. compact/jsonl is JSON Lines; pretty is indented JSON; toon is flat-table TOON.",
    )
    group.add_argument(
        "--compact",
        action="store_const",
        const="compact",
        dest="format",
        help="Output compact JSON Lines.",
    )
    group.add_argument(
        "--pretty",
        action="store_const",
        const="pretty",
        dest="format",
        help="Output indented JSON.",
    )
    group.add_argument(
        "--toon",
        action="store_const",
        const="toon",
        dest="format",
        help="Output TOON; valid only for table-producing subcommands.",
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Include the full structured schema instead of the minimal default.",
    )
    parser.set_defaults(format=None, full=False, acli_toon_allowed=allow_toon)
    setattr(parser, "_acli_standard_args", True)


# --- Completion protocol (topics/agent-cli.md § Completion protocol) ---
#
# `tool --acli-complete <argv-prefix...>` emits JSONL candidates for the
# final token of the prefix (an empty final token means "fresh token") and
# exits 0. The prefix excludes the program name. Zero lines is the
# definitive "no completions"; consumers fall back to path completion.

COMPLETE_FLAG = "--acli-complete"

# A value completer takes (prefix, tokens) — the token under completion and
# the full partial argv — and yields candidates: strings, or dicts with
# "completion" and optional "kind"/"help" keys. A completer does its own
# prefix filtering (case-insensitive if it likes); only the automatic
# `choices` fallback is filtered centrally.
Completer = Callable[[str, "list[str]"], Iterable[Any]]


def set_completer(action: argparse.Action, fn: Completer) -> argparse.Action:
    """Attach an opt-in value completer to an argparse action.

    Actions with `choices` complete from them automatically; a completer
    overrides that. Completers must be side-effect-free and fast.
    """
    setattr(action, "acli_completer", fn)
    return action


def _subparsers_action(
    parser: argparse.ArgumentParser,
) -> argparse._SubParsersAction | None:
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            return action
    return None


def _takes_value(action: argparse.Action) -> bool:
    return action.nargs != 0


def _walk(parser: argparse.ArgumentParser, tokens: list[str]):
    """Best-effort walk of the already-complete tokens.

    Returns (parser, pending_option_action, positionals_consumed). The walk
    approximates one value per option and per positional slot — enough for
    the flat grammars ACLI tools keep.
    """
    pending: argparse.Action | None = None
    positionals = 0
    for tok in tokens:
        if pending is not None:
            pending = None
            continue
        if tok.startswith("-") and tok != "-":
            action = parser._option_string_actions.get(tok.partition("=")[0])
            if action is not None and _takes_value(action) and "=" not in tok:
                pending = action
            continue
        sub = _subparsers_action(parser)
        if sub is not None and tok in sub.choices:
            parser = sub.choices[tok]
            positionals = 0
            continue
        positionals += 1
    return parser, pending, positionals


def _positional_action(
    parser: argparse.ArgumentParser, index: int
) -> argparse.Action | None:
    slots = [
        action
        for action in parser._actions
        if not action.option_strings
        and not isinstance(action, argparse._SubParsersAction)
    ]
    if index < len(slots):
        return slots[index]
    if slots and slots[-1].nargs in ("*", "+", argparse.REMAINDER):
        return slots[-1]
    return None


def _candidate(entry: Any, kind: str, help_text: str | None = None) -> dict[str, Any]:
    if isinstance(entry, dict):
        row = {"completion": str(entry["completion"])}
        row["kind"] = str(entry.get("kind", kind))
        text = entry.get("help", help_text)
    else:
        row = {"completion": str(entry), "kind": kind}
        text = help_text
    if text:
        row["help"] = text
    return row


def _value_candidates(
    action: argparse.Action, prefix: str, tokens: list[str]
) -> list[dict[str, Any]]:
    completer = getattr(action, "acli_completer", None)
    if completer is not None:
        return [
            _candidate(entry, "value", action.help)
            for entry in completer(prefix, tokens)
        ]
    if action.choices:
        return [
            _candidate(str(choice), "value", action.help)
            for choice in action.choices
            if str(choice).startswith(prefix)
        ]
    return []


def complete(
    parser: argparse.ArgumentParser,
    tokens: list[str],
    out: TextIO = sys.stdout,
) -> None:
    """Emit JSONL completion candidates for a partial argv (program name excluded)."""
    if not tokens:
        tokens = [""]
    current = tokens[-1]
    target, pending, positionals = _walk(parser, tokens[:-1])
    rows: list[dict[str, Any]] = []
    if pending is not None:
        rows = _value_candidates(pending, current, tokens)
    elif current.startswith("--") and "=" in current:
        name, _, value = current.partition("=")
        action = target._option_string_actions.get(name)
        if action is not None and _takes_value(action):
            rows = [
                {**row, "completion": f"{name}={row['completion']}"}
                for row in _value_candidates(action, value, tokens)
            ]
    elif current.startswith("-"):
        seen: set[str] = set()
        for action in target._actions:
            if action.help == argparse.SUPPRESS:
                continue
            for opt in action.option_strings:
                if opt.startswith(current) and opt not in seen:
                    seen.add(opt)
                    rows.append(_candidate(opt, "flag", action.help))
    else:
        sub = _subparsers_action(target)
        if sub is not None:
            helps = {
                choice.dest: choice.help
                for choice in sub._choices_actions
                if choice.help != argparse.SUPPRESS
            }
            for name in sub.choices:
                if name.startswith(current):
                    rows.append(_candidate(name, "subcommand", helps.get(name)))
        action = _positional_action(target, positionals)
        if action is not None:
            rows.extend(_value_candidates(action, current, tokens))
    emitted: set[str] = set()
    for row in sorted(rows, key=lambda r: r["completion"]):
        if row["completion"] in emitted:
            continue
        emitted.add(row["completion"])
        out.write(json.dumps(row, separators=(",", ":"), sort_keys=True) + "\n")


def maybe_complete(
    parser: argparse.ArgumentParser,
    argv: list[str] | None = None,
    out: TextIO = sys.stdout,
) -> None:
    """Serve `--acli-complete` when requested, else return.

    Call before normal parsing and before any side effect:
    `maybe_complete(parser)`. When argv[1] is --acli-complete, emits
    candidates for argv[2:] and exits 0.
    """
    argv = sys.argv if argv is None else argv
    if len(argv) < 2 or argv[1] != COMPLETE_FLAG:
        return
    complete(parser, list(argv[2:]), out)
    raise SystemExit(0)
