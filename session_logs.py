"""Locate harness session transcripts for log-mining tools.

Claude Code writes one JSONL transcript per session under
`~/.claude/projects/<claude_project_dir_name(launch cwd)>/`. Codex writes
rollouts under `~/.codex/sessions/YYYY/MM/DD/`, recording the session's cwd
in its leading `session_meta` record. Miners (`scripts/tool-surprises`,
`scripts/intervention-needles`) share this discovery so a project's sessions
are scoped the same way everywhere.
"""

from __future__ import annotations

import json
import os
import struct
import time
from pathlib import Path

HARNESSES = ("claude", "codex")


class NoTranscriptDir(Exception):
    """The harness has no transcript directory for the requested scope."""

    def __init__(self, harness: str, looked_under: Path) -> None:
        super().__init__(f"no {harness} transcript dir under {looked_under}")
        self.harness = harness
        self.looked_under = looked_under


def claude_projects_dir() -> Path:
    return Path.home() / ".claude" / "projects"


def codex_sessions_dir() -> Path:
    return Path.home() / ".codex" / "sessions"


CLAUDE_DIR_NAME_MAX = 200


def claude_project_dir_name(cwd: str) -> str:
    """Claude Code's `projects/` directory name for a launch cwd.

    Read from the installed Claude Code 2.1.302 bundle: each UTF-16 code unit
    that is not an ASCII letter or digit becomes "-"; a name over 200
    characters keeps its first 200 plus "-" and the base-36 absolute value of
    the path's 32-bit Java-style string hash.
    """
    name = "".join(
        c if c.isascii() and c.isalnum() else "-" * (2 if ord(c) > 0xFFFF else 1)
        for c in cwd
    )
    if len(name) <= CLAUDE_DIR_NAME_MAX:
        return name
    units = cwd.encode("utf-16-le")
    digest = 0
    for (unit,) in struct.iter_unpack("<H", units):
        digest = (digest * 31 + unit) & 0xFFFFFFFF
    value = abs(digest - (1 << 32) if digest >= 1 << 31 else digest)
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    encoded = ""
    while True:
        value, rest = divmod(value, 36)
        encoded = digits[rest] + encoded
        if not value:
            break
    return f"{name[:CLAUDE_DIR_NAME_MAX]}-{encoded}"


def transcript_dirs(project_root: Path) -> list[Path]:
    base = claude_projects_dir()
    path = base / claude_project_dir_name(str(project_root))
    return [path] if path.is_dir() else []


def codex_session_info(path: Path) -> tuple[str, Path | None]:
    """Return the resumable session id and recorded cwd from a rollout."""
    with path.open(encoding="utf-8", errors="replace") as fh:
        for index, line in enumerate(fh):
            if index >= 20:
                break
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if record.get("type") != "session_meta":
                continue
            payload = record.get("payload") or {}
            session_id = str(
                payload.get("id") or payload.get("session_id") or path.stem
            )
            cwd = payload.get("cwd")
            return session_id, Path(cwd).expanduser().resolve() if cwd else None
    return path.stem, None


def current_session_ids() -> set[str]:
    """Ids naming the calling session, so a miner can skip its own log."""
    ids = set()
    for var in ("AGENTCTL_SESSION_ID", "CLAUDE_CODE_SESSION_ID", "CODEX_THREAD_ID"):
        value = os.environ.get(var, "").strip()
        if value:
            ids.add(value)
    return ids


def session_sources(
    harness: str,
    project_root: Path | None,
    *,
    days: float = 0,
    exclude: set[str] | frozenset[str] = frozenset(),
) -> list[tuple[Path, str]]:
    """Return sorted `(transcript path, session id)` pairs for one harness.

    `project_root=None` selects every project's sessions. Raises
    `NoTranscriptDir` when the harness has no log directory for the scope.
    """
    cutoff = time.time() - days * 86400 if days else 0.0
    sources: list[tuple[Path, str]] = []
    if harness == "claude":
        if project_root is None:
            base = claude_projects_dir()
            dirs = (
                sorted(p for p in base.iterdir() if p.is_dir()) if base.is_dir() else []
            )
        else:
            dirs = transcript_dirs(project_root)
        if not dirs:
            raise NoTranscriptDir(harness, claude_projects_dir())
        sources = [
            (path, path.stem)
            for directory in dirs
            for path in directory.glob("*.jsonl")
            if path.stem not in exclude and path.stat().st_mtime >= cutoff
        ]
    elif harness == "codex":
        base = codex_sessions_dir()
        if not base.is_dir():
            raise NoTranscriptDir(harness, base)
        for path in base.rglob("*.jsonl"):
            if path.stat().st_mtime < cutoff:
                continue
            session_id, cwd = codex_session_info(path)
            if session_id in exclude:
                continue
            if project_root is None or cwd == project_root:
                sources.append((path, session_id))
    else:
        raise ValueError(f"unknown harness {harness!r}")
    sources.sort(key=lambda source: str(source[0]))
    return sources
