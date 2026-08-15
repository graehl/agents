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
`active`/`others`/`tending`/`alone` verbs, staleness window, launch-depth
guard, or plugin contract. `AGENTS.global.md` keeps only the first-turn obligations
needed to enter a shared workdir safely.

Scope boundary: this topic owns the launcher, state files, and plugin hook
contract. `topics/provenance-tracking.md` owns the run graph implemented by
the `aim` plugin: `runs/aim/` dump schema, declared inputs/outputs,
`<output>.meta.json` back-pointers, propagation facts, and ancestry rules.
Provenance tracking is therefore an `agentctl` concern, but separated because
its invariants are shared by `artifact_meta.py`, downstream Aim import/export
tooling, the cooperative declaration helper, and project migration docs.

## Active-sessions file schema

`.agentctl/active/<session-id>` files are agent-authored coordination
state, not job state. `AGENTS.global.md § Active sessions` carries the
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
claimed extension — so one grep tests overlap with no glob engine.

A `tending:` header line (below line 1, beside `scope:`, either order
accepted; canonical writes put scope first) declares steward presence:
the forward-looking claim that this session will launch more queued
work when it next wakes — a different question from "is anyone here
now", because a steward between hourly wakes has no running process
and possibly no running job. The value names what is tended (normally
`on-deck`), optionally qualified ` until <deadline>` (absolute UTC, or
`forever`). The deadline is informative for readers, not enforced —
entry freshness is the enforcement, so a crashed steward stops
counting within the stale window. Keep the line exactly while future
launches are armed (a wired `--after` chain, a foreground wait that
triggers a follow-up round, a loop or fallback heartbeat); drop it
(`agentctl active "<status>" --no-tending`) when a round ends with
nothing armed, or end the session with `DONE`. The dependency-free
check is `find .agentctl/active -maxdepth 1 -type f -mmin -70 -exec
grep -l '^tending:' {} +`, minus DONE and self entries; `agentctl
tending` is the verb form (§ Contracts).

Anything beyond the header (line 1, `scope:`, `tending:`) is free
content at agent discretion (plan notes, considered approaches, longer
status); brief readers stop after the header. Readers treat files
whose line 1 starts with `DONE` (`DONE*`) as complete.

A line 1 starting `REWRITE` is the advisory history-rewrite lock
(`AGENTS.global.md § Amends`): the holder took the floor via `agentctl alone
<id> -b "REWRITE: <what>"` and is mid rewrite-chain. While a fresh
non-self `REWRITE` entry exists, peers create no commits and make no
other git history/index moves; the lock clears when the holder
rewrites its banner or marks `DONE`, and a crashed holder ages out at
the stale window like any entry.

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
both touch only `active/`. Foreground launches (`start`/`smoke`/`restart`)
run the same sweep silently, so a project that launches jobs stays bounded
with nobody remembering the verb; `--sweep` remains for by-hand runs and
`--dry-run` audits.

`awaiting/` is a fourth, orthogonal dir: the non-blocking "awaiting alone"
queue written by `agentctl alone` while it waits (§ Contracts). It is
intentionally outside the `active/` peer scan, so a queued wait is visible to
browsers (`agentctl active` emits it in the `awaiting` array; the `/others`
skill shows it) without ever counting as a present peer — the wait is noticed
but imposes no re-Read ceremony. `alone` refreshes its own entry each
poll and removes it on exit; a crashed waiter's entry simply ages out of the
window.

## Contracts

- The base writes canonical run state to
  `.agentctl/runs/<job>/<run-id>/state.json` and mirrors a pointer to
  `.agentctl/jobs/<job>/current.json`. These files are the ground truth for
  process status; everything else (sidecars, dumps) is derived.
- `start` and `smoke` load project-root `agentctl.env` when it exists. This is
  a declarative defaults file, not a shell script: it accepts blank lines,
  full-line `#` comments, and unique `KEY=VALUE` entries only. The literal
  `${AGENTCTL_ROOT}` expands to the resolved invocation-project root, making
  tracked paths portable across local and remote clones. Precedence is
  ambient child environment over project defaults, then `--source-env`, then
  explicit `--env KEY=VALUE`. `--project-env PATH` selects another file;
  `--no-project-env` disables loading. The run state and metadata record the
  resolved path, file hash, and key names, never values. `restart` preserves
  the original launch's selected file or disabled state rather than adopting
  a newly created default.
