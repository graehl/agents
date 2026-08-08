from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Callable, Iterable, Mapping
from typing import Any, TextIO

# Protocol version advertised by the capability line
# (topics/agent-cli.md § Capability line and help footer).
ACLI_PROTOCOL_VERSION = 1


def capability_line(capabilities: Iterable[str]) -> str:
    """The `acli: <version> <capability>...` discovery line."""
    return f"acli: {ACLI_PROTOCOL_VERSION} {' '.join(capabilities)}".rstrip()


class ArgumentParser(argparse.ArgumentParser):
    """argparse.ArgumentParser plus the ACLI help footer.

    `capabilities` renders the trailing `acli: <version> ...` discovery
    line (default assumes the tool calls `maybe_complete`; advertise only
    wired capabilities — pass `()` to opt out, add "repl"/"toon" as
    earned). `exit_codes` maps code -> one-line meaning, rendered as an
    `exit codes:` table above the capability line. Subparsers inherit the
    parent's capability line so every help screen agrees.
    """

    def __init__(
        self,
        *args,
        capabilities: Iterable[str] = ("complete",),
        exit_codes: Mapping[int, str] | None = None,
        **kwargs,
    ):
        kwargs.setdefault("formatter_class", argparse.RawTextHelpFormatter)
        self.acli_capabilities = tuple(capabilities)
        self.acli_exit_codes = dict(exit_codes or {})
        super().__init__(*args, **kwargs)

    def add_subparsers(self, **kwargs):
        parent = self

        class _SubParser(type(parent)):  # type: ignore[misc]
            def __init__(self, *args, **sub_kwargs):
                sub_kwargs.setdefault("capabilities", parent.acli_capabilities)
                super().__init__(*args, **sub_kwargs)

        kwargs.setdefault("parser_class", _SubParser)
        return super().add_subparsers(**kwargs)

    def format_help(self) -> str:
        text = super().format_help().rstrip("\n")
        if self.acli_exit_codes:
            width = max(len(str(code)) for code in self.acli_exit_codes)
            table = "\n".join(
                f"  {str(code).rjust(width)}  {meaning}"
                for code, meaning in sorted(self.acli_exit_codes.items())
            )
            text += "\n\nexit codes:\n" + table
        if self.acli_capabilities:
            text += "\n\n" + capability_line(self.acli_capabilities)
        return text + "\n"


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
    parser._acli_standard_args = True


_STANDARD_FLAG_ARITY: dict[str, int] | None = None


def standard_flag_arity() -> dict[str, int]:
    """Each standard flag, mapped to how many later tokens its value takes.

    Derived by asking `add_standard_args` itself, so the flags and their
    arity have one definition. Callers that must recognize a standard flag
    *before* argparse runs read this instead of restating the table: a
    launcher deciding where its verb starts has to know that `--format`
    swallows the next token but `--pretty` does not, and a hand-rolled copy
    of that goes stale the day a flag is added.
    """
    global _STANDARD_FLAG_ARITY
    if _STANDARD_FLAG_ARITY is None:
        probe = argparse.ArgumentParser(add_help=False)
        add_standard_args(probe, allow_toon=True)
        _STANDARD_FLAG_ARITY = {
            option: _option_value_bounds(action)[0] if _takes_value(action) else 0
            for action in probe._actions
            for option in action.option_strings
        }
    return _STANDARD_FLAG_ARITY


def skip_standard_flags(tokens: list[str]) -> int:
    """Index of the first token that is not a leading standard flag.

    `--format pretty` and `--format=pretty` both consume their value, so a
    caller splitting leading flags from what follows never mistakes a
    flag's value for the next grammar element.
    """
    arity = standard_flag_arity()
    index = 0
    while index < len(tokens):
        name, separator, _ = tokens[index].partition("=")
        if name not in arity:
            break
        index += 1 if separator else 1 + arity[name]
    return index


# --- Completion protocol (topics/agent-cli.md § Completion protocol) ---
#
# `tool --acli-complete <argv-prefix...>` emits JSONL candidates for the
# final token of the prefix (an empty final token means "fresh token") and
# exits 0. The prefix excludes the program name. Zero lines is the
# definitive "no completions"; consumers fall back to path completion.

COMPLETE_FLAG = "--acli-complete"

# A value completer takes (prefix, tokens) — the token under completion and
# the full partial argv — and yields candidates: strings, or dicts with
# "completion" and optional "kind"/"help"/"nospace" keys (hint() builds
# guidance rows). A completer does its own prefix filtering
# (case-insensitive if it likes) and chooses candidate order — emission
# order is preserved end to end; only the automatic `choices` fallback is
# filtered centrally.
Completer = Callable[[str, "list[str]"], Iterable[Any]]


def hint(text: str) -> dict[str, Any]:
    """A non-insertable guidance row for the current slot (kind="hint").

    Consumers render it dimmed and never insert it; emitting one also
    counts as answering, which suppresses the consumer's path fallback.
    """
    return {"completion": "", "kind": "hint", "help": text}


