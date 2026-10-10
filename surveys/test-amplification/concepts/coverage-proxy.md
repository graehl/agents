# Coverage as a proxy for test-suite effectiveness

> Read-backed digest (cluster A, trust `contested`: this study finds that
> coverage tracks mutant-kill effectiveness only weakly once suite size is
> fixed, while earlier and concurrent studies it surveys, notably Gopinath
> et al. 2014, report coverage correlated with effectiveness).

**Paper.** Inozemtseva, Holmes, "Coverage Is Not Strongly Correlated with
Test Suite Effectiveness," ICSE 2014
([PDF](https://www.cs.ubc.ca/~rtholmes/papers/icse_2014_inozemtseva.pdf),
[local extract](../related-work/extract/inozemtseva2014-coverage-effectiveness/inozemtseva2014-coverage-effectiveness.md)).

## Method

The study uses five Java projects of 80k–724k SLOC: Apache POI, Closure
Compiler, HSQLDB, JFreeChart, and Joda Time, each with 628–7,947
developer-written test methods. For each project, 1,000 random suites were
drawn from the master suite at each size 3, 10, 30, 100, and so on, for
31,000 suites in total.

Coverage is measured as statement, decision, and modified-condition
coverage (CodeCover). Effectiveness is measured with PIT mutants in two
ways: raw kill score (killed / all non-equivalent mutants) and normalized
kill score (killed / non-equivalent mutants the suite covers). Mutants the
full suite does not kill are treated as equivalent, which is 0.4–35% per
project.

Association is Kendall \(\tau\), computed both ignoring size and within
each fixed size.

## Evidence

**Size.** Suite size alone correlates with effectiveness. For normalized
effectiveness, adjusted \(r^2\) is 0.26–0.97 (implied \(r\) 0.51–0.98);
for raw kill score, \(r^2\) is 0.69–0.99.

**Coverage, size ignored.** Raw-kill \(\tau\) is 0.79–0.95 across
projects. Normalized-kill \(\tau\) is 0.50–0.84, except HSQLDB at -0.35:
its higher-coverage suites kill fewer of the mutants they cover.

**Coverage, size fixed.** Controlling for size always lowered the
correlation:

- Normalized effectiveness: typically low.
- Raw effectiveness: typically moderate.
- Joda Time: drops from 0.80–0.85 to about zero; Closure (normalized
  effectiveness) does the same.
- Apache POI, raw effectiveness: drops from 0.94 to 0.46–0.85.

The two most comprehensive suites, Joda Time (91% statement coverage) and
Closure (76%), showed the weakest size-controlled relationship.

**Coverage type.** Statement, decision, and modified-condition coverage
are nearly interchangeable: Kendall \(\tau\) between them is 0.91–0.92,
and Pearson is 0.97–0.99. The stronger criteria add no predictive
information.

**Prior work surveyed.**
- Gligoric et al. 2013 found suite size alone predicts mutation score
  (\(\tau\) 0.585–0.958) on large manually tested programs.
- Gopinath et al. 2014 found coverage correlated with effectiveness across
  about 200 projects. Size did not add to their regression, possibly due
  to multicollinearity.

## Decision edge and limits

- **Do not allocate test-generation or test-selection compute to maximize
  coverage as a proxy for fault detection.** Once suite size is held
  fixed, extra coverage buys little predictable gain in mutant kills, and
  sometimes none.
- **Coverage remains useful as a negative signal.** Uncovered code cannot
  be tested; low coverage flags under-tested regions. High coverage does
  not certify a suite.
- **Do not pay for stronger coverage criteria as a quality target.** They
  rank suites the same way statement coverage does.
- **Mutation score is the authors' suggested substitute**, but it is
  expensive. The same field's predictive-mutation and real-fault-coupling
  papers decide whether that cost pays off.
- **Limits.**
  - Mutants stand in for real faults, and the equivalence assumption
    affects up to 35% of mutants.
  - Suites are random subsets of one master suite, not independently
    written or generated suites.
  - Generated suites rarely reached very high coverage, so a
    high-coverage threshold effect cannot be ruled out.
  - Five open-source Java projects; correlation only, no causal claim.