- A default tracked `start`/`smoke` requires a Git checkout at committed
  `HEAD`. It rejects source-relevant tracked/index changes, non-ignored
  untracked `*.py`, and selected script/environment-control bytes that are not
  recoverable from the recorded commit. Tracked changes under `runs/aim/` are
  excluded from the launcher's two cleanliness queries because those files are
  run bookkeeping, not source; they remain visible to ordinary `git status`
  for later result triage. Pixi requires a committed manifest+lock pair. A
  detached or queued child repeats the guard immediately before payload
  launch. `--no-aim` deliberately bypasses this admission rule and is limited
  to trivial, non-evidence-producing work. Standard Git ignores/excludes
  exempt derived Python trees such as `.pixi/`; unchecked-in intermediate data
  remains valid when declared and tracked through the ordinary run-provenance
  surface.
  This guard records an admission-time fact only: the payload still runs from
  the mutable invoking checkout. `source_snapshot.execution_guarantee` is
  `admission-time-only`, and commit-isolated execution requires invoking from a
  separately materialized, protected checkout.
  Every Git cleanliness, listing, and blob-content probe fails closed; a Git
  command error is not treated as an empty clean result. Pixi-specific
  `--manifest-path`/`-m` parsing applies only to a direct `pixi` invocation
  before its subcommand, while an executable located under `.pixi/` also
  identifies its environment root. The same-looking flags on other tools are
  ordinary payload arguments.
- `start --after <job-or-output>` is a mechanical launch gate, not a
  result-interpretation scheduler. It records the new job as `waiting`, then
  starts the payload only after each named `agentctl` job exits cleanly or
  each named artifact's `.running.md` marker resolves cleanly. If the
  follow-on decision depends on reading completed outputs or `.meta.md`
  contents, do not prequeue it with `--after`.
- Queued (`waiting`) is a live, pending state everywhere: a `--after` job
  target blocks while the dependency is `waiting` or `running`; an artifact
  target with no marker follows the job that declares it via `--output`
  (a queued/running producer blocks — a stale completion sidecar from an
  earlier run does not release the dependent — and a producer that ends
  without a clean finish fails the chain). An output path with a
  queued/running producer also *resolves* as a `--after` target, so a
  dependent can queue before its producer starts. `wait --target
  not-running` keeps blocking through `waiting`; `watch` stays attached
  through the queued phase; `stop` cancels a queued run (kills the wrapper,
  marks it `stopped`); `restart` stops a queued wrapper and requeues behind
  the same `--after` chain. A `stopped` or otherwise unclean-terminal
  dependency fails `--after` dependents rather than releasing them, and a
  `waiting` run whose wrapper process is gone is marked `finished
  returncode=unknown` on the next status refresh, so dependents fail fast
  instead of blocking forever.
- A finished run with nonzero or `unknown` return code is an early-failure
  result, not a still-running wait state. `status` and `list` print `FAILED`
  for these runs, `list` includes them even when `--completed-min-elapsed`
  would hide short successful runs, and `status/list --failed` exists as a
  troubleshooting view. `wait --target not-running` prints the final return
  code and log path, and exits nonzero for failed `finished` jobs.
- `wait <job> --tail N` stays quiet apart from requested heartbeat lines until
  the target status is reached, then prints the terminal status and the final
  `N` log lines. Use this one-command form when completion diagnostics are
  useful but live training-log traffic is not. `watch --tail N` has different,
  explicitly live-debug semantics: it prints the last `N` existing lines once
  at attachment, then streams only bytes appended after that snapshot.
