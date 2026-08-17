#!/usr/bin/env python3
"""Behavior tests for scripts/session-turn."""

from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import tempfile
import threading
import time
import traceback
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "session-turn"


def _assert(condition, message="assertion failed"):
    if not condition:
        raise AssertionError(message)


class FakeProviderHost:
    def __init__(self, responses, host_protocol_version=2, features=None):
        self.runtime = Path(tempfile.mkdtemp(prefix="session-turn-host-"))
        self.runtime.chmod(0o700)
        self.socket_path = self.runtime / "control.sock"
        self.token_path = self.runtime / "token"
        self.token_path.write_text("test-token\n")
        self.token_path.chmod(0o600)
        self.responses = responses
        self.requests = []
        self.server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.server.bind(str(self.socket_path))
        self.socket_path.chmod(0o600)
        self.server.listen()
        self.features = features or ["runtime-control", "session-turn"]
        descriptor = {
            "descriptorVersion": 1,
            "descriptorId": "test-host",
            "hostProtocolVersion": host_protocol_version,
            "features": self.features,
            "controlSocketPath": str(self.socket_path),
            "tokenFilePath": str(self.token_path),
            "owner": {"pid": os.getpid(), "startTime": "test"},
            "startedAt": "2026-08-12T00:00:00.000Z",
            "sourceIdentity": {},
            "buildIdentity": "test",
        }
        descriptor_path = self.runtime / "host.json"
        descriptor_path.write_text(json.dumps(descriptor) + "\n")
        descriptor_path.chmod(0o600)
        self.thread = threading.Thread(target=self._serve, daemon=True)
        self.thread.start()

    def _serve(self):
        for response in self.responses:
            connection, _ = self.server.accept()
            threading.Thread(
                target=self._handle,
                args=(connection, response),
                daemon=True,
            ).start()
        self.server.close()

    def _handle(self, connection, response):
        with connection:
            request = json.loads(connection.makefile().readline())
            self.requests.append(request)
            try:
                for record in response(request):
                    connection.sendall((json.dumps(record) + "\n").encode())
            except (BrokenPipeError, ConnectionResetError):
                pass


def _status(request):
    return [
        {
            "id": request["id"],
            "ok": True,
            "result": {
                "protocolVersion": 2,
                "features": ["runtime-control", "session-turn"],
            },
        }
    ]


def _run(
    host: FakeProviderHost,
    *args: str,
    stdin: str = "Review this.",
    extra_env: dict[str, str] | None = None,
):
    env = os.environ.copy()
    env["YEP_PROVIDER_HOST_RUNTIME_DIR"] = str(host.runtime)
    env.update(extra_env or {})
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        input=stdin,
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


def _records(proc):
    return [json.loads(line) for line in proc.stdout.splitlines()]


def test_hosted_turn_streams_lifecycle_and_provider_records():
    def turn(request):
        submission = request["submissionId"]
        return [
            {
                "id": request["id"],
                "type": "accepted",
                "submissionId": submission,
                "runtimeId": "runtime-1",
            },
            {
                "id": request["id"],
                "type": "providerEvent",
                "submissionId": submission,
                "sequence": 7,
                "message": {"type": "assistant", "content": "Done"},
            },
            {
                "id": request["id"],
                "type": "providerEvent",
                "submissionId": submission,
                "sequence": 8,
                "message": {"type": "system", "subtype": "compact_boundary"},
            },
            {
                "id": request["id"],
                "type": "terminal",
                "submissionId": submission,
                "outcome": "completed",
                "receipt": {"lastProviderEventSequence": 8},
            },
        ]

    host = FakeProviderHost([_status, turn])
    proc = _run(
        host,
        "claude",
        "provider-session-1",
        extra_env={"PATH": tempfile.mkdtemp(prefix="session-turn-no-native-")},
    )

    _assert(proc.returncode == 0, proc.stderr)
    records = _records(proc)
    _assert(records[0]["type"] == "transport", records)
    _assert(records[0]["transport"] == "provider-host", records)
    _assert(
        [record["type"] for record in records[1:]]
        == ["accepted", "providerEvent", "providerEvent", "terminal"]
    )
    _assert(records[-1]["harness"] == "claude", records[-1])
    _assert(records[-1]["providerSessionId"] == "provider-session-1")
    _assert(records[-1]["receipt"]["lastProviderEventSequence"] == 8)
    _assert(records[-2]["message"]["subtype"] == "compact_boundary")
    _assert(host.requests[1]["message"] == {"text": "Review this."})


