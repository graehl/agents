# On-deck GPU fillers

> On-deck is a priority-ordered, guarded queue of single-step GPU jobs that a
> moderate-capability *steward* agent launches when the GPU is idle, re-deriving
> the next step each cycle rather than executing a precompiled workflow.

Topic: on-deck

RUNS/RESEARCH overlap: run-orchestration policy (RUNS) used to keep a research
program's GPU productive between higher-capability agent cycles (RESEARCH).

## Model

Not a fixed-in-advance DAG (no Condor/DAGMan-style precompiled workflow). A
moderate-understanding agent (the *steward*) is in the loop and single-steps
via `agentctl`: when GPU capacity is idle, it picks the next eligible on-deck
entry, launches one job, watches it, records the result, then returns to
watching. A higher-capability agent (the *director*) periodically refreshes
priorities and the per-entry guards as results land.

Division of labor:
- **Director owns ratified judgment**: priority, guards, skip-if conditions,
  cost class, launch command, and check for director-authored entries.
- **Steward owns mechanics**: evaluate guards, launch, watch, run the
  prespecified check, record facts, and flag the director for interpretation.
- **Steward may author filler entries**: only in the capped priority band
  0-3, only when cheap/reversible, and only with mechanical guards and checks.
  Director review is retroactive: ratify/reprioritize, edit, or retire.

## Why, vs. the alternatives

- vs. precompiled DAG: research priority reshuffles as results land; a fixed
  DAG over-commits. An in-loop agent re-derives the frontier each cycle. Also
  stays on the right side of "no resident scheduler" — this is a file
  convention plus pull-based agent behavior, not a daemon.
- vs. a fully-autonomous cheap agent: a limited agent next-stepping on stale
  priority burns GPU on pointless runs. Guards plus bounded autonomy contain
  that.
- Bonus: the on-deck directory plus per-entry status logs are durable "what is
  next" state — continuity and resumability if other measures fail. Live "what
  is running now" remains `agentctl` run metadata.

## Five requirements (these make or break it)

1. **Each entry carries an executable eligibility guard and an invalidation
   (skip-if) condition**: bash commands run from the project root whose exit
   status decides (guard exit 0 = preconditions met; skip-if exit 0 = the
   entry is already satisfied or moot). `on_deck.py eligible` evaluates them,
   so "mechanical" is machine-checked rather than exhorted — prose guards
   fail loudly as commands. Guard and skip-if answer different questions
   (can it run now / is it still worth running); do not restate one as the
   negation of the other. Soft dependencies must compile down to such
   commands.
2. **On-deck is the executable projection of the program's triage** (the
   progress-report triage table, topic next-steps, `--depends-on`), not a
   parallel plan store — entries link back to those rows, or it drifts.
3. **Steward autonomy is bounded to cheap/reversible entries** (runtime
   estimate + size class present); expensive or irreversible runs stay
   director-gated even when on-deck.
4. **The result step is a prespecified check** (result-sanity preview +
   expected baseline comparison) executed as a checklist; the steward records
   raw numbers and flags interpretation up, never concludes.
5. **Partition write authority**. The director owns fields on ratified entries;
   the steward appends status logs and may create capped, cheap filler entries.
   Steward proposals cannot preempt director-ranked work.

## Directory Layout

```
on-deck/
  <slug>.md       # one entry; director-owned frontmatter + steward status log
  INDEX.md        # derived priority-sorted table; regenerate, do not hand-edit
  done/<slug>.md  # retired entries, content preserved
```

`on-deck/INDEX.md` is derived by `scripts/on_deck.py`; if it looks stale, trust
the entry files and regenerate. Do not keep a separate live-running list in
`on-deck/`; that duplicates `agentctl`.

## Entry Schema

Each entry is Markdown with flat frontmatter and fixed sections:

````markdown
---
slug: "pilot-a"
priority: 5
by: "director"
status: "pending"
runtime_estimate: "45m"
size_class: "small"
cheap_reversible: true
guard: "test -f data/X && test -f runs/Y/returncode && test $(cat runs/Y/returncode) = 0"
skip_if: "test -f out/Z.md && grep -q 'metric:' out/Z.md"
provenance: "tasks/123.md; research/foo.log.md"
created_at: "2026-06-11T00:00:00Z"
---

