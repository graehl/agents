"""Opt-in, key-authenticated Chat Completions with explicit message history."""

from __future__ import annotations

import asyncio
import json
import uuid
from collections.abc import Callable, Mapping, Sequence
from typing import TYPE_CHECKING, Any, Self

import httpx

from .sessions import Turn

if TYPE_CHECKING:
    from .runner import AnnotationConfig, Recorder

ENDPOINT = "https://api.openai.com/v1/chat/completions"


def message(role: str, text: str) -> dict[str, Any]:
    return {"role": role, "content": [{"type": "text", "text": text}]}


def settings(max_output_tokens: int, cache_mode: str) -> dict[str, Any]:
    if type(max_output_tokens) is not int or max_output_tokens < 1:
        raise ValueError(
            "--max-output-tokens must be positive for --backend openai-chat-completions"
        )
    if cache_mode not in ("explicit", "automatic"):
        raise ValueError("--chat-cache-mode must be explicit or automatic")
    return {
        "backend": "openai-chat-completions",
        "endpoint": ENDPOINT,
        "httpx_version": httpx.__version__,
        "cache_mode": cache_mode,
        "prompt_cache_options": {"mode": "explicit", "ttl": "30m"}
        if cache_mode == "explicit"
        else None,
        "max_completion_tokens": max_output_tokens,
        "service_tier": "default",
        "store": False,
    }


class ChatCompletions:
    def __init__(
        self, api_key: str, *, max_output_tokens: int, cache_mode: str = "explicit"
    ) -> None:
        if not isinstance(api_key, str) or not api_key.strip():
            raise ValueError(
                "OPENAI_API_KEY must be nonempty for --backend openai-chat-completions"
            )
        self.identity = settings(max_output_tokens, cache_mode)
        self.client = httpx.AsyncClient(
            headers={"Authorization": "Bearer " + api_key},
            follow_redirects=False,
            trust_env=False,
        )

    async def __aenter__(self) -> Self:
        await self.client.__aenter__()
        return self

    async def __aexit__(self, *exc: object) -> None:
        await self.client.__aexit__(*exc)

    async def start(
        self, config: AnnotationConfig, record: Recorder, index: int, document_id: str
    ) -> ChatSession:
        session = ChatSession(self, config, "local-" + str(uuid.uuid4()))
        record(
            {
                "kind": "session_start",
                "document_id": document_id,
                "index": index,
                "thread": {"id": session.id, "storage": "local_message_history"},
                "backend": self.identity["backend"],
            }
        )
        return session

    async def resume(
        self, config: AnnotationConfig, rows: Sequence[Mapping[str, Any]]
    ) -> ChatSession:
        last = rows[-1]
        session = ChatSession(self, config, last["continuation_thread_id"])
        history = rows[-last["session_segments"] :]
        if not history or any(
            row["continuation_thread_id"] != session.id
            or row["status"] not in ("validated", "unvalidated")
            or row["session_segments"] != index + 1
            for index, row in enumerate(history)
        ):
            raise ValueError(
                "saved document history does not match its continuation receipt"
            )
        for row in history:
            session.messages.extend(
                [
                    message("user", row["input"]["prompt"]),
                    message("assistant", row["text"]),
                ]
            )
        return session


