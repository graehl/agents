"""Terminal program status reports (OSC 7501, Program Status Protocol 0.3).

A long-running tool tells an interactive terminal whether it is working,
blocked, done, or failed; the terminal decides how to show it (tab badge,
progress, notification). Spec:
https://www.superlogical.com/rex/docs/build/program-status

Reports go to stderr only when it is a terminal and no agent-session
indicator is set (the same detection as the output-format default), so
structured stdout, captured logs, and agent-read streams never carry the
escape. Terminals that do not know the sequence ignore it, so no probe is
needed before writing.
"""

from __future__ import annotations

import base64
import re
import sys
import threading
from collections.abc import Mapping
from types import TracebackType
from typing import Self, TextIO

from .session import is_agent_session

STATES = frozenset({"idle", "working", "done", "blocked", "error", "clear"})
FINAL_STATES = frozenset({"done", "error", "clear"})
KINDS = frozenset({"permission", "question", "auth"})

_NAME = re.compile(r"[A-Za-z0-9_.+-]{1,32}")
_MAX_ID_BYTES = 128
_MAX_ID_DEPTH = 8
_MAX_TITLE_BYTES = 192
_MAX_MSG_BYTES = 2048
_MAX_SEQUENCE_BYTES = 4096
# Terminals discard a report whose decoded text holds any control character.
_CONTROL = re.compile(r"[\x00-\x1f\x7f-\x9f]")


def _check_id(record_id: str) -> None:
    segments = record_id.split("/")
    if (
        len(record_id.encode()) > _MAX_ID_BYTES
        or len(segments) > _MAX_ID_DEPTH
        or not all(_NAME.fullmatch(s) for s in segments)
    ):
        raise ValueError(f"invalid program-status id {record_id!r}")


def _encode_text(text: str, limit: int) -> str:
    """Base64 of one line, controls replaced and cut to `limit` UTF-8 bytes."""
    raw = _CONTROL.sub(" ", text).encode()[:limit]
    # A cut inside a multibyte character drops that partial character.
    clean = raw.decode(errors="ignore").encode()
    return base64.b64encode(clean).decode("ascii")


def program_status(
    state: str,
    *,
    app: str | None = None,
    record_id: str | None = None,
    kind: str | None = None,
    progress: int | None = None,
    title: str | None = None,
    msg: str | None = None,
) -> str:
    """Return one OSC 7501 report terminated by ST.

    `app` and each `/`-separated `record_id` segment are 1-32 characters of
    `[A-Za-z0-9_.+-]`; `kind` applies to `blocked`; `progress` (0-100)
    applies to `working` and `blocked`. `title` and `msg` are free text,
    made one line and cut to the spec's byte limits.
    """
    if state not in STATES:
        raise ValueError(f"unknown program-status state {state!r}")
    # Key order follows the spec's examples; terminals accept any order.
    pairs = [f"state={state}"]
    if kind is not None:
        if state != "blocked" or kind not in KINDS:
            raise ValueError(f"kind {kind!r} is invalid for state {state!r}")
        pairs.append(f"kind={kind}")
    if record_id is not None:
        _check_id(record_id)
        pairs.append(f"id={record_id}")
    if app is not None:
        if not _NAME.fullmatch(app):
            raise ValueError(f"invalid program-status app {app!r}")
        pairs.append(f"app={app}")
    if title:
        pairs.append(f"title={_encode_text(title, _MAX_TITLE_BYTES)}")
    if progress is not None:
        if state not in {"working", "blocked"} or not 0 <= progress <= 100:
            raise ValueError(f"progress {progress!r} is invalid for state {state!r}")
        pairs.append(f"progress={int(progress)}")
    if msg:
        pairs.append(f"msg={_encode_text(msg, _MAX_MSG_BYTES)}")
    report = "\x1b]7501;" + ":".join(pairs) + "\x1b\\"
    # The field limits keep a report well under the sequence limit.
    assert len(report.encode()) <= _MAX_SEQUENCE_BYTES
    return report


def terminal_status_enabled(
    stream: TextIO | None = None, env: Mapping[str, str] | None = None
) -> bool:
    """True when `stream` (default stderr) is a human's terminal."""
    return not is_agent_session(sys.stderr if stream is None else stream, env)


class ProgramStatus:
    """Report one program's status to its terminal, repeating `app` each time.

    Writes nothing unless `terminal_status_enabled` (or an explicit
    `enabled`). As a context manager it ends with `done`, or `error` when
    the block raises, unless the caller already reported a final state.
    Thread-safe: each report is one write.
    """

    def __init__(
        self,
        app: str,
        *,
        stream: TextIO | None = None,
        env: Mapping[str, str] | None = None,
        enabled: bool | None = None,
    ) -> None:
        program_status("idle", app=app)  # validate `app` once, up front
        self.app = app
        self.stream = sys.stderr if stream is None else stream
        self.enabled = (
            terminal_status_enabled(self.stream, env) if enabled is None else enabled
        )
        self.finished = False
        self._lock = threading.Lock()

    def report(
        self,
        state: str,
        *,
        record_id: str | None = None,
        kind: str | None = None,
        progress: int | None = None,
        title: str | None = None,
        msg: str | None = None,
    ) -> bool:
        """Write one report; return whether it was written."""
        text = program_status(
            state,
            app=self.app,
            record_id=record_id,
            kind=kind,
            progress=progress,
            title=title,
            msg=msg,
        )
        if record_id is None and state in FINAL_STATES:
            self.finished = True
        if not self.enabled:
            return False
        with self._lock:
            self.stream.write(text)
            self.stream.flush()
        return True

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        if self.finished:
            return
        if exc_type is None:
            self.report("done")
        elif isinstance(exc, SystemExit):
            if exc.code in (None, 0):
                self.report("done")
            else:
                self.report("error", msg=f"exited with status {exc.code}")
        elif isinstance(exc, KeyboardInterrupt):
            # The user cancelled; nothing is left for them to look at.
            self.report("clear")
        else:
            self.report("error", msg=f"{type(exc).__name__}: {exc}")
