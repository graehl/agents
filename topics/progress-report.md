# Progress report

> A progress report (research progress report) is a dated instalment in a
> project's `research/` stream that restates where the program stands for a
> reader who will not delve into the repo, emphasizes plan changes over run
> status, and ends every thread with an explicit triage verdict.

Topic: progress-report

## Reader model

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
- Link the program or project glossary near the opening when one exists. The
  link is a lookup aid, not a substitute for defining dominant jargon and
  abbreviations at first use.
- Polish is unimportant; legibility is paramount.

## Synthesis before dissemination

A progress report naturally begins as a chronological accumulation of runs and
working-session decisions. Before dissemination, perform a substantial
whole-document consolidate, review, and revise pass. Lead with why the program
deserves attention now, the current conclusions, and the plan changes they
cause. Reorganize the body around those conclusions; move supporting chronology
to references or a short retrospective only when it explains a decision.

Merely prepending a summary to a chronological log does not satisfy this pass.
The report should remain accurate if it is the first installment the reader
actually reads.

## Scanability and typography

Assume the report is *scanned*, not read. Headings, tables, and bold
carry the story; prose is the supporting layer a scanner drills into
once or twice. Concretely:

- Every major results claim appears in a **results table**, not only
  in prose. Bold the runs/conditions that are **new since the previous
  instalment** — the bolded cells are the stream's visual record of
  exploration progress.
- Captions and adjacent notes identify the population or split and N, metric
  direction, compared conditions, principal baseline, and the intended
  takeaway. A table must not require working-session context to decode.
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

- A brief restatement for a new reader is still wanted — enough orientation
  that an instalment can be someone's first.
- But not full details: refer to older reports, topic docs, and papers for
  anything already established. Do not re-derive prior conclusions; restate
  them in a sentence and link.
- Open with `follows <previous-report>` so the stream order is explicit.
- Once disseminated, an instalment is frozen. Commit it verbatim; never
  revise it afterward. Corrections and retractions go in the next
  instalment.

File naming: `research/progress-YYYY-MM-DD.md` in the project repo.

## Content emphasis

- **Plan changes, not run status.** Every section ends in a decision (a
  `Plan change:` line or equivalent), not a number dump. Live run state
  belongs in run metadata and logs, not here.
- **Explicit triage.** For each thread: the next concrete cell (experiment
  or deliverable), its cost, the probability it yields something worth
  keeping, and a verdict — pursue / hold / park / wrapped. A summary table
  at the end is the standard form. Rationale: a large-scope program must
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
