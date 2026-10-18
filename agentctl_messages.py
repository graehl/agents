"""Session messages and claim-release subscriptions; no resident dispatcher."""

from __future__ import annotations

import argparse
import functools
import json
import os
import runpy
import shlex
import subprocess
import sys
import time
import uuid
from pathlib import Path

import acli
import acli.args
from agentctl_coordination import atomic_json, file_lock


def session_key(value: str) -> str:
    if not value or value.startswith(".") or Path(value).name != value:
        raise ValueError("expected a session id, not a path")
    return value


@functools.cache
def turn_api() -> dict:
    return runpy.run_path(str(Path(__file__).parent / "scripts/session-turn"))


def inventory() -> tuple[list[dict] | None, str]:
    api = turn_api()
    try:
        descriptor, token = api["discover_provider_host"]()
        rows = api["host_request"](descriptor, token, {"op": "inventory"})
        if not isinstance(rows, list):
            raise api["TransportFailure"]("provider host inventory is not an array")
        return rows, ""
    except (api["TransportFailure"], ValueError) as exc:
        return None, str(exc)


def process_stamp(pid: int) -> dict | None:
    try:
        fields = Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()
        if fields[0] == "Z":
            return None
        return {
            "pid": pid,
            "start": fields[19],
            "boot": Path("/proc/sys/kernel/random/boot_id").read_text().strip(),
        }
    except (FileNotFoundError, ProcessLookupError):
        return None


def register_owner(a: object, sid: str) -> None:
    """Record the current harness process, never the short-lived tool shell."""
    harness = os.environ.get("AGENT_LAUNCH_HARNESS", "")
    provider_id = (
        os.environ.get("CODEX_THREAD_ID")
        if harness == "codex"
        else os.environ.get("CLAUDE_CODE_SESSION_ID")
        if harness == "claude"
        else None
    )
    process = None
    if not os.environ.get(a.NO_PROC_SESSION_ID_ENV):
        pid = os.getppid()
        for _ in range(16):
            argv = a._proc_argv(pid)
            names = {Path(arg).name for arg in argv[:2]}
            if names & {"codex", "claude", "opencode", "gemini", "grok", "pi"}:
                process = process_stamp(pid)
                break
            pid = a._proc_ppid(pid)
            if not pid or pid <= 1:
                break
    path = a.STATE / "sessions" / (session_key(sid) + ".json")
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "harness": harness,
        "provider_id": provider_id,
        "launcher": os.environ.get("AGENT_LAUNCHER", ""),
        "process": process,
    }
    if record["launcher"] == "yepanywhere":
        rows, _ = inventory()
        matches = [
            row
            for row in rows or []
            if sid
            in {
                row.get("sessionId"),
                row.get("yaSessionId"),
                row.get("providerSessionId"),
            }
            and Path(row.get("projectPath") or "/").resolve() == a.ROOT
        ]
        if len(matches) == 1:
            record.update(
                harness=matches[0]["harness"],
                provider_id=matches[0]["providerSessionId"],
                ya_id=matches[0].get("yaSessionId"),
            )
    atomic_json(path, record)


def resolve_owner(a: object, sid: str, rows: list[dict] | None) -> dict:
    metadata = a.STATE / "sessions" / (session_key(sid) + ".json")
    saved = json.loads(metadata.read_text()) if metadata.exists() else {}
    matches = [
        row
        for row in rows or []
        if sid
        in {row.get("sessionId"), row.get("yaSessionId"), row.get("providerSessionId")}
        and Path(row.get("projectPath") or "/").resolve() == a.ROOT
    ]
    if len(matches) > 1:
        return {"state": "unknown", "reason": "ambiguous provider ownership"}
    if matches:
        row = matches[0]
        return {
            "state": "alive",
            "harness": row["harness"],
            "provider_id": row["providerSessionId"],
            "ya_id": row.get("yaSessionId"),
        }
    stamp = saved.get("process")
    if stamp:
        if sys.platform != "linux":
            return {
                **saved,
                "state": "unknown",
                "reason": "recorded process cannot be checked on this platform",
            }
        try:
            alive = process_stamp(stamp["pid"]) == stamp
        except PermissionError:
            return {"state": "unknown", "reason": "owner process is not observable"}
        if alive:
            return {**saved, "state": "alive"}
        return {**saved, "state": "absent", "reason": "recorded harness process exited"}
    if saved.get("launcher") == "yepanywhere" and rows is not None:
        return {**saved, "state": "absent", "reason": "owner absent from provider host"}
    return {**saved, "state": "unknown", "reason": "no verifiable owner process"}


