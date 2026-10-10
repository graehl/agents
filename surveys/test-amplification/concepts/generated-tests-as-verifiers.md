# Generated tests as verifiers for candidate patches

> Read-backed digest (cluster D, trust `single-source` per paper. The
> qualitative effect, that filtering patches by generated reproduction tests
> trades recall for much higher precision, was found independently by two
> groups (SWT-bench, Otter); magnitudes are single-source. CodeT supplies the
> function-level origin of test-based voting).

**Paper.** Mündler, Müller, He, Vechev, "SWT-Bench: Testing and Validating
Real-World Bug-Fixes with Code Agents," NeurIPS 2024
([arXiv](https://arxiv.org/abs/2406.12952),
[PDF](https://arxiv.org/pdf/2406.12952),
[local extract](../related-work/extract/mundler2024-swtbench/html/2406.12952.md);
cited as SWT).

**Paper.** Ahmed, Ganhotra, Pan, Shinnar, Sinha, Hirzel, "Otter: Generating
Tests from Issues to Validate SWE Patches," ICML 2025
([arXiv](https://arxiv.org/abs/2502.05368),
[PDF](https://arxiv.org/pdf/2502.05368),
[local extract](../related-work/extract/ahmed2025-otter/html/2502.05368.md);
cited as OT).

**Paper.** Ehrlich, Brown, Juravsky, Clark, Ré, Mirhoseini, "CodeMonkeys:
Scaling Test-Time Compute for Software Engineering," arXiv 2025
([arXiv](https://arxiv.org/abs/2501.14723),
[PDF](https://arxiv.org/pdf/2501.14723),
[local extract](../related-work/extract/ehrlich2025-codemonkeys/html/2501.14723.md);
cited as CM).

**Paper.** Chen, Zhang, Nguyen, Zan, Lin, Lou, Chen, "CodeT: Code Generation
with Generated Tests," ICLR 2023
([arXiv](https://arxiv.org/abs/2207.10397),
[PDF](https://arxiv.org/pdf/2207.10397),
[local extract](../related-work/extract/chen2022-codet/chen2022-codet.md);
cited as CT).

## Method

### CodeT (function level, the origin of test voting)

The same model samples many solutions and many test cases (up to 100
samples, 5 asserts each, so at most 500 tests per HumanEval problem) from a
prompt with the example I/O removed (CT:103, 225). Solutions that pass the
same set of tests form a consensus set, scored as (number of solutions) ×
(number of tests passed). One solution is taken from the top set (*dual
execution agreement*, RANSAC-inspired) (CT:31, 51-75). Evaluation uses
Codex variants, InCoder and CodeGen on HumanEval, MBPP, APPS and
CodeContests, zero-shot (CT:33).

### SWT-bench

SWE-bench is turned into a test-generation benchmark of over 1,900 instances
plus a Lite split. A generated test *reproduces* the issue when it fails
before the golden patch and passes after it; change coverage of the golden
patch is a secondary metric (SWT:20, 178-190). Methods compared are zero-shot
prompting, a robust test-specific diff format (ZeroShotPlus), Pass@5 with
oracle choice, libro, and repair agents (SWE-Agent, aider, AutoCodeRover)
re-prompted to write tests. GPT-4 is the default model, with a cap of 20
SWE-Agent API calls (SWT:269-301). The filter experiment runs SWE-Agent
separately to produce fixes and tests, then keeps only fixes on which every
generated test is fail-to-pass or pass-to-pass (SWT:393).

### Otter

Otter generates tests from the issue *before* any patch exists, on
TDD-Bench-Verified (449 SWE-bench Verified instances). It uses file
localization, a self-reflective action planner, and rule-based checks and
repairs such as import fixing (OT:21-23, 75). Otter++ runs the generator
five times with heterogeneous prompts (with or without the planner and each
localization) and ranks by execution logs on the old code (OT:79). The
filter experiment runs the five Otter++ tests on the submitted patches of 22
SWE-bench Verified leaderboard systems and rejects a patch when all tests
fail on it (OT:613).

### CodeMonkeys

For each issue, ten pairs of state machines run with Claude 3.5 Sonnet. A
testing machine iterates a standalone reproduction script against the
unedited code, and an editing machine iterates the edit while it may still
revise the test ("two-sided debugging", so the test must fail before and
pass after) (CM:168-179). Each machine gets up to 8 iterations. Selection
runs all 10 tests against all 10 edits, keeps the top 3 by pass count, and
hands them to a selection state machine that can write new discriminating
tests (CM:210-213).

## Evidence

### Test voting over samples (CT)

- With code-davinci-002 on HumanEval, pass@1 rose by 18.8 points to 65.8%,
  so the random-choice baseline was 47.0% by subtraction. The other Codex
  models gained about +10, MBPP +9.6, and InCoder/CodeGen +4.2 to +13.1 (CT:127-129). Clustering by
  outputs without test agreement (AlphaCode-C) was consistently worse
  (CT:131).
- On harder sets the gain fades: +7.4 pass@1 on APPS introductory problems,
  not significant on APPS competition level or CodeContests (CT:135).
- Tester quality transfers. Giving weaker models code-davinci-002's tests
  adds +6.2 to +15.9 pass@1 for InCoder/CodeGen over their own tests
  (CT:208). Ten tests already give +9.5; gains flatten beyond about 50
  samples × 3 asserts (CT:225). In 53 of 164 problems a correct solution
  existed but was not top-ranked, about 20% of them due to ambiguous specs
  or missing corner cases (CT:233). Grade: `benchmark-reported`.

### Agents as test writers (SWT)

- On SWT-bench Lite with GPT-4, success rates were ZeroShot (unified diff)
  about 3x lower than ZeroShotPlus, ZeroShotPlus 9.4%, libro 14.1%, aider
  12.7%, AutoCodeRover 9.1%, SWE-Agent 15.9%, and SWE-Agent+ (told to run its
  tests) 18.5% (SWT:293, 307). Oracle Pass@5 reached 20.3%. Execution feedback
  and a test-friendly edit format are the main tool effects.
- An ideal ensemble of the four best methods solves 71% more instances than
  the best single method. Repair success and reproduction success correlate
  overall but not per instance (SWT:24).
- Giving the model the right test file to edit nearly doubles success (8.1%
  to 15.1%). Giving it a candidate patch, correct or not, helps less (10.5%)
  (SWT:389).

### Precision filtering

- **SWT:** filtering SWE-Agent fixes by SWE-Agent-generated tests raised
  precision to 47.8% at 20% recall, "more than double" the unfiltered
  precision (SWT:10, 393). The unfiltered baseline precision is not given
  in that passage. SWE-bench-Lite resolution was about 20% for
  state-of-the-art methods at the time (SWT:393). Grade: `single-source`.
- **OT:** Otter's fail-to-pass rate was 31.4% and Otter++'s 37.0%, against
  18.7% for its baseline, with GPT-4o at under $0.10 per issue (OT:21, 177,
  455). On SWT-bench Lite it reached 25.4% and 29.0% vs 19.2% for SWE-Agent+
  (OT:394). Filtering leaderboard patches gave 65-92% precision at 30-41%
  recall; for the third-ranked system precision went from 60.8% to 91.9% at
  33% recall (OT:23, 613). Removing the planner loses 14-20% of fail-to-pass
  tests with GPT-4o (OT:251). Five heterogeneous prompts beat five
  temperature-1.0 samples at top-1 (166 vs 146) (OT:609). Grade:
  `single-source`; the precision effect agrees with SWT across groups.

### Test-based selection at scale (CM)

- Coverage (any correct edit among the 10) was 69.8%. Random selection
  scored 45.8%. Top-3 test voting followed by the selection state machine
  scored 57.4% on SWE-bench Verified, closing about half the random-to-oracle
  gap, for about $2,300 total (CM:11, 113, 208, 217). Model selection without
  the test-vote prefilter did worse than pure test voting (CM:217).
- Pooling CodeMonkeys with the top-4 leaderboard submissions (80.8%
  coverage) and selecting gave 66.2%. The best single member scored 62.8% and
  random selection 60.9%, so selection recovered a smaller share of the gap
  (CM:115, 223). Grade: `benchmark-reported` (SWE-bench Verified score, not
  independently executed here).
- Serial and parallel generation compute reach similar coverage at matched
  cost after the first few iterations, but more parallel candidates make
  selection harder (CM:179).

## Decision edge and limits

**Where verifier-test compute pays off.** A separately generated
reproduction test is a cheap, strong *precision* filter. It cost about $0.09
per issue in Otter, and the same group of five tests lifts many leaderboard
systems to 65-92% precision. This pays when a wrong patch is costly and
abstaining is acceptable (auto-merge gates, triage), and when many
candidates exist (CodeMonkeys' test voting is the useful first stage of
selection). At function level, voting with many cheap tests is the
founding result (CodeT, +18.8 pass@1). Its value tracks tester quality more
than coder quality: a better model's tests lift weaker coders by up to 15.9
points. Execution feedback while writing the test (SWE-Agent+, Otter's
planner and repair, CodeMonkeys' two-sided debugging) and heterogeneous
prompts each add measurable yield.

**Where it is neutral or harmful.** The filters cost recall: SWT keeps only
20% of correct fixes and Otter 30-41%. Fail-to-pass rates of 30-40% mean
most issues get no valid test. Selection over heterogeneous strong
candidates recovers little (66.2% vs 60.9% random). CodeT's gain vanishes
on competition-level problems, where few samples are correct. Generated
tests can
themselves be wrong; see
[agent-written-tests](agent-written-tests.md) for the overfitting rate when
the same tests drive refinement rather than only filtering.

**Who writes the test.** In CodeT the same model samples code and tests,
independently. In SWT and Otter the tester is a separate run or a
dedicated tool, independent of the patch. In CodeMonkeys the editing machine
co-writes its own test, but selection votes across tests from all ten
independent trajectories. None of these papers isolates self-written vs
cross-written tests at equal compute.