def test_hosted_codex_uses_the_same_provider_host_protocol():
    def completed(request):
        _assert(request["target"]["harness"] == "codex", request)
        return [
            {
                "id": request["id"],
                "type": "accepted",
                "submissionId": request["submissionId"],
                "runtimeId": "runtime-codex",
            },
            {
                "id": request["id"],
                "type": "terminal",
                "submissionId": request["submissionId"],
                "outcome": "completed",
                "receipt": {"lastProviderEventSequence": 0},
            },
        ]

    host = FakeProviderHost([_status, completed])
    proc = _run(
        host,
        "codex",
        "codex-session-1",
        extra_env={"PATH": tempfile.mkdtemp(prefix="session-turn-no-native-")},
    )

    _assert(proc.returncode == 0, proc.stderr)
    _assert(_records(proc)[0]["transport"] == "provider-host")
    _assert(
        host.requests[1]["target"]
        == {
            "harness": "codex",
            "providerSessionId": "codex-session-1",
        }
    )
    _assert("launch" not in host.requests[1], host.requests[1])


def test_protocol_v3_atomically_resumes_an_absent_provider_runtime():
    project = Path(tempfile.mkdtemp(prefix="session-turn-project-"))

    def status(request):
        return [
            {
                "id": request["id"],
                "ok": True,
                "result": {
                    "protocolVersion": 3,
                    "features": ["runtime-control", "session-turn"],
                },
            }
        ]

    def completed(request):
        _assert(
            request["launch"]
            == {
                "providerName": "codex",
                "projectPath": str(project),
                "options": {
                    "model": "codex-smoke-model",
                    "effort": "high",
                },
                "reattach": {
                    "model": "codex-smoke-model",
                    "effort": "high",
                },
            },
            request,
        )
        return [
            {
                "id": request["id"],
                "type": "accepted",
                "submissionId": request["submissionId"],
                "runtimeId": "resumed-runtime",
            },
            {
                "id": request["id"],
                "type": "terminal",
                "submissionId": request["submissionId"],
                "outcome": "completed",
                "receipt": {"lastProviderEventSequence": 0},
            },
        ]

    host = FakeProviderHost([status, completed], host_protocol_version=3)
    proc = _run(
        host,
        "codex",
        "codex-session-1",
        "--ya-session-id",
        "ya-session-1",
        "--cwd",
        str(project),
        "--model",
        "codex-smoke-model",
        "--effort",
        "high",
        extra_env={"PATH": tempfile.mkdtemp(prefix="session-turn-no-native-")},
    )

    _assert(proc.returncode == 0, proc.stderr)
    records = _records(proc)
    _assert(records[0]["transport"] == "provider-host", records)
    _assert(records[0]["resumeIfAbsent"] is True, records[0])
    _assert(host.requests[1]["target"]["yaSessionId"] == "ya-session-1")


def test_protocol_v3_prefers_a_recent_exact_recipe_with_launch_fallback():
    features = [
        "runtime-control",
        "session-turn",
        "recent-runtime-recovery",
    ]

    def status(request):
        return [
            {
                "id": request["id"],
                "ok": True,
                "result": {"protocolVersion": 3, "features": features},
            }
        ]

    def completed(request):
        _assert(request["resumeRecentRuntime"] is True, request)
        _assert(request["launch"]["providerName"] == "codex", request)
        return [
            {
                "id": request["id"],
                "type": "accepted",
                "submissionId": request["submissionId"],
                "runtimeId": "recent-runtime",
                "cursor": 1,
            },
            {
                "id": request["id"],
                "type": "terminal",
                "submissionId": request["submissionId"],
                "outcome": "completed",
                "cursor": 2,
            },
        ]

    host = FakeProviderHost(
        [status, completed],
        host_protocol_version=3,
        features=features,
    )
    proc = _run(host, "codex", "codex-session-1")

    _assert(proc.returncode == 0, proc.stderr)
    _assert(_records(proc)[0]["resumeRecentRuntime"] is True, _records(proc))


def test_send_detaches_after_acceptance_and_await_resumes_from_cursor():
    submission_id = "detached-submission"
    features = ["runtime-control", "session-turn", "session-turn-await"]

    def status(request):
        return [
            {
                "id": request["id"],
                "ok": True,
                "result": {"protocolVersion": 3, "features": features},
            }
        ]

    def accepted(request):
        _assert(request["op"] == "sessionTurn", request)
        return [
            {
                "id": request["id"],
                "type": "accepted",
                "submissionId": request["submissionId"],
                "runtimeId": "runtime-1",
                "cursor": 1,
            }
        ]

    def resumed(request):
        _assert(request["op"] == "awaitSessionTurn", request)
        _assert(request["submissionId"] == submission_id, request)
        _assert(request["afterCursor"] == 1, request)
        return [
            {
                "id": request["id"],
                "type": "providerEvent",
                "submissionId": submission_id,
                "cursor": 2,
                "sequence": 1,
                "message": {"type": "assistant", "content": "Done"},
            },
            {
                "id": request["id"],
                "type": "terminal",
                "submissionId": submission_id,
                "cursor": 3,
                "outcome": "completed",
                "receipt": {"lastProviderEventSequence": 1},
            },
        ]

    host = FakeProviderHost(
        [status, accepted, status, resumed],
        host_protocol_version=3,
        features=features,
    )
    sent = _run(
        host,
        "send",
        "codex",
        "codex-session-1",
        "--submission-id",
        submission_id,
    )
    _assert(sent.returncode == 0, sent.stderr)
    _assert(_records(sent)[-1]["type"] == "accepted", _records(sent))
    _assert(_records(sent)[-1]["cursor"] == 1, _records(sent))

    awaited = _run(
        host,
        "await",
        submission_id,
        "--after-cursor",
        "1",
        "--timeout",
        "1",
        stdin="",
    )
    _assert(awaited.returncode == 0, awaited.stderr)
    _assert(
        [record["type"] for record in _records(awaited)]
        == ["transport", "providerEvent", "terminal"],
        _records(awaited),
    )
    _assert(_records(awaited)[-1]["cursor"] == 3, _records(awaited))