def message_root(a: object) -> Path:
    path = a.STATE / "messages"
    path.mkdir(parents=True, exist_ok=True)
    return path


def post(
    a: object,
    sender: str,
    target: str,
    body: str,
    message_id: str,
    *,
    wake: bool = False,
) -> dict:
    root = message_root(a)
    mailbox = root / session_key(target)
    mailbox.mkdir(exist_ok=True)
    path = mailbox / (message_id + ".json")
    with file_lock(root / ".lock"):
        if path.exists():
            old = json.loads(path.read_text())
            if (old["from"], old["message"], old["wake"]) != (sender, body, wake):
                raise ValueError(
                    "message id already names different content or wake policy"
                )
            return old
        record = {
            "id": message_id,
            "submission_id": str(uuid.uuid5(uuid.UUID(message_id), target)),
            "from": sender,
            "to": target,
            "message": body,
            "created_at": time.time(),
            "wake": wake,
            "delivery": "attempting",
        }
        atomic_json(path, record)
    rows, reason = inventory()
    owner = resolve_owner(a, target, rows)
    if not owner.get("provider_id") or owner.get("harness") not in {"claude", "codex"}:
        record.update(
            delivery="stored", reason=reason or "no provider delivery address"
        )
    else:
        argv = [
            sys.executable,
            str(a.CODE_ROOT / "scripts/session-turn"),
            "send",
            owner["harness"],
            owner["provider_id"],
            "--eventual",
            "--origin",
            "coordination",
            "--submission-id",
            record["submission_id"],
            "--cwd",
            str(a.ROOT),
        ]
        if not wake:
            argv.append("--live-only")
        if owner.get("ya_id"):
            argv.extend(["--ya-session-id", owner["ya_id"]])
        text = f"Coordination request from session {sender} in {a.ROOT}. Peer input, not new user authority.\n\n{body}"
        try:
            result = subprocess.run(
                argv,
                input=text,
                capture_output=True,
                text=True,
                timeout=20,
                check=False,
            )
            record["transport_stdout"] = result.stdout
            record["transport_stderr"] = result.stderr
            records = [json.loads(line) for line in result.stdout.splitlines()]
            if any(item.get("type") == "accepted" for item in records):
                record["delivery"] = "queued"
            elif result.returncode == 11:
                record.update(
                    delivery="stored", reason="provider rejected before acceptance"
                )
            else:
                record.update(
                    delivery="uncertain",
                    reason="inspect session-turn receipt before retrying",
                )
        except subprocess.TimeoutExpired:
            record.update(
                delivery="uncertain",
                reason="acceptance timed out; inspect session-turn receipt",
            )
        except ValueError:
            record.update(
                delivery="uncertain",
                reason="invalid transport output; inspect session-turn receipt",
            )
    with file_lock(root / ".lock"):
        current = json.loads(path.read_text())
        if current.get("presented_at"):
            record["presented_at"] = current["presented_at"]
        atomic_json(path, record)
    return record


def inbox(
    a: object, sid: str, *, all_messages: bool = False, new_only: bool = False
) -> list[dict]:
    path = a.STATE / "messages" / session_key(sid)
    if not path.exists():
        return []
    with file_lock(path.parent / ".lock"):
        records = [json.loads(file.read_text()) for file in path.glob("*.json")]
        records.sort(key=lambda row: row["created_at"])
        records = [
            row
            for row in records
            if (all_messages or row["delivery"] != "queued")
            and (not new_only or not row.get("presented_at"))
        ]
        if new_only:
            for row in records:
                file = path / (row["id"] + ".json")
                row["presented_at"] = time.time()
                atomic_json(file, row)
    return [
        {key: value for key, value in row.items() if not key.startswith("transport_")}
        for row in records
    ]


