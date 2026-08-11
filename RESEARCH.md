# RESEARCH

Load this file before substantive research or experimentation: notebooks,
train/eval work, significance claims, paper/report drafting, field surveys, or
research-advisor decisions. After compaction or resume, an earlier read is not
proof that this policy survived; re-read this main file at the next research
action boundary unless the harness verifiably reconstructs this exact current
packet in model context or a boot-loaded scoped supplement explicitly sets an
evidence-backed cadence.

This file retains triggers and binding rules. `RESEARCH.supplemental.md` holds
optional templates, rationale, worked examples, and rare mechanics; read its
matching section when this compact rule is insufficient. This file wins on
conflict.

## Task and branch structure

Each main research task (significant feature, experiment, or refactor) uses a
task-named branch and owns:

- `research/<branch>.md` — future-reader-readable paper/design doc with
  hypotheses, setup, results, findings, and open questions;
- `research/<branch>.log.md` — newest-first factual running log with commands,
  intermediate results, dead ends, and decisions; and
- a main task file that tracks acceptance criteria, implementation, subtasks,
  and current state rather than merely indexing files.

Subtasks remain on the parent branch. Minor work stays inline; create a separate
subtask file only when the user asks or project convention requires it. Finish
or park the branch's subtasks, then merge the main task once rather than merging
each subtask separately.

## Research programs

A research program is a declared, durable line of inquiry containing multiple
papers or artifacts under `research/<program>/`. Its
`research/<program>/GLOSSARY.md` applies by path and declares:

```text
Research program: <slug>
```

The directory basename is the slug. A directory or glossary without that
declaration scopes vocabulary only; it does not create an advisor/program
boundary. Declare a program only when its evidence stream and narrative are
independent enough to benefit from separate advising.

### Research log conventions

Prepend entries. Each experiment records what/why, the verbatim command, and
the result. Mark a reconstructed command explicitly and never log a command
that was not run. When a paper uses a short run reference, place the same
reference beside the log summary and link its saved metadata. Update the log
whenever the paper's headline conclusion changes. The full entry template is
under “Research log conventions” in
[RESEARCH.supplemental.md](RESEARCH.supplemental.md).

### Research paper conventions

When a paper compares at least three systems on quality versus cost, read
`topics/pareto-figures.md` and commit its required scatter, script, and evidence
(SVG for Markdown, PDF for LaTeX).

#### `topics/` vs `research/` placement, and the stub-topic rule

Placement is an audience/plan distinction, not a rigor distinction:
`research/` is on a path toward external publication; `topics/` owns internal
cross-cutting contracts, mechanisms, and live project knowledge.

Every active publication thread keeps a companion `topics/<name>.md`, at least
a bidirectional stub pointing to `research/<paper>.md`. The topic basename
remains the `Topic:` trailer namespace and the discoverable home for mechanisms,
live status, exploratory/negative findings, parked variants, and detailed
experiment specifications. Promote publication-worthy material into the paper;
do not move durable system contracts out of the topic merely because a paper
cites them.

#### Speculative drafts

A paper may be drafted before evidence to establish vision and experiment
targets, but it is unmistakably speculative: top-level status plus per-claim
markers for unsupported assertions. A concise placeholder names the
measurement and points to the companion topic, where the full spec and
falsifier live. Tactical work and debugging stay in the topic/log. When
evidence lands, replace the placeholder and mark the claim confirmed, partial,
or refuted, including cutting framing the evidence killed.

#### First-contact public-facing sections

The opening writes for a reader with no live context. State the main
claim/result before mechanism detail; define abbreviations and project terms;
use literal condition names; distinguish stage from cumulative cost, estimates
from measurements, scored conditions from diagnostic runs, and measured from
pending work. The main table contains comparable scored conditions, not parser
or instrumentation audits. Name the principal comparison and missing
controls/baselines.

A paper-specific related-work cache lives beside the paper only when no shared
field survey covers it, or for a truly paper-specific overlap tier. Commit a
small recreating fetch/extract script and lightweight bibliographic metadata;
normally ignore downloaded PDFs and generated extracts. Every extracted item
retains a stable citation key, title/authors/date/venue, canonical identifier
and source URL, fetch time, and tool version. Make extraction coverage tiers
explicit before claiming bibliography-wide coverage. Detailed layouts and the
first-contact checklist are under “First-contact public-facing sections” in
[RESEARCH.supplemental.md](RESEARCH.supplemental.md).

### Progress reports

