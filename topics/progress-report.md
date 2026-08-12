# Progress report

> A progress report (research progress report) is a dated installment in a
> project's `research/` stream: a first-contact refresher followed by a
> self-contained `Previously` and an honest current disposition for every
> research thread promised by the prior report.

Topic: progress-report

## Reader model

Follow [`technical-writing`](technical-writing.md) for the common cold-reader,
terminology, evidence-separation, display, and whole-document revision
contract. Follow [`research-writing`](research-writing.md) for prior art that
changes a current interpretation, baseline, decision, or publication claim;
link the fuller survey or paper instead of copying its bibliography.

Write for a manager or peer research organization consuming the *stream* of
reports. Treat each installment as a possible first contact for an effectively
uninterested reader: they may have ignored the earlier updates until the
program demonstrated something worth attention. They may have access to the
project git but are unlikely to delve into it. Consequences:

- Conclusions must be legible from the report alone. Links to papers, topic
  docs, and run artifacts are optional depth for the rare delving reader,
  never required context.
- Project-internal shorthand (run names, split labels, recipe codenames) is
  expanded or glossed at first use. Metrics state their direction
  ("lower is better") at first mention. Conditions are stated in
  newcomer-legible expanded fashion, at conclusion grain — the full
  eval-condition precision standard (see `RESEARCH.md` § Reporting eval
  conditions precisely) applies to the underlying artifacts, which the
  report cites rather than reproduces.
- Polish is unimportant; legibility is paramount.

## Generate by reconciling the previous report

Read the immediately preceding progress report in full, then inspect what was
actually done since through the relevant working documents, research log, run
records, result tables, and decisions. Enumerate every thread the previous
report left active or planned and account for each one in the new report. Add
new threads only when work since the previous report made them
decision-relevant.

For the first report, use the program's starting state and original plan as the
prior frontier and state that no earlier installment exists.

This is a reconciliation, not transcription. The previous report supplies the
promised frontier; current evidence says what advanced, changed, stalled, or
disappeared. Do not silently drop an old active/planned item because another
thread became more interesting.

## Refresher before the delta

After the `follows <previous-report>` pointer, open every installment with a
clearly marked `## Refresher` or equivalent first-contact section. Restate why
the program matters now, its current conclusion or baseline, the minimum shared
vocabulary, and the decision context needed to understand this installment.
This section pays the same introductory burden as a standalone handout even
when a regular reader will skim it.

Use this compact opening shape by default:

```markdown
## Refresher

Context: <why this program and update matter now>
Goal: <current program objective and success criterion>
Prior baseline: <state or decision from which this installment departs>
Reader aids: <glossary and essential prior-report/paper links>
```

The body may then be more delta- and chronology-oriented than a handout:
organize by thread, changed result, or order of discovery when that makes the
program's movement easiest to follow. It is still a curated report, not a raw
log. Include chronology that changes evidence, interpretation, or plan; move
routine run status and debugging elsewhere.

When several threads share a real theme, group their sections under that theme
so coordinated or potentially unifying work is visible. The report remains an
account of what was done; prospective coordination belongs in concise,
explicitly planned or speculative lines rather than becoming a paper-style
backfill program.

Give each continuing thread or aspect this delta shape:

```markdown
## <thread>

Previously: <prior evidence, interpretation, and plan>
Now: <new evidence and what changed, with caveats>
<inline table or representative input/output example when illuminating>
Planned: <next action, cost/likelihood when material, and
          pursue | hold | park | wrapped verdict>
```

`Previously:` is self-contained: describe the whole thread, why it mattered,
the prior evidence/state, and what had been active or planned. Do not write only
“unchanged from the last report” or make the reader follow a link to understand
the thread.

For every prior active/planned thread, use one of these dispositions:

- continuing — `Now:` plus `Planned:` as above;
- deliberately parked — `Tabled because: <decision and reason>`; or
- deferred without a firm table decision — `Maybe next time: <credible revisit
  condition or timing, plus an honest likelihood/intention>`.

These are alternative successors to `Previously:`. Do not write `Now: nothing
done` followed by `Planned: nothing`; use `Tabled because:` or `Maybe next
time:` to communicate the actual disposition.

