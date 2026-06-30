# agentctl: process manager + plugin contract

> Dependency-free local job manager: process-group lifecycle,
> GPU/CPU resource gating, and on-disk run state under `.agentctl/`,
> with project-specific concerns delegated to plugins under
> `agentctl_plugins/`.

Topic: `agentctl`

`agentctl` is a small, dependency-free local job manager. The base layer owns
process-group lifecycle, GPU/CPU resource gating, and on-disk run state under
`.agentctl/`. Project-specific concerns (run-record export, experiment
tracking, domain verbs) live in optional plugins under `agentctl_plugins/`.

Read this topic before changing active-session semantics, diagnosing
`.agentctl` run state, modifying `agentctl`, or relying on details of the
`agentctl active` verb, staleness window, launch-depth guard, or plugin
contract. `AGENTS.md` keeps only the first-turn obligations needed to enter
a shared workdir safely.

Scope boundary: this topic owns the launcher, state files, and plugin hook
contract. `topics/provenance-tracking.md` owns the run graph implemented by
the `aim` plugin: `runs/aim/` dump schema, declared inputs/outputs,
`<output>.meta.json` back-pointers, propagation facts, and ancestry rules.
Provenance tracking is therefore an `agentctl` concern, but separated because
its invariants are shared by `artifact_meta.py`, downstream Aim import/export
tooling, the cooperative declaration helper, and project migration docs.

## Active-sessions file schema

`.agentctl/active/<session-id>` files are agent-authored coordination
state, not job state. `AGENTS.md § Active sessions` carries the
first-turn obligations (create, update, peer-check, `DONE`); this
section is the normative file format. The file is an ordinary text
artifact: `agentctl active` is a convenience for writing it, never a
requirement, and agents in projects without `agentctl` hand-write it —
the plain `find .agentctl/active -maxdepth 1 -type f -mmin -70` peer
check stays the dependency-free definition of the convention.

Line 1 is the present-tense gist — self-contained, readable on its
own. Line 2 may declare scope as `scope: <paths>`: a space- or
comma-separated list of project-root-relative paths for tool-detected
overlap with peers. A path is literal, or carries a wildcard only at a
separator boundary — at the start of a segment (right after `/`, or the
string start) or right after a `.`:
- `dir/**` — the whole subtree, any depth. `**` is the only form that
  spans `/`; a lone `*` stops at the next `/`, so `dir/*` is one level
  and `*.py` is one segment.
- `*.py`, `config.*` — extension/suffix narrowing.
Interior wildcards (`pkg*/cli`, `src/foo_*.ts`) are barred: they force
a glob-aware consumer. Every blessed form instead reduces to an
anchored match — a concrete path overlaps a claim when the claim's
literal anchor prefixes it (segment/subtree forms) or it ends in the
claimed extension — so one grep tests overlap with no glob engine. Anything beyond line 2 is free content at agent
discretion (plan notes, considered approaches, longer status); brief
readers stop after line 2. Readers treat files whose line 1 starts
with `DONE` (`DONE*`) as complete.

`agentctl active --sweep` archives entries older than the stale window
(`ACTIVE_STALE_MINUTES`, default 70) out of `active/`, so the hot peer-check
`find .agentctl/active -maxdepth 1 -type f -mmin -70` only ever stats
within-window entries instead of an unbounded pile of corpses. A
`DONE`-prefixed (completed) entry moves to `.agentctl/done/`; any other
(crashed/quiet) entry moves to `.agentctl/stale/`, which is then exactly the
neglected-session list to audit. Fresh entries — live peers and just-finished
sessions still inside the window — stay put. The move is reversible (entries
are relocated, not deleted), and the list views read them back: `--minutes 0`
also scans `stale/`, and `--done` also scans `done/`, so the audit survives a
sweep. `--dry-run` reports without moving. `active/`/`stale/`/`done/` thus
partition entries by liveness, and the default-window list and the raw `find`
both touch only `active/`.

`awaiting/` is a fourth, orthogonal dir: the non-blocking "awaiting alone"
queue written by `agentctl alone` while it waits (§ Contracts). It is
intentionally outside the `active/` peer scan, so a queued wait is visible to
browsers (`agentctl active` lists it tagged `(awaiting, non-blocking)`; the
`/others` skill shows it) without ever counting as a present peer — the wait is
noticed but imposes no re-Read ceremony. `alone` refreshes its own entry each
poll and removes it on exit; a crashed waiter's entry simply ages out of the
window.

