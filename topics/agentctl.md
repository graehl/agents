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

Scope boundary: this topic owns the launcher, state files, and plugin hook
contract. `topics/provenance-tracking.md` owns the run graph implemented by
the `aim` plugin: `runs/aim/` dump schema, declared inputs/outputs,
`<output>.meta.json` back-pointers, propagation facts, and ancestry rules.
Provenance tracking is therefore an `agentctl` concern, but separated because
its invariants are shared by `artifact_meta.py`, downstream Aim import/export
tooling, future compliance-library work, and project migration docs.

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
  an AGENTS.md convention owned by agents and read by the `/others` skill, not
  job state. `agent_session_id()` resolves the launching agent's id from
  `AGENTCTL_SESSION_ID`, else a known harness var (`SESSION_ID_ENVS`, e.g.
  `CLAUDE_CODE_SESSION_ID`), so plain `./agentctl` participates with no per-call
  setup. On `start`/`smoke`/`restart` it keeps that agent's entry live: create
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
2. `.venv/bin/python`, `.pixi/envs/default/bin/python`,
   `pixi-gemma4/.pixi/envs/default/bin/python` under the project root
3. `$CONDA_PREFIX/bin/python` (active conda env)
4. `python3.13`, `python3.12`, `python3.11`, `python3.10` on PATH
5. bare `python3` if it is recent enough

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
