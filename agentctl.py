#!/usr/bin/env python3
from __future__ import annotations

import argparse
import atexit
import datetime as dt
import importlib
import json
import os
from pathlib import Path
import re
import shlex
import signal
import subprocess
import sys
import time


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
DECLARED_IO_FILENAME = "declared.json"
PROPAGATE_FILENAME = "propagate.json"


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


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run_id() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def instance_name(job: str, serial: int) -> str:
    return f"{job}-{serial:04d}"


def parse_utc(ts: str) -> dt.datetime:
    return dt.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)


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
    return int(round(total))


def format_duration(seconds: float | int | None) -> str:
    if seconds is None:
        return "?"
    total = max(0, int(round(float(seconds))))
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


def agent_session_id() -> str:
    """The launching agent's session id for active-sessions upkeep, or "".

    Empty when this invocation is inside an agentctl-launched job
    (LAUNCH_DEPTH > 0) — a job is not an agent — or when no session id is
    advertised. Otherwise the first set of SESSION_ID_ENVS wins, so plain
    `./agentctl` adopts the harness's ambient session id with no per-call
    setup.
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
    return ""


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
        print(f"warning: could not update active session {path}: {exc}", file=sys.stderr)


def active_scope_path(raw: str) -> str:
    """Normalize one intend-to-edit path for an active-session `scope:` line.

    Scope paths are project-root-relative so the prefix-match overlap check
    (AGENTS.md § Active sessions) lines up across peers regardless of each
    agent's cwd. An absolute path under ROOT is made relative; a leading
    `./` is stripped; a trailing `**` is kept. Everything else is preserved
    verbatim, and existence is not required — the path may name a file the
    agent is about to create.
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

    path = ACTIVE / sid
    old_scope: str | None = None
    body: list[str] = []
    if path.exists():
        rest = path.read_text(encoding="utf-8", errors="replace").splitlines()[1:]
        if rest and rest[0].startswith("scope:"):
            old_scope = rest[0]
            rest = rest[1:]
        body = rest

    out = [banner]
    scope_line = ("scope: " + " ".join(scope_paths)) if scope_paths else old_scope
    if scope_line:
        out.append(scope_line)
    out.extend(body)

    try:
        ACTIVE.mkdir(parents=True, exist_ok=True)
        tmp = path.parent / (path.name + ".tmp")
        tmp.write_text("\n".join(out) + "\n", encoding="utf-8")
        tmp.replace(path)
    except OSError as exc:
        print(f"agentctl active: could not write {path}: {exc}", file=sys.stderr)
        return 1

    try:
        shown: Path | str = path.relative_to(ROOT)
    except ValueError:
        shown = path
    print(f"active {shown}: {banner}")
    if scope_line:
        print(f"  {scope_line}")
    return 0


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

    Output is to stdout, newest first, one entry per block:

        .agentctl/active/<id>  (12m34s ago)  status line one  (self)
            scope: pkg/a/** pkg/b
    """
    minutes = max(0, int(getattr(args, "minutes", ACTIVE_STALE_MINUTES)))
    include_done = bool(getattr(args, "done", False))
    self_id = agent_session_id()
    now = time.time()

    if not ACTIVE.is_dir():
        print("no active sessions (.agentctl/active/ does not exist)")
        return 0

    rows: list[tuple[float, str, str, str, bool]] = []
    for path in ACTIVE.iterdir():
        if not path.is_file():
            continue
        try:
            mtime = path.stat().st_mtime
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        lines = text.splitlines()
        line1 = lines[0].strip() if lines else ""
        is_done = line1.startswith("DONE")
        if is_done and not include_done:
            continue
        age = now - mtime
        if minutes and age > minutes * 60:
            continue
        scope = lines[1].strip() if len(lines) > 1 and lines[1].startswith("scope:") else ""
        rows.append((mtime, path.name, line1, scope, path.name == self_id))

    if not rows:
        window = "any age" if not minutes else f"last {minutes}m"
        kind = "sessions" if include_done else "non-DONE sessions"
        print(f"no active {kind} ({window})")
        return 0

    rows.sort(key=lambda r: r[0], reverse=True)
    for mtime, name, line1, scope, is_self in rows:
        rel = f".agentctl/active/{name}"
        age = format_duration(now - mtime)
        marker = "  (self)" if is_self else ""
        print(f"{rel}  ({age} ago)  {line1 or '(empty)'}{marker}")
        if scope:
            print(f"    {scope}")
    return 0


def active_cmd(args) -> int:
    """Dispatch the `active` verb: list with no banner, author with one."""
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
    parts = [part.decode("utf-8", errors="replace") for part in raw.split(b"\0") if part]
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
            if started_epoch is not None and proc_epoch is not None and proc_epoch + 60 < started_epoch:
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
    if leader_pid > 0 and leader_pid in members and pid_matches_state(leader_pid, state):
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
            if process_group_alive(pgid_int) and process_group_matches_state(pgid_int, state):
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
        if process_group_members(pgid_int) and not process_group_matches_state(pgid_int, state):
            return True
    return False


def refresh_state(state: dict) -> dict:
    state = apply_exit_status_record(state)
    if (
        state.get("status") == "finished"
        and state.get("returncode") == "unknown"
        and state_alive(state)
    ):
        state["status"] = "running"
        state.pop("finished_at", None)
        state.pop("returncode", None)
        update_state_files(state)
    if state.get("status") == "running" and not state_alive(state):
        if process_visibility_limited() and not state_liveness_refuted_by_visible_process(state):
            state["_liveness_note"] = "process visibility limited; not marking finished"
            return state
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
    finished_at = str(record.get("finished_at") or state.get("finished_at") or utc_now())
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
        raise SystemExit(f"failed to source env script {script_path}: exit {exc.returncode}") from exc
    updated = env.copy()
    for entry in out.split(b"\0"):
        if not entry:
            continue
        key, sep, value = entry.partition(b"=")
        if not sep:
            continue
        updated[key.decode("utf-8", errors="replace")] = value.decode("utf-8", errors="replace")
    return updated


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
        out = subprocess.check_output(["git", *args], cwd=ROOT, text=True, stderr=subprocess.DEVNULL)
    except Exception:
        return ""
    return out.strip()


# ---- Input/output declaration helpers ----

_INTERPRETERS = frozenset({"bash", "sh", "zsh", "python", "python3", "perl", "node", "ruby", "Rscript"})


def compute_sha256(path: str | Path) -> str:
    """SHA256 of a file's bytes, hex-encoded. Streams in chunks (large tensors
    don't fit in memory). Caller is responsible for whether the cost is justified
    — used by --input-hash, --output-hash, and the script fingerprint."""
    import hashlib as _hashlib

    h = _hashlib.sha256()
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
            if cst.st_mtime > newest:
                newest = cst.st_mtime
        rec["size"] = total
        rec["mtime"] = dt.datetime.fromtimestamp(newest, tz=dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        rec["size"] = st.st_size
        rec["mtime"] = dt.datetime.fromtimestamp(st.st_mtime, tz=dt.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )
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
            print(f"warning: sha256 failed for input {key}={path}: {exc}", file=sys.stderr)
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
    payload = {
        kind: dict(values)
        for kind, values in _DECLARED_IO.items()
        if values
    }
    if not payload:
        return
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(f"{path.suffix}.tmp")
        tmp.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
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


def _declared_io_items(declared_file: Path, kind: str, payload: dict) -> list[tuple[str, str]]:
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
            raise ValueError(f"{declared_file}: {kind}.{key} must be a non-empty path string")
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
                print(f"warning: sha256 failed for output {key}: {exc}", file=sys.stderr)
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
        if p.exists() and p.is_file():
            candidate = p
            break
    if candidate is None:
        if not argv:
            return None
        p = Path(argv[0])
        if not p.is_absolute():
            p = ROOT / p
        if not p.exists() or not p.is_file():
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
        setup.append(("source_env", ",".join(str(item) for item in state["source_env"])))
    if depends_on:
        setup.append(("depends_on_jobs", ",".join(depends_on)))
    if state.get("aim_run_hash"):
        setup.append(("aim_run_hash", state["aim_run_hash"]))
    results: list[tuple[str, str]] = []
    machine = [
        ("git_branch", state.get("git_branch", "")),
        ("git_commit", state.get("git_commit", "")),
        ("started_at", state["started_at"]),
        ("pid", str(state["pid"])),
    ]
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
            new = fn(state, meta, output_path=output, log_path=state["log_path"], build_meta=_build)
        except Exception as exc:
            print(f"warning: plugin {p.__name__} on_meta_built failed: {exc}", file=sys.stderr)
            continue
        if new is not None:
            meta = new
    Path(f"{output}.meta.md").parent.mkdir(parents=True, exist_ok=True)
    Path(f"{output}.meta.md").write_text(meta, encoding="utf-8")
    return state


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
        marker = candidate if str(candidate).endswith(".running.md") else running_marker_path(candidate)
        output = Path(str(marker)[: -len(".running.md")]) if str(marker).endswith(".running.md") else candidate
        if marker.exists() or completion_sidecar(output) is not None:
            return {
                "kind": "running_marker",
                "spec": spec,
                "marker_path": str(marker),
                "output_path": str(output),
            }

    raise SystemExit(
        f"--after target not found as an agentctl job or .running.md artifact: {spec}"
    )


def after_target_done(target: dict) -> tuple[bool, int, str]:
    kind = target.get("kind")
    if kind == "job":
        dep_state = load_job(str(target["job"]))
        status = dep_state.get("status", "")
        if status in {"running", "waiting"}:
            return False, 0, f"job={dep_state['job']} status={status} elapsed={elapsed_estimate_text(dep_state)}"
        if status == "finished" and dep_state.get("returncode") in (None, "", "unknown"):
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
        if rc != 0:
            return True, rc, f"job={dep_state['job']} ended status={status} returncode={dep_state.get('returncode')}"
        return True, 0, f"job={dep_state['job']} ended status={status} returncode={dep_state.get('returncode', '')}"

    if kind == "running_marker":
        marker = Path(str(target["marker_path"]))
        output = Path(str(target["output_path"]))
        if not marker.exists():
            sidecar = completion_sidecar(output)
            if sidecar is not None:
                return True, 0, f"marker gone: {marker} sidecar={sidecar}"
            return True, 1, f"marker gone without completion sidecar: {marker} out={output}"
        fields = marker_fields(marker)
        output = output_for_marker(marker, fields)
        sidecar = completion_sidecar(output)
        pid_state = marker_pid_status(fields)
        if sidecar is not None and pid_state != "running":
            return True, 0, f"marker completed: {marker} sidecar={sidecar}"
        if pid_state == "running":
            return False, 0, f"marker={marker} pid={fields.get('pid', '') or '?'} running"
        return True, 1, f"marker interrupted: {marker} pid={fields.get('pid', '') or '?'} out={output}"

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
            print(f"timeout waiting for --after targets: {'; '.join(pending)}", file=sys.stderr)
            return 1
        time.sleep(poll)


def mark_wait_failed(state_path: Path, current: Path, exit_status_path: Path, rc: int) -> None:
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
        print(f"warning: wait-after failure state update failed: {exc!r}", file=sys.stderr)


def start(args: argparse.Namespace) -> int:
    if not args.argv:
        raise SystemExit("missing command after --")
    if args.watch and args.after:
        raise SystemExit("--after is not supported with --watch; start queued work detached, then watch the job")
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
    # --output-hash KEY=PATH also declares an output and flags it for sha256 at completion.
    declared_outputs: dict = {}
    primary_output_path: Path | None = None
    for spec in (args.output or []):
        key, path = parse_keypath(spec, default_key="primary")
        p = Path(path).expanduser()
        if not p.is_absolute():
            p = (ROOT / p).resolve(strict=False)
        declared_outputs[key] = {"path": str(p)}
        if primary_output_path is None:
            primary_output_path = p
    for spec in (args.output_hash or []):
        key, path = parse_keypath(spec, default_key="primary")
        p = Path(path).expanduser()
        if not p.is_absolute():
            p = (ROOT / p).resolve(strict=False)
        rec = declared_outputs.get(key) or {}
        rec["path"] = str(p)
        rec["needs_hash"] = True
        declared_outputs[key] = rec
        if primary_output_path is None:
            primary_output_path = p
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

    for spec in (args.input or []):
        key, path = parse_keypath(spec)
        _record_input(key, path, raw=False, do_hash=False)
    for spec in (args.input_raw or []):
        key, path = parse_keypath(spec)
        _record_input(key, path, raw=True, do_hash=False)
    for spec in (args.input_hash or []):
        key, path = parse_keypath(spec)
        _record_input(key, path, raw=False, do_hash=True)

    state_path = run_dir / "state.json"
    exit_status_path = run_dir / "exit-status.json"
    launch_gpu_stats = None
    if args.gpu_patience > 0:
        try:
            launch_gpu_stats = query_gpu_stats(args.watch_gpu)
        except Exception as exc:
            print(f"warning: failed to snapshot launch gpu stats for gpu={args.watch_gpu}: {exc}", file=sys.stderr)

    env = os.environ.copy()
    for script in args.source_env:
        env = source_env_script(env, script)
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
    for item in args.env:
        key, _, value = item.partition("=")
        if not key or not _:
            raise SystemExit(f"expected --env KEY=VALUE, got {item!r}")
        env[key] = value

    # Build the final argv for the child: user's argv + translated --input flags.
    final_argv = list(args.argv)
    for key, path in input_translations:
        final_argv.append(f"--{key}={path}")

    # Producer-flagged propagation (static at launch). Run-time-computed facts
    # arrive via $AGENTCTL_RUN_DIR/propagate.json (read at completion in run_child).
    propagate: dict = {}
    if args.propagate_json:
        try:
            parsed = json.loads(args.propagate_json)
            if not isinstance(parsed, dict):
                raise SystemExit(f"--propagate-json must be a JSON object, got {type(parsed).__name__}")
            propagate = parsed
        except (json.JSONDecodeError, ValueError) as exc:
            raise SystemExit(f"--propagate-json failed to parse: {exc}")

    # Script: explicit --script PATH override wins; otherwise heuristic on argv.
    if args.script:
        script_rec = script_fingerprint(args.script)
    else:
        script_rec = detect_script(final_argv) or {}

    # Pre-launch state: canonical fields plugins can read/extend.
    state = {
        "context_note": args.context_note,
        "pre_run_note": args.context_note,
        "depends_on": [slug(dep) for dep in args.depends_on],
        "exit_status_path": str(exit_status_path),
        "argv": final_argv,
        "cwd": str(ROOT),
        "git_branch": git_value(["branch", "--show-current"]),
        "git_commit": git_value(["rev-parse", "HEAD"]),
        "headline_path": str(headline_path),
        "inputs": declared_inputs,
        "job": job,
        "launch_name": launch_name,
        "log_path": str(log_path),
        "meta_path": str(Path(f"{output_path}.meta.md")) if output_path is not None else "",
        "mode": args.mode,
        "output_path": str(output_path) if output_path is not None else "",
        "outputs": declared_outputs,
        "parent_run": parent_run_id,
        "propagate": propagate,
        "run_dir": str(run_dir),
        "run_id": rid,
        "runtime_estimate": runtime_estimate,
        "runtime_estimate_seconds": runtime_estimate_seconds,
        "script": script_rec,
        "serial": serial,
        "source_env": list(args.source_env),
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
    child_argv = final_argv
    if not args.watch:
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
    # write_meta runs in run_child for non-watch launches (so the dump record is in
    # state.json before run_child's completion path needs to read it). For --watch,
    # run_child is bypassed and start owns the full lifecycle, so write_meta here.
    if args.watch and output_path is not None and args.meta:
        state = write_meta(state)
        update_state_files(state)
    print(f"started {launch_name} job={job} serial={serial} run={rid} pid={proc.pid}")
    print(f"log: {log_path}")
    refresh_active_register(
        summary=f"agentctl {args.mode} {launch_name}: {command_string(final_argv)}",
        note=f"agentctl: started {launch_name} run={rid}",
    )
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
        print(f"warning: wait-after failed before payload launch: {exc!r}", file=sys.stderr)
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
        print(f"warning: deferred wait-gpu failed before payload launch: {exc!r}", file=sys.stderr)
        mark_wait_failed(state_path, current, exit_status_path, 1)
        return 1
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


def status(args: argparse.Namespace) -> int:
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
            states = [state for state in states if state.get("status") == "running"]
        elif getattr(args, "where", False) and not getattr(args, "all_jobs", False):
            running = [state for state in states if state.get("status") == "running"]
            min_elapsed = max(0, getattr(args, "completed_min_elapsed", 0))
            completed = [
                state
                for state in states
                if state.get("status") == "finished"
                and ((elapsed_seconds(state) or 0) >= min_elapsed or state_failed(state))
            ]
            completed_n = args.recent if args.recent and args.recent > 0 else args.completed_recent
            completed = completed[: max(0, completed_n)]
            groups = [("Running Jobs", running), ("Recent Finished Jobs", completed)]
            states = [*running, *completed]
        elif args.recent and args.recent > 0:
            states = states[: args.recent]
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

    headline_path = Path(state.get("headline_path", "")) if state.get("headline_path") else None
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
        skip = {".git", ".agentctl", "runs", "__pycache__", ".venv", ".pixi", "node_modules"}
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
                print(f"{'would-remove' if path.exists() and args.dry_run else 'missing'} {path}")
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
            print(f"{state} kept {path} pid={fields.get('pid', '') or '?'} out={output}")
    if not args.quiet:
        dry_run_part = f", {would_remove} would-remove" if args.dry_run else ""
        print(f"{removed} removed{dry_run_part}, {kept} kept")
    return 0


def wait_job(args: argparse.Namespace) -> int:
    deadline = time.time() + args.timeout if args.timeout > 0 else None
    next_report = 0.0
    heartbeat_interval = max(0.0, float(getattr(args, "heartbeat", 30.0) or 0.0))
    while True:
        state = load_job(args.job)
        status = state.get("status", "")
        if args.target == "not-running":
            done = status != "running"
        else:
            done = status == args.target
        if done:
            bits = [state["job"], state["run_id"], status]
            if status_returncode_text(state):
                bits.append(f"returncode={status_returncode_text(state)}")
            if state.get("log_path"):
                bits.append(f"log={state['log_path']}")
            print(" ".join(bits))
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


def query_gpu_stats(gpu_index: int) -> dict[str, float | int | None]:
    out = subprocess.check_output(
        [
            "nvidia-smi",
            f"--id={gpu_index}",
            "--query-gpu=index,memory.used,power.draw,utilization.gpu",
            "--format=csv,noheader,nounits",
        ],
        text=True,
        stderr=subprocess.STDOUT,
    )
    line = out.strip().splitlines()[0]
    fields = [field.strip() for field in line.split(",")]
    if len(fields) != 4:
        raise RuntimeError(f"unexpected nvidia-smi output for gpu {gpu_index}: {line!r}")
    return {
        "gpu": int(fields[0]),
        "memory_used_mib": int(fields[1]),
        "power_draw_w": parse_nvidia_smi_number(fields[2]),
        "utilization_gpu_pct": parse_nvidia_smi_number(fields[3]),
    }


def query_gpu_stats_smoothed(
    gpu_index: int,
    *,
    samples: int = DEFAULT_HEARTBEAT_GPU_SMOOTH_SAMPLES,
    interval: float = DEFAULT_HEARTBEAT_GPU_SMOOTH_INTERVAL_S,
) -> dict[str, float | int | None]:
    sample_count = max(1, int(samples))
    sleep_interval = max(0.0, float(interval))
    stats_list: list[dict[str, float | int | None]] = []
    for idx in range(sample_count):
        if idx and sleep_interval > 0:
            time.sleep(sleep_interval)
        stats_list.append(query_gpu_stats(gpu_index))
    merged = dict(stats_list[-1])
    utils = [float(s["utilization_gpu_pct"]) for s in stats_list if s.get("utilization_gpu_pct") is not None]
    powers = [float(s["power_draw_w"]) for s in stats_list if s.get("power_draw_w") is not None]
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
    heartbeat_interval = max(0.0, float(max(10.0, poll) if heartbeat is None else heartbeat))
    last_report = 0.0
    while True:
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
        if heartbeat_interval > 0 and (last_report == 0.0 or now - last_report >= heartbeat_interval):
            print(f"[wait-gpu] {format_gpu_stats(stats)} target<={max_memory_used}MiB", flush=True)
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
    return args.notify_max_memory_used is not None or args.notify_max_power_draw is not None


def gpu_below_watch_thresholds(stats: dict[str, float | int | None], args: argparse.Namespace) -> bool:
    memory_ok = args.notify_max_memory_used is None or int(stats["memory_used_mib"]) <= args.notify_max_memory_used
    power_draw = stats.get("power_draw_w")
    power_ok = args.notify_max_power_draw is None or (
        power_draw is not None and float(power_draw) <= args.notify_max_power_draw
    )
    return memory_ok and power_ok


def format_gpu_stats(stats: dict[str, float | int | None]) -> str:
    bits = [f"gpu={int(stats['gpu'])}", f"VRAM={int(stats['memory_used_mib'])}MiB"]
    power_draw = stats.get("power_draw_w_avg", stats.get("power_draw_w"))
    util = stats.get("utilization_gpu_pct_avg", stats.get("utilization_gpu_pct"))
    util_peak = stats.get("utilization_gpu_pct_max")
    bits.append(f"power={power_draw:.1f}W" if power_draw is not None else "power=unavailable")
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
    if launch_power is not None and current_power is not None and float(current_power) >= float(launch_power) + 15.0:
        return True
    launch_util = launch_stats.get("utilization_gpu_pct")
    current_util = stats.get("utilization_gpu_pct")
    if current_util is not None and float(current_util) >= 10.0:
        if launch_util is None or float(current_util) >= float(launch_util) + 10.0:
            return True
    return False


def poll_watch_gpu_state(
    *,
    gpu: int,
    args: argparse.Namespace,
    launch_gpu_stats: dict[str, float | int | None] | None,
    last_gpu_below: bool | None,
    last_gpu_error: str,
    gpu_activity_seen: bool,
) -> tuple[bool | None, str, bool, bool, dict[str, float | int | None] | None]:
    try:
        stats = query_gpu_stats(gpu)
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
            print(f"[watch] gpu query failed for gpu={gpu}: {message}", file=sys.stderr, flush=True)
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


def watch(args: argparse.Namespace, proc: subprocess.Popen | None = None) -> int:
    """Stream new log lines until the job is no longer running, then print final status."""
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
        data = log_path.read_bytes()
        if args.tail > 0:
            lines = data.splitlines(keepends=True)
            tail_lines = lines[-args.tail :]
            sys.stdout.buffer.write(b"".join(tail_lines))
            sys.stdout.buffer.flush()
        else:
            offset = len(data)
    print(f"[watch] job={state['job']} run={state['run_id']} status={state.get('status','?')} log={log_path}", flush=True)
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
        if proc_returncode is None:
            proc_returncode = reap_proc(proc)
        state = load_job(args.job)
        if proc is not None and proc_returncode is not None:
            if int(state.get("pid", -1)) == proc.pid and (
                state.get("status") == "running" or state.get("returncode") == "unknown"
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
        if watching_gpu and now >= next_gpu_poll_at:
            next_gpu_poll_at = now + gpu_poll
            last_gpu_below, last_gpu_error, gpu_activity_seen, gpu_polled, last_gpu_stats = poll_watch_gpu_state(
                gpu=args.gpu,
                args=args,
                launch_gpu_stats=launch_gpu_stats,
                last_gpu_below=last_gpu_below,
                last_gpu_error=last_gpu_error,
                gpu_activity_seen=gpu_activity_seen,
            )
            if gpu_polled and waiting_for_gpu_thresholds:
                gpu_done = bool(last_gpu_below)
        if watching_gpu and state.get("status") == "running" and gpu_activity_seen and last_gpu_stats is not None:
            util = last_gpu_stats.get("utilization_gpu_pct")
            used = int(last_gpu_stats["memory_used_mib"])
            if util is not None and float(util) <= 0.0 and used > DEFAULT_ZERO_COMPUTE_MIN_VRAM_MIB:
                if zero_compute_started_at == 0.0:
                    zero_compute_started_at = now
                    zero_compute_last_report_at = now
                zero_elapsed = now - zero_compute_started_at
                if zero_elapsed >= DEFAULT_ZERO_COMPUTE_REPORT_INTERVAL_S and (
                    now - zero_compute_last_report_at >= DEFAULT_ZERO_COMPUTE_REPORT_INTERVAL_S
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
                print(f"[watch] launch gpu baseline: {format_gpu_stats(launch_gpu_stats)}", flush=True)
            gpu_patience_warned = True
        if heartbeat_interval > 0 and (next_heartbeat_at == 0.0 or now >= next_heartbeat_at):
            heartbeat_line = (
                f"[watch] heartbeat job={state['job']} status={state.get('status', '?')} "
                f"elapsed={elapsed_estimate_text(state)}"
            )
            if watching_gpu and last_gpu_below is not None:
                heartbeat_line += " gpu_threshold=" + ("met" if last_gpu_below else "pending")
            if gpu_patience > 0:
                heartbeat_line += " gpu_activity=" + ("seen" if gpu_activity_seen else "not-yet-seen")
            if getattr(args, "heartbeat_gpu", False):
                gpu_stats = None
                try:
                    gpu_stats = query_gpu_stats_smoothed(args.gpu)
                except Exception as exc:
                    gpu_stats = last_gpu_stats
                    if gpu_stats is None:
                        heartbeat_line += f" gpu_query_failed={exc}"
                if gpu_stats is not None:
                    heartbeat_line += " " + format_gpu_stats(gpu_stats)
            print(heartbeat_line, flush=True)
            next_heartbeat_at = now + heartbeat_interval
        current_status = state.get("status", "")
        if current_status != "running":
            if watching_gpu:
                last_gpu_below, last_gpu_error, gpu_activity_seen, gpu_polled, last_gpu_stats = poll_watch_gpu_state(
                    gpu=args.gpu,
                    args=args,
                    launch_gpu_stats=launch_gpu_stats,
                    last_gpu_below=last_gpu_below,
                    last_gpu_error=last_gpu_error,
                    gpu_activity_seen=gpu_activity_seen,
                )
                if gpu_polled and waiting_for_gpu_thresholds:
                    gpu_done = bool(last_gpu_below)
            if not job_done_reported:
                done_bits = [f"\n[watch] done: {state['job']} {state['run_id']} status={current_status}"]
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
                return status_returncode_exit_code(state) if current_status == "finished" else 0
            if not waiting_for_gpu_reported:
                rc_text = status_returncode_text(state)
                suffix = f" returncode={rc_text}" if rc_text else ""
                print(
                    f"[watch] job finished but continuing until gpu={args.gpu} satisfies "
                    f"{format_gpu_watch_thresholds(args)}{suffix}",
                    flush=True,
                )
                waiting_for_gpu_reported = True
        time.sleep(args.poll)


def stop(args: argparse.Namespace) -> int:
    state = load_job(args.job)
    if state.get("status") != "running":
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


def restart(args: argparse.Namespace) -> int:
    state = load_job(args.job)
    if state.get("status") == "running":
        stop(argparse.Namespace(job=args.job, grace=args.grace))
    start_args = argparse.Namespace(
        argv=state["argv"],
        context_note=state.get("context_note", ""),
        depends_on=state.get("depends_on", []),
        after=[],
        after_poll=10.0,
        after_heartbeat=30.0,
        after_timeout=0.0,
        env=[],
        gpus="",
        input_file="",
        # Plugin-managed in on_restart but defaulted here so the namespace exists.
        input=[],
        input_raw=[],
        input_hash=[],
        output=[],
        output_hash=[],
        script="",
        propagate_json="",
        job=state["job"],
        log="",
        meta=bool(state.get("output_path")),
        mode=state.get("mode", "start"),
        run_id="",
        runtime_estimate=state.get("runtime_estimate", ""),
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
            "Use only for mechanical dependencies; inspect results manually when follow-on "
            "choice depends on completed content."
        ),
    )
    sp.add_argument("--after-poll", type=float, default=10.0, help="Seconds between --after dependency checks.")
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
    sp.add_argument("--env", action="append", default=[], help="Extra environment KEY=VALUE.")
    sp.add_argument("--gpus", default="", help="CUDA_VISIBLE_DEVICES value.")
    sp.add_argument("--input-file", default="", help="Input file path exposed as AGENTCTL_INPUT_FILE.")
    sp.add_argument("--log", default="", help="Log file path. Defaults under .agentctl/runs/.")
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
            "Declare an output as KEY=PATH (repeatable). The first declared output is the primary "
            "(its path anchors .meta.md). A bare PATH (no '=') is accepted as shorthand for primary=PATH. "
            "Each output gets a <path>.meta.json sidecar at completion pointing back at the run."
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
    sp.add_argument("--wait-gpu", type=int, default=0, help="GPU index to poll before launch.")
    sp.add_argument(
        "--wait-max-memory-used",
        type=int,
        default=None,
        help="Before launch, wait until this GPU VRAM threshold is met.",
    )
    sp.add_argument("--wait-poll", type=float, default=10.0, help="Seconds between prelaunch GPU checks.")
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
    sp.add_argument("--watch-tail", type=int, default=20, help="Tail lines to show when --watch is enabled.")
    sp.add_argument("--watch-poll", type=float, default=5.0, help="Seconds between watch status checks.")
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
    sp.add_argument("--watch-gpu", type=int, default=0, help="GPU index for watch threshold notifications.")
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
    p = argparse.ArgumentParser(prog=f"agentctl {name}")
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
    p = argparse.ArgumentParser(description="Small local job helper for agent-managed runs.")
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
    s.set_defaults(func=status, live_only=False, failed_only=False, all_jobs=True,
                   where=False, completed_recent=0)

    s = sub.add_parser(
        "list",
        help="List running jobs plus a small recent-completed tail by default; use --all for history.",
    )
    s.add_argument(
        "--settle",
        type=float,
        default=0.0,
        help="Wait this many seconds before checking.",
    )
    s.add_argument("--tail", type=int, default=0, help="Also print last N log lines for each job.")
    s.add_argument(
        "--running-only",
        "--live",
        "--active",
        action="store_true",
        dest="live_only",
        help="Show only jobs currently marked running.",
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
        "--completed",
        type=int,
        default=2,
        dest="completed_recent",
        help="In default list mode, include this many recent non-running jobs (0 = live only).",
    )
    s.add_argument(
        "--completed-min-elapsed",
        type=int,
        default=60,
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
            "Default list mode: include the most recent N non-running jobs. "
            "With --all: show only the most recent N jobs after filtering (0 = all)."
        ),
    )
    s.set_defaults(func=status, job=None, live_only=False, failed_only=False,
                   all_jobs=False, where=True)

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
    s.add_argument("--dry-run", action="store_true", help="Report actions without deleting markers.")
    s.add_argument("-q", "--quiet", action="store_true", help="Only set the exit status.")
    s.set_defaults(func=cleanup_running)

    s = sub.add_parser(
        "watch",
        help="Stream log output until a job finishes, then print final status.",
    )
    s.add_argument("job")
    s.add_argument("--poll", type=float, default=5.0, help="Seconds between log/status checks.")
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
    s.add_argument("--gpu", type=int, default=0, help="GPU index to poll for optional threshold notifications.")
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
        help="Status to wait for. 'not-running' means any terminal/non-running status.",
    )
    s.add_argument("--poll", type=float, default=30.0, help="Seconds between status checks.")
    s.add_argument(
        "--heartbeat",
        type=float,
        default=30.0,
        help="Seconds between wait heartbeat lines (0 disables the periodic heartbeat).",
    )
    s.add_argument("--gpu", type=int, default=0, help="GPU index used by --heartbeat-gpu.")
    s.add_argument(
        "--heartbeat-gpu",
        action="store_true",
        help="Include formatted GPU stats in wait heartbeat lines.",
    )
    s.add_argument("--timeout", type=float, default=0.0, help="Maximum seconds to wait; 0 means no timeout.")
    s.set_defaults(func=wait_job)

    s = sub.add_parser("wait-gpu", help="Wait for GPU VRAM usage to fall below a threshold.")
    s.add_argument("--gpu", type=int, default=0, help="GPU index to poll.")
    s.add_argument("--max-memory-used", type=int, default=3000, help="Required VRAM threshold in MiB.")
    s.add_argument("--poll", type=float, default=15.0, help="Seconds between checks.")
    s.add_argument(
        "--heartbeat",
        type=float,
        default=10.0,
        help="Seconds between wait-gpu heartbeat lines (0 disables the periodic heartbeat).",
    )
    s.add_argument("--timeout", type=float, default=0.0, help="Maximum seconds to wait; 0 means no timeout.")
    s.set_defaults(func=wait_gpu)

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
        "-m", "--minutes", type=int, default=ACTIVE_STALE_MINUTES,
        help="List mode: freshness window in minutes (default %(default)s, the "
             "AGENTS.md stale threshold). 0 shows entries of any age, including "
             "stale/crashed ones.",
    )
    s.add_argument(
        "--done", action="store_true",
        help="List mode: also include DONE-prefixed (completed) sessions.",
    )
    s.set_defaults(func=active_cmd)

    _call_hook("register_verbs", sub)

    return p


def main() -> int:
    _load_plugins()
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
    except BrokenPipeError:
        # Let common truncating consumers such as `head` close the pipe without
        # turning a successful status/list command into a traceback.
        try:
            sys.stdout.close()
        finally:
            raise SystemExit(0)
