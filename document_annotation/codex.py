"""Async Codex app-server transport for document annotation."""

from __future__ import annotations

import asyncio
import hashlib
import json
from collections import defaultdict, deque
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, Self

APP_SERVER_JSONL_LIMIT_BYTES = 8 * 1024 * 1024
TURN_INTERRUPT_TIMEOUT_SECONDS = 30.0
TERMINAL_TURN_STATUSES = frozenset({"completed", "failed", "interrupted"})
CLIENT_SOURCE_SHA256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


class CodexAppServerError(RuntimeError):
    """The app-server transport or a protocol request failed."""


def _required_mapping(value: Any, description: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise CodexAppServerError(f"app-server returned no {description}")
    return value


def app_server_usage(events: Sequence[Mapping[str, Any]]) -> dict[str, int]:
    """Return the final per-turn usage notification in exec-compatible names."""
    last_usage: Mapping[str, Any] | None = None
    for event in events:
        if event.get("method") != "thread/tokenUsage/updated":
            continue
        params = event.get("params")
        if not isinstance(params, Mapping):
            continue
        token_usage = params.get("tokenUsage")
        if not isinstance(token_usage, Mapping):
            continue
        candidate = token_usage.get("last")
        if isinstance(candidate, Mapping):
            last_usage = candidate
    if last_usage is None:
        raise CodexAppServerError(
            "completed app-server turn has no token-usage notification"
        )
    return {
        "input_tokens": int(last_usage.get("inputTokens") or 0),
        "cached_input_tokens": int(last_usage.get("cachedInputTokens") or 0),
        "cache_write_input_tokens": int(last_usage.get("cacheWriteInputTokens") or 0),
        "output_tokens": int(last_usage.get("outputTokens") or 0),
        "reasoning_output_tokens": int(last_usage.get("reasoningOutputTokens") or 0),
    }


def app_server_response(
    events: Sequence[Mapping[str, Any]],
    *,
    thread_id: str,
    turn_id: str,
    stderr: str,
) -> dict[str, Any]:
    """Translate one completed app-server turn into the labeler's response contract."""
    messages: list[str] = []
    completed_turn: Mapping[str, Any] | None = None
    for event in events:
        params = event.get("params")
        if not isinstance(params, Mapping):
            continue
        if event.get("method") == "item/completed":
            item = params.get("item")
            if (
                isinstance(item, Mapping)
                and item.get("type") == "agentMessage"
                and isinstance(item.get("text"), str)
            ):
                messages.append(str(item["text"]))
        elif event.get("method") == "turn/completed":
            turn = params.get("turn")
            if isinstance(turn, Mapping):
                completed_turn = turn
    if completed_turn is None:
        raise CodexAppServerError("app-server emitted no turn/completed notification")
    if completed_turn.get("status") != "completed":
        raise CodexAppServerError(
            f"app-server turn {turn_id} ended with status {completed_turn.get('status')!r}: "
            f"{completed_turn.get('error')!r}"
        )
    if not messages:
        raise CodexAppServerError("app-server emitted no completed assistant message")
    return {
        "content": [{"type": "text", "text": messages[-1]}],
        "usage": app_server_usage(events),
        "codex_events": list(events),
        "codex_stderr": stderr,
        "app_server": {"thread_id": thread_id, "turn_id": turn_id},
        "transport": {
            "implementation": "document_annotation.codex",
            "source_sha256": CLIENT_SOURCE_SHA256,
        },
    }


class CodexAppServer:
    """One initialized JSONL app-server connection with concurrent turn routing."""

    def __init__(
        self,
        command: Sequence[str],
        *,
        env: Mapping[str, str],
        request_timeout: float,
    ) -> None:
        self.command = list(command)
        self.env = dict(env)
        self.request_timeout = request_timeout
        self.process: asyncio.subprocess.Process | None = None
        self._next_request_id = 1
        self._requests: dict[int, asyncio.Future[Mapping[str, Any]]] = {}
        self._turn_events: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
        self._turn_completions: dict[str, Mapping[str, Any]] = {}
        self._turn_waiters: dict[str, asyncio.Future[Mapping[str, Any]]] = {}
        self._stderr_lines: deque[str] = deque(maxlen=200)
        self._reader_task: asyncio.Task[None] | None = None
        self._stderr_task: asyncio.Task[None] | None = None
        self._write_lock = asyncio.Lock()
        self._reader_error: Exception | None = None

    async def __aenter__(self) -> Self:
        self.process = await asyncio.create_subprocess_exec(
            *self.command,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=self.env,
            limit=APP_SERVER_JSONL_LIMIT_BYTES,
        )
        self._reader_task = asyncio.create_task(self._read_stdout())
        self._stderr_task = asyncio.create_task(self._read_stderr())
        try:
            await self.request(
                "initialize",
                {
                    "capabilities": {"experimentalApi": True},
                    "clientInfo": {
                        "name": "document-annotation",
                        "title": "Document annotation",
                        "version": "1",
                    },
                },
            )
            await self.notify("initialized", {})
        except BaseException:
            await self.close()
            raise
        return self

    async def __aexit__(self, *_exc: object) -> None:
        await self.close()

    def stderr(self) -> str:
        return "\n".join(self._stderr_lines)

    async def close(self) -> None:
        process = self.process
        if process is None:
            return
        if process.stdin is not None:
            process.stdin.close()
        if process.returncode is None:
            process.terminate()
            try:
                await asyncio.wait_for(process.wait(), timeout=5)
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
        for task in (self._reader_task, self._stderr_task):
            if task is not None and not task.done():
                task.cancel()
        await asyncio.gather(
            *(
                task
                for task in (self._reader_task, self._stderr_task)
                if task is not None
            ),
            return_exceptions=True,
        )
        self._fail_pending(CodexAppServerError("app-server connection closed"))
        self.process = None

    async def notify(self, method: str, params: Mapping[str, Any]) -> None:
        await self._write({"method": method, "params": dict(params)})

    async def request(
        self,
        method: str,
        params: Mapping[str, Any],
        *,
        timeout: float | None = None,
    ) -> Mapping[str, Any]:
        request_id = self._next_request_id
        self._next_request_id += 1
        future = asyncio.get_running_loop().create_future()
        self._requests[request_id] = future
        try:
            await self._write(
                {"method": method, "id": request_id, "params": dict(params)}
            )
            message = await asyncio.wait_for(
                future,
                timeout=self.request_timeout if timeout is None else timeout,
            )
        finally:
            self._requests.pop(request_id, None)
        error = message.get("error")
        if error is not None:
            raise CodexAppServerError(f"app-server {method} failed: {error!r}")
        return _required_mapping(message.get("result"), f"result for {method}")

    async def start_protocol_root(
        self,
        *,
        base_instructions: str,
        cwd: str,
        model: str,
    ) -> Mapping[str, Any]:
        result = await self.request(
            "thread/start",
            {
                "approvalPolicy": "never",
                "baseInstructions": base_instructions,
                "cwd": cwd,
                "ephemeral": False,
                "model": model,
                "sandbox": "read-only",
                "serviceName": "document-annotation",
            },
        )
        thread = _required_mapping(result.get("thread"), "thread from thread/start")
        self._require_isolated_instructions(thread)
        self._thread_id(thread)
        return thread

    async def read_thread(self, thread_id: str) -> Mapping[str, Any]:
        result = await self.request(
            "thread/read",
            {"threadId": thread_id, "includeTurns": True},
        )
        thread = _required_mapping(result.get("thread"), "thread from thread/read")
        self._thread_id(thread)
        return thread

    async def resume_thread(
        self, thread_id: str, *, base_instructions: str, cwd: str, model: str
    ) -> Mapping[str, Any]:
        result = await self.request(
            "thread/resume",
            {
                "threadId": thread_id,
                "baseInstructions": base_instructions,
                "cwd": cwd,
                "model": model,
                "approvalPolicy": "never",
                "sandbox": "read-only",
            },
        )
        thread = _required_mapping(result.get("thread"), "thread from thread/resume")
        self._require_isolated_instructions(thread)
        if self._thread_id(thread) != thread_id:
            raise CodexAppServerError("thread/resume returned a different thread")
        return thread

    async def fork_thread(
        self,
        thread_id: str,
        *,
        cwd: str,
        model: str,
        before_turn_id: str | None = None,
        base_instructions: str | None = None,
    ) -> Mapping[str, Any]:
        params: dict[str, Any] = {
            "approvalPolicy": "never",
            "cwd": cwd,
            "ephemeral": False,
            "excludeTurns": True,
            "model": model,
            "sandbox": "read-only",
            "threadId": thread_id,
        }
        if before_turn_id is not None:
            params["beforeTurnId"] = before_turn_id
        if base_instructions is not None:
            params["baseInstructions"] = base_instructions
        result = await self.request(
            "thread/fork",
            params,
        )
        thread = _required_mapping(result.get("thread"), "thread from thread/fork")
        self._require_isolated_instructions(thread)
        self._thread_id(thread)
        forked_from = thread.get("forkedFromId")
        if forked_from is not None and forked_from != thread_id:
            raise CodexAppServerError(
                f"forked thread names source {forked_from!r}, expected {thread_id!r}"
            )
        return thread

    async def run_turn(
        self,
        thread_id: str,
        prompt: str,
        *,
        cwd: str,
        model: str,
        effort: str,
        timeout: float,
    ) -> dict[str, Any]:
        result = await self.request(
            "turn/start",
            {
                "approvalPolicy": "never",
                "cwd": cwd,
                "effort": effort,
                "input": [{"type": "text", "text": prompt}],
                "model": model,
                "sandboxPolicy": {"type": "readOnly"},
                "threadId": thread_id,
            },
        )
        turn = _required_mapping(result.get("turn"), "turn from turn/start")
        turn_id = turn.get("id")
        if not isinstance(turn_id, str) or not turn_id:
            raise CodexAppServerError("turn/start returned no turn id")
        timed_out = None
        try:
            await self._wait_for_turn_completion(turn_id, timeout=timeout)
        except (asyncio.TimeoutError, asyncio.CancelledError) as error:
            timed_out = error
            interrupt_timeout = min(
                self.request_timeout, TURN_INTERRUPT_TIMEOUT_SECONDS
            )
            terminal_confirmed = False
            if turn_id not in self._turn_completions:
                try:
                    await self.request(
                        "turn/interrupt",
                        {"threadId": thread_id, "turnId": turn_id},
                        timeout=interrupt_timeout,
                    )
                except (asyncio.TimeoutError, CodexAppServerError) as interrupt_error:
                    terminal_confirmed = turn_id in self._turn_completions
                    if not terminal_confirmed:
                        terminal_confirmed = await self._turn_is_terminal(
                            thread_id,
                            turn_id,
                            timeout=interrupt_timeout,
                        )
                    if turn_id not in self._turn_completions and not terminal_confirmed:
                        raise CodexAppServerError(
                            f"timed-out app-server turn {turn_id} could not be interrupted"
                        ) from interrupt_error
            if not terminal_confirmed:
                try:
                    await self._wait_for_turn_completion(
                        turn_id, timeout=interrupt_timeout
                    )
                except asyncio.TimeoutError as completion_error:
                    terminal_confirmed = turn_id in self._turn_completions
                    if not terminal_confirmed:
                        terminal_confirmed = await self._turn_is_terminal(
                            thread_id,
                            turn_id,
                            timeout=interrupt_timeout,
                        )
                    if not terminal_confirmed:
                        raise CodexAppServerError(
                            f"interrupted app-server turn {turn_id} emitted no completion"
                        ) from completion_error
        events = self._turn_events.pop(turn_id, [])
        self._turn_completions.pop(turn_id, None)
        if timed_out is not None:
            if isinstance(timed_out, asyncio.CancelledError):
                raise timed_out
            raise asyncio.TimeoutError(
                f"app-server turn {turn_id} exceeded {timeout:g}s and was interrupted"
            ) from timed_out
        return app_server_response(
            events,
            thread_id=thread_id,
            turn_id=turn_id,
            stderr=self.stderr(),
        )

    async def _wait_for_turn_completion(self, turn_id: str, *, timeout: float) -> None:
        if turn_id in self._turn_completions:
            return
        if self._reader_error is not None:
            raise self._reader_error
        waiter = asyncio.get_running_loop().create_future()
        self._turn_waiters[turn_id] = waiter
        if turn_id in self._turn_completions and not waiter.done():
            waiter.set_result(self._turn_completions[turn_id])
        try:
            await asyncio.wait_for(waiter, timeout=timeout)
        finally:
            if self._turn_waiters.get(turn_id) is waiter:
                self._turn_waiters.pop(turn_id, None)

    async def _turn_is_terminal(
        self, thread_id: str, turn_id: str, *, timeout: float
    ) -> bool:
        result = await self.request(
            "thread/read",
            {"threadId": thread_id, "includeTurns": True},
            timeout=timeout,
        )
        thread = _required_mapping(result.get("thread"), "thread from thread/read")
        turns = thread.get("turns")
        if not isinstance(turns, list):
            raise CodexAppServerError("thread/read returned malformed turns")
        for turn in turns:
            if not isinstance(turn, Mapping) or turn.get("id") != turn_id:
                continue
            status = turn.get("status")
            if not isinstance(status, str):
                raise CodexAppServerError(
                    f"thread/read returned no status for turn {turn_id}"
                )
            return status in TERMINAL_TURN_STATUSES
        raise CodexAppServerError(f"thread/read returned no turn {turn_id}")

    @staticmethod
    def _thread_id(thread: Mapping[str, Any]) -> str:
        thread_id = thread.get("id")
        if not isinstance(thread_id, str) or not thread_id:
            raise CodexAppServerError("app-server returned no thread id")
        return thread_id

    @staticmethod
    def _require_isolated_instructions(thread: Mapping[str, Any]) -> None:
        sources = thread.get("instructionSources", [])
        if not isinstance(sources, list):
            raise CodexAppServerError(
                "app-server returned malformed instructionSources"
            )
        if sources:
            raise CodexAppServerError(
                "isolated app-server thread loaded instruction files: "
                + ", ".join(str(source) for source in sources)
            )

    async def _write(self, message: Mapping[str, Any]) -> None:
        if self._reader_error is not None:
            raise self._reader_error
        process = self.process
        if process is None or process.stdin is None or process.returncode is not None:
            raise CodexAppServerError("app-server is not running")
        encoded = (json.dumps(message, ensure_ascii=False) + "\n").encode()
        async with self._write_lock:
            process.stdin.write(encoded)
            await process.stdin.drain()

    async def _read_stdout(self) -> None:
        assert self.process is not None and self.process.stdout is not None
        try:
            while line := await self.process.stdout.readline():
                try:
                    message = json.loads(line)
                except json.JSONDecodeError as error:
                    raise CodexAppServerError(
                        f"app-server emitted malformed JSON: {line[:500]!r}"
                    ) from error
                if not isinstance(message, Mapping):
                    raise CodexAppServerError("app-server emitted a non-object message")
                request_id = message.get("id")
                if request_id is not None and message.get("method"):
                    await self._write(
                        {
                            "id": request_id,
                            "error": {
                                "code": -32601,
                                "message": "Document annotation does not serve tool or approval requests",
                            },
                        }
                    )
                    raise CodexAppServerError(
                        f"unexpected server request: {message['method']}"
                    )
                if isinstance(request_id, int) and request_id in self._requests:
                    future = self._requests[request_id]
                    if not future.done():
                        future.set_result(message)
                    continue
                params = message.get("params")
                turn_id = params.get("turnId") if isinstance(params, Mapping) else None
                if (
                    not isinstance(turn_id, str)
                    and message.get("method") == "turn/completed"
                    and isinstance(params, Mapping)
                ):
                    turn = params.get("turn")
                    turn_id = turn.get("id") if isinstance(turn, Mapping) else None
                if isinstance(turn_id, str) and turn_id:
                    self._turn_events[turn_id].append(message)
                    if message.get("method") == "turn/completed":
                        self._turn_completions[turn_id] = message
                        waiter = self._turn_waiters.get(turn_id)
                        if waiter is not None and not waiter.done():
                            waiter.set_result(message)
            if self.process.returncode is None:
                await self.process.wait()
            raise CodexAppServerError(
                f"app-server stdout closed with code {self.process.returncode}; {self.stderr()}"
            )
        except asyncio.CancelledError:
            raise
        except (OSError, ValueError, CodexAppServerError) as error:
            self._reader_error = error
            self._fail_pending(error)

    async def _read_stderr(self) -> None:
        assert self.process is not None and self.process.stderr is not None
        while line := await self.process.stderr.readline():
            self._stderr_lines.append(line.decode("utf-8", errors="replace").rstrip())

    def _fail_pending(self, error: Exception) -> None:
        for future in (*self._requests.values(), *self._turn_waiters.values()):
            if not future.done():
                future.set_exception(error)