## Contracts

- The base writes canonical run state to
  `.agentctl/runs/<job>/<run-id>/state.json` and mirrors a pointer to
  `.agentctl/jobs/<job>/current.json`. These files are the ground truth for
  process status; everything else (sidecars, dumps) is derived.
- `start --after <job-or-output>` is a mechanical launch gate, not a
  result-interpretation scheduler. It records the new job as `waiting`, then
  starts the payload only after each named `agentctl` job exits cleanly or
  each named artifact's `.running.md` marker resolves cleanly. If the
  follow-on decision depends on reading completed outputs or `.meta.md`
  contents, do not prequeue it with `--after`.
- A finished run with nonzero or `unknown` return code is an early-failure
  result, not a still-running wait state. `status` and `list` print `FAILED`
  for these runs, `list` includes them even when `--completed-min-elapsed`
  would hide short successful runs, and `status/list --failed` exists as a
  troubleshooting view. `wait --target not-running` prints the final return
  code and log path, and exits nonzero for failed `finished` jobs.
- Active-sessions participation: the `.agentctl/active/<session-id>` files are
  an agent-owned convention (§ Active-sessions file schema above) read by the
  `/others` skill and the `others` verb (below), not job state. `agent_session_id()` resolves the launching agent's id from
  `AGENTCTL_SESSION_ID`, else a known harness var (`SESSION_ID_ENVS`, e.g.
  `CLAUDE_CODE_SESSION_ID`), so plain `./agentctl` participates with no per-call
  setup. When no env var carries an id — a resumed session that exports none,
  e.g. a terminal `codex resume <id>` — it falls back to
  `session_id_from_proc_tree()`, which walks the parent process chain (Linux
  `/proc`) and reads the id off a `resume <id>` / `--resume <id>` ancestor argv
  (PPid from `/proc/<pid>/status`, not the paren-`comm` `stat` field). The
  recovery is a fallback only: an env id always wins, the launch-depth guard is
  checked first (below), and `AGENTCTL_NO_PROC_SESSION_ID` disables it for
  environments under an unrelated `resume <uuid>` ancestor and for hermetic
  tests. On `start`/`smoke`/`restart` it keeps that agent's entry live: create
  with a placeholder line 1 if absent, else append a free-text launch note
  (which refreshes mtime), never rewriting the agent-authored line 1 or
  `scope:` line 2, and never touching a `DONE`-prefixed entry. Each launch
  increments `AGENTCTL_LAUNCH_DEPTH` in the child env; `agent_session_id()`
  returns "" at depth > 0, so a launched job (or any agentctl it shells) cannot
  refresh or masquerade as the agent — a count-down-once guard that needs no
  env stripping and leaves the harness's own session var intact. With no
  session id resolvable, the launcher does not touch `active/` at all.
- The `active` verb is the explicit, run-free counterpart to that passive
  refresh: `agentctl active "<banner>" [paths...]` authors the agent's own
  line 1 and (from the path args) `scope:` line 2 directly — no job, no dump,
  no log. Because the agent owns those lines, the verb writes them
  authoritatively (line 1 replaced verbatim, a leading `DONE` honored; scope
  replaced when paths are given, preserved when omitted) while keeping any
  free-content lines below the header. It shares the launch-depth guard
  (`active` from inside a job is refused) and the no-session-id behavior
  (refuses with a nonzero exit rather than writing an unkeyed entry).
- `active` with no banner is the read counterpart: it lists active-sessions
  entries (newest first) with each one's line-1 status and `scope:` line —
  the `find .agentctl/active -mmin -70` peer-check idiom as a verb. Default
  shows only fresh (mtime within `--minutes`, default `ACTIVE_STALE_MINUTES`
  = 70) non-DONE entries; `--minutes 0` drops the window to include
  stale/crashed entries (and reads back `stale/`), `--done` adds DONE-prefixed
  (completed) ones (and reads back `done/`), and the caller's own entry (by
  resolved session id) is tagged `(self)`. Listing is read-only: no session id
  is required, no `active/` dir is created, and it exits 0 even when empty
  (unlike the write path, it never errors on missing identity — there is
  nothing to key).
