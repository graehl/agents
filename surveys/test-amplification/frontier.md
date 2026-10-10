# Frontier: test amplification

> Overlay on [survey.md](survey.md). **Mode:** grounded; **depth:** analysis
> only (void map and ranked capstone candidates; no proposal drafted).
> **Cutoff:** 2026-10-10. Candidate voids came from the four discovery
> clusters; each top candidate received a separate falsification search on
> 2026-10-10, recorded under `prior-art-checked`.

## Provisional claims

Fresh claims relevant to choosing where test compute goes. Revisit dates
are unscheduled reminders; no `at/` entry was created because no live
decision currently depends on them.

### Self-written agent tests do not move SWE-bench outcomes

- **Claim.** On SWE-bench Verified trajectories of six LLMs, resolved and
  unresolved tasks show similar test-writing frequency, agent tests are
  mostly print-based observation, and prompting four models to write more
  or fewer tests left 83.2% of outcomes unchanged with no significant
  McNemar test, while suppressing tests cut input tokens 33–49% (Chen et
  al. 2026, [agent-written tests](concepts/agent-written-tests.md)).
- **Regime.** Python repositories, issue-resolution tasks, scaffolds and
  models as of early 2026.
- **Confounds.** Benchmark tests are themselves weak (SWE-ABS strengthens
  50.2% of instances); "test-writing" is measured by trajectory content,
  not by test quality; no compute matching against extra samples.
- **Independent check.** None located. ExecCritic's separate-tester result
  is compatible (weak tests hurt, strong tests help) but measures a
  different arrangement.
- **Cheapest discriminating check.** Same agent, same budget: (i) no tests,
  (ii) self-written tests, (iii) tests from a separate stronger model,
  frozen; score on SWE-ABS-strengthened tests.
- **Revisit.** 2027-04 (unscheduled reminder).

### Change-awareness is the dominant multiplier for LLM test generation

- **Claim.** Meta's just-in-time catching tests, aimed at a pending diff
  and its intent, have a per-test weak-catch rate of 6.4% versus 0.8–2.0%
  for hardening workflows and 0.2% for coincidental failures (the abstract
  rounds this to 4× and 20×); the bottleneck moves to false-positive
  triage, and the paper's own counts of true positives are internally
  inconsistent (8 of 41 versus "7 issues from 41") (Becker et al. 2026).
  Liu et al. 2026 find that removing commit information cuts bugs found
  from 20 to 4.
- **Regime.** One company's Android/Kotlin and server code; FSE 2026
  industry track.
- **Independent check.** None outside Meta; Liu et al. is a separate group
  on open-source regression tasks.
- **Revisit.** 2027-04.

### Directed fuzzing adds nothing over undirected fuzzing plus corpus replay in CI

- **Claim.** LibAFLGo (2025) and Huang & Lemieux (2026) find no directed
  policy beating a modern undirected fuzzer, and short CI campaigns
  trigger bugs mainly by replaying the existing corpus.
- **Confounds.** LibAFLGo pre-filters bugs by LibAFL reachability; Huang &
  Lemieux use single-bug Magma versions.
- **Independent check.** Two groups agree in direction; PaZZer (2026)
  reaches more changed code but triggers no real bugs in CI budgets.
- **Revisit.** On the next directed-fuzzing paper that compares against
  LibAFL with build time charged.

## Void map

Axes: **unit of compute** (test runs, mutants, fuzz inputs, LLM generation)
× **decision** (where to spend, how much, when to stop, how to value the
result over time). A wrong axis would produce fake voids; these two are the
ones every cluster's methods are organized by.

| unit \ decision | where to spend | how much per change / target | when to stop | lifetime value |
|---|---|---|---|---|
| test runs | filled (predictive and safe selection) | filled heuristically (recall targets, THEO) | filled (recall calibration) | **untried** (per-test ledger) |
| mutants | filled (diff, coverage, arid, commit relevance) | partial (per-line caps; no derived optimum) | filled for score estimation (constant sample) | in-progress (Google exposure study) |
| fuzz inputs | contested (directed vs undirected) | filled within campaign; **partial** across programs | filled (residual risk, saturation) | filled (OSS-Fuzz longitudinal) |
| LLM generation | filled (uncovered lines, mutants, diff) | **untried** (compute-matched vs more samples) | untried | **untried** (generated-test maintenance) |
| across units | — | **untried** (one per-change budget over all four) | untried | untried |

## Voids and falsification

### V1. One per-change budget across selection, mutation, fuzzing and generation

- **Why unexplored.** Each community optimizes its own unit with its own
  oracle (test failures, mutant kills, crashes, accepted tests); no common
  currency of expected escaped-defect cost per CPU-hour or token.
- **Why it might matter.** All four units share the same targeting signal
  (the change) and the same diminishing-returns shape, so the marginal unit
  of compute for a given diff likely belongs to different methods for
  different changes.
- **prior-art-checked.** Web search "per-change testing budget allocation
  across test selection mutation testing fuzzing value of information
  continuous integration" (extended): only single-unit work (CIDFuzz,
  MOTIF per-mutant fuzzing budgets, a mutation-in-CI patent). Discovery
  cluster A searched Herzig citers and "value of information" framings;
  nearest are THEO (single unit), Probabilistic Greens (release gating),
  and Software World Models (arXiv 2610.04940, predicts breakage to decide
  whether another execution is worth it; not read). Status: untried as a
  joint allocator.

