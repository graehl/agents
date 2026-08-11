# RUNS

Load this file before launching, monitoring, or summarizing a long-running job.
After compaction or resume, an earlier read is not proof that this policy
survived: re-read this main file at the next run-operation boundary unless the
harness verifiably reconstructs this exact current packet in model context or a
boot-loaded scoped supplement explicitly sets an evidence-backed cadence.

This file retains triggers and binding rules. `RUNS.supplemental.md` holds
optional templates, rationale, examples, and rare mechanics; read its matching
section when this compact rule is insufficient. This file wins on conflict.

## GPU access for Python ML commands

For an ML repository with local accelerators, run Python with GPU-visible
permissions whenever imports may reach `torch`, `transformers`, `unsloth`,
`vllm`, TensorRT, or similar code, including `--help` paths that import before
argument parsing. A sandboxed CUDA-detection failure is not evidence that the
host has no GPU; retry with GPU visibility before drawing that conclusion.

Before launch, inspect `nvidia-smi`. Unexpected existing use warrants a warning,
but proceed when estimated free VRAM still leaves the planned run safe. Block or
change the plan only when current use makes launch materially risky.

Every PyTorch job sets:

```text
PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True,garbage_collection_threshold:0.5
```

Source a project `env.sh` that sets it or export it explicitly before detached
jobs. `PYTORCH_ALLOC_CONF` (without `CUDA_`) is silently ineffective.

## GPU utilization and parallelism policy

On a non-shared GPU, keep already-planned work moving without waiting for
another prompt:

- After launch or completion, inspect VRAM and utilization.
- When the current run uses under 50% of total VRAM, launch an independent
  planned job that fits with at least 10% headroom. One run is sufficient only
  at 80% or more VRAM or sustained utilization; 50–80% is the trigger zone for
  finding a compatible second run.
- Runs are independent only when they use different output locations and
  neither reads the other's in-progress output.
- Draw from the accepted task/research queue first. Propose new experiments
  only when it is exhausted.
- About 30 seconds after each background launch, confirm VRAM rose and inspect
  the log if it did not. Never infer launch success from a PID alone.
- Gate chained GPU successors by observed VRAM release rather than a fixed
  sleep; workers may retain memory after the parent exits.
- When a run finishes, promptly report its headline result, key metrics, and
  one or two useful output comparisons.

### On-deck GPU fillers

`on-deck/` is an optional guarded queue of single-step fillers; its contract is
`topics/on-deck.md`. The queue answers what should run next, while `.agentctl/`
records what is running. `/steward` performs one fill-until-full pass;
`/rep steward` repeatedly services it. An absent queue is a no-op.

A steward may launch an eligible entry without confirmation when its guard
passes, its skip condition is false, and its cost is within steward autonomy.
Preempt a lower-priority filler only when the saved time justifies lost work and
the stop is safe.

## Routine run-operation authority

Routine, reversible plumbing needed for an already-approved run—GPU access,
project edits, shell execution, logging, and stopping processes launched by this
session—is authorized. This does not broaden the task: global big-effect,
shared-worktree, secrecy, and destructive-action gates still govern. After a
sidebar, resume the agreed run step unless the sidebar changed the plan; ask
only when the remaining alternatives materially differ.

## Research artifact metadata

Anchor an important saved output with:

- `<out>` — primary artifact;
- `<out>.meta.md` — compact human provenance/summary for legacy or manual runs;
- `<out>.log` — full runtime log; and
- `<out>.running.md` — crash-resilient in-flight record, removed after clean
  completion.

### In-flight job tracking (`.running.md`)

The launching agent or `agentctl` writes the marker immediately; payload
scripts do not own it. Record at least status, PID, start time, cwd/full command,
log, and output. On resume, find markers, use `kill -0` and the log to classify
live versus interrupted work, and treat an adjacent completed metadata sidecar
as stale-marker cleanup. `agentctl cleanup-running` is the canonical sweep.
The exact template and explicit cleanup forms are under “In-flight job
tracking (`.running.md`)” in [RUNS.supplemental.md](RUNS.supplemental.md).

`agentctl start --after <job-or-output>` is for a mechanically determined
successor. Prequeueing eval-after-train is encouraged when exit status is a
sufficient gate. If semantic validity matters, make the successor run a small
standalone guard first; if interpretation is required, wait and inspect instead.

### Run records and provenance

For tracked `agentctl` work, the canonical record is the JSON run dump under
`runs/aim/<experiment>/runs/<run-id>.json`. Follow an output's
`<output>.meta.json` back-pointer before reconstructing provenance from logs.
The record owns argv/cwd, declared inputs and outputs, script fingerprint, Git
state, and producer propagation.

Prefer `agentctl start ... -- <command>` for launches that may need audit or
reproduction. Use the default tracked form for research outputs; use
`--no-aim` only for genuinely trivial runs that need launcher/process handling
but no durable run record.

Stable non-secret project launch defaults may live in tracked
`agentctl.env`. Ambient variables override it, then `--source-env`, then
explicit `--env KEY=VALUE`. Never put secrets there. When one output path must
both reach the payload as `--KEY=PATH` and be declared for provenance, use
`--output-arg KEY=PATH`; plain `--output` is provenance-only.

