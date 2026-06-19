# RUNS supplement

This file is loaded when run-operation indicators are present. It covers
launch, monitoring, GPU scheduling, wait/watchdog behavior, and run metadata.

### GPU access for Python ML commands

When working in an ML repo that uses local accelerators, default to running Python
commands with GPU-visible permissions whenever the script might import `torch`,
`transformers`, `unsloth`, `vllm`, TensorRT helpers, or related ML code. This includes
commands that look lightweight such as `--help`, because some scripts import the full
runtime before parsing arguments.

Do not infer "this machine has no GPU" from a sandboxed failure like `torch.cuda` or
`unsloth` accelerator detection returning false. Treat that first as a likely sandbox
GPU-visibility issue. If there is any realistic chance the command will touch the ML
stack, rerun it with GPU-capable permissions instead of continuing with a sandboxed
Python path.

Before launching a GPU job, first confirm whether the GPU appears idle. If GPU use is
already present unexpectedly, warn but proceed when estimated free VRAM still looks
sufficient for the planned job, since this resource is assumed to be single-user. Only
block or change the plan when current use makes the launch materially risky.

**PyTorch CUDA allocator — prevent memory over-reservation:**
Always set `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True,garbage_collection_threshold:0.5`
before any PyTorch job — without it the caching allocator holds large VRAM slabs between
jobs, preventing concurrency. `env.sh` sets this; always `source env.sh` or export
explicitly before `nohup` jobs. (The typo `PYTORCH_ALLOC_CONF`, missing `CUDA_`, is silently ignored.)

### GPU utilization and parallelism policy

The GPU is non-shared and must be kept busy with planned work at all times —
without being asked and without churning the repo.

**Keep-busy rule**: Whenever a job finishes (or while one runs and a slot is
free), immediately queue or launch the next planned job. Never leave the GPU
idle between planned jobs. Use `wait <PID>` wrappers with a brief sleep buffer
(~90 s) between sequential jobs to let GPU memory fully release.

**Parallelism rule** — two independent jobs must run simultaneously whenever:
- the running job uses **< 50% of total VRAM**, AND
- a second planned job also fits in remaining VRAM with ≥ 10% headroom.

A single job is acceptable only when it uses **≥ 80% of VRAM** (or ≥ 80%
sustained utilization per `nvidia-smi utilization.gpu`). The 50–80% band is
the trigger zone: find and launch a second job from the plan without asking.

**Operationally**:
1. After any job launch or completion, run `nvidia-smi` and check VRAM.
2. If VRAM < 50%: immediately identify the next independent planned job that
   fits in free VRAM (≥ 10% headroom) and launch it without asking.
3. Two jobs are "independent" if they write to different output directories and
   neither reads the other's in-progress output.
4. Prefer the next *planned* job from the task/research queue; only propose new
   experiments if the queue is exhausted.
5. When chaining via `wait <PID>`, check whether any queued job can be promoted
   to run now in parallel with the current job.
6. When a run finishes, immediately show the user a brief highlight: headline
   result, key metric(s), and 1–2 sample output comparisons. Do not wait to be
   asked.
7. **Verify GPU is in use after every job launch.** After starting a background
   job (direct or via a `nohup` wrapper), wait ~30 s and run `nvidia-smi` to
   confirm VRAM rose as expected. If the GPU stays at 0 MiB, the job silently
   failed — investigate the log immediately and relaunch. Never assume a
   background job succeeded without this check.
8. **Use VRAM-polling waits between chained jobs**, not fixed sleeps.
   Before launching the next job in a chain, poll until VRAM drops below a
   safe threshold (e.g. `while [ $(nvidia-smi --query-gpu=memory.used
   --format=csv,noheader | tr -d ' MiB') -gt 3000 ]; do sleep 15; done`).
   Fixed sleeps are unreliable because child/worker processes can hold GPU
   memory well past the parent's exit.

### On-deck GPU fillers

Projects may opt into `on-deck/` as a guarded queue of single-step GPU fillers;
see `topics/on-deck.md`. `$on-deck` creates the queue. A steward agent may fill
idle GPU without waiting for confirmation when an entry's guard passes, its
skip-if does not fire, and its cost is within steward autonomy. If `on-deck/`
is absent, `/steward` is a no-op. Use `/steward` for one fill-until-full pass
and `/rep steward` when repeated servicing is desired.

