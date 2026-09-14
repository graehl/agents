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
    def __init__(self, server: CodexAppServer, config: AnnotationConfig) -> None:
        self.server = server
        self.config = config

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
            if row["config_sha256"] != self.config.identity() or row["input"] != asdict(
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
        thread_id = None
        session_segments = 0
        restore = False
        last_turn_id = None
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
                    last_turn_id = row["turn_id"]
                    continue
                if restore:
                    await self.server.resume_thread(
                        thread_id,
                        base_instructions=cfg.prefix,
                        cwd=cfg.cwd,
                        model=cfg.model,
                    )
                    thread = await self.server.read_thread(thread_id)
                    turns = thread.get("turns")
                    if (
                        thread.get("id") != thread_id
                        or not isinstance(turns, list)
                        or not turns
                        or not isinstance(turns[-1], Mapping)
                        or turns[-1].get("id") != last_turn_id
                        or turns[-1].get("status") != "completed"
                    ):
                        raise ValueError(
                            "saved document thread no longer ends at its completed receipt"
                        )
                    restore = False
                total_usage: dict[str, int] = defaultdict(int)
                for attempt in range(cfg.retries + 1):
                    if (
                        thread_id is None
                        or session_segments >= cfg.max_segments_per_session
                    ):
                        thread = await self.server.start_protocol_root(
                            base_instructions=cfg.prefix, cwd=cfg.cwd, model=cfg.model
                        )
                        thread_id, session_segments = str(thread["id"]), 0
                        record(
                            {
                                "kind": "session_start",
                                "document_id": segment.document_id,
                                "index": index,
                                "thread": dict(thread),
                            }
                        )
                        if cfg.fixed_messages:
                            record(
                                {
                                    "kind": "fixed_messages_start",
                                    "thread_id": thread_id,
                                    "index": index,
                                    "provenance": "caller_authored",
                                    "messages": [asdict(m) for m in cfg.fixed_messages],
                                    "config_sha256": cfg.identity(),
                                }
                            )
                            receipt = await self.server.inject_fixed_messages(
                                thread_id, cfg.fixed_messages
                            )
                            record(
                                {
                                    "kind": "fixed_messages_complete",
                                    "thread_id": thread_id,
                                    "index": index,
                                    "response": dict(receipt),
                                }
                            )
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
                    try:
                        response = await self.server.run_turn(
                            thread_id,
                            segment.prompt,
                            cwd=cfg.cwd,
                            model=cfg.model,
                            effort=cfg.effort,
                            timeout=cfg.timeout,
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
                    record(
                        {
                            "kind": "attempt_response",
                            "attempt_id": attempt_id,
                            "index": index,
                            "elapsed_seconds": time.monotonic() - started,
                            "response": response,
                        }
                    )
                    session_segments += 1
                    for key, count in response["usage"].items():
                        total_usage[key] += count
                    text = response["content"][0]["text"]
                    reason = None
                    if response["usage"]["input_tokens"] > cfg.max_input_tokens:
                        reason = "context input-token ceiling exceeded"
                    elif any(_compacted(event) for event in response["codex_events"]):
                        reason = "context was compacted"
                    elif validate is not None:
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
                row = {
                    "kind": "segment_result",
                    "index": index,
                    "document_id": segment.document_id,
                    "segment_id": segment.segment_id,
                    "input": asdict(segment),
                    "config_sha256": cfg.identity(),
                    "status": "rejected"
                    if reason
                    else ("validated" if validate else "unvalidated"),
                    "rejection": reason,
                    "text": text,
                    "attempts": attempt + 1,
                    "usage": dict(total_usage),
                    "thread_id": response["app_server"]["thread_id"],
                    "turn_id": response["app_server"]["turn_id"],
                    "continuation_thread_id": thread_id,
                    "session_segments": session_segments,
                }
                record(row)
                results.append(row)
        return results


def _compacted(event: Mapping[str, Any]) -> bool:
    if "compact" in str(event.get("method", "")).lower():
        return True
    params = event.get("params")
    item = params.get("item") if isinstance(params, Mapping) else None
    return isinstance(item, Mapping) and "compact" in str(item.get("type", "")).lower()