Bare `agentctl` assumes PATH lookup; fall back to `~/agents/agentctl`, not
`./agentctl` from an arbitrary project. Full schemas and algorithms live in
`topics/provenance-tracking.md` and `topics/agentctl.md`. The legacy
`*.meta.md` template and one-level input inheritance rules are retained under
“Research artifact metadata” in
[RUNS.supplemental.md](RUNS.supplemental.md).

### Verified provenance for row-wise text transforms

A batch translation, paraphrase, or other row-wise rewrite carries stable
source identity in each output row when the format permits: dataset/document,
an explicit base-qualified row locator, source text and hash, Unicode-codepoint
input/output lengths, and `AGENTCTL_RUN_ID`. A keyed sidecar is acceptable only
with exact membership, order, and hash validation; row position alone is not
provenance.

When a tokenizer is already loaded, also record token counts, immutable
tokenizer revision, and special-token convention. Independently resolve a
sample (all rows when cheap) against the source, record the checked count, and
save length-ratio outliers. Acceptance uses a policy frozen before the batch;
same-batch fitting is exploratory only. The normative envelope and check are
`topics/verified-provenance.md` and
`run_quality.length_ratio.LengthRatioPolicy`.

## Long-running commands

For a generic command timeout, state the elapsed limit, show the exact command
and useful log tail, and ask whether to extend the timeout or change flags.
Builds and tests keep full output in a log; never discard upstream status behind
a bare `| tail`.

For foreground `agentctl` monitoring, use native `wait`/`watch --timeout` and
`--tail`. Never wrap it in shell `timeout` or pipe it through `tail`: the
pipeline can report the wrong process status. A watch-window timeout returns
124 and leaves the job running; `[agentctl-watch-timeout-v1]` distinguishes it
from a payload that itself exits 124.

### Foreground wait atomic protocol

Immediately before a foreground `agentctl` wait/watch, tell the user exactly:

```text
going into foreground agentctl wait now.
```

The synchronous wait call is the next action in the same turn. Emit no
intervening status/final prose or unrelated tool call. If the tool yields a live
terminal/session id, only continue consuming it until a wake condition or
timeout returns control. A detached watcher, background polling, or intention
to reattach later is not equivalent. If the call fails to start, report that
and never claim the wait happened. A protocol violation resets the session's
earned wait cap to five minutes and must be disclosed.

New user steering may interrupt the interval without failure; later foreground
waiting requires a fresh state check, announcement, and synchronous call. When
a watched job ends or the awaited resource becomes available, consume the
result and launch or attach an already-approved successor in the same turn
before resting at a status update.

### Detach long runs from the session

A run expected to exceed about 15 minutes launches detached so session teardown
cannot kill it. Use two commands: `agentctl start ... -- <cmd>` without
`--watch`, then a separately announced foreground `agentctl wait/watch`.
`start --watch` or a harness-owned background shell can keep the payload in the
session descendant tree. If uncertain, verify the payload's PPID is 1. Short
smokes and janitorial jobs may remain attached.

### Wait watchdog discipline

When completion requires agent reaction, wait in the foreground. Prefer
`agentctl wait/watch --heartbeat ... --timeout ...`; use `wait-work` when
awaiting a new launchable item. A background wait, passive PTY, or tmux dashboard
does not create a reliable continuation in harnesses without wake-up support.
External watchdog/nudge alternatives and their exact use are optional detail
under “Wait watchdog discipline” in
[RUNS.supplemental.md](RUNS.supplemental.md).

Keep healthy-run waiting low-token: heartbeat rather than repeated log pulls.
On a user activity turn, check live run/GPU state, engage briefly, then re-enter
the foreground wait in that same turn. Never claim a wait remains live after
its process resolved.

After any interrupted wait, manual sleep, timeout, or no-output poll, query
`agentctl status <job>` before saying the job is pending. A finished
nonzero/unknown return code is failure: inspect the log and report it. Watch a
short sidecar by job completion, not GPU-idle, while another intended GPU job
still runs.

### Proven foreground-wait cap

Every resumable session starts at a five-minute maximum foreground wait. A
longer rung is earned only when the transcript proves the prior rung remained
live to its condition or timeout. The global ladder is
`5 → 10 → 20 → 40 → 55 minutes`; a harness/model supplement may tighten or
replace it. Failed starts, lost sessions, announcement alone, or assistant
output while monitoring do not advance it.

A timeout segments one logical wait. If the job remains healthy, inspect state,
announce again, and re-wait using at most the next earned rung. Only terminal
state ends the loop. The `agentctl` call carries its native timeout and the tool
allowance sits slightly above it; do not prefix shell `timeout`. Provider
ceiling details and validation probes are under “Proven foreground-wait cap
(5 → 55 min)” in [RUNS.supplemental.md](RUNS.supplemental.md).

When nothing is waiting and GPU-fill/steward work is active, idle capacity is
the failure: launch an eligible useful or speculative job at low recorded
priority rather than entering an empty wait.

### Natural pause run status

At a natural pause in a project with run/GPU state, end with a fresh concise
run/GPU footer: active jobs or explicitly none, GPU use or idle, and whether
the known queue is exhausted. Always include `Pending GPU Jobs: ...`, using
`none known` when truthful. This observability footer does not weaken the
keep-busy rule.

### Failure postmortems

When reconstructing a failure to follow run policy, cite the governing
RUNS/AGENTS section and distinguish direct evidence from post-hoc inference.
Prefer section names and short exact phrases over vague summaries.