On-deck does not replace `agentctl` run state. The queue answers "what should
run next"; `.agentctl/` answers "what is running now." If a higher-priority
eligible entry appears while a steward filler is running, pause/kill only as a
judgment call when the saved time is worth the lost work and the stop is safe.

### Implicitly authorized routine operations and return-from-sidebar liveness

After a sidebar, immediately resume with the previously agreed next step (or its
successor if the sidebar changed the plan). Treat any plan previously proposed and
not contradicted as approved; ask only when two alternatives have meaningfully
different outcomes and comparable expected value. Offer to run independent forks
in parallel when feasible.

Full GPU access is always permitted.

Editing project files always permitted.

Standard git operations (excluding private/gitignored files such as
`tasks/`) always permitted. Standard command-execution plumbing —
shell, tee, timeout, kill (processes you launched) — always permitted.


### Research artifact metadata

For important saved research outputs, use the output artifact as the anchor:

- `<out>` — primary artifact
- `<out>.meta.md` — compact provenance and summary (written by agent-managed
  launch plumbing such as `agentctl`, not by payload scripts)
- `<out>.log` — full stderr/runtime log
- `<out>.running.md` — launch record written by the agent at job start; deleted on clean completion

#### In-flight job tracking (`.running.md`)

**The agent writes `.running.md` immediately when launching a background job.** Scripts
are not responsible for creating or deleting it. This file survives crashes and lets a
resumed agent discover in-flight or interrupted work without reading shell history.

Minimal structure:

```markdown
# In-Flight Job: <out-name>

- status: running
- pid: <PID>
- started: <ISO timestamp>
- log: <path to stdout/stderr log>
- trainlog: <path to structured trainlog, if separate>
- out: <output dir or file path>

## Command
\`\`\`bash
cd <cwd>
<full command>
\`\`\`
```

**On session resume after a crash:**
1. `ls untracked/*.running.md` (or wherever jobs are launched) to find candidates.
2. For each: `kill -0 <pid>` — if alive, job is still running; tail the log for progress.
   If dead and no `.meta.md` exists, the job was killed mid-run — tail the log for
   partial results and record them informally in the research log.
3. If `.meta.md` exists alongside `.running.md`, the job completed but cleanup was
   skipped — delete the `.running.md`.

**Cleanup:** ordinary operation should not require a manual cleanup step: the
launching agent, or `agentctl` when it owns the launch, removes `.running.md`
after a clean completion. If a reboot, crash, or interrupted cleanup leaves
stale markers and you need a "where were we?" pass, run
`agentctl cleanup-running` with no arguments: it scans the workspace, reports
`running` / `completed` / `interrupted`, and only removes markers that are
clearly completed via adjacent `.meta.md` or `.meta.json`. To delete a known
marker explicitly, run `agentctl cleanup-running <out>` or pass the marker
path directly, `agentctl cleanup-running <out>.running.md`. Payload scripts
should not be expected to create `.meta.md` or clean up `.running.md`; they
produce outputs and may optionally write cooperative run declarations such as
`$AGENTCTL_RUN_DIR/propagate.json`.

`agentctl start --after <job-or-output>` may depend on either an `agentctl`
job or an output path following this `.running.md` convention. The queued job
is visible as `waiting`, but its payload is not launched and output metadata is
not written until all dependencies complete cleanly. Use this only when the
follow-on is mechanically determined; if the next step depends on interpreting
the completed `.meta.md` or output contents, wait and inspect before launching.

The naming relationship is strict: `.meta.md` and `.log` are formed directly from the
exact output filename. When a run has one primary output, redirect stderr to `<out>.log`.

For new tracked runs, prefer the `agentctl` run record and the output
`<out>.meta.json` back-pointer. For legacy or manually managed artifacts,
`*.meta.md` remains a useful compact human summary; if writing one manually,
use the same structure so later agents can parse it.

Use short relative paths inside `*.meta.md`, interpreted relative to that metadata file.

