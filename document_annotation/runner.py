"""Ordered document sessions with externally defined annotation validation."""

from __future__ import annotations

import asyncio
import hashlib
import inspect
import json
import math
import time
import uuid
from collections import defaultdict
from collections.abc import Awaitable, Callable, Mapping, Sequence
from dataclasses import asdict, dataclass, field
from typing import Any

from .codex import CodexAppServer
from .messages import FixedMessage
from .sessions import Backend, CodexSessions, Session


@dataclass(frozen=True)
class Segment:
    document_id: str
    segment_id: str
    prompt: str
    metadata: Mapping[str, Any] = field(default_factory=dict)


Validator = Callable[[str, Segment], str | None | Awaitable[str | None]]
Recorder = Callable[[dict[str, Any]], None]


@dataclass(frozen=True)
class AnnotationConfig:
    prefix: str
    model: str
    effort: str
    cwd: str
    max_segments_per_session: int
    max_input_tokens: int
    concurrency: int = 4
    retries: int = 1
    timeout: float = 300
    validator_id: str | None = None
    fixed_messages: tuple[FixedMessage, ...] = ()

    def __post_init__(self) -> None:
        if not all(
            isinstance(s, str) and s
            for s in (self.prefix, self.model, self.effort, self.cwd)
        ):
            raise ValueError("prefix, model, effort and cwd must be nonempty strings")
        for name in ("max_segments_per_session", "max_input_tokens", "concurrency"):
            if type(getattr(self, name)) is not int or getattr(self, name) < 1:
                raise ValueError(f"{name} must be a positive integer")
        if type(self.retries) is not int or self.retries < 0:
            raise ValueError("retries must be a nonnegative integer")
        if not math.isfinite(self.timeout) or self.timeout <= 0:
            raise ValueError("timeout must be finite and positive")
        if self.validator_id is not None and (
            not isinstance(self.validator_id, str) or not self.validator_id
        ):
            raise ValueError("validator_id must be a nonempty versioned identity")
        if not isinstance(self.fixed_messages, tuple) or not all(
            isinstance(message, FixedMessage) for message in self.fixed_messages
        ):
            raise TypeError("fixed_messages must be a tuple of FixedMessage values")

    def record(self) -> dict[str, Any]:
        result = asdict(self)
        result["fixed_messages"] = [asdict(message) for message in self.fixed_messages]
        return result

    def identity(self) -> str:
        return hashlib.sha256(
            json.dumps(self.record(), sort_keys=True).encode()
        ).hexdigest()


