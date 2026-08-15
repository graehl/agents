# Research artifacts and publication

> Rules, templates, and rationale for research branches, programs, logs, paper
> proposals, papers, handouts, research blogs, result tables, and progress
> reports.

Read this packet before creating, reorganizing, or materially updating a
research branch's paper proposal, paper, handout, research blog, log, task
structure, program, result table, or progress report. `RESEARCH.md` is the
router and wins on conflict.

## Binding rules

### Task and branch structure

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

#### Paper proposals and program drafts

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

#### Research log conventions

Prepend entries. Each experiment records what/why, the verbatim command, and
the result. Mark a reconstructed command explicitly and never log a command
that was not run. When a paper uses a short run reference, place the same
reference beside the log summary and link its saved metadata. Update the log
whenever the paper's headline conclusion changes. The full entry template is
below under the second “Research log conventions” heading.

#### Research paper conventions

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

##### `topics/` vs `research/` placement, and canonical topic surfaces

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

##### Speculative drafts

A paper may be drafted before evidence to establish vision and experiment
targets, but it is unmistakably speculative: top-level status plus per-claim
markers for unsupported assertions. A concise placeholder names the
measurement and points to the canonical internal topic, where the full spec and
falsifier live; create that internal topic once this material exists if the
paper was previously the only canonical surface. Tactical work and debugging
stay in the topic/log. When evidence lands, replace the placeholder and mark
the claim confirmed, partial, or refuted, including cutting framing the
evidence killed.

##### First-contact public-facing sections

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
first-contact checklist are below under the second “First-contact public-facing
sections” heading.

#### Progress reports

For sizable programs, periodically write a dated
`research/progress-YYYY-MM-DD.md` for a non-delving manager or peer org. Follow
`topics/progress-report.md`: each installment restates enough for a new reader,
expands condition names, ends every thread with pursue/hold/park, and freezes
once disseminated; later reports carry corrections.

#### Handouts

Before creating or substantially revising a research handout, follow
`topics/handout-writing.md`. A handout is a mutable, two-speed discussion
snapshot, not another chronological research log: its opening gives an
uninvolved participant the work's flavor and one evidence-grounded insight,
while the whole artifact gives an interested reader the representative full
picture. Its claim-bearing comparisons remain subject to the same evidence,
result-table, and Pareto-figure rules as a paper. Its cooperative-review
presentation bar is lower: show decisive evidence and signal/link the complete
audit trail instead of reproducing every rigorous detail in the main path.

#### Research blogs

Before drafting or substantially revising a research blog post, follow
`topics/blog-post-writing.md`, `topics/research-writing.md`, and
`topics/research-blog-writing.md`. The post may select one cool thing that
worked rather than represent the program, but every claim it makes retains the
ordinary evidence, prior-art, attribution, and provenance standard.


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


## Retained detail and examples

### Task and branch structure

Each **main task** (a significant feature, experiment, or refactor) gets its own
git branch named after the task (e.g., `logit-vs-merge-lora` for task 002). A main
task also owns two companion documents in `research/`:

- `research/<branchname>.md` — the **research paper / design doc**: hypotheses,
  setup, results tables, key findings, open questions. Written to be readable by a
  future agent or human without the full conversation history.
- `research/<branchname>.log.md` — the **running log**: timestamped notes,
  intermediate results, dead ends, decisions. Less polished, more complete.

The main task file itself should explicitly track the branch's acceptance criteria,
implementation steps, and current state, not merely act as a subtask index.

### Research programs

A **research program** is a durable, named line of inquiry that contains more
than one paper, report, or supporting research artifact. It lives under
`research/<program>/`; standalone papers may remain directly under
`research/`.

Every research program has `research/<program>/GLOSSARY.md`. That glossary
defines the program's shared vocabulary and applies by path to every document
below the program directory, including papers, reports, advisor notes, logs,
and related-work artifacts. A nested document is presumed to use that glossary;
authors need not repeat the association in each file. Define a term in the
program glossary when multiple program artifacts use it, while paper-local
notation that does not recur stays in the paper.

A sibling `PROGRAM.md` declares the directory as a program root, provides its
descriptive charter, and may carry binding `Program instructions` for that
subtree. The directory path is the canonical locator; its basename remains the
research slug, and an optional first-line H1 may supply an alternative formal
name. It is the sole declaration for advisor scope, followed-document defaults,
and everything else keyed on programs. An old `Research program:` glossary
header may coexist but is inert. Declare deliberately, once the program's
evidence stream and narrative are independent enough that separate advising
beats shared context. A directory existing under `research/`, holding papers,
or holding only a glossary is not by itself a program:
`topics/glossary.md` permits subtree glossaries whenever local jargon recurs,
so an undeclared glossary under `research/` scopes vocabulary and nothing more.