Canonical `*.meta.md` structure:

```markdown
# Run Metadata: <artifact name or short title>

## Output
- out: [<out>](relative/path)
- log: [<out>.log](relative/path)

## Command
```bash
cd <working-directory-used-for-the-run>
<actual command line used to generate the artifact>
```

## Setup
- split: `<split>`
- N: `<N, if known>`
- metric: `<metric, if any>`
- model: `<model, if useful>`
- method: `<method summary, if useful>`

## Result
- <key>: `<value>`

## Machine
- <key>: `<value>`
- <key>: `<value>`

## Related
- <label>: [<path>](relative/path)

## Inputs
### `<code>`
- path: [<path>](relative/path)
- meta: [<path>.meta.md](relative/path)
- (`<code>.output`) out: [<path>](relative/path)
- (`<code>.result`) score-summary: `<headline result>`
- (`<code>.machine`) <key>: `<value>`

## Notes
- <free-form note>
```

Section semantics:
- `## Command` is required when a command generated the artifact. Include the explicit
  `cd ...` and the actual command that was run, not a reconstruction.
- `## Result` is for headline outcomes a human will compare first.
- `## Machine` is for compact machine-generated run stats or parsed summaries that are
  still small enough to keep in the metadata file.
- `## Related`, `## Inputs`, and `## Notes` are optional.
- Under `## Inputs`, use one `### <code>` block per input. Short codenames should be
  explicit when helpful (for example via `--input train=path/to/out`), otherwise derived
  from the filename.
- Inherited input metadata is **one level deep only**. Inline only selected top-level facts
  from the input's own `*.meta.md` (typically `Output`, `Result`, and `Machine`) and prefix
  them with the input codename such as `(<code>.result)`. Do **not** recursively inline the
  input's own `## Inputs`.
- The inherited restatement must not introduce additional `##` headings; reserve `##` for the
  current artifact's top-level sections so simple `^## ` header scans remain reliable.

When updating a research log, link directly to the saved output or its `*.meta.md`.
If a linked artifact is missing later, search first for the corresponding `*.meta.md`,
then by naming convention or distinctive command/log lines.

### Run records and provenance

When a project tracks runs through `agentctl`, the canonical run record is the
JSON dump under `runs/aim/<experiment>/runs/<run-id>.json`, using the
`artifact_meta.find_aim_run_record/text` lookup path. Refer to that record
rather than reconstructing run history from logs or `.meta.md` content alone: the
dump carries the structured argv/cwd, declared inputs and outputs, the script
fingerprint, git branch+commit, and any producer-tagged propagation facts.

Output files produced under tracked runs get a `<output>.meta.json` sidecar next
to them, containing `agentctl_run_id` and `run_dump` pointing back at the
producing record. When you encounter an unfamiliar file, check for this sidecar
before assuming it's untracked — following `run_dump` gives you the full
provenance one read away.

Bare `agentctl` invocations throughout this doc assume PATH lookup; when
`command -v agentctl` fails, invoke it via `~/agents/agentctl` (the canonical
absolute path — `./agentctl` will not work from arbitrary project CWDs).

When `agentctl` is on `PATH`, prefer `agentctl start ... -- <command>` for any
launch you might later need to reproduce, audit, or trace. Two tiers:

- **Tracked launch** (default): writes the full dump + meta sidecars; the run is
  reachable via the runs DB and via filesystem-discoverable back-pointers.
  Declared inputs (`--input KEY=PATH`) get sidecar lookup so the run record
  shows what produced each input one-deep.
- **Trivial launch** (`agentctl start --no-aim ...`): records nothing under
  `runs/aim/`, no sidecars. Useful when the value is just having a tracked
  launcher and an agent-permission boundary (one trusted binary in PATH instead
  of raw shell exec) without paying the dump cost. Per project-local
  run-record policy, trivial janitorial commands do not need Aim records.

For the full schema and algorithms (input source resolution, output sidecar
writing, propagation protocol, plugin contract), see
`topics/provenance-tracking.md`. For the agentctl plugin/hook surface
specifically, see `topics/agentctl.md`.