- Both verbs accept a native observation bound via `--timeout SECONDS` (0 =
  unbounded). `wait` reports an unmet target and returns 1. `watch` leaves the
  job running, returns 124, and writes
  `[agentctl-watch-timeout-v1] job=<name> status=<state> timeout=<seconds>s` to
  its own stderr. If the job reaches terminal state first, `watch` instead
  returns the job's exit code unchanged; a payload exit of 124 has the normal
  `[watch] done: ... returncode=124` output and no timeout marker. Use these
  native options rather than shell `timeout` or a `tail` pipeline, which
  obscures which process supplied the enclosing shell status.
- Default `list` is a catch-up view, not just a live-process view: it shows
  live jobs (`running` and queued `waiting` behind `--after`) plus enough
  recent finished jobs to reach `--show-last` rows total (default 6), when
  that many finished jobs exist. `--completed N` and `--recent N` override
  the recent-finished tail count directly; `--completed-min-elapsed` is an
  opt-in threshold for hiding short successful runs.
- `wait-work` is the new-work counterpart to the status waits: it blocks
  until a new agentctl run appears (`--runs`: any run id not present at
  launch, restarts included) and/or a new or modified `on-deck/*.md` queue
  entry lands (`--on-deck`; derived `INDEX.md` ignored), defaulting to both
  sources, then prints what appeared and exits 0 (1 on `--timeout`).
  Baselines snapshot at entry, so already-present work never fires it, and
  it works from an empty queue or a project with no runs yet. The watch-only
  use wakes on a fresh launch; the tending use wakes on newly queued work
  (`topics/on-deck.md`).
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
- The long-blocking verbs (`wait`, `watch`, `wait-gpu`, `wait-work`,
  `fleet-watch`) keep
  the agent's entry
  *fresh* without writing content: each poll loop runs a self-throttled mtime
  touch (`touch_active_entry`, at most every 300s — never creating an entry,
  never reviving a DONE one, launch-depth-guarded). Without it, a session
  obeying the RUNS.md 55-min blanket wait cap that launches nothing between
  waits crosses the 70-min window while demonstrably alive and blocked — the
  false absence that would defeat both the peer check and the tending check.
  This touch is what lets one stale window double as liveness enforcement for
  steward presence.
- The `active` verb is the explicit, run-free counterpart to that passive
  refresh: `agentctl active "<banner>" [paths...]` authors the agent's own
  line 1 and (from the path args) `scope:` line 2 directly — no job, no dump,
  no log. Because the agent owns those lines, the verb writes them
  authoritatively (line 1 replaced verbatim, a leading `DONE` honored; scope
  replaced when paths are given, preserved when omitted) while keeping any
  free-content lines below the header. It shares the launch-depth guard
  (`active` from inside a job is refused) and the no-session-id behavior
  (refuses with a nonzero exit rather than writing an unkeyed entry).
- `active` with no banner is the read counterpart: it emits an ACLI payload
  listing active-sessions entries (newest first) with each entry's id, status,
  age, optional `scope`/`tending`, and a `self` boolean for the resolved caller
  id — the `find .agentctl/active -mmin -70` peer-check idiom as a structured
  verb. Default shows only fresh (mtime within `--minutes`, default
  `ACTIVE_STALE_MINUTES` = 70) non-DONE entries; `--minutes 0` drops the
  window to include stale/crashed entries (and reads back `stale/`), `--done`
  adds DONE-prefixed (completed) ones (and reads back `done/`), and `--full`
  adds archive paths and raw mtimes. Listing is read-only: no session id is
  required, no `active/` dir is created, and it exits 0 even when empty (unlike
  the write path, it never errors on missing identity — there is nothing to
  key).
- `active --sweep` is the maintenance counterpart: it archives stale entries
  out of `active/` (DONE → `done/`, others → `stale/`) so the peer-check `find`
  stays bounded; `--minutes` sets the stale threshold (a value ≤ 0 falls back
  to the default window rather than emptying `active/`), `--dry-run` emits the
  would-archive entries without moving, and banner/paths are ignored.
  Reversible by design; the list views above read the archive dirs back. The
  same sweep runs silently on each foreground launch — piggybacked on that
  write path so listing stays read-only.
- The active-session verbs (`active`, `others`, `tending`, `alone`) use the
  shared `acli` output flags: compact JSONL by default for agents/pipes,
  indented JSON under `--pretty`, `--full` for wider schemas, and `--toon`
  rejected because these verbs are not table producers.
