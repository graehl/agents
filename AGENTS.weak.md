# Weak-model supplement to AGENTS.md

Restates behavior that frontier agents perform by default. Read in
addition to `AGENTS.md` (everything there still applies); this file
only adds redundancy for behaviors smaller models are more likely to
miss. Not loaded by `AGENTS.md`; a provider-specific launcher surfaces
this file alongside `AGENTS.md` when a smaller model is in use.

## Direct instructions and readiness questions

When the user has given a clear, direct instruction, treat it as
authorization to proceed. Do not ask permission-style or readiness
questions ("are you ready?", "should I proceed?", "want me to start?",
"should I do X?") unless a genuinely new ambiguity, risk, or decision
point has arisen.

User statements such as "I'm comfortable with X" or "just do Y" are
standing authorizations; act on them, do not reconfirm.

## Do not narrate or restate tool output

Do not announce each tool call before making it ("I will now read the
file", "Next I will edit X"). Make the call.

Do not paste tool output back at the user verbatim — they can see it. A
one-line summary of what was found or what changed is enough; if nothing
surprising was found, say nothing.

## Verify before naming a symbol or path

Before stating that a file, function, flag, type, or command exists at a
specific name, confirm with `rg` or by reading the file. Do not
paraphrase or invent signatures from prior knowledge — they get believed
and break the next step.

## Issue independent tool calls in parallel

When two or more tool calls do not depend on each other's output (e.g.
reading file A and grepping for symbol B), issue them in the same
response rather than one at a time. Serial issuing of independent calls
is the most common cost waste for smaller models.

## Read a file before editing it; do not blind-retry tool errors

The Edit tool requires a prior Read of the same file in this
conversation. If an edit errors with "have not read this file", do not
retry the edit — Read first, then Edit. More generally: when a tool call
fails, read the error and adjust, rather than reissuing the same call.

## Conditional file loads

Load these files when the corresponding trigger first fires in the
session — not all at session start.

| Trigger | File(s) to load |
|---------|----------------|
| First tool use in a repo | root `AGENTS.md`, `AGENTS.local.md`, `CLAUDE.md`, any named README, `GLOSSARY.md` |
| Before diagnosing a bug | `topics/debugging.md` |
| Before designing or extending tests | `topics/testing.md` |
| Before building a prototype | `topics/prototyping.md` |
| Before research or experimentation work | `RESEARCH.md` |
| Before launching or monitoring long-running jobs | `RUNS.md` |
| Before surveying a field or gathering prior art | `survey-field.md`, `research-frontier.md` |
| Entering a topic area for the first time in session | that topic's `.md` and `.bearings.md` |
| User says `bearings`, `orient`, or `lost` | relevant topic `.md`/`.bearings.md`, plus recent dirty files, topic/task edits, git history, run records, and live job state |
| User invokes `/doubt` or says they doubt/distrust/want a re-check | `skills/doubt/SKILL.md` |

## Gate record: worked example

A gate record is reasoning under observation, not a fill-in form. State
only the checks that actually apply, as current facts, before running
the command.

**Scenario**: pushing a commit that fixes a typo in `docs/auth.md`.

> Pushing `docs/fix-auth-typo` to origin — gated because push is
> shared-state and hard to undo if wrong scope goes out.
>
> [scope] staged diff is one file, `docs/auth.md`, three lines;
> no unrelated changes present.
> [wip] working tree clean on all tracked paths.
> [branch] on `docs/fix-auth-typo`; target is not `main`.
>
> ```
> git push origin docs/fix-auth-typo
> ```

A check that cannot be confirmed is a blocker — stop and resolve it,
do not substitute a warning and proceed.
