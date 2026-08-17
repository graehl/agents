"""Best-effort YA session wake notification for detached agentctl runs."""

from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.request
from collections.abc import Mapping
from pathlib import Path

import agentctl

WAKE_ENV_PAIRS = (
    ("AGENT_SESSION_WAKE_URL", "AGENT_SESSION_WAKE_TOKEN"),
    ("YEP_SESSION_WAKE_URL", "YEP_SESSION_WAKE_TOKEN"),
)
WAKE_TIMEOUT_SECONDS = 3.0
WAKE_ATTEMPTS = 2
WAKE_TEXT_MAX_CHARS = 2_000
FAILURE_LOG_TAIL_BYTES = 8_192
FAILURE_LOG_LINE_MAX_CHARS = 320


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


WAKE_OPENER = urllib.request.build_opener(_NoRedirect)


def register_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--no-wake",
        action="store_true",
        help="Do not notify the launching YA session when this run finishes.",
    )


def _wake_credentials(env: Mapping[str, str]) -> tuple[str, str]:
    for url_name, token_name in WAKE_ENV_PAIRS:
        url = env.get(url_name, "").strip()
        token = env.get(token_name, "").strip()
        if url and token:
            return url, token
    return "", ""


def on_start(args, state, env) -> None:
    state["wake_opted_out"] = bool(getattr(args, "no_wake", False))
    try:
        launch_depth = int(env.get(agentctl.LAUNCH_DEPTH_ENV, "0") or "0")
    except ValueError:
        launch_depth = 0
    url, token = _wake_credentials(env)
    state["wake_armed"] = bool(
        not state["wake_opted_out"] and launch_depth == 1 and url and token
    )


def _one_line(value: object, max_chars: int) -> str:
    return " ".join(str(value).replace("\0", "").split())[:max_chars]


def _last_log_line(state: dict) -> str:
    path_text = str(state.get("log_path") or "").strip()
    if not path_text:
        return ""
    try:
        with Path(path_text).open("rb") as log:
            log.seek(0, 2)
            size = log.tell()
            log.seek(max(0, size - FAILURE_LOG_TAIL_BYTES))
            lines = log.read().decode("utf-8", errors="replace").splitlines()
    except OSError:
        return ""
    for line in reversed(lines):
        normalized = _one_line(line, FAILURE_LOG_LINE_MAX_CHARS)
        if normalized:
            return normalized
    return ""


def _wake_text(state: dict) -> str:
    fields = [
        "[agentctl-wake]",
        f"job {_one_line(state.get('job', '?'), 160)} finished",
        f"returncode={agentctl.status_returncode_text(state) or 'unknown'}",
        f"elapsed={agentctl.format_duration(agentctl.elapsed_seconds(state))}",
        f"log={_one_line(state.get('log_path', ''), 600)}",
    ]
    output_path = _one_line(state.get("output_path", ""), 600)
    if output_path:
        fields.append(f"out={output_path}")
    if agentctl.status_returncode_exit_code(state) != 0:
        last_line = _last_log_line(state)
        if last_line:
            fields.append(f"last={last_line}")
    return " ".join(fields)[:WAKE_TEXT_MAX_CHARS]


def _failure_summary(error: Exception) -> str:
    if isinstance(error, urllib.error.HTTPError):
        return f"HTTP {error.code}"
    if isinstance(error, urllib.error.URLError):
        reason = error.reason
        if isinstance(reason, OSError) and reason.errno is not None:
            return f"network errno={reason.errno}"
        return f"network {type(reason).__name__}"
    if isinstance(error, OSError) and error.errno is not None:
        return f"network errno={error.errno}"
    return type(error).__name__


def on_finish(state) -> None:
    if not state.get("wake_armed"):
        return
    url, token = _wake_credentials(os.environ)
    if not url or not token:
        return
    body = json.dumps(
        {
            "text": _wake_text(state),
            "source": "agentctl",
            "jobId": str(state.get("run_id") or ""),
        },
        separators=(",", ":"),
    ).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    last_error: Exception | None = None
    for _attempt in range(WAKE_ATTEMPTS):
        try:
            with WAKE_OPENER.open(request, timeout=WAKE_TIMEOUT_SECONDS):
                return
        except Exception as error:  # noqa: BLE001 - best-effort plugin boundary
            last_error = error
    print(
        "agentctl: session wake failed after retry: "
        f"{_failure_summary(last_error or RuntimeError())}",
        flush=True,
    )


def on_restart(state, args) -> None:
    args.no_wake = bool(state.get("wake_opted_out", False))
