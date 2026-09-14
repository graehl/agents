import asyncio
import sys
from builtins import ExceptionGroup

import pytest

from document_annotation.codex import CodexAppServer
from document_annotation.messages import FixedMessage
from document_annotation.runner import AnnotationConfig, DocumentAnnotator, Segment

FAKE_SERVER = r"""
import json
import sys

threads = {}
next_turn = 0
rejected = set()

def send(value):
    print(json.dumps(value), flush=True)

for line in sys.stdin:
    m = json.loads(line)
    method, p = m['method'], m.get('params', {})
    if method == 'initialize':
        send({'id': m['id'], 'result': {'userAgent': 'fixture'}})
    elif method == 'initialized':
        pass
    elif method == 'thread/start':
        tid = str(len(threads) + 1)
        threads[tid] = {'prefix': p['baseInstructions'], 'prompts': [], 'turns': [], 'fixed': []}
        send({'id': m['id'], 'result': {'thread': {'id': tid, 'instructionSources': []}}})
    elif method == 'thread/resume':
        tid = p['threadId']
        assert tid in threads
        send({'id': m['id'], 'result': {'thread': {'id': tid, 'instructionSources': []}}})
    elif method == 'thread/read':
        tid = p['threadId']
        send({'id': m['id'], 'result': {'thread': {'id': tid, 'turns': threads[tid]['turns']}}})
    elif method == 'thread/inject_items':
        threads[p['threadId']]['fixed'].extend(p['items'])
        send({'id': m['id'], 'result': {}})
    elif method == 'turn/start':
        next_turn += 1
        tid, turn = p['threadId'], str(next_turn)
        prompt = p['input'][0]['text']
        history = threads[tid]['prompts']
        text = json.dumps({'prefix': threads[tid]['prefix'], 'prior': list(history), 'prompt': prompt, 'fixed': threads[tid]['fixed']})
        if prompt == 'retry' and prompt not in rejected:
            rejected.add(prompt)
            text = 'invalid'
        history.append(prompt)
        threads[tid]['turns'].append({'id': turn, 'status': 'inProgress'})
        send({'id': m['id'], 'result': {'turn': {'id': turn}}})
        if prompt == 'stall':
            continue
        threads[tid]['turns'][-1]['status'] = 'completed'
        send({'method': 'item/completed', 'params': {'turnId': turn, 'item': {'type': 'agentMessage', 'text': text}}})
        send({'method': 'thread/tokenUsage/updated', 'params': {'turnId': turn, 'tokenUsage': {'last': {'inputTokens': 100 + len(history), 'cachedInputTokens': 90 if len(history) > 1 else 0, 'outputTokens': 5}}}})
        send({'method': 'turn/completed', 'params': {'turn': {'id': turn, 'status': 'completed'}}})
    elif method == 'turn/interrupt':
        tid, turn = p['threadId'], p['turnId']
        threads[tid]['turns'][-1]['status'] = 'interrupted'
        send({'id': m['id'], 'result': {}})
        send({'method': 'turn/completed', 'params': {'turn': {'id': turn, 'status': 'interrupted'}}})
"""


@pytest.mark.parametrize("seeded", [False, True])
def test_documents_keep_order_without_sharing_history_and_retry_fresh(tmp_path, seeded):
    import json

    async def exercise():
        async with CodexAppServer(
            [sys.executable, "-u", "-c", FAKE_SERVER], env={}, request_timeout=2
        ) as server:
            runner = DocumentAnnotator(
                server,
                AnnotationConfig(
                    prefix="fixed bytes\n",
                    model="test-model",
                    effort="low",
                    cwd=str(tmp_path),
                    max_segments_per_session=8,
                    max_input_tokens=1000,
                    retries=1,
                    validator_id="json-v1",
                    fixed_messages=(
                        FixedMessage("user", "Label carefully."),
                        FixedMessage("assistant", "I will do a good job."),
                    )
                    if seeded
                    else (),
                ),
            )
            events = []
            result = await runner.annotate(
                [
                    Segment("A", "1", "first"),
                    Segment("B", "1", "separate"),
                    Segment("A", "2", "retry"),
                    Segment("A", "3", "last"),
                ],
                validate=lambda text, segment: (
                    "not JSON" if text == "invalid" else None
                ),
                record=events.append,
            )
            return result, events

    results, events = asyncio.run(exercise())
    assert [(r["document_id"], r["segment_id"]) for r in results] == [
        ("A", "1"),
        ("B", "1"),
        ("A", "2"),
        ("A", "3"),
    ]
    assert json.loads(results[1]["text"])["prior"] == []
    assert json.loads(results[2]["text"])["prior"] == []
    assert json.loads(results[3]["text"])["prior"] == ["retry"]
    assert json.loads(results[0]["text"])["prefix"] == "fixed bytes\n"
    assert len([e for e in events if e["kind"] == "attempt_response"]) == 5
    assert results[2]["attempts"] == 2
    assert results[2]["usage"]["input_tokens"] == 203
    assert len([e for e in events if e["kind"] == "fixed_messages_complete"]) == (
        3 if seeded else 0
    )
    fixed = [json.loads(row["text"])["fixed"] for row in results]
    assert all(items == fixed[0] for items in fixed)
    assert len(fixed[0]) == (2 if seeded else 0)


