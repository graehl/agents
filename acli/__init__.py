"""Agent-first CLI helpers.

Small pure-function surface for CLIs that follow topics/agent-cli.md.
"""

from __future__ import annotations

from .emit import emit, write_jsonl, write_pretty, write_toon_table
from .errors import ExitCode, die, error_envelope
from .session import Format, is_agent_session, resolve_format

__all__ = [
    "ExitCode",
    "Format",
    "die",
    "emit",
    "error_envelope",
    "is_agent_session",
    "resolve_format",
    "write_jsonl",
    "write_pretty",
    "write_toon_table",
]
