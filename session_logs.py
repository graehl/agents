"""Locate harness session transcripts for log-mining tools.

Claude Code writes one JSONL transcript per session under
`~/.claude/projects/<launch-cwd with "/" replaced by "-">/`. Codex writes
rollouts under `~/.codex/sessions/YYYY/MM/DD/`, recording the session's cwd
in its leading `session_meta` record. Miners (`scripts/tool-surprises`,
`scripts/intervention-needles`) share this discovery so a project's sessions
are scoped the same way everywhere.
"""

from __future__ import annotations

import json
import os
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


def transcript_dirs(project_root: Path) -> list[Path]:
    base = claude_projects_dir()
    munged = str(project_root).replace("/", "-")
    candidates = [base / munged, base / munged.replace(".", "-")]
    seen: list[Path] = []
    for cand in candidates:
        if cand.is_dir() and cand not in seen:
            seen.append(cand)
    return seen


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
    for var in ("AGENTCTL_SESSION_ID", "CLAUDE_CODE_SESSION_ID"):
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