def test_no_validator_retains_raw_outputs_without_format_retries(tmp_path):
    async def exercise():
        async with CodexAppServer(
            [sys.executable, "-u", "-c", FAKE_SERVER], env={}, request_timeout=2
        ) as server:
            runner = DocumentAnnotator(
                server,
                AnnotationConfig(
                    prefix="fixed",
                    model="test",
                    effort="low",
                    cwd=str(tmp_path),
                    max_segments_per_session=1,
                    max_input_tokens=1000,
                ),
            )
            return await runner.annotate(
                [Segment("A", "1", "retry")], record=lambda _: None
            )

    result = asyncio.run(exercise())[0]
    assert result["status"] == "unvalidated"
    assert result["text"] == "invalid"
    assert result["attempts"] == 1


def test_repeated_rejection_is_bounded_and_next_segment_has_clean_context(tmp_path):
    import json

    async def exercise():
        async with CodexAppServer(
            [sys.executable, "-u", "-c", FAKE_SERVER], env={}, request_timeout=2
        ) as server:
            runner = DocumentAnnotator(
                server,
                AnnotationConfig(
                    prefix="fixed",
                    model="test",
                    effort="low",
                    cwd=str(tmp_path),
                    max_segments_per_session=8,
                    max_input_tokens=1000,
                    retries=1,
                    validator_id="v1",
                ),
            )
            return await runner.annotate(
                [Segment("A", "1", "bad"), Segment("A", "2", "good")],
                validate=lambda text, segment: (
                    "reject" if segment.segment_id == "1" else None
                ),
                record=lambda _: None,
            )

    result = asyncio.run(exercise())
    assert result[0]["status"] == "rejected"
    assert result[0]["attempts"] == 2
    assert result[0]["continuation_thread_id"] is None
    assert json.loads(result[1]["text"])["prior"] == []


def test_failed_initialize_reaps_the_owned_server():
    from document_annotation.codex import CodexAppServerError

    async def exercise():
        server = CodexAppServer(
            [sys.executable, "-u", "-c", "import sys; sys.exit(1)"],
            env={},
            request_timeout=1,
        )
        with pytest.raises(CodexAppServerError):
            await server.__aenter__()
        assert server.process is None

    asyncio.run(exercise())


@pytest.mark.parametrize("stop", ["timeout", "cancel"])
def test_stopping_an_active_turn_confirms_interrupt_and_reaps_server(tmp_path, stop):
    async def exercise():
        async with CodexAppServer(
            [sys.executable, "-u", "-c", FAKE_SERVER], env={}, request_timeout=2
        ) as server:
            thread = await server.start_protocol_root(
                base_instructions="fixed", model="test", cwd=str(tmp_path)
            )
            task = asyncio.create_task(
                server.run_turn(
                    thread["id"],
                    "stall",
                    model="test",
                    effort="low",
                    cwd=str(tmp_path),
                    timeout=0.05 if stop == "timeout" else 5,
                )
            )
            if stop == "cancel":

                async def wait_until_started():
                    while not (await server.read_thread(thread["id"]))["turns"]:
                        await asyncio.sleep(0.001)

                await asyncio.wait_for(wait_until_started(), timeout=2)
                task.cancel()
            with pytest.raises(
                asyncio.TimeoutError if stop == "timeout" else asyncio.CancelledError
            ):
                await task
            final = await server.read_thread(thread["id"])
            assert final["turns"][-1]["status"] == "interrupted"
        assert server.process is None

    asyncio.run(exercise())


def test_resume_keeps_completed_prefix_without_repeating_annotation(tmp_path):
    import json

    async def exercise():
        async with CodexAppServer(
            [sys.executable, "-u", "-c", FAKE_SERVER], env={}, request_timeout=2
        ) as server:
            runner = DocumentAnnotator(
                server,
                AnnotationConfig(
                    prefix="fixed",
                    model="test",
                    effort="low",
                    cwd=str(tmp_path),
                    max_segments_per_session=8,
                    max_input_tokens=1000,
                    fixed_messages=(
                        FixedMessage("assistant", "I will do a good job."),
                    ),
                ),
            )
            first = Segment("A", "1", "one")
            prior = await runner.annotate([first], record=lambda _: None)
            events = []
            result = await runner.annotate(
                [first, Segment("A", "2", "two")], record=events.append, completed=prior
            )
            assert len([e for e in events if e["kind"] == "attempt_start"]) == 1
            assert json.loads(result[1]["text"])["prior"] == ["one"]
            assert len(json.loads(result[1]["text"])["fixed"]) == 1
            assert not any(e["kind"].startswith("fixed_messages") for e in events)

    asyncio.run(exercise())


