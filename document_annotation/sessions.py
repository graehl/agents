"""Annotation sessions independent of provider history storage."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING, Any, Protocol

from .codex import CodexAppServer

if TYPE_CHECKING:
    from .runner import AnnotationConfig, Recorder


@dataclass(frozen=True)
class Turn:
    text: str
    usage: dict[str, int]
    session_id: str
    turn_id: str
    rejection: str | None = None


class Session(Protocol):
    id: str

    async def run_turn(
        self, prompt: str, record_response: Callable[[dict[str, Any]], None]
    ) -> Turn: ...


class Backend(Protocol):
    identity: Mapping[str, Any] | None

    async def start(
        self, config: AnnotationConfig, record: Recorder, index: int, document_id: str
    ) -> Session: ...

    async def resume(
        self, config: AnnotationConfig, rows: Sequence[Mapping[str, Any]]
    ) -> Session: ...


class CodexSessions:
    identity = None  # Preserve subscription config/result identities.

    def __init__(self, server: CodexAppServer) -> None:
        self.server = server

    async def start(
        self, config: AnnotationConfig, record: Recorder, index: int, document_id: str
    ) -> CodexSession:
        thread = await self.server.start_protocol_root(
            base_instructions=config.prefix, cwd=config.cwd, model=config.model
        )
        thread_id = str(thread["id"])
        record(
            {
                "kind": "session_start",
                "document_id": document_id,
                "index": index,
                "thread": dict(thread),
            }
        )
        if config.fixed_messages:
            record(
                {
                    "kind": "fixed_messages_start",
                    "thread_id": thread_id,
                    "index": index,
                    "provenance": "caller_authored",
                    "messages": [asdict(m) for m in config.fixed_messages],
                    "config_sha256": config.identity(),
                }
            )
            receipt = await self.server.inject_fixed_messages(
                thread_id, config.fixed_messages
            )
            record(
                {
                    "kind": "fixed_messages_complete",
                    "thread_id": thread_id,
                    "index": index,
                    "response": dict(receipt),
                }
            )
        return CodexSession(self.server, config, thread_id)

    async def resume(
        self, config: AnnotationConfig, rows: Sequence[Mapping[str, Any]]
    ) -> CodexSession:
        last = rows[-1]
        thread_id = last["continuation_thread_id"]
        await self.server.resume_thread(
            thread_id,
            base_instructions=config.prefix,
            cwd=config.cwd,
            model=config.model,
        )
        thread = await self.server.read_thread(thread_id)
        turns = thread.get("turns")
        if (
            thread.get("id") != thread_id
            or not isinstance(turns, list)
            or not turns
            or not isinstance(turns[-1], Mapping)
            or turns[-1].get("id") != last["turn_id"]
            or turns[-1].get("status") != "completed"
        ):
            raise ValueError(
                "saved document thread no longer ends at its completed receipt"
            )
        return CodexSession(self.server, config, thread_id)


class CodexSession:
    def __init__(
        self, server: CodexAppServer, config: AnnotationConfig, session_id: str
    ) -> None:
        self.server, self.config, self.id = server, config, session_id

    async def run_turn(
        self, prompt: str, record_response: Callable[[dict[str, Any]], None]
    ) -> Turn:
        cfg = self.config
        raw = await self.server.run_turn(
            self.id,
            prompt,
            cwd=cfg.cwd,
            model=cfg.model,
            effort=cfg.effort,
            timeout=cfg.timeout,
        )
        record_response(raw)
        return Turn(
            raw["content"][0]["text"],
            raw["usage"],
            self.id,
            raw["app_server"]["turn_id"],
            "context was compacted"
            if any(_compacted(e) for e in raw["codex_events"])
            else None,
        )


def _compacted(event: Mapping[str, Any]) -> bool:
    if "compact" in str(event.get("method", "")).lower():
        return True
    params = event.get("params")
    item = params.get("item") if isinstance(params, Mapping) else None
    return isinstance(item, Mapping) and "compact" in str(item.get("type", "")).lower()