def set_completer(action: argparse.Action, fn: Completer) -> argparse.Action:
    """Attach an opt-in value completer to an argparse action.

    Actions with `choices` complete from them automatically; a completer
    overrides that. Completers must be side-effect-free and fast.
    """
    action.acli_completer = fn
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


def _option_value_bounds(action: argparse.Action) -> tuple[int, int | None, bool]:
    """Minimum, maximum, and whether another option ends this value slot."""
    nargs = action.nargs
    if nargs is None:
        return 1, 1, True
    if isinstance(nargs, int):
        return nargs, nargs, True
    if nargs == "?":
        return 0, 1, True
    if nargs == "*":
        return 0, None, True
    if nargs == "+":
        return 1, None, True
    if nargs == argparse.REMAINDER:
        return 0, None, False
    if nargs == argparse.PARSER:
        return 1, None, False
    return 1, 1, True


def _walk(parser: argparse.ArgumentParser, tokens: list[str]):
    """Best-effort walk of the already-complete tokens.

    Returns (parser, pending_option_action, positionals_consumed). The walk
    tracks argparse's option cardinality and approximates one value per
    positional slot — enough for the flat grammars ACLI tools keep.
    """
    pending: tuple[argparse.Action, int, int | None, bool] | None = None
    positionals = 0
    for tok in tokens:
        if pending is not None:
            action, required, remaining, stops_at_option = pending
            option = (
                parser._option_string_actions.get(tok.partition("=")[0])
                if tok.startswith("-") and tok != "-"
                else None
            )
            if option is not None and stops_at_option and required == 0:
                pending = None
            else:
                required = max(0, required - 1)
                if remaining is not None:
                    remaining -= 1
                pending = (
                    (action, required, remaining, stops_at_option)
                    if remaining is None or remaining > 0
                    else None
                )
                continue
        if tok.startswith("-") and tok != "-":
            name, separator, _ = tok.partition("=")
            action = parser._option_string_actions.get(name)
            if action is not None and _takes_value(action):
                required, remaining, stops_at_option = _option_value_bounds(action)
                if separator:
                    required = max(0, required - 1)
                    if remaining is not None:
                        remaining -= 1
                if remaining is None or remaining > 0:
                    pending = (action, required, remaining, stops_at_option)
            continue
        sub = _subparsers_action(parser)
        if sub is not None and tok in sub.choices:
            parser = sub.choices[tok]
            positionals = 0
            continue
        positionals += 1
    return parser, pending[0] if pending is not None else None, positionals


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
        if entry.get("nospace"):
            row["nospace"] = True
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
    # Value rows carry only completer-provided help: the action's own help
    # describes the slot, not each value, and belongs in a hint row.
    completer = getattr(action, "acli_completer", None)
    if completer is not None:
        return [_candidate(entry, "value") for entry in completer(prefix, tokens)]
    if action.choices:
        return [
            _candidate(str(choice), "value")
            for choice in action.choices
            if str(choice).startswith(prefix)
        ]
    return []


def candidates(
    parser: argparse.ArgumentParser, tokens: list[str]
) -> list[dict[str, Any]]:
    """Completion rows for a partial argv (program name excluded).

    Rows keep the order declarations and completers produce them — data
    order is often meaningful — deduplicated on first occurrence.
    """
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
                row
                if row.get("kind") == "hint"
                else {**row, "completion": f"{name}={row['completion']}"}
                for row in _value_candidates(action, value, tokens)
            ]
    elif current.startswith("-"):
        for action in target._actions:
            if action.help == argparse.SUPPRESS:
                continue
            for opt in action.option_strings:
                if opt.startswith(current):
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
    unique: list[dict[str, Any]] = []
    seen: set[str] = set()
    for row in rows:
        if row.get("kind") != "hint":
            if row["completion"] in seen:
                continue
            seen.add(row["completion"])
        unique.append(row)
    return unique


def complete(
    parser: argparse.ArgumentParser,
    tokens: list[str],
    out: TextIO = sys.stdout,
) -> None:
    """Emit JSONL completion candidates for a partial argv (program name excluded)."""
    out.writelines(
        json.dumps(row, separators=(",", ":"), sort_keys=True) + "\n"
        for row in candidates(parser, tokens)
    )


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


REPL_FLAG = "--repl"


def maybe_repl(parser: argparse.ArgumentParser, argv: list[str] | None = None) -> None:
    """Serve the reserved `--repl` verb when requested, else return.

    Call beside `maybe_complete`, before normal parsing. When argv[1] is
    --repl (no further arguments), runs the interactive shell over this
    parser and exits with its status.
    """
    argv = sys.argv if argv is None else argv
    if len(argv) < 2 or argv[1] != REPL_FLAG:
        return
    if len(argv) > 2:
        parser.error(f"{REPL_FLAG} takes no arguments")
    from . import shell  # lazy: the repl (and optional prompt_toolkit) load on use

    raise SystemExit(shell.run(parser))