def test_journal_refuses_unfinished_attempts_and_partial_lines(tmp_path):
    from document_annotation.journal import Journal

    journal = Journal(tmp_path / "events.jsonl")
    journal.write({"kind": "attempt_start", "index": 0})
    with pytest.raises(ValueError, match="unfinished attempts"):
        journal.completed()
    with journal.path.open("a") as stream:
        stream.write("{")
    with pytest.raises(ValueError, match="incomplete journal line"):
        journal.completed()


@pytest.mark.parametrize("with_validator", [False, True])
@pytest.mark.parametrize("with_fixed_messages", [False, True])
def test_cli_runs_real_stdio_transport_and_refuses_changed_resume(
    tmp_path, with_validator, with_fixed_messages
):
    import json
    import subprocess
    from pathlib import Path

    executable = tmp_path / "codex-fixture"
    executable.write_text(
        "#!"
        + sys.executable
        + '\nimport sys\nif "--version" in sys.argv:\n    print("fixture-v1")\n    sys.exit(0)\n'
        + FAKE_SERVER
    )
    executable.chmod(0o700)
    auth = tmp_path / "auth"
    auth.mkdir()
    (auth / "auth.json").write_text(
        json.dumps({"tokens": {"access_token": "fixture-only"}})
    )
    prompt, inputs, output = (
        tmp_path / "prompt.txt",
        tmp_path / "input.jsonl",
        tmp_path / "out",
    )
    prompt.write_bytes(b"fixed\r\n")
    inputs.write_text(
        json.dumps(
            {
                "document_id": "A",
                "segment_id": "1",
                "prompt": "retry" if with_validator else "one",
            }
        )
        + "\n"
    )
    entry = Path(__file__).resolve().parents[1] / "scripts/document-annotate"
    command = [
        sys.executable,
        str(entry),
        "--input",
        str(inputs),
        "--prompt",
        str(prompt),
        "--out",
        str(output),
        "--auth-home",
        str(auth),
        "--model",
        "test",
        "--effort",
        "low",
        "--max-session-segments",
        "8",
        "--max-input-tokens",
        "1000",
        "--codex-command",
        str(executable),
        "--json",
    ]
    if with_validator:
        (tmp_path / "annotation_check.py").write_text(
            'async def check(text, segment):\n    return "invalid JSON" if text == "invalid" else None\n'
        )
        command += ["--validator", "annotation_check:check"]
    messages = tmp_path / "fixed-messages.json"
    if with_fixed_messages:
        messages.write_text(
            json.dumps(
                [
                    {"role": "user", "content": "Follow the annotation protocol."},
                    {"role": "assistant", "content": "I will do a good job.\r\n"},
                ]
            )
        )
        command += ["--fixed-messages", str(messages)]
    first = subprocess.run(command, cwd=tmp_path, text=True, capture_output=True)
    assert first.returncode == 0, first.stderr
    assert (
        json.loads(first.stdout)["validated" if with_validator else "unvalidated"] == 1
    )
    rows = [
        json.loads(line) for line in (output / "results.jsonl").read_text().splitlines()
    ]
    assert rows[0]["attempts"] == (2 if with_validator else 1)
    fixed = json.loads(rows[0]["text"])["fixed"]
    assert len(fixed) == (2 if with_fixed_messages else 0)
    if with_fixed_messages:
        assert [(item["role"], item["content"][0]["type"]) for item in fixed] == [
            ("user", "input_text"),
            ("assistant", "output_text"),
        ]
        assert fixed[1]["content"][0]["text"] == "I will do a good job.\r\n"
    assert (output / "prefix.txt").read_bytes() == b"fixed\r\n"
    assert (output / ".codex/auth.json").stat().st_mode & 0o777 == 0o600
    events_before = (output / "events.jsonl").read_bytes()
    resumed = subprocess.run(
        command + ["--resume", "--pretty"], cwd=tmp_path, text=True, capture_output=True
    )
    assert resumed.returncode == 2  # mutually exclusive output encodings
    resumed = subprocess.run(
        command + ["--resume"], cwd=tmp_path, text=True, capture_output=True
    )
    assert resumed.returncode == 0, resumed.stderr
    assert (output / "events.jsonl").read_bytes() == events_before
    if with_fixed_messages:
        messages.write_text("[]")
        changed = subprocess.run(
            command + ["--resume"], cwd=tmp_path, text=True, capture_output=True
        )
        assert changed.returncode != 0
        assert "changed" in changed.stderr
        assert (output / "events.jsonl").read_bytes() == events_before
    prompt.write_text("changed")
    changed = subprocess.run(
        command + ["--resume"], cwd=tmp_path, text=True, capture_output=True
    )
    assert changed.returncode != 0
    assert "changed" in json.loads(changed.stderr.splitlines()[-1])["error"]["message"]