### V2. Compute-matched value of tester tokens versus more coder samples

- **Why unexplored.** Agent papers report budgets but do not equalize
  them; ExecCritic and CodeMonkeys vary tester and selection arrangements
  without holding total tokens fixed.
- **prior-art-checked.** Web search "compute-matched comparison test
  generation versus more patch samples SWE-bench tester agent budget
  2026" (extended): no matched study; Otter and the ICSE 2026
  "solved issues really solved" study (differentiating tests catch
  suspicious patches developer tests miss) are adjacent. Discovery
  cluster D: SWT-bench forward citations (300), newest CodeT citations; a
  2026 audit of evolution loops on small tasks did find equal-budget
  resampling beating mutation-based evolution (arXiv 2608.19626, not
  read). Status: untried on repository-level tasks.

### V3. Test access × resolution × gaming on solvable tasks

- **prior-art-checked.** Web search "coding agent hidden vs read-only vs
  editable tests reward hacking resolution rate experiment" (extended):
  ImpossibleBench already compares full, hidden and read-only test access
  — hiding tests drives cheating near zero but lowers performance on the
  original benchmark, and read-only access restores legitimate performance
  while blocking test edits but not special-casing
  ([test gaming](concepts/test-gaming-and-oracles.md)). HackTrace (arXiv
  2610.03055) detects shortcuts and reports read-only/editable splits.
  Status: **partially filled**; what remains is the same contrast on
  ordinary solvable tasks with strengthened hidden tests, reporting
  resolution and overfit rate together.

### V4. Budget allocation across many fuzz targets

- **prior-art-checked.** Discovery cluster C found nothing (Semantic
  Scholar "fuzzing budget allocation across harnesses": zero results;
  Böhme & Falk and residual-risk citers: within-target only). Falsification
  web search "fuzzing campaign scheduling across many fuzz targets budget
  allocation OSS-Fuzz ClusterFuzz multi-armed bandit harness selection"
  found **Nikolic & Jain 2024, "Fuzzing at Scale: The Untold Story of the
  Scheduler"** (arXiv 2406.18058, read in full): its best scheduler
  reallocates time by discounted coverage progress and beats round-robin
  on total coverage by 29% (5,467 Ubuntu binaries) and 10% (OSS-Fuzz
  targets), but simpler bandits lose to equal allocation per program,
  each configuration ran once, and no bug comparison was made; it asserts
  without citation that OSS-Fuzz allocates equally. Status: **partially
  filled** (coverage-progress scheduling, single runs). A replicated,
  bug-measured scheduler driven by residual-risk estimates, charging
  harness creation including LLM harness generation, remains untried.

### V5. A per-test lifetime ledger

- **Why unexplored.** Needs joined data that few organizations keep: per
  test runtime, flake investigations, maintenance edits, and regressions
  caught that would otherwise have shipped.
- **prior-art-checked.** Discovery cluster A: OpenAlex "test maintenance
  cost" (noise), arXiv `abs:"test suite" AND abs:"maintenance cost"`,
  forward citations of Herzig and Labuschagne. Nearest: Labuschagne's
  per-test bug-minus-maintenance score (counts, not cost), Leinen's
  project-level flaky cost, Memon's per-month target statistics, Bhatta's
  deletion reasons. Not checked: test/code co-evolution studies (Zaidman
  et al. 2010). Status: untried.

### V6. Maintenance cost of generated tests

- **Why it matters.** Industrial LLM test generation reports acceptance
  rates (73% at Meta) at the point of landing, while one in four
  deterministic test failures is already test maintenance (Labuschagne);
  generated tests could add maintenance faster than they catch bugs.
- **prior-art-checked.** Discovery cluster D (ACH forward citations, 70
  items 2025–26) and an MSR 2026 study of AI-authored test commits
  (coverage comparable to human tests; maintenance not measured, not
  read). Status: untried.

## Capstone ranking

1. **V2 — compute-matched tester tokens versus coder samples.**
   *Impact:* high; decides whether agent harnesses should spend on testing
   at all, and on which tester. *Tractability:* high; SWE-bench Verified
   plus SWE-ABS strengthened tests, existing scaffolds, a token budget
   sweep. *Novelty-confidence:* medium; fast-moving area, and the small-task
   audit shows the idea is in the air.
2. **V1 — one per-change budget across units.** *Impact:* high if the
   marginal method differs by change type. *Tractability:* medium; needs a
   shared cost currency and a corpus with real regressions (OSS-Fuzz
   regressions plus Defects4J-style histories). *Novelty-confidence:*
   medium-high after the search.
3. **V3 residual — access contrast on solvable tasks.** *Impact:* medium.
   *Tractability:* high. *Novelty-confidence:* low-medium; ImpossibleBench
   covers much of it.
4. **V6 — maintenance of generated tests.** *Impact:* high for adoption
   decisions. *Tractability:* low without industrial history data.
   *Novelty-confidence:* medium.
5. **V5 — per-test lifetime ledger.** *Impact:* medium-high. *Tractability:*
   low (data). *Novelty-confidence:* medium.
