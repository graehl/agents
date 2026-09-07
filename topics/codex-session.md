# Codex session mechanics

> Recover a real Codex session identity and preserve owned work across waits
> without loading rare recovery and run mechanics into every task.

Topic: `codex-session`

`AGENTS.codex.md` routes the matching section at identity-recovery and owned-job
boundaries. Shared registration semantics belong in `agentctl.md`; run policy
belongs in `RUNS.md` and its packets. Higher-priority tool limits still govern
which wait durations the current harness can actually use.

## Identity recovery

Use the real resumable id, not a personal tag. The `~/bin/codex` wrapper exports
`AGENTCTL_SESSION_ID` from positional `codex resume <id>`; when absent,
`agentctl` can walk process ancestors for it. `AGENTCTL_NO_PROC_SESSION_ID`
disables that fallback. A present launcher id already supplies the answer.

Only after the normal environment/process routes fail, use available evidence
to establish this session's id. Recovery is open-ended, not a fixed sequence.
Useful clues include rollout files under `~/.codex/sessions/` (first-line
`session_meta.payload.id` and cwd), launch time, process state, and distinctive
conversation content. Recency or an absent active entry can rank candidates;
neither proves identity when fresh or resumed peers share the cwd.

Set `AGENTCTL_SESSION_ID` to the recovered id and call `agentctl active` in the
same Bash invocation; agent-set environment does not persist across tool
calls. If recovery remains ambiguous, report the specific missing evidence
instead of registering a false identity. An invented id leaves an orphaned
live-peer entry when a later shell or resume supplies the real one.

## Job ownership and waits

Do not assume native Codex will start another turn after a final response.
Consume running/queued work and the successor decisions you own, or remain in
the announced foreground `agentctl wait`/`watch` at the earned rung from
`_RUNS/monitoring.md` § Wait watchdog discipline. Explicit user deferral is the
exception. A launcher completion-wake facility is separate; its availability
alone does not establish that a wake is armed for this job.

Answer an interactive question, then re-enter the wait in the same turn.
After compaction, re-verify job state and continue; compaction does not clear
the obligation. A completed job still needs its result consumed. The motivating
incident ended a turn with a queued training chain; after it finished, a GPU
remained idle until the user returned ten hours later.

For Codex running GPT-5.6 or later, the configured foreground ladder is
`5 → 10 → 20 → 28 minutes`, replacing RUNS' 40- and 55-minute rungs. This is
the cache-margin policy recorded in `agent-instructions.evidence.md` under
"2026-08-10 — GPT-5.6 Codex waits stay inside cache minimum"; it is not a
claim about a newly verified provider cache guarantee. Other models retain
the ordinary RUNS ladder. This bounds observer lifetime, not passive time
without model continuation. Every observer timeout still requires status,
consumption if complete, or another wait if work remains.

During waits, schedule return to the model at most 540 seconds apart, allowing
for return/continuation overhead before ten minutes. This is the user's
cache-warmth precaution, not a verified eviction threshold; it supersedes the
older allowance for a passive 28-minute tool call. A printed command heartbeat
alone does not establish model continuation. If the harness cannot yield back
to the model while the observer lives, shorten the observer timeout accordingly,
within the earned rung and any stricter tool limits.

A tool's `yield_time_ms` controls one call's blocking interval; it does not set
`agentctl wait --timeout`. Continue the same live terminal `session_id` with
`write_stdin`, or the same still-running orchestration `cell_id` with
`functions.wait`. Do not hide repeated short yields inside an orchestration
loop that withholds model continuation beyond 540 seconds. Required short tool
yields are transport polling; repeatedly launching short-lived observers adds
unnecessary polling and announcements. Announce a new observer, not each yield.
`--poll` checks job state; `--heartbeat` prints status. Neither sets observer
lifetime or proves cache warmth. Consume a terminal result instead of reusing
its handle.