def test_resume_refuses_a_thread_changed_outside_the_campaign(tmp_path):
    async def exercise():
        async with CodexAppServer(
            [sys.executable, "-u", "-c", FAKE_SERVER], env={}, request_timeout=2
        ) as server:
            runner = DocumentAnnotator(
                server, AnnotationConfig("fixed", "test", "low", str(tmp_path), 8, 1000)
            )
            first = Segment("A", "1", "one")
            prior = await runner.annotate([first], record=lambda _: None)
            await server.run_turn(
                prior[0]["thread_id"],
                "outside turn",
                cwd=str(tmp_path),
                model="test",
                effort="low",
                timeout=2,
            )
            events = []
            with pytest.raises(ExceptionGroup) as error:
                await runner.annotate(
                    [first, Segment("A", "2", "two")],
                    completed=prior,
                    record=events.append,
                )
            assert "no longer ends" in str(error.value.exceptions[0])
            assert events == []

    asyncio.run(exercise())


def test_validator_exception_preserves_response_and_does_not_retry(tmp_path):
    from document_annotation.journal import Journal

    async def broken(text, segment):
        raise RuntimeError("validator bug")

    async def exercise():
        async with CodexAppServer(
            [sys.executable, "-u", "-c", FAKE_SERVER], env={}, request_timeout=2
        ) as server:
            runner = DocumentAnnotator(
                server,
                AnnotationConfig(
                    "fixed",
                    "test",
                    "low",
                    str(tmp_path),
                    8,
                    1000,
                    validator_id="broken-v1",
                ),
            )
            journal = Journal(tmp_path / "events.jsonl")
            with pytest.raises(ExceptionGroup):
                await runner.annotate(
                    [Segment("A", "1", "one")], record=journal.write, validate=broken
                )
            text = journal.path.read_text()
            assert text.count('"kind": "attempt_start"') == 1
            assert '"kind": "attempt_response"' in text
            assert '"kind": "segment_result"' not in text
            with pytest.raises(ValueError, match="unfinished attempts"):
                journal.completed()
        assert server.process is None

    asyncio.run(exercise())


@pytest.mark.parametrize("segment_cap,input_cap", [(1, 1000), (8, 101)])
def test_context_bounds_start_clean_sessions(tmp_path, segment_cap, input_cap):
    import json

    async def exercise():
        async with CodexAppServer(
            [sys.executable, "-u", "-c", FAKE_SERVER], env={}, request_timeout=2
        ) as server:
            runner = DocumentAnnotator(
                server,
                AnnotationConfig(
                    "fixed", "test", "low", str(tmp_path), segment_cap, input_cap
                ),
            )
            return await runner.annotate(
                [Segment("A", "1", "one"), Segment("A", "2", "two")],
                record=lambda _: None,
            )

    rows = asyncio.run(exercise())
    assert json.loads(rows[1]["text"])["prior"] == []
    assert rows[1]["attempts"] == (1 if segment_cap == 1 else 2)


def test_profile_copies_only_subscription_auth_and_blocks_api_key(
    tmp_path, monkeypatch
):
    import json

    from document_annotation.isolation import prepare_profile

    auth, output = tmp_path / "auth", tmp_path / "out"
    auth.mkdir()
    output.mkdir()
    (auth / "auth.json").write_text(json.dumps({"tokens": {"access_token": "fixture"}}))
    (auth / "AGENTS.md").write_text("not annotation instructions")
    (auth / "config.toml").write_text("not annotation config")
    monkeypatch.setenv("OPENAI_API_KEY", "fixture-key")
    monkeypatch.setenv("AGENTCTL_SESSION_ID", "parent-session")
    env = prepare_profile(auth, output, resume=False)
    assert "OPENAI_API_KEY" not in env
    assert "AGENTCTL_SESSION_ID" not in env
    assert not (output / ".codex/AGENTS.md").exists()
    assert (output / ".codex/config.toml").read_text() != "not annotation config"
    (auth / "auth.json").write_text(json.dumps({"OPENAI_API_KEY": "fixture-key"}))
    with pytest.raises(ValueError, match="API-key transport is not implemented"):
        prepare_profile(auth, tmp_path / "other", resume=False)