#### Research log conventions

Log entries go at the **top** (newest first). For each experiment: brief preface
(what and why), the actual command in a fenced block, brief coda with the result.
Update the log whenever the paper's headline conclusion changes.

````markdown
### <run reference>: <short experiment name>

<What was tested and why.>

```bash
<verbatim command actually run>
```

<Result and decision consequence.>
````

If a command was not recorded at the time and must be reconstructed, note that
explicitly: `(reconstructed from adapter_config.json / task notes — not verified
as the verbatim original)`.

Do NOT log commands that were never actually run, or future plans disguised as
past runs. The log is a factual record.

When a paper table cites a numbered or short-named run reference (for example `R17`,
`pm-tau01`, or similar), the research log entry for that run should place the same ref
immediately next to a one-line summary and point at the saved `*.meta.md` artifact when
available. The log should make it easy to go from paper ref -> run summary -> metadata
without scanning prose blocks.

### Research paper conventions

When a handout/paper compares three or more systems on quality versus any
cost axis, read [`topics/pareto-figures.md`](../topics/pareto-figures.md) and
include the mandated Pareto scatter (SVG for the `.md`, PDF for LaTeX,
script + evidence committed together).

#### `topics/` vs `research/` placement, and canonical topic surfaces

`topics/` vs `research/` is fundamentally an **audience/plan axis, not a rigor
axis**: `research/` means the work is on a path toward external publication;
`topics/` means not yet (internal cross-cutting contract, buildable-mechanism,
or system documentation). The same discipline — honest controls, recorded
provenance, sanity checks — applies either way. A clean finding can graduate
from a `topics/` thread into a standalone `research/<paper>.md` when it earns a
publication path.

The topic system's machinery is glossary-scoped: named terms, canonical
`topic / refs` links, read-before-touching triggers, and collision-safe
`Topic:` names. Content named and linked by the owning program glossary is
therefore topic-like even when its canonical file lives under `research/`.

Rule: **every active thread has one canonical topic-like surface named in its
owning glossary**. Reuse an existing proposal, draft, handoff, or other
well-placed doc; do not manufacture a `topics/` stub solely for discoverability.
When no canonical doc exists, create a formal topic in the glossary-owned
collection. For a declared program this is normally
`research/<program>/topics/<name>.md`, whose commit-facing name is
`research/<program>/<name>`; standalone work normally uses the project-wide
topic collection. If a separate internal topic and external draft both exist,
link them **bidirectionally**.

A separate internal topic is the **holding area for material not (yet) suitable
for the draft paper** — exploratory findings, parked variants, mechanism
detail, negative results, and caveats that the external-facing narrative should
not carry yet. Its absence is acceptable only while there is no such internal
decision surface to hold. Create and link it when that need appears. Promote
into the paper when a piece earns its place; until then it stays discoverable
in the topic rather than lost in chat or a task file. Correspondingly, do not
migrate durable mechanism/contract content *out* of a topic into a publication
draft merely because the paper cites it.

#### Speculative drafts (vision-first, evidence-pending)

A `research/<paper>.md` draft **may be written ahead of its evidence**. Writing the
intended paper first — claims, framing, and result tables as scaffolds — is a
legitimate way to form an ambition, force coherent framing, and serve as a
vision-refresher; the implicit goal of such a draft is the set of measurements that
*would* turn its placeholders into evidence. This generalizes the "materialize the
plan as a skeleton/TBD scaffold" habit into a writing *mode*.

Discipline that keeps this honest rather than self-deceiving:

- **Default epistemic status is speculative.** Mark it unmissably: a status banner at
  the top of the draft (e.g. `Status: SPECULATIVE — claims unverified, evidence pending`)
  plus a per-claim marker on any assertion not yet backed by a result. Never let
  vision-first prose be mined later as an established finding. This is the *inverse* of
  the overselling prior in *Reproduce before comparing*: there the risk is overstating a
  real number; here it is mistaking an aspiration for a number at all.