- `active --sweep` is the maintenance counterpart: it archives stale entries
  out of `active/` (DONE → `done/`, others → `stale/`) so the peer-check `find`
  stays bounded; `--minutes` sets the stale threshold (a value ≤ 0 falls back
  to the default window rather than emptying `active/`), `--dry-run` reports
  without moving, and banner/paths are ignored. Reversible by design; the list
  views above read the archive dirs back.
- `others [<session-id>]` is the peer-check specialization of `active` (list):
  same window scan (shared `_scan_active` helper, same `--minutes`/`--done`),
  but it drops the caller's own entry and leads with a count — `N other active
  session(s) (last 70m):` or `no other active sessions (...)`. The motivation
  is behavioral, not cosmetic: a session that formed a "peers present" belief
  early keeps paying the per-file re-Read ceremony (`AGENTS.md § Pre-edit
  re-Read`) after the peers have finished. `others` makes the re-confirming
  check cheap to re-run at the point of caution instead of trusting the stale
  belief. The **exit code is the signal** — 0 when you are alone, nonzero when
  peers are present — so it composes as `agentctl others <id> && <solo-only
  step>` without parsing stdout. The explicit `<session-id>` argument is the
  exclusion key *and* a deliberate nudge for a session to know its own id; omit
  it to fall back to `agent_session_id()`, and with no id resolvable nothing is
  excluded (it degrades to `active`-style output). All peers count: there is
  deliberately **no narrowing to `scope:` overlap** — `others`/`alone` are the
  intentionally project-serial verbs, distinct from the per-path re-Read+scope
  coordination. A **provided** id is also a claim: on the alone path it calls
  `ensure_active_registered` to create/refresh `active/<id>` before returning,
  so observe-no-peers and claim-the-floor are near-atomic (the residual
  simultaneous-clearance race is why the claim is atomic-*ish*, not a lock);
  with the id only resolved (no positional) the verb stays read-only and
  creates no dir. A freshly created claim is a placeholder line 1, and the
  verdict prints how to set a real status (`agentctl active "<status>"`). It is
  the agentctl-backed counterpart to the dependency-free
  `/others` skill's peer bucket — pass your *real* session id, since a wrong id
  would count your own entry as a peer and re-manufacture the stale belief.
- `alone [<session-id>]` is the waiting form of `others`: the same
  self-excluded, all-peers (no `scope:` narrowing) computation, polled until
  the peer set is empty, then exit 0; exit nonzero only on `--timeout` (0 =
  forever). For an intentionally project-serial step — `agentctl alone <id> &&
  <whole-project amend/rebase>`. A peer leaves the set on its DONE write or
  when it ages past `--minutes`, so a crashed peer clears on going stale, not
  instantly. `--poll` sets the check cadence (one `.` tick each), `--heartbeat`
  the cadence of fresh naming lines while waiting (0 = ticks only); a
  foreground caller consumes the stream so ticks are unguarded. Like `others`,
  a **provided** id is registered as a claim — but only on the became-alone
  return, never mid-wait: two mutual `alone` callers that registered up front
  would each see the other and deadlock. `--banner` (with optional `scope`
  positionals) folds `agentctl active` into the wait — register your real
  status + scope and wait in one go, written authoritatively via
  `write_active_entry` on success; bare, the claim is a placeholder and the
  line prints how to set a real status. The on-success timing of the *active*
  claim is deliberate: it lands when you take the floor, not while waiting, so
  you never advertise a blocking claim you have not secured, and two mutual
  `alone` callers cannot deadlock.

  Visibility while waiting is handled separately, so a wait is noticed without
  imposing cost: once peers are present, `alone` writes a **non-blocking**
  `awaiting/<id>` status (`awaiting alone`, plus `then: <banner>` when given,
  with the scope), refreshes it every poll, and removes it on exit. It lives in
  `awaiting/`, not `active/`, so the edit-check peer scan (`find
  .agentctl/active`, `_scan_active`) never counts it — `agentctl active` lists
  it tagged `(awaiting, non-blocking)` and `/others` shows it, but no peer pays
  re-Read ceremony for a session that is only queued. (Announcing the wait as a
  blocking `active/` entry is the rejected alternative — it reintroduces the
  mutual-`alone` deadlock.)
- Every plugin hook is optional. Missing hooks are silently skipped; loader
  errors print one warning and continue without the failing plugin so a
  broken plugin does not break the launcher.
- Plugins reach base helpers via `import agentctl`. The loader registers the
  running module under that name even when invoked as `__main__`, so
  `agentctl.ROOT`, `agentctl.slug`, `agentctl.command_string`,
  `agentctl.utc_now`, etc. resolve to the same module instance the base is
  using.
- The base never imports a plugin directly. Plugin discovery is by filesystem
  scan of `agentctl_plugins/*.py` (skipping `_`-prefixed names and
  `__init__.py`). Order is alphabetical, deterministic.
- Plugins **may not** assume the base imports any third-party package on
  their behalf. Imports that may fail (e.g. the Aim SDK) must be guarded
  inside the plugin and treated as best-effort.

## Hook surface

All hooks are optional; the base calls them via `getattr` and a small
`_call_hook` / `_first_hook` dispatcher.

| Hook | Phase | Effect |
|------|-------|--------|
| `register_args(parser)` | parser build | Add args to `start`/`smoke`. Called once per parser. |
| `register_verbs(subparsers)` | parser build | Add top-level subcommands. |
| `on_start(args, state, env)` | pre-launch | Mutate `state` and `env` before subprocess fork. |
| `default_output_path(args, run_dir) -> Path \| None` | pre-launch | First non-None wins. Used when user did not pass `--output`. |
| `on_meta_built(state, meta_text, *, output_path, log_path, build_meta) -> str \| None` | post-meta | Write sidecars; return updated meta text or `None`. `build_meta()` rebuilds with current state. |
| `on_finish(state)` | post-child-exit | Update plugin-owned completion artifacts after outputs are stat'd. |
| `on_status_print(state, lines)` | status print | Mutate the bits list appended to the one-line status. |
| `on_note(state, note, stamp, *, meta_path, meta_text)` | `note` verb | React to post-run analysis note. |
| `on_restart(state, args)` | restart | Refill plugin-specific args on the rebuilt namespace. |

## State schema

The base writes a flat dict to `state.json`. Canonical keys (read freely):

`job`, `launch_name`, `run_id`, `serial`, `mode`, `status`, `started_at`,
`finished_at`, `returncode`, `pid`, `pgid`, `pid_namespace`,
`pid_start_ticks`, `pid_cmdline`, `argv`, `cwd`, `log_path`, `headline_path`,
`output_path`, `meta_path`, `state_path`, `exit_status_path`, `run_dir`,
`runtime_estimate`, `runtime_estimate_seconds`, `context_note`,
`pre_run_note`, `post_run_note`, `post_run_noted_at`, `analysis_notes`,
`depends_on`, `wait_on`, `wait_after`, `queued_at`, `source_env`,
`git_branch`, `git_commit`, `launch_gpu_stats`.

Plugins should write their own keys directly on `state` (the dict is the
in-memory record passed to every hook). Existing convention from the `aim`
plugin: `aim`, `aim_run_hash`, `experiment`, `tags`, `aim_dump_record`. New
plugins should namespace less obviously named additions to avoid collisions.

## Run-tracking framing

Two intended use cases for `agentctl`, both first-class:

1. **Tracked runs.** Default. Every launch writes an Aim-format run record
   under `runs/aim/<experiment>/` (see `aim` plugin and the
   `aim-text-dump-v1` schema). These dumps are the authoritative branch
   record for the run; live `.aim/` is a rebuildable materialization,
   produced by downstream tooling like `import_aim_text.py`.
2. **Trivial / untracked runs.** `--no-aim` opts out of dump writing.
   Useful when the value of running through `agentctl` is just the launcher
   + state-tracking + permission story (an agent with `agentctl` in `PATH`
   does not need raw shell exec rights for routine launches), not the
   research-record story.

The Aim SDK is **not** required. The plugin writes JSON dumps directly. If
the SDK is installed, users can run `aim up` to browse the materialized view
after import; if not, a one-line install hint prints once per process and
the dumps are still written.

## Failure visibility ADR

Decision: treat early failures as first-class status output, not as a special
case left to log inspection. The launcher already records child return codes in
`exit-status.json` and refreshes state from that sidecar, so the status layer
can reliably distinguish `finished returncode=0` from `finished returncode=1`
without reading logs. Agents are prone to interpret "no summary rows yet" or
an interrupted polling command as "still running"; surfacing `FAILED` in the
same one-line status path makes the cheap check harder to skip.

Operational consequences:

- `agentctl status <job>` is the required truth check after a manual sleep,
  timeout, interrupted tool call, or apparent lack of output.
- In a sandboxed PID namespace, an invisible recorded PID is inconclusive, but
  a visible PID that fails the recorded launch identity (`pid_start_ticks` or
  `pid_cmdline`) is conclusive PID reuse; status refresh may mark that run
  `finished returncode=unknown` rather than keeping it `running`.
- `agentctl list --failed` is the fastest catch-up view for short failed runs
  that would otherwise be absent from "recent completed" lists.
- Default `list` includes failed finished runs regardless of
  `--completed-min-elapsed`, because a job that failed after 18 seconds is
  often more important than a job that succeeded after 18 seconds.
- `agentctl wait <job> --target not-running` is preferred over ad hoc
  `sleep; cat summary` loops when a run's terminal state matters, because it
  returns nonzero for failed `finished` jobs and prints the log path.

## Wrapper Python resolution

`./agentctl` treats its install directory as `CODE_ROOT` and the invocation
directory (or `$AGENTCTL_ROOT`) as the project `ROOT`. State, logs,
project-relative inputs/outputs, git metadata, and `runs/aim/` records are
rooted in the project; plugin code and shared helper imports are rooted in
`CODE_ROOT`. This lets a single global `~/agents/agentctl` operate inside many
projects without writing their state under `~/agents`.

The wrapper finds a Python ≥ 3.10 by checking, in order:

1. `$AGENTCTL_PYTHON` (explicit override)
2. `.agentctl/python` project pointer file: first non-comment line names the
   interpreter (absolute, `~`-prefixed, or relative to the project root). Use
   this to pin a project whose desired env is shadowed by an earlier match in
   the list below — e.g. a research env carrying extra packages (an experiment
   tracker, say) under a non-default path, losing to a bare project-root
   `.pixi/envs/default`.
3. `.venv/bin/python`, `.pixi/envs/default/bin/python` under the project root
4. `$CONDA_PREFIX/bin/python` (active conda env)
5. `python3.13`, `python3.12`, `python3.11`, `python3.10` on PATH
6. bare `python3` if it is recent enough

Bare `python3` is intentionally last because legacy distros still ship
Python 3.6 there. The wrapper hard-fails with an actionable message if no
suitable interpreter is found.

## Invariants

- The base does not call any plugin's functions directly by name. All plugin
  interaction goes through the hook dispatcher.
- A plugin with a syntax error or failing top-level `import` is skipped
  with one stderr warning; the rest of the launcher continues to work.
- `state["aim_run_hash"]`, when present, is the discovery key used by
  `artifact_meta.find_aim_run_record/text` to locate dumps. The `aim` plugin
  synthesizes this from `state["run_id"]` (24-hex md5); any other plugin that
  populates this key must guarantee uniqueness per dump tree.
- `runs/aim/` is the current canonical dump root. No fallback dump root
  should be used for new writes.
- `.agentctl/` is runtime state and should normally be gitignored. `runs/`
  policy is project-specific: commit `runs/aim/` when a project declares text
  run dumps to be reviewable branch authority; otherwise ignore it as runtime
  provenance.
- Every `agentctl` invocation calls `ensure_state_ignored()` (in `main()`),
  which adds an *uncommitted* `/<path>/.agentctl/` rule to the repo's
  `$GIT_DIR/info/exclude` when git does not already ignore the dir — so the
  state dir stays untracked without editing the project's committed
  `.gitignore`. No-op when `ROOT` is not under git control, when the dir is
  already ignored (probed via a path under it so directory-only patterns like
  `.agentctl/` match before the dir exists), or on any git/fs error
  (best-effort, never the caller's task).

## Catch-up notes

<!-- assumed -->
The hook surface (9 hooks) was sized to the actual extraction of the `aim`
plugin from a previously-monolithic `agentctl.py`. It covers every Aim
touchpoint without requiring base-level knowledge of Aim or its dump format.
A second plugin would prove the surface is genuinely general; until then,
treat the hook list as falsifiable by the next concrete plugin rather than
fixed.

<!-- assumed -->
The 24-hex md5-of-run_id synthesis for `aim_run_hash` is collision-safe
within agentctl-generated dumps because run_ids are unique. It is **not**
guaranteed not to collide with externally-generated real Aim hashes;
treat the `agentctl_run_id` field as the truly authoritative identifier
when both are present.
