# Research workflow and continuity

> Rules, templates, and rationale for on-deck work, subtasks, checkpoints, direction roots, paths, and resume.

Read this packet before queueing, resuming, checkpointing, or autonomously
selecting research work, or creating or updating a research handoff.
`RESEARCH.md` is the router and wins on conflict.

## Binding rules

Read Program-scoped handoffs and recovery plus Research document paths and
resume for research resume/handoff work; On-deck research runs for queueing;
Subtasks and commit checkpoints for milestones; and Research direction root
before autonomous work selection. Compaction alone uses the next action's
routes rather than repeating full resume orientation.

### Workflow and continuity

#### Program-scoped handoffs and recovery

Follow the general most-specific-program placement, visibility, contents, and
maintenance rules in [handoffs.md](../topics/handoffs.md). A research example is
`research/<program>/handoffs/<scope>.md`, beneath its owning `PROGRAM.md`.

When an older handoff lives outside its program, record its owning program
path explicitly and follow that program's chain on resume. Relocation must
preserve the old entry point and update known references; do not silently move
a peer's live handoff or its `ROOT` pointer.

On session resume or takeover of research work, including a supplied handoff:

1. Resolve the named scope under the global resume-source priority. Locate and
   fully read the governing `PROGRAM.md` chain through the owning program,
   including unlinked parents. Stop only at an explicit `Program root: self`
   boundary under [TOPICS.md](../TOPICS.md#self-rooted-programs), or the project
   root when none exists. A command run from root `scripts/` still serves the
   program owning its research
   inputs/outputs; its working directory does not bypass those requirements.
2. Read the process map's overall flow, applicable stage contracts and selected
   variations, plus the relevant inventories' status/identity conventions and
   entries for the active inputs, ancestry, and comparison/reserved sets.
   Follow their required detail-document routes. Read enough to reconstruct
   the active path; do not ingest unrelated programs or every historical row.
3. Reconcile the handoff with those records and live artifacts/run receipts.
   Establish the actual versions and roles in use, inherited model/data
   exposure, and the evidence required before the next stage. For additional
   data, establish what it must be additional to and locate the program's
   deduplication method and comparison inventory before annotation or split
   admission; a filename or hash-only check cannot stand in for a required
   partial-overlap check.
4. Give a compact account of the reconstructed path, the next action's
   load-bearing requirements, and satisfied/open gates with evidence links.
   Resolve missing, stale, or contradictory evidence before the dependent
   action; continue independent authorized work. A handoff's assertion that
   checks passed is insufficient when its receipt does not bind current inputs.

Demonstrate understanding by applying the records to the next action.
If required process records are missing, follow
[program guidance and process records](artifacts.md#program-guidance-and-process-records)
to reconstruct them from evidence within the authorized scope; mark unknowns
instead of inventing clearance. Keep the governing handoff current at meaningful
milestones, including changed input/prompt versions or reopened gates.

Compaction within active work does not trigger this full resume orientation.
At the next governed action, refresh applicable program instructions and stage
contracts under the global refresh rule, and check current input/gate evidence.
Broaden recovery only when scope, versions, or live state changed or the next
action's prerequisites cannot be reconstructed. A fresh specific request is
not a resume; ordinary project-entry and scoped action reads still apply.

#### On-deck research runs

`on-deck/` is the executable projection of research triage into guarded
single-step runs. Every entry points to its governing
artifact; steward records raw run facts while interpretation lands in the
paper, log, gap, or topic. See `topics/on-deck.md`.

#### Subtasks and commit checkpoints

Commit paper/log updates and source checkpoints when meaningful findings or
subtask states land. Private working-handoff files remain private
unless the user explicitly asks otherwise. Stage only known work; do not infer
ownership from timestamps or sweep unrelated files. Global shared-worktree and
commit rules govern any ambiguity.

Track unresolved work in the owning gaps and maintain the current handoff when
continuity needs it. Keep small substeps inline; no numbered-file or subtask
table convention is required.

#### Research direction root (`research/ROOT.md`)

When present, `research/ROOT.md` records established user direction about
fruitful projects for autonomous research/tending. Read it before choosing such
work. Routine detail/progress may update it; reversing which projects are
fruitful requires explicit user consent.

This is distinct from a program's `PROGRAM.md`: `ROOT.md` is current
cross-program triage for autonomous effort, while `PROGRAM.md` is the durable
aspiration and thematic boundary of one program.

#### Research document paths and resume

Use the program's canonical paper/log paths. Git-branch-derived names remain
a fallback when no owner has declared paths; a paper does not require a
separate tracking file merely to satisfy a directory convention.

On explicit `/hi` or resume of research work:

1. perform [program-scoped recovery](#program-scoped-handoffs-and-recovery)
   when a program governs the work; otherwise resolve the named handoff,
   or for bare `/hi` the default discovery hint, under the global resume-source
   priority and reconcile it with live state;
2. follow the program's canonical document paths when declared, using branch
   naming only as the fallback;
3. skim `research/ROOT.md` when present;
4. skim the branch paper/current framing;
5. read the relevant gaps and handoff's unfinished work; and
6. read the newest research-log entries.

Do not run this checklist for a fresh specific request without a resume signal.