# Long-running commands 
If a command times out:
- Clearly say "Command timed out after X minutes"
- Show the last 100 lines of output
- Show the exact command that was run
- Ask me if I want to increase the timeout or change flags

When running builds or tests, always redirect full output to a log file
(e.g., `make 2>&1 | tee /tmp/build.log`) and show only the tail.
Never discard output with bare `| tail`.

For `agentctl` and other long-running waits, do not say `in agentctl wait.`
unless the wait/watch command is still live in this turn and you are actively
using its output as the current control point. If the environment will not
reliably wake you on completion, do not use that phrase.

A resolved wait is not a resting state. Once the watched job finishes or the
relevant idle condition is met, immediately consume that completion and launch
or attach the next already-approved successor in the same turn before giving a
status update.

### Wait watchdog discipline

In this Codex environment, a live PTY does **not** automatically create a new
assistant turn when fresh output appears. Therefore, a bare `agentctl watch`
process is not a sufficient wait primitive by itself. Likewise, a tmux pane
that merely prints status to the screen is useful for the human operator but
does not by itself create a fresh user-input event for the local CLI.

When work is gated on a long-running job, run the wait **in the foreground** and
stay blocked in it until it terminates. A single foreground `agentctl
wait`/`watch` Bash call (bounded per *Blanket wait cap* below) is the intended
liveness/progress reaction: the harness hands control back at the exact moment
the wait condition is met, so the returning block *is* the re-invocation, and one
bounded block stays a cache hit. Do **not** push the wait into the background
(`run_in_background`, a detached `&`, a fire-and-forget watchdog) when you must
react to its completion — a backgrounded wait forfeits that turn continuation,
falls out of cache, and degrades into ad hoc polling. The default wait primitive
is:
- the built-in `agentctl wait/watch --heartbeat ...` path first, run foreground;
  prefer this over ad hoc shell sleep loops when all you need is bounded-latency
  liveness output
- a foreground watchdog process that emits a timestamped poll at least every
  300 seconds and includes `agentctl status`/`list` plus `nvidia-smi`
- explicit PTY polling by the agent at least every 300 seconds while the wait
  is active
- when Codex itself is running inside tmux, a second helper from another shell
  or pane that periodically injects a benign key into the Codex pane so the
  local CLI receives a real tty input event; default to `C-l` unless there is
  a concrete reason to use a different key sequence

When a healthy run is the only active foreground obligation, prefer the
low-token `agentctl` heartbeat path over repeated log pulling or speculative
planning. Use the heartbeat interval to keep the session recoverable, then
defer deeper planning and analysis until the run finishes, fails, stalls, or
needs a successor decision.

User heartbeat or activity turns are wake-up points, not a request to stay in
high-token log-following mode forever. At minimum, check current run and GPU
state, give a concise status, and briefly engage with steering, planning, or
pre-finish interpretation when useful, then re-enter the foreground wait in the
same turn. That blocking call *is* the low-token posture and the way you stay
available — the user interrupts it to interject again. Do not idle for ~N minutes
of possible input first: this harness has no such timed stay-open state, since
yielding the turn forfeits any auto-resume of the wait while blocking is itself
interruptible rest. Resume the block immediately.

Use the helper `~/agents/agent-wait-watchdog` (mirrored as
`~/bin/agent-wait-watchdog`) when you need an external poll block that combines
`agentctl` state with `nvidia-smi`, not as the first-line substitute for the
built-in `agentctl` heartbeat. When Codex is running inside tmux and prolonged
quiescence would be harmful, pair the normal `agentctl` wait/watch path with
`~/agents/agent-tmux-nudge` (mirrored as `~/bin/agent-tmux-nudge`) targeting
the Codex pane. This helper is for synthetic tty input, not for on-screen
dashboards.

Never claim to be waiting on a job after the watchdog or watch PTY has already
resolved. Re-check live state first.

Early failure is a terminal result, not a wait state. After any manual sleep,
timeout, interrupted tool call, or "no output yet" poll for an `agentctl` run,
immediately run `agentctl status <job>` (or `agentctl list --failed`) before
telling the user the run is still pending. If status is `finished` with a
nonzero or `unknown` return code, inspect the run log and report the failure
instead of continuing to wait. Prefer `agentctl wait <job> --target
not-running --heartbeat ...` over ad hoc `sleep; cat summary` loops because it
returns nonzero for failed runs and prints the final return code and log path.

