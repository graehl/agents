# Progress report

> A progress report (research progress report) is a dated instalment in a
> project's `research/` stream that restates where the program stands for a
> reader who will not delve into the repo, emphasizes plan changes over run
> status, and ends every thread with an explicit triage verdict.

Topic: progress-report

## Reader model

Write for a manager or peer research organization consuming the *stream* of
reports. They may have access to the project git but are unlikely to delve
into it. Consequences:

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