- **Evidence placeholders double as experiment specs — but the spec lives in
  the internal topic.** A `TBD`/`TODO` table cell, figure slot, or result
  sentence should *name* what would be measured, on what data, and the outcome
  that would **confirm or falsify** the surrounding claim. Keep the paper's
  placeholder concise (a claim + speculative marker + pointer); the full spec,
  run queue, and falsifier live in the canonical internal topic doc. Create one
  in the owning glossary's collection when this need first appears. The topic,
  not the paper, is the generator of the experiment queue.
- **Keep tactical content out of the paper — it is not a diary.** The draft
  carries vision, framing, and (eventually) settled evidence; the tactical
  layer — detailed experiment specs, intermediate and negative results,
  debugging, run mechanics — belongs in the internal topic doc and the
  timestamped `research/<branch>.log.md` running log, not the paper. Push it
  there as it accrues so the draft stays a coherent narrative rather than a
  work journal.
- **Settle placeholders explicitly.** When a measurement lands, replace the placeholder and
  adjust the marker (confirmed / partial / refuted) — including downgrading or cutting
  framing the evidence killed. A speculative draft is a hypothesis to be disproved, not a
  press release to defend.

#### First-contact public-facing sections

For the first public-facing section of a research paper, report, or
presentation, model a reader who has none of the live conversation context.
Before accepting the opening framing, check:

- Does the opening state the main result or claim before mechanism detail?
- Can a reader understand the task without knowing internal run names?
- Are condition names literal enough to decode from the table alone?
- Are all abbreviations, glossary terms, and project-specific labels expanded
  or briefly glossed on first use?
- Does the first table avoid implementation/debug-only columns?
- Are table columns defined immediately below the caption when they are not
  ordinary field-wide terms?
- Are cost columns clearly stage vs. cumulative, or omitted until needed?
- Are estimates labeled as estimates?
- Are diagnostic, parser-audit, or instrumentation-only runs separated from
  scored experimental conditions?
- Does the text say what is measured, what is not measured, and what is
  pending?
- Would a reader know which comparison is the main claim?
- Would a skeptical reader know which controls or baselines are missing?

Diagnostic, parser-audit, or instrumentation-only runs do not belong in the
main result table unless they are scored under the same output contract as the
main conditions. Mention them separately as audit evidence.

For a paper-specific related-work catch-up, prefer a companion artifact folder
next to the paper: `research/<paper-name>/related-work/` for
`research/<paper-name>.md`. Put a small fetch/extract script there that
recreates the PDF/HTML/markdown extraction cache for cited papers. The generated
markdown/text output is a valuable `rg` search target for finding method,
threat-model, limitation, and table sections before reading them carefully.
Commit the script and lightweight notes when useful; normally ignore downloaded
PDFs, model caches, and generated extraction outputs unless the project
explicitly wants vendored sources.

Do not let extracted markdown become citation-orphaned text. The related-work
script should also create a lightweight metadata manifest for every paper key,
morally equivalent to a BibTeX entry plus source URL: stable key, title,
authors, venue or preprint server, year/date, DOI/arXiv/OpenReview/ACL/etc.
identifier when available, PDF URL, fetched/extracted timestamp, and extraction
tool/version. Prefer one repo-readable file such as `papers.bib`, `papers.yaml`,
or per-paper markdown front matter that can be regenerated alongside the
extracts. The paper can still hand-format citations, but the artifact folder
must preserve enough metadata for a future agent to reconstruct exact
bibliography entries without re-searching the web.

When the candidate related-work list grows beyond about eight papers, tier the
artifact folder and fetch/extract script. Fully extract the high-value tier:
papers with suspected proposal overlap, directly applicable methods, or likely
threat-model lessons. Leave peripheral/background papers on demand until a
comprehensive pass needs them. Make the tiering explicit in the paper or
companion notes, because `rg` over generated markdown/text only searches papers
that have actually been extracted; expand the extraction tier before claiming
coverage across the whole bibliography.

### Progress reports