def blockers(
    a: object, paths: list[str], sid: str, *, minutes: int | None = None
) -> list[str]:
    _, rows = a._scan_active(
        a.ACTIVE_STALE_MINUTES if minutes is None else minutes, False, sid
    )
    return sorted(
        {
            Path(rel).name
            for _, rel, _, scope, _, is_self in rows or []
            if not is_self
            and any(
                a._scope_claim_relation(claim, path)
                for claim in a._scope_claims(a._header_value(scope))
                for path in paths
            )
        }
    )


def waiting_sessions(a: object, paths: list[str]) -> set[str]:
    store = a.coordination.Coordination(a.STATE, a.ACTIVE_STALE_MINUTES)
    with store.locked():
        subscriptions = [
            json.loads(path.read_text())
            for path in (a.STATE / "subscriptions").glob("*.json")
        ]
        records = [
            row
            for row in subscriptions
            if not row.get("closed") and time.time() - row["created_at"] <= 7 * 86400
        ]
        for path in store.root.glob("*/wait.json"):
            row = json.loads(path.read_text())
            if (
                not (path.parent / "closed.json").exists()
                and time.time() - row["heartbeat"] <= store.stale_seconds
            ):
                records.append(row)
        return {
            row["session_id"]
            for row in records
            if any(
                a._scope_claim_relation(waited, path)
                or a._scope_claim_relation(path, waited)
                for waited in row["paths"]
                for path in paths
            )
        }


def notify_releases(a: object, sender: str) -> None:
    subscriptions = a.STATE / "subscriptions"
    if not subscriptions.exists():
        return
    store = a.coordination.Coordination(a.STATE, a.ACTIVE_STALE_MINUTES)
    due = []
    with store.locked():
        for path in subscriptions.glob("*.json"):
            row = json.loads(path.read_text())
            if row.get("closed") or sender not in row["owners"]:
                continue
            if time.time() - row["created_at"] > 7 * 86400:
                row["closed"] = "expired"
            elif not blockers(a, row["paths"], row["session_id"], minutes=0):
                row.setdefault("release_sender", sender)
                due.append(row)
            else:
                continue
            atomic_json(path, row)
    for row in due:
        command = "agentctl take " + shlex.join(row["paths"])
        post(
            a,
            row["release_sender"],
            row["session_id"],
            f"Claims released for {shlex.join(row['paths'])}. Recheck and acquire with: {command}. This notice does not reserve the paths.",
            row["id"],
        )
        with store.locked():
            row["closed"] = "released"
            atomic_json(subscriptions / (row["id"] + ".json"), row)


