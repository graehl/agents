---
name: on-deck
description: Add guarded single-step research/run jobs to a project's on-deck queue. Use when the user invokes /on-deck, asks to on-deck or queue one or more runs, asks to turn a triage/progress-report next step into steward-runnable work, or asks to prepare a series of runs for later steward launch.
---

# On-Deck

Author `on-deck/<slug>.md` entries. Do not launch jobs unless the user also
asks to steward or run them.

## Load

1. Resolve the project root and read its instructions as usual.
2. Read `RUNS.md` and `RESEARCH.md` when present.
3. Read `topics/on-deck.md` in the project; if absent, read
   `~/agents/topics/on-deck.md`.
4. Inspect the governing task, research log, progress report triage, or topic
   next-steps that the user wants projected into on-deck entries.

## Entry Rules

- One entry is one launchable step, not a precompiled DAG.
- Every entry needs a mechanical `guard`, mechanical `skip_if`,
  runtime estimate, size class, `cheap_reversible`, launch command,
  provenance link, `on_success`, and prespecified `check`.
- Use `by: director` for user/director-authored work. Use `by: steward` only
  for speculative filler the steward invents.
- Director priority bands: 8-10 urgent, 4-7 normal. Steward-authored entries
  must stay 0-3 and `cheap_reversible: true`.
- Do not encode "think about whether X is good" as a guard/check. Convert it
  to a file/job/metric condition, or leave the entry blocked for director work.

## Add Entries

Use the helper when available:

```bash
python3 ~/agents/scripts/on_deck.py add <slug> --root <project-root> \
  --priority <0-10> --by director --runtime-estimate <time> \
  --size-class <small|medium|large> --cheap-reversible <true|false> \
  --guard "<mechanical precondition>" --skip-if "<mechanical invalidation>" \
  --what "<one sentence>" --why "<one sentence>" \
  --provenance <task/topic/research path> --on-success "<what this unlocks>" \
  --check "<result-sanity + comparison checklist>" -- <agentctl start ...>
```

For a series, create one entry per run. Use guards and skip-if clauses to
express dependencies, not `agentctl --after`, unless the follow-on is
mechanically determined without reading the predecessor result.

After adding entries, run:

```bash
python3 ~/agents/scripts/on_deck.py validate --root <project-root>
python3 ~/agents/scripts/on_deck.py index --root <project-root>
```

Report the entries added and any guard/check that is still too interpretive
for a steward.