def test_blocking_wait_timeout_streams_partial_output_and_prints_resume_hint():
    submission_id = "wait-timeout-submission"
    features = ["runtime-control", "session-turn", "session-turn-await"]

    def status(request):
        return [
            {
                "id": request["id"],
                "ok": True,
                "result": {"protocolVersion": 3, "features": features},
            }
        ]

    def slow_turn(request):
        yield {
            "id": request["id"],
            "type": "accepted",
            "submissionId": submission_id,
            "runtimeId": "runtime-1",
            "cursor": 1,
        }
        yield {
            "id": request["id"],
            "type": "providerEvent",
            "submissionId": submission_id,
            "cursor": 2,
            "sequence": 1,
            "message": {"type": "assistant", "content": "partial"},
        }
        time.sleep(0.2)
        yield {
            "id": request["id"],
            "type": "terminal",
            "submissionId": submission_id,
            "cursor": 3,
            "outcome": "completed",
        }

    host = FakeProviderHost(
        [status, slow_turn],
        host_protocol_version=3,
        features=features,
    )
    proc = _run(
        host,
        "codex",
        "codex-session-1",
        "--submission-id",
        submission_id,
        "--wait-timeout",
        "0.05",
    )

    _assert(proc.returncode == 13, proc.stderr)
    records = _records(proc)
    _assert(
        [record["type"] for record in records]
        == ["transport", "accepted", "providerEvent", "waitExpired"],
        records,
    )
    _assert(records[-1]["cursor"] == 2, records[-1])
    _assert(records[-1]["accepted"] is True, records[-1])
    _assert("session-turn await wait-timeout-submission" in proc.stderr, proc.stderr)
    _assert("--after-cursor 2" in proc.stderr, proc.stderr)


def test_await_timeout_streams_new_records_and_prints_next_cursor():
    submission_id = "await-timeout-submission"
    features = ["runtime-control", "session-turn", "session-turn-await"]

    def status(request):
        return [
            {
                "id": request["id"],
                "ok": True,
                "result": {"protocolVersion": 3, "features": features},
            }
        ]

    def slow_await(request):
        _assert(request["op"] == "awaitSessionTurn", request)
        _assert(request["afterCursor"] == 1, request)
        yield {
            "id": request["id"],
            "type": "providerEvent",
            "submissionId": submission_id,
            "cursor": 2,
            "sequence": 1,
            "message": {"type": "assistant", "content": "new partial output"},
        }
        time.sleep(0.2)
        yield {
            "id": request["id"],
            "type": "terminal",
            "submissionId": submission_id,
            "cursor": 3,
            "outcome": "completed",
        }

    host = FakeProviderHost(
        [status, slow_await],
        host_protocol_version=3,
        features=features,
    )
    proc = _run(
        host,
        "await",
        submission_id,
        "--after-cursor",
        "1",
        "--timeout",
        "0.05",
        stdin="",
    )

    _assert(proc.returncode == 13, proc.stderr)
    records = _records(proc)
    _assert(
        [record["type"] for record in records]
        == ["transport", "providerEvent", "waitExpired"],
        records,
    )
    _assert(records[-1]["cursor"] == 2, records[-1])
    _assert("session-turn await await-timeout-submission" in proc.stderr, proc.stderr)
    _assert("--after-cursor 2" in proc.stderr, proc.stderr)


def test_blocking_wait_timeout_never_detaches_a_native_fallback():
    host = FakeProviderHost([])
    (host.runtime / "host.json").unlink()
    fake_bin = Path(tempfile.mkdtemp(prefix="session-turn-no-native-detach-"))
    marker = fake_bin / "native-was-run"
    executable = fake_bin / "codex"
    executable.write_text(
        '#!/bin/sh\nprintf invoked > "$FAKE_NATIVE_MARKER"\nexit 99\n'
    )
    executable.chmod(0o755)

    proc = _run(
        host,
        "codex",
        "provider-session-1",
        "--wait-timeout",
        "0.05",
        extra_env={
            "PATH": f"{fake_bin}{os.pathsep}{os.environ['PATH']}",
            "FAKE_NATIVE_MARKER": str(marker),
        },
    )

    _assert(proc.returncode == 11, proc.stderr)
    _assert(not marker.exists(), "finite observer waits must stay host-owned")
    _assert(_records(proc)[-1]["accepted"] is False, _records(proc))