For sizable programs, periodically write a dated
`research/progress-YYYY-MM-DD.md` for a non-delving manager or peer org. Follow
`topics/progress-report.md`: each installment restates enough for a new reader,
expands condition names, ends every thread with pursue/hold/park, and freezes
once disseminated; later reports carry corrections.

### Field surveys and frontier mapping

For field survey, prior-art, or direction-ranking work, load in order:

1. `literature-search.md` — retrieval and citation snowballing;
2. `field-map.md` — field organization and maintenance; and
3. `frontier-map.md` — provisional claims, voids, and capstone questions.

Resolve repo-root files first, then `~/agents/`; report a missing trigger target
once and continue. Search shared `~/agents/surveys/<field>/` before extracting a
field afresh from any repo. A survey's `survey.md` is the map and
`concepts/<short>.md` holds read-backed per-concept understanding. A paper
references and extends the shared survey rather than duplicating its extraction
cache, except for paper-specific overlap material. The full survey schema is
`topics/research-survey.md`.

### Research-advisor handoff

Use one long-lived skeptical advisor per declared research program, with the
project-wide fallback for standalone/cross-program work. Invoke the applicable
advisor once for each new decision/evidence state that:

- commits to, reverses, parks, or revives a material direction, architecture,
  evaluation regime, or program specification;
- changes the causal story after a surprising, weak, or null result;
- promotes a provisional claim or uses it to justify a material next step;
- consolidates local results into a paper, progress report, or portfolio
  narrative; or
- operationally addresses the advisor (tell/ask advisor).

Load and follow `research-advisor.md` for scope resolution, packet
deduplication, followed-document state, semantic reconciliation, and the
challenge memo. Do not substitute “advisor review would help” for invocation.
Routine plumbing, frozen sweep cells, and unchanged claim/decision states do
not trigger it.

## Research method

### Reproduce before comparing

Treat published effectiveness as unverified until reproduced under the
comparison you will claim. Reproduce the strongest relevant existing variants
before saying a new method beats them. Report with/without each technique under
controls that block selection/evaluation leakage: frozen non-selection splits,
independent metric families where applicable, controlled seeds/config search,
tuned baselines, and per-compute cost.

A research result table always states scoring split and N. Training/decode
comparisons also include wall time; concurrent decode states batch width. Use
one typed column per quantity, carry units in headers, and put free-form caveats
in footnotes rather than numeric cells. Add explicit `TBD` cells for intended
unrun comparisons, remove stale conditions to the log, and correlate important
paper numbers to their run/log artifacts with stable hidden references.
Detailed formatting and decoration conventions remain under “Reproduce before
comparing (the overselling prior)” in
[RESEARCH.supplemental.md](RESEARCH.supplemental.md).

### Paper, log, and task boundaries

The paper records claims and findings, not debugging or routine plumbing.
Correctness evidence appears only when it is itself a reproducible,
publication-facing finding. The log carries factual experiment history.
Private `tasks/` files carry investigation control, planned/parked work, and
acceptance state; durable conclusions move to the paper or a topic.

A draft may contain brief marked navigation scaffolding, removed before
submission. Never publish local/private data paths as intake recipes. Include
`## Future Work` for directions meaningful to an unfamiliar reader; routine
follow-ups stay private.

### Research communication stance

When the user states an unrun hypothesis baldly, record it as a hypothesis
(“we expect X”); do not waste a reply restating that it needs testing. Push back
promptly when evidence makes it probably wrong.

Truth outranks momentum: null results, falsification, and “does not work” are
successful outcomes. Use positive affect only when evidence supports it.
Prefer ambitious probes that resolve live uncertainty or distinguish competing
hypotheses over redundant confirmation of well-established expectations.

### Evaluation scale and significance

Use head-20 to head-50 only for smoke/reject-bad checks, not conclusions. Tune
on dev, increasing N as needed. Default test evaluation is head-1000 after
selection; full test runs once for final paper confirmation and never chooses
methods. A project may override these dataset-specific defaults explicitly.

A superiority claim uses paired bootstrap over per-example scores, normally
10,000 two-tailed resamples, reports both means, difference, p-value, and win
rate, and uses at least N=200. Save per-example scores so later comparisons do
not rerun the model. Significance symbols are `*` p<.05, `**` p<.01 unless a
project declares otherwise.

After editing `research/<branch>.md`, show the modified diff, eliding only long
unchanged spans to stay readable.

### Result-sanity preview

Before presenting a newly wired experiment, evaluator, scorer, decode, parser,
or extraction result as meaningful—even a pilot—preview the output contract:

- counts, empty/malformed output, and producer/consumer formats;
- one aligned example per new condition: input, expected target when present,
  produced output, and the exact scorer/downstream payload; and
- condition order plus row/item mapping for concatenations, joins, prompt sets,
  extractions, and multi-policy output.

Quote the preview with a new result unless the path is unchanged. Until it
passes, numbers are provisional; fix the path and explicitly supersede
contaminated results. For no-reference outputs, use a kept-case property,
metric, or rubric plus metamorphic checks without leaking the oracle into the
generator (`topics/soft-checks.md`).

### Build the strongest cheap baseline early

Build and tune the strongest cheap/simple baseline before judging an elaborate
arm. A cheap method that wins is a result; a strong baseline also diagnoses
what the elaborate method must fix. Judge each arm independently rather than
giving a recurring cross-arm story extra triage weight.

### Attributing a surprising change across multiple differences

When several changes precede a surprising result, run one-at-a-time or
baseline-progression ablations when cheap. If controls are expensive, a
single-dominant-cause hypothesis is only a first-probe prior and requires
approximately separable, skewed effects. Distrust it under interaction,
saturation, comparable effects/many changes, sign cancellation, or
slice-dependent regimes.

Aim the first leave-one-out/add-one control at the suspected dominant cause,
then use the residual. A large or sign-flipped residual requires the remaining
factorial cells before attribution. Distinguish the main harmful component from
the net of helpful and harmful effects; an unrun interaction remains
uncertainty, not evidence. The formal additive model and worked diagnostics are
under “Attributing a surprising change across multiple differences” in
[RESEARCH.supplemental.md](RESEARCH.supplemental.md).

### Reporting eval conditions precisely

A run/eval/gate summary states, without branch shorthand:

- train corpus/split/N actually fit;
- epoch ceiling and checkpoint-selection/early-stop rule;
- selection corpus, exact split/N, and fixed versus derived status;
- decode/eval corpus, exact split/N, and overlap with selection;
- separate score/reference corpus when applicable; and
- overlap among train, selection, and eval.

Training-split smokes are labeled correctness checks, not generalization.
Reuse saved hypotheses/per-example scores for small comparable pilots when
possible. For MT, also verify source/reference/hypothesis counts and inspect
aligned plain-text outputs.

Dev is for selection; test is once after selection. A test result never chooses
a method. Divergent dev/test ranking is evidence about overfitting, not a “bad
slice.”

Before leaving a substantial weak or surprising experiment line, run reasonable
closure tests: configuration/bug checks, strongest cheap baseline, and
same-budget null controls where combination-only gains need them. Record the
closure evidence before parking the line. When logs suggest a tool anomaly,
search current `--help` and nearby option descriptions before declaring a tool
limit; name the relevant option and smallest discriminating follow-up.

## Workflow and continuity

### On-deck research runs

`on-deck/` is the executable projection of research triage into guarded
single-step runs, not the paper/log/task. Every entry points to its governing
artifact; steward records raw run facts while interpretation lands in the
paper, log, task, or topic. See `topics/on-deck.md`.

### Subtasks and commit checkpoints

Commit paper/log updates and source checkpoints when meaningful findings or
subtask states land. Private task and working-handoff files remain private
unless the user explicitly asks otherwise. Stage only known work; do not infer
ownership from timestamps or sweep unrelated files. Global shared-worktree and
commit rules govern any ambiguity.

Each main task file maintains a `## Subtasks` list covering file-backed and
inline work, with status, last worked, likely next, and user-confirmed
completion. The detailed table template and branch search command are under
“Main task file: subtask tracking section” in
[RESEARCH.supplemental.md](RESEARCH.supplemental.md).

### Research direction root (`research/ROOT.md`)

When present, `research/ROOT.md` records established user direction about
fruitful projects for autonomous research/tending. Read it before choosing such
work. Routine detail/progress may update it; reversing which projects are
fruitful requires explicit user consent.

### Research document paths and resume

Derive paper/log names from the Git branch. A branch paper requires a
corresponding main task file; report a missing one. “Update the research
paper/log” means the branch-derived file unless the governing task names
another.

On explicit `/hi` or resume of research work:

1. resolve the named handoff/task, or for bare `/hi` the default discovery hint,
   under “Resume source priority” in [AGENTS.global.md](AGENTS.global.md);
2. reconcile it with live state;
3. skim `research/ROOT.md` when present;
4. skim the branch paper/current framing;
5. read the governing task's Subtasks section and listed in-progress subtask
   files; and
6. read the newest research-log entries.

Do not run this checklist for a fresh specific request without a resume signal.