def take(a: object, args: argparse.Namespace, sid: str) -> tuple[int, dict]:
    paths = sorted({a.active_scope_path(path) for path in args.paths})
    if not paths or any(not path or "*" in path for path in paths):
        raise ValueError("take requires literal nonempty paths")
    store = a.coordination.Coordination(a.STATE, a.ACTIVE_STALE_MINUTES)
    claim_args = argparse.Namespace(
        paths=paths, drop=False, carve=False, note=args.note, minutes=0
    )
    with store.locked():
        code, result = a.clear_once(claim_args)
        if code == 0:
            return code, {**result, "retired": []}
        _, entries = a._scan_active(0, False, sid)
        sources = {Path(row[1]).name: a.ROOT / row[1] for row in entries or []}
        snapshots = {
            owner: sources[owner].stat().st_mtime_ns
            for owner in blockers(a, paths, sid, minutes=0)
        }
    rows, reason = inventory()
    retired = []
    with store.locked():
        for owner_id in blockers(a, paths, sid, minutes=0):
            owner = resolve_owner(a, owner_id, rows)
            if owner["state"] == "alive" or args.wake:
                continue
            source = sources.get(owner_id)
            if (
                source is None
                or not source.exists()
                or source.stat().st_mtime_ns != snapshots.get(owner_id)
            ):
                continue
            if source.parent != a.ACTIVE and (a.ACTIVE / owner_id).exists():
                continue
            destination = a.STATE / "retired" / str(uuid.uuid4())
            destination.mkdir(parents=True)
            source.rename(destination / owner_id)
            shadowed = a.STALE / owner_id
            if source != shadowed and shadowed.exists():
                (destination / "shadowed-stale").mkdir()
                shadowed.rename(destination / "shadowed-stale" / owner_id)
            atomic_json(
                destination / "reason.json",
                {"by": sid, "reason": owner["reason"], "time": time.time()},
            )
            retired.append(owner_id)
        code, result = a.clear_once(claim_args)
        result["retired"] = retired
        if retired:
            result["takeover_notice"] = (
                "Retired claims without a verifiable active owner; no active process is assumed to mean no progress. Previous entries are preserved under .agentctl/retired/."
            )
        if code == 0:
            return code, result
        owners = sorted({conflict["id"] for conflict in result["conflicts"]})
        directory = a.STATE / "subscriptions"
        directory.mkdir(exist_ok=True)
        subscription = None
        for path in directory.glob("*.json"):
            previous = json.loads(path.read_text())
            if (
                not previous.get("closed")
                and time.time() - previous["created_at"] <= 7 * 86400
                and previous["session_id"] == sid
                and previous["paths"] == paths
            ):
                subscription = previous
                break
        if subscription is None:
            subscription = {
                "id": str(uuid.uuid4()),
                "session_id": sid,
                "paths": paths,
                "created_at": time.time(),
            }
        subscription["owners"] = owners
        atomic_json(directory / (subscription["id"] + ".json"), subscription)
    result.update(
        verdict="blocked",
        subscription_id=subscription["id"],
        warning="Do not edit: an owner still holds these paths. Release notification is best effort; rerun take to acquire.",
    )
    result["notifications"] = []
    for target in owners:
        claims = sorted(
            {
                conflict["claim"]
                for conflict in result["conflicts"]
                if conflict["id"] == target
            }
        )
        release = (
            "agentctl clear --drop " + shlex.join(claims)
            if all("*" not in claim for claim in claims)
            else "agentctl active 'DONE: summary'"
        )
        body = (
            f"Session {sid} requests {shlex.join(paths)}. "
            + (f"Purpose: {args.note}. " if args.note else "")
            + "The user may have directed conflicting work; coordinate the latest direction or best synthesis within existing authorization. "
            f"To coordinate: agentctl message --to {shlex.quote(sid)} --message 'your reply'. "
            f"When {'all your claimed work' if any('*' in claim for claim in claims) else 'this claimed work'} is finished, {release} releases it and triggers a best-effort notification once all blockers release. "
            "If other work remains, narrow your scope instead of marking the session DONE. "
            "Read topics/agentctl.md § Receiving coordination requests for resolving competing user directions without requiring the user in this session. "
            "Release or narrow claims after a handoff or completed work; preserve unfinished edits."
        )
        message_id = str(
            uuid.uuid5(uuid.UUID(subscription["id"]), target + str(args.wake) + body)
        )
        sent = post(a, sid, target, body, message_id, wake=args.wake)
        result["notifications"].append({"to": target, "delivery": sent["delivery"]})
    if reason:
        result["transport_note"] = reason
    return 1, result