def test_host_rejection_before_acceptance_falls_back_to_native_codex():
    def unavailable(request):
        return [
            {
                "id": request["id"],
                "type": "error",
                "submissionId": request["submissionId"],
                "outcome": "unavailable",
                "accepted": False,
                "error": "No incumbent runtime",
            }
        ]

    host = FakeProviderHost([_status, unavailable])
    fake_bin = Path(tempfile.mkdtemp(prefix="session-turn-bin-"))
    capture = fake_bin / "capture.json"
    executable = fake_bin / "codex"
    executable.write_text(
        """#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

body = sys.stdin.read()
Path(os.environ["FAKE_NATIVE_CAPTURE"]).write_text(
    json.dumps(
        {
            "argv": sys.argv[1:],
            "stdin": body,
            "env": {
                name: os.environ.get(name)
                for name in json.loads(os.environ["FAKE_NATIVE_ENV_NAMES"])
            },
        }
    )
)
for record in (
    {"type": "thread.started", "thread_id": "provider-session-1"},
    {"type": "item.completed", "item": {"type": "agent_message", "text": "Done"}},
    {"type": "turn.completed", "usage": {}},
):
    print(json.dumps(record), flush=True)
"""
    )
    executable.chmod(0o755)
    proc = _run(
        host,
        "codex",
        "provider-session-1",
        "--model",
        "codex-smoke-model",
        "--effort",
        "low",
        "--ya-session-id",
        "target-ya-session",
        extra_env={
            "PATH": f"{fake_bin}{os.pathsep}{os.environ['PATH']}",
            "FAKE_NATIVE_CAPTURE": str(capture),
            "FAKE_NATIVE_ENV_NAMES": json.dumps(
                [
                    "AGENTCTL_SESSION_ID",
                    "AGENT_LAUNCHER",
                    "AGENT_LAUNCH_HARNESS",
                    "AGENT_GUARD",
                    "CLAUDE_CODE_SESSION_ID",
                    "CODEX_THREAD_ID",
                    "CLAUDECODE",
                    "PI_CODING_AGENT",
                    "AGENTCTL_LAUNCH_DEPTH",
                    "AGENTCTL_NO_PROC_SESSION_ID",
                    "AGENT_LAUNCH_MODEL",
                    "AGENT_LAUNCH_EFFORT",
                    "YEP_AGENT_HARNESS",
                    "BASH_ENV",
                    "YEP_ORIGINAL_BASH_ENV",
                    "YEP_SESSION_WAKE_URL",
                    "YEP_SESSION_WAKE_TOKEN",
                ]
            ),
            "AGENTCTL_SESSION_ID": "caller-session",
            "AGENT_LAUNCHER": "yepanywhere",
            "AGENT_LAUNCH_HARNESS": "claude",
            "AGENT_GUARD": "1",
            "CLAUDE_CODE_SESSION_ID": "caller-claude-session",
            "CODEX_THREAD_ID": "caller-codex-thread",
            "CLAUDECODE": "1",
            "PI_CODING_AGENT": "1",
            "AGENTCTL_LAUNCH_DEPTH": "2",
            "AGENTCTL_NO_PROC_SESSION_ID": "1",
            "AGENT_LAUNCH_MODEL": "caller-model",
            "AGENT_LAUNCH_EFFORT": "caller-effort",
            "YEP_AGENT_HARNESS": "claude",
            "BASH_ENV": "/caller/bash-env",
            "YEP_ORIGINAL_BASH_ENV": "/caller/original-bash-env",
            "YEP_SESSION_WAKE_URL": "https://caller.invalid/wake",
            "YEP_SESSION_WAKE_TOKEN": "caller-secret",
        },
    )

    _assert(proc.returncode == 0, proc.stderr)
    records = _records(proc)
    _assert(
        [record["transport"] for record in records if record["type"] == "transport"]
        == [
            "provider-host",
            "native-resume",
        ]
    )
    native = next(
        record
        for record in records
        if record["type"] == "transport" and record["transport"] == "native-resume"
    )
    _assert(native["forkRisk"] == "concurrent-native-resume", native)
    _assert("concurrent native resume" in proc.stderr.lower(), proc.stderr)
    _assert(any(record["type"] == "accepted" for record in records), records)
    _assert(records[-1]["type"] == "terminal", records[-1])
    _assert(records[-1]["transport"] == "native-resume", records[-1])
    _assert(records[-1]["receipt"]["watermark"] == "native-record:3")
    invocation = json.loads(capture.read_text())
    _assert(
        invocation["argv"]
        == [
            "exec",
            "resume",
            "--json",
            "--model",
            "codex-smoke-model",
            "-c",
            'model_reasoning_effort="low"',
            "provider-session-1",
            "-",
        ]
    )
    _assert(invocation["stdin"] == "Review this.")
    _assert(invocation["env"]["AGENTCTL_SESSION_ID"] == "target-ya-session")
    _assert(invocation["env"]["AGENT_LAUNCH_HARNESS"] == "codex")
    _assert(invocation["env"]["AGENT_GUARD"] == "1")
    _assert(
        all(
            value is None
            for name, value in invocation["env"].items()
            if name
            not in {
                "AGENTCTL_SESSION_ID",
                "AGENT_LAUNCH_HARNESS",
                "AGENT_GUARD",
            }
        ),
        invocation["env"],
    )
    _assert(host.requests[1]["target"]["yaSessionId"] == "target-ya-session")


