---
name: on-deck
disable-model-invocation: true
description: Add guarded single-step research/run jobs to a project's on-deck queue. Use when the user invokes /on-deck, asks to on-deck or queue one or more runs, asks to on-deck and go, asks to turn a triage/progress-report next step into steward-runnable work, or asks to prepare a series of runs for later steward launch.
---

# On-Deck

Author `on-deck/<slug>.md` entries, creating `on-deck/` when absent. Do not
launch jobs unless the user also asks to steward, run, or "and go" them.

## Load

1. Resolve the project root and read its instructions as usual.
2. Read `RUNS.md` and `RESEARCH.md` when present.
3. Read `topics/on-deck.md` in the project; if absent, read
   `~/agents/topics/on-deck.md`.
4. Inspect the governing task, research log, progress report triage, or topic
   next-steps that the user wants projected into on-deck entries.

## Survey First

Before authoring any entry, emit the candidate list as a short table — one
row per triage thread under consideration: proposed slug, priority,
runnable-now?, and (when not runnable) what is missing. Then author `pending`
entries for the runnable rows and `--status blocked` placeholder entries for
high-priority rows whose launch cannot be written yet. The table makes the
projection decisions reviewable before any entry is smoked in detail, and the
blocked entries keep the most important "what is next" items durable instead
of leaving them as a sentence in chat. Exclusions (threads deliberately not
queued) get one line each in the report.

## Entry Rules

- One entry is one launchable step, not a precompiled DAG.
- Every entry needs an executable `guard` and `skip_if` — bash commands run
  from the project root whose exit status decides (guard exit 0 =
  preconditions met; skip_if exit 0 = already satisfied or moot) — plus a
  runtime estimate, size class, `cheap_reversible`, launch command,
  provenance link, `on_success`, and prespecified `check`. Guard and skip_if
  answer different questions (can it run now / is it still worth running);
  do not restate one as the other's negation. Verify each command runs
  cleanly via `on_deck.py eligible <slug>` after adding.
- The launch parameterizes committed, tested scripts. If the step needs more
  than a few lines of new logic, write the script into the repo first (or
  file the entry `--status blocked`); never inline a program in the entry.
- Quality bar: reasonably likely to succeed straightforwardly, not fully
  specified. A new script needs one successful smoke-scale functional run
  before its entry is `pending`; beyond that, leave residual surprise to the
  steward's status-log/flag-director loop rather than longer specification.
- Use `by: director` for user/director-authored work. Use `by: steward` only
  for speculative filler the steward invents.
- Director-authored entries may use any priority (8-10 urgent, 4-7 normal,
  0-3 deprioritized filler). Steward-authored entries must stay 0-3 and
  `cheap_reversible: true`.
- Do not encode "think about whether X is good" as a guard/check. Convert it
  to a file/job/metric condition, or leave the entry blocked for director work.
- For `agentctl` launches, make the launch self-explaining: include a
  `--context-note` carrying the entry's what/why/provenance/on-success, and
  declare obvious known paths with `--input`, `--input-raw`, or `--output`.
  If the user supplies an `agentctl` launch without that context, rewrite the
  launch before adding the entry; the helper intentionally does not reject
  legacy or hand-written entries that lack it.

## Add Entries

Use the helper when available:

```bash
python3 ~/agents/scripts/on_deck.py add <slug> --root <project-root> \
  --priority <0-10> --by director --runtime-estimate <time> \
  --size-class <small|medium|large> --cheap-reversible <true|false> \
  --guard "<bash precondition command>" --skip-if "<bash invalidation command>" \
  --what "<one sentence>" --why "<one sentence>" \
  --provenance <task/topic/research path> --on-success "<what this unlocks>" \
  --check "<result-sanity + comparison checklist>" -- \
  agentctl start <job> --context-note "<what; why; provenance; on success>" \
    --input <key=path> --output <key=path> -- <command>
```

For a not-yet-runnable triage item, add `--status blocked`, put the missing
prerequisite in `--guard` (e.g. `test -f scripts/new_tool.py`), and sketch
the intended launch.

For a series, create one entry per run. Use guards and skip-if clauses to
express dependencies, not `agentctl --after`, unless the follow-on is
mechanically determined without reading the predecessor result.

After adding entries, run:

```bash
python3 ~/agents/scripts/on_deck.py validate --root <project-root>
python3 ~/agents/scripts/on_deck.py eligible --root <project-root>
```

(`add` regenerates the index; `eligible` exercises every pending guard and
skip_if as real commands, which catches prose or broken conditions now
rather than at steward time.) Report the survey table, the entries added,
and any guard/check that is still too interpretive for a steward.

## And Go

When the user asks to "on-deck and go" or otherwise asks to run immediately,
first create, validate, and index the entries above. Then run one steward pass
in the same session: read `~/agents/skills/steward/SKILL.md` and follow its
steward loop inline without asking for another confirmation. (Reading the
file rather than invoking the skill keeps working even though steward sets
`disable-model-invocation: true`.) Report both the entries
created and any launch/skipped/blocked status facts from that steward pass.
