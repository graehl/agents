import asyncio
import json
from builtins import ExceptionGroup
from dataclasses import replace

import httpx
import pytest

from document_annotation.chat import ChatCompletions
from document_annotation.cli import main, parser, run
from document_annotation.journal import Journal
from document_annotation.messages import FixedMessage
from document_annotation.runner import AnnotationConfig, DocumentAnnotator, Segment


def install_http(monkeypatch, respond):
    original = httpx.AsyncClient

    class NetworkFixture(original):
        def __init__(self, **kwargs):
            super().__init__(transport=httpx.MockTransport(respond), **kwargs)

    monkeypatch.setattr(httpx, "AsyncClient", NetworkFixture)


def completion(
    text="label", *, completion_id="chatcmpl-test", finish="stop", refusal=None
):
    return {
        "id": completion_id,
        "model": "gpt-5.6-fixture",
        "choices": [
            {
                "index": 0,
                "finish_reason": finish,
                "message": {"role": "assistant", "content": text, "refusal": refusal},
            }
        ],
        "usage": {"prompt_tokens": 1400, "completion_tokens": 9},
    }


def test_chat_cli_requires_key_and_marks_end_of_all_fixed_messages(
    tmp_path, monkeypatch, capfd
):
    prompt, segments, fixed = [
        tmp_path / name for name in ("prompt", "segments", "fixed")
    ]
    prompt.write_text("fixed instructions\n")
    segments.write_text(
        json.dumps({"document_id": "A", "segment_id": "1", "prompt": "variable"}) + "\n"
    )
    fixed.write_text(
        json.dumps(
            [
                {"role": "user", "content": "Follow the protocol."},
                {"role": "assistant", "content": "I will do a good job."},
            ]
        )
    )
    output = tmp_path / "campaign"
    argv = [
        "document-annotate",
        "--backend",
        "openai-chat-completions",
        "--input",
        str(segments),
        "--prompt",
        str(prompt),
        "--fixed-messages",
        str(fixed),
        "--out",
        str(output),
        "--model",
        "gpt-5.6",
        "--effort",
        "low",
        "--max-session-segments",
        "8",
        "--max-input-tokens",
        "5000",
        "--max-output-tokens",
        "1024",
        "--json",
    ]
    monkeypatch.setattr("sys.argv", argv)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(ValueError, match="OPENAI_API_KEY"):
        run(parser().parse_args())
    assert not output.exists()

    requests = []

    def respond(request):
        assert str(request.url) == "https://api.openai.com/v1/chat/completions"
        assert request.headers["authorization"] == "Bearer fixture-key"
        body = json.loads(request.content)
        requests.append(body)
        return httpx.Response(
            200,
            json={
                "id": "chatcmpl-fixture",
                "model": "gpt-5.6-fixture",
                "choices": [
                    {
                        "index": 0,
                        "finish_reason": "stop",
                        "message": {
                            "role": "assistant",
                            "content": "label",
                            "refusal": None,
                        },
                    }
                ],
                "usage": {
                    "prompt_tokens": 1400,
                    "completion_tokens": 9,
                    "prompt_tokens_details": {
                        "cached_tokens": 1024,
                        "cache_write_tokens": 128,
                    },
                    "completion_tokens_details": {"reasoning_tokens": 5},
                },
            },
            headers={"x-request-id": "req-fixture"},
        )

    install_http(monkeypatch, respond)
    monkeypatch.setenv("OPENAI_API_KEY", "fixture-key")
    assert main() == 0, capfd.readouterr().err
    assert len(requests) == 1
    request = requests[0]
    assert request["prompt_cache_options"] == {"mode": "explicit", "ttl": "30m"}
    assert [m["role"] for m in request["messages"]] == [
        "developer",
        "user",
        "assistant",
        "user",
    ]
    assert [
        m["content"][0].get("prompt_cache_breakpoint") for m in request["messages"]
    ] == [None, None, {"mode": "explicit"}, None]
    assert request["messages"][0]["content"][0]["text"] == "fixed instructions\n"
    assert request["messages"][-1]["content"][0]["text"] == "variable"
    row = json.loads((output / "results.jsonl").read_text())
    assert row["status"] == "unvalidated"
    assert row["usage"]["cached_input_tokens"] == 1024
    assert row["usage"]["cache_write_input_tokens"] == 128
    assert row["usage"]["reasoning_output_tokens"] == 5
    assert not (output / ".codex").exists()
    manifest = json.loads((output / "manifest.json").read_text())
    assert manifest["backend"] == "openai-chat-completions"
    for path in output.rglob("*"):
        if path.is_file():
            assert "fixture-key" not in path.read_text()
    monkeypatch.setattr("sys.argv", argv + ["--resume"])
    assert main() == 0
    assert len(requests) == 1

    monkeypatch.setattr(
        "sys.argv", argv + ["--resume", "--chat-cache-mode", "automatic"]
    )
    with pytest.raises(ValueError, match="changed"):
        run(parser().parse_args())
    assert len(requests) == 1
    monkeypatch.setattr("sys.argv", argv[:1] + argv[3:])
    with pytest.raises(ValueError, match="codex-subscription requires --auth-home"):
        run(parser().parse_args())