class ChatSession:
    def __init__(
        self, backend: ChatCompletions, config: AnnotationConfig, session_id: str
    ) -> None:
        self.backend, self.config, self.id = backend, config, session_id
        self.messages = [message("developer", config.prefix)] + [
            message(m.role, m.content) for m in config.fixed_messages
        ]
        if backend.identity["cache_mode"] == "explicit":
            self.messages[-1]["content"][-1]["prompt_cache_breakpoint"] = {
                "mode": "explicit"
            }

    async def run_turn(
        self, prompt: str, record_response: Callable[[dict[str, Any]], None]
    ) -> Turn:
        cfg, identity = self.config, self.backend.identity
        request = {
            "model": cfg.model,
            "reasoning_effort": cfg.effort,
            "messages": self.messages + [message("user", prompt)],
            "max_completion_tokens": identity["max_completion_tokens"],
            "service_tier": identity["service_tier"],
            "store": False,
            "n": 1,
            "stream": False,
        }
        if identity["prompt_cache_options"] is not None:
            request["prompt_cache_options"] = identity["prompt_cache_options"]
        try:
            async with asyncio.timeout(cfg.timeout):
                response = await self.backend.client.post(
                    ENDPOINT, json=request, timeout=cfg.timeout
                )
        except httpx.HTTPError as error:
            raise RuntimeError(
                f"Chat Completions transport failed ({type(error).__name__}); reconcile before retrying"
            ) from error
        raw = {
            "backend": identity["backend"],
            "request": request,
            "status_code": response.status_code,
            "request_id": response.headers.get("x-request-id"),
            "body": response.text,
        }
        record_response(raw)
        if response.status_code != 200:
            raise RuntimeError(
                f"Chat Completions HTTP {response.status_code}; inspect the recorded response; no automatic replay"
            )
        turn = parse_response(json.loads(response.text), self.id)
        if turn.rejection is None:
            self.messages.extend(
                [message("user", prompt), message("assistant", turn.text)]
            )
        return turn


def parse_response(body: Any, session_id: str) -> Turn:
    if (
        not isinstance(body, dict)
        or not isinstance(body.get("id"), str)
        or not body["id"]
    ):
        raise ValueError("Chat Completions response has no completion id")
    choices, usage = body.get("choices"), body.get("usage")
    if (
        not isinstance(choices, list)
        or len(choices) != 1
        or not isinstance(choices[0], dict)
    ):
        raise ValueError("Chat Completions response must contain one choice")
    if not isinstance(usage, dict):
        raise TypeError("Chat Completions response has no usage object")
    counts = {
        "input_tokens": count(usage, "prompt_tokens"),
        "output_tokens": count(usage, "completion_tokens"),
    }
    for details_key, fields in (
        (
            "prompt_tokens_details",
            {
                "cached_tokens": "cached_input_tokens",
                "cache_write_tokens": "cache_write_input_tokens",
            },
        ),
        ("completion_tokens_details", {"reasoning_tokens": "reasoning_output_tokens"}),
    ):
        details = usage.get(details_key)
        if details is not None:
            if not isinstance(details, dict):
                raise ValueError(f"Chat Completions {details_key} must be an object")
            for source, target in fields.items():
                if source in details and details[source] is not None:
                    counts[target] = count(details, source)
    choice = choices[0]
    answer = choice.get("message")
    if not isinstance(answer, dict) or answer.get("role") != "assistant":
        raise ValueError("Chat Completions choice has no assistant message")
    finish = choice.get("finish_reason")
    if (
        finish not in ("stop", "length", "content_filter")
        or answer.get("tool_calls")
        or answer.get("function_call")
    ):
        raise ValueError(
            "Chat Completions returned an unsupported finish reason or tool call"
        )
    rejection = None if finish == "stop" else f"Chat Completions finish_reason={finish}"
    text, refusal = answer.get("content"), answer.get("refusal")
    if refusal is not None:
        if not isinstance(refusal, str):
            raise ValueError("Chat Completions refusal must be text")
        rejection = "Chat Completions refusal"
    if text is None and rejection is not None:
        text = ""
    if not isinstance(text, str):
        raise TypeError("Chat Completions content must be text")
    if not text and rejection is None:
        rejection = "Chat Completions returned empty content"
    return Turn(text, counts, session_id, body["id"], rejection)


def count(values: Mapping[str, Any], key: str) -> int:
    value = values.get(key)
    if type(value) is not int or value < 0:
        raise ValueError(f"Chat Completions usage {key} must be a nonnegative integer")
    return value