def command(args: argparse.Namespace) -> int:
    import agentctl as a

    try:
        if int(os.environ.get(a.LAUNCH_DEPTH_ENV, "0") or "0") > 0:
            raise ValueError("session coordination is for sessions, not launched jobs")
        sid = a.agent_session_id()
        if not sid:
            raise ValueError("session coordination requires this session's identity")
        session_key(sid)
        if args.cmd == "take":
            code, result = take(a, args, sid)
            acli.emit(result, acli.resolve_format(args))
            return code
        if args.cmd == "inbox":
            acli.emit(
                {
                    "kind": "session_inbox",
                    "messages": inbox(a, sid, all_messages=args.all),
                },
                acli.resolve_format(args),
            )
            return 0
        if not args.message.strip() or len(args.message.encode()) > 64 * 1024:
            raise ValueError("--message must be nonempty and at most 64 KiB")
        targets = set(args.to or [])
        if args.active:
            _, rows = a._scan_active(a.ACTIVE_STALE_MINUTES, False, sid)
            targets.update(Path(row[1]).name for row in rows or [] if not row[5])
        if args.holding:
            targets.update(
                blockers(a, [a.active_scope_path(path) for path in args.holding], sid)
            )
        if args.waiting_for:
            targets.update(
                waiting_sessions(
                    a, [a.active_scope_path(path) for path in args.waiting_for]
                )
            )
        for target in targets:
            session_key(target)
        message_id = args.message_id or str(uuid.uuid4())
        root = message_root(a)
        outbox = root / ".outbox"
        outbox.mkdir(exist_ok=True)
        envelope = {
            "from": sid,
            "message": args.message,
            "wake": args.wake,
            "selectors": {
                "to": sorted(set(args.to or [])),
                "active": args.active,
                "holding": sorted(args.holding or []),
                "waiting_for": sorted(args.waiting_for or []),
            },
        }
        with file_lock(root / ".lock"):
            path = outbox / (message_id + ".json")
            if path.exists():
                old = json.loads(path.read_text())
                if any(old[key] != value for key, value in envelope.items()):
                    raise ValueError(
                        "message id already names another message or recipient selection"
                    )
                targets = set(old["targets"])
            else:
                if not targets:
                    raise ValueError(
                        "no recipients; use --to, --active, --holding, or --waiting-for"
                    )
                atomic_json(path, {**envelope, "targets": sorted(targets)})
        deliveries = [
            post(a, sid, target, args.message, message_id, wake=args.wake)
            for target in sorted(targets)
        ]
        acli.emit(
            {
                "kind": "session_message",
                "id": message_id,
                "deliveries": [
                    {"to": row["to"], "delivery": row["delivery"]} for row in deliveries
                ],
            },
            acli.resolve_format(args),
        )
        return 0
    except ValueError as exc:
        acli.die(str(exc), acli.ExitCode.USAGE)
    except (OSError, RuntimeError) as exc:
        acli.die(str(exc), acli.ExitCode.UNAVAILABLE)


def register(subparsers: object) -> None:
    parser = subparsers.add_parser(
        "take",
        help="Acquire paths now; retire inactive owners, otherwise return blocked and arrange release notification.",
    )
    parser.add_argument("paths", nargs="+")
    parser.add_argument(
        "--wake",
        action="store_true",
        help="Conservative mode: retain claims and ask the owning session, resuming it if necessary.",
    )
    parser.add_argument("--note", default="")
    acli.args.add_standard_args(parser)
    parser.set_defaults(func=command)
    parser = subparsers.add_parser(
        "message",
        help="Persist peer input and attempt one provider-host delivery; absent host falls back to the recipient inbox.",
    )
    parser.add_argument(
        "--to", action="append", help="Recipient session id; repeatable."
    )
    parser.add_argument(
        "--active", action="store_true", help="All fresh project peers, excluding self."
    )
    parser.add_argument(
        "--holding", nargs="+", help="Owners of overlapping path claims."
    )
    parser.add_argument(
        "--waiting-for",
        nargs="+",
        help="Sessions with pending takeover subscriptions or fresh foreground waits on overlapping paths.",
    )
    parser.add_argument("--message", required=True)
    parser.add_argument(
        "--message-id",
        type=a_uuid,
        help="UUID for an identical retry; never retries uncertain provider delivery.",
    )
    parser.add_argument(
        "--wake",
        action="store_true",
        help="Permit provider-host resume; default is live-only.",
    )
    acli.args.add_standard_args(parser)
    parser.set_defaults(func=command)
    parser = subparsers.add_parser(
        "inbox",
        help="Read persisted notices not queued to a provider; --all includes queued messages. No acknowledgment or deletion.",
    )
    parser.add_argument("--all", action="store_true")
    acli.args.add_standard_args(parser)
    parser.set_defaults(func=command)


def a_uuid(value: str) -> str:
    try:
        return str(uuid.UUID(value))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected a UUID") from exc