def test_disconnect_after_host_acceptance_reports_uncertain_without_fallback():
    submission_id = "submission-accepted"

    def accepted_then_disconnect(request):
        return [
            {
                "id": request["id"],
                "type": "accepted",
                "submissionId": request["submissionId"],
                "runtimeId": "runtime-1",
            }
        ]

    def accepted_status(request):
        _assert(request["op"] == "sessionTurnStatus", request)
        _assert(request["submissionId"] == submission_id, request)
        return [
            {
                "id": request["id"],
                "ok": True,
                "result": {
                    "submissionId": submission_id,
                    "state": "accepted",
                    "accepted": True,
                    "acceptedAt": "2026-08-12T00:00:00.000Z",
                },
            }
        ]

    host = FakeProviderHost([_status, accepted_then_disconnect, accepted_status])
    fake_bin = Path(tempfile.mkdtemp(prefix="session-turn-no-native-"))
    marker = fake_bin / "native-was-run"
    executable = fake_bin / "codex"
    executable.write_text(
        '#!/bin/sh\nprintf invoked > "$FAKE_NATIVE_MARKER"\nexit 99\n'
    )
    executable.chmod(0o755)

    proc = _run(
        host,
        "codex",
        "provider-session-1",
        "--submission-id",
        submission_id,
        extra_env={
            "PATH": f"{fake_bin}{os.pathsep}{os.environ['PATH']}",
            "FAKE_NATIVE_MARKER": str(marker),
        },
    )

    _assert(proc.returncode == 12, proc.stderr)
    _assert(not marker.exists(), "an accepted host turn must never fall back")
    records = _records(proc)
    _assert(records[-1]["type"] == "error", records[-1])
    _assert(records[-1]["accepted"] is True, records[-1])
    _assert(records[-1]["outcome"] == "uncertain-after-acceptance", records[-1])
    _assert(
        records[-1]["receiptLookup"]
        == {"command": ["session-turn", "receipt", submission_id]}
    )


def test_host_error_cannot_revoke_observed_acceptance_and_trigger_fallback():
    def accepted_then_error(request):
        return [
            {
                "id": request["id"],
                "type": "accepted",
                "submissionId": request["submissionId"],
                "runtimeId": "runtime-1",
            },
            {
                "id": request["id"],
                "type": "error",
                "submissionId": request["submissionId"],
                "outcome": "uncertain-after-acceptance",
                "accepted": False,
                "error": "stale acceptance flag",
            },
        ]

    host = FakeProviderHost([_status, accepted_then_error])
    fake_bin = Path(tempfile.mkdtemp(prefix="session-turn-no-native-"))
    marker = fake_bin / "native-was-run"
    executable = fake_bin / "codex"
    executable.write_text(
        '#!/bin/sh\nprintf invoked > "$FAKE_NATIVE_MARKER"\nexit 99\n'
    )
    executable.chmod(0o755)

    proc = _run(
        host,
        "codex",
        "provider-session-1",
        extra_env={
            "PATH": f"{fake_bin}{os.pathsep}{os.environ['PATH']}",
            "FAKE_NATIVE_MARKER": str(marker),
        },
    )

    _assert(proc.returncode == 12, proc.stderr)
    _assert(not marker.exists(), "observed acceptance must block native fallback")
    records = _records(proc)
    _assert(records[-1]["type"] == "error", records[-1])
    _assert(records[-1]["transport"] == "provider-host", records[-1])
    _assert(records[-1]["accepted"] is True, records[-1])
    _assert(
        records[-1]["receiptLookup"]["command"][:2] == ["session-turn", "receipt"],
        records[-1],
    )
    _assert(
        not any(record["transport"] == "native-resume" for record in records),
        records,
    )