@pytest.mark.parametrize("cache_mode", ["explicit", "automatic"])
def test_chat_reconstructs_only_accepted_document_history_after_retry_and_resume(
    tmp_path, monkeypatch, cache_mode
):
    requests = []

    def respond(request):
        body = json.loads(request.content)
        prompt = body["messages"][-1]["content"][0]["text"]
        reject = prompt == "two" and not any(
            r["messages"][-1]["content"][0]["text"] == "two" for r in requests
        )
        requests.append(body)
        return httpx.Response(
            200,
            json=completion(
                "bad" if reject else prompt + "-label",
                completion_id=f"chatcmpl-{len(requests)}",
            ),
        )

    install_http(monkeypatch, respond)
    cfg = AnnotationConfig(
        "fixed\r\n",
        "gpt-5.6",
        "low",
        str(tmp_path),
        2,
        5000,
        validator_id="v1",
        fixed_messages=(FixedMessage("assistant", "canned"),),
    )
    segments = [
        Segment("A", "1", "one"),
        Segment("B", "1", "solo"),
        Segment("A", "2", "two"),
        Segment("A", "3", "three"),
        Segment("A", "4", "four"),
    ]

    async def validate(text, segment):
        return "bad annotation" if text == "bad" else None

    async def exercise():
        async with ChatCompletions(
            "fixture", max_output_tokens=100, cache_mode=cache_mode
        ) as backend:
            prior = await DocumentAnnotator(backend, cfg).annotate(
                segments[:3], record=lambda _: None, validate=validate
            )
        events = []
        async with ChatCompletions(
            "fixture", max_output_tokens=100, cache_mode=cache_mode
        ) as backend:
            result = await DocumentAnnotator(backend, cfg).annotate(
                segments, completed=prior, record=events.append, validate=validate
            )
            with pytest.raises(ValueError, match="config and input"):
                await DocumentAnnotator(
                    backend, replace(cfg, fixed_messages=())
                ).annotate(
                    segments, completed=result, record=events.append, validate=validate
                )
        return result, events

    rows, events = asyncio.run(exercise())
    assert len(requests) == 6
    assert [r["index"] for r in rows] == list(range(5))
    assert rows[2]["attempts"] == 2
    assert rows[2]["usage"] == {"input_tokens": 2800, "output_tokens": 18}
    for body in requests:
        markers = [
            i
            for i, m in enumerate(body["messages"])
            if "prompt_cache_breakpoint" in m["content"][0]
        ]
        assert markers == ([1] if cache_mode == "explicit" else [])
        assert ("prompt_cache_options" in body) == (cache_mode == "explicit")
        assert body["messages"][0]["content"][0]["text"] == "fixed\r\n"
    suffixes = [[m["content"][0]["text"] for m in r["messages"][2:]] for r in requests]
    assert ["solo"] in suffixes
    assert ["one", "one-label", "two"] in suffixes
    assert ["two"] in suffixes
    assert ["two", "two-label", "three"] in suffixes
    assert ["four"] in suffixes
    assert all("bad" not in suffix for suffix in suffixes)
    assert len([e for e in events if e["kind"] == "attempt_start"]) == 2


@pytest.mark.parametrize("failure", ["http", "malformed", "usage", "timeout", "cancel"])
def test_chat_failure_is_not_replayed_and_blocks_automatic_resume(
    tmp_path, monkeypatch, failure
):
    requests = []

    async def respond(request):
        requests.append(request)
        if failure == "timeout":
            await asyncio.sleep(1)
        if failure == "cancel":
            raise asyncio.CancelledError()
        if failure == "malformed":
            return httpx.Response(200, text="not JSON")
        body = completion()
        if failure == "usage":
            del body["usage"]
        return httpx.Response(503 if failure == "http" else 200, json=body)

    install_http(monkeypatch, respond)
    journal = Journal(tmp_path / "events.jsonl")

    async def exercise():
        async with ChatCompletions("fixture", max_output_tokens=100) as backend:
            cfg = AnnotationConfig(
                "fixed", "gpt-5.6", "low", str(tmp_path), 2, 5000, timeout=0.01
            )
            with pytest.raises(
                ExceptionGroup if failure != "cancel" else asyncio.CancelledError
            ):
                await DocumentAnnotator(backend, cfg).annotate(
                    [Segment("A", "1", "one")], record=journal.write
                )
        assert backend.client.is_closed

    asyncio.run(exercise())
    assert len(requests) == 1
    events = [json.loads(line) for line in journal.path.read_text().splitlines()]
    assert any(e["kind"] == "attempt_response" for e in events) == (
        failure not in ("timeout", "cancel")
    )
    assert events[-1]["kind"] == "attempt_error"
    with pytest.raises(ValueError, match="unfinished attempts"):
        journal.completed()


@pytest.mark.parametrize(
    "rejection", ["length", "content_filter", "refusal", "empty", "context"]
)
def test_chat_unusable_outputs_retry_fresh_even_without_validator(
    tmp_path, monkeypatch, rejection
):
    requests = []

    def respond(request):
        requests.append(json.loads(request.content))
        body = completion(
            text=""
            if rejection == "empty"
            else None
            if rejection in ("content_filter", "refusal")
            else "partial",
            finish=rejection if rejection in ("length", "content_filter") else "stop",
            refusal="declined" if rejection == "refusal" else None,
        )
        return httpx.Response(200, json=body)

    install_http(monkeypatch, respond)

    async def exercise():
        async with ChatCompletions("fixture", max_output_tokens=100) as backend:
            cfg = AnnotationConfig(
                "fixed",
                "gpt-5.6",
                "low",
                str(tmp_path),
                8,
                100 if rejection == "context" else 5000,
            )
            return await DocumentAnnotator(backend, cfg).annotate(
                [Segment("A", "1", "one"), Segment("A", "2", "two")],
                record=lambda _: None,
            )

    rows = asyncio.run(exercise())
    assert len(requests) == 4
    assert all(
        row["status"] == "rejected"
        and row["attempts"] == 2
        and row["continuation_thread_id"] is None
        for row in rows
    )
    assert all(len(r["messages"]) == 2 for r in requests)
    assert all(
        r["messages"][0]["content"][0]["prompt_cache_breakpoint"]
        == {"mode": "explicit"}
        for r in requests
    )
