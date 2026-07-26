"""Agent-first CLI helpers.

Small pure-function surface for CLIs that follow topics/agent-cli.md.
"""

from __future__ import annotations

from .args import (
    add_standard_args,
    argument_parser,
    candidates,
    capability_line,
    complete,
    hint,
    maybe_complete,
    maybe_repl,
    set_completer,
)
from .emit import emit, write_jsonl, write_pretty, write_toon_table
from .errors import ExitCode, die, error_envelope
from .session import Format, is_agent_session, resolve_format

__all__ = [
    "ExitCode",
    "Format",
    "add_standard_args",
    "argument_parser",
    "candidates",
    "capability_line",
    "complete",
    "die",
    "emit",
    "error_envelope",
    "hint",
    "is_agent_session",
    "maybe_complete",
    "maybe_repl",
    "resolve_format",
    "set_completer",
    "write_jsonl",
    "write_pretty",
    "write_toon_table",
]
