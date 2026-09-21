# Research artifacts and publication

> Rules, templates, and rationale for research branches, programs, logs, paper
> proposals, papers, handouts, research blogs, result tables, and progress
> reports.

Read this packet before creating, reorganizing, or materially updating a
research branch's paper proposal, paper, handout, research blog, log, task
structure, program, process map, artifact inventory, result table, or progress
report. `RESEARCH.md` is the router and wins on conflict.

## Binding rules

Read complete sections for the action below, including their subsections and
named routes. A paper edit does not activate program setup or every other
publication form.

| Action | Sections |
|---|---|
| Establish or reorganize a work unit | Task and branch structure; Paper, log, and task boundaries |
| Declare or reorganize a research program | Research programs; Program guidance and process records |
| Maintain data/model processes or inventories | Program guidance and process records |
| Choose or pitch a paper | Paper proposals and program drafts |
| Write a log entry | Research log conventions; Research log entry template |
| Write a paper | Research paper conventions, including placement, speculative drafts, and first-contact sections; Paper, log, and task boundaries |
| Write a progress report, handout, or research blog | Its named section; Paper, log, and task boundaries |
| Author a result table or claim-bearing figure in any form | Result tables and document boundaries; the figure routes under Research paper conventions |

### Task and branch structure

Follow the project's branch policy; research work alone does not require a
branch. A significant research work unit maintains, under its owning program
or the established standalone layout:

- a paper/design doc — future-reader-readable, with
  hypotheses, setup, results, findings, and open questions;
- a companion `.log.md` — newest-first factual running log with commands,
  intermediate results, dead ends, and decisions; and
- a governing gap for unresolved work and, when continuity needs it, a handoff.

Reuse existing documents. In a project using task branches, standalone defaults
are `research/<branch>.md` and `research/<branch>.log.md`; subtasks stay on the
parent branch and merge as one work unit. Minor work stays inline; split files
only when their size, audience, or project convention warrants it.

### Research programs

A research program is a declared, durable line of inquiry containing multiple
papers or artifacts under `research/<program>/`. Declare it with
`research/<program>/PROGRAM.md`, whose descriptive charter states the
program's durable aspirations, themes, and boundaries and whose optional
`Program instructions` section is binding in that subtree. The directory path
is the canonical locator; `<program>` remains its research slug, and an
optional first-line H1 may supply an alternative formal name. Its sibling
`GLOSSARY.md` applies by path. `PROGRAM.md` is the sole declaration used for
program/advisor discovery; an old
`Research program:` glossary header may coexist but is inert. A directory or
glossary without `PROGRAM.md` scopes vocabulary only; it does not create an
advisor/program boundary. Declare a program only when its evidence stream and
narrative are independent enough to benefit from separate advising.

### Program guidance and process records

