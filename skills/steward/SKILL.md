---
name: steward
disable-model-invocation: true
description: Fill idle GPU/resource capacity from a project's on-deck queue; one wired round by default, looping under a duration argument (/steward 8h, /steward forever), with any further argument text read as director guidance. Use when the user invokes /steward (with or without duration/guidance), asks to steward or tend on-deck jobs, asks to fill idle GPU with research/runs work, asks to run eligible on-deck entries, or uses /rep steward for repeated on-deck service.
---

# Steward

Steward the current project by launching eligible `on-deck/` entries until GPU
or other declared resources are full.

**Arguments**: `/steward [duration] [guidance...]`. A leading `Nm`/`Nh`/`Nd`
or `forever` token sets the loop window; everything else is read as director
guidance for the round(s) — reprioritizations, exclusions, or new work
("front-load X", which routes through the on-deck authoring flow as
ratified director input before the first pass). Carry guidance verbatim in
re-arm prompts so later wakes still honor it; convert a duration to an
absolute UTC deadline in the re-arm prompt (`/steward until <ISO> ...`).

Modes by duration:

- **once** — say `once` or `no watch`: one round, nothing armed afterward
  (attended use, no later wake wanted);
- **once+chained** — the default (no duration): one round that leaves its
  work wired (*Completion triggers* below), so chained follow-ons and one
  completion wake happen without polling;
- **duration / forever** — re-arms each wake until the deadline (or, for
  `forever`, until told to stop).

This is pull-based agent work, not a daemon.

## Load

1. Resolve the project root and read its instructions as usual.
2. Read `RUNS.md` and `RESEARCH.md` when present.
3. Read `topics/on-deck.md` in the project; if absent, read
   `~/agents/topics/on-deck.md`.
4. If `on-deck/` is absent, report that there is no on-deck queue and stop
   without creating files. `$on-deck` is the opt-in initializer.
5. If `~/agents/scripts/on_deck.py` exists and `on-deck/` is present,
   regenerate `on-deck/INDEX.md` before selecting entries:
   `python3 ~/agents/scripts/on_deck.py index --root <project-root>`.

## Steward Loop

Work without asking for confirmation when the GPU is idle or underfilled. Ask
only when a required guard cannot be mechanically checked, the launch would
exceed the entry's autonomy bound, or stopping an unrelated/user job is being
considered.

1. Inspect `agentctl list`, current `on-deck/*.md`, and GPU state
   (`nvidia-smi` when available).
2. Run `python3 ~/agents/scripts/on_deck.py eligible --steward --root
   <project-root>`: it evaluates each pending entry's `skip_if` and `guard`
   commands in priority order and names the first launchable entry. Drop
   `--steward` only when the director has granted launch on a gated entry.
   Confirm the named entry's cost is within steward autonomy before
   launching.
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
   or the next entry requires director judgment. In the final report, list
   any `blocked` or guard-failing entries that need director work — they are
   the queue's open questions, not noise.
## Completion Triggers (every round, including the default single round)

A round never ends with unwired work; polling is not the mechanism:

1. Wire mechanically-determined follow-ons with `agentctl --after` chains
   (success-conditional) at launch time — they need no agent wake at all.
2. If jobs are still running at round end, **wait in the foreground**: sit in a
   single bounded, blocking `agentctl wait`/`watch` (or
   `~/agents/scripts/steward-idle-watch <project-root>` run in the foreground),
   re-waiting per the *Blanket wait cap* in RUNS.md until it terminates. The
   foreground block returning *is* the re-invocation — the harness hands control
   back at the exact judgment point (newest job ended *and* VRAM/power drained to
   idle, covering allocator drain), and one bounded block stays a cache hit. Do
   **not** background this wait expecting a wake: a detached watchdog forfeits the
   turn continuation and can fall out of cache, degrading into polling.
   (`steward-idle-watch` exits immediately if nothing is running.) This keeps a
   bare `/steward` or `/rep steward` event-driven: the returning wake services
   results and selects next work as one follow-up round.

## Looping (`/steward <duration>` / `/steward forever`)

Each wake runs a round, re-enters the foreground wait, and re-arms one *long*
`ScheduleWakeup` fallback heartbeat (3600s) whose only purpose is safety —
agentctl malfunction, miswiring, or an unexpectedly missed event — not
cadence. Past the deadline, write the final report and stop. When the queue
is terminal (no eligible entries, no running jobs, remainder blocked on
director judgment), report and stop early — except `forever`, which keeps
idling at heartbeat cadence since new entries may arrive.

## Autonomy Bounds

- Director-authored entries may carry any priority 0-10. Launch one only when
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
  --guard "<bash precondition command>" --skip-if "<bash invalidation command>" \
  --what "<one sentence>" --why "<one sentence>" \
  --provenance <task/topic path> --on-success "<director review target>" \
  --check "<result-sanity checklist>" -- <agentctl start ...>
```

Then steward it like any other eligible entry.
