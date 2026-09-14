"""ACLI entry point for subscription document annotation."""

from __future__ import annotations

import asyncio
import fcntl
import hashlib
import importlib
import json
import os
import shutil
import subprocess
import sys
from builtins import ExceptionGroup
from pathlib import Path
from typing import Any

import acli
from acli.args import duration_seconds

from .codex import CodexAppServer
from .isolation import CONFIG, prepare_profile
from .journal import Journal
from .messages import FixedMessage
from .runner import AnnotationConfig, DocumentAnnotator, Segment, Validator


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_segments(data: bytes) -> list[Segment]:
    rows = []
    for number, line in enumerate(data.decode("utf-8").splitlines(), 1):
        row = json.loads(line)
        if not isinstance(row, dict) or set(row) - {
            "document_id",
            "segment_id",
            "prompt",
            "metadata",
        }:
            raise ValueError(
                f"input line {number}: expected document_id, segment_id, prompt and optional metadata"
            )
        if not isinstance(row.get("metadata", {}), dict):
            raise TypeError(f"input line {number}: metadata must be an object")
        rows.append(Segment(**row))
    return rows


def load_validator(spec: str | None) -> tuple[Validator | None, str | None]:
    if spec is None:
        return None, None
    module_name, sep, name = spec.partition(":")
    if not sep or not module_name or not name:
        raise ValueError("--validator requires module:callable")
    sys.path.insert(0, str(Path.cwd()))
    module = importlib.import_module(module_name)
    callback = getattr(module, name)
    if not callable(callback) or not module.__file__:
        raise ValueError(
            "--validator must resolve to a callable in a file-backed module"
        )
    return callback, spec + "@sha256:" + sha256(Path(module.__file__).read_bytes())


def read_fixed_messages(data: bytes | None) -> tuple[FixedMessage, ...]:
    if data is None:
        return ()
    values = json.loads(data)
    if not isinstance(values, list) or any(
        not isinstance(value, dict) or set(value) != {"role", "content"}
        for value in values
    ):
        raise ValueError("--fixed-messages requires an array of role/content objects")
    return tuple(FixedMessage(**value) for value in values)


def parser() -> Any:
    result = acli.argument_parser(
        description="Annotate ordered document segments through Codex subscription sessions (seconds to hours; final summary on stdout, durable attempts in --out/events.jsonl).",
        capabilities=("complete",),
    )
    acli.add_standard_args(result)
    result.add_argument(
        "--input",
        type=Path,
        required=True,
        help="JSONL: document_id, segment_id, prompt, optional metadata; order within each document is preserved.",
    )
    result.add_argument(
        "--prompt",
        type=Path,
        required=True,
        help="Complete fixed instruction prefix, passed byte-for-byte as baseInstructions.",
    )
    result.add_argument(
        "--fixed-messages",
        type=Path,
        help="Optional JSON array of authored user/assistant role/content messages, injected once into each fresh thread. Annotation-quality effect is unqualified.",
    )
    result.add_argument(
        "--out",
        type=Path,
        required=True,
        help="New private campaign directory; contains credentials under .codex. --resume reuses it without changing inputs.",
    )
    result.add_argument(
        "--auth-home",
        type=Path,
        required=True,
        help="Existing subscription login home; only auth.json is copied. API-key fallback is never automatic.",
    )
    result.add_argument("--model", required=True)
    result.add_argument("--effort", required=True)
    result.add_argument(
        "--max-session-segments",
        type=int,
        required=True,
        help="Qualified segment count before starting a fresh session; 1 disables document-history reuse.",
    )
    result.add_argument(
        "--max-input-tokens",
        type=int,
        required=True,
        help="Reject responses beyond this qualified context size and retry fresh within the retry budget.",
    )
    result.add_argument(
        "--workers", type=int, default=4, help="Maximum concurrent documents."
    )
    result.add_argument(
        "--retries",
        type=int,
        default=1,
        help="Additional fresh-session attempts after a validation/context rejection. Transport errors stop, without automatic replay.",
    )
    result.add_argument(
        "--timeout",
        type=duration_seconds,
        default=300,
        help="Per-turn deadline in seconds or a duration such as 5m.",
    )
    result.add_argument(
        "--validator",
        help="Trusted Python module:callable(text, segment); return None or a rejection reason; sync and async supported.",
    )
    result.add_argument(
        "--codex-command",
        default="codex",
        help="Codex executable; starts one owned app-server and closes it on every exit.",
    )
    result.add_argument(
        "--resume",
        action="store_true",
        help="Verify immutable campaign inputs and resume completed document prefixes. Unfinished attempts require explicit reconciliation.",
    )
    return result


