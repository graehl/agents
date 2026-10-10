# Change-aware and predictive regression test selection

> Read-backed digest (cluster A, trust `reproduced` for the core claim that a
> learned per-change selector keeps about 95% of real test failures while
> running a small fraction of the dependency-selected tests: Facebook and
> T-Bank report it independently with different models; every other result
> here, including the GPU-CI subsection on FastCI, is `single-source`).

**Papers.**
Machalica, Samylkin, Porth, Chandra, "Predictive Test Selection," ICSE-SEIP
2019 ([arXiv](https://arxiv.org/abs/1810.05286),
[PDF](https://arxiv.org/pdf/1810.05286),
[local extract](../related-work/extract/machalica2019-predictive-test-selection/html/1810.05286.md)).
Plyusnin et al., "Targeted Test Selection Approach in Continuous
Integration," ICSME 2025 ([arXiv](https://arxiv.org/abs/2509.10279),
[PDF](https://arxiv.org/pdf/2509.10279),
[local extract](../related-work/extract/plyusnin2025-targeted-test-selection/html/2509.10279.md)).
Memon et al., "Taming Google-Scale Continuous Testing," ICSE-SEIP 2017
([PDF](https://huang.isis.vanderbilt.edu/cs8395-f23/paper/google-testing-icse-seip-17.pdf),
[local extract](../related-work/extract/memon2017-taming-google-scale/memon2017-taming-google-scale.md)).
Wang, Pradel, Liu, "Names Are All You Need: Effective and Safe Regression
Test Selection for Python," arXiv 2026
([arXiv](https://arxiv.org/abs/2605.25356),
[PDF](https://arxiv.org/pdf/2605.25356),
[local extract](../related-work/extract/wang2026-namerts/html/2605.25356.md)).
Jin, Servant, "What Helped, and What Did Not? An Evaluation of the
Strategies to Improve Continuous Integration," ICSE 2021
([arXiv](https://arxiv.org/abs/2102.06666),
[PDF](https://arxiv.org/pdf/2102.06666),
[local extract](../related-work/extract/jin2021-ci-strategies/html/2102.06666.md)).
Ayyad, Wang, Shin, Zou, Adams, "Trajectory-Aware Benchmark Subset Selection
for Cost-Efficient Software Engineering Agent Regression Testing," arXiv 2026
([arXiv](https://arxiv.org/abs/2609.24928),
[PDF](https://arxiv.org/pdf/2609.24928),
[local extract](../related-work/extract/ayyad2026-trajectory-subset-selection/html/2609.24928.md)).
Qiao, Zheng, Liu, Wang, Gu, Liu, Jin, "FastCI: Efficient GPU-Intensive CI
for LLM Training Frameworks," arXiv 2026
([arXiv](https://arxiv.org/abs/2610.01967),
[PDF](https://arxiv.org/pdf/2610.01967),
[local extract](../related-work/extract/qiao2026-fastci/qiao2026-fastci.md)).
Pan, Bagherzadeh, Ghaleb, Briand, "Test Case Selection and Prioritization
Using Machine Learning: A Systematic Literature Review," Empirical Software
Engineering 2021 ([arXiv](https://arxiv.org/abs/2106.13891),
[PDF](https://arxiv.org/pdf/2106.13891),
[local extract](../related-work/extract/pan2021-ml-test-selection-slr/html/2106.13891.md)).

## Method

**Facebook predictive selection.** A gradient-boosted classifier scores
each (change, test target) pair among the targets that transitively depend
on the change in the build graph. Retained features: file extensions,
recent change counts, per-target historical failure rates, project name,
number of tests, and minimal build-graph distance. Labels come from
"learning runs" that execute every dependent target on about a quarter of
changes in off-peak capacity; failing targets are retried up to ten times
and only all-attempts-failed outcomes count as real. Weekly retraining is
gated on a held-out week.

**T-Bank T-TS.** Same model family on mobile UI tests, but commits are a
bag of changed files, and test-to-file proximity is directory distance to
the three nearest changed files, with no coverage map or build graph.
Training data are nightly batch runs; inference is per commit. Flaky and
broken tests are filtered by an internal stability service.

**Google TAP study.** No deployed selector: a month of post-submit data
(500K+ changes, 5.5M targets, 4B+ outcomes) mined for signals of pass/fail
transitions, plus a replayed build-graph distance cutoff.

**NameRTS.** Safe static selection for Python: a test file is selected if
any modified code element is reachable from its names through a
name-to-definition graph, with two prunings against cascades; ground truth
from instrumenting modified functions.

**Jin & Servant.** Replays 14 variants of 10 CI-saving techniques
(including the Facebook selector) on 82,427 builds of 100 TravisTorrent
projects with chronological 11-fold validation.

**Ayyad et al.** "Tests" are SWE-agent benchmark instances (full LLM agent
runs), stratified by historical pass count and picked nearest each
stratum's trajectory-embedding centroid; the estimand is the
full-benchmark resolve rate on later runs.

**Pan et al.** Review of 29 ML-based selection/prioritization studies.

## Evidence

**Facebook.** Calibrated at land time to test recall above 0.95 and
faulty-change recall above 0.999, both measured against de-flaked failures
among build-dependency-selected targets; selection rate below 0.33 of that
set. Deployed, it cut test executions by a factor of three and machine
cost by a factor of two versus dependency-based selection. The top two
scored targets alone catch a failure on 70% of faulty changes. Without
de-flaking, a model that appears to have 0.9 recall at 15% selection has
about 0.7 real recall.

**T-Bank.** Offline on its own data, 15% of tests catch 97% of failures,
and the top 0.8% catch 60%. In a month of production, the 15% setting
gives recall 0.95 at 34.0 versus 202 test-minutes for the full suite
(5.9x); the deployed 0.8% (50 tests per commit) setting gives recall 0.26
in 4.7 minutes, versus 0.21 for the coverage-map tool, which runs 43% of
tests. Name/path similarity features hurt; ablations dropping file or
cross-file features cost about 0.013 NAPFD. Nightly full runs are kept.

**Google.** Per change, 99:1 passed vs. failed targets. Edge targets with
an unambiguous culprit lie within build-graph distance 10; replaying only
targets within distance 10 or 6 would have used 42% or 55% fewer
resources in the month studied with no missed breakage or fix. Change
frequency, file type (.hpp 80%, .cc 60%, .java 40% in edge changes),
author or tool identity, and three or more recent authors on a file
predict breakage. The authors call these preliminary correlations.

**NameRTS.** On 500 commits across 10 projects (12k–426k LoC), it skips
69.90% of test files (ground-truth ceiling 80.69%) and saves 45.59% of
end-to-end time including its own 10.04% overhead. It is safe on 99.6%
of commits (two misses: test-state interference, a library callback).
BabelRTS skips 28.36% but is safe on 76.6%; a safe file-level baseline
skips 7.42%, because one Python test file imports 83% of source files on
average. Pays off after about five commits.

**Jin & Servant.** Across techniques, ranking by build time saved is
almost exactly the reverse of ranking by failures missed. Test-level
selectors skip most tests (84% for the Herzig cost model, 80% for the
within-project Facebook re-implementation) but save much less build time
because test execution is only about 40% of build time; skipping whole
builds saves more. "Safe-looking" rules (skip no-code changes, skip tests
not reaching the change) still miss many failing builds, because 35% of
failing builds fail outside tests. Cross-project training misses fewer
failures but saves less. Topic-diversity test prioritization was near the
perfect ordering for early feedback.

**Ayyad et al.** At a 10% subset, median resolve-rate error stays below 5
points and worst-case error under about 10 points. Versus the best
baseline (pass-count stratified random), mean RMSE falls by up to 11.4%
and worst-case error by 4–11% (typical draw) or 38–46% (95th-percentile
draw), at 5% and 10% subsets only. Token cost is simply proportional to
subset size, so a 10% subset saves about 90% (3.44B to about 345M
tokens). Stratifying by past outcome alone cuts median RMSE 31–51% versus
uniform random sampling; dropping the stratification costs 30–37% RMSE.

**Pan et al.** Most benchmark subjects have very low failure rates;
metrics are computed inconsistently. Execution-history features associate
with higher NAPFD, but are confounded with smaller test suites. Few
studies are reproducible (the text gives both 6 of 29 and 5 of 12).

### When each test is expensive GPU work: FastCI

**Regime.** ByteDance's LLM training framework: more than 200 merge
requests per week, a CI pool of thousands of GPUs that stays saturated,
and CI runs averaging over four hours. Most tests are end-to-end training
or evaluation jobs. The deployed baseline is a hand-maintained file-to-test
path map. Pipelines are not fail-stop, so the selected set always runs to
completion.

**Mechanisms.** Four stages, each applied to the output of the one before:

- **Change-impact selection from runtime evidence.** py-spy samples each
  CI test at 50 Hz to build a graph of the functions and calls observed
  per test. A change selects every test observed executing a modified
  function. Sampling misses short-lived functions, so when a modified
  function has no evidence, the search expands to the rest of its class
  and to its callers.
- **Context-aware pruning.** Two tests are treated as redundant for a
  modified function only if its 3-hop caller/callee subgraph is identical
  in both and their task and hardware metadata match. Only the cheapest
  test in each group (by historical GPU-hours) is kept.
- **Risk ordering.** The paper uses historical outcomes only to order
  tests, never to skip them, because predictions give no skipping
  guarantee. Each test's score blends its past failure rate when the same
  file changed with its recent instability, weighted by how many past
  observations back the first signal.
- **Workload shrinking.** Settings outside a test's purpose, such as
  model size or logging, are reduced as configuration overrides. The test
  is periodically rerun at full size, and the reduction is dropped if the
  pass/fail results ever disagree.

**Evidence (single-source).**
- **End to end vs. the path map.** Production merge requests were replayed
  in a separate shadow CI for two days. As fractions of full CI:
  - Path map: 50.6% of tests, 51.5% of GPU use, 26.9% of latency.
  - FastCI: 18.6% of GPU use, 6.1% of latency.
  - That is 63.9% less GPU and 77.5% less latency than the path map.
  - NameRTS selected 55.1% of tests and did worse than the path map on
    every metric, because these end-to-end tests share an entry point.
- **Selection only (offline replay against full-suite line coverage):**

  | Method | Tests selected | GPU cost | Affected tests caught | Modified lines covered |
  |---|---|---|---|---|
  | Path map | 62.6% | 67.6% | 76.1% | 96.0% |
  | Runtime selection, no pruning | 35.9% | 39.4% | 84.5% | 99.8% |
  | With pruning | 25.7% | 28.6% | 66.2% | 99.2% |
  | GPT-5.5 agent choosing tests | 39.4% | — | 54.6% | 83.1% |

- **Risk ordering vs. first-in-first-out:** GPU use before the first
  failure fell 89.2%. Against the COLEMAN bandit prioritizer, the median
  first-failure position went from 9 to 4 and GPU use before it from 12.6
  to 2.3 GPU-hours.
- **Workload shrinking:** single tests ran 11.8% faster and used 19.3% less
  GPU.
- **Sampling rate:** 10 Hz costs 0.3% overhead and covers 97.5% of
  modified lines; 50 Hz costs 4.1% and covers 99.2%; 100 Hz costs 17.0%
  and covers 99.6%.
- **Production:** latency fell 58.4%, with no regressions reported from
  skipped tests across 784 CI runs over three weeks.

## Decision edge and limits

- **Run a learned or distance-bounded subset per change; backstop with
  batch runs.** Two companies independently land at about 95% failure
  recall for 15–33% of the candidate set. Both rely on a later full run
  (stabilization, nightly) to catch the tail, so the subset's job is fast
  feedback, not release safety.
- **The missed tail is where marginal compute goes.** At T-Bank, raising
  recall from 26% to 95% costs about 7x the test-minutes. Spend the extra
  compute there only if a late-found breakage is worth that much developer
  time; otherwise rely on the batch backstop.
- **Signals that recur across Google, Facebook, and T-Bank:** per-test
  failure history, distance between change and test (build graph or
  directory), file type, and churn of the touched files. Lexical name
  similarity is negative or useless in both ML studies.
- **Label hygiene is a precondition.** Flaky failures outnumber real ones
  about 4:1 in Facebook's learning runs; training on raw outcomes yields a
  selector that chases flakes.
- **Skip whole builds where possible.** Per-test savings are capped by
  build preparation time, and non-test failures (35% of failing builds)
  escape test-level selectors entirely.
- **Safe selection is viable in Python at function granularity**, but its
  safety is "selects every test that executes changed code," not "catches
  every failure."
- **When each test is GPU training work (FastCI)**, use sampled runtime
  evidence to choose tests, then add "one test per distinct calling
  context." In offline replay, these two steps cut GPU cost 2.4x versus a
  path map while covering more modified lines; with all four stages, end
  to end, the cut is 2.8x. Use failure prediction only to
  order the selected tests, so failures surface after a fraction of the
  GPU-hours.
  - Pruning gives up per-test recall (84.5% to 66.2% of affected tests)
    while losing only 0.6 points of modified-line coverage. That is a
    deliberate bet that one representative per context is enough.
  - Coverage here means executed Python lines. It excludes C++/CUDA and
    whether a test's assertions and inputs differ, so the missed tail is
    unmeasured beyond a three-week production record with no reported
    regressions.
  - Shrinking each test's workload is a separate lever, worth about 18%
    more GPU, and is guarded by periodic full-size reruns.
  - Static function-level selection that works for unit tests (NameRTS)
    over-selects when end-to-end tests share an entry point.
- **For LLM-agent benchmarks**, keep history-based stratification and
  choose representative instances deterministically. This bounds error on
  the aggregate resolve rate; it does not detect which instances regressed.
  It was tested only on code-repair benchmarks.