A newly opened thread may use `Previously: Not in the prior report; <why it
opened now>`. Routine chronology still belongs in the research log.

A final `## Detailed narrative and raw results` section is allowed for fuller
chronology, supporting tables, and additional examples. Keep the strongest
self-describing table or representative input/output example inline in the
thread when it efficiently explains `Now:`; do not make the reader search a
long final dump to discover the evidence behind the delta.

When several deltas coalesce into a candidate publication claim, consult
[`paper-writing`](paper-writing.md) for the form-led claim and evidence spine.
The report can preview that paper case while retaining its own dated-stream
contract.

## Scanability and typography

Assume the report is *scanned*, not read. Headings, tables, and bold
carry the story; prose is the supporting layer a scanner drills into
once or twice. Concretely:

- Every major results claim appears in a **results table**, not only
  in prose. Bold the runs/conditions that are **new since the previous
  instalment** — the bolded cells are the stream's visual record of
  exploration progress.
- Apply the self-decoding display contract from `technical-writing`; emphasize
  what is new without making the prior baseline visually disappear.
- A scanner reading only headings, tables, and bolded text must still
  come away with the correct conclusions and triage verdicts.

## Self-contained terms (export targets)

Reports get pasted into Confluence, emailed, and printed; repo-relative
links do not resolve there. Anything load-bearing lives in the document
itself:

- A named enumeration referenced by number ("rung 4", "stage 2",
  "tier 1") requires a defining table in an appendix of the same
  document, with in-document anchor links from the references. A
  `topics/` link may supplement the appendix, never substitute for it.
- Project coinages ("the single-knob law", recipe or metric nicknames)
  get a definition at first use: a clickable footnote or a brief
  parenthetical. The first-use gloss rule above is the floor; coinages
  recurring across sections deserve the footnote form so a scanner
  landing mid-document is not stranded.

## Stream contract (cumulative context)

Each report implicitly contains all prior reports in the project. That means:

- The marked refresher above provides enough orientation that an installment
  can be someone's first.
- But not full details: refer to older reports, topic docs, and papers for
  anything already established. Do not re-derive prior conclusions; restate
  them in a sentence and link.
- Open with `follows <previous-report>` so the stream order is explicit.
- Once disseminated, an instalment is frozen. Commit it verbatim; never
  revise it afterward. Corrections and retractions go in the next
  instalment.

File naming: `research/progress-YYYY-MM-DD.md` in the project repo.

## Content emphasis

- **Plan changes, not run status.** Every continuing thread ends with the
  `Planned:` decision, not a number dump. Live run state belongs in run metadata
  and logs, not here.
- **Explicit triage.** `Planned:` names the next concrete cell (experiment or
  deliverable), its cost, the probability it yields something worth keeping,
  and a pursue / hold / wrapped verdict. `Tabled because:` records a park;
  `Maybe next time:` makes a noncommittal deferral equally visible. A summary
  table at the end may recap all four triage states. Rationale: a large-scope
  program must
  deliberately neglect lesser curiosities unless they are cheap or close to
  a nicely tied-up (even if small) paper-ready finding; the report is where
  that neglect is made explicit and accountable rather than implicit drift.
- **Surface relationships.** Writing the report is itself the triage
  exercise: look across threads for shared shapes, combinations, and
  candidate unifying claims that no single thread shows alone. Name them.
- **Reframe negatives.** A "number didn't go up" result is often worth
  restating as a claimable finding ("what scale/setup is *required* for
  X?"). The report is the place to catch thinking that stopped too soon.
- **Caveats lead.** When a result is underpowered, circular, or a
  prompt-selection lead rather than a quality claim, say so before the
  numbers, not after — this stream is consumed by people who will quote it.

## Rationale

Three forces motivate the form. First, the consuming audience reads
conclusions, not repos: anything load-bearing that lives only in run
metadata or topic docs is invisible to them. Second, periodic forced
synthesis surfaces cross-thread relationships and stalls that day-to-day
run management hides. Third, explicit per-thread triage with costs and
likelihoods is the mechanism that keeps a large-scope exploratory program
from accumulating half-pursued curiosities.

Prototyped as `research/progress-2026-05-18/-06-01/-06-10.md` in the MT
conditioned-diversity branch; the 06-10 instalment is the first carrying
the full triage-table form.
