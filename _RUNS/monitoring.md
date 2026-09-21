# Long-run monitoring and completion

> Rules, protocols, and rationale for detachment, foreground waits, watchdogs, status reporting, and failure reconstruction.

Read this packet before launching a job expected to outlive the session,
receiving or resuming a yielded live terminal/session handle from run work,
entering a foreground wait, monitoring or summarizing a long job, or
reconstructing a run-policy failure. `RUNS.md` is the router and wins on
conflict.

## Binding rules

For launch or waiting, read Long-running commands and its applicable
subsections through Proven foreground-wait cap. Natural pause run status
applies to status/handoff pauses; Failure postmortems applies to policy-failure
reconstruction. Harness wait-limit diagnosis is only for diagnosing or
validating provider timeout behavior.

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

#### Launch observation and completion observers

Run `agentctl start` in the foreground. Its default launch observation begins
only after dependency/resource waits and reproducibility checks pass and the
payload process is created, then returns an early terminal status during the
next five seconds; process-creation failure returns before the clock starts. A
failure also prints the log tail. `--launch-wait 0`
explicitly skips that window. Do not background `start`, locally or through
SSH; if immediate return from a deep queue is needed, use `--launch-wait 0` and
attach the explicit observer below.

Every run still live after `start` returns must have one completion observer.
The reported `completion_wake=armed` qualifies. When it is `unarmed`, start an
explicit `agentctl wait/watch` before yielding. Keep that wait in the foreground
when its result gates the next action. It may instead use a harness-tracked
background facility while the agent performs other work only when that facility
creates a completion event/turn on success or failure. A shell `&`, passive PTY,
tmux pane, repeated `status`, or intention to check later is not an observer.
Only explicit wait/watch commands are candidates for backgrounding; never the
launch command itself.

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

For claim-clearance waits (`agentctl clear`), a streamed peer notice is also
an observation point: the agent may pause the wait to converse, then resume or
cancel it under `topics/agentctl.md` § Claim-clearance dialogue. The notice
grants neither clearance nor user authorization.

#### Detach long runs from the session

A run expected to exceed about 15 minutes launches through detached
`agentctl start ... -- <cmd>` without `--watch`. Keep `start` foreground through
its bounded launch observation. Under YepAnywhere, `agentctl` automatically
places the wrapper in a transient systemd user service, outside the app-server
session cgroup; `--user-service` requests the same boundary elsewhere and
fails visibly when no user manager is available. `--no-user-service` is an
explicit downgrade to the process-session wrapper. Then rely on an armed
completion wake or attach the separately announced `agentctl wait/watch`.
Short smokes and janitorial jobs may remain attached.

#### Wait watchdog discipline

When completion requires agent reaction, wait in the foreground. Prefer
`agentctl wait/watch --timeout ...` with its default heartbeat; use `wait-work`
when awaiting a new launchable item. A background wait, passive PTY, or tmux
dashboard does not create a reliable continuation in harnesses without wake-up
support.
Use `agentctl wait JOB --heartbeat-gpu --gpu 0 --timeout 5m` when the
heartbeat should include GPU state. For capacity readiness independently of a
job, use `agentctl wait-gpu --gpu 0 --max-memory-used <MiB> --timeout 5m`;
choose the threshold from the successor's VRAM requirement and headroom.
For fleet readiness, use `agentctl fleet-watch` under `topics/agentctl.md`
§ Fleet capacity watch. These foreground waits follow the same announcement
and live-handle protocol. Job completion and GPU readiness are different
conditions: do not substitute GPU-idle for a sidecar's terminal status.

Keep healthy-run waiting low-token: heartbeat rather than repeated log pulls.
Keep completion polling separate from status output: `--poll` may stay short so
completion returns promptly. For an unchanged healthy run, use the default
`wait`/`watch` heartbeat: one status line on entry, then one every 540 seconds.
A line of foreground `agentctl` wait output must reach the harness at least
every 570 seconds (9.5 minutes); retain the 540-second default for margin.
Do not buffer or swallow those lines in a wrapper. Yield and consume live
tool output often enough to meet that bound, continuing the same live handle.
Harness/model rules may additionally require model continuation; printed
output alone does not prove cache reuse.
A shorter explicit heartbeat is only for bounded startup or diagnosis; never
leave minute-spaced unchanged-status output active through a long steady wait.
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
ceiling details and validation probes are under “Harness wait-limit diagnosis”;
read that section only when diagnosing or validating a harness timeout limit.

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

### Harness wait-limit diagnosis

The earned maximum remains subject to the actual harness ceiling and any
stricter model policy. The shorter initial rungs establish liveness; they do
not set the steady-state heartbeat or model-continuation cadence.

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