def test_absent_host_uses_native_claude_and_maps_provider_failure():
    host = FakeProviderHost([])
    (host.runtime / "host.json").unlink()
    fake_bin = Path(tempfile.mkdtemp(prefix="session-turn-claude-"))
    capture = fake_bin / "capture.json"
    executable = fake_bin / "claude"
    executable.write_text(
        """#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

Path(os.environ["FAKE_NATIVE_CAPTURE"]).write_text(
    json.dumps({"argv": sys.argv[1:], "stdin": sys.stdin.read()})
)
print(json.dumps({"type": "result", "subtype": "error", "session_id": "claude-1"}), flush=True)
raise SystemExit(7)
"""
    )
    executable.chmod(0o755)

    proc = _run(
        host,
        "claude",
        "claude-1",
        "--model",
        "claude-smoke-model",
        "--effort",
        "high",
        extra_env={
            "PATH": f"{fake_bin}{os.pathsep}{os.environ['PATH']}",
            "FAKE_NATIVE_CAPTURE": str(capture),
        },
    )

    _assert(proc.returncode == 10, proc.stderr)
    records = _records(proc)
    _assert(records[0]["transport"] == "native-resume", records)
    _assert(records[-1]["outcome"] == "provider-failed", records[-1])
    _assert(records[-1]["providerExitCode"] == 7, records[-1])
    invocation = json.loads(capture.read_text())
    _assert(
        invocation["argv"]
        == [
            "-p",
            "--resume",
            "claude-1",
            "--input-format",
            "text",
            "--output-format",
            "stream-json",
            "--verbose",
            "--prompt-suggestions",
            "false",
            "--model",
            "claude-smoke-model",
            "--effort",
            "high",
        ]
    )


