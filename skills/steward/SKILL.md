---
name: steward
description: Fill idle GPU/resource capacity from a project's on-deck queue. Use when the user invokes /steward, asks to steward or tend on-deck jobs, asks to fill idle GPU with research/runs work, asks to run eligible on-deck entries, or uses /rep steward for repeated on-deck service.
---

# Steward

Steward the current project by launching eligible `on-deck/` entries until GPU
or other declared resources are full, then stop. This is pull-based agent work,
not a daemon; `/rep steward` can repeat it.

## Load

1. Resolve the project root and read its instructions as usual.
2. Read `RUNS.md` and `RESEARCH.md` when present.
3. Read `topics/on-deck.md` in the project; if absent, read
   `~/agents/topics/on-deck.md`.
4. If `~/agents/scripts/on_deck.py` exists, regenerate `on-deck/INDEX.md`
   before selecting entries:
   `python3 ~/agents/scripts/on_deck.py index --root <project-root>`.

## Steward Loop

Work without asking for confirmation when the GPU is idle or underfilled. Ask
only when a required guard cannot be mechanically checked, the launch would
exceed the entry's autonomy bound, or stopping an unrelated/user job is being
considered.

1. Inspect `agentctl list`, current `on-deck/*.md`, and GPU state
   (`nvidia-smi` when available).
2. Select the highest-priority live entry whose guard passes, whose `skip_if`
   does not fire, and whose cost is within steward autonomy.
3. Launch with `agentctl` exactly as the entry says, preserving its
   `--context-note`, provenance, declared inputs/outputs, and runtime estimate.
   Prefer `agentctl start ... --watch-notify-gpu-idle` when the entry does not
   already choose watch behavior.
4. Append a status-log line to that entry: launched job/run id, skipped reason,
   blocked guard, done check, or director-needed note. Re-read the entry before
   each delayed status edit.
5. When a job completes, run the entry's `## Check` exactly as a checklist.
   Record raw numbers and sample paths; do not interpret the result as a
   research conclusion.
6. If RUNS parallelism says more independent work fits, continue selecting and
   launching entries. Stop when resources are full, no eligible entry remains,
   or the next entry requires director judgment.

## Autonomy Bounds

- Director-authored entries may use priority 4-10. Launch them only when
  `cheap_reversible: true` or the entry explicitly grants steward launch.
- Steward-authored entries must stay in priority 0-3 and
  `cheap_reversible: true`; they can run without retroactive director review.
- Never edit director-owned fields (`priority`, `guard`, `skip_if`, cost,
  launch, check) while stewarding. Append status/log facts only.
- If higher-priority eligible work appears while a steward job is running,
  use judgment: pause/stop the steward job only when the saved time is worth
  the lost work and the stop is safe. Otherwise let it finish and launch the
  higher-priority job next.

## Steward-Authored Fillers

When no director-ranked entry is eligible and resources are idle, you may
author a new filler entry if it is cheap, reversible, and mechanically guarded.
Create it with:

```bash
python3 ~/agents/scripts/on_deck.py add <slug> --root <project-root> \
  --priority 0 --by steward --runtime-estimate <time> \
  --size-class <small|medium> --cheap-reversible true \
  --guard "<mechanical precondition>" --skip-if "<mechanical invalidation>" \
  --what "<one sentence>" --why "<one sentence>" \
  --provenance <task/topic path> --on-success "<director review target>" \
  --check "<result-sanity checklist>" -- <agentctl start ...>
```

Then steward it like any other eligible entry.
