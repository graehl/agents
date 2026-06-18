# Claude Supplement

Read this after `~/agents/AGENTS.md` and `~/agents/AGENTS.user.md` when
running in Claude. This file contains Claude harness mechanics; shared
policy stays in `AGENTS.md`.

Model tier: do not trust self-knowledge of your model name — models
misreport it. Read the harness-recorded id from your own transcript:

```bash
tac "$HOME/.claude/projects/${PWD//\//-}/$CLAUDE_CODE_SESSION_ID.jsonl" |
  rg -m1 -o '"model":"[^"]*"'
```

A haiku-class (small-tier) id, or a surfaced `AGENTS.weak.md`, means
weak tier: read `~/agents/AGENTS.weak.md` and do not read
`AGENTS.frontier.md`. Otherwise read `~/agents/AGENTS.frontier.md`
next — frontier-tier latitude.

## Session Identity And Logs

If `$AGENTCTL_SESSION_ID` is already set in your Bash env, use it
verbatim and skip the transcript-stem discovery below — that is the
done answer, not a hint to verify. A launcher such as yepanywhere
(YA) injects it per command through a `BASH_ENV` bridge, and
`agentctl` adopts the same var first, so its `active/` entry and
yours name the same file with no extra work. When the launcher mints
that id with `claude --session-id <uuid>` (the supported way to fix a
new session's id up front), it also equals this session's transcript
stem; if it is an arbitrary tag instead, `active/` stays
self-consistent but will not match a transcript.

Otherwise the harness exports your session id ambiently as
`$CLAUDE_CODE_SESSION_ID` in every Bash shell — use it directly as
the session id for `.agentctl/active/<session-id>` and other
identifiers. It equals the stem of this session's transcript at
`~/.claude/projects/<project-hash>/<session-id>.jsonl`, where
`<project-hash>` is cwd with `/` replaced by `-` (leading `/`
becomes a leading `-`).

You do not need to do anything for active-sessions upkeep:
`agentctl` adopts `$CLAUDE_CODE_SESSION_ID` on its own (no export,
no per-call prefix), so plain `./agentctl start …` maintains this
session's entry (`AGENTS.md` § Active sessions), and a launched job
never inherits your identity (agentctl's internal launch-depth
counter). Because each Bash tool call is a fresh shell, do not rely
on `export`ing the id to carry between calls — the ambient var
already does that.

If `$CLAUDE_CODE_SESSION_ID` is empty (very first turn before the
transcript exists), derive it from the newest transcript stem, and
fall back to a temporary personal tag only until the real id
appears — do not silently keep the tag once the real id is known:

```bash
cwd=$(pwd -P)
project_dir="$HOME/.claude/projects/${cwd//\//-}"
ls -t "$project_dir"/*.jsonl 2>/dev/null |
  head -n1 | xargs -r basename | sed 's/\.jsonl$//'
```

When `AGENTS.md` says to search provider session logs, search
`~/.claude/projects/**/*.jsonl`, excluding the current session
file.

## Pause-then-default flows ("wait for steer, else proceed")

The harness gives you a turn from exactly three things: a user message, a
*tracked background job* finishing (an `agentctl wait …` or other command
launched in the background re-invokes you on completion), or a *scheduled
wakeup* (`ScheduleWakeup`, verified this session; `CronCreate` for a native
cron schedule). Ending a turn with **no running job and no wakeup** is a
dead-stop — nothing fires, so an announced "proceed if no steer" never happens
and you sit idle until the user types. This has bitten a real session: the
agent said it would proceed, then stalled.

Pick by weight of the fork:

- **Light / interruptible step** (the next run in an interruptible research
  campaign, cheap and reversible): just proceed this turn and say what you did.
  Accept that the proposal scrolls off-screen — fine when the step is cheap.
- **Weighty fork** (expensive, hard to reverse, or the user clearly wants a
  say): do **not** silently proceed and do **not** dismiss the wait. State an
  **absolute wall-clock deadline** the user can act on — "answer before
  5:45 PST or I begin as proposed" — and schedule a wakeup to fire then
  (`ScheduleWakeup` with `delaySeconds` = seconds-to-deadline, capped at 3600;
  `CronCreate` for a true absolute-time/cron firing). When it fires, check for
  an intervening user message; if none, proceed exactly as proposed and say so.
  The absolute time keeps the commitment legible as the chat scrolls, which a
  bare "5 minutes" does not.

During an autonomous campaign keep at least one tracked job running so
completion-notifications self-sustain the loop; the wakeup/cron is the fallback
for gaps. **Invariant:** never end an autonomous-work turn with no job running
and no wakeup scheduled — verify before yielding.