def test_ctrl_c_requests_host_turn_interrupt_without_killing_incumbent():
    terminal_ready = threading.Event()

    def turn(request):
        yield {
            "id": request["id"],
            "type": "accepted",
            "submissionId": request["submissionId"],
            "runtimeId": "runtime-1",
        }
        terminal_ready.wait(5)
        yield {
            "id": request["id"],
            "type": "terminal",
            "submissionId": request["submissionId"],
            "outcome": "interrupted",
            "receipt": {"lastProviderEventSequence": 0},
        }

    def interrupt(request):
        _assert(request["op"] == "interruptSessionTurn", request)
        terminal_ready.set()
        return [
            {
                "id": request["id"],
                "ok": True,
                "result": {"requested": True, "status": {"state": "accepted"}},
            }
        ]

    def replay(request):
        return [
            {
                "id": request["id"],
                "type": "accepted",
                "submissionId": request["submissionId"],
                "runtimeId": "runtime-1",
            },
            {
                "id": request["id"],
                "type": "terminal",
                "submissionId": request["submissionId"],
                "outcome": "interrupted",
                "receipt": {"lastProviderEventSequence": 0},
            },
        ]

    host = FakeProviderHost([_status, turn, interrupt, _status, replay])
    env = os.environ.copy()
    env["YEP_PROVIDER_HOST_RUNTIME_DIR"] = str(host.runtime)
    process = subprocess.Popen(
        [sys.executable, str(SCRIPT), "claude", "provider-session-1"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
    )
    assert process.stdin is not None
    assert process.stdout is not None
    process.stdin.write("Stop after acceptance.")
    process.stdin.close()
    process.stdin = None
    prefix = [process.stdout.readline(), process.stdout.readline()]
    _assert(json.loads(prefix[1])["type"] == "accepted", prefix)
    process.send_signal(2)
    remaining_stdout, stderr = process.communicate(timeout=10)

    _assert(process.returncode == 10, stderr)
    records = [json.loads(line) for line in prefix + remaining_stdout.splitlines()]
    _assert(any(record["type"] == "interruptRequested" for record in records), records)
    _assert(records[-1]["type"] == "terminal", records[-1])
    _assert(records[-1]["outcome"] == "interrupted", records[-1])
    _assert(any(request["op"] == "interruptSessionTurn" for request in host.requests))


def test_pre_accept_disconnect_checks_receipt_before_native_fallback():
    submission_id = "submission-not-accepted"

    def disconnect(_request):
        return []

    def missing_status(request):
        _assert(request["op"] == "sessionTurnStatus", request)
        return [{"id": request["id"], "ok": True, "result": None}]

    host = FakeProviderHost([_status, disconnect, missing_status])
    fake_bin = Path(tempfile.mkdtemp(prefix="session-turn-reconciled-fallback-"))
    executable = fake_bin / "codex"
    executable.write_text(
        """#!/usr/bin/env python3
import json
import sys

sys.stdin.read()
print(json.dumps({"type": "turn.completed", "usage": {}}), flush=True)
"""
    )
    executable.chmod(0o755)
    proc = _run(
        host,
        "codex",
        "provider-session-1",
        "--submission-id",
        submission_id,
        extra_env={"PATH": f"{fake_bin}{os.pathsep}{os.environ['PATH']}"},
    )

    _assert(proc.returncode == 0, proc.stderr)
    _assert(
        [request["op"] for request in host.requests]
        == [
            "status",
            "sessionTurn",
            "sessionTurnStatus",
        ]
    )
    transports = [
        record["transport"]
        for record in _records(proc)
        if record["type"] == "transport"
    ]
    _assert(transports == ["provider-host", "native-resume"], transports)


def test_terminal_receipt_lookup_recovers_a_completed_host_turn():
    submission_id = "submission-completed"

    def accepted_then_disconnect(request):
        return [
            {
                "id": request["id"],
                "type": "accepted",
                "submissionId": request["submissionId"],
                "runtimeId": "runtime-1",
            }
        ]

    def terminal_status(request):
        return [
            {
                "id": request["id"],
                "ok": True,
                "result": {
                    "submissionId": submission_id,
                    "state": "terminal",
                    "accepted": True,
                    "outcome": "completed",
                    "receipt": {"lastProviderEventSequence": 12},
                },
            }
        ]

    host = FakeProviderHost([_status, accepted_then_disconnect, terminal_status])
    proc = _run(
        host,
        "codex",
        "provider-session-1",
        "--submission-id",
        submission_id,
    )

    _assert(proc.returncode == 0, proc.stderr)
    terminal = _records(proc)[-1]
    _assert(terminal["type"] == "terminal", terminal)
    _assert(terminal["reconciledFromStatus"] is True, terminal)
    _assert(terminal["receipt"]["lastProviderEventSequence"] == 12, terminal)


def test_receipt_command_exposes_persisted_terminal_status():
    submission_id = "submission-receipt"

    def terminal_status(request):
        _assert(request["op"] == "sessionTurnStatus", request)
        return [
            {
                "id": request["id"],
                "ok": True,
                "result": {
                    "submissionId": submission_id,
                    "state": "terminal",
                    "accepted": True,
                    "outcome": "completed",
                    "receipt": {"lastProviderEventSequence": 21},
                },
            }
        ]

    host = FakeProviderHost([_status, terminal_status])
    proc = _run(host, "receipt", submission_id, stdin="")

    _assert(proc.returncode == 0, proc.stderr)
    record = _records(proc)[0]
    _assert(record["type"] == "receiptStatus", record)
    _assert(record["submissionId"] == submission_id, record)
    _assert(record["outcome"] == "completed", record)
    _assert(record["receipt"]["lastProviderEventSequence"] == 21, record)


def test_missing_native_executable_is_transport_failure_before_acceptance():
    host = FakeProviderHost([])
    (host.runtime / "host.json").unlink()
    empty_path = tempfile.mkdtemp(prefix="session-turn-empty-path-")
    proc = _run(
        host,
        "codex",
        "provider-session-1",
        extra_env={"PATH": empty_path},
    )

    _assert(proc.returncode == 11, proc.stderr)
    error = _records(proc)[-1]
    _assert(error["type"] == "error", error)
    _assert(error["accepted"] is False, error)
    _assert(error["outcome"] == "transport-failed-before-acceptance", error)


def test_native_resume_rejection_before_provider_output_is_not_accepted():
    host = FakeProviderHost([])
    (host.runtime / "host.json").unlink()
    fake_bin = Path(tempfile.mkdtemp(prefix="session-turn-native-reject-"))
    executable = fake_bin / "codex"
    executable.write_text(
        """#!/usr/bin/env python3
import sys

sys.stdin.read()
print("thread/resume failed: active writer", file=sys.stderr)
raise SystemExit(7)
"""
    )
    executable.chmod(0o755)
    proc = _run(
        host,
        "codex",
        "provider-session-1",
        extra_env={"PATH": f"{fake_bin}{os.pathsep}{os.environ['PATH']}"},
    )

    _assert(proc.returncode == 11, proc.stderr)
    records = _records(proc)
    _assert([record["type"] for record in records] == ["transport", "error"])
    _assert(records[-1]["accepted"] is False, records[-1])
    _assert(records[-1]["providerExitCode"] == 7, records[-1])
    _assert(
        records[-1]["outcome"] == "transport-failed-before-acceptance",
        records[-1],
    )


def test_native_provider_output_cannot_accept_a_broken_stdin_delivery():
    host = FakeProviderHost([])
    (host.runtime / "host.json").unlink()
    fake_bin = Path(tempfile.mkdtemp(prefix="session-turn-native-broken-stdin-"))
    executable = fake_bin / "codex"
    executable.write_text(
        """#!/usr/bin/env python3
import json
import os
import time

os.close(0)
print(json.dumps({"type": "thread.started"}), flush=True)
time.sleep(0.1)
raise SystemExit(7)
"""
    )
    executable.chmod(0o755)
    proc = _run(
        host,
        "codex",
        "provider-session-1",
        stdin="x" * (512 * 1024),
        extra_env={"PATH": f"{fake_bin}{os.pathsep}{os.environ['PATH']}"},
    )

    _assert(proc.returncode == 11, proc.stderr)
    records = _records(proc)
    _assert(
        [record["type"] for record in records]
        == ["transport", "providerEvent", "error"],
        records,
    )
    _assert(records[-1]["accepted"] is False, records[-1])
    _assert(
        records[-1]["outcome"] == "transport-failed-before-acceptance",
        records[-1],
    )


def test_native_non_json_warning_is_not_an_acceptance_receipt():
    host = FakeProviderHost([])
    (host.runtime / "host.json").unlink()
    fake_bin = Path(tempfile.mkdtemp(prefix="session-turn-native-warning-"))
    executable = fake_bin / "codex"
    executable.write_text(
        """#!/usr/bin/env python3
import json
import sys

sys.stdin.read()
print("warning: loading configuration", flush=True)
print(json.dumps({"type": "resume.rejected"}), flush=True)
raise SystemExit(7)
"""
    )
    executable.chmod(0o755)
    proc = _run(
        host,
        "codex",
        "provider-session-1",
        extra_env={"PATH": f"{fake_bin}{os.pathsep}{os.environ['PATH']}"},
    )

    _assert(proc.returncode == 11, proc.stderr)
    records = _records(proc)
    _assert(
        [record["type"] for record in records]
        == ["transport", "providerEvent", "providerEvent", "error"],
        records,
    )
    _assert(records[1]["providerRecord"]["raw"].startswith("warning:"), records)
    _assert(records[-1]["accepted"] is False, records[-1])


def test_native_ctrl_c_interrupts_only_the_helper_process_group():
    host = FakeProviderHost([])
    (host.runtime / "host.json").unlink()
    fake_bin = Path(tempfile.mkdtemp(prefix="session-turn-native-interrupt-"))
    executable = fake_bin / "claude"
    executable.write_text(
        """#!/usr/bin/env python3
import json
import signal
import sys
import time

def interrupted(_signum, _frame):
    print(json.dumps({"type": "result", "subtype": "interrupted"}), flush=True)
    raise SystemExit(130)

signal.signal(signal.SIGINT, interrupted)
sys.stdin.read()
print(json.dumps({"type": "system", "subtype": "started"}), flush=True)
while True:
    time.sleep(0.1)
"""
    )
    executable.chmod(0o755)
    env = os.environ.copy()
    env["YEP_PROVIDER_HOST_RUNTIME_DIR"] = str(host.runtime)
    env["PATH"] = f"{fake_bin}{os.pathsep}{os.environ['PATH']}"
    process = subprocess.Popen(
        [sys.executable, str(SCRIPT), "claude", "claude-1"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
    )
    assert process.stdin is not None
    assert process.stdout is not None
    process.stdin.write("Interrupt this native turn.")
    process.stdin.close()
    process.stdin = None
    prefix = [
        process.stdout.readline(),
        process.stdout.readline(),
        process.stdout.readline(),
    ]
    _assert(json.loads(prefix[-1])["type"] == "providerEvent", prefix)
    process.send_signal(2)
    remaining_stdout, stderr = process.communicate(timeout=10)

    _assert(process.returncode == 10, stderr)
    records = [json.loads(line) for line in prefix + remaining_stdout.splitlines()]
    _assert(any(record["type"] == "interruptRequested" for record in records), records)
    _assert(records[-1]["type"] == "terminal", records[-1])
    _assert(records[-1]["providerExitCode"] == 130, records[-1])


def test_host_uncertain_terminal_uses_uncertain_delivery_exit_code():
    def uncertain(request):
        return [
            {
                "id": request["id"],
                "type": "accepted",
                "submissionId": request["submissionId"],
                "runtimeId": "runtime-1",
            },
            {
                "id": request["id"],
                "type": "terminal",
                "submissionId": request["submissionId"],
                "outcome": "uncertain-after-acceptance",
                "receipt": {"lastProviderEventSequence": 4},
            },
        ]

    host = FakeProviderHost([_status, uncertain])
    proc = _run(host, "codex", "provider-session-1")

    _assert(proc.returncode == 12, proc.stderr)
    _assert(_records(proc)[-1]["outcome"] == "uncertain-after-acceptance")


def test_every_grammar_accepts_the_explicit_json_alias():
    import importlib.machinery
    import importlib.util

    loader = importlib.machinery.SourceFileLoader("session_turn", str(SCRIPT))
    spec = importlib.util.spec_from_loader("session_turn", loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)

    for parser, argv in (
        (module.turn_parser(), ["--json", "codex", "deadbeef"]),
        (module.send_parser(), ["--json", "codex", "deadbeef"]),
        (module.await_parser(), ["--json", "submission-1"]),
        (module.receipt_parser(), ["--json", "submission-1"]),
    ):
        args = parser.parse_args(argv)
        _assert(args.json is True, (parser.prog, args))


def _collect_tests():
    return [
        (name, fn)
        for name, fn in sorted(globals().items())
        if name.startswith("test_") and callable(fn)
    ]


def main() -> int:
    passed = failed = 0
    failures = []
    for name, fn in _collect_tests():
        try:
            fn()
            passed += 1
            print(".", end="", flush=True)
        except Exception:
            failed += 1
            failures.append((name, traceback.format_exc()))
            print("F", end="", flush=True)
    print("\n")
    for name, trace in failures:
        print(f"--- {name} ---\n{trace}")
    print(f"{passed} passed, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