# pilot-a

## What
One-sentence description.

## Why
Why this run belongs in the triage plan.

## Launch
```bash
agentctl start ... -- ...
```

## Check
Mechanical result-sanity preview and expected comparison.

## On Success
What this unlocks or what the director should inspect.

## Status Log
- 2026-06-11T00:00:00Z director: created pending entry
````

`by` is `director` or `steward`. `status` is one of `pending`,
`launched`, `done`, `skipped`, `blocked`, or `retired`. A `blocked` entry is
the durable home for a high-priority triage item whose launch cannot be
written yet (missing script, undecided design): it keeps the "what is next"
state visible to director and steward instead of evaporating into chat.

The launch command parameterizes committed, tested scripts. If the step
needs more than a few lines of new logic, land the script in the repo first
or file the entry as `blocked` — never inline a program in the entry. An
inline program is untested code frozen into a director-owned field: the
steward may not repair it when it surprises, while a script bug is fixable
by any agent without touching the entry.

The quality bar for an entry is *reasonably likely to succeed in a
straightforward way*, not fully specified: any new script has at least one
successful functional run at smoke scale before its entry goes `pending`,
and beyond that, do not chase completeness — environment surprises (a
dtype/attention/loader interaction) hit even proven scripts, and the
status-log → flag-director → repair-and-relaunch loop absorbs them more
cheaply than pre-specification ever could. agentctl `--after` chains are
success-conditional: a failed predecessor fails the waiting job with
`wait-after failed` *without running its payload*, so a chain fail-fasts
cleanly and the whole chain is relaunched after the fix.

Runs launched from on-deck inherit the entry's provenance: the authoring skill
adds a `--context-note` carrying `what/why`, declares known inputs/outputs, and
carries provenance and `on-success` into the run note / metadata so the run
record self-explains. The helper remains schema-level plumbing and does not
reject legacy or hand-written launches that lack this context.

Priority is numeric, highest first. Coarse bands are enough:

- 8-10: director urgent;
- 4-7: director normal;
- 0-3: steward band / speculative fill.

Ties break by slug for deterministic steward selection.

## Steward loop

If `on-deck/` is absent, stewardship is a no-op; do not create files. `$on-deck`
is the opt-in initializer that creates the queue directory.

One `/steward` invocation fills idle resources until GPU or other declared
resources are full, no eligible entry remains, or the next entry needs director
judgment. `/steward <duration>` (`8h`, `forever`) is the looped form: `--after`
chains carry mechanical follow-ons, a background
`scripts/steward-idle-watch` (agentctl `--notify-gpu-idle`) re-invokes the
steward when a resource is actually freed, and scheduled wakeups serve only
as the fallback heartbeat. `/rep steward` remains a working alias. There is
no resident scheduler.

GPU-idle heartbeat → regenerate/read `INDEX.md` → `on_deck.py eligible
[--steward]` runs each pending entry's skip-if and guard commands in priority
order and names the first launchable entry → `agentctl` wait-gpu/start/watch
→ on completion run `check`, record numbers, set status, flag director if
interpretation is needed → return to watch/idle.

Stewards do not wait for confirmation to fill idle GPU. If a higher-priority
eligible entry appears while a steward job is running, the steward uses
judgment: pause/kill only when the saved time is worth the lost work and the
stop is safe; otherwise finish the current cheap run and launch the higher
priority job next.

## Continuity

The on-deck directory slots into the resume-priority order (live worktree →
active root task → `.agentctl/active` → run metadata → **on-deck** → session
logs): a fresh agent reads it to recover what is next. Current running state is
still resolved from `agentctl`.

## Caveat

Value lives almost entirely in guard/skip-if quality. Wrong guards make this
an efficient way to burn the GPU on stale runs. The director's real per-cycle
job is maintaining guards as results land — the ordering is the easy part.
Executable guards keep the *form* honest but not the *content*: a guard that
checks the wrong file still passes.

## Adoption

Per-project opt-in via `$on-deck`; `on-deck/` is live working state (gitignored
unless a project tracks its plans). First used for research programs where idle
GPU time is valuable but full autonomy would burn compute on stale priorities.
