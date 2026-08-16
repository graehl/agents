# Long-run monitoring and completion

> Rules, protocols, and rationale for detachment, foreground waits, watchdogs, status reporting, and failure reconstruction.

Read this packet before launching a job expected to outlive the session,
receiving or resuming a yielded live terminal/session handle from run work,
entering a foreground wait, monitoring or summarizing a long job, or
reconstructing a run-policy failure. `RUNS.md` is the router and wins on
conflict.

## Binding rules

### Long-running commands

For a generic command timeout, state the elapsed limit, show the exact command
and useful log tail, and ask whether to extend the timeout or change flags.
Builds and tests keep full output in a log; never discard upstream status behind
a bare `| tail`.

For foreground `agentctl` monitoring, use native `wait`/`watch --timeout` and
`--tail`. Never wrap it in shell `timeout` or pipe it through `tail`: the
pipeline can report the wrong process status. A watch-window timeout returns
124 and leaves the job running; `[agentctl-watch-timeout-v1]` distinguishes it
from a payload that itself exits 124.

#### Foreground wait atomic protocol

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

#### Detach long runs from the session

A run expected to exceed about 15 minutes launches detached so session teardown
cannot kill it. Use two commands: `agentctl start ... -- <cmd>` without
`--watch`, then a separately announced foreground `agentctl wait/watch`.
`start --watch` or a harness-owned background shell can keep the payload in the
session descendant tree. If uncertain, verify the payload's PPID is 1. Short
smokes and janitorial jobs may remain attached.

#### Wait watchdog discipline

When completion requires agent reaction, wait in the foreground. Prefer
`agentctl wait/watch --heartbeat ... --timeout ...`; use `wait-work` when
awaiting a new launchable item. A background wait, passive PTY, or tmux dashboard
does not create a reliable continuation in harnesses without wake-up support.
External watchdog/nudge alternatives and their exact use appear below under the
second “Wait watchdog discipline” heading.

Keep healthy-run waiting low-token: heartbeat rather than repeated log pulls.
On a user activity turn, check live run/GPU state, engage briefly, then re-enter
the foreground wait in that same turn. Never claim a wait remains live after
its process resolved.

After any interrupted wait, manual sleep, timeout, or no-output poll, query
`agentctl status <job>` before saying the job is pending. A finished
nonzero/unknown return code is failure: inspect the log and report it. Watch a
short sidecar by job completion, not GPU-idle, while another intended GPU job
still runs.

#### Proven foreground-wait cap

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
ceiling details and validation probes appear below under the second “Proven
foreground-wait cap (5 → 55 min)” heading.

When nothing is waiting and GPU-fill/steward work is active, idle capacity is
the failure: launch an eligible useful or speculative job at low recorded
priority rather than entering an empty wait.

#### Natural pause run status

At a natural pause in a project with run/GPU state, end with a fresh concise
run/GPU footer: active jobs or explicitly none, GPU use or idle, and whether
the known queue is exhausted. Always include `Pending GPU Jobs: ...`, using
`none known` when truthful. This observability footer does not weaken the
keep-busy rule.

#### Failure postmortems

When reconstructing a failure to follow run policy, cite the governing
_RUNS or AGENTS section and distinguish direct evidence from post-hoc inference.
Prefer section names and short exact phrases over vague summaries.

## Retained detail and examples

### Long-running commands
If a command times out:
- Clearly say "Command timed out after X minutes"
- Show the last 100 lines of output
- Show the exact command that was run
- Ask me if I want to increase the timeout or change flags

When running builds or tests, always redirect full output to a log file
(e.g., `make 2>&1 | tee /tmp/build.log`) and show only the tail.
Never discard output with bare `| tail`.

For foreground `agentctl` monitoring, use `wait`/`watch`'s native `--timeout`
and `--tail` options. Never wrap them in shell `timeout` or pipe them through
`tail`: a pipeline reports its final `tail` process's status instead of the
watched job's, and merging with `2>&1` also mixes agentctl control messages
with payload output. Use the one-command form:

```bash
agentctl watch JOB --tail 2 --heartbeat 1500 --timeout 3300
```

Completion returns the watched job's exit code. A watch-window timeout leaves
the job running, returns 124, and emits `[agentctl-watch-timeout-v1]` on
agentctl's stderr; the marker plus exit code distinguishes it from a watched
payload that itself exits 124.

**The announcement.** Immediately before entering a foreground `agentctl`
wait/watch, tell the user exactly: `going into foreground agentctl wait now.`
Then invoke the blocking `agentctl` call as the next action in the same turn
and keep the turn open until it returns. The call must be synchronous with
this assistant turn: a meaningful output line, watched condition, job end, or
timeout must return control to the agent. A tool call yielding only a
terminal/session id does not satisfy the announcement; immediately continue
consuming that session without sending a response. Use `agentctl fleet-watch`
with the local host included when fleet/resource availability is the wake
condition; otherwise use the specific job's normal `wait`/`watch`.

The announcement creates an execution obligation. Do not make it unless the
effective foreground call is the next action, and do not replace it with a
post-launch `in agentctl wait` response: yielding that response can tear down
the monitor and forfeit completion wake-up.

**Hard gate — no latitude or inferred equivalent.** The announcement and its
effective synchronous `agentctl` call are one atomic protocol. After the
announcement, the agent may emit no final/status/planning prose and run no
status query or unrelated tool before starting the call. While a yielded
terminal/session remains live, the only permitted action is continuing to
consume it until a wake condition or timeout returns control. Background
monitoring, a detached job, a session id, `agentctl status` polling, or an
intention to reattach later is not equivalent. If the call fails to start,
report that failure immediately and never claim the wait occurred. Any
violation resets this session's proven wait cap to five minutes and must be
disclosed explicitly.

