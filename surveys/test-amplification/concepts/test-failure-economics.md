# What test runs cost and what they catch

> Read-backed digest (cluster A, trust `single-source` for each number. The
> order-of-magnitude claim that well under 1% of test executions reveal a
> change-caused failure is convergent across Google, Facebook, T-Bank, and
> 61 Travis CI projects measured independently).

**Papers.**
Labuschagne, Inozemtseva, Holmes, "Measuring the Cost of Regression Testing
in Practice: A Study of Java Projects Using Continuous Integration,"
ESEC/FSE 2017
([PDF](https://www.cs.ubc.ca/~rtholmes/papers/fse_2017_labuschange.pdf),
[local extract](../related-work/extract/labuschagne2017-cost-regression-testing/labuschagne2017-cost-regression-testing.md)).
Memon et al., "Taming Google-Scale Continuous Testing," ICSE-SEIP 2017
([PDF](https://huang.isis.vanderbilt.edu/cs8395-f23/paper/google-testing-icse-seip-17.pdf),
[local extract](../related-work/extract/memon2017-taming-google-scale/memon2017-taming-google-scale.md)).
Supporting rates from Machalica et al. 2019, Plyusnin et al. 2025, Jin &
Servant 2021, and Ayyad et al. 2026; see
[test-selection](test-selection.md) for links.

## Method

**Labuschagne et al.** 61 mature Java projects on Travis CI (106,738
builds over about two years). The 20% of projects with the most failures
and the 20% with the fewest were dropped. The study focuses on
Pass→Fail→Pass triples (1,381 found, 935 still re-executable). Each failed
build was rerun three times on Travis; a mixed result marks it flaky,
which is a lower bound. Non-flaky failures were classified by what the
fixing commit changed: source only (a real bug, counted as benefit), tests
only (maintenance, counted as cost), or both (split 70/30 by changed
lines). Individual test outcomes were parsed from logs for 40 projects.

**Memon et al.** One month of Google TAP post-submit data: 500K+ changes,
5,562,881 test targets, 4B+ outcomes. Each target's full history is
partitioned into never-failed, always-failed, mixed, and flaky. Targets
are Bazel test targets (suites, scripts, or single cases), not individual
test cases.

## Evidence

**Labuschagne: suite-level outcomes.**
- 18.4% of builds end in test failure. Another 14.5% error before tests
  run, so 33% of builds are not passing.
- Of the 935 re-executed single-build failures, 12.8% are flaky.
- Of the 815 deterministic failures, 58.7% were fixed by source changes
  only, 19.3% by test changes only, and 22.0% by both. After the line
  split, that is 74.1% benefit and 25.9% test maintenance.

**Labuschagne: per-test outcomes.**
- Inside failing builds, the average project fails 0.38% of its test
  executions. This is not the global failure rate, which is lower.
- 64% of failing builds have more than one failing test, usually from one
  root cause.

**Labuschagne: per-test lifetime value.**
- Each test was scored as bug-finding failures minus maintenance-only
  failures. In nine of 28 plotted projects, tests needed maintenance more
  often than they found bugs, on average.
- 85% of tests that ever fail do so only once, and 97% fail two times or
  fewer.
- 24 tests scored 5 or higher (repeat bug-finders); 609 scored -1.
- Over the period, test code grew from 10.8% to 21.9% of all code.

**Memon: how rarely tests fail.**
- 91.3% of targets passed at least once and never failed.
- Only 115,160 (2.07%) both passed and failed; 46,694 of those are flaky.
  That leaves 68,466 targets (1.23% of all targets) that ever caught a
  breakage or fix in the month.
- The abstract-level phrasing "1.23% of test executions" is inconsistent
  with Table II, which counts targets.
- Average outcome per change: 48.5% passed, 43.1% affected but not yet
  run, 7.5% skipped, 0.42% failed.

**Memon: cost.**
- A day of TAP is 800K builds and 150M test runs.
- Testing every change separately grew compute quadratically, so TAP
  batches changes into roughly 45-minute milestones, with observed
  feedback delays of up to 9 hours.
- Half of targets were affected fewer than 14 times in the month, while
  some were affected hundreds of times.

**Where failures concentrate.**
- Memon: within build distance 10 of the change; in frequently modified
  files (77% of files modified 42 times appear in breaking changes); and
  among specific authors and release tools (one tool broke on 39 of 42
  commits).
- Machalica: about 99.9% of build-dependency-selected targets pass, and
  flaky failures are about four times as common as real ones in exhaustive
  learning runs.
- Plyusnin: 0.8% of verdicts fail on its UI suite.
- Jin & Servant: 35% of failing Travis builds have no failing test (build
  or configuration failures), and test execution is about 40% of build
  time.
- Ayyad: 21% of SWE-bench instances flip outcome between two runs of
  different models, and per-instance token cost varies by up to 492x.

**Second-hand.** Labuschagne cites Herzig et al.'s Microsoft THEO selector
skipping 35–50% of tests while letting 0.2–13% of defects escape. This is
not read from the primary source.

## Decision edge and limits

- **Most test compute confirms passes.** A perfect oracle would skip more
  than 99% of executions (Labuschagne) or 99% of targets per change
  (Memon). That gap is the budget available for reallocation.
- **A test's yield is concentrated and short-lived.** Most failing tests
  fail once; a small set fail repeatedly and pay for themselves. Scheduling
  on per-test history (Memon, Machalica) exploits this.
- **About one in four deterministic failures is test debt, not a bug.**
  Count that maintenance as cost when valuing extra or generated tests. A
  generated test that fails on intended behavior changes has negative
  value.
- **Flakiness is first-order.** It is 13% of failures in Travis and about
  4x the real failures in Facebook's runs. Any compute spent rerunning or
  learning from raw failures buys mostly noise unless the outcomes are
  de-flaked.
- **Redundant co-failures (64% of failing builds) mean one representative
  per root cause would suffice.** A selector that knows tests fail
  together can drop more.
- **Limits.** Labuschagne counts fixes, not hours or dollars, and studies
  only Java on Travis after dropping the extreme projects. Memon reports
  post-submit target-level correlations from one month and states that the
  distance-10 cutoff may not transfer. No source here gives a per-test
  dollar lifetime cost or a calibrated probability that a given test ever
  catches a real regression. Memon's 1.23% per month and Labuschagne's
  failure-count scores are the nearest proxies.