- `others [<session-id>]` is the peer-check specialization of `active` (list):
  same window scan (shared `_scan_active` helper, same `--minutes`/`--done`),
  but it drops the caller's own entry and emits `other_count`, `has_peers`, and
  a `peers` array. The motivation is behavioral, not cosmetic: a session that
  formed a "peers present" belief early keeps paying the per-file re-Read
  ceremony (`AGENTS.global.md § Pre-edit re-Read`) after the peers have finished.
  `others` makes the re-confirming check cheap to re-run at the point of
  caution instead of trusting the stale belief. The **exit code is the
  signal** — 0 when you are alone, nonzero when peers are present — so it
  composes as `agentctl others <id> && <solo-only step>` without parsing
  stdout. The explicit `<session-id>` argument is the exclusion key *and* a
  deliberate nudge for a session to know its own id; omit it to fall back to
  `agent_session_id()`, and with no id resolvable nothing is excluded (it
  degrades to `active`-style output). All peers count: there is deliberately
  **no narrowing to `scope:` overlap** — `others`/`alone` are the intentionally
  project-serial verbs, distinct from the per-path re-Read+scope coordination.
  A **provided** id is also a claim: on the alone path it calls
  `ensure_active_registered` to create/refresh `active/<id>` before returning,
  so observe-no-peers and claim-the-floor are near-atomic (the residual
  simultaneous-clearance race is why the claim is atomic-*ish*, not a lock);
  with the id only resolved (no positional) the verb stays read-only and
  creates no dir. A freshly created claim is a placeholder line 1, and the
  payload carries `next_command: agentctl active "<status>"`. It is the
  agentctl-backed counterpart to the dependency-free
  `/others` skill's peer bucket — pass your *real* session id, since a wrong id
  would count your own entry as a peer and re-manufacture the stale belief.
- `tending [<session-id>]` is the steward-presence specialization of `others`:
  the same window scan and self-exclusion, but only entries carrying a
  `tending:` header line count (§ Active-sessions file schema). It answers
  "will an agent launch more queued work when it wakes?" rather than "is
  anyone here now" — what a steward round, an on-deck author wondering
  whether entries will get picked up, or an interactive session eyeing idle
  GPU each actually need. The exit code is the signal, as with `others`: 0 =
  no other tending session, nonzero = tending session(s) listed, so a steward
  round gates itself with `agentctl tending <id> && <round>` and two stewards
  do not race one queue; stdout carries `other_count`, `has_tending_peer`, and
  a `tenders` array for readers that need details. A **provided** id is also a
  claim on the clear path
  (same near-atomic observe-then-claim as `others`, via
  `ensure_active_registered`): it writes `tending: on-deck` (plus
  `until <deadline>` from `--until`) onto your entry, creating a placeholder
  entry when you have none. A bare re-claim rewrites the existing tending
  value verbatim, so an `until` qualifier survives hourly re-claims; passing
  `--until` re-authors it. The `active` verb's `--tending`/`--until`/
  `--no-tending` flags author the same line together with a real banner, and
  a banner-only `active` update preserves an existing tending line, so a
  steward's routine status rewrites never silently shed the claim.
  `scripts/on_deck.py eligible` is the mechanical backstop for informal
  stewarding: it warns on stderr when another fresh session is tending —
  a warning, never a refusal, so taking over from a crashed-but-not-yet-stale
  steward stays possible, and it does not auto-register the caller (authoring
  flows run `eligible` for validation; misregistering them would poison the
  signal).
