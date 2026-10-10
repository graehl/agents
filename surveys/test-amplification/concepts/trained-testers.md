# Training the tester

> Read-backed digest (cluster D, trust `benchmark-reported` for CURE's
> standard-benchmark scores and `single-source` for UTGen's custom debugging
> splits; neither has been independently rerun. Both are function-level
> Python tasks, not repository-level agents).

**Paper.** Wang, Yang, Tian, Shen, Wang, "Co-Evolving LLM Coder and Unit
Tester via Reinforcement Learning," NeurIPS 2025
([arXiv](https://arxiv.org/abs/2506.03136),
[PDF](https://arxiv.org/pdf/2506.03136),
[local extract](../related-work/extract/wang2025-cure/html/2506.03136.md);
cited as CURE).

**Paper.** Prasad, Stengel-Eskin, Chen, Khan, Bansal, "Learning to Generate
Unit Tests for Automated Debugging," COLM 2025
([arXiv](https://arxiv.org/abs/2502.01619),
[PDF](https://arxiv.org/pdf/2502.01619),
[local extract](../related-work/extract/prasad2025-utgen/html/2502.01619.md);
cited as UT).

## Method

### CURE: one policy as coder and tester, trained by RL

For each training task the policy samples 16 solutions and 16 unit tests.
Every solution is executed against every generated test plus the task's
ground-truth tests (CURE:157, 505). A solution's reward is the number of
ground-truth tests it passes. A test's reward is an estimate of
\(\mu = p_u(1-p_{01}) - (1-p_u)p_{00}\). It is positive when the test passes
all correct solutions and fails incorrect ones, and negative when it
rejects a correct solution or admits incorrect ones (CURE:169-179). The
derivation shows that best-of-N reward precision goes to 1 as the number of
tests grows exactly when \(\mu > 0\) (CURE:117-153). "No ground-truth code"
means no reference *solutions*; ground-truth *tests* still define which
solutions count as correct. Training used 4.5k CodeContests problems,
Qwen2.5-7B/14B-Instruct for 350 steps and Qwen3-4B (long-CoT) for 50 steps,
on 8 A100s. The long-CoT tester gets a length penalty (CURE:264-287, 505).

### UTGen and UTDebug: supervised tester, guarded debugging loop

UTGen builds training data from Tulu-3 code. It perturbs reference
solutions into buggy ones, keeps test inputs on which the reference and the
buggy code disagree, labels each with the reference output and a
chain-of-thought, and fine-tunes on about 30K (8B) or 70K (32B) examples
(UT:74-82). UTDebug uses the tests during debugging. Each predicted output
gets 8 self-consistency samples with a majority vote (UT:96). Each round
generates \(n=3\) tests, uses one as feedback, and accepts an edit only if
the pass rate on the whole generated set improves, backtracking otherwise
(UT:100). The intrinsic metrics are *attack rate* (does the input expose the
bug) and *output accuracy* (is the expected value right) (UT:122-124).
Evaluation uses HumanEval+Fix (158), MBPP+Fix (325) and a harder MBPP+Fix
(Hard) split (170) whose buggy code passes 50-95% of tests (UT:112-114).

## Evidence

### CURE

- Against their Qwen2.5-Instruct bases on five benchmarks (LiveBench, MBPP,
  LiveCodeBench, CodeContests, CodeForces), the 7B/14B ReasonFlux-Coder
  models gained on average 37.8% in unit-test accuracy, 5.3% in one-shot code
  accuracy and 9.0% in best-of-N accuracy with 16 codes and 16 tests
  (CURE:15, 287, 639). The extract does not say whether these are absolute
  points or relative gains.
- Used across other test-time pipelines (MPSC, AlphaCodium, S*), the 14B
  model gained 8.1% over its base (CURE:665). The 4B long-CoT tester cut
  test-generation response length to 64.8% (CURE:643).
- **Separate small tester for a stronger coder:** ReasonFlux-Coder-4B as
  tester raised best-of-N for GPT-4o-mini by 5.5% and GPT-4.1-mini by 1.8%.
  GPT-4o-mini plus the 4B tester beat GPT-4o one-shot by 7.0% at lower cost.
  Scaling GPT-4o-mini alone gained 1.5% at about twice the API cost
  (CURE:657).
- **Tester as RL reward:** tests from the 4B model as the reward for RL on
  Qwen2.5-14B gave gains comparable to ground-truth tests (CURE:661).
  Grade: `benchmark-reported`.

### UTGen / UTDebug

- Untrained models show a trade-off. Inputs that expose bugs are hard edge
  cases whose outputs the model mispredicts, while random tests have correct
  outputs but rarely expose bugs (UT:31, 236). UTGen beats LLM baselines by
  7.59% on the joint accuracy-and-attack metric (UT:9).
- After 3 rounds of debugging with Qwen2.5-32B on MBPP+Fix, UTGen tests beat
  random tests by 4.61, prompted failing tests by 3.38 and no-test debugging
  by 15.07 points. On MBPP+Fix (Hard) they beat random tests by 22.35 and
  no-test debugging by 12.35 points (UT:353). Tests from the 32B UTGen model
  improved GPT-4o as debugger by 13.8% (UT:9, 523).
- As a best-of-10 judge on HumanEval+ with Llama3-8B, UTGen tests beat an 8B
  reward model by 4.36, random tests by 3.73 and prompted tests by 1.83 points
  (UT:428).
- **Ablation:** without self-consistency on outputs, UTGen-based debugging
  drops 11.4 points (random tests drop 4). Without validation and
  backtracking, the model overfits to the feedback test and loses up to 3.2
  points (UT:1604). On MBPP+Fix (Hard), scaling to 15 tests leaves a
  10-point gap between UTGen and random tests (UT:1694). Grade:
  `single-source` (custom debugging splits).

## Decision edge and limits

**Where tester training and tester compute pay off.** A tester trained to
discriminate (CURE's \(\mu\) reward) or to target the given buggy code
(UTGen) gives better selection and debugging signal than prompting the same
model for tests. A small trained tester can lift a larger API coder more
cheaply than sampling the coder more (CURE:657). Inside the debugging loop,
the compute that pays is output-voting on each test (self-consistency) and
cross-validating edits on held-out generated tests. Both guard against the
tester's own wrong oracles, the dominant failure of generated tests.
The repository-level analogue is ExecCritic's RL-trained tester, which
nearly triples Base-to-Gold validity (22.2% to 62.2%) and turns harmful
feedback into a gain (see [agent-written-tests](agent-written-tests.md)).

**Neutral or harmful.** Debugging against a single generated test without
validation overfits (UT:1604), the function-level version of the
repository-level overfitting in
[agent-written-tests](agent-written-tests.md). CURE notes that the
test-voting reward breaks down when generated tests are inaccurate, when the
problem is ambiguous, or for binary-output tasks (CURE:101). Gains are
smaller for long-CoT models, which already capture much of the benefit
through reasoning (CURE:643).

**Limits.** All evidence is single-function Python with I/O-style tests.
CURE's training still needs ground-truth tests, and its abstract numbers
are averages over heterogeneous benchmarks. Neither paper tests an adversarial
tester against the coder that wrote the code. In CURE coder and tester are
the *same* policy, rewarded cooperatively through the execution matrix, and
whether that invites collusion is not studied. Ahmed et al. flag CURE
as potentially susceptible to test overfitting and reward hacking
([extract](../related-work/extract/ahmed2025-test-overfitting/html/2511.16858.md),
line 120).