async def execute(
    args: Any,
    env: dict[str, str],
    config: AnnotationConfig,
    segments: list[Segment],
    validate: Validator | None,
    journal: Journal,
    completed: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    async with CodexAppServer(
        [args.codex_command, "app-server", "--strict-config", "--stdio"],
        env=env,
        request_timeout=min(args.timeout, 60),
    ) as server:
        return await DocumentAnnotator(server, config).annotate(
            segments, record=journal.write, validate=validate, completed=completed
        )


def run(args: Any) -> dict[str, Any]:
    output = args.out.expanduser().resolve()
    input_bytes = args.input.read_bytes()
    segments = read_segments(input_bytes)
    validate, validator_id = load_validator(args.validator)
    prefix = args.prompt.read_bytes().decode("utf-8")
    messages_bytes = args.fixed_messages.read_bytes() if args.fixed_messages else None
    config = AnnotationConfig(
        prefix,
        args.model,
        args.effort,
        str(output / "work"),
        args.max_session_segments,
        args.max_input_tokens,
        args.workers,
        args.retries,
        args.timeout,
        validator_id,
        fixed_messages=read_fixed_messages(messages_bytes),
    )
    executable = shutil.which(args.codex_command)
    if executable is None:
        raise ValueError(f"Codex executable not found: {args.codex_command}")
    args.codex_command = executable
    version = subprocess.run(
        [executable, "--version"],
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    ).stdout.strip()
    implementation = {
        p.name: sha256(p.read_bytes()) for p in Path(__file__).parent.glob("*.py")
    }
    manifest = {
        "schema": "document-annotation/v1",
        "backend": "codex-subscription",
        "config": config.record(),
        "fixed_messages_sha256": sha256(messages_bytes)
        if messages_bytes is not None
        else None,
        "input_sha256": sha256(input_bytes),
        "prefix_sha256": sha256(prefix.encode()),
        "implementation": implementation,
        "codex_command": executable,
        "codex_version": version,
        "isolation_sha256": sha256(CONFIG.encode()),
    }
    if args.resume:
        if json.loads((output / "manifest.json").read_text()) != manifest:
            raise ValueError(
                "campaign input, prefix, settings, validator, implementation or Codex version changed"
            )
    else:
        output.mkdir(mode=0o700, parents=True, exist_ok=False)
    with (output / ".lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        journal = Journal(output / "events.jsonl")
        completed = journal.completed() if args.resume else []
        env = prepare_profile(
            args.auth_home.expanduser().resolve(), output, resume=args.resume
        )
        if not args.resume:
            (output / "manifest.json").write_text(
                json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
            )
            (output / "prefix.txt").write_bytes(prefix.encode())
            (output / "input.jsonl").write_bytes(input_bytes)
            if messages_bytes is not None:
                (output / "fixed-messages.json").write_bytes(messages_bytes)
        results = asyncio.run(
            execute(args, env, config, segments, validate, journal, completed)
        )
        result_path = output / "results.jsonl"
        temporary = output / "results.jsonl.new"
        temporary.write_text(
            "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in results)
        )
        os.replace(temporary, result_path)
        usage: dict[str, int] = {}
        for row in results:
            for key, count in row["usage"].items():
                usage[key] = usage.get(key, 0) + count
        return {
            "kind": "annotation_complete",
            "segments": len(results),
            "validated": sum(row["status"] == "validated" for row in results),
            "unvalidated": sum(row["status"] == "unvalidated" for row in results),
            "rejected": sum(row["status"] == "rejected" for row in results),
            "usage": usage,
            "results": str(result_path),
            "journal": str(journal.path),
        }


def main() -> int:
    p = parser()
    acli.maybe_complete(p)
    args = p.parse_args()
    try:
        fmt = acli.resolve_format(args)
        result = run(args)
        acli.emit(result, fmt)
        return 1 if result["rejected"] else 0
    except (
        OSError,
        ValueError,
        TypeError,
        RuntimeError,
        ImportError,
        AttributeError,
        subprocess.SubprocessError,
        ExceptionGroup,
    ) as error:
        message = (
            "; ".join(f"{type(child).__name__}: {child}" for child in error.exceptions)
            if isinstance(error, ExceptionGroup)
            else str(error)
        )
        acli.die(
            message,
            acli.ExitCode.SOFTWARE,
            detail={"exception": type(error).__name__},
        )
    return 1