When establishing or maintaining a research program, read
[TOPICS.md § Program scope charters](../TOPICS.md#program-scope-charters).
Create a missing descriptive charter only when the authorized work and
established project evidence support a coherent program. Add links to its
canonical process map, inventories, and handoff location as those become
necessary. Reuse existing owners; a pipeline stage or run variant does not
need its own program. Creating or revising binding `Program instructions`
still requires explicit user direction, including when promoting a discovered
convention into a requirement.

Keep `PROGRAM.md` concise. Group requirements by the activity they govern;
each routed section names when a detail document must be read and the immediate
requirement before proceeding. Put shared requirements at the nearest common
owning program and specializations in its children. A child inherits every
ancestor program whether or not it links them, up to an explicit self-rooted
boundary under TOPICS.md. Keep stage mechanics in detail documents and dated
decisions, failures, and current run state in their
existing owners, rather than accumulating them in the charter.

For a multi-stage program that reuses or revises data, annotations, prompts,
models, or evaluation views, maintain a process map and artifact inventories.
Extend the existing records; a small program may use sections of one document.
Keep these distinct:

- **Process map:** stage inputs/outputs, allowed variations and feedback,
  acceptance requirements, the detail/checker that owns each requirement, and
  whether enforcement is implemented or still manual. Include gates before
  costly annotation and split admission where applicable.
- **Inventories:** exact artifact identities and versions, producer and input
  ancestry, intended role, admission/quarantine/supersession state, and gate
  evidence. Track source-group and prior-use/exposure history where separation
  matters; the current train file alone cannot establish a model's history.
- **Current realization/handoff:** the chosen route, exact versions in use,
  satisfied and open gates, and next decision, linked to executed evidence.

Versions identify their own component: source membership, annotation prompt
and examples, label schema, alignment/projection, admitted dataset, recipe,
checkpoint, or scorer/reference view. Pin the actual bytes or immutable
revision used; a shared `vN` suffix or a mutable `latest` path does not bind
these components together. Preserve old inputs, raw outputs, and producing
records when deriving a replacement. An inventory may remain a current index
if its historical artifact identities remain recoverable.

A feedback step consumes a named earlier output as input to a **new** execution
and version; it does not rewrite the earlier execution. Record whether the new
input adds to, replaces, or reannotates existing material. Prompt revisions
retain their examples' source ancestry and affect only named new annotation
products. A change record names the affected descendants, checks that must
rerun, and justified reuse; a repaired dataset does not undo a checkpoint's
past exposure. Explicitly consuming development or evaluation data in a final
fit changes the evaluation eligibility of that model and its descendants:
scores on consumed data cannot support held-out generalization claims for
either. Record the exposed membership and last unexposed checkpoint under the
local policy; documenting this possibility does not authorize such a fit.

### Paper proposals and program drafts

Before choosing or pitching a paper form or focus, follow
`topics/paper-drafting.md`. A multi-paper program keeps the comparative index
at `research/<program>/paper-proposals.md`, may split developed candidates
under `research/<program>/paper-proposals/`, and promotes a selected candidate
to a lightweight `research/<program>/papers/<paper-slug>.md` skeleton. When it
needs a renderer, references, assets, or multiple outputs, relocate it under
`research/<program>/papers/<paper-slug>/index.<source-extension>` according to
`topics/document-writing.md` (`index.qmd` for the Quarto default); do not
maintain both as editable manuscripts.
Existing papers directly below a program root need no migration.

The intended v1 of a proposal portfolio or promoted draft is a working-document
change for the program advisor. Use `topics/paper-reviewer.md` when asking the
advisor to test the publication case.

### Research log conventions

Prepend entries. Each experiment records what/why, the verbatim command, and
the result. Mark a reconstructed command explicitly and never log a command
that was not run. When a paper uses a short run reference, place the same
reference beside the log summary and link its saved metadata. Update the log
whenever the paper's headline conclusion changes. Use “Research log entry
template” below when creating entries.

### Research paper conventions

Use `topics/paper-drafting.md` before selecting or materially changing a
paper's governing form or focus. After promotion, follow
`topics/technical-writing.md`, `topics/research-writing.md`, and
`topics/paper-writing.md` for the manuscript. Once the draft needs buildable
web or print output, follow `topics/document-writing.md` and its browser-
interactive and printable companions.

When a paper compares at least three systems on quality versus cost, read
`topics/pareto-figures.md` and commit its required scatter, script, and evidence
(SVG for Markdown, PDF for LaTeX).

Before selecting or generating a claim-bearing graph, diagram, or quantitative
display for a paper, handout, progress report, or research blog, follow
`topics/document-writing-figures.md`. It owns the Quarto-native vocabulary,
external plotting choices, matched web/print assets, build commands, and
freshness checks. Pareto figures inherit it and add their dominance-specific
contract.

#### `topics/` vs `research/` placement, and canonical topic surfaces

Placement is an audience/plan distinction, not a rigor distinction:
`research/` is on a path toward external publication; `topics/` owns internal
cross-cutting contracts, mechanisms, and live project knowledge.

Every active publication thread has one canonical topic-like surface named in
its owning glossary. An existing proposal, paper, handoff, or other program doc
may serve directly; do not create a stub merely to put it under `topics/`. If no
canonical doc exists, create a formal topic in the owning glossary's collection
— normally `research/<program>/topics/<name>.md` for a declared program, or the
project-wide topic collection for a standalone paper. A formal program topic's
commit name is `research/<program>/<name>`.

When the internal topic and publication draft are distinct, link them in both
directions. The internal topic remains the discoverable home for mechanisms,
live status, exploratory/negative findings, parked variants, and detailed
experiment specifications. Promote publication-worthy material into the paper;
do not move durable system contracts out of the topic merely because a paper
cites them. If such internal material first accumulates while the paper itself
is the only canonical doc, that is the point to create and link a separate
formal topic rather than requiring one preemptively.

#### Speculative drafts

A paper may be drafted before evidence to establish vision and experiment
targets, but it is unmistakably speculative: top-level status plus per-claim
markers for unsupported assertions. A concise placeholder names the
measurement and points to the canonical internal topic, where the full spec and
falsifier live; create that internal topic once this material exists if the
paper was previously the only canonical surface. Tactical work and debugging
stay in the topic/log. When evidence lands, replace the placeholder and mark
the claim confirmed, partial, or refuted, including cutting framing the
evidence killed.

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
explicit before claiming bibliography-wide coverage. For more than about eight
candidate papers, extract the high-value overlap/method/threat-model tier first
and leave peripheral sources on demand. Expand that tier before claiming full
bibliography coverage. Define nonstandard table columns by the caption.

### Progress reports

For sizable programs, periodically write a dated
`research/progress-YYYY-MM-DD.md` for a non-delving manager or peer org. Follow
`topics/progress-report.md`: each installment restates enough for a new reader,
expands condition names, ends every thread with pursue/hold/park, and freezes
once disseminated; later reports carry corrections.

### Handouts

Before creating or substantially revising a research handout, follow
`topics/handout-writing.md`. A handout is a mutable, two-speed discussion
snapshot, not another chronological research log: its opening gives an
uninvolved participant the work's flavor and one evidence-grounded insight,
while the whole artifact gives an interested reader the representative full
picture. Its claim-bearing comparisons remain subject to the same evidence,
result-table, and Pareto-figure rules as a paper. Its cooperative-review
presentation bar is lower: show decisive evidence and signal/link the complete
audit trail instead of reproducing every rigorous detail in the main path.

### Research blogs

Before drafting or substantially revising a research blog post, follow
`topics/blog-post-writing.md`, `topics/research-writing.md`, and
`topics/research-blog-writing.md`. The post may select one cool thing that
worked rather than represent the program, but every claim it makes retains the
ordinary evidence, prior-art, attribution, and provenance standard.


### Paper, log, and task boundaries

The paper records claims and findings, not debugging or routine plumbing.
Correctness evidence appears only when it is itself a reproducible,
publication-facing finding. The log carries factual experiment history.
Gaps track unresolved investigation work; private program-scoped handoffs carry
continuity and acceptance state. Durable conclusions move to the paper or a topic.
A governing handoff summarizes framing, acceptance, and needed synchronization;
it links the manuscript rather than duplicating its sections.

A draft may contain brief marked navigation scaffolding, removed before
submission. Never publish local/private data paths as intake recipes. Include
`## Future Work` for directions meaningful to an unfamiliar reader; routine
follow-ups stay private.


### Research log entry template

````markdown
### <run reference>: <short experiment name>

<What was tested and why.>

```bash
<verbatim command actually run>
```

<Result and decision consequence.>
````

### Result tables and document boundaries

Research result tables must include:
- The **split** (dev / test / dev-subset) and **N** (number of examples) used for scoring.
  A table row without these is uninterpretable after time passes.
- Training and decode comparisons must also report **wall time**; decode rows must report
  **batch width** whenever more than one request/example was translated concurrently.
  Many methods are attempted speedups, so a result is incomplete unless a future reader can
  place it on the time/performance Pareto frontier.
- **One typed column per quantity; caveats go in footnotes, never in the cell.**
  Carry units in headers. Bold, confidence intervals, declared significance
  markers, exception marks, and footnote references may annotate numbers.
  Significance defaults live in `_RESEARCH/evidence.md` § Evaluation scale and
  significance. Write explanatory footnotes as caveats arise; after the table,
  caption, and analysis are complete, reorganize notes when readability or the
  renderer benefits. Keep legitimate commentary rather than deleting it to
  force numeric cells.
- For multi-corpus/multi-model comparisons, widen the table; repeated model-identifying
  rows or separator rows are fine as long as direct comparison stays legible.
- When a new model or corpus is added to an existing comparison table, add explicit `TBD`
  placeholders where the not-yet-run numbers belong so the intended comparison surface is
  visible before all runs are complete.
- Stale methods/conditions no longer part of the decision story should be removed from the
  paper and archived to the research log with a note.
- Important paper numbers should carry a human-invisible correlation marker such as an HTML
  comment (`<!-- ref: R17 -->`) so a future reader can align the paper table entry with the
  corresponding research-log run record and saved artifacts.

When editing a branch research paper (`research/<branchname>.md`), show the full diff
afterward, eliding only long unchanged stretches if needed to keep the displayed output
within roughly one 70-line screen. Focus the displayed diff on the modified output.