**New user steering interrupts the atomic interval.** When the user interrupts
with other work, the agent may stop the foreground monitor and use background
status checks while doing that work, until the user asks it to foreground-wait
again. This is neither a failed wait nor a protocol violation, and it neither
resets nor advances the proven timeout rung. A later foreground wait still
requires a fresh state check, announcement, and immediately following
synchronous call.

A resolved wait is not a resting state. Once the watched job finishes or the
relevant idle condition is met, immediately consume that completion and launch
or attach the next already-approved successor in the same turn before giving a
status update.

#### Detach long runs from the session (teardown immunity)

Any run that may exceed ~15 min must **launch detached and be monitored
separately** — it must not stay a child of the agent process. When the agent
session is torn down or restarted (UI stop, crash, Monitor timeout, process
exit), the harness SIGKILLs its **whole descendant process tree**; a job still in
that tree dies mid-run, a job that has left it survives.

With `agentctl`: `agentctl start … -- <cmd>` **without** `--watch` forks the
payload under `setsid` (`start_new_session=True`) and the launcher exits, so the
job reparents to **init (PPID 1)** and leaves the descendant tree — teardown-immune.
What defeats this is keeping a session-tied parent alive on top of the detached
job: `agentctl start --watch` (the watcher blocks in the launching shell, re-
anchoring the job as a descendant) or wrapping the launch in a backgrounded shell
the harness still owns. Either way the teardown SIGKILL reaches the job. `agentctl`
itself documents the split ("start queued work detached, then watch the job").
Verify once if unsure: `ps -o ppid= -p <job-pid>` should print `1`.

For a run expected to exceed 15 minutes, therefore use two commands: detached
`agentctl start` first, then the separately announced foreground
`agentctl wait/watch`. Never use `start --watch` for that run class.

Monitor the now-detached job with a **separate** `agentctl watch`/`status`/`wait`
(foreground or backgrounded per the harness — see *Wait watchdog discipline*). That
monitor process is disposable: its death (turn boundary, teardown) does not touch
the reparented job, so re-attach freely. Short jobs (≲15 min, smokes, janitorial)
can stay attached under `--watch`; the detach rule is for the runs whose loss hurts.

#### Wait watchdog discipline

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
  liveness output. When the thing awaited is new work rather than a known
  job — a fresh launch to watch, or a new `on-deck/` entry to tend —
  `agentctl wait-work` is the same foreground-block primitive
  (`topics/agentctl.md`)
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

#### Proven foreground-wait cap (5 → 55 min)

Every resumable session starts with a maximum foreground-wait timeout of
**5 minutes**. Longer calls are earned only when this session's transcript
shows the previous rung actually remained live until its awaited condition or
timeout. Use the ladder **5 → 10 → 20 → 40 → 55 minutes**; a failed start,
lost terminal/session, announcement alone, or assistant response while the
monitor is pending does not advance it. A new resumable session starts again
at five minutes. This observable gate is excluded from any frontier-agent
latitude to substitute an inferred equivalent for the required steps.

The cap segments one logical wait, so **re-wait is mandatory** when the job
remains healthy: inspect status after a timeout, announce again immediately
before the next synchronous call, and use at most the next earned rung. Only
a terminal status ends the loop (a finished `unknown`/nonzero returncode is
failure — the still-running case that *Early failure is a terminal result*
leaves open). Best-effort in practice: an agent mid-analysis may instead pause
to confirm with the user, which is fine.

The dual when nothing is waiting: in GPU-fill / steward mode idling is the
failure — the default, even absent user feedback, is to launch a useful or
speculative job at **low recorded priority** (an explicit interrupt/abandon
candidate), not to wait. Slot it via *On-deck GPU fillers* and the
on-deck/steward instructions.

The earned 55-minute maximum sits under both the 59-minute harness ceiling and
the 1h extended-cache TTL. The shorter initial rungs are a liveness proof, not
a preferred steady-state polling cadence.

The `agentctl wait`/`watch` invocation must carry its explicit native timeout.
Set the harness's tool-call timeout slightly above that bound so agentctl
regains control first; do not prefix the command with shell `timeout`. The
2-min Bash-tool default (`BASH_DEFAULT_TIMEOUT_MS`, deliberately left unset)
otherwise kills a call that does not opt into a longer tool-call allowance —
wanted for silent hangs, but not the foreground-wait deadline.

- **Claude:** the ceiling is `BASH_MAX_TIMEOUT_MS=3540000` (ms = 59 min), set
  before launch (`~/keys.sh`) and kept on yepanywhere's claude-provider env
  allowlist so the session env scrub does not strip it. Some versions ignore
  the var, so validate once per build with a wait that should return "still
  running" at 55 min; if it is killed earlier the cap is not honored and the
  scheme silently fails.
- **Codex:** no such env var or `config.toml` key; `agentctl --timeout`
  carries the cap by itself (Codex has no default shell timeout). Confirm the
  internal `bash -lc` wrapper timeout does not cut a 55-min foreground short.

#### Natural pause run status

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

#### Failure postmortems

When troubleshooting your own failure to comply with instructions, explicitly
cite the _RUNS or AGENTS sections that were likely governing or distorting the mistaken
behavior. This may require post-hoc reconstruction rather than direct access to
the exact activations that produced an earlier turn; say so plainly when
uncertain. Prefer section headers and short quoted phrases over vague
summaries, for example `Long-running commands`, `Wait watchdog discipline`, or
repo-local wait-state rules.