Projects with sizable research scope should periodically emit a dated
`research/progress-YYYY-MM-DD.md` instalment — a plan-change and triage
report written for a manager or peer research org consuming the stream of
reports without delving into the repo. Spec and rationale:
`topics/progress-report.md` ("progress report" / "research progress
report"). Key contract: each instalment implicitly contains its
predecessors (brief restatement for a new reader, details by reference to
older reports/topics), states conditions in newcomer-legible expanded
form, ends every thread with an explicit pursue/hold/park triage verdict,
and is frozen once disseminated (corrections go in the next instalment).

### Result tables and document boundaries

Results tables in `research/<branchname>.md` **must** include:
- The **split** (dev / test / dev-subset) and **N** (number of examples) used for scoring.
  A table row without these is uninterpretable after time passes.
- Training and decode comparisons must also report **wall time**; decode rows must report
  **batch width** whenever more than one request/example was translated concurrently.
  Many methods are attempted speedups, so a result is incomplete unless a future reader can
  place it on the time/performance Pareto frontier.
- **One typed column per quantity; caveats go in footnotes, never in the cell.**
  A column is homogeneous down its length (all tokens, all seconds, all the same
  metric); a table is heterogeneous across columns. So a metric request means one
  column per quantity — "tokens and time" is **two** numeric columns, not one cell
  holding `1234 tok / 5.6s`. Manual decoration is always allowed regardless of a
  column's type — it annotates the number rather than replacing it: **bold** the
  best value, a `±ci` confidence interval on the number, or stat-sig markers in a
  comparison (use the project's declared significance symbols; absent an
  override, the binding default above is `*`/`**` for p<.05/.01), a `†` for a
  noted exception, or footnote refs. These form a small fixed set, so
  a query treating the table as a database strips them to recover the bare value;
  free prose has no such closed vocabulary and cannot be stripped, which is the
  operational reason it must move to a footnote rather than sit in the cell. (A
  per-cell unit recap like `5.6s` is itself such a strippable token, so it breaks
  nothing — but it's stylistically discouraged: carry the unit in the header and
  leave cells bare. The searching-agent-friendly rule that favors self-describing
  *log lines* doesn't transfer, since a cell's header sits right beside it; recap
  only earns its noise for a table whose cells are quoted out of context.) When a
  number needs words — an outlier, an OOM-truncated run, a
  not-comparable condition — write a Markdown footnote (`[^r17]`) inline, freely,
  the moment you notice it: as cheap and local as cramming the cell (drop the
  marker, append one line) but the column stays clean and no table rewrite is
  forced. Make no column-vs-footnote decision mid-build — footnote always works.
  Defer the only structural choice to one pass *after* the table, its captions, and
  all explanatory/analysis prose are written: revisit then and extract or promote
  footnotes where it improves readability and renderer compatibility (e.g. dense
  parallel notes lifted into a mostly-empty comment column). The two errors to
  avoid are both about the cell: prose fragments crammed into a numeric cell, and —
  over-correcting — deleting legitimate commentary to force a numbers-only table.
- Example header: `HF results, chi.dev head-20 (N=20, dev subset), MetricX-24 hybrid-large:`
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

**What belongs in the paper vs. log vs. task files**:
- Debugging steps, failed commands, environment troubleshooting, and routine
  "plumbing works" sanity checks belong exclusively in `tasks/` files and the
  research log until they produce a legitimate publication-facing insight.
- The paper is a record of findings, not process — strip debugging/testing narrative
  from claim-bearing sections. Exception: a correctness demonstration that is
  itself a finding (replicable, meaningful to an unfamiliar reader) may appear in
  the paper.
- **`tasks/` files are the private control plane for research investigations** —
  in-progress, parked, or planned work items live in `tasks/NNN-*.md`. They are
  not committed to the branch and are not public. Durable conclusions belong in
  the paper or an appropriate committed `topics/` doc once they are more than
  private direction-setting.
- Working research-paper drafts may temporarily include a brief plan note or
  related-task pointer when it improves navigation for active collaborators. Mark
  such text as draft/navigation scaffolding and keep it short; do not let it carry
  the actual investigation detail, which belongs in `tasks/` and the research log.
  The final/submission-prep phase must remove these task references so the paper
  stands alone. The precise pre-submittal cleanup gate can be defined later for
  each project.
- When a task governs a research paper, keep the task file as a summary and
  control plane: point to the paper, summarize the current framing or acceptance
  state, and note what session learnings should be synced into the paper when
  applicable. Do not duplicate whole paper sections into the task file; that
  creates two divergent sources of truth.
- **Published intake/split recipes must NOT reference private paths** such as `/private-mount`
  or other local-only mounts. Paper-facing recipes must point at public sources,
  checked-in scripts, or explicitly named non-public prerequisites instead.
- **Include a `## Future Work` section** for high-level directions meaningful to
  an unfamiliar reader. Routine follow-ups stay in `tasks/` only.


When editing a branch research paper (`research/<branchname>.md`), show the full diff
afterward, eliding only long unchanged stretches if needed to keep the displayed output
within roughly one 70-line screen. Focus the displayed diff on the modified output.