- `alone [<session-id>]` is the waiting form of `others`: the same
  self-excluded, all-peers (no `scope:` narrowing) computation, polled until
  the peer set is empty, then exit 0; exit nonzero only on `--timeout` (0 =
  forever). For an intentionally project-serial step — `agentctl alone <id> &&
  <whole-project amend/rebase>`. A peer leaves the set on its DONE write or
  when it ages past `--minutes`, so a crashed peer clears on going stale, not
  instantly. `--poll` sets the check cadence; `--heartbeat` sets the cadence
  for repeated `alone_wait` events while waiting (0 disables repeats). Like
  `others`, a **provided** id is registered as a claim — but only on the
  became-alone return, never mid-wait: two mutual `alone` callers that
  registered up front would each see the other and deadlock. `--banner` (with
  optional `scope` positionals) folds `agentctl active` into the wait —
  register your real status + scope and wait in one go, written
  authoritatively via `write_active_entry` on success; bare, the claim is a
  placeholder and the payload carries `next_command`. The on-success timing of
  the *active* claim is deliberate: it lands when you take the floor, not while
  waiting, so you never advertise a blocking claim you have not secured, and
  two mutual `alone` callers cannot deadlock.

  Visibility while waiting is handled separately, so a wait is noticed without
  imposing cost: once peers are present, `alone` writes a **non-blocking**
  `awaiting/<id>` status (`awaiting alone`, plus `then: <banner>` when given,
  with the scope) keyed by the resolved id — env fallback included, unlike
  the positional-only `active/` claim — refreshed every poll and removed on
  exit. It lives in
  `awaiting/`, not `active/`, so the edit-check peer scan (`find
  .agentctl/active`, `_scan_active`) never counts it — `agentctl active` emits
  it in the `awaiting` array and `/others` shows it, but no peer pays re-Read
  ceremony for a session that is only queued. (Announcing the wait as a
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

## Fleet capacity watch

`fleet-watch` is one foreground wait across the local GPU and any number of
named SSH workers. It exists to replace agent-authored polling loops: the
calling agent supplies the free-VRAM requirement of the smallest worthwhile
on-deck run, receives no output while the condition is false, and regains
control when capacity is durable or a watched job ends.

The local target is implicit. Remote targets are additive and probed
concurrently, so one slow SSH round does not multiply by the worker count:

```bash
~/agents/agentctl fleet-watch \
  --target hi=ubuntu@172.18.93.214 \
  --target g7=ubuntu@54.175.245.181 \
  --root hi=/local/draft \
  --root g7=/local/draft \
  --ssh-arg=-i \
  --ssh-arg=/home/graehl/.ssh/id_ed25519_rws \
  --min-free-memory 30000 \
  --timeout 3300
```

`--min-free-memory` is available VRAM, not a nearly-idle used-memory
threshold. A 96-GiB GPU already using 60 GiB is therefore eligible for a
30-GiB run when the remaining headroom is durable. The foreground process is
a blocking primitive, not a dashboard: it emits nothing until a wake
condition is satisfied. Its one flushed wake line then carries the fleet
snapshot, running native jobs, completed job/PID details, and the durability
evidence for qualifying capacity.

One sample never releases the wait. With the default ten-second poll:

- two consecutive qualifying samples establish ordinary capacity;
- six are required if a PID seen on the GPU disappears from the GPU process
  list but remains alive, because the process may be between unload and
  reload;
- three are required when GPU-process enumeration is unavailable.

Any below-threshold sample silently resets the candidate. The final capacity
line names free memory, the requested minimum, sample count, native jobs
still running, and any watched completions accumulated while
`--no-wake-on-job-end` was active.

Native job awareness is opportunistic. On local and SSH targets with
`agentctl`, the watcher automatically discovers jobs live at entry or later,
then reports their terminal status, elapsed time, and return code. A named
`--job NAME=JOB` may also be supplied. Job/PID endings wake the agent by
default so it can do a rough result check before filling the capacity;
`--no-wake-on-job-end` deliberately sleeps through them and waits for GPU
capacity instead, so it is valid only with `--min-free-memory`.

The local target always means the invocation project's agentctl state. A
named `HOST=local` target may select its GPU or jobs explicitly, but its
`--root` must resolve to that same project. Use a separate invocation for a
different local project; accepting the path while reading the invocation
project would silently monitor the wrong jobs.

Foreground invocations should use a sub-hour timeout (`--timeout 3300` is
the normal 55-minute bound) so the agent periodically regains control even
when no resource or job transition occurs. The verb defaults to that bound;
`--timeout 0` is the deliberate unbounded override. A timeout is itself a
wake and prints the final fleet snapshot.

A fresh remote needs only SSH and `nvidia-smi` for capacity monitoring.
Install-free process monitoring uses `--pid NAME=PID`. If `<root>/agentctl`
is executable, or `agentctl` is on the remote `PATH`, native job state is
added; asking for a named job without either is an error rather than a
silent downgrade.

A remote that launches tracked work has a stronger precondition: its project
root is an exact Git checkout with the recorded commit available and a clean
working tree. Copying `agentctl` alone is enough for monitoring, but an rsynced
source snapshot without `.git` is intentionally rejected as an experiment
source. Transfer named data/artifacts separately and declare them as inputs;
use a checkout (or a future verified snapshot materialization), not a mutable
source rsync, for code.

This verb is a wake point, not a scheduler. Worker provisioning, staging,
successor choice, launch, result interpretation, and artifact copy-back
remain explicit agent actions after it returns. A copied remote `agentctl`
is useful for native job state and launches but is never a prerequisite for
capacity monitoring.

## Job-completion wake

`agentctl_plugins/wake.py` closes the
Codex dead-stop gap (`AGENTS.codex.md § Turn-End Is A Dead Stop`): a
launch made from a YA-supervised session inherits
`YEP_SESSION_WAKE_URL`/`YEP_SESSION_WAKE_TOKEN`; the plugin arms on
launch-depth-0 launches carrying that env (`--no-wake` opts out), and
`on_finish` — running in the detached `_run-child` wrapper, which
survives agent teardown with the launch-time env — POSTs a one-line
completion summary (`[agentctl-wake] job <name> finished
returncode=<rc> …`) back to the launching session, waking the agent to
consume the result. It appends the last non-empty log line for a failed job,
never follows HTTP redirects with the bearer credential, and persists no URL
or token in run state. Best-effort: stdlib HTTP with a three-second timeout,
one retry, then one log line and stop; YA heartbeat turns are the backstop.
Full contract — endpoint, token, delivery-time gating, resume-on-wake rules,
and the narrow provider-CLI injection fallback — lives in the yepanywhere
repo's `topics/session-wake.md`.

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
`project_env`, `git_branch`, `git_commit`, `source_snapshot`,
`machine_snapshot`, `launch_gpu_stats`.

`project_env` is null when project defaults were absent or disabled. Otherwise
it contains `path`, `sha256`, and `keys`; values are deliberately excluded.

`user_argv` preserves the payload argv before translated `--input` and
`--output-arg` declarations are appended. Restarts rebuild translated flags
from declarations against that original argv, preventing duplicate flags.
For run state written before `user_argv` existed, restart removes the exact
declaration-owned suffix from final `argv` before rebuilding it. It refuses a
legacy record whose suffix disagrees with its input/output declarations.

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
   produced by downstream tooling like `import_aim_text.py`. The tracked form
   also enforces commit-aligned source admission and records the selected source
   snapshot plus best-effort host/OS/GPU/cloud identity.
2. **Trivial / untracked runs.** `--no-aim` opts out of dump writing.
   Useful when the value of running through `agentctl` is just the launcher
   + state-tracking + permission story (an agent with `agentctl` in `PATH`
   does not need raw shell exec rights for routine launches), not the
   research-record story. It bypasses commit-aligned source admission and must not
   produce experimental evidence.

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
- `agentctl list --failed` is the fastest catch-up view for failed runs that
  have aged out of the default recent tail or are hidden by explicit filters.
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

<!-- observed -->
The `fleet` plugin uses `register_verbs` to add a multi-host foreground
monitor without putting SSH or fleet semantics in the base launcher. The
run-record `aim` plugin exercises other lifecycle hooks; together the two
plugins establish both top-level verb extension and launch-lifecycle
extension without direct plugin calls from the base.

<!-- assumed -->
The 24-hex md5-of-run_id synthesis for `aim_run_hash` is collision-safe
within agentctl-generated dumps because run_ids are unique. It is **not**
guaranteed not to collide with externally-generated real Aim hashes;
treat the `agentctl_run_id` field as the truly authoritative identifier
when both are present.

Candidate extensions are kept in [agentctl sketches](agentctl.sketches.md).
