# Intervention needles

> A first-pass filter over harness session logs that lists user turns
> starting with `bad` or `no`, so a reviewing agent can judge which ones
> corrected an agent and generalize those into guidance or tooling changes.

Topic: `intervention-needles`
Governs: mining session logs for user corrections or interventions

## The signal

A user who gives one ask and walks away mostly speaks mid-task to
intervene. An engaged user also asks questions that change nothing, so a
mid-task turn is not by itself a correction. The user's convention is to
open a deliberate correction with `bad` (`Bad`, `bad!`, `bad.`). A turn
that opens with `no` followed by punctuation, a newline, or nothing else
is a broader, natural-speech candidate. `scripts/intervention-needles`
emits both kinds. Neither needle classifies; both choose which turns to
read closely.

## Running it

```sh
scripts/intervention-needles                     # this project, both harnesses
scripts/intervention-needles --all-projects --days 14 --needle bad
```

Each `candidate` record carries the turn `text`, `prior_assistant` (the
assistant text it answered, tail-trimmed) with `prior_asked` (that text
ended in `?`), `next_reply`, up to five `next_actions`, and the
`transcript` path and `line` for drilling in. Rows are newest first;
`--limit` caps them and the summary reports what was dropped. The current
session is excluded unless `--all-sessions`. Leading whitespace, quotes,
emoji, and a bracketed dictation tag such as YA's `[ASR]` are skipped
before matching.

A full scan of about 11 GB of Claude and Codex logs took 64 s
(2026-10-03); a project-scoped scan is sub-second. Session discovery is
shared with [tool-surprises](tool-surprises.md) through `session_logs.py`.

## Judging candidates

Read each candidate against its context and sort it:

- **Agent error.** The agent's action did not follow from a reasonable
  reading of what the user wrote. Group errors by cause. A cause seen
  more than once gets the strongest available enforcer: a structural
  change, then a lint or tool whose error names the fix, then a test,
  and instruction text last. Record instruction changes through the
  [evidence ledger](evidence-ledger.md).
- **No-fault clarification.** The user misstated, retracted, or wrote
  something ambiguous, and the agent acted reasonably. This produces no
  agent rule. It can still point at an ambiguous glossary term, a
  dictation error, or a misconception worth a `user/MASTERY.md` entry.
- **Answer.** The turn answered a question the agent asked
  (`prior_asked` is a hint, not proof). Nothing to generalize unless the
  question itself should not have been needed.

Propose changes to the user rather than applying instruction edits from
mining alone.
