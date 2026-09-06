# Codex Supplement

Read this after `~/agents/AGENTS.global.md` and `~/agents/AGENTS.user.md` when
running in Codex / OpenAI Codex. This file contains Codex harness
mechanics; shared and model-scoped policy stays outside this file.

Model tier: do not trust self-knowledge of your model name — models
misreport it. Use `$AGENT_LAUNCH_MODEL` when present; otherwise read the
harness-recorded id from your own rollout file:

```bash
tac "$(find ~/.codex/sessions -name "*$AGENTCTL_SESSION_ID*.jsonl" |
  head -1)" | rg -m1 -o '"model":"[^"]*"'
```

Below GPT-5.5 (e.g. Codex 5.3 Spark), or with `AGENTS.weak.md`
surfaced, you are weak tier: read `~/agents/AGENTS.weak.md` and do
not read `AGENTS.frontier.md`. At GPT-5.5 or above, read
`~/agents/AGENTS.frontier.md` next — frontier-tier latitude.

Then load the model-scoped behavior patches selected by that same recorded id:
an id containing `claude` reads `~/agents/AGENTS.anthropic.md`; an id containing
`opus` also reads `~/agents/AGENTS.opus.md`; an id containing a `sol`
model-family segment (for example, `gpt-5.6-sol`) reads
`~/agents/AGENTS.sol.md`; an id containing an `astra` model-family segment
(for example, `gpt-6-astra`) reads `~/agents/AGENTS.astra.md`. This routing
follows the model across harnesses rather than assuming Codex always runs Sol.

## Session Identity

Register the real resumable Codex id, never an invented tag. Normally use
`agentctl active "<banner>" [scope...]` without an id; `active`, `others`, and
`alone` resolve `$AGENTCTL_SESSION_ID`, else a `resume <id>` process ancestor.
If resolution reports "no session id", read `topics/codex-session.md`
§ Identity recovery and recover this session's real id before retrying.
Do not create a placeholder entry. `topics/agentctl.md` owns helper semantics.

## Session Logs

When `AGENTS.global.md` says to search provider session logs, search
`~/.codex/sessions/**/*.jsonl`, excluding your own session
(`$AGENTCTL_SESSION_ID`).

Rollout lines are wall-clock timestamped (top-level `timestamp`,
ISO-8601 Z). The rendered prompt carries no times, so elapsed
time between turns is invisible in context but recoverable here:
date a past observation by grepping your own rollout file.
`queued-anchor` v1 (spec: `topics/helper-scripts.md`) parses only
Claude transcripts; on Codex, read the timestamps directly.

## Programmatic exec output budget

`functions.exec` and a nested `exec_command` apply independent result
budgets. Without `functions.exec`'s first-line `// @exec` pragma, the current
outer default is 10,000 tokens: once exceeded, the model receives roughly the
first and last 5,000 with the middle elided. A larger nested
`max_output_tokens` alone cannot raise that outer ceiling.

Treat about 10,000 tokens minus wrapper text as the maximum complete read for
this default call shape. The pragma may request more, but a harness policy cap
can still lower it. Required reads approaching the smaller active budget use
separate calls or bounded ranges; any truncation warning or elision marker
means the read remains incomplete.

## Code-mode cell handles

A terminal `wait` result consumes its `cell_id`; do not wait on that id again.
Reuse the id only when the most recent result explicitly says the script is
still running with that cell id.

## Turn-End Is A Dead Stop

Do not send a final response while you own an unconsumed running/queued job or
its successor decision unless the user explicitly deferred it. Consume the
result or stay in a foreground wait; a promise to resume is not a wakeup.
Before launching, resuming, or waiting on such work, read
`topics/codex-session.md` § Job ownership and waits alongside the triggered
RUNS packets. User questions and compaction do not discharge ownership.

## Skills Path Aliasing

`~/agents/skills` and the current Codex user root `~/.agents/skills` may alias
the same directory;
treat `~/agents/skills` as the canonical edit target. Do not "sync" them into
symlinks — that creates self-referential loops that break skill loading.
Follow symlinks when checking identity:

```bash
stat -Lc '%d:%i %n' ~/agents/skills ~/.agents/skills
```
