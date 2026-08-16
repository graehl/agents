#!/usr/bin/env python3
from __future__ import annotations

import argparse
import atexit
import datetime as dt
import hashlib
import importlib
import json
import os
import platform
import re
import shlex
import signal
import subprocess
import sys
import time
from pathlib import Path

import acli
import acli.args as acli_args

CODE_ROOT = Path(__file__).resolve().parent
ROOT = Path(os.environ.get("AGENTCTL_ROOT") or os.getcwd()).expanduser().resolve()
STATE = ROOT / ".agentctl"
JOBS = STATE / "jobs"
RUNS = STATE / "runs"
# Active sessions (AGENTS.md convention, not job state): one file per
# launching-agent session, named by that session's id. agentctl maintains
# the current agent's entry on launch; see agent_session_id().
ACTIVE = STATE / "active"
# Minutes after which a non-DONE active-sessions entry is treated as stale
# (crashed / quiet), matching the AGENTS.md "check for active peers" idiom
# (`find .agentctl/active -mmin -70`). The `active` list view uses it as the
# default freshness window.
ACTIVE_STALE_MINUTES = 70
# Sweep destinations (`agentctl active --sweep`). Entries older than the stale
# window are archived out of active/ so the hot peer-check find never stats a
# corpse: completed (DONE-prefixed) entries go to done/, crashed/quiet ones to
# stale/ (which is then exactly the neglected-session list to audit later).
DONE_DIR = STATE / "done"
STALE = STATE / "stale"
# A session blocking in `agentctl alone` announces a non-blocking "awaiting
# alone" status here, NOT in active/. The edit-check peer scan (`find
# .agentctl/active -mmin -70`, and `_scan_active`) only reads active/, so a
# waiter is visible to browsers (`agentctl active`, the `/others` skill)
# without counting as a present peer that would impose re-Read ceremony on
# others. `alone` refreshes its entry while waiting and removes it on exit.
AWAITING = STATE / "awaiting"
# Env vars carrying the launching agent's session id, in priority order: an
# explicit override first, then known harness-provided ids. agentctl adopts the
# first value set, so plain `./agentctl` maintains the entry with no per-call
# setup. Add other harnesses' session-id vars here as they are learned.
SESSION_ID_ENVS = ("AGENTCTL_SESSION_ID", "CLAUDE_CODE_SESSION_ID")
# Set in every launched child's env and incremented per hop. A launched job is
# not an agent, so agentctl ignores the session id at depth > 0: this is the
# count-down-once flag that stops a job (or any agentctl it shells) from
# refreshing or masquerading as the launching agent's active-sessions entry.
LAUNCH_DEPTH_ENV = "AGENTCTL_LAUNCH_DEPTH"
# Set to a non-empty value to disable the parent-process-tree session-id
# recovery (session_id_from_proc_tree). Recovery is a fallback used only when
# no SESSION_ID_ENVS var is set; this opt-out exists for environments that run
# under an unrelated `resume <uuid>` ancestor and for hermetic tests.
NO_PROC_SESSION_ID_ENV = "AGENTCTL_NO_PROC_SESSION_ID"
DECLARED_IO_FILENAME = "declared.json"
PROPAGATE_FILENAME = "propagate.json"
PROJECT_ENV_FILENAME = "agentctl.env"
LIVE_JOB_STATUSES = {"running", "waiting"}
DEFAULT_LIST_SHOW_LAST = 6
ENVIRONMENT_CONTROL_FILES = (
    "pixi.toml",
    "pixi.lock",
    "pyproject.toml",
    "uv.lock",
    "poetry.lock",
    "requirements.txt",
    "environment.yml",
    "environment.yaml",
    "conda-lock.yml",
    "conda-lock.yaml",
)


def nonnegative_float(value: str) -> float:
    number = float(value)
    if number < 0:
        raise argparse.ArgumentTypeError("must be non-negative")
    return number


# ---- Plugin loader ----
#
# Plugins live in CODE_ROOT/agentctl_plugins/<name>.py and expose any subset of these
# optional hook functions; the base calls each via getattr, so missing hooks are
# simply skipped. Plugins may import this module as `agentctl` to reach the
# helpers below (e.g. `agentctl.slug`, `agentctl.command_string`, `agentctl.ROOT`).
# `agentctl.ROOT` is the project root; `agentctl.CODE_ROOT` is the install path.
#
#   register_args(parser)                       — extend start/smoke parsers
#   register_verbs(subparsers)                  — add top-level subcommands
#   on_start(args, state, env)                  — mutate state/env before launch
#   default_output_path(args, run_dir) -> Path  — first non-None wins
#   on_meta_built(state, meta_text, *,
#                 output_path, log_path,
#                 build_meta) -> str | None     — write sidecars; return new meta
#   on_finish(state)                            — post-child completion artifacts
#   on_status_print(state, lines)               — append to status one-liner
#   on_note(state, note, stamp, *,
#           meta_path, meta_text)               — react to `agentctl note`
#   on_restart(state, args)                     — refill plugin args on restart

_PLUGINS: list = []


def _load_plugins() -> None:
    if _PLUGINS:
        return
    # Make this module importable as `agentctl` for plugins, even when run
    # as __main__ (which would otherwise cause a second load on `import agentctl`).
    if "agentctl" not in sys.modules:
        sys.modules["agentctl"] = sys.modules[__name__]
    plugin_dir = CODE_ROOT / "agentctl_plugins"
    if not plugin_dir.is_dir():
        return
    if str(CODE_ROOT) not in sys.path:
        sys.path.insert(0, str(CODE_ROOT))
    for path in sorted(plugin_dir.glob("*.py")):
        if path.name.startswith("_"):
            continue
        modname = f"agentctl_plugins.{path.stem}"
        try:
            mod = importlib.import_module(modname)
        except Exception as exc:
            print(f"warning: failed to load plugin {modname}: {exc}", file=sys.stderr)
            continue
        _PLUGINS.append(mod)


def _call_hook(name: str, *args, **kw) -> None:
    for p in _PLUGINS:
        fn = getattr(p, name, None)
        if fn is not None:
            fn(*args, **kw)


def _first_hook(name: str, *args, **kw):
    for p in _PLUGINS:
        fn = getattr(p, name, None)
        if fn is not None:
            r = fn(*args, **kw)
            if r is not None:
                return r
    return None


DEFAULT_IDLE_GPU_MEMORY_USED_MIB = 3000
DEFAULT_IDLE_GPU_POWER_DRAW_W = 50.0
DEFAULT_HEARTBEAT_GPU_SMOOTH_SAMPLES = 3
DEFAULT_HEARTBEAT_GPU_SMOOTH_INTERVAL_S = 1.0
DEFAULT_ZERO_COMPUTE_REPORT_INTERVAL_S = 300.0
DEFAULT_ZERO_COMPUTE_INTERRUPT_AFTER_S = 1200.0
DEFAULT_ZERO_COMPUTE_MIN_VRAM_MIB = 3000
DEFAULT_WAIT_AFTER_UNKNOWN_GRACE_S = 15.0
WATCH_TIMEOUT_EXIT_CODE = 124
WATCH_TIMEOUT_MARKER = "agentctl-watch-timeout-v1"


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run_id() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def instance_name(job: str, serial: int) -> str:
    return f"{job}-{serial:04d}"


def parse_utc(ts: str) -> dt.datetime:
    return dt.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=dt.timezone.utc
    )


def parse_duration_seconds(text: str) -> int:
    raw = text.strip().lower()
    if not raw:
        raise ValueError("empty duration")
    if raw.isdigit():
        return int(raw)
    total = 0.0
    matches = list(re.finditer(r"(\d+(?:\.\d+)?)([smhd])", raw))
    if not matches or "".join(m.group(0) for m in matches) != raw:
        raise ValueError(f"invalid duration {text!r}")
    scales = {"s": 1.0, "m": 60.0, "h": 3600.0, "d": 86400.0}
    for match in matches:
        total += float(match.group(1)) * scales[match.group(2)]
    return round(total)