Do not use GPU-idle thresholds for a short sidecar watch if another intended
GPU job is still running. For sidecars, watch the job to completion only; keep
GPU-idle watches for the gating job whose successor truly needs the GPU clear.

If a watched job is no longer running, or the GPU is idle unexpectedly, or an
already-approved successor can now be launched, the wait state is over and must
be consumed immediately in the same turn.

See `~/agents/yepanywhere.md` for heartbeat turn handling and the `PULSE:`
observability convention.

### Blanket wait cap (55 min)

All agents here bound a foreground `agentctl wait` at **55 min**
(`--timeout 3300`). The cap segments one logical wait, so **re-wait is
mandatory**: on a still-running return (timeout exit 1, `timeout waiting for
<job> to reach <target>` on stderr) start another 55-min wait; only a terminal
status ends the loop (a finished `unknown`/nonzero returncode is failure — the
still-running case that *Early failure is a terminal result* leaves open).
Best-effort in practice: an agent mid-analysis may instead pause to confirm
with the user, which is fine.

The dual when nothing is waiting: in GPU-fill / steward mode idling is the
failure — the default, even absent user feedback, is to launch a useful or
speculative job at **low recorded priority** (an explicit interrupt/abandon
candidate), not to wait. Slot it via *On-deck GPU fillers* and the
on-deck/steward instructions.

55 sits under both the 59-min harness ceiling and the 1h extended-cache TTL,
so one block stays a cache hit while waking the model only ~once an hour. Do
not re-poll under 5 min for genuinely long jobs — that churns context and
degrades reasoning for no cache gain; the sub-TTL re-poll only helps under the
5-min standard cache, which is not in use here.

The agent must pass an explicit ~59-min `timeout` on the Bash call that runs
the wait; the 2-min default (`BASH_DEFAULT_TIMEOUT_MS`, deliberately left
unset) otherwise kills any call that does not opt in — wanted for silent
hangs.

- **Claude:** the ceiling is `BASH_MAX_TIMEOUT_MS=3540000` (ms = 59 min), set
  before launch (`~/keys.sh`) and kept on yepanywhere's claude-provider env
  allowlist so the session env scrub does not strip it. Some versions ignore
  the var, so validate once per build with a wait that should return "still
  running" at 55 min; if it is killed earlier the cap is not honored and the
  scheme silently fails.
- **Codex:** no such env var or `config.toml` key; `agentctl --timeout`
  carries the cap by itself (Codex has no default shell timeout). Confirm the
  internal `bash -lc` wrapper timeout does not cut a 55-min foreground short.

### Natural pause run status

When reaching a natural pause in any project that has run operations,
background jobs, `.agentctl/`, `*.running.md`, or GPU scheduling state, end the
status or final response with a brief live run/GPU footer even if no wait is
currently active. This footer should use the freshest cheap checks available
(`agentctl list` / `agentctl status` and `nvidia-smi` when present), name active
jobs if any, and say explicitly when there are no active jobs and the GPU is
idle. If the known queue is exhausted, say that too rather than leaving the user
to infer it from silence.

If planned or pending runs are known, end with a clearly marked `Pending GPU
Jobs` line naming them. If none are known, write `Pending GPU Jobs: none known`
or the closest truthful equivalent. This is a presentation rule for observability
at handoff/pause points; it does not weaken the stronger keep-busy rule that
agents should zoom back out, choose, and launch the next valuable planned run
when the project instructions call for that.

### Failure postmortems

When troubleshooting your own failure to comply with instructions, explicitly
cite the RUNS/AGENTS sections that were likely governing or distorting the mistaken
behavior. This may require post-hoc reconstruction rather than direct access to
the exact activations that produced an earlier turn; say so plainly when
uncertain. Prefer section headers and short quoted phrases over vague
summaries, for example `Long-running commands`, `Wait watchdog discipline`, or
repo-local wait-state rules.