class DocumentAnnotator:
    def __init__(
        self, server: CodexAppServer | Backend, config: AnnotationConfig
    ) -> None:
        self.server = server
        self.config = config
        self.backend = (
            CodexSessions(server) if isinstance(server, CodexAppServer) else server
        )
        self.config_sha256 = (
            config.identity()
            if self.backend.identity is None
            else hashlib.sha256(
                json.dumps(
                    {"config": config.record(), "backend": self.backend.identity},
                    sort_keys=True,
                ).encode()
            ).hexdigest()
        )

    async def annotate(
        self,
        segments: Sequence[Segment],
        *,
        record: Recorder,
        validate: Validator | None = None,
        completed: Sequence[Mapping[str, Any]] = (),
    ) -> list[dict[str, Any]]:
        if (validate is None) != (self.config.validator_id is None):
            raise ValueError(
                "a validator and its versioned validator_id must be supplied together"
            )
        if validate is not None and not callable(validate):
            raise TypeError("validate must be callable")
        by_document: dict[str, list[tuple[int, Segment]]] = defaultdict(list)
        ids = set()
        for index, segment in enumerate(segments):
            if not all(
                isinstance(s, str) and s
                for s in (segment.document_id, segment.segment_id, segment.prompt)
            ):
                raise ValueError(
                    "document_id, segment_id and prompt must be nonempty strings"
                )
            key = (segment.document_id, segment.segment_id)
            if key in ids:
                raise ValueError(f"duplicate segment identity: {key}")
            json.dumps(asdict(segment), allow_nan=False)
            ids.add(key)
            by_document[segment.document_id].append((index, segment))
        saved = {}
        for row in completed:
            index = row["index"]
            if (
                type(index) is not int
                or index in saved
                or not 0 <= index < len(segments)
            ):
                raise ValueError("invalid or duplicate completed segment index")
            segment = segments[index]
            if row["config_sha256"] != self.config_sha256 or row["input"] != asdict(
                segment
            ):
                raise ValueError(
                    "completed result does not bind current config and input"
                )
            saved[index] = dict(row)
        for entries in by_document.values():
            seen_pending = False
            for index, _ in entries:
                if index not in saved:
                    seen_pending = True
                elif seen_pending:
                    raise ValueError(
                        "completed segments must form a prefix within each document"
                    )
        semaphore = asyncio.Semaphore(self.config.concurrency)
        tasks = []
        async with asyncio.TaskGroup() as group:
            for entries in by_document.values():
                tasks.append(
                    group.create_task(
                        self._document(entries, saved, semaphore, record, validate)
                    )
                )
        return sorted(
            (row for task in tasks for row in task.result()),
            key=lambda row: row["index"],
        )

    async def _document(
        self,
        entries: list[tuple[int, Segment]],
        saved: Mapping[int, dict[str, Any]],
        semaphore: asyncio.Semaphore,
        record: Recorder,
        validate: Validator | None,
    ) -> list[dict[str, Any]]:
        cfg = self.config
        results = []
        session: Session | None = None
        thread_id = None
        session_segments = 0
        restore = False
        async with semaphore:
            for index, segment in entries:
                if index in saved:
                    row = saved[index]
                    results.append(row)
                    thread_id = row["continuation_thread_id"]
                    session_segments = row["session_segments"]
                    restore = (
                        thread_id is not None
                        and session_segments < cfg.max_segments_per_session
                    )
                    continue
                if restore:
                    session = await self.backend.resume(cfg, results)
                    restore = False
                total_usage: dict[str, int] = defaultdict(int)
                for attempt in range(cfg.retries + 1):
                    if (
                        session is None
                        or session_segments >= cfg.max_segments_per_session
                    ):
                        session = await self.backend.start(
                            cfg, record, index, segment.document_id
                        )
                        thread_id, session_segments = session.id, 0
                    attempt_id = str(uuid.uuid4())
                    record(
                        {
                            "kind": "attempt_start",
                            "attempt_id": attempt_id,
                            "index": index,
                            "document_id": segment.document_id,
                            "segment_id": segment.segment_id,
                            "thread_id": thread_id,
                            "attempt": attempt + 1,
                            "session_segments_before": session_segments,
                        }
                    )
                    started = time.monotonic()

                    def record_response(
                        raw: dict[str, Any],
                        *,
                        attempt_id: str = attempt_id,
                        index: int = index,
                        started: float = started,
                    ) -> None:
                        record(
                            {
                                "kind": "attempt_response",
                                "attempt_id": attempt_id,
                                "index": index,
                                "elapsed_seconds": time.monotonic() - started,
                                "response": raw,
                            }
                        )

                    try:
                        response = await session.run_turn(
                            segment.prompt, record_response
                        )
                    except BaseException as error:
                        record(
                            {
                                "kind": "attempt_error",
                                "attempt_id": attempt_id,
                                "index": index,
                                "error_type": type(error).__name__,
                                "error": str(error),
                            }
                        )
                        raise
                    session_segments += 1
                    for key, count in response.usage.items():
                        total_usage[key] += count
                    text = response.text
                    reason = response.rejection
                    if response.usage["input_tokens"] > cfg.max_input_tokens:
                        reason = "context input-token ceiling exceeded"
                    elif reason is None and validate is not None:
                        reason = validate(text, segment)
                        if inspect.isawaitable(reason):
                            reason = await reason
                        if reason is not None and (
                            not isinstance(reason, str) or not reason
                        ):
                            raise TypeError(
                                "validator must return None or a nonempty rejection reason"
                            )
                    record(
                        {
                            "kind": "attempt_validation",
                            "attempt_id": attempt_id,
                            "index": index,
                            "rejection": reason,
                        }
                    )
                    if reason is None:
                        break
                    thread_id, session_segments = None, 0
                    session = None
                row = {
                    "kind": "segment_result",
                    "index": index,
                    "document_id": segment.document_id,
                    "segment_id": segment.segment_id,
                    "input": asdict(segment),
                    "config_sha256": self.config_sha256,
                    "status": "rejected"
                    if reason
                    else ("validated" if validate else "unvalidated"),
                    "rejection": reason,
                    "text": text,
                    "attempts": attempt + 1,
                    "usage": dict(total_usage),
                    "thread_id": response.session_id,
                    "turn_id": response.turn_id,
                    "continuation_thread_id": thread_id,
                    "session_segments": session_segments,
                }
                record(row)
                results.append(row)
        return results