def format_duration(seconds: float | None) -> str:
    if seconds is None:
        return "?"
    total = max(0, round(float(seconds)))
    days, rem = divmod(total, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, secs = divmod(rem, 60)
    if days:
        return f"{days}d{hours:02d}h"
    if hours:
        return f"{hours}h{minutes:02d}m"
    if minutes:
        return f"{minutes}m{secs:02d}s"
    return f"{secs}s"


def elapsed_seconds(state: dict) -> int | None:
    started = state.get("started_at") or state.get("queued_at")
    if not started:
        return None
    try:
        start_dt = parse_utc(str(started))
    except ValueError:
        return None
    end_ts = state.get("finished_at") or utc_now()
    try:
        end_dt = parse_utc(str(end_ts))
    except ValueError:
        return None
    return max(0, int((end_dt - start_dt).total_seconds()))


def elapsed_estimate_text(state: dict) -> str:
    elapsed = format_duration(elapsed_seconds(state))
    estimate = state.get("runtime_estimate")
    if estimate:
        return f"{elapsed}/{estimate}"
    return elapsed


def status_returncode_text(state: dict) -> str:
    rc = state.get("returncode")
    if rc in (None, ""):
        return ""
    return str(rc)


def status_returncode_exit_code(state: dict) -> int:
    rc = state.get("returncode")
    if isinstance(rc, int):
        return rc
    if isinstance(rc, str):
        if rc == "unknown":
            return 1
        try:
            return int(rc)
        except ValueError:
            return 1
    return 0


def state_failed(state: dict) -> bool:
    return state.get("status") == "finished" and status_returncode_exit_code(state) != 0


def state_live(state: dict) -> bool:
    return state.get("status") in LIVE_JOB_STATUSES


def ensure_state_ignored() -> None:
    """Make git ignore the `.agentctl/` state dir without touching `.gitignore`.

    Runtime state under `.agentctl/` should not be committed (see
    topics/agentctl.md). Rather than edit the project's tracked `.gitignore`,
    add an *uncommitted*, repo-local rule to `$GIT_DIR/info/exclude` — visible
    only to this checkout, never staged. No-op when ROOT is not under git
    control, or when `.agentctl` is already ignored (via `.gitignore`,
    `info/exclude`, or any other source git recognizes). Best-effort: any git
    or filesystem failure is swallowed, since this is a convenience and never
    the caller's actual task.
    """

    def git(*args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["git", "-C", str(ROOT), *args],
            capture_output=True,
            text=True,
            check=False,
        )

    try:
        # Not a git repo (or git unavailable): do nothing, do not freak out.
        if git("rev-parse", "--is-inside-work-tree").returncode != 0:
            return
        # Already ignored by some source git honors: nothing to add. Probe a
        # path *under* the dir, not the bare dir, so directory-only patterns
        # (`.agentctl/`) are recognized even before the dir exists on disk —
        # git's check-ignore only matches a trailing-slash pattern against a
        # known directory otherwise.
        if git("check-ignore", "-q", str(STATE / "_")).returncode == 0:
            return
        top = git("rev-parse", "--show-toplevel").stdout.strip()
        common = git("rev-parse", "--git-common-dir").stdout.strip()
        if not top or not common:
            return
        common_path = Path(common)
        if not common_path.is_absolute():
            common_path = (ROOT / common_path).resolve()
        # Anchor the pattern to the repo root so it matches only this dir,
        # even when ROOT is a subdirectory of the worktree.
        try:
            rel = STATE.relative_to(Path(top).resolve())
        except ValueError:
            return
        pattern = "/" + rel.as_posix() + "/"
        exclude = common_path / "info" / "exclude"
        existing = ""
        if exclude.exists():
            existing = exclude.read_text(encoding="utf-8", errors="replace")
            if pattern in existing.splitlines():
                return
        exclude.parent.mkdir(parents=True, exist_ok=True)
        prefix = "" if existing == "" or existing.endswith("\n") else "\n"
        with exclude.open("a", encoding="utf-8") as fh:
            fh.write(f"{prefix}{pattern}\n")
    except Exception:
        return


def slug(text: str) -> str:
    out = "".join(ch if ch.isalnum() or ch in "._-" else "-" for ch in text.strip())
    while "--" in out:
        out = out.replace("--", "-")
    return out.strip("-") or "job"


def write_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def normalize_headline_text(text: str, max_chars: int = 240) -> str:
    flat = " | ".join(part.strip() for part in str(text).splitlines() if part.strip())
    if len(flat) > max_chars:
        flat = flat[: max_chars - 3].rstrip() + "..."
    return flat


def read_headline(path: Path) -> str:
    if not path.exists():
        return ""
    return normalize_headline_text(path.read_text(encoding="utf-8", errors="replace"))


def write_headline(path: Path, text: str) -> None:
    headline = normalize_headline_text(text)
    if not headline:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(headline + "\n", encoding="utf-8")


_UUID_RE = re.compile(
    r"\A[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}"
    r"-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\Z"
)


def _proc_ppid(pid: int) -> int | None:
    """Parent pid of `pid` from /proc/<pid>/status, or None.

    Read `PPid:` from status, not field 4 of /proc/<pid>/stat: the stat
    `comm` field is parenthesized and may contain spaces, so naive
    whitespace-splitting of stat returns the wrong field.
    """
    try:
        for line in (
            Path(f"/proc/{pid}/status")
            .read_text(encoding="utf-8", errors="replace")
            .splitlines()
        ):
            if line.startswith("PPid:"):
                return int(line.split()[1])
    except (OSError, ValueError, IndexError):
        return None
    return None


def _proc_argv(pid: int) -> list[str]:
    """argv tokens of `pid` from /proc/<pid>/cmdline (NUL-separated), or []."""
    try:
        raw = Path(f"/proc/{pid}/cmdline").read_bytes()
    except OSError:
        return []
    return [tok.decode("utf-8", "replace") for tok in raw.split(b"\x00") if tok]


def _resume_id_from_argv(argv: list[str]) -> str:
    """A resume session id from a `resume <uuid>` / `--resume[=]<uuid>` argv.

    Matches both the Codex form (positional `resume <uuid>` subcommand) and
    the Claude form (`--resume <uuid>` / `--resume=<uuid>`). Returns the first
    UUID-shaped value so found, else "".
    """
    for i, tok in enumerate(argv):
        if tok in ("resume", "--resume"):
            if i + 1 < len(argv) and _UUID_RE.match(argv[i + 1]):
                return argv[i + 1]
        elif tok.startswith("--resume="):
            val = tok[len("--resume=") :]
            if _UUID_RE.match(val):
                return val
    return ""


def session_id_from_proc_tree(max_hops: int = 8) -> str:
    """Recover a resumable session id from an ancestor's `resume <uuid>` argv.

    A terminal `codex resume <id>` (and Claude's `--resume <id>`) carries the
    resumable session id on the launching process's command line but exports
    no AGENTCTL_SESSION_ID, so a resumed agent — and agentctl with it — would
    otherwise not know which `.agentctl/active/<id>` entry is its own. Walk the
    parent chain (Linux /proc) and return the nearest such id. Best-effort:
    returns "" off Linux, in a sandbox PID namespace that hides the launcher,
    or when no resume arg is present.

    Set AGENTCTL_NO_PROC_SESSION_ID to opt out of the process-tree walk
    entirely (returns "" before reading any /proc): for a caller that does not
    want agentctl inspecting ancestor command lines, and for hermetic tests
    that must not pick up the harness's own resume id from the ambient tree.
    """
    if os.environ.get(NO_PROC_SESSION_ID_ENV, "").strip():
        return ""
    try:
        pid: int | None = os.getppid()
    except OSError:
        return ""
    hops = 0
    while pid and pid > 1 and hops < max_hops:
        sid = _resume_id_from_argv(_proc_argv(pid))
        if sid:
            return sid
        nxt = _proc_ppid(pid)
        if not nxt or nxt == pid:
            break
        pid = nxt
        hops += 1
    return ""


def agent_session_id() -> str:
    """The launching agent's session id for active-sessions upkeep, or "".

    Empty when this invocation is inside an agentctl-launched job
    (LAUNCH_DEPTH > 0) — a job is not an agent — or when no session id is
    resolvable. The launch-depth guard is checked first so a recursive /
    looping agentctl (each launch increments the count-down var) never
    refreshes or masquerades as the agent's entry, no matter how the id would
    otherwise resolve. Then the first set of SESSION_ID_ENVS wins (so plain
    `./agentctl` adopts the harness's ambient id), and finally — for a resumed
    session that exports no id (e.g. a terminal `codex resume <id>`) — the id
    is recovered from a `resume <id>` ancestor in the process tree.
    """
    try:
        depth = int(os.environ.get(LAUNCH_DEPTH_ENV, "0") or "0")
    except ValueError:
        depth = 0
    if depth > 0:
        return ""
    for var in SESSION_ID_ENVS:
        sid = os.environ.get(var, "").strip()
        if sid:
            return sid
    if os.environ.get(NO_PROC_SESSION_ID_ENV, "").strip():
        return ""
    return session_id_from_proc_tree()


def refresh_active_register(summary: str, note: str) -> None:
    """Keep the launching agent's `.agentctl/active/<session-id>` entry live.

    Active sessions are an AGENTS.md convention, not agentctl job state:
    line 1 is an agent-authored present-tense summary, optional line 2 is
    `scope:`, and a leading `DONE` on line 1 marks completion. agentctl
    maintains the current agent's entry (per `agent_session_id()`) on
    foreground launches (start / smoke / restart). It then:

      - creates the entry with `summary` as line 1 when the file did not
        exist before (the agent has not authored one yet; the agent is
        expected to overwrite this degraded line later);
      - otherwise appends `note` as a free-text line (which also refreshes
        mtime for staleness checks), never rewriting the agent-authored
        line 1 or `scope:` line 2;
      - leaves a DONE-prefixed entry untouched — the session is complete and
        readers (the /others skill) key off that prefix.

    Best-effort: a failure here must never affect the launch.
    """
    sid = agent_session_id()
    if not sid:
        return
    path = ACTIVE / sid
    try:
        if not path.exists():
            ACTIVE.mkdir(parents=True, exist_ok=True)
            path.write_text(normalize_headline_text(summary) + "\n", encoding="utf-8")
            return
        first = path.read_text(encoding="utf-8", errors="replace").splitlines()[:1]
        if first and first[0].startswith("DONE"):
            return
        line = normalize_headline_text(note)
        if line:
            with path.open("a", encoding="utf-8") as fh:
                fh.write(line + "\n")
    except OSError as exc:
        print(
            f"warning: could not update active session {path}: {exc}", file=sys.stderr
        )


ACTIVE_CLAIM_PLACEHOLDER = "active (placeholder status — set via agentctl active)"


def _split_active_header(
    lines: list[str],
) -> tuple[str | None, str | None, str | None, list[str]]:
    """Split an active entry into (line1, scope_line, tending_line, body).

    The header is line 1 plus at most one `scope:` and one `tending:` line
    immediately below it, accepted in either order (hand-written entries
    vary); the first line matching neither ends the header and starts the
    free-content body.
    """
    if not lines:
        return None, None, None, []
    scope: str | None = None
    tending: str | None = None
    idx = 1
    while idx < len(lines):
        line = lines[idx]
        if scope is None and line.startswith("scope:"):
            scope = line
        elif tending is None and line.startswith("tending:"):
            tending = line
        else:
            break
        idx += 1
    return lines[0], scope, tending, lines[idx:]


def write_active_entry(
    sid: str,
    banner: str | None = None,
    scope_paths: list[str] | None = None,
    tending: str | None = None,
    clear_tending: bool = False,
) -> tuple[str, str, str]:
    """Author `.agentctl/active/<sid>` header (line 1, `scope:`, `tending:`), body kept.

    The authoritative write shared by the `active`/`tending` verbs and
    `alone`'s register-on-success. Returns the `(line1, scope_line,
    tending_line)` actually written ("" for an absent line). Semantics:

      - line 1 := `banner` when given (a leading DONE marks completion, exactly
        as a hand-written entry); when `banner is None` the existing line 1 is
        preserved, or the placeholder is used for a new entry;
      - the `scope:` line := `scope_paths` when given, else the prior scope is
        kept;
      - the `tending:` line := `tending` when given (the value after the
        colon), dropped when `clear_tending`, else the prior line is kept —
        so a routine banner/scope update never silently sheds a steward's
        tending claim;
      - any free-content lines below the header are preserved, and the header
        is rewritten in canonical order (scope before tending).

    May raise OSError; callers decide whether that is fatal (the `active` verb)
    or best-effort (claim registration).
    """
    path = ACTIVE / sid
    old_line1: str | None = None
    old_scope: str | None = None
    old_tending: str | None = None
    body: list[str] = []
    if path.exists():
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        old_line1, old_scope, old_tending, body = _split_active_header(lines)
    if banner is not None:
        line1 = banner
    elif old_line1:
        line1 = old_line1
    else:
        line1 = normalize_headline_text(ACTIVE_CLAIM_PLACEHOLDER)
    scope_line = (
        ("scope: " + " ".join(scope_paths)) if scope_paths else (old_scope or "")
    )
    if clear_tending:
        tending_line = ""
    elif tending is not None:
        tending_line = "tending: " + tending
    else:
        tending_line = old_tending or ""
    out = [line1] + [ln for ln in (scope_line, tending_line) if ln] + body
    ACTIVE.mkdir(parents=True, exist_ok=True)
    tmp = path.parent / (path.name + ".tmp")
    tmp.write_text("\n".join(out) + "\n", encoding="utf-8")
    tmp.replace(path)
    return line1, scope_line, tending_line


def ensure_active_registered(
    sid: str,
    banner: str | None = None,
    scope_paths: list[str] | None = None,
    tending: str | None = None,
) -> str:
    """Register/refresh `.agentctl/active/<sid>` as a presence claim.

    Passing your own id to `others`/`alone` declares this session wishes to be
    active, so on the became-alone path the verb asserts that presence before
    returning — making "observed no peers" and "claimed the floor" near-atomic
    (the residual simultaneous-clearance race is why it is atomic-*ish*, not a
    lock). `alone` may also pass a `banner` (+ `scope_paths`) to fold the usual
    `agentctl active` registration into the same call — register your real
    status and wait in one go — written authoritatively on success. The
    `tending` verb passes `tending` the same way to claim steward presence on
    its observed-no-other-tending path. Returns a status word for the
    caller's message:

      - `authored` — a real banner/scope was written;
      - `created`  — a placeholder line 1 was written (caller nudges the agent
        to set a real status via `agentctl active`);
      - `refreshed`— an existing non-DONE entry's mtime was bumped, content
        intact (no file growth on repeat calls);
      - `done`     — a completed (DONE) entry was left untouched (revive it
        deliberately with `agentctl active`);
      - `noop`     — no id, or a write error.

    Registration happens only at the became-alone return, never while an
    `alone` loop is still waiting: two mutual `alone` callers that registered
    up front would each see the other and deadlock. Best-effort — a failure
    here must not fail the verb (you still observed you were alone).
    """
    if not sid:
        return "noop"
    scope_paths = scope_paths or []
    placeholder = normalize_headline_text(ACTIVE_CLAIM_PLACEHOLDER)
    path = ACTIVE / sid
    try:
        if banner or scope_paths or tending:
            # Authoring status, scope, and/or a tending claim. A bare scope or
            # tending update must not revive a completed entry; an explicit
            # banner may deliberately re-author.
            if banner is None and path.exists():
                first = path.read_text(encoding="utf-8", errors="replace").splitlines()[
                    :1
                ]
                if first and first[0].startswith("DONE"):
                    return "done"
            line1, _, _ = write_active_entry(sid, banner, scope_paths, tending=tending)
            return "created" if line1 == placeholder else "authored"
        # Pure claim: ensure an entry exists and is fresh, without clobbering.
        if not path.exists():
            ACTIVE.mkdir(parents=True, exist_ok=True)
            path.write_text(placeholder + "\n", encoding="utf-8")
            return "created"
        first = path.read_text(encoding="utf-8", errors="replace").splitlines()[:1]
        if first and first[0].startswith("DONE"):
            return "done"
        os.utime(path, None)  # refresh mtime to now, leaving content intact
        return "refreshed"
    except OSError as exc:
        print(
            f"warning: could not register active session {path}: {exc}", file=sys.stderr
        )
        return "noop"


_ACTIVE_TOUCH_INTERVAL = 300.0
_last_active_touch = 0.0


def touch_active_entry() -> None:
    """Refresh this agent's active-entry mtime during a long foreground block.

    The `wait`/`watch`/`wait-gpu` loops call this each poll so a session
    obeying the ~55-min blanket wait cap (RUNS.md) stays inside the
    ACTIVE_STALE_MINUTES window even when it launches nothing between waits —
    otherwise a genuinely present session (e.g. an on-deck steward between
    hourly wakes) ages out and reads as absent to peer and tending checks.
    Self-throttled to one touch per _ACTIVE_TOUCH_INTERVAL. Content is never
    written: no growth, no DONE revival, and no entry is manufactured for a
    session that never registered one.
    """
    global _last_active_touch
    now = time.monotonic()
    if now - _last_active_touch < _ACTIVE_TOUCH_INTERVAL:
        return
    _last_active_touch = now
    sid = agent_session_id()
    if not sid:
        return
    path = ACTIVE / sid
    try:
        first = path.read_text(encoding="utf-8", errors="replace").splitlines()[:1]
        if first and first[0].startswith("DONE"):
            return
        os.utime(path, None)
    except OSError:
        return


def active_scope_path(raw: str) -> str:
    """Normalize one intend-to-edit path for an active-session `scope:` line.

    Scope paths are project-root-relative so the prefix-match overlap check
    (AGENTS.md § Active sessions) lines up across peers regardless of each
    agent's cwd. An absolute path under ROOT is made relative; a leading
    `./` is stripped; wildcards are kept verbatim. Callers should use the
    separator-anchored glob grammar (topics/agentctl.md § Active-sessions
    file schema: trailing `/**` or `.`-anchored extension globs); this
    normalizer keeps but does not enforce it. Existence is not required —
    the path may name a file the agent is about to create.
    """
    p = raw.strip()
    if not p:
        return ""
    candidate = Path(p)
    if candidate.is_absolute():
        try:
            return str(candidate.resolve(strict=False).relative_to(ROOT))
        except ValueError:
            return p
    if p.startswith("./"):
        return p[2:]
    return p


def active_register(args) -> int:
    """`active` verb: author this session's `.agentctl/active/<id>` entry.

    Unlike the passive refresh on launch (refresh_active_register), this is
    the agent deliberately authoring its own entry, and it writes no run
    record — no job, no Aim dump, no log — so a session can announce or
    re-scope its presence without launch noise. The launch-depth guard
    still applies: a launched job (depth > 0) is not an agent and may not
    author the entry.

    The agent owns line 1 and the `scope:` line 2, so both are written
    authoritatively rather than appended:

      - line 1 becomes `banner` verbatim; a leading `DONE` marks the
        session complete exactly as a hand-written entry would;
      - `scope: <paths>` becomes line 2 when intend-to-edit paths are
        given, replacing any prior scope line; with no paths an existing
        scope line is left in place;
      - any free-content lines below the header are preserved.
    """
    try:
        depth = int(os.environ.get(LAUNCH_DEPTH_ENV, "0") or "0")
    except ValueError:
        depth = 0
    if depth > 0:
        print(
            "agentctl active: refusing to author an active entry from inside a "
            "launched job (a job is not an agent)",
            file=sys.stderr,
        )
        return 2
    sid = agent_session_id()
    if not sid:
        print(
            "agentctl active: no session id; set one of "
            f"{', '.join(SESSION_ID_ENVS)} (a launcher such as yepanywhere can "
            "inject AGENTCTL_SESSION_ID)",
            file=sys.stderr,
        )
        return 2
    banner = normalize_headline_text(args.banner)
    if not banner:
        print("agentctl active: empty banner", file=sys.stderr)
        return 2
    scope_paths = [s for s in (active_scope_path(p) for p in args.paths) if s]

    claim_tending = bool(getattr(args, "tending", False))
    clear_tending = bool(getattr(args, "no_tending", False))
    until = getattr(args, "until", None)
    if claim_tending and clear_tending:
        print("agentctl active: --tending and --no-tending conflict", file=sys.stderr)
        return 2
    if until and not claim_tending:
        print("agentctl active: --until requires --tending", file=sys.stderr)
        return 2
    tending = (
        ("on-deck" + (f" until {until}" if until else "")) if claim_tending else None
    )
    fmt = _resolve_acli_format(args)

    path = ACTIVE / sid
    try:
        _, scope_line, tending_line = write_active_entry(
            sid, banner, scope_paths, tending=tending, clear_tending=clear_tending
        )
    except OSError as exc:
        print(f"agentctl active: could not write {path}: {exc}", file=sys.stderr)
        return 1

    try:
        shown: Path | str = path.relative_to(ROOT)
    except ValueError:
        shown = path
    payload = {
        "kind": "active_register",
        "ok": True,
        "path": str(shown),
        "id": sid,
        "banner": banner,
    }
    scope_value = _header_value(scope_line)
    tending_value = _header_value(tending_line)
    if scope_value:
        payload["scope"] = scope_value
    if tending_value:
        payload["tending"] = tending_value
    if bool(getattr(args, "full", False)):
        payload["scope_line"] = scope_line
        payload["tending_line"] = tending_line
    acli.emit(payload, fmt)
    return 0


_SESSION_ID_RE = re.compile(
    r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\Z"
)


def _looks_like_session_id(name: str) -> bool:
    """True for a UUID-shaped id (Codex rollout id, Claude session id).

    A conservative smell test: real provider session ids are UUIDs, so a
    non-UUID active/ filename (e.g. `codex-recap-quote-reply`) is almost
    certainly an agent-invented "tasteful" tag. Kept loose on purpose (any
    UUID shape, no version-nibble check) to avoid false-flagging a provider
    that mints a differently-versioned uuid.
    """
    return bool(_SESSION_ID_RE.match(name))


def _id_name_warning(rel: str) -> str:
    """A loud suffix for an entry whose filename is not a plausible session id.

    A hand-invented tag is never DONE-marked by the session it names — a
    fabricated id is not carried in env across calls, and on resume the real
    id reappears — so it lingers as a false live peer until it ages out. We
    flag it rather than filter it: it still counts as a peer, and the reader
    needs to see (and retire) it.
    """
    name = rel.rsplit("/", 1)[-1]
    if _looks_like_session_id(name):
        return ""
    return "  (WARN: not a session-id filename — likely a hand-invented tag)"


def _scan_active(minutes: int, include_done: bool, self_id: str):
    """Scan active-sessions entries; return (now, rows), or (now, None) when no
    active-state dir exists at all.

    rows are newest-first tuples `(mtime, relpath, line1, scope, tending,
    is_self)`, shared by the `active` (list), `others`, and `tending` verbs
    so all read the same window. The performance-critical peer check is the raw
    `find .agentctl/active -maxdepth 1 -type f -mmin -70`; these verbs are the
    richer convenience. active/ holds within-window entries; the sweep archives
    older ones to stale/ (crashed/quiet) and done/ (completed), so a window
    reaching past the stale threshold must read those dirs too. The default
    window touches only active/, keeping the common call cheap.
    """
    now = time.time()
    dirs = [ACTIVE]
    if minutes == 0 or minutes > ACTIVE_STALE_MINUTES:
        dirs += [STALE, DONE_DIR]
    dirs = [d for d in dirs if d.is_dir()]
    if not dirs:
        return now, None

    rows: list[tuple[float, str, str, str, str, bool]] = []
    seen: set[str] = set()  # a re-authored id can sit in both active/ and an archive
    for d in dirs:
        for path in d.iterdir():
            if not path.is_file() or path.name in seen:
                continue
            seen.add(path.name)
            try:
                mtime = path.stat().st_mtime
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            raw_line1, raw_scope, raw_tending, _ = _split_active_header(
                text.splitlines()
            )
            line1 = (raw_line1 or "").strip()
            is_done = line1.startswith("DONE")
            if is_done and not include_done:
                continue
            if minutes and now - mtime > minutes * 60:
                continue
            scope = (raw_scope or "").strip()
            tending = (raw_tending or "").strip()
            rows.append(
                (
                    mtime,
                    f".agentctl/{d.name}/{path.name}",
                    line1,
                    scope,
                    tending,
                    path.name == self_id,
                )
            )

    rows.sort(key=lambda r: r[0], reverse=True)
    return now, rows


def _scan_awaiting(minutes: int) -> list[tuple[float, str, str, str]]:
    """Scan the non-blocking `awaiting/` queue: rows `(mtime, relpath, line1, scope)`.

    Read only for display (`agentctl active`); awaiting entries never enter the
    peer/aloneness computation, so a waiting session is noticed without
    imposing edit-check ceremony. Windowed like active/ (a waiter refreshes its
    entry every poll, so a live one is always fresh; a crashed waiter ages out).
    """
    if not AWAITING.is_dir():
        return []
    now = time.time()
    rows: list[tuple[float, str, str, str]] = []
    for path in AWAITING.iterdir():
        if not path.is_file():
            continue
        try:
            mtime = path.stat().st_mtime
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if minutes and now - mtime > minutes * 60:
            continue
        lines = text.splitlines()
        line1 = lines[0].strip() if lines else ""
        scope = (
            lines[1].strip() if len(lines) > 1 and lines[1].startswith("scope:") else ""
        )
        rows.append((mtime, f".agentctl/awaiting/{path.name}", line1, scope))
    rows.sort(key=lambda r: r[0], reverse=True)
    return rows


def _window_label(minutes: int) -> str:
    return "any age" if not minutes else f"last {minutes}m"


def _header_value(line: str) -> str:
    return line.partition(":")[2].strip() if line else ""


def _active_row_payload(
    now: float,
    mtime: float,
    rel: str,
    line1: str,
    scope: str,
    tending: str,
    is_self: bool = False,
    *,
    full: bool = False,
) -> dict:
    row = {
        "id": Path(rel).name,
        "status": line1 or "",
        "age_seconds": int(max(0, now - mtime)),
    }
    scope_value = _header_value(scope)
    tending_value = _header_value(tending)
    if scope_value:
        row["scope"] = scope_value
    if tending_value:
        row["tending"] = tending_value
    if is_self:
        row["self"] = True
    warning = _id_name_warning(rel).strip()
    if warning:
        row["warning"] = warning
    if full:
        row.update(
            {
                "path": rel,
                "mtime": mtime,
                "age": format_duration(now - mtime),
                "scope_line": scope,
                "tending_line": tending,
            }
        )
    return row


def _awaiting_row_payload(
    now: float,
    mtime: float,
    rel: str,
    line1: str,
    scope: str,
    *,
    full: bool = False,
) -> dict:
    row = {
        "id": Path(rel).name,
        "status": line1 or "",
        "age_seconds": int(max(0, now - mtime)),
        "awaiting": True,
    }
    scope_value = _header_value(scope)
    if scope_value:
        row["scope"] = scope_value
    warning = _id_name_warning(rel).strip()
    if warning:
        row["warning"] = warning
    if full:
        row.update(
            {
                "path": rel,
                "mtime": mtime,
                "age": format_duration(now - mtime),
                "scope_line": scope,
            }
        )
    return row


def _resolve_acli_format(args) -> acli.Format:
    try:
        return acli.resolve_format(args)
    except ValueError as exc:
        acli.die(str(exc), acli.ExitCode.USAGE)


def write_awaiting(path: Path, status: str, scope_paths: list[str]) -> bool:
    """Best-effort write of a non-blocking `awaiting/` entry. Returns success.

    line 1 is the `awaiting alone[ then: <X>]` status; line 2 is the optional
    `scope:`. Never raises — a failure here must not break the wait loop.
    """
    out = [status] + ([f"scope: {' '.join(scope_paths)}"] if scope_paths else [])
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.parent / (path.name + ".tmp")
        tmp.write_text("\n".join(out) + "\n", encoding="utf-8")
        tmp.replace(path)
        return True
    except OSError as exc:
        print(f"warning: could not write awaiting entry {path}: {exc}", file=sys.stderr)
        return False


def active_list(args) -> int:
    """`active` with no banner: list active-sessions entries + status lines.

    The read counterpart to authoring `agentctl active "<banner>"`. It is the
    AGENTS.md "check for active peers" idiom (`find .agentctl/active -mmin -70`,
    entries not starting with DONE) as a verb, printing each session's line-1
    status and `scope:` line so a peer-overlap check is one command instead of
    a find+head pipeline. By default it shows only fresh (mtime within
    --minutes, default ACTIVE_STALE_MINUTES) non-DONE entries; --minutes 0
    drops the freshness window so stale/crashed entries show too, and --done
    also includes DONE-prefixed (completed) entries.

    Output is an ACLI payload with `sessions` and `awaiting` arrays, newest
    first, defaulting to compact JSONL for agents and pipes.
    """
    minutes = max(0, int(getattr(args, "minutes", ACTIVE_STALE_MINUTES)))
    include_done = bool(getattr(args, "done", False))
    fmt = _resolve_acli_format(args)
    now, rows = _scan_active(minutes, include_done, agent_session_id())
    awaiting = _scan_awaiting(minutes)
    full = bool(getattr(args, "full", False))
    sessions = [
        _active_row_payload(now, mtime, rel, line1, scope, tending, is_self, full=full)
        for mtime, rel, line1, scope, tending, is_self in (rows or [])
    ]
    # Awaiting peers are listed after working ones, tagged so a browser sees
    # the queued wait without mistaking it for a blocking (edit-check) peer.
    awaiting_rows = [
        _awaiting_row_payload(now, mtime, rel, line1, scope, full=full)
        for mtime, rel, line1, scope in awaiting
    ]
    acli.emit(
        {
            "kind": "active_sessions",
            "window": _window_label(minutes),
            "minutes": minutes,
            "include_done": include_done,
            "count": len(sessions),
            "awaiting_count": len(awaiting_rows),
            "missing_active_dir": rows is None,
            "sessions": sessions,
            "awaiting": awaiting_rows,
        },
        fmt,
    )
    return 0


def others_cmd(args) -> int:
    """`others [session-id]`: the peer-check with self excluded and a verdict.

    Why carry your own id: `active` lists everyone and leaves you to subtract
    yourself, so a session re-confirming a "peers present" belief still has to
    parse rows. `others <id>` drops your entry and emits a structured verdict
    with `other_count` and `has_peers`. Passing the id is also the nudge for a
    session to know it; with no
    id given it falls back to agent_session_id(), and excludes nothing if that
    is empty too (so it degrades to `active`-style output rather than failing).

    The exit code is the peer signal: 0 when you are alone (no other peers in
    the window), nonzero when peers are present, so `agentctl others <id> &&
    <solo-only step>` gates work on actually being solo. Passing your id is
    also a claim: on the alone path it registers your `active/<id>` entry
    (ensure_active_registered) before returning, so the observe-then-proceed
    race is mostly closed; with the id only resolved (no positional) the verb
    stays read-only. All peers count — there is deliberately no narrowing to
    `scope:`-overlapping peers (these are the project-serial verbs). Same
    window semantics: default fresh non-DONE; --minutes 0 widens to any age
    (stale/crashed), --done adds completed peers.
    """
    minutes = max(0, int(getattr(args, "minutes", ACTIVE_STALE_MINUTES)))
    include_done = bool(getattr(args, "done", False))
    provided = getattr(args, "uuid", None)
    fmt = _resolve_acli_format(args)
    now, rows = _scan_active(minutes, include_done, provided or agent_session_id())
    window = _window_label(minutes)
    full = bool(getattr(args, "full", False))

    peers = [r for r in rows if not r[5]] if rows else []
    if not peers:
        payload = {
            "kind": "active_peers",
            "window": window,
            "other_count": 0,
            "has_peers": False,
            "peers": [],
            "missing_active_dir": rows is None,
        }
        if provided:
            status = ensure_active_registered(provided)
            payload["registered"] = {"id": provided, "status": status}
            if status == "created":
                payload["next_command"] = 'agentctl active "<status>" [<scope>...]'
        acli.emit(payload, fmt)
        return 0

    acli.emit(
        {
            "kind": "active_peers",
            "window": window,
            "other_count": len(peers),
            "has_peers": True,
            "peers": [
                _active_row_payload(now, mtime, rel, line1, scope, tending, full=full)
                for mtime, rel, line1, scope, tending, _ in peers
            ],
            "missing_active_dir": rows is None,
        },
        fmt,
    )
    return 1


def tending_cmd(args) -> int:
    """`tending [<session-id>]`: is any other session tending this project?

    The steward-presence specialization of `others`. `others` answers "is
    anyone here?"; this answers the forward-looking question "will an agent
    launch more queued work when it wakes?" — the difference matters because
    a steward between hourly wakes has no running process and may have no
    running job, yet is still committed to filling the queue. A session
    declares that commitment with a `tending:` header line in its own
    `.agentctl/active/<id>` entry (schema: topics/agentctl.md), and this verb
    counts exactly the fresh, non-DONE entries carrying one, self excluded.

    The exit code is the signal, mirroring `others`: 0 = no other tending
    session, nonzero = one or more (listed). A steward round gates itself
    with `agentctl tending <id> && <round>` so two stewards do not race the
    same queue. Passing your id on the clear path is also the claim: the verb
    writes your entry's `tending:` line (creating a placeholder entry when
    you have none), so observe-nobody-tending and claim-tending are
    near-atomic — the same atomic-ish race window as `others`. The claim
    value is `on-deck`, plus `until <deadline>` from --until; the deadline is
    informative for readers, not enforced — staleness (the --minutes window)
    is the enforcement, so a crashed steward stops counting within ~70m.
    """
    minutes = max(0, int(getattr(args, "minutes", ACTIVE_STALE_MINUTES)))
    include_done = bool(getattr(args, "done", False))
    provided = getattr(args, "uuid", None)
    fmt = _resolve_acli_format(args)
    now, rows = _scan_active(minutes, include_done, provided or agent_session_id())
    window = _window_label(minutes)
    full = bool(getattr(args, "full", False))

    tenders = [r for r in (rows or []) if r[4] and not r[5]]
    if not tenders:
        payload = {
            "kind": "tending_sessions",
            "window": window,
            "other_count": 0,
            "has_tending_peer": False,
            "tenders": [],
            "missing_active_dir": rows is None,
        }
        if provided:
            until = getattr(args, "until", None)
            own_tending = next((r[4] for r in (rows or []) if r[5] and r[4]), "")
            if own_tending and not until:
                # Re-claim of an existing line: rewrite the same value, so an
                # `until` qualifier authored earlier survives the hourly wake.
                value = own_tending.partition(":")[2].strip()
                claim_action = "refreshed"
            else:
                value = "on-deck" + (f" until {until}" if until else "")
                claim_action = "registered"
            status = ensure_active_registered(provided, tending=value)
            payload["registered"] = {
                "id": provided,
                "status": status,
                "tending": value,
                "action": claim_action,
            }
            if status == "done":
                payload["next_command"] = 'agentctl active "<status>"'
            elif status == "created":
                payload["next_command"] = 'agentctl active "<status>" [<scope>...]'
        acli.emit(payload, fmt)
        return 0

    acli.emit(
        {
            "kind": "tending_sessions",
            "window": window,
            "other_count": len(tenders),
            "has_tending_peer": True,
            "tenders": [
                _active_row_payload(now, mtime, rel, line1, scope, tending, full=full)
                for mtime, rel, line1, scope, tending, _ in tenders
            ],
            "missing_active_dir": rows is None,
        },
        fmt,
    )
    return 1


def alone_cmd(args) -> int:
    """`alone [<session-id>]`: block until no other active peer remains.

    The waiting counterpart to `others`: the same self-excluded peer set, but
    instead of a one-shot verdict it polls until the set is empty and then
    returns 0 — so `agentctl alone <id> && <solo-only step>` blocks the step
    until you are actually alone (e.g. before an amend/rebase in a shared
    worktree). All peers count — there is deliberately no narrowing to
    `scope:`-overlapping peers; this is whole-project serialization, not the
    finer per-path coordination handled by the re-Read + scope check. A peer
    leaves the set when it writes DONE or ages past the --minutes window, so a
    crashed peer clears when it goes stale, not the instant it dies. Returns
    nonzero only on --timeout (0 = wait forever).

    Passing your id claims the floor: on the became-alone return (only there,
    so two mutual callers do not deadlock) it registers your `active/<id>`
    entry before returning, near-atomically with observing no peers. With
    `--banner`/scope it folds `agentctl active` into the wait — register your
    real status and scope and wait in one go, written on success; bare, the
    claim is a placeholder and the payload names the follow-up command.

    While actually waiting, it announces a non-blocking `awaiting/<id>` status
    (`awaiting alone`, plus `then: <banner>` when one is given), refreshed each
    poll and removed on exit. That entry lives outside active/, so a browser
    (`agentctl active`, `/others`) notices the queued wait but no peer's
    edit-check counts it — the wait is seen without imposing re-Read ceremony.

    Output is a JSONL event stream by default: one `alone_wait` event when
    peers block progress, heartbeat `alone_wait` events when --heartbeat asks
    for re-statements, and a final `alone` or `alone_timeout` event.
    """
    minutes = max(0, int(getattr(args, "minutes", ACTIVE_STALE_MINUTES)))
    include_done = bool(getattr(args, "done", False))
    provided = getattr(args, "uuid", None)
    self_id = provided or agent_session_id()
    banner = normalize_headline_text(getattr(args, "banner", None) or "") or None
    scope_paths = [
        s
        for s in (active_scope_path(p) for p in (getattr(args, "scope", None) or []))
        if s
    ]
    poll = max(0.5, float(getattr(args, "poll", 5.0)))
    heartbeat_interval = max(0.0, float(getattr(args, "heartbeat", 30.0) or 0.0))
    timeout = float(getattr(args, "timeout", 0.0) or 0.0)
    deadline = time.time() + timeout if timeout > 0 else None
    fmt = _resolve_acli_format(args)

    announced = False  # printed the initial naming line yet
    next_report = 0.0

    # A non-blocking "awaiting alone" announcement, written only once we are
    # actually waiting (peers present) and removed on exit. "then: <X>" is
    # appended when a banner names what the wait is for. It lives in awaiting/,
    # not active/, so a browser notices the wait but the edit-check peer scan
    # never counts it. Keyed by the resolved id (positional or env) — only the
    # active/ *claim* requires the deliberate positional id.
    await_path = (AWAITING / self_id) if self_id else None
    await_status = "awaiting alone" + (f" then: {banner}" if banner else "")
    await_written = False

    try:
        while True:
            now, rows = _scan_active(minutes, include_done, self_id)
            peers = [r for r in rows if not r[5]] if rows else []
            if not peers:
                payload = {
                    "kind": "alone",
                    "window": _window_label(minutes),
                    "alone": True,
                    "other_count": 0,
                    "peers": [],
                    "missing_active_dir": rows is None,
                }
                if provided:
                    status = ensure_active_registered(provided, banner, scope_paths)
                    payload["registered"] = {"id": provided, "status": status}
                    if banner:
                        payload["registered"]["banner"] = banner
                    if scope_paths:
                        payload["registered"]["scope"] = scope_paths
                    if status == "created":
                        payload["next_command"] = (
                            'agentctl active "<status>" [<scope>...]'
                        )
                acli.emit(payload, fmt)
                return 0

            # Waiting: announce the non-blocking awaiting status once, then keep
            # it fresh each poll so a long wait stays inside the staleness window.
            if await_path is not None:
                if not await_written:
                    await_written = write_awaiting(
                        await_path, await_status, scope_paths
                    )
                else:
                    try:
                        os.utime(await_path, None)
                    except OSError:
                        pass

            now = time.time()
            peer_rows = [
                _active_row_payload(now, mtime, rel, line1, scope, tending, full=True)
                for mtime, rel, line1, scope, tending, _ in peers
            ]
            if not announced:
                acli.emit(
                    {
                        "kind": "alone_wait",
                        "window": _window_label(minutes),
                        "other_count": len(peers),
                        "peers": peer_rows,
                    },
                    fmt,
                )
                announced = True
                next_report = now + heartbeat_interval
            elif heartbeat_interval > 0 and now >= next_report:
                acli.emit(
                    {
                        "kind": "alone_wait",
                        "window": _window_label(minutes),
                        "other_count": len(peers),
                        "peers": peer_rows,
                        "heartbeat": True,
                    },
                    fmt,
                )
                next_report = now + heartbeat_interval

            if deadline is not None and time.time() >= deadline:
                acli.emit(
                    {
                        "kind": "alone_timeout",
                        "window": _window_label(minutes),
                        "timeout_seconds": timeout,
                        "other_count": len(peers),
                        "peers": peer_rows,
                    },
                    fmt,
                )
                return 1

            time.sleep(poll)
    finally:
        if await_written and await_path is not None:
            try:
                await_path.unlink()
            except OSError:
                pass


def active_sweep(args) -> int:
    """`active --sweep`: archive stale active-sessions entries out of active/.

    Keeps the hot peer-check dir — scanned by the AGENTS.md idiom
    `find .agentctl/active -maxdepth 1 -type f -mmin -70` — holding only
    within-window entries, so the common "no peers" check never stats a
    completed or crashed corpse. Entries older than --minutes (default
    ACTIVE_STALE_MINUTES) are moved out of active/:

      - a DONE-prefixed (completed) entry -> .agentctl/done/
      - any other (crashed / quiet) entry -> .agentctl/stale/, which is then
        exactly the neglected-session list to audit later

    Fresh entries (live peers, just-finished sessions still inside the window)
    are left in place. Moves are reversible — entries are relocated, not
    deleted, and `active --minutes 0` / `--done` list them back from the
    archive dirs. --dry-run reports without moving.
    """
    minutes = int(getattr(args, "minutes", ACTIVE_STALE_MINUTES))
    # A sweep with minutes <= 0 would treat every entry as stale and empty
    # active/ wholesale; that is never the intent, so fall back to the window.
    if minutes <= 0:
        minutes = ACTIVE_STALE_MINUTES
    dry_run = bool(getattr(args, "dry_run", False))
    fmt = _resolve_acli_format(args)

    if not ACTIVE.is_dir():
        acli.emit(
            {
                "kind": "active_sweep",
                "missing_active_dir": True,
                "done": 0,
                "stale": 0,
                "dry_run": dry_run,
                "threshold_minutes": minutes,
            },
            fmt,
        )
        return 0

    moved = sweep_stale_entries(minutes, dry_run=dry_run, quiet=True)
    acli.emit(
        {
            "kind": "active_sweep",
            "missing_active_dir": False,
            "done": moved["done"],
            "stale": moved["stale"],
            "entries": moved["entries"],
            "dry_run": dry_run,
            "threshold_minutes": minutes,
        },
        fmt,
    )
    return 0


def sweep_stale_entries(
    minutes: int, dry_run: bool = False, quiet: bool = False
) -> dict:
    """Archive active/ entries older than `minutes`: DONE -> done/, else stale/.

    The shared core of `active --sweep` and the opportunistic sweep on
    foreground launches (which passes quiet=True so launch output stays
    clean). Returns the moved counts {"done": n, "stale": n}; per-entry
    failures warn and continue, so a best-effort caller needs no guard.
    """
    now = time.time()
    threshold = minutes * 60
    moved = {"done": 0, "stale": 0, "entries": []}
    if not ACTIVE.is_dir():
        return moved
    for path in sorted(ACTIVE.iterdir()):
        if not path.is_file():
            continue
        try:
            mtime = path.stat().st_mtime
            first = path.read_text(encoding="utf-8", errors="replace").splitlines()[:1]
        except OSError:
            continue
        if now - mtime <= threshold:
            continue  # fresh: live peer or just-finished session
        kind = "done" if (first and first[0].startswith("DONE")) else "stale"
        dest_dir = DONE_DIR if kind == "done" else STALE
        if dry_run:
            moved["entries"].append(
                {"id": path.name, "target": kind, "action": "would_archive"}
            )
            if not quiet:
                print(f"would move {path.name} -> {kind}/")
        else:
            try:
                dest_dir.mkdir(parents=True, exist_ok=True)
                path.replace(
                    dest_dir / path.name
                )  # atomic within .agentctl; overwrites
            except OSError as exc:
                print(
                    f"agentctl active sweep: could not move {path}: {exc}",
                    file=sys.stderr,
                )
                continue
            moved["entries"].append(
                {"id": path.name, "target": kind, "action": "archived"}
            )
            if not quiet:
                print(f"moved {path.name} -> {kind}/")
        moved[kind] += 1
    return moved


def active_cmd(args) -> int:
    """Dispatch the `active` verb: sweep, list (no banner), or author (banner)."""
    if getattr(args, "sweep", False):
        return active_sweep(args)
    if getattr(args, "banner", None) is None:
        return active_list(args)
    return active_register(args)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def current_path(job: str) -> Path:
    return JOBS / slug(job) / "current.json"


def update_state_files(state: dict) -> None:
    write_json(Path(state["state_path"]), state)
    write_json(current_path(state["job"]), state)


def exit_status_path_for_state(state: dict) -> Path:
    raw = state.get("exit_status_path")
    if raw:
        return Path(str(raw))
    run_dir = state.get("run_dir")
    if run_dir:
        return Path(str(run_dir)) / "exit-status.json"
    return Path(state["state_path"]).with_name("exit-status.json")


def running_marker_path(target: str | Path) -> Path:
    path = Path(target)
    if str(path).endswith(".running.md"):
        return path
    return Path(f"{path}.running.md")


def marker_fields(path: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return fields
    for line in lines:
        if not line.startswith("- ") or ": " not in line:
            continue
        key, value = line[2:].split(": ", 1)
        fields[key.strip()] = value.strip()
    return fields


def output_for_marker(path: Path, fields: dict[str, str]) -> Path:
    raw = fields.get("out", "").strip()
    if raw:
        out = Path(raw)
        return out if out.is_absolute() else (ROOT / out).resolve(strict=False)
    marker = str(path)
    if marker.endswith(".running.md"):
        return Path(marker[: -len(".running.md")])
    return path


def completion_sidecar(output: Path) -> Path | None:
    for candidate in (Path(f"{output}.meta.md"), Path(f"{output}.meta.json")):
        if candidate.exists():
            return candidate
    return None


def marker_pid_status(fields: dict[str, str]) -> str:
    raw = fields.get("pid", "").strip()
    if not raw:
        return "unknown"
    try:
        pid = int(raw)
    except ValueError:
        return "unknown"
    return "running" if pid_alive(pid) else "dead"


def serial_path(job: str) -> Path:
    return JOBS / slug(job) / "next-serial.txt"


def next_serial(job: str) -> int:
    path = serial_path(job)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        current = int(path.read_text(encoding="utf-8").strip())
    except Exception:
        current = 0
    serial = current + 1
    tmp = path.with_suffix(".tmp")
    tmp.write_text(f"{serial}\n", encoding="utf-8")
    tmp.replace(path)
    return serial


def pid_alive(pid: int) -> bool:
    state = proc_state(pid)
    if state == "Z":
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        # Sandboxed status calls can report ESRCH for a process that is visible
        # through /proc and still owns GPU work. Trust /proc as the Linux fallback.
        return Path(f"/proc/{pid}").exists() and proc_state(pid) != "Z"
    except PermissionError:
        return True
    return True


def process_visibility_limited() -> bool:
    """Return true when /proc only reflects a sandbox PID namespace.

    In that situation a host PID recorded by agentctl can be invisible even
    though the job is still alive.  Status calls must not persist "finished"
    based on that false negative.
    """
    try:
        proc1 = Path("/proc/1/cmdline").read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False
    return "codex-linux-sandbox" in proc1 or "bwrap" in proc1


def proc_pgid(pid: int) -> int | None:
    """Return process group id from /proc/<pid>/stat, or None if unavailable."""
    try:
        stat = Path(f"/proc/{pid}/stat").read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    # comm is parenthesized and may contain spaces, so split after the final ")".
    _, sep, rest = stat.rpartition(")")
    if not sep:
        return None
    fields = rest.strip().split()
    if len(fields) < 3:
        return None
    try:
        return int(fields[2])
    except ValueError:
        return None


def proc_state(pid: int) -> str | None:
    try:
        stat = Path(f"/proc/{pid}/stat").read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    _, sep, rest = stat.rpartition(")")
    if not sep:
        return None
    fields = rest.strip().split()
    if not fields:
        return None
    return fields[0]


def proc_cmdline(pid: int) -> str | None:
    try:
        raw = Path(f"/proc/{pid}/cmdline").read_bytes()
    except OSError:
        return None
    if not raw:
        return ""
    parts = [
        part.decode("utf-8", errors="replace") for part in raw.split(b"\0") if part
    ]
    return "\0".join(parts)


def proc_start_ticks(pid: int) -> int | None:
    try:
        stat = Path(f"/proc/{pid}/stat").read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    _, sep, rest = stat.rpartition(")")
    if not sep:
        return None
    fields = rest.strip().split()
    if len(fields) < 20:
        return None
    try:
        return int(fields[19])
    except ValueError:
        return None


def boot_time_epoch() -> float | None:
    try:
        uptime = float(Path("/proc/uptime").read_text(encoding="utf-8").split()[0])
    except Exception:
        return None
    return time.time() - uptime


def proc_start_epoch(pid: int) -> float | None:
    ticks = proc_start_ticks(pid)
    if ticks is None:
        return None
    boot_epoch = boot_time_epoch()
    if boot_epoch is None:
        return None
    try:
        hz = os.sysconf(os.sysconf_names["SC_CLK_TCK"])
    except (AttributeError, KeyError, ValueError):
        hz = 100
    if not hz:
        return None
    return boot_epoch + (ticks / float(hz))


def current_pid_namespace() -> str:
    try:
        return os.readlink("/proc/self/ns/pid")
    except OSError:
        return ""


def pid_matches_state(pid: int, state: dict) -> bool:
    if pid <= 0:
        return False
    if proc_state(pid) == "Z":
        return False
    recorded_ticks = state.get("pid_start_ticks")
    if recorded_ticks not in (None, ""):
        try:
            if proc_start_ticks(pid) != int(recorded_ticks):
                return False
        except (TypeError, ValueError):
            return False
    else:
        started_at = state.get("started_at")
        if started_at:
            try:
                started_epoch = parse_utc(str(started_at)).timestamp()
            except ValueError:
                started_epoch = None
            proc_epoch = proc_start_epoch(pid)
            # Older states lack launch-time pid identity. In that case, reject
            # obviously unrelated host processes that predate the recorded job.
            if (
                started_epoch is not None
                and proc_epoch is not None
                and proc_epoch + 60 < started_epoch
            ):
                return False
    recorded_cmdline = state.get("pid_cmdline")
    if recorded_cmdline not in (None, ""):
        current_cmdline = proc_cmdline(pid)
        if current_cmdline != str(recorded_cmdline):
            return False
    return True


def process_group_members(pgid: int) -> list[int]:
    members: list[int] = []
    proc = Path("/proc")
    try:
        entries = list(proc.iterdir())
    except OSError:
        return members
    for entry in entries:
        if not entry.name.isdigit():
            continue
        pid = int(entry.name)
        if proc_pgid(pid) == pgid and proc_state(pid) != "Z":
            members.append(pid)
    return sorted(members)


def process_group_alive(pgid: int) -> bool:
    members = process_group_members(pgid)
    if members:
        return True
    try:
        os.killpg(pgid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return process_visibility_limited()


def process_group_matches_state(pgid: int, state: dict) -> bool:
    members = process_group_members(pgid)
    if not members:
        return False
    try:
        leader_pid = int(state.get("pid", 0) or 0)
    except (TypeError, ValueError):
        leader_pid = 0
    if (
        leader_pid > 0
        and leader_pid in members
        and pid_matches_state(leader_pid, state)
    ):
        return True
    started_at = state.get("started_at")
    if not started_at:
        return True
    try:
        started_epoch = parse_utc(str(started_at)).timestamp()
    except ValueError:
        return True
    for member in members:
        proc_epoch = proc_start_epoch(member)
        if proc_epoch is not None and proc_epoch + 60 >= started_epoch:
            return True
    return False


def state_alive(state: dict) -> bool:
    pgid = state.get("pgid")
    if pgid:
        try:
            pgid_int = int(pgid)
            if process_group_alive(pgid_int) and process_group_matches_state(
                pgid_int, state
            ):
                return True
        except (TypeError, ValueError):
            pass
    try:
        pid = int(state["pid"])
    except (KeyError, TypeError, ValueError):
        return False
    if not pid_matches_state(pid, state):
        return False
    return pid_alive(pid)


def state_liveness_refuted_by_visible_process(state: dict) -> bool:
    """Return true when visible /proc state proves a recorded job is gone.

    A sandbox may hide the host PID namespace, so an invisible recorded PID is
    not enough to declare a job finished. A visible PID that does not match the
    recorded launch identity is different: that proves the PID was reused or is
    otherwise not the payload agentctl launched.
    """
    try:
        pid = int(state["pid"])
    except (KeyError, TypeError, ValueError):
        pid = 0
    if pid > 0 and Path(f"/proc/{pid}").exists():
        if proc_state(pid) == "Z":
            return True
        if not pid_matches_state(pid, state):
            return True

    pgid = state.get("pgid")
    if pgid:
        try:
            pgid_int = int(pgid)
        except (TypeError, ValueError):
            return False
        if process_group_members(pgid_int) and not process_group_matches_state(
            pgid_int, state
        ):
            return True
    return False


def refresh_state(state: dict) -> dict:
    state = apply_exit_status_record(state)
    if (
        state.get("status") == "finished"
        and state.get("returncode") == "unknown"
        and state_alive(state)
    ):
        # started_at is set only when the payload launches, so its absence
        # means the run was still queued behind --after.
        state["status"] = "running" if state.get("started_at") else "waiting"
        state.pop("finished_at", None)
        state.pop("returncode", None)
        update_state_files(state)
    # A queued (waiting) run's liveness is its _run-child wrapper: a dead
    # wrapper means the payload will never launch, so mark it finished rather
    # than leaving --after dependents blocked on it forever.
    if state.get("status") in ("running", "waiting") and not state_alive(state):
        if (
            process_visibility_limited()
            and not state_liveness_refuted_by_visible_process(state)
        ):
            state["_liveness_note"] = "process visibility limited; not marking finished"
            return state
        # Re-read before writing: `stop` may have just marked this run
        # stopped, and the derived liveness verdict must not clobber that
        # authoritative terminal state with finished/unknown.
        try:
            ondisk = read_json(Path(str(state.get("state_path") or "")))
        except Exception:
            ondisk = None
        if ondisk is not None:
            if ondisk.get("status") not in ("running", "waiting"):
                return apply_exit_status_record(ondisk)
            state = ondisk
        state["status"] = "finished"
        state["finished_at"] = utc_now()
        state["returncode"] = "unknown"
        update_state_files(state)
    return state


def apply_exit_status_record(state: dict) -> dict:
    exit_path = exit_status_path_for_state(state)
    if not exit_path.exists():
        return state
    try:
        record = read_json(exit_path)
    except Exception:
        return state
    rc = record.get("returncode")
    if rc in (None, ""):
        return state
    changed = False
    payload_pid = record.get("payload_pid")
    if payload_pid not in (None, "") and state.get("payload_pid") != payload_pid:
        state["payload_pid"] = payload_pid
        changed = True
    finished_at = str(
        record.get("finished_at") or state.get("finished_at") or utc_now()
    )
    if state.get("status") != "finished":
        state["status"] = "finished"
        changed = True
    if state.get("finished_at") != finished_at:
        state["finished_at"] = finished_at
        changed = True
    if state.get("returncode") != rc:
        state["returncode"] = rc
        changed = True
    if changed:
        update_state_files(state)
    return state


def command_string(argv: list[str]) -> str:
    return " ".join(shlex.quote(arg) for arg in argv)


def source_env_script(env: dict[str, str], script: str | Path) -> dict[str, str]:
    """Apply a shell env script without wrapping the monitored payload in a shell."""
    script_path = Path(script).expanduser()
    if not script_path.is_absolute():
        script_path = ROOT / script_path
    script_path = script_path.resolve()
    if not script_path.exists():
        raise SystemExit(f"missing env script: {script_path}")
    cmd = 'source "$1" >/dev/null 2>&1 && env -0'
    try:
        out = subprocess.check_output(
            ["/usr/bin/bash", "-c", cmd, "agentctl-source-env", str(script_path)],
            cwd=str(ROOT),
            env=env,
        )
    except subprocess.CalledProcessError as exc:
        raise SystemExit(
            f"failed to source env script {script_path}: exit {exc.returncode}"
        ) from exc
    updated = env.copy()
    for entry in out.split(b"\0"):
        if not entry:
            continue
        key, sep, value = entry.partition(b"=")
        if not sep:
            continue
        updated[key.decode("utf-8", errors="replace")] = value.decode(
            "utf-8", errors="replace"
        )
    return updated


def load_project_env(
    env: dict[str, str], spec: str = ""
) -> tuple[dict[str, str], dict | None]:
    """Fill missing child variables from a declarative project env file.

    The default file is ``ROOT / agentctl.env``. It is deliberately not a
    shell script: only full-line comments, blank lines, and ``KEY=VALUE`` are
    accepted. ``${AGENTCTL_ROOT}`` expands to the resolved invocation-project
    root so one tracked file works from differently located local and remote
    clones. Ambient variables remain authoritative; ``--source-env`` and
    ``--env`` are applied later and may override these defaults.
    """
    explicit = bool(spec)
    path = Path(spec or PROJECT_ENV_FILENAME).expanduser()
    if not path.is_absolute():
        path = ROOT / path
    path = path.resolve(strict=False)
    if not path.exists():
        if explicit:
            raise SystemExit(f"missing project env file: {path}")
        return env, None
    if not path.is_file():
        raise SystemExit(f"project env path is not a file: {path}")

    updated = env.copy()
    keys: list[str] = []
    seen: set[str] = set()
    try:
        project_env_bytes = path.read_bytes()
        lines = project_env_bytes.decode("utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        raise SystemExit(f"failed to read project env file {path}: {exc}") from exc
    for line_number, raw_line in enumerate(lines, 1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        key, sep, value = line.partition("=")
        key = key.strip()
        if not sep or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key):
            raise SystemExit(
                f"invalid project env entry {path}:{line_number}: expected KEY=VALUE"
            )
        if key in seen:
            raise SystemExit(
                f"duplicate project env key {key!r} at {path}:{line_number}"
            )
        seen.add(key)
        value = value.strip().replace("${AGENTCTL_ROOT}", str(ROOT))
        updated.setdefault(key, value)
        keys.append(key)
    return updated, {
        "path": str(path),
        "sha256": hashlib.sha256(project_env_bytes).hexdigest(),
        "keys": keys,
    }


def mark_state_finished(state: dict, returncode: int | str) -> dict:
    state["status"] = "finished"
    state["finished_at"] = state.get("finished_at") or utc_now()
    state["returncode"] = returncode
    update_state_files(state)
    return state


def terminate_state(state: dict, *, grace: float, reason: str | None = None) -> bool:
    pgid = int(state.get("pgid") or state["pid"])
    if not process_group_alive(pgid) and process_visibility_limited():
        return False
    try:
        os.killpg(pgid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    deadline = time.time() + grace
    while time.time() < deadline and process_group_alive(pgid):
        time.sleep(0.25)
    if process_group_alive(pgid):
        try:
            os.killpg(pgid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    state["status"] = "stopped"
    state["finished_at"] = utc_now()
    if reason:
        state["stop_reason"] = reason
    write_json(Path(state["state_path"]), state)
    write_json(current_path(state["job"]), state)
    return True


def reap_proc(proc: subprocess.Popen | None) -> int | None:
    if proc is None:
        return None
    rc = proc.poll()
    if rc is None:
        return None
    return proc.wait()


def git_value(args: list[str]) -> str:
    try:
        out = subprocess.check_output(
            ["git", *args], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
        )
    except Exception:
        return ""
    return out.strip()


class GitProbeError(SystemExit):
    """A required Git observation failed instead of producing evidence."""


def git_output(args: list[str], *, cwd: Path = ROOT, text: bool = True):
    try:
        return subprocess.check_output(
            ["git", *args], cwd=cwd, text=text, stderr=subprocess.PIPE
        )
    except subprocess.CalledProcessError as exc:
        detail = exc.stderr or ""
        if isinstance(detail, bytes):
            detail = detail.decode("utf-8", errors="replace")
        detail = detail.strip() or f"exit {exc.returncode}"
        raise GitProbeError(
            f"reproducibility guard: Git probe failed: "
            f"{shlex.join(['git', *args])}: {detail}"
        ) from exc
    except (OSError, subprocess.SubprocessError, UnicodeError) as exc:
        raise GitProbeError(
            f"reproducibility guard: Git probe failed: "
            f"{shlex.join(['git', *args])}: {exc}"
        ) from exc


def tracked_source_status(git_root: Path) -> str:
    # Aim records remain visible to ordinary Git status for later triage,
    # but every project root in this checkout shares their bookkeeping writes.
    pathspecs = [".", ":(top,glob,exclude)**/runs/aim/**"]
    return git_output(
        [
            "status",
            "--porcelain=v1",
            "--untracked-files=no",
            "--ignore-submodules=none",
            "--",
            *pathspecs,
        ],
        cwd=git_root,
    ).strip()


def committed_file_record(path: str | Path, *, git_root: Path, commit: str) -> dict:
    p = Path(path).expanduser().resolve()
    try:
        relative = p.relative_to(git_root)
    except ValueError as exc:
        raise SystemExit(
            f"reproducibility guard: source/control file is outside the Git checkout: {p}"
        ) from exc
    rel = relative.as_posix()
    tree_entry = git_output(
        ["ls-tree", "-z", commit, "--", rel], cwd=git_root, text=False
    )
    if not tree_entry:
        fingerprint = compute_sha256(p) if p.is_file() else "unavailable"
        raise SystemExit(
            "reproducibility guard: file bytes are not recoverable from the recorded "
            f"commit: {rel} sha256={fingerprint}"
        )
    try:
        blob = tree_entry.split(b"\t", 1)[0].split()[2].decode("ascii")
    except (IndexError, UnicodeError) as exc:
        raise GitProbeError(
            f"reproducibility guard: Git probe returned malformed ls-tree data for {rel}"
        ) from exc
    committed_bytes = git_output(["show", f"{commit}:{rel}"], cwd=git_root, text=False)
    current_sha256 = compute_sha256(p)
    committed_sha256 = hashlib.sha256(committed_bytes).hexdigest()
    if current_sha256 != committed_sha256:
        raise SystemExit(
            "reproducibility guard: file differs from the recorded commit: "
            f"{rel} current_sha256={current_sha256} committed_sha256={committed_sha256}"
        )
    st = p.stat()
    return {
        "path": str(p),
        "git_path": rel,
        "git_blob": blob,
        "sha256": current_sha256,
        "size": st.st_size,
    }


def pixi_roots_from_argv(argv: list[str]) -> set[Path]:
    roots: set[Path] = set()
    if not argv:
        return roots

    executable = Path(argv[0]).expanduser()
    if not executable.is_absolute():
        executable = ROOT / executable
    executable_parts = executable.resolve(strict=False).parts
    try:
        pixi_index = executable_parts.index(".pixi")
    except ValueError:
        pass
    else:
        roots.add(Path(*executable_parts[:pixi_index]))

    if Path(argv[0]).name != "pixi":
        return roots
    roots.add(ROOT)
    index = 1
    while index < len(argv):
        arg = argv[index]
        if arg == "--" or not arg.startswith("-"):
            break
        manifest_value = None
        if arg in {"--manifest-path", "-m"}:
            if index + 1 >= len(argv):
                break
            manifest_value = argv[index + 1]
            index += 1
        elif arg.startswith("--manifest-path="):
            manifest_value = arg.partition("=")[2]
        if manifest_value:
            manifest = Path(manifest_value).expanduser()
            if not manifest.is_absolute():
                manifest = ROOT / manifest
            roots.add(manifest.resolve(strict=False).parent)
        index += 1
    return roots


def foreign_environment_record(env_root: Path) -> dict:
    """Pin an environment outside the invoking checkout to its own repository.

    Only the declarative manifests are pinned: `pixi.toml` alone may carry
    version ranges, so the paired `pixi.lock` is what makes a rebuild
    reproducible. The realized `.pixi/envs/**` tree is derived state and is
    never commit-required nor hashed here.
    """
    try:
        git_root_text = git_output(
            ["rev-parse", "--show-toplevel"], cwd=env_root
        ).strip()
        commit = git_output(["rev-parse", "HEAD"], cwd=env_root).strip()
    except GitProbeError as exc:
        raise SystemExit(
            "reproducibility guard: selected environment is outside the project "
            f"checkout and is not pinned by a Git checkout of its own: {env_root}; "
            f"{exc.code}"
        ) from exc
    if not git_root_text or not commit:
        raise SystemExit(
            "reproducibility guard: selected environment is outside the project "
            f"checkout and its Git checkout has no committed HEAD: {env_root}"
        )
    git_root = Path(git_root_text).resolve()
    manifest = env_root / "pixi.toml"
    lock = env_root / "pixi.lock"
    if not manifest.is_file() or not lock.is_file():
        raise SystemExit(
            "reproducibility guard: a cross-repo Pixi environment requires both "
            f"{manifest} and {lock}"
        )
    try:
        files = {
            path.name: committed_file_record(path, git_root=git_root, commit=commit)
            for path in (manifest, lock)
        }
    except SystemExit as exc:
        raise SystemExit(
            f"reproducibility guard: cross-repo environment {env_root} is not "
            f"recoverable from its checkout {git_root} at HEAD {commit}: {exc.code}"
        ) from exc
    return {
        "env_root": str(env_root),
        "git_root": str(git_root),
        "git_branch": git_output(["branch", "--show-current"], cwd=git_root).strip(),
        "git_commit": commit,
        # Unrelated dirt in the environment's repository does not affect the
        # pinned manifests; record it, never refuse on it.
        "tracked_dirty_elsewhere": bool(tracked_source_status(git_root)),
        "files": files,
    }


def environment_control_paths(
    argv: list[str], project_env: dict | None, source_env: list[str]
) -> tuple[dict[str, Path], list[dict]]:
    paths: dict[str, Path] = {}
    foreign: list[dict] = []
    roots = {ROOT, *pixi_roots_from_argv(argv)}
    for env_root in sorted(roots):
        try:
            env_relative = env_root.relative_to(ROOT)
        except ValueError:
            foreign.append(foreign_environment_record(env_root))
            continue
        manifest = env_root / "pixi.toml"
        lock = env_root / "pixi.lock"
        if (env_root != ROOT or manifest.exists() or lock.exists()) and (
            not manifest.is_file() or not lock.is_file()
        ):
            raise SystemExit(
                "reproducibility guard: a selected Pixi environment requires both "
                f"{manifest} and {lock}"
            )
        for name in ENVIRONMENT_CONTROL_FILES:
            path = env_root / name
            if path.is_file():
                paths[f"environment:{env_relative / name}"] = path
    if project_env:
        paths["project_env"] = Path(project_env["path"])
    for index, spec in enumerate(source_env):
        path = Path(spec).expanduser()
        if not path.is_absolute():
            path = ROOT / path
        paths[f"source_env:{index}"] = path.resolve(strict=False)
    return paths, foreign


def build_source_snapshot(
    *,
    argv: list[str],
    script: dict,
    explicit_script: bool,
    project_env: dict | None,
    source_env: list[str],
) -> dict:
    try:
        git_root_text = git_output(["rev-parse", "--show-toplevel"]).strip()
        commit = git_output(["rev-parse", "HEAD"]).strip()
    except GitProbeError as exc:
        raise SystemExit(
            "reproducibility guard: tracked runs require a Git checkout with a "
            f"committed HEAD; {exc.code}"
        ) from exc
    if not git_root_text or not commit:
        raise SystemExit(
            "reproducibility guard: tracked runs require a Git checkout with a committed HEAD; "
            "an rsynced source tree without .git is not an experiment source"
        )
    git_root = Path(git_root_text).resolve()
    dirty = tracked_source_status(git_root)
    if dirty:
        first = dirty.splitlines()[0]
        raise SystemExit(
            "reproducibility guard: tracked/index changes must be committed before a tracked "
            f"run; first change: {first}"
        )
    untracked_python = git_output(
        ["ls-files", "--others", "--exclude-standard", "--", "*.py"], cwd=git_root
    ).splitlines()
    if untracked_python:
        preview = ", ".join(untracked_python[:5])
        suffix = (
            f" (+{len(untracked_python) - 5} more)" if len(untracked_python) > 5 else ""
        )
        raise SystemExit(
            "reproducibility guard: all non-ignored Python source must be committed before a "
            f"tracked run: {preview}{suffix}"
        )

    files, foreign_environments = environment_control_paths(
        argv, project_env, source_env
    )
    script_path = Path(script["path"]).resolve() if script.get("path") else None
    if script_path is not None:
        try:
            script_path.relative_to(git_root)
        except ValueError:
            if explicit_script or script_path.suffix in {".py", ".sh", ".bash", ".zsh"}:
                raise SystemExit(
                    "reproducibility guard: experiment scripts must be committed in the "
                    f"project checkout: {script_path}"
                )
        else:
            files["script"] = script_path

    records = {
        label: committed_file_record(path, git_root=git_root, commit=commit)
        for label, path in sorted(files.items())
    }
    if "script" in records:
        script.update({key: records["script"][key] for key in ("git_path", "git_blob")})
    snapshot = {
        "schema": "agentctl-source-v1",
        "status": "committed",
        "execution_guarantee": "admission-time-only",
        "execution_tree": "mutable-shared-worktree",
        "submission_check_at": utc_now(),
        "launch_check_at": "",
        "git_root": str(git_root),
        "git_branch": git_output(["branch", "--show-current"], cwd=git_root).strip(),
        "git_commit": commit,
        "tracked_clean": True,
        "untracked_python_count": 0,
        "files": records,
    }
    if foreign_environments:
        snapshot["foreign_environments"] = foreign_environments
    return snapshot


def revalidate_foreign_environment(record: dict) -> None:
    git_root = Path(record["git_root"])
    commit = record["git_commit"]
    if git_output(["rev-parse", "HEAD"], cwd=git_root).strip() != commit:
        raise SystemExit(
            "reproducibility guard: cross-repo environment checkout HEAD changed after "
            f"submission; refusing payload launch: {git_root}"
        )
    for expected in (record.get("files") or {}).values():
        current = committed_file_record(
            expected["path"], git_root=git_root, commit=commit
        )
        if (
            current["sha256"] != expected["sha256"]
            or current["git_blob"] != expected["git_blob"]
        ):
            raise SystemExit(
                "reproducibility guard: cross-repo environment manifest changed after "
                f"submission: {expected['path']}"
            )


def revalidate_source_snapshot(snapshot: dict) -> None:
    git_root = Path(snapshot["git_root"])
    commit = snapshot["git_commit"]
    if git_output(["rev-parse", "HEAD"], cwd=git_root).strip() != commit:
        raise SystemExit(
            "reproducibility guard: checkout HEAD changed after submission; refusing payload launch"
        )
    dirty = tracked_source_status(git_root)
    if dirty:
        raise SystemExit(
            "reproducibility guard: checkout became dirty after submission; refusing payload launch"
        )
    untracked_python = git_output(
        ["ls-files", "--others", "--exclude-standard", "--", "*.py"], cwd=git_root
    ).splitlines()
    if untracked_python:
        raise SystemExit(
            "reproducibility guard: untracked Python appeared after submission; refusing payload launch"
        )
    for expected in (snapshot.get("files") or {}).values():
        current = committed_file_record(
            expected["path"], git_root=git_root, commit=commit
        )
        if (
            current["sha256"] != expected["sha256"]
            or current["git_blob"] != expected["git_blob"]
        ):
            raise SystemExit(
                "reproducibility guard: source/control fingerprint changed after submission: "
                f"{expected['git_path']}"
            )
    for record in snapshot.get("foreign_environments") or []:
        revalidate_foreign_environment(record)


def machine_snapshot() -> dict:
    snapshot: dict = {
        "hostname": platform.node(),
        "architecture": platform.machine(),
        "kernel": platform.release(),
        "python_executable": sys.executable,
        "python_version": platform.python_version(),
    }
    os_release = Path("/etc/os-release")
    try:
        if os_release.is_file():
            values = {}
            for raw in os_release.read_text(
                encoding="utf-8", errors="replace"
            ).splitlines():
                key, sep, value = raw.partition("=")
                if sep and key in {"ID", "VERSION_ID", "PRETTY_NAME"}:
                    values[key.lower()] = value.strip().strip('"')
            if values:
                snapshot["os"] = values
    except OSError:
        pass
    try:
        output = subprocess.check_output(
            [
                "nvidia-smi",
                "--query-gpu=name,uuid,driver_version,memory.total",
                "--format=csv,noheader,nounits",
            ],
            text=True,
            stderr=subprocess.DEVNULL,
            timeout=3,
        )
        gpus = []
        for line in output.splitlines():
            fields = [field.strip() for field in line.split(",", 3)]
            if len(fields) == 4:
                gpus.append(
                    dict(
                        zip(
                            ("name", "uuid", "driver_version", "memory_total_mib"),
                            fields,
                        )
                    )
                )
        if gpus:
            snapshot["gpus"] = gpus
    except (OSError, subprocess.SubprocessError):
        pass
    cloud_init = Path("/run/cloud-init/instance-data.json")
    try:
        if cloud_init.is_file():
            metadata = (
                json.loads(cloud_init.read_text(encoding="utf-8"))
                .get("ds", {})
                .get("meta_data", {})
            )
            cloud = {
                key: metadata[key]
                for key in ("ami_id", "instance_id", "instance_type", "region")
                if metadata.get(key)
            }
            placement = metadata.get("placement") or {}
            if placement.get("availability-zone"):
                cloud["availability_zone"] = placement["availability-zone"]
            if cloud:
                snapshot["cloud"] = cloud
    except (OSError, UnicodeError, json.JSONDecodeError, AttributeError):
        pass
    return snapshot


# ---- Input/output declaration helpers ----

_INTERPRETERS = frozenset(
    {"bash", "sh", "zsh", "python", "python3", "perl", "node", "ruby", "Rscript"}
)


def compute_sha256(path: str | Path) -> str:
    """SHA256 of a file's bytes, hex-encoded. Streams in chunks (large tensors
    don't fit in memory). Caller is responsible for whether the cost is justified
    — used by --input-hash, --output-hash, and the script fingerprint."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def script_fingerprint(path: str | Path) -> dict:
    """Return the canonical script record {path, size, mtime, sha256} for an
    explicit --script override. Raises SystemExit if the path is missing or
    not a regular file."""
    p = Path(path).expanduser()
    if not p.is_absolute():
        p = ROOT / p
    p = p.resolve()
    if not p.exists() or not p.is_file():
        raise SystemExit(f"--script path not found or not a file: {p}")
    st = p.stat()
    return {
        "path": str(p),
        "size": st.st_size,
        "mtime": dt.datetime.fromtimestamp(st.st_mtime, tz=dt.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        ),
        "sha256": compute_sha256(p),
    }


def parse_keypath(spec: str, default_key: str = "primary") -> tuple[str, str]:
    """Parse 'KEY=PATH' or bare 'PATH' (then key defaults to default_key)."""
    if "=" in spec:
        key, _, path = spec.partition("=")
        if not key or not path:
            raise SystemExit(f"expected KEY=PATH, got {spec!r}")
        return key, path
    return default_key, spec


def resolve_artifact_path(path: str | Path) -> Path:
    """Resolve user-facing artifact paths relative to the project root.

    This preserves symlink identity for absolute paths and for paths that are
    already rooted under ROOT, matching the existing input/output provenance
    convention: `path` records what the user named; `realpath` records symlink
    resolution when it differs.
    """
    p = Path(path).expanduser()
    if not p.is_absolute():
        p = (ROOT / p).resolve(strict=False)
    return p


def stat_artifact(path: str | Path, *, missing_ok: bool = False) -> dict:
    """Return {path, [realpath], size, mtime, [is_dir]} for an existing path.
    Raises SystemExit if missing — declared inputs/outputs that don't exist
    indicate a usage error worth surfacing immediately."""
    p = resolve_artifact_path(path)
    abs_str = str(p)
    if not p.exists():
        if missing_ok:
            return {"path": abs_str, "status": "missing"}
        raise SystemExit(f"declared path does not exist: {p}")
    real = p.resolve()
    rec: dict = {"path": abs_str}
    if str(real) != abs_str:
        rec["realpath"] = str(real)
    st = p.stat()
    if p.is_dir():
        rec["is_dir"] = True
        # Recursive size; use the newest mtime in the tree as the effective mtime.
        total = 0
        newest = st.st_mtime
        for child in p.rglob("*"):
            try:
                cst = child.stat()
            except OSError:
                continue
            if child.is_file():
                total += cst.st_size
            newest = max(newest, cst.st_mtime)
        rec["size"] = total
        rec["mtime"] = dt.datetime.fromtimestamp(newest, tz=dt.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )
    else:
        rec["size"] = st.st_size
        rec["mtime"] = dt.datetime.fromtimestamp(
            st.st_mtime, tz=dt.timezone.utc
        ).strftime("%Y-%m-%dT%H:%M:%SZ")
    return rec


def input_record(
    key: str,
    path: str | Path,
    *,
    raw: bool = False,
    do_hash: bool = False,
    missing_ok: bool = False,
) -> dict:
    """Build the canonical state.inputs record for one declared input."""
    rec = stat_artifact(path, missing_ok=missing_ok)
    if raw:
        rec["raw"] = True
    if rec.get("status") == "missing":
        return rec
    if do_hash:
        try:
            rec["sha256"] = compute_sha256(rec["path"])
        except OSError as exc:
            print(
                f"warning: sha256 failed for input {key}={path}: {exc}", file=sys.stderr
            )
    src = resolve_input_source(rec["path"])
    if src:
        rec.update(src)
    return rec


_DECLARED_IO: dict[str, dict[str, str]] = {"inputs": {}, "outputs": {}}
_DECLARED_IO_REGISTERED = False


def _declared_io_path() -> Path | None:
    run_dir = os.environ.get("AGENTCTL_RUN_DIR", "").strip()
    if not run_dir:
        return None
    return Path(run_dir) / DECLARED_IO_FILENAME


def _write_declared_io_at_exit() -> None:
    path = _declared_io_path()
    if path is None:
        return
    payload = {kind: dict(values) for kind, values in _DECLARED_IO.items() if values}
    if not payload:
        return
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(f"{path.suffix}.tmp")
        tmp.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        tmp.replace(path)
    except Exception as exc:
        print(f"warning: failed to write {path}: {exc!r}", file=sys.stderr)


def _register_declared_io_writer() -> None:
    global _DECLARED_IO_REGISTERED
    if _DECLARED_IO_REGISTERED:
        return
    _DECLARED_IO_REGISTERED = True
    atexit.register(_write_declared_io_at_exit)


def _declare_artifact(kind: str, key: str, path: str | Path) -> None:
    if kind not in _DECLARED_IO:
        raise ValueError(f"unknown declaration kind: {kind!r}")
    if not isinstance(key, str) or not key:
        raise ValueError("declaration key must be a non-empty string")
    value = str(path)
    if not value:
        raise ValueError("declaration path must be non-empty")
    if _declared_io_path() is None:
        return
    _DECLARED_IO[kind][key] = value
    _register_declared_io_writer()


def declare_input(key: str, path: str | Path) -> None:
    """Declare a run input from inside a cooperating payload program.

    When the program is launched by agentctl, declarations are buffered and
    written at process exit to `$AGENTCTL_RUN_DIR/declared.json`. Outside an
    agentctl run this is a no-op, so cooperating programs do not need wrapper
    conditionals.
    """
    _declare_artifact("inputs", key, path)


def declare_output(key: str, path: str | Path) -> None:
    """Declare a run output from inside a cooperating payload program."""
    _declare_artifact("outputs", key, path)


def _declared_io_items(
    declared_file: Path, kind: str, payload: dict
) -> list[tuple[str, str]]:
    value = payload.get(kind, {})
    if value in ({}, None):
        return []
    if not isinstance(value, dict):
        raise ValueError(f"{declared_file}: {kind} must be an object")
    out: list[tuple[str, str]] = []
    for key, path in value.items():
        if not isinstance(key, str) or not key:
            raise ValueError(f"{declared_file}: {kind} key must be a non-empty string")
        if not isinstance(path, str) or not path:
            raise ValueError(
                f"{declared_file}: {kind}.{key} must be a non-empty path string"
            )
        out.append((key, path))
    return out


def _record_declaration_warning(state: dict, message: str) -> None:
    print(f"warning: {message}", file=sys.stderr)
    state.setdefault("declaration_warnings", [])
    state["declaration_warnings"].append(message)


def merge_declared_io(state: dict, declared_file: Path) -> None:
    """Merge cooperative `$AGENTCTL_RUN_DIR/declared.json` into run state."""
    if not declared_file.exists():
        return
    try:
        payload = json.loads(declared_file.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("top-level value must be an object")
        input_items = _declared_io_items(declared_file, "inputs", payload)
        output_items = _declared_io_items(declared_file, "outputs", payload)
    except Exception as exc:
        _record_declaration_warning(state, f"failed to read {declared_file}: {exc!r}")
        return

    inputs = state.setdefault("inputs", {})
    outputs = state.setdefault("outputs", {})
    for key, path in input_items:
        rec = input_record(key, path, missing_ok=True)
        existing = inputs.get(key)
        if existing and existing.get("path") != rec.get("path"):
            _record_declaration_warning(
                state,
                (
                    f"{declared_file}: input {key!r}={rec.get('path')!r} conflicts "
                    f"with existing {existing.get('path')!r}; keeping existing"
                ),
            )
            continue
        inputs[key] = {**(existing or {}), **rec}
    for key, path in output_items:
        rec = {"path": str(resolve_artifact_path(path))}
        existing = outputs.get(key)
        if existing and existing.get("path") != rec["path"]:
            _record_declaration_warning(
                state,
                (
                    f"{declared_file}: output {key!r}={rec['path']!r} conflicts "
                    f"with existing {existing.get('path')!r}; keeping existing"
                ),
            )
            continue
        outputs[key] = {**rec, **(existing or {})}


def finalize_finished_state(state: dict) -> dict:
    """Apply provenance finalization once a payload has a finished state."""
    run_dir_str = state.get("run_dir", "")
    if run_dir_str:
        merge_declared_io(state, Path(run_dir_str) / DECLARED_IO_FILENAME)
    # Stat declared outputs at completion. Missing outputs are recorded as such
    # rather than failing — a tracked job with a missing output is a real outcome
    # worth seeing in the record.
    outputs = state.get("outputs") or {}
    for key, info in outputs.items():
        p = Path(info.get("path", ""))
        if not p.exists():
            info["status"] = "missing"
            continue
        try:
            stat_rec = stat_artifact(info["path"])
            for k, v in stat_rec.items():
                if k != "path":
                    info[k] = v
        except Exception as exc:
            info["status"] = f"stat_failed: {exc}"
            continue
        # --output-hash: compute sha256 now that the file exists.
        if info.get("needs_hash"):
            try:
                info["sha256"] = compute_sha256(info["path"])
            except OSError as exc:
                print(
                    f"warning: sha256 failed for output {key}: {exc}", file=sys.stderr
                )
    # Cooperative propagation: program may have written facts to
    # $AGENTCTL_RUN_DIR/propagate.json during the run. Merge into the static
    # facts from --propagate-json (if any) — runtime values override static.
    if run_dir_str:
        propagate_file = Path(run_dir_str) / PROPAGATE_FILENAME
        if propagate_file.exists():
            try:
                cooperative = json.loads(propagate_file.read_text(encoding="utf-8"))
                if isinstance(cooperative, dict):
                    merged = dict(state.get("propagate") or {})
                    merged.update(cooperative)
                    state["propagate"] = merged
            except Exception as exc:
                print(
                    f"warning: failed to read {propagate_file}: {exc!r}",
                    file=sys.stderr,
                )
    # Plugin hook: opportunity to write per-output sidecars, mirror to live aim, etc.
    _call_hook("on_finish", state)
    return state


def resolve_input_source(input_path: str) -> dict | None:
    """Look for <input_path>.meta.json sidecar; return flat source-identity keys
    plus a small automatic one-deep recap (experiment, started_at, command_text,
    produced_path) read from the producer's dump record when available. Plus any
    producer-flagged propagation facts under `source_facts` (verbatim from the
    sidecar's `propagate` field, written via --propagate-json or
    $AGENTCTL_RUN_DIR/propagate.json). All keys are flat for aim queryability.

    Returns None if no sidecar exists or it lacks the required identity fields.
    Caller merges the returned dict into the input record."""
    sidecar = Path(f"{input_path}.meta.json")
    if not sidecar.exists():
        return None
    try:
        side = json.loads(sidecar.read_text(encoding="utf-8"))
    except Exception:
        return None
    run_id = side.get("agentctl_run_id")
    run_dump = side.get("run_dump")
    if not run_id or not run_dump:
        return None
    out: dict = {"source_run_id": run_id, "source_dump": run_dump}
    # Producer-flagged propagation: arbitrary JSON the producer wanted quoted at
    # the next consumer. Verbatim, no schema imposed by us.
    propagate = side.get("propagate")
    if isinstance(propagate, dict) and propagate:
        out["source_facts"] = propagate
    # Automatic one-deep recap: a small set of producer facts useful for human
    # review and aim grouping/filtering without forcing a separate DB read for
    # common queries. Read best-effort; the dump may be unreadable or absent.
    dump_path = Path(run_dump)
    if not dump_path.is_absolute():
        dump_path = (ROOT / dump_path).resolve(strict=False)
    if dump_path.exists():
        try:
            dump = json.loads(dump_path.read_text(encoding="utf-8"))
            params = dump.get("params") or {}
            identity = dump.get("identity") or {}
            if identity.get("experiment"):
                out["source_experiment"] = identity["experiment"]
            cmd = params.get("command") or {}
            if cmd.get("text"):
                out["source_command_text"] = cmd["text"]
            # source_origin: where the producer originally wrote this output.
            # Drift between source_origin and the consumer's `path` indicates
            # the file was moved/copied between runs.
            outputs_block = params.get("outputs") or {}
            output_key = side.get("output_key", "")
            if output_key and isinstance(outputs_block.get(output_key), dict):
                produced = outputs_block[output_key].get("path")
                if produced:
                    out["source_origin"] = produced
            elif params.get("output", {}).get("path"):
                out["source_origin"] = params["output"]["path"]
        except Exception:
            pass
    return out


def detect_script(argv: list[str]) -> dict | None:
    """Heuristic: first argv entry that's an existing file and not a known interpreter
    is taken as the script. Falls back to argv[0] if nothing else matches. Returns
    {path, size, mtime, sha256} or None if no suitable file found."""
    candidate: Path | None = None
    for a in argv:
        if not a or a.startswith("-"):
            continue
        bn = Path(a).name
        if bn in _INTERPRETERS:
            continue
        p = Path(a)
        if not p.is_absolute():
            p = ROOT / p
        try:
            if p.exists() and p.is_file():
                candidate = p
                break
        except OSError:
            # Inline programs and other non-path argv may exceed the host's
            # filename limit. They are not script candidates.
            continue
    if candidate is None:
        if not argv:
            return None
        p = Path(argv[0])
        if not p.is_absolute():
            p = ROOT / p
        try:
            usable_fallback = p.exists() and p.is_file()
        except OSError:
            usable_fallback = False
        if not usable_fallback:
            return None
        candidate = p
    st = candidate.stat()
    rec = {
        "path": str(candidate.resolve()),
        "size": st.st_size,
        "mtime": dt.datetime.fromtimestamp(st.st_mtime, tz=dt.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        ),
    }
    # Fingerprint scripts always (small files, cheap, very high reproducibility value).
    try:
        rec["sha256"] = compute_sha256(candidate)
    except OSError:
        pass
    return rec


def write_meta(state: dict) -> dict:
    output = state.get("output_path")
    if not output:
        return state
    sys.path.insert(0, str(CODE_ROOT))
    import artifact_meta

    launch_note = "Created by agentctl at launch; output-specific metadata may overwrite or extend this file."
    context_note = (state.get("context_note") or "").strip()
    depends_on = [slug(dep) for dep in state.get("depends_on", [])]
    setup = [
        ("job", state["job"]),
        ("job_serial", str(state.get("serial", ""))),
        ("run_id", state["run_id"]),
        ("launch_status", state["status"]),
    ]
    if state.get("runtime_estimate"):
        setup.append(("runtime_estimate", str(state["runtime_estimate"])))
    if state.get("source_env"):
        setup.append(
            ("source_env", ",".join(str(item) for item in state["source_env"]))
        )
    if state.get("project_env"):
        project_env = state["project_env"]
        setup.extend(
            [
                ("project_env", str(project_env["path"])),
                ("project_env_sha256", str(project_env["sha256"])),
                ("project_env_keys", ",".join(project_env["keys"])),
            ]
        )
    if depends_on:
        setup.append(("depends_on_jobs", ",".join(depends_on)))
    if state.get("aim_run_hash"):
        setup.append(("aim_run_hash", state["aim_run_hash"]))
    results: list[tuple[str, str]] = []
    machine = [
        ("git_branch", state.get("git_branch", "")),
        ("git_commit", state.get("git_commit", "")),
        (
            "source_status",
            str((state.get("source_snapshot") or {}).get("status", "")),
        ),
        ("started_at", state["started_at"]),
        ("pid", str(state["pid"])),
    ]
    machine_snapshot_record = state.get("machine_snapshot") or {}
    for key in ("hostname", "architecture", "kernel", "python_version"):
        if machine_snapshot_record.get(key):
            machine.append((key, str(machine_snapshot_record[key])))
    gpu_names = [gpu.get("name", "") for gpu in machine_snapshot_record.get("gpus", [])]
    if any(gpu_names):
        machine.append(("gpus", ",".join(name for name in gpu_names if name)))
    related = [("agentctl-state", Path(state["state_path"]))]
    for dep in depends_on:
        dep_current = current_path(dep)
        if not dep_current.exists():
            continue
        try:
            dep_state = read_json(dep_current)
        except Exception:
            continue
        related.append((f"depends-on-state:{dep}", Path(dep_state["state_path"])))
        dep_output = dep_state.get("output_path")
        if dep_output:
            related.append((f"depends-on-output:{dep}", Path(dep_output)))
    notes = [launch_note]
    if context_note:
        notes.append(f"pre-run-note: {context_note}")

    def _build():
        return artifact_meta.build_meta_markdown(
            output_path=output,
            title=f"{state['job']} {state['run_id']}",
            cwd=Path(state["cwd"]),
            command=command_string(state["argv"]),
            setup=setup,
            results=results,
            machine=machine,
            plan=[],
            notes=notes,
            inputs=[],
            related=related,
        )

    meta = _build()
    for p in _PLUGINS:
        fn = getattr(p, "on_meta_built", None)
        if fn is None:
            continue
        try:
            new = fn(
                state,
                meta,
                output_path=output,
                log_path=state["log_path"],
                build_meta=_build,
            )
        except Exception as exc:
            print(
                f"warning: plugin {p.__name__} on_meta_built failed: {exc}",
                file=sys.stderr,
            )
            continue
        if new is not None:
            meta = new
    Path(f"{output}.meta.md").parent.mkdir(parents=True, exist_ok=True)
    Path(f"{output}.meta.md").write_text(meta, encoding="utf-8")
    return state


def latest_producer_for_output(output: Path) -> dict | None:
    """The latest-run state among jobs declaring `output` as a declared output.

    Scans jobs/*/current.json (each job's latest run). A queued or running
    producer wins over terminal ones; ties break to the most recent
    queued_at/started_at. Returns the raw state (caller refreshes if needed).
    """
    target = Path(output).resolve(strict=False)
    if not JOBS.is_dir():
        return None
    live: list[dict] = []
    terminal: list[dict] = []
    for current in JOBS.glob("*/current.json"):
        try:
            state = read_json(current)
        except Exception:
            continue
        declared = [state.get("output_path") or ""]
        outputs = state.get("outputs")
        if isinstance(outputs, dict):
            declared.extend(
                rec.get("path", "") for rec in outputs.values() if isinstance(rec, dict)
            )
        if any(raw and Path(raw).resolve(strict=False) == target for raw in declared):
            bucket = live if state.get("status") in ("waiting", "running") else terminal
            bucket.append(state)
    for bucket in (live, terminal):
        if bucket:
            bucket.sort(
                key=lambda s: str(s.get("queued_at") or s.get("started_at") or "")
            )
            return bucket[-1]
    return None


def live_producer_for_output(output: Path) -> dict | None:
    """The queued/running producer of `output`, liveness-refreshed, if any."""
    state = latest_producer_for_output(output)
    if state is None or state.get("status") not in ("waiting", "running"):
        return None
    state = refresh_state(state)
    return state if state.get("status") in ("waiting", "running") else None


def resolve_after_target(spec: str) -> dict:
    job_path = current_path(spec)
    if job_path.exists():
        return {"kind": "job", "spec": spec, "job": slug(spec)}

    raw = Path(spec).expanduser()
    candidates: list[Path] = []
    if raw.is_absolute():
        candidates.append(raw)
    else:
        candidates.append((ROOT / raw).resolve(strict=False))
    for candidate in list(candidates):
        candidates.append(running_marker_path(candidate))

    seen: set[Path] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        marker = (
            candidate
            if str(candidate).endswith(".running.md")
            else running_marker_path(candidate)
        )
        output = (
            Path(str(marker)[: -len(".running.md")])
            if str(marker).endswith(".running.md")
            else candidate
        )
        # A queued producer job (no marker until its payload launches, e.g.
        # itself waiting behind --after) also makes an artifact target real.
        if (
            marker.exists()
            or completion_sidecar(output) is not None
            or live_producer_for_output(output) is not None
        ):
            return {
                "kind": "running_marker",
                "spec": spec,
                "marker_path": str(marker),
                "output_path": str(output),
            }

    raise SystemExit(
        f"--after target not found as an agentctl job, .running.md artifact, "
        f"or declared output of a queued/running job: {spec}"
    )


def after_target_done(target: dict) -> tuple[bool, int, str]:
    kind = target.get("kind")
    if kind == "job":
        dep_state = load_job(str(target["job"]))
        status = dep_state.get("status", "")
        if status in {"running", "waiting"}:
            return (
                False,
                0,
                f"job={dep_state['job']} status={status} elapsed={elapsed_estimate_text(dep_state)}",
            )
        if status == "finished" and dep_state.get("returncode") in (
            None,
            "",
            "unknown",
        ):
            finished_at = dep_state.get("finished_at")
            try:
                finished_age = time.time() - parse_utc(str(finished_at)).timestamp()
            except (TypeError, ValueError):
                finished_age = 0.0
            if finished_age < DEFAULT_WAIT_AFTER_UNKNOWN_GRACE_S:
                return (
                    False,
                    0,
                    f"job={dep_state['job']} status=finished returncode=unknown settling",
                )
        rc = status_returncode_exit_code(dep_state)
        if status != "finished":
            # stopped (or an unrecognized terminal state) is not a clean exit:
            # fail the chain rather than launching a payload whose
            # precondition never completed.
            rc = rc or 1
        if rc != 0:
            return (
                True,
                rc,
                f"job={dep_state['job']} ended status={status} returncode={dep_state.get('returncode')}",
            )
        return (
            True,
            0,
            f"job={dep_state['job']} ended status={status} returncode={dep_state.get('returncode', '')}",
        )

    if kind == "running_marker":
        marker = Path(str(target["marker_path"]))
        output = Path(str(target["output_path"]))
        if not marker.exists():
            # No live marker: defer to the producing job when one is known.
            # A queued/running producer blocks (a stale completion sidecar
            # from an earlier run must not release the dependent); a producer
            # that ended without a clean finish fails the chain.
            producer = latest_producer_for_output(output)
            if producer is not None:
                producer = refresh_state(producer)
                status = producer.get("status", "")
                if status in ("waiting", "running"):
                    return (
                        False,
                        0,
                        (
                            f"output={output} producer job={producer['job']} status={status} "
                            f"elapsed={elapsed_estimate_text(producer)}"
                        ),
                    )
                rc = status_returncode_exit_code(producer)
                if status != "finished":
                    rc = rc or 1
                if rc != 0:
                    return (
                        True,
                        rc,
                        (
                            f"producer job={producer['job']} ended status={status} "
                            f"returncode={producer.get('returncode')} out={output}"
                        ),
                    )
                sidecar = completion_sidecar(output)
                return (
                    True,
                    0,
                    (
                        f"producer job={producer['job']} finished returncode=0 "
                        f"sidecar={sidecar or 'none'} out={output}"
                    ),
                )
            sidecar = completion_sidecar(output)
            if sidecar is not None:
                return True, 0, f"marker gone: {marker} sidecar={sidecar}"
            return (
                True,
                1,
                f"marker gone without completion sidecar: {marker} out={output}",
            )
        fields = marker_fields(marker)
        output = output_for_marker(marker, fields)
        sidecar = completion_sidecar(output)
        pid_state = marker_pid_status(fields)
        if sidecar is not None and pid_state != "running":
            return True, 0, f"marker completed: {marker} sidecar={sidecar}"
        if pid_state == "running":
            return (
                False,
                0,
                f"marker={marker} pid={fields.get('pid', '') or '?'} running",
            )
        return (
            True,
            1,
            f"marker interrupted: {marker} pid={fields.get('pid', '') or '?'} out={output}",
        )

    return True, 1, f"unknown --after target kind: {kind!r}"


def wait_for_after_targets(state: dict) -> int:
    targets = state.get("wait_after") or []
    if not targets:
        return 0
    poll = float(state.get("wait_after_poll") or 10.0)
    timeout = float(state.get("wait_after_timeout") or 0.0)
    heartbeat = float(state.get("wait_after_heartbeat") or 30.0)
    deadline = time.time() + timeout if timeout > 0 else None
    next_report = 0.0
    while True:
        pending: list[str] = []
        for target in targets:
            done, rc, detail = after_target_done(target)
            if done and rc != 0:
                print(f"[wait-after] failed: {detail}", file=sys.stderr, flush=True)
                return rc
            if not done:
                pending.append(detail)
        if not pending:
            return 0
        now = time.time()
        if heartbeat > 0 and (next_report == 0.0 or now >= next_report):
            headline = "waiting on " + "; ".join(pending)
            if state.get("headline_path"):
                write_headline(Path(state["headline_path"]), headline)
            print(f"[wait-after] {headline}", flush=True)
            next_report = now + heartbeat
        if deadline is not None and now >= deadline:
            print(
                f"timeout waiting for --after targets: {'; '.join(pending)}",
                file=sys.stderr,
            )
            return 1
        time.sleep(poll)


def mark_wait_failed(
    state_path: Path, current: Path, exit_status_path: Path, rc: int
) -> None:
    finished_at = utc_now()
    record = {"finished_at": finished_at, "returncode": rc}
    write_json(exit_status_path, record)
    try:
        state = read_json(state_path)
        state["status"] = "finished"
        state["finished_at"] = finished_at
        state["returncode"] = rc
        update_state_files(state)
        write_json(current, state)
    except Exception as exc:
        print(
            f"warning: wait-after failure state update failed: {exc!r}", file=sys.stderr
        )


def start(args: argparse.Namespace) -> int:
    if not args.argv:
        raise SystemExit("missing command after --")
    if args.watch and args.after:
        raise SystemExit(
            "--after is not supported with --watch; start queued work detached, then watch the job"
        )
    runtime_estimate = ""
    runtime_estimate_seconds = 0
    if args.runtime_estimate:
        runtime_estimate_seconds = parse_duration_seconds(args.runtime_estimate)
        runtime_estimate = format_duration(runtime_estimate_seconds)
    if args.wait_max_memory_used is not None and not args.after:
        wait_rc = wait_for_gpu_memory(
            gpu=args.wait_gpu,
            max_memory_used=args.wait_max_memory_used,
            poll=args.wait_poll,
            timeout=args.wait_timeout,
            heartbeat=getattr(args, "wait_heartbeat", None),
        )
        if wait_rc != 0:
            return wait_rc
    wait_after = [resolve_after_target(spec) for spec in (args.after or [])]
    job = slug(args.job)
    rid = args.run_id or run_id()
    # run_id() resolution is one second; consecutive starts (e.g. quick restart)
    # would otherwise collide on the same run_dir and silently overwrite the
    # prior run's state. Suffix on collision to keep records disjoint.
    base_rid = rid
    suffix = 0
    while (RUNS / job / rid).exists():
        suffix += 1
        rid = f"{base_rid}-{suffix}"
    serial = next_serial(job)
    launch_name = instance_name(job, serial)
    run_dir = RUNS / job / rid
    run_dir.mkdir(parents=True, exist_ok=True)
    log_path = Path(args.log).expanduser() if args.log else run_dir / "run.log"
    if not log_path.is_absolute():
        log_path = ROOT / log_path
    headline_path = run_dir / "headline.txt"

    # Declared outputs: --output KEY=PATH (repeatable; bare PATH → key="primary").
    # --output-arg also appends --KEY=PATH to the payload. --output-hash flags
    # the same declaration for sha256 at completion.
    declared_outputs: dict = {}
    output_translations: list[tuple[str, str]] = []
    primary_output_path: Path | None = None

    def _record_output(spec: str, *, translate: bool, do_hash: bool) -> None:
        nonlocal primary_output_path
        if translate and "=" not in spec:
            raise SystemExit(f"--output-arg requires KEY=PATH, got {spec!r}")
        key, path = parse_keypath(spec, default_key="primary")
        p = Path(path).expanduser()
        if not p.is_absolute():
            p = (ROOT / p).resolve(strict=False)
        prior = declared_outputs.get(key)
        if prior is not None and prior["path"] != str(p):
            raise SystemExit(
                f"conflicting output declarations for {key!r}: "
                f"{prior['path']!r} != {str(p)!r}"
            )
        rec = prior or {"path": str(p)}
        if translate and not rec.get("arg"):
            rec["arg"] = True
            output_translations.append((key, str(p)))
        if do_hash:
            rec["needs_hash"] = True
        declared_outputs[key] = rec
        if primary_output_path is None:
            primary_output_path = p

    for spec in args.output or []:
        _record_output(spec, translate=False, do_hash=False)
    for spec in args.output_arg or []:
        _record_output(spec, translate=True, do_hash=False)
    for spec in args.output_hash or []:
        _record_output(spec, translate=False, do_hash=True)
    output_path = primary_output_path
    if output_path is None:
        plugin_default = _first_hook("default_output_path", args, run_dir)
        if plugin_default is not None:
            output_path = plugin_default

    # Declared inputs: --input KEY=PATH (translated to --KEY=PATH appended),
    # --input-raw KEY=PATH (no translation), --input-hash KEY=PATH (translated + sha256).
    declared_inputs: dict = {}
    input_translations: list[tuple[str, str]] = []

    def _record_input(key: str, path: str, raw: bool, do_hash: bool) -> None:
        rec = input_record(key, path, raw=raw, do_hash=do_hash)
        declared_inputs[key] = rec
        if not raw:
            input_translations.append((key, rec["path"]))

    for spec in args.input or []:
        key, path = parse_keypath(spec)
        _record_input(key, path, raw=False, do_hash=False)
    for spec in args.input_raw or []:
        key, path = parse_keypath(spec)
        _record_input(key, path, raw=True, do_hash=False)
    for spec in args.input_hash or []:
        key, path = parse_keypath(spec)
        _record_input(key, path, raw=False, do_hash=True)

    state_path = run_dir / "state.json"
    exit_status_path = run_dir / "exit-status.json"
    launch_gpu_stats = None
    if args.gpu_patience > 0:
        try:
            launch_gpu_stats = query_gpu_stats(args.watch_gpu)
        except Exception as exc:
            print(
                f"warning: failed to snapshot launch gpu stats for gpu={args.watch_gpu}: {exc}",
                file=sys.stderr,
            )

    env = os.environ.copy()
    project_env = None
    if not args.no_project_env:
        env, project_env = load_project_env(env, args.project_env)
    env.setdefault("PYTHONUNBUFFERED", "1")
    # Count-down-once: mark the child as one hop deeper into an agentctl launch
    # so neither the job nor any agentctl it shells adopts the launching agent's
    # session id (agent_session_id() ignores it at depth > 0). A job is not an
    # agent and must not refresh or masquerade as that agent's active-sessions
    # entry — without rewriting the harness's own ambient session var.
    try:
        _launch_depth = int(env.get(LAUNCH_DEPTH_ENV, "0") or "0")
    except ValueError:
        _launch_depth = 0
    env[LAUNCH_DEPTH_ENV] = str(_launch_depth + 1)
    # Inherit parent run id (if this agentctl invocation is itself running under
    # another agentctl-tracked run) so the child record can reference parent_run.
    parent_run_id = env.get("AGENTCTL_PARENT_RUN_ID", "").strip()
    env.update(
        {
            "AGENTCTL_JOB": job,
            "AGENTCTL_RUN_ID": rid,
            "AGENTCTL_RUN_DIR": str(run_dir),
            "AGENTCTL_MODE": args.mode,
            "AGENTCTL_HEADLINE_FILE": str(headline_path),
            # Set our own run_id as AGENTCTL_PARENT_RUN_ID for any child agentctl
            # invocations during this run — they'll record us as their parent.
            "AGENTCTL_PARENT_RUN_ID": rid,
        }
    )
    if output_path is not None:
        env["AGENTCTL_OUTPUT"] = str(output_path)
    if args.input_file:
        env["AGENTCTL_INPUT_FILE"] = str(Path(args.input_file).expanduser().resolve())
    if args.gpus:
        env["CUDA_VISIBLE_DEVICES"] = args.gpus
    explicit_env: dict[str, str] = {}
    for item in args.env:
        key, separator, value = item.partition("=")
        if not key or not separator:
            raise SystemExit(f"expected --env KEY=VALUE, got {item!r}")
        explicit_env[key] = value

    # Build the final argv for the child: user's argv + translated I/O flags.
    final_argv = list(args.argv)
    for key, path in input_translations:
        final_argv.append(f"--{key}={path}")
    for key, path in output_translations:
        final_argv.append(f"--{key}={path}")

    # Producer-flagged propagation (static at launch). Run-time-computed facts
    # arrive via $AGENTCTL_RUN_DIR/propagate.json (read at completion in run_child).
    propagate: dict = {}
    if args.propagate_json:
        try:
            parsed = json.loads(args.propagate_json)
            if not isinstance(parsed, dict):
                raise SystemExit(
                    f"--propagate-json must be a JSON object, got {type(parsed).__name__}"
                )
            propagate = parsed
        except (json.JSONDecodeError, ValueError) as exc:
            raise SystemExit(f"--propagate-json failed to parse: {exc}")

    # Script: explicit --script PATH override wins; otherwise heuristic on argv.
    if args.script:
        script_rec = script_fingerprint(args.script)
        script_rec["selection"] = "explicit"
    else:
        script_rec = detect_script(final_argv) or {}
        if script_rec:
            script_rec["selection"] = "detected"

    source_snapshot = None
    if not getattr(args, "no_aim", False):
        source_snapshot = build_source_snapshot(
            argv=final_argv,
            script=script_rec,
            explicit_script=bool(args.script),
            project_env=project_env,
            source_env=list(args.source_env),
        )
    for script in args.source_env:
        env = source_env_script(env, script)
    env.update(explicit_env)

    # Pre-launch state: canonical fields plugins can read/extend.
    state = {
        "context_note": args.context_note,
        "pre_run_note": args.context_note,
        "depends_on": [slug(dep) for dep in args.depends_on],
        "exit_status_path": str(exit_status_path),
        "argv": final_argv,
        "cwd": str(ROOT),
        "git_branch": (source_snapshot or {}).get("git_branch")
        or git_value(["branch", "--show-current"]),
        "git_commit": (source_snapshot or {}).get("git_commit")
        or git_value(["rev-parse", "HEAD"]),
        "headline_path": str(headline_path),
        "inputs": declared_inputs,
        "user_argv": list(args.argv),
        "job": job,
        "launch_name": launch_name,
        "log_path": str(log_path),
        "meta_path": str(Path(f"{output_path}.meta.md"))
        if output_path is not None
        else "",
        "mode": args.mode,
        "output_path": str(output_path) if output_path is not None else "",
        "outputs": declared_outputs,
        "parent_run": parent_run_id,
        "propagate": propagate,
        "run_dir": str(run_dir),
        "run_id": rid,
        "runtime_estimate": runtime_estimate,
        "runtime_estimate_seconds": runtime_estimate_seconds,
        "machine_snapshot": machine_snapshot(),
        "project_env": project_env,
        "script": script_rec,
        "serial": serial,
        "source_env": list(args.source_env),
        "source_snapshot": source_snapshot,
        "state_path": str(state_path),
    }
    if wait_after:
        state["wait_after"] = wait_after
        state["wait_after_specs"] = list(args.after or [])
        state["wait_after_poll"] = args.after_poll
        state["wait_after_heartbeat"] = args.after_heartbeat
        state["wait_after_timeout"] = args.after_timeout
        state["wait_on"] = ",".join(target["spec"] for target in wait_after)
        if args.wait_max_memory_used is not None:
            state["deferred_wait_gpu"] = args.wait_gpu
            state["deferred_wait_max_memory_used"] = args.wait_max_memory_used
            state["deferred_wait_poll"] = args.wait_poll
            state["deferred_wait_heartbeat"] = args.wait_heartbeat
            state["deferred_wait_timeout"] = args.wait_timeout
    _call_hook("on_start", args, state, env)

    log_path.parent.mkdir(parents=True, exist_ok=True)
    if args.context_note:
        write_headline(headline_path, args.context_note)
    # The detached wrapper owns terminal recording; a watcher is disposable.
    child_argv = [
        sys.executable,
        str(Path(__file__).resolve()),
        "_run-child",
        "--state-path",
        str(state_path),
        "--current-path",
        str(current_path(job)),
        "--exit-status-path",
        str(exit_status_path),
        "--",
        *final_argv,
    ]
    log = log_path.open("ab")
    proc = subprocess.Popen(
        child_argv,
        cwd=str(ROOT),
        env=env,
        stdout=log,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    log.close()

    state.update(
        {
            "pgid": proc.pid,
            "pid": proc.pid,
            "pid_cmdline": proc_cmdline(proc.pid) or "",
            "pid_namespace": current_pid_namespace(),
            "pid_start_ticks": proc_start_ticks(proc.pid) or 0,
            "status": "waiting" if wait_after else "running",
            "meta": bool(args.meta),
        }
    )
    if wait_after:
        state["queued_at"] = utc_now()
    else:
        state["started_at"] = utc_now()
    if launch_gpu_stats is not None:
        state["launch_gpu_stats"] = launch_gpu_stats
    update_state_files(state)
    print(f"started {launch_name} job={job} serial={serial} run={rid} pid={proc.pid}")
    print(f"log: {log_path}")
    refresh_active_register(
        summary=f"agentctl {args.mode} {launch_name}: {command_string(final_argv)}",
        note=f"agentctl: started {launch_name} run={rid}",
    )
    # Piggybacked on this write-path verb (listing stays read-only): archive
    # stale active/ entries so the hot peer-check `find` never scans an
    # unbounded corpse pile in a project that launches jobs.
    sweep_stale_entries(ACTIVE_STALE_MINUTES, quiet=True)
    if args.watch:
        try:
            return watch(
                argparse.Namespace(
                    job=job,
                    poll=args.watch_poll,
                    heartbeat=args.watch_heartbeat,
                    heartbeat_gpu=args.watch_heartbeat_gpu,
                    tail=args.watch_tail,
                    gpu=args.watch_gpu,
                    gpu_poll=args.watch_gpu_poll,
                    gpu_patience=args.gpu_patience,
                    notify_gpu_idle=args.watch_notify_gpu_idle,
                    notify_max_memory_used=args.watch_notify_max_memory_used,
                    notify_max_power_draw=args.watch_notify_max_power_draw,
                ),
                proc=proc,
            )
        finally:
            reap_proc(proc)
    return 0


def run_child(args: argparse.Namespace) -> int:
    argv = list(args.argv)
    if argv and argv[0] == "--":
        argv = argv[1:]
    if not argv:
        raise SystemExit("missing command after --")
    state_path = Path(args.state_path)
    current = Path(args.current_path)
    exit_status_path = Path(args.exit_status_path)
    try:
        state = read_json(state_path)
        wait_rc = wait_for_after_targets(state)
    except Exception as exc:
        print(
            f"warning: wait-after failed before payload launch: {exc!r}",
            file=sys.stderr,
        )
        wait_rc = 1
    if wait_rc != 0:
        mark_wait_failed(state_path, current, exit_status_path, wait_rc)
        return wait_rc
    try:
        state = read_json(state_path)
        if state.get("deferred_wait_max_memory_used") is not None:
            wait_rc = wait_for_gpu_memory(
                gpu=int(state.get("deferred_wait_gpu") or 0),
                max_memory_used=int(state["deferred_wait_max_memory_used"]),
                poll=float(state.get("deferred_wait_poll") or 10.0),
                timeout=float(state.get("deferred_wait_timeout") or 0.0),
                heartbeat=float(state.get("deferred_wait_heartbeat") or 10.0),
            )
            if wait_rc != 0:
                mark_wait_failed(state_path, current, exit_status_path, wait_rc)
                return wait_rc
    except Exception as exc:
        print(
            f"warning: deferred wait-gpu failed before payload launch: {exc!r}",
            file=sys.stderr,
        )
        mark_wait_failed(state_path, current, exit_status_path, 1)
        return 1
    try:
        state = read_json(state_path)
        source_snapshot = state.get("source_snapshot")
        if source_snapshot:
            revalidate_source_snapshot(source_snapshot)
            source_snapshot["launch_check_at"] = utc_now()
            state["source_snapshot"] = source_snapshot
            write_json(state_path, state)
            write_json(current, state)
    except (OSError, KeyError, TypeError, ValueError, SystemExit) as exc:
        detail = exc.code if isinstance(exc, SystemExit) else str(exc)
        print(
            f"reproducibility guard failed before payload launch: {detail}",
            file=sys.stderr,
        )
        mark_wait_failed(state_path, current, exit_status_path, 2)
        return 2
    # Pre-launch: write meta + dump record now (serialized inside the child so
    # there's no race between start()'s post-Popen writes and our completion read).
    try:
        state = read_json(state_path)
        if state.get("status") == "waiting":
            state["status"] = "running"
            state["started_at"] = utc_now()
            state.pop("returncode", None)
            state.pop("finished_at", None)
        if state.get("meta", True) and state.get("output_path"):
            state = write_meta(state)
        update_state_files(state)
    except Exception as exc:
        print(f"warning: pre-launch meta write failed: {exc!r}", file=sys.stderr)
    proc = subprocess.Popen(argv, cwd=str(ROOT))
    payload_pid = proc.pid
    try:
        state = read_json(state_path)
        state["payload_pid"] = payload_pid
        update_state_files(state)
    except Exception:
        pass
    rc = proc.wait()
    record = {
        "finished_at": utc_now(),
        "payload_pid": payload_pid,
        "returncode": rc,
    }
    write_json(exit_status_path, record)
    try:
        state = read_json(state_path)
        state["payload_pid"] = payload_pid
        state["status"] = "finished"
        state["finished_at"] = record["finished_at"]
        state["returncode"] = rc
        state = finalize_finished_state(state)
        write_json(state_path, state)
        write_json(current, state)
    except Exception as exc:
        print(f"warning: post-completion update failed: {exc!r}", file=sys.stderr)
    return rc


def load_job(job: str) -> dict:
    path = current_path(job)
    if not path.exists():
        raise SystemExit(f"unknown job: {job}")
    return refresh_state(read_json(path))


def state_sort_key(state: dict) -> tuple[str, str, str]:
    finished_at = str(state.get("finished_at") or "")
    started_at = str(state.get("started_at") or "")
    return (finished_at, started_at, str(state.get("run_id") or ""))


def status_state_payload(state: dict, args: argparse.Namespace) -> dict:
    if bool(getattr(args, "full", False)):
        payload = dict(state)
        payload["elapsed"] = elapsed_estimate_text(state)
        payload["failed"] = state_failed(state)
    else:
        payload = {
            "job": state["job"],
            "run_id": state.get("run_id"),
            "status": state.get("status"),
            "elapsed": elapsed_estimate_text(state),
            "returncode": state.get("returncode"),
            "log_path": state.get("log_path"),
        }
    if args.tail:
        path = Path(state["log_path"])
        if path.exists():
            payload["tail"] = path.read_text(
                encoding="utf-8", errors="replace"
            ).splitlines()[-args.tail :]
        else:
            payload["tail"] = []
            payload["tail_error"] = f"missing log: {path}"
    return payload


def status(args: argparse.Namespace) -> int:
    structured = getattr(args, "format", None) is not None or bool(
        getattr(args, "full", False)
    )
    fmt = _resolve_acli_format(args) if structured else None
    if args.settle > 0:
        time.sleep(args.settle)
    states: list[dict] = []
    groups: list[tuple[str, list[dict]]] | None = None
    if args.job:
        states = [load_job(args.job)]
    else:
        for path in sorted(JOBS.glob("*/current.json")):
            states.append(refresh_state(read_json(path)))
        states.sort(key=state_sort_key, reverse=True)
        if getattr(args, "failed_only", False):
            states = [state for state in states if state_failed(state)]
            if args.recent and args.recent > 0:
                states = states[: args.recent]
        elif getattr(args, "live_only", False):
            states = [state for state in states if state_live(state)]
        elif getattr(args, "where", False) and not getattr(args, "all_jobs", False):
            live = [state for state in states if state_live(state)]
            min_elapsed = max(0, getattr(args, "completed_min_elapsed", 0))
            completed = [
                state
                for state in states
                if state.get("status") == "finished"
                and (
                    (elapsed_seconds(state) or 0) >= min_elapsed or state_failed(state)
                )
            ]
            if args.recent and args.recent > 0:
                completed_n = args.recent
            elif args.completed_recent is not None:
                completed_n = args.completed_recent
            else:
                completed_n = args.show_last - len(live)
            completed = completed[: max(0, completed_n)]
            groups = [("Live Jobs", live), ("Recent Finished Jobs", completed)]
            states = [*live, *completed]
        elif args.recent and args.recent > 0:
            states = states[: args.recent]
    if fmt is not None:
        payload = {
            "kind": "job_status" if args.job else "job_list",
            "count": len(states),
            "jobs": [status_state_payload(state, args) for state in states],
        }
        if groups is not None:
            payload["groups"] = [
                {"name": title.lower().replace(" ", "_"), "count": len(group)}
                for title, group in groups
            ]
        acli.emit(payload, fmt)
        return 0
    if groups is not None:
        for group_idx, (title, group_states) in enumerate(groups):
            if group_idx:
                print()
            print(f"{title}:")
            if not group_states:
                print("  none")
                continue
            for idx, state in enumerate(group_states):
                if idx:
                    print("\n---\n")
                print_status_state(state, args)
        return 0
    if not states:
        print("no jobs")
        return 0
    for idx, state in enumerate(states):
        if idx:
            print("\n---\n")
        print_status_state(state, args)
    return 0


def print_status_state(state: dict, args: argparse.Namespace) -> None:
    headline = ""
    hp = Path(state.get("headline_path", ""))
    if hp.exists():
        headline = read_headline(hp)
    if not headline:
        headline = normalize_headline_text(state.get("context_note", ""))
    bits = [
        state["job"],
        f"serial={state.get('serial', '')}",
        state["run_id"],
        state["status"],
        f"elapsed={elapsed_estimate_text(state)}",
        f"pid={state.get('pid', '')}",
        f"pgid={state.get('pgid', '')}",
        f"log={state.get('log_path', '')}",
    ]
    if state_failed(state):
        bits.append("FAILED")
    if status_returncode_text(state):
        bits.append(f"returncode={status_returncode_text(state)}")
    if state.get("depends_on"):
        bits.append(f"depends_on={','.join(state['depends_on'])}")
    if state.get("wait_on"):
        bits.append(f"wait_on={state['wait_on']}")
    if state.get("_liveness_note"):
        bits.append("liveness=unknown")
    elif state.get("status") == "running" and state.get("pgid"):
        members = process_group_members(int(state["pgid"]))
        if members:
            bits.append(f"procs={len(members)}")
    _call_hook("on_status_print", state, bits)
    print(" ".join(bits))
    context_note = normalize_headline_text(state.get("context_note", ""))
    if state.get("_liveness_note"):
        print(f"  {state['_liveness_note']}")
    if context_note and context_note != headline:
        print(f"  context: {state['context_note']}")
    if headline:
        print(f"  {headline}")
    if args.tail:
        print_tail(Path(state["log_path"]), args.tail)


def print_tail(path: Path, n: int) -> None:
    if not path.exists():
        print(f"missing log: {path}")
        return
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    for line in lines[-n:]:
        print(line)


def tail(args: argparse.Namespace) -> int:
    state = load_job(args.job)
    print_tail(Path(state["log_path"]), args.lines)
    return 0


def note_job(args: argparse.Namespace) -> int:
    state = load_job(args.job)
    sys.path.insert(0, str(CODE_ROOT))
    import artifact_meta

    note = artifact_meta.normalize_one_line(" ".join(args.note).strip())
    if not note:
        raise SystemExit("empty note")

    stamp = utc_now()
    state.setdefault("analysis_notes", [])
    state["analysis_notes"] = [*state["analysis_notes"], {"at": stamp, "text": note}]
    state["post_run_note"] = note
    state["post_run_noted_at"] = stamp

    headline_path = (
        Path(state.get("headline_path", "")) if state.get("headline_path") else None
    )
    if headline_path is not None:
        write_headline(headline_path, f"analysis: {note}")

    meta_text = ""
    meta_path = Path(state.get("meta_path", "")) if state.get("meta_path") else None
    if meta_path is not None and not meta_path.exists() and state.get("output_path"):
        state = write_meta(state)
        meta_path = Path(state.get("meta_path", "")) if state.get("meta_path") else None

    if meta_path is not None and meta_path.exists():
        meta_text = artifact_meta.upsert_analysis_summary_markdown(
            meta_path.read_text(encoding="utf-8"),
            note,
            timestamp=stamp,
        )
        meta_path.write_text(meta_text, encoding="utf-8")

    _call_hook("on_note", state, note, stamp, meta_path=meta_path, meta_text=meta_text)

    write_json(Path(state["state_path"]), state)
    write_json(current_path(state["job"]), state)
    print(f"{state['job']}: {note}")
    return 0


def cleanup_running(args: argparse.Namespace) -> int:
    sys.path.insert(0, str(CODE_ROOT))
    import artifact_meta

    def _scan_markers() -> list[Path]:
        skip = {
            ".git",
            ".agentctl",
            "runs",
            "__pycache__",
            ".venv",
            ".pixi",
            "node_modules",
        }
        found: list[Path] = []
        for dirpath, dirnames, filenames in os.walk(ROOT):
            dirnames[:] = [name for name in dirnames if name not in skip]
            for name in filenames:
                if name.endswith(".running.md"):
                    found.append(Path(dirpath) / name)
        return sorted(found)

    removed = 0
    would_remove = 0
    if args.outputs:
        for output in args.outputs:
            path = artifact_meta.running_path(output)
            if args.dry_run:
                did_remove = False
                if path.exists():
                    would_remove += 1
            else:
                did_remove = artifact_meta.cleanup_running(output)
            if did_remove:
                removed += 1
                if not args.quiet:
                    print(f"removed {path}")
            elif not args.quiet:
                print(
                    f"{'would-remove' if path.exists() and args.dry_run else 'missing'} {path}"
                )
        if not args.quiet:
            suffix = f", {would_remove} would-remove" if args.dry_run else ""
            print(f"{removed} removed{suffix}")
        return 0

    markers = _scan_markers()
    if not markers:
        if not args.quiet:
            print("no .running.md markers")
        return 0

    kept = 0
    for path in markers:
        fields = marker_fields(path)
        output = output_for_marker(path, fields)
        pid_state = marker_pid_status(fields)
        sidecar = completion_sidecar(output)
        if sidecar is not None and pid_state != "running":
            if args.dry_run:
                would_remove += 1
            else:
                path.unlink()
                removed += 1
            if not args.quiet:
                action = "would-remove" if args.dry_run else "removed"
                print(f"completed {action} {path} sidecar={sidecar}")
            continue
        kept += 1
        if not args.quiet:
            state = "running" if pid_state == "running" else "interrupted"
            print(
                f"{state} kept {path} pid={fields.get('pid', '') or '?'} out={output}"
            )
    if not args.quiet:
        dry_run_part = f", {would_remove} would-remove" if args.dry_run else ""
        print(f"{removed} removed{dry_run_part}, {kept} kept")
    return 0


def wait_job(args: argparse.Namespace) -> int:
    deadline = time.time() + args.timeout if args.timeout > 0 else None
    next_report = 0.0
    heartbeat_interval = max(0.0, float(getattr(args, "heartbeat", 30.0) or 0.0))
    while True:
        touch_active_entry()
        state = load_job(args.job)
        status = state.get("status", "")
        if args.target == "not-running":
            # A queued (waiting) run is pending, not terminal: its payload has
            # not run yet, so releasing on it defeats the wait.
            done = status not in ("running", "waiting")
        else:
            done = status == args.target
        if done:
            bits = [state["job"], state["run_id"], status]
            if status_returncode_text(state):
                bits.append(f"returncode={status_returncode_text(state)}")
            if state.get("log_path"):
                bits.append(f"log={state['log_path']}")
            print(" ".join(bits))
            if args.tail > 0 and state.get("log_path"):
                print_tail(Path(state["log_path"]), args.tail)
            return status_returncode_exit_code(state) if status == "finished" else 0
        now = time.time()
        if heartbeat_interval > 0 and (next_report == 0.0 or now >= next_report):
            line = f"[wait] job={state['job']} status={status} elapsed={elapsed_estimate_text(state)} target={args.target}"
            if getattr(args, "heartbeat_gpu", False):
                try:
                    gpu_stats = query_gpu_stats(args.gpu)
                    line += " " + format_gpu_stats(gpu_stats)
                except Exception as exc:
                    line += f" gpu_query_failed={exc}"
            print(line, flush=True)
            next_report = now + heartbeat_interval
        if deadline is not None and time.time() >= deadline:
            print(
                f"timeout waiting for {state['job']} to reach {args.target}; "
                f"current status={status}",
                file=sys.stderr,
            )
            return 1
        time.sleep(args.poll)


def parse_nvidia_smi_number(text: str) -> float | None:
    value = text.strip()
    if not value or value.lower() in {"[not supported]", "not supported", "n/a"}:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def query_gpu_stats(
    gpu_index: int, *, timeout: float | None = None
) -> dict[str, float | int | None]:
    out = subprocess.check_output(
        [
            "nvidia-smi",
            f"--id={gpu_index}",
            "--query-gpu=index,memory.total,memory.used,power.draw,utilization.gpu",
            "--format=csv,noheader,nounits",
        ],
        text=True,
        stderr=subprocess.STDOUT,
        timeout=timeout,
    )
    line = out.strip().splitlines()[0]
    fields = [field.strip() for field in line.split(",")]
    if len(fields) != 5:
        raise RuntimeError(
            f"unexpected nvidia-smi output for gpu {gpu_index}: {line!r}"
        )
    return {
        "gpu": int(fields[0]),
        "memory_total_mib": int(fields[1]),
        "memory_used_mib": int(fields[2]),
        "power_draw_w": parse_nvidia_smi_number(fields[3]),
        "utilization_gpu_pct": parse_nvidia_smi_number(fields[4]),
    }


def query_gpu_stats_smoothed(
    gpu_index: int,
    *,
    samples: int = DEFAULT_HEARTBEAT_GPU_SMOOTH_SAMPLES,
    interval: float = DEFAULT_HEARTBEAT_GPU_SMOOTH_INTERVAL_S,
    timeout: float | None = None,
) -> dict[str, float | int | None]:
    sample_count = max(1, int(samples))
    sleep_interval = max(0.0, float(interval))
    deadline = time.monotonic() + timeout if timeout is not None else None
    stats_list: list[dict[str, float | int | None]] = []
    for idx in range(sample_count):
        if idx and sleep_interval > 0:
            if deadline is None:
                time.sleep(sleep_interval)
            else:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise subprocess.TimeoutExpired("nvidia-smi", timeout)
                time.sleep(min(sleep_interval, remaining))
        remaining = None if deadline is None else deadline - time.monotonic()
        if remaining is not None and remaining <= 0:
            raise subprocess.TimeoutExpired("nvidia-smi", timeout)
        stats_list.append(query_gpu_stats(gpu_index, timeout=remaining))
    merged = dict(stats_list[-1])
    utils = [
        float(s["utilization_gpu_pct"])
        for s in stats_list
        if s.get("utilization_gpu_pct") is not None
    ]
    powers = [
        float(s["power_draw_w"])
        for s in stats_list
        if s.get("power_draw_w") is not None
    ]
    if utils:
        merged["utilization_gpu_pct_avg"] = sum(utils) / len(utils)
        merged["utilization_gpu_pct_max"] = max(utils)
    if powers:
        merged["power_draw_w_avg"] = sum(powers) / len(powers)
    merged["sample_count"] = len(stats_list)
    merged["sample_window_s"] = sleep_interval * max(0, len(stats_list) - 1)
    return merged


def gpu_memory_used_mib(gpu_index: int) -> int:
    return int(query_gpu_stats(gpu_index)["memory_used_mib"])


def wait_for_gpu_memory(
    *,
    gpu: int,
    max_memory_used: int,
    poll: float,
    timeout: float,
    heartbeat: float | None = None,
) -> int:
    deadline = time.time() + timeout if timeout > 0 else None
    heartbeat_interval = max(
        0.0, float(max(10.0, poll) if heartbeat is None else heartbeat)
    )
    last_report = 0.0
    while True:
        touch_active_entry()
        try:
            stats = query_gpu_stats(gpu)
        except Exception as exc:
            print(f"failed to query gpu {gpu}: {exc}", file=sys.stderr)
            return 2
        used = int(stats["memory_used_mib"])
        now = time.time()
        if used <= max_memory_used:
            print(f"gpu={gpu} VRAM={used}MiB <= {max_memory_used}MiB")
            return 0
        if heartbeat_interval > 0 and (
            last_report == 0.0 or now - last_report >= heartbeat_interval
        ):
            print(
                f"[wait-gpu] {format_gpu_stats(stats)} target<={max_memory_used}MiB",
                flush=True,
            )
            last_report = now
        if deadline is not None and now >= deadline:
            print(
                f"timeout waiting for gpu={gpu} VRAM <= {max_memory_used}MiB; "
                f"current={used}MiB",
                file=sys.stderr,
            )
            return 1
        time.sleep(poll)


def gpu_watch_thresholds_requested(args: argparse.Namespace) -> bool:
    return (
        args.notify_max_memory_used is not None
        or args.notify_max_power_draw is not None
    )


def gpu_below_watch_thresholds(
    stats: dict[str, float | int | None], args: argparse.Namespace
) -> bool:
    memory_ok = (
        args.notify_max_memory_used is None
        or int(stats["memory_used_mib"]) <= args.notify_max_memory_used
    )
    power_draw = stats.get("power_draw_w")
    power_ok = args.notify_max_power_draw is None or (
        power_draw is not None and float(power_draw) <= args.notify_max_power_draw
    )
    return memory_ok and power_ok


def format_gpu_stats(stats: dict[str, float | int | None]) -> str:
    total = stats.get("memory_total_mib")
    used = int(stats["memory_used_mib"])
    memory = (
        f"VRAM={used}/{int(total)}MiB free={int(total) - used}MiB"
        if total is not None
        else f"VRAM={used}MiB"
    )
    bits = [f"gpu={int(stats['gpu'])}", memory]
    power_draw = stats.get("power_draw_w_avg", stats.get("power_draw_w"))
    util = stats.get("utilization_gpu_pct_avg", stats.get("utilization_gpu_pct"))
    util_peak = stats.get("utilization_gpu_pct_max")
    bits.append(
        f"power={power_draw:.1f}W" if power_draw is not None else "power=unavailable"
    )
    if util is None:
        bits.append("compute=unavailable")
    elif util_peak is not None and abs(float(util_peak) - float(util)) >= 1.0:
        bits.append(f"compute={util:.0f}% avg/{util_peak:.0f}% peak")
    else:
        bits.append(f"compute={util:.0f}%")
    return " ".join(bits)


def format_gpu_watch_thresholds(args: argparse.Namespace) -> str:
    bits: list[str] = []
    if args.notify_max_memory_used is not None:
        bits.append(f"VRAM<={args.notify_max_memory_used}MiB")
    if args.notify_max_power_draw is not None:
        bits.append(f"power<={args.notify_max_power_draw:g}W")
    return ", ".join(bits) or "none"


def gpu_activity_seen_since_launch(
    stats: dict[str, float | int | None],
    launch_stats: dict[str, float | int | None] | None,
) -> bool:
    if launch_stats is None:
        return int(stats["memory_used_mib"]) > 1024
    launch_mem = int(launch_stats.get("memory_used_mib") or 0)
    current_mem = int(stats["memory_used_mib"])
    if current_mem >= launch_mem + 1024:
        return True
    launch_power = launch_stats.get("power_draw_w")
    current_power = stats.get("power_draw_w")
    if (
        launch_power is not None
        and current_power is not None
        and float(current_power) >= float(launch_power) + 15.0
    ):
        return True
    launch_util = launch_stats.get("utilization_gpu_pct")
    current_util = stats.get("utilization_gpu_pct")
    return (
        current_util is not None
        and float(current_util) >= 10.0
        and (launch_util is None or float(current_util) >= float(launch_util) + 10.0)
    )


def poll_watch_gpu_state(
    *,
    gpu: int,
    args: argparse.Namespace,
    launch_gpu_stats: dict[str, float | int | None] | None,
    last_gpu_below: bool | None,
    last_gpu_error: str,
    gpu_activity_seen: bool,
    query_timeout: float | None = None,
) -> tuple[bool | None, str, bool, bool, dict[str, float | int | None] | None]:
    try:
        stats = query_gpu_stats(gpu, timeout=query_timeout)
        if gpu_activity_seen_since_launch(stats, launch_gpu_stats):
            gpu_activity_seen = True
        if not gpu_watch_thresholds_requested(args):
            return None, "", gpu_activity_seen, True, stats
        gpu_below = gpu_below_watch_thresholds(stats, args)
        last_gpu_error = ""
        if last_gpu_below is None:
            if gpu_below:
                print(
                    f"[watch] gpu threshold satisfied: {format_gpu_stats(stats)} "
                    f"thresholds={format_gpu_watch_thresholds(args)}",
                    flush=True,
                )
        elif gpu_below and not last_gpu_below:
            print(
                f"[watch] gpu threshold satisfied: {format_gpu_stats(stats)} "
                f"thresholds={format_gpu_watch_thresholds(args)}",
                flush=True,
            )
        elif last_gpu_below and not gpu_below:
            print(
                f"[watch] gpu rose above threshold again: {format_gpu_stats(stats)} "
                f"thresholds={format_gpu_watch_thresholds(args)}",
                flush=True,
            )
        return gpu_below, last_gpu_error, gpu_activity_seen, True, stats
    except Exception as exc:
        message = str(exc)
        if message != last_gpu_error:
            print(
                f"[watch] gpu query failed for gpu={gpu}: {message}",
                file=sys.stderr,
                flush=True,
            )
            last_gpu_error = message
        return last_gpu_below, last_gpu_error, gpu_activity_seen, False, None


def wait_gpu(args: argparse.Namespace) -> int:
    return wait_for_gpu_memory(
        gpu=args.gpu,
        max_memory_used=args.max_memory_used,
        poll=args.poll,
        timeout=args.timeout,
        heartbeat=args.heartbeat,
    )


ON_DECK_DIRNAME = "on-deck"


def snapshot_job_runs() -> dict[tuple[str, str], str]:
    """Each job's latest run identity: {(job, run_id): status} from jobs/*/current.json."""
    seen: dict[tuple[str, str], str] = {}
    if not JOBS.is_dir():
        return seen
    for current in JOBS.glob("*/current.json"):
        try:
            state = read_json(current)
        except Exception:
            continue
        rid = str(state.get("run_id") or "")
        if rid:
            job = str(state.get("job") or current.parent.name)
            seen[(job, rid)] = str(state.get("status") or "")
    return seen


def snapshot_on_deck() -> dict[str, float]:
    """mtime by entry name for on-deck/*.md (INDEX.md is derived and ignored;
    done/ is a subdir and out of the top-level glob)."""
    entries: dict[str, float] = {}
    deck = ROOT / ON_DECK_DIRNAME
    if not deck.is_dir():
        return entries
    for path in deck.glob("*.md"):
        if path.name == "INDEX.md":
            continue
        try:
            entries[path.name] = path.stat().st_mtime
        except OSError:
            continue
    return entries


def wait_work(args: argparse.Namespace) -> int:
    """Block until new work appears: a new run id and/or a new on-deck entry.

    Baselines are snapshotted at entry, so work already present never fires;
    the verb works from an empty queue and an idle project. Prints what
    appeared and exits 0; exits 1 on --timeout.
    """
    watch_runs = args.runs or not args.on_deck
    watch_deck = args.on_deck or not args.runs
    sources = " or ".join(
        name
        for name, on in (
            ("new agentctl run", watch_runs),
            (f"new/updated {ON_DECK_DIRNAME}/ entry", watch_deck),
        )
        if on
    )
    base_runs = snapshot_job_runs() if watch_runs else {}
    base_deck = snapshot_on_deck() if watch_deck else {}
    deadline = time.time() + args.timeout if args.timeout > 0 else None
    started = time.time()
    heartbeat = max(0.0, float(args.heartbeat or 0.0))
    next_report = 0.0
    while True:
        touch_active_entry()
        news: list[str] = []
        if watch_runs:
            runs = snapshot_job_runs()
            for job, rid in sorted(set(runs) - set(base_runs)):
                status = runs[(job, rid)]
                news.append(
                    f"new run: job={job} run={rid}"
                    + (f" status={status}" if status else "")
                )
        if watch_deck:
            deck = snapshot_on_deck()
            for name in sorted(deck):
                if name not in base_deck:
                    news.append(
                        f"new {ON_DECK_DIRNAME} entry: {ON_DECK_DIRNAME}/{name}"
                    )
                elif deck[name] != base_deck[name]:
                    news.append(
                        f"updated {ON_DECK_DIRNAME} entry: {ON_DECK_DIRNAME}/{name}"
                    )
        if news:
            for line in news:
                print(line)
            return 0
        now = time.time()
        if heartbeat > 0 and (next_report == 0.0 or now >= next_report):
            print(
                f"[wait-work] waiting for {sources} "
                f"({format_duration(int(now - started))} elapsed)",
                flush=True,
            )
            next_report = now + heartbeat
        if deadline is not None and now >= deadline:
            print(f"timeout waiting for {sources}", file=sys.stderr)
            return 1
        time.sleep(args.poll)


def watch(args: argparse.Namespace, proc: subprocess.Popen | None = None) -> int:
    """Stream new log lines until the job is no longer running, then print final status."""
    timeout = float(getattr(args, "timeout", 0.0) or 0.0)
    started = time.monotonic()
    deadline = started + timeout if timeout > 0 else None
    if getattr(args, "notify_gpu_idle", False):
        if args.notify_max_memory_used is None:
            args.notify_max_memory_used = DEFAULT_IDLE_GPU_MEMORY_USED_MIB
        if args.notify_max_power_draw is None:
            args.notify_max_power_draw = DEFAULT_IDLE_GPU_POWER_DRAW_W
    state = load_job(args.job)
    log_path = Path(state["log_path"])
    offset = 0
    proc_returncode: int | None = None
    gpu_patience = float(getattr(args, "gpu_patience", 0.0) or 0.0)
    launch_gpu_stats = state.get("launch_gpu_stats")
    waiting_for_gpu_thresholds = gpu_watch_thresholds_requested(args)
    watching_gpu = waiting_for_gpu_thresholds or gpu_patience > 0
    gpu_done = not waiting_for_gpu_thresholds
    job_done_reported = False
    job_headline_reported = False
    waiting_for_gpu_reported = False
    gpu_patience_warned = False
    gpu_activity_seen = False
    zero_compute_started_at = 0.0
    zero_compute_last_report_at = 0.0
    zero_compute_interrupt_reported = False
    last_gpu_below: bool | None = None
    last_gpu_stats: dict[str, float | int | None] | None = None
    last_gpu_error = ""
    next_gpu_poll_at = 0.0
    next_heartbeat_at = 0.0
    heartbeat_interval = max(0.0, float(getattr(args, "heartbeat", 30.0) or 0.0))
    gpu_poll = args.gpu_poll if args.gpu_poll > 0 else args.poll
    if log_path.exists():
        # Follow from the end either way; --tail only decides how much of
        # the existing log is replayed first.
        data = log_path.read_bytes()
        if args.tail > 0:
            tail_lines = data.splitlines(keepends=True)[-args.tail :]
            sys.stdout.buffer.write(b"".join(tail_lines))
            sys.stdout.buffer.flush()
        offset = len(data)
    print(
        f"[watch] job={state['job']} run={state['run_id']} status={state.get('status', '?')} log={log_path}",
        flush=True,
    )
    if watching_gpu:
        print(
            f"[watch] gpu watch enabled for gpu={args.gpu}: "
            f"thresholds={format_gpu_watch_thresholds(args)} gpu_patience={format_duration(gpu_patience)}",
            flush=True,
        )
    if not waiting_for_gpu_thresholds:
        print(
            "[watch] note: no GPU-idle notification thresholds requested; "
            "watch will exit when the tracked job state changes, not when the GPU becomes idle",
            flush=True,
        )
    while True:
        touch_active_entry()
        if proc_returncode is None:
            proc_returncode = reap_proc(proc)
        state = load_job(args.job)
        if (
            proc is not None
            and proc_returncode is not None
            and int(state.get("pid", -1)) == proc.pid
            and (
                state.get("status") == "running" or state.get("returncode") == "unknown"
            )
        ):
            state = mark_state_finished(state, proc_returncode)
            state = finalize_finished_state(state)
            write_json(Path(state["state_path"]), state)
            write_json(current_path(state["job"]), state)
        if log_path.exists():
            try:
                data = log_path.read_bytes()
            except OSError:
                data = b""
            if len(data) > offset:
                sys.stdout.buffer.write(data[offset:])
                sys.stdout.buffer.flush()
                offset = len(data)
        now = time.monotonic()
        if (
            watching_gpu
            and now >= next_gpu_poll_at
            and (deadline is None or now < deadline)
        ):
            next_gpu_poll_at = now + gpu_poll
            (
                last_gpu_below,
                last_gpu_error,
                gpu_activity_seen,
                gpu_polled,
                last_gpu_stats,
            ) = poll_watch_gpu_state(
                gpu=args.gpu,
                args=args,
                launch_gpu_stats=launch_gpu_stats,
                last_gpu_below=last_gpu_below,
                last_gpu_error=last_gpu_error,
                gpu_activity_seen=gpu_activity_seen,
                query_timeout=None if deadline is None else max(0.001, deadline - now),
            )
            now = time.monotonic()
            if gpu_polled and waiting_for_gpu_thresholds:
                gpu_done = bool(last_gpu_below)
        if (
            watching_gpu
            and state.get("status") == "running"
            and gpu_activity_seen
            and last_gpu_stats is not None
        ):
            util = last_gpu_stats.get("utilization_gpu_pct")
            used = int(last_gpu_stats["memory_used_mib"])
            if (
                util is not None
                and float(util) <= 0.0
                and used > DEFAULT_ZERO_COMPUTE_MIN_VRAM_MIB
            ):
                if zero_compute_started_at == 0.0:
                    zero_compute_started_at = now
                    zero_compute_last_report_at = now
                zero_elapsed = now - zero_compute_started_at
                if zero_elapsed >= DEFAULT_ZERO_COMPUTE_REPORT_INTERVAL_S and (
                    now - zero_compute_last_report_at
                    >= DEFAULT_ZERO_COMPUTE_REPORT_INTERVAL_S
                ):
                    print(
                        f"[watch] zero-compute persists: job={state['job']} "
                        f"elapsed={elapsed_estimate_text(state)} zero_compute={format_duration(zero_elapsed)} "
                        f"{format_gpu_stats(last_gpu_stats)}",
                        flush=True,
                    )
                    zero_compute_last_report_at = now
                if (
                    zero_elapsed >= DEFAULT_ZERO_COMPUTE_INTERRUPT_AFTER_S
                    and not zero_compute_interrupt_reported
                ):
                    zero_compute_interrupt_reported = True
                    print(
                        f"[watch] interrupting {state['job']}: compute stayed at 0% for "
                        f"{format_duration(zero_elapsed)} while VRAM remained occupied "
                        f"({format_gpu_stats(last_gpu_stats)})",
                        flush=True,
                    )
                    if terminate_state(
                        state,
                        grace=10.0,
                        reason=(
                            "agentctl zero-compute timeout: compute remained at 0% for "
                            f"{format_duration(zero_elapsed)} with VRAM occupied"
                        ),
                    ):
                        state = load_job(args.job)
            else:
                zero_compute_started_at = 0.0
                zero_compute_last_report_at = 0.0
                zero_compute_interrupt_reported = False
        if (
            gpu_patience > 0
            and not gpu_activity_seen
            and not gpu_patience_warned
            and (elapsed_seconds(state) or 0) >= gpu_patience
        ):
            print(
                f"[watch] gpu patience expired: job={state['job']} elapsed={elapsed_estimate_text(state)} "
                f"has not shown GPU activity on gpu={args.gpu} since launch",
                flush=True,
            )
            if launch_gpu_stats is not None:
                print(
                    f"[watch] launch gpu baseline: {format_gpu_stats(launch_gpu_stats)}",
                    flush=True,
                )
            gpu_patience_warned = True
        if heartbeat_interval > 0 and (
            next_heartbeat_at == 0.0 or now >= next_heartbeat_at
        ):
            heartbeat_line = (
                f"[watch] heartbeat job={state['job']} status={state.get('status', '?')} "
                f"elapsed={elapsed_estimate_text(state)}"
            )
            if watching_gpu and last_gpu_below is not None:
                heartbeat_line += " gpu_threshold=" + (
                    "met" if last_gpu_below else "pending"
                )
            if gpu_patience > 0:
                heartbeat_line += " gpu_activity=" + (
                    "seen" if gpu_activity_seen else "not-yet-seen"
                )
            if getattr(args, "heartbeat_gpu", False) and (
                deadline is None or time.monotonic() < deadline
            ):
                gpu_stats = None
                try:
                    gpu_stats = query_gpu_stats_smoothed(
                        args.gpu,
                        timeout=None
                        if deadline is None
                        else max(0.001, deadline - time.monotonic()),
                    )
                except Exception as exc:
                    gpu_stats = last_gpu_stats
                    if gpu_stats is None:
                        heartbeat_line += f" gpu_query_failed={exc}"
                if gpu_stats is not None:
                    heartbeat_line += " " + format_gpu_stats(gpu_stats)
                now = time.monotonic()
            print(heartbeat_line, flush=True)
            next_heartbeat_at = now + heartbeat_interval
        current_status = state.get("status", "")
        # waiting (queued behind --after) is a live state: stay attached
        # through the queued phase and the run itself.
        if current_status not in ("running", "waiting"):
            if watching_gpu and (deadline is None or time.monotonic() < deadline):
                query_started_at = time.monotonic()
                (
                    last_gpu_below,
                    last_gpu_error,
                    gpu_activity_seen,
                    gpu_polled,
                    last_gpu_stats,
                ) = poll_watch_gpu_state(
                    gpu=args.gpu,
                    args=args,
                    launch_gpu_stats=launch_gpu_stats,
                    last_gpu_below=last_gpu_below,
                    last_gpu_error=last_gpu_error,
                    gpu_activity_seen=gpu_activity_seen,
                    query_timeout=None
                    if deadline is None
                    else max(0.001, deadline - query_started_at),
                )
                now = time.monotonic()
                if gpu_polled and waiting_for_gpu_thresholds:
                    gpu_done = bool(last_gpu_below)
            if not job_done_reported:
                done_bits = [
                    f"\n[watch] done: {state['job']} {state['run_id']} status={current_status}"
                ]
                if status_returncode_text(state):
                    done_bits.append(f"returncode={status_returncode_text(state)}")
                print(" ".join(done_bits), flush=True)
                job_done_reported = True
            headline_path = Path(state.get("headline_path", ""))
            if headline_path.exists() and not job_headline_reported:
                headline = read_headline(headline_path)
                if headline:
                    print(f"[watch] headline: {headline}", flush=True)
                    job_headline_reported = True
            if not waiting_for_gpu_thresholds or gpu_done:
                return (
                    status_returncode_exit_code(state)
                    if current_status == "finished"
                    else 0
                )
            if not waiting_for_gpu_reported:
                rc_text = status_returncode_text(state)
                suffix = f" returncode={rc_text}" if rc_text else ""
                print(
                    f"[watch] job finished but continuing until gpu={args.gpu} satisfies "
                    f"{format_gpu_watch_thresholds(args)}{suffix}",
                    flush=True,
                )
                waiting_for_gpu_reported = True
        now = time.monotonic()
        if deadline is not None and now >= deadline:
            print(
                f"[{WATCH_TIMEOUT_MARKER}] job={state['job']} "
                f"status={current_status} timeout={timeout:g}s",
                file=sys.stderr,
                flush=True,
            )
            return WATCH_TIMEOUT_EXIT_CODE
        sleep_for = args.poll
        if deadline is not None:
            sleep_for = min(sleep_for, max(0.0, deadline - time.monotonic()))
        time.sleep(sleep_for)


def stop(args: argparse.Namespace) -> int:
    state = load_job(args.job)
    # A waiting (queued behind --after) run has a live wrapper process to
    # kill: stopping it cancels the queued payload before it ever launches.
    if state.get("status") not in ("running", "waiting"):
        print(f"{state['job']} is {state['status']}")
        return 0
    pgid = int(state.get("pgid") or state["pid"])
    if not process_group_alive(pgid) and process_visibility_limited():
        print(
            f"cannot verify or stop {state['job']} from this process namespace; "
            "rerun agentctl stop with host-visible process permissions",
            file=sys.stderr,
        )
        return 2
    terminate_state(state, grace=args.grace, reason="agentctl stop")
    print(f"stopped {state['job']} {state['run_id']}")
    return 0


def restart_user_argv(state: dict) -> list[str]:
    """Recover the payload argv, including from pre-user_argv run state."""
    if "user_argv" in state:
        user_argv = state["user_argv"]
        if not isinstance(user_argv, list):
            raise SystemExit("cannot restart: user_argv is not a list")
        return list(user_argv)

    final_argv = list(state.get("argv") or [])
    declaration_suffix = []
    for key, info in (state.get("inputs") or {}).items():
        if not info.get("raw") and info.get("path"):
            declaration_suffix.append(f"--{key}={info['path']}")
    for key, info in (state.get("outputs") or {}).items():
        if info.get("arg") and info.get("path"):
            declaration_suffix.append(f"--{key}={info['path']}")
    if declaration_suffix:
        if final_argv[-len(declaration_suffix) :] != declaration_suffix:
            raise SystemExit(
                "cannot restart legacy run: declaration-owned argv suffix does not "
                "match recorded inputs/outputs"
            )
        del final_argv[-len(declaration_suffix) :]
    return final_argv


def restart(args: argparse.Namespace) -> int:
    state = load_job(args.job)
    # Stop a waiting (queued) run too, or the old wrapper would launch the
    # payload a second time when its --after dependencies clear.
    if state.get("status") in ("running", "waiting"):
        stop(argparse.Namespace(job=args.job, grace=args.grace))
    start_args = argparse.Namespace(
        argv=restart_user_argv(state),
        context_note=state.get("context_note", ""),
        depends_on=state.get("depends_on", []),
        # Requeue behind the same --after dependencies; a clean-finished
        # dependency releases the new wait immediately.
        after=list(state.get("wait_after_specs") or []),
        after_poll=float(state.get("wait_after_poll") or 10.0),
        after_heartbeat=float(state.get("wait_after_heartbeat") or 30.0),
        after_timeout=float(state.get("wait_after_timeout") or 0.0),
        env=[],
        gpus="",
        input_file="",
        # Plugin-managed in on_restart but defaulted here so the namespace exists.
        input=[],
        input_raw=[],
        input_hash=[],
        output=[],
        output_arg=[],
        output_hash=[],
        script="",
        propagate_json="",
        job=state["job"],
        log="",
        meta=bool(state.get("output_path")),
        mode=state.get("mode", "start"),
        run_id="",
        runtime_estimate=state.get("runtime_estimate", ""),
        project_env=(state.get("project_env") or {}).get("path", ""),
        no_project_env=not bool(state.get("project_env")),
        source_env=state.get("source_env", []),
        gpu_patience=600.0,
        wait_gpu=0,
        wait_max_memory_used=None,
        wait_poll=10.0,
        wait_heartbeat=10.0,
        wait_timeout=0.0,
        watch=False,
        watch_tail=20,
        watch_poll=5.0,
        watch_heartbeat=30.0,
        watch_heartbeat_gpu=False,
        watch_gpu=0,
        watch_gpu_poll=10.0,
        watch_notify_gpu_idle=False,
        watch_notify_max_memory_used=None,
        watch_notify_max_power_draw=None,
    )
    _call_hook("on_restart", state, start_args)
    return start(start_args)


def add_start_options(sp: argparse.ArgumentParser) -> None:
    sp.add_argument("job")
    sp.add_argument(
        "--context-note",
        default="",
        help="Brief free-form reason/context for this job; copied into agentctl state and output metadata.",
    )
    sp.add_argument(
        "--depends-on",
        action="append",
        default=[],
        help="Prior job name this run logically follows; metadata only, does not auto-schedule.",
    )
    sp.add_argument(
        "--after",
        action="append",
        default=[],
        help=(
            "Queue this launch until an agentctl job or <output>.running.md artifact is done. "
            "An output path also resolves through a queued or running job that declares it "
            "via --output, so a dependent can queue before its producer starts. "
            "Use only for mechanical dependencies; inspect results manually when follow-on "
            "choice depends on completed content."
        ),
    )
    sp.add_argument(
        "--after-poll",
        type=float,
        default=10.0,
        help="Seconds between --after dependency checks.",
    )
    sp.add_argument(
        "--after-heartbeat",
        type=float,
        default=30.0,
        help="Seconds between --after heartbeat lines/headline updates (0 disables).",
    )
    sp.add_argument(
        "--after-timeout",
        type=float,
        default=0.0,
        help="Maximum seconds to wait for --after dependencies; 0 means no timeout.",
    )
    sp.add_argument(
        "--env", action="append", default=[], help="Extra environment KEY=VALUE."
    )
    project_env = sp.add_mutually_exclusive_group()
    project_env.add_argument(
        "--project-env",
        default="",
        help=(
            "Declarative KEY=VALUE defaults file for the child environment. "
            "Defaults to ./agentctl.env when that file exists; ${AGENTCTL_ROOT} "
            "expands to the resolved project root."
        ),
    )
    project_env.add_argument(
        "--no-project-env",
        action="store_true",
        help="Do not auto-load the project-root agentctl.env file.",
    )
    sp.add_argument("--gpus", default="", help="CUDA_VISIBLE_DEVICES value.")
    sp.add_argument(
        "--input-file",
        default="",
        help="Input file path exposed as AGENTCTL_INPUT_FILE.",
    )
    sp.add_argument(
        "--log", default="", help="Log file path. Defaults under .agentctl/runs/."
    )
    sp.add_argument(
        "--no-meta",
        dest="meta",
        action="store_false",
        help=(
            "Do not write the human-readable launch .meta.md. The .meta.json back-pointer "
            "sidecar is independent — see --no-aim."
        ),
    )
    sp.add_argument(
        "--output",
        action="append",
        default=[],
        help=(
            "Declare an output as KEY=PATH for provenance only; this does NOT pass an --output "
            "argument to the payload (repeatable). The first declared output is the primary "
            "(its path anchors .meta.md). A bare PATH (no '=') is accepted as shorthand for primary=PATH. "
            "Each output gets a <path>.meta.json sidecar at completion pointing back at the run. "
            "Use --output-arg output=PATH when the payload also needs --output=PATH."
        ),
    )
    sp.add_argument(
        "--output-arg",
        action="append",
        default=[],
        help=(
            "Declare an output as KEY=PATH and append --KEY=PATH to the payload argv (repeatable). "
            "This avoids repeating a payload output path separately from its provenance declaration."
        ),
    )
    sp.add_argument(
        "--input",
        action="append",
        default=[],
        help=(
            "Declare an input as KEY=PATH (repeatable). Translates to --KEY=PATH appended to "
            "the underlying program argv. Captures size/mtime/source-pointer in the run record."
        ),
    )
    sp.add_argument(
        "--input-raw",
        action="append",
        default=[],
        help="Like --input KEY=PATH but does NOT translate to argv (you pass --KEY=PATH yourself).",
    )
    sp.add_argument(
        "--input-hash",
        action="append",
        default=[],
        help=(
            "Like --input KEY=PATH but additionally computes sha256 of the file at launch "
            "(opt-in because hashing large weight tensors is expensive)."
        ),
    )
    sp.add_argument(
        "--output-hash",
        action="append",
        default=[],
        help=(
            "Like --output KEY=PATH but additionally computes sha256 at completion. "
            "Cost is paid after the user command finishes (run_child)."
        ),
    )
    sp.add_argument(
        "--script",
        default="",
        help=(
            "Override the auto-detected script with an explicit path. Useful when argv has no "
            "script-shaped argument (bash -c '...'), the heuristic picks the wrong file, or a "
            "multi-word launcher hides the actual code (pixi run, conda run, nohup, etc.)."
        ),
    )
    sp.add_argument(
        "--propagate-json",
        default="",
        help=(
            "JSON object of producer-flagged facts to be quoted at the next consumer's input "
            "record. Stored in the run record and folded into each output's .meta.json sidecar "
            "under `propagate`. Can also be supplied at runtime by writing the same shape to "
            "$AGENTCTL_RUN_DIR/propagate.json (cooperative protocol; merged at completion)."
        ),
    )
    sp.add_argument("--run-id", default="", help="Override generated run id.")
    sp.add_argument(
        "--runtime-estimate",
        default="",
        help="Expected runtime such as 90s, 15m, 2h, or 1h30m; stored in job state for status displays.",
    )
    sp.add_argument(
        "--source-env",
        action="append",
        default=[],
        help=(
            "Source an extra shell env script before launch, then exec the payload directly via argv. "
            "Prefer this to wrapping the payload in bash -lc just to load exports."
        ),
    )
    sp.add_argument(
        "--gpu-patience",
        type=float,
        default=600.0,
        help=(
            "Warn during watch if the launched job still has not shown GPU activity after this many seconds. "
            "Default is intentionally generous for large-model download/load startup."
        ),
    )
    sp.add_argument(
        "--wait-gpu", type=int, default=0, help="GPU index to poll before launch."
    )
    sp.add_argument(
        "--wait-max-memory-used",
        type=int,
        default=None,
        help="Before launch, wait until this GPU VRAM threshold is met.",
    )
    sp.add_argument(
        "--wait-poll",
        type=float,
        default=10.0,
        help="Seconds between prelaunch GPU checks.",
    )
    sp.add_argument(
        "--wait-heartbeat",
        type=float,
        default=10.0,
        help="Seconds between prelaunch wait-gpu heartbeat lines (0 disables the periodic heartbeat).",
    )
    sp.add_argument(
        "--wait-timeout",
        type=float,
        default=0.0,
        help="Maximum seconds to wait before launch; 0 means no timeout.",
    )
    sp.add_argument(
        "--watch",
        action="store_true",
        help="After launch, immediately attach agentctl watch instead of returning.",
    )
    sp.add_argument(
        "--watch-tail",
        type=int,
        default=20,
        help="Tail lines to show when --watch is enabled.",
    )
    sp.add_argument(
        "--watch-poll",
        type=float,
        default=5.0,
        help="Seconds between watch status checks.",
    )
    sp.add_argument(
        "--watch-heartbeat",
        type=float,
        default=30.0,
        help="Seconds between watch heartbeat lines (0 disables the periodic heartbeat).",
    )
    sp.add_argument(
        "--watch-heartbeat-gpu",
        action="store_true",
        help="Include formatted GPU stats in watch heartbeat lines.",
    )
    sp.add_argument(
        "--watch-gpu",
        type=int,
        default=0,
        help="GPU index for watch threshold notifications.",
    )
    sp.add_argument(
        "--watch-gpu-poll",
        type=float,
        default=10.0,
        help="Seconds between GPU polls when --watch threshold notifications are enabled.",
    )
    sp.add_argument(
        "--watch-notify-gpu-idle",
        action="store_true",
        help=(
            "With --watch, keep watching until the GPU looks idle again "
            f"(defaults: VRAM<={DEFAULT_IDLE_GPU_MEMORY_USED_MIB}MiB and "
            f"power<={DEFAULT_IDLE_GPU_POWER_DRAW_W:g}W unless explicitly overridden)."
        ),
    )
    sp.add_argument(
        "--watch-notify-max-memory-used",
        type=int,
        default=None,
        help="With --watch, keep watching until GPU VRAM is at or below this threshold.",
    )
    sp.add_argument(
        "--watch-notify-max-power-draw",
        type=float,
        default=None,
        help="With --watch, keep watching until GPU power is at or below this threshold.",
    )
    sp.set_defaults(func=start, meta=True)
    _call_hook("register_args", sp)


def parse_start_command(name: str, mode: str, argv: list[str]) -> argparse.Namespace:
    # capabilities=(): agentctl does not wire maybe_complete yet, so its
    # --help must not advertise `complete` (gaps/agentctl-acli-complete.md).
    p = acli_args.ArgumentParser(prog=f"agentctl {name}", capabilities=())
    add_start_options(p)
    if "--" not in argv:
        if any(arg in {"-h", "--help"} for arg in argv):
            p.print_help()
            raise SystemExit(0)
        raise SystemExit(f"usage: agentctl {name} JOB [options] -- COMMAND ARG...")
    sep = argv.index("--")
    head = argv[:sep]
    child_argv = argv[sep + 1 :]
    args = p.parse_args(head)
    args.argv = child_argv
    args.mode = mode
    return args


def build_parser() -> argparse.ArgumentParser:
    # capabilities=(): agentctl does not wire maybe_complete yet, so its
    # --help must not advertise `complete` (gaps/agentctl-acli-complete.md).
    # Subparsers inherit the opt-out via acli's add_subparsers default.
    p = acli_args.ArgumentParser(
        description="Small local job helper for agent-managed runs.",
        capabilities=(),
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("start", help="start a job.")
    add_start_options(s)
    s.add_argument("argv", nargs=argparse.REMAINDER, help="Command after --.")
    s.set_defaults(func=start, mode="start")

    s = sub.add_parser("smoke", help="smoke a job.")
    add_start_options(s)
    s.add_argument("argv", nargs=argparse.REMAINDER, help="Command after --.")
    s.set_defaults(func=start, mode="smoke")

    s = sub.add_parser("_run-child", help=argparse.SUPPRESS)
    s.add_argument("--state-path", required=True)
    s.add_argument("--current-path", required=True)
    s.add_argument("--exit-status-path", required=True)
    s.add_argument("argv", nargs=argparse.REMAINDER, help=argparse.SUPPRESS)
    s.set_defaults(func=run_child)

    s = sub.add_parser("status", help="Show job status.")
    s.add_argument("job", nargs="?")
    s.add_argument(
        "--settle",
        type=float,
        default=0.0,
        help="Wait this many seconds before checking.",
    )
    s.add_argument("--tail", type=int, default=0, help="Also print last N log lines.")
    s.add_argument(
        "--running-only",
        "--live",
        "--active",
        action="store_true",
        dest="live_only",
        help="Show only jobs currently marked running (ignored when a job is named).",
    )
    s.add_argument(
        "--failed",
        action="store_true",
        dest="failed_only",
        help="Show only finished jobs with nonzero/unknown return codes.",
    )
    s.add_argument(
        "--all",
        action="store_true",
        dest="all_jobs",
        help="Show all current job records, including finished/stopped jobs.",
    )
    s.add_argument(
        "--recent",
        "--last",
        "--limit",
        type=int,
        default=0,
        dest="recent",
        help="Show only the most recent N jobs after filtering (0 = all).",
    )
    acli_args.add_standard_args(s)
    s.set_defaults(
        func=status,
        live_only=False,
        failed_only=False,
        all_jobs=True,
        where=False,
        completed_recent=0,
    )

    s = sub.add_parser(
        "list",
        help="List live jobs plus enough recent finished jobs to fill the default view; use --all for history.",
    )
    s.add_argument(
        "--settle",
        type=float,
        default=0.0,
        help="Wait this many seconds before checking.",
    )
    s.add_argument(
        "--tail", type=int, default=0, help="Also print last N log lines for each job."
    )
    s.add_argument(
        "--running-only",
        "--live",
        "--active",
        action="store_true",
        dest="live_only",
        help="Show only jobs currently marked running or waiting behind --after.",
    )
    s.add_argument(
        "--failed",
        action="store_true",
        dest="failed_only",
        help="Show only finished jobs with nonzero/unknown return codes.",
    )
    s.add_argument(
        "--all",
        action="store_true",
        dest="all_jobs",
        help="Show all current job records, including finished/stopped jobs.",
    )
    s.add_argument(
        "--show-last",
        type=int,
        default=DEFAULT_LIST_SHOW_LAST,
        help=(
            "In default list mode, target this many total live + recent finished "
            "jobs (default: %(default)s)."
        ),
    )
    s.add_argument(
        "--completed",
        type=int,
        default=None,
        dest="completed_recent",
        help=(
            "In default list mode, include this many recent finished jobs, "
            "overriding --show-last (0 = live only)."
        ),
    )
    s.add_argument(
        "--completed-min-elapsed",
        type=int,
        default=0,
        help="In default list mode, only show recent finished jobs that ran at least this many seconds.",
    )
    s.add_argument(
        "--recent",
        "--last",
        "--limit",
        type=int,
        default=0,
        dest="recent",
        help=(
            "Default list mode: include the most recent N finished jobs, overriding --show-last. "
            "With --all: show only the most recent N jobs after filtering (0 = all)."
        ),
    )
    acli_args.add_standard_args(s)
    s.set_defaults(
        func=status,
        job=None,
        live_only=False,
        failed_only=False,
        all_jobs=False,
        where=True,
    )

    s = sub.add_parser("tail", help="Print last log lines for a job.")
    s.add_argument("job")
    s.add_argument("-n", "--lines", type=int, default=40)
    s.set_defaults(func=tail)

    s = sub.add_parser(
        "note",
        help="Attach a one-line post-run analysis summary to agentctl/Aim/meta records.",
    )
    s.add_argument("job")
    s.add_argument("note", nargs="+", help="Short human summary of the completed run.")
    s.set_defaults(func=note_job)

    s = sub.add_parser(
        "cleanup-running",
        help="Escape hatch: delete stale <output>.running.md launch markers.",
    )
    s.add_argument(
        "outputs",
        nargs="*",
        help="Output path or the .running.md marker path itself. With none, scan the workspace.",
    )
    s.add_argument(
        "--dry-run",
        action="store_true",
        help="Report actions without deleting markers.",
    )
    s.add_argument(
        "-q", "--quiet", action="store_true", help="Only set the exit status."
    )
    s.set_defaults(func=cleanup_running)

    s = sub.add_parser(
        "watch",
        help="Stream log output until a job finishes, then print final status.",
    )
    s.add_argument("job")
    s.add_argument(
        "--poll", type=float, default=5.0, help="Seconds between log/status checks."
    )
    s.add_argument(
        "--heartbeat",
        type=float,
        default=30.0,
        help="Seconds between watch heartbeat lines (0 disables the periodic heartbeat).",
    )
    s.add_argument(
        "--tail",
        type=int,
        default=20,
        help="Print last N lines of existing log before streaming (0 = start from current end).",
    )
    s.add_argument(
        "--timeout",
        type=nonnegative_float,
        default=0.0,
        help="Maximum seconds to watch; 0 means no timeout.",
    )
    s.add_argument(
        "--gpu",
        type=int,
        default=0,
        help="GPU index to poll for optional threshold notifications.",
    )
    s.add_argument(
        "--heartbeat-gpu",
        action="store_true",
        help="Include formatted GPU stats in watch heartbeat lines.",
    )
    s.add_argument(
        "--gpu-poll",
        type=float,
        default=10.0,
        help="Seconds between GPU polls when threshold notifications are enabled (0 = reuse --poll).",
    )
    s.add_argument(
        "--gpu-patience",
        type=float,
        default=600.0,
        help=(
            "Warn if the watched job still has not shown GPU activity after this many seconds. "
            "Default is intentionally generous for large-model startup."
        ),
    )
    s.add_argument(
        "--notify-gpu-idle",
        action="store_true",
        help=(
            "Keep watching until the GPU looks idle again "
            f"(defaults: VRAM<={DEFAULT_IDLE_GPU_MEMORY_USED_MIB}MiB and "
            f"power<={DEFAULT_IDLE_GPU_POWER_DRAW_W:g}W unless explicitly overridden)."
        ),
    )
    s.add_argument(
        "--notify-max-memory-used",
        type=int,
        default=None,
        help=(
            "Emit a watch notification when GPU VRAM falls to this threshold or lower. "
            "If set, watch also stays attached after job completion until the threshold is met."
        ),
    )
    s.add_argument(
        "--notify-max-power-draw",
        type=float,
        default=None,
        help=(
            "Emit a watch notification when GPU power falls to this threshold or lower. "
            "Uses live nvidia-smi power, so it still reflects untracked jobs."
        ),
    )
    s.set_defaults(func=watch)

    s = sub.add_parser("wait", help="Wait until a job reaches a target status.")
    s.add_argument("job")
    s.add_argument(
        "--target",
        choices=["finished", "stopped", "running", "not-running"],
        default="not-running",
        help="Status to wait for. 'not-running' means any terminal status; a "
        "queued (waiting) --after run is still pending and keeps blocking.",
    )
    s.add_argument(
        "--poll", type=float, default=30.0, help="Seconds between status checks."
    )
    s.add_argument(
        "--heartbeat",
        type=float,
        default=30.0,
        help="Seconds between wait heartbeat lines (0 disables the periodic heartbeat).",
    )
    s.add_argument(
        "--gpu", type=int, default=0, help="GPU index used by --heartbeat-gpu."
    )
    s.add_argument(
        "--heartbeat-gpu",
        action="store_true",
        help="Include formatted GPU stats in wait heartbeat lines.",
    )
    s.add_argument(
        "--timeout",
        type=float,
        default=0.0,
        help="Maximum seconds to wait; 0 means no timeout.",
    )
    s.add_argument(
        "--tail",
        type=int,
        default=0,
        help="After the target status is reached, print the last N log lines (default: 0).",
    )
    s.set_defaults(func=wait_job)

    s = sub.add_parser(
        "wait-gpu", help="Wait for GPU VRAM usage to fall below a threshold."
    )
    s.add_argument("--gpu", type=int, default=0, help="GPU index to poll.")
    s.add_argument(
        "--max-memory-used",
        type=int,
        default=3000,
        help="Required VRAM threshold in MiB.",
    )
    s.add_argument("--poll", type=float, default=15.0, help="Seconds between checks.")
    s.add_argument(
        "--heartbeat",
        type=float,
        default=10.0,
        help="Seconds between wait-gpu heartbeat lines (0 disables the periodic heartbeat).",
    )
    s.add_argument(
        "--timeout",
        type=float,
        default=0.0,
        help="Maximum seconds to wait; 0 means no timeout.",
    )
    s.set_defaults(func=wait_gpu)

    s = sub.add_parser(
        "wait-work",
        help="Wait until new work appears: a new agentctl run and/or a new or "
        "updated on-deck/ queue entry. Works from an empty queue; prints "
        "what appeared and exits 0 (1 on --timeout).",
    )
    s.add_argument(
        "--runs",
        action="store_true",
        help="Wake on a new agentctl run: any run id not present at wait-work "
        "launch, restarts included (the watch-only wake: something new to watch).",
    )
    s.add_argument(
        "--on-deck",
        dest="on_deck",
        action="store_true",
        help="Wake on a new or modified on-deck/*.md queue entry; INDEX.md is "
        "derived and ignored (the tending wake: newly queued work). "
        "With neither --runs nor --on-deck, both sources wake.",
    )
    s.add_argument("--poll", type=float, default=10.0, help="Seconds between checks.")
    s.add_argument(
        "--heartbeat",
        type=float,
        default=60.0,
        help="Seconds between wait-work heartbeat lines (0 disables the periodic heartbeat).",
    )
    s.add_argument(
        "--timeout",
        type=float,
        default=0.0,
        help="Maximum seconds to wait; 0 means no timeout.",
    )
    s.set_defaults(func=wait_work)

    s = sub.add_parser("stop", help="Stop a running job process group.")
    s.add_argument("job")
    s.add_argument("--grace", type=float, default=5.0)
    s.set_defaults(func=stop)

    s = sub.add_parser("restart", help="Restart the current command for a job.")
    s.add_argument("job")
    s.add_argument("--grace", type=float, default=5.0)
    s.set_defaults(func=restart)

    s = sub.add_parser(
        "active",
        help="With a banner: author this session's .agentctl/active/<id> entry "
        "(banner + optional intend-to-edit scope) without launching a job. "
        "With no banner: list active (non-DONE) sessions and their status.",
    )
    s.add_argument(
        "banner",
        nargs="?",
        help="Line-1 present-tense status (quote it). A leading DONE marks the "
        "session complete. Omit entirely to list active sessions instead.",
    )
    s.add_argument(
        "paths",
        nargs="*",
        help="Intended-edit paths -> a `scope:` line 2 for peer overlap detection. "
        "Omit to leave any existing scope unchanged.",
    )
    s.add_argument(
        "-m",
        "--minutes",
        type=int,
        default=ACTIVE_STALE_MINUTES,
        help="List mode: freshness window in minutes (default %(default)s, the "
        "AGENTS.md stale threshold). 0 shows entries of any age, including "
        "stale/crashed ones.",
    )
    s.add_argument(
        "--done",
        action="store_true",
        help="List mode: also include DONE-prefixed (completed) sessions.",
    )
    s.add_argument(
        "--sweep",
        action="store_true",
        help="Archive stale entries out of active/: DONE-prefixed -> "
        ".agentctl/done/, others -> .agentctl/stale/, leaving only "
        "within-window entries so the peer-check find stays fast. Uses "
        "--minutes as the stale threshold; ignores banner/paths. Also "
        "runs silently on each foreground launch (start/smoke/restart).",
    )
    s.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="Sweep mode: report what would move without moving.",
    )
    s.add_argument(
        "--tending",
        action="store_true",
        help="Author mode: add a `tending: on-deck` header line — this session "
        "will keep launching queued work when it wakes (steward "
        "presence, read by `agentctl tending`). Without this flag an "
        "existing tending line is preserved.",
    )
    s.add_argument(
        "--until",
        help="Qualify --tending with a deadline, e.g. an absolute UTC time or "
        "'forever'. Informative for readers; not enforced — entry "
        "staleness is the enforcement.",
    )
    s.add_argument(
        "--no-tending",
        action="store_true",
        help="Author mode: drop the `tending:` line — this session no longer "
        "arms future launches (round ended with nothing wired).",
    )
    acli_args.add_standard_args(s)
    s.set_defaults(func=active_cmd)

    s = sub.add_parser(
        "others",
        help="List only your peers (your own active/<id> entry excluded) and "
        "lead with a count, so a stale 'peers present' belief is refuted "
        "in one line with nothing to parse. Pass your own session id.",
    )
    s.add_argument(
        "uuid",
        nargs="?",
        help="Your own session id, excluded from the list. Omit to resolve it "
        "from the environment; if none resolves, nothing is excluded.",
    )
    s.add_argument(
        "-m",
        "--minutes",
        type=int,
        default=ACTIVE_STALE_MINUTES,
        help="Freshness window in minutes (default %(default)s, the AGENTS.md "
        "stale threshold). 0 includes stale/crashed peers of any age.",
    )
    s.add_argument(
        "--done",
        action="store_true",
        help="Also include DONE-prefixed (completed) peers.",
    )
    acli_args.add_standard_args(s)
    s.set_defaults(func=others_cmd)

    s = sub.add_parser(
        "tending",
        help="Is any other session tending this project — a `tending:` header "
        "in its active entry, meaning it will launch more queued work "
        "when it wakes (e.g. an on-deck steward between hourly wakes)? "
        "Exit 0 = no other tending session; nonzero = listed. Pass your "
        "own session id to claim tending when the answer is no.",
    )
    s.add_argument(
        "uuid",
        nargs="?",
        help="Your own session id, excluded from the scan and — when no other "
        "session is tending — registered as your tending claim "
        "(`tending: on-deck` on your active entry, created placeholder "
        "if absent). Omit to resolve from the env (then nothing is "
        "claimed).",
    )
    s.add_argument(
        "--until",
        help="Deadline text for the registered claim, e.g. an absolute UTC "
        "time or 'forever'. Informative; staleness is the enforcement.",
    )
    s.add_argument(
        "-m",
        "--minutes",
        type=int,
        default=ACTIVE_STALE_MINUTES,
        help="Freshness window in minutes (default %(default)s, the AGENTS.md "
        "stale threshold). 0 includes stale/crashed entries of any age.",
    )
    s.add_argument(
        "--done",
        action="store_true",
        help="Also count DONE-prefixed (completed) entries.",
    )
    acli_args.add_standard_args(s)
    s.set_defaults(func=tending_cmd)

    s = sub.add_parser(
        "alone",
        help="Block until no other active peer remains (the waiting form of "
        "`others`), then exit 0; exit nonzero on --timeout. For "
        "intentionally project-serial steps. Pass your own session id; "
        "on success it registers your entry to claim the floor.",
    )
    s.add_argument(
        "uuid",
        nargs="?",
        help="Your own session id, excluded from the wait and registered as an "
        "active claim once you are alone. Omit to resolve from the env "
        "(then nothing is excluded or claimed).",
    )
    s.add_argument(
        "scope",
        nargs="*",
        help="Optional intend-to-edit paths -> the `scope:` line of the entry "
        "registered when you become alone (pairs with --banner).",
    )
    s.add_argument(
        "-b",
        "--banner",
        help="Status line to register on success, folding `agentctl active` "
        "into the wait (register your real status + scope and wait in one "
        "go). Without it the success claim is a placeholder.",
    )
    s.add_argument(
        "-m",
        "--minutes",
        type=int,
        default=ACTIVE_STALE_MINUTES,
        help="Freshness window in minutes (default %(default)s). A crashed peer "
        "clears when it ages past this; 0 waits on peers of any age.",
    )
    s.add_argument(
        "--done",
        action="store_true",
        help="Count DONE-prefixed (completed) entries as peers to wait on.",
    )
    s.add_argument(
        "--poll", type=float, default=5.0, help="Seconds between peer checks."
    )
    s.add_argument(
        "--heartbeat",
        type=float,
        default=30.0,
        help="Seconds between repeated alone_wait events while waiting (0 disables repeats).",
    )
    s.add_argument(
        "--timeout",
        type=float,
        default=0.0,
        help="Maximum seconds to wait; 0 means wait forever.",
    )
    acli_args.add_standard_args(s)
    s.set_defaults(func=alone_cmd)

    _call_hook("register_verbs", sub)

    return p


def main() -> int:
    _load_plugins()
    ensure_state_ignored()
    raw = sys.argv[1:]
    if raw[:1] == ["start"]:
        args = parse_start_command("start", "start", raw[1:])
        return start(args)
    if raw[:1] == ["smoke"]:
        args = parse_start_command("smoke", "smoke", raw[1:])
        return start(args)
    args = build_parser().parse_args(raw)
    if getattr(args, "argv", None) and args.argv[:1] == ["--"]:
        args.argv = args.argv[1:]
    return args.func(args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit(130) from None
    except BrokenPipeError:
        # Let common truncating consumers such as `head` close the pipe without
        # turning a successful status/list command into a traceback.
        try:
            sys.stdout.close()
        finally:
            raise SystemExit(0)
