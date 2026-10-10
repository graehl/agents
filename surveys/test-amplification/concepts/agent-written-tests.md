# Tests written by the implementing agent

> Read-backed digest (cluster D, trust `single-source`; five read studies,
> four on SWE-bench-derived Python tasks and one function-level. They agree
> that the implementing agent's own tests are a weak or harmful lever unless
> test quality is enforced. The levers they find are a strong, frozen
> separate tester, rigorous rather than lax reproduction tests, writing the
> test before the fix and hardening it against mutants, and feedback that
> avoids trusting self-generated pass/fail verdicts).

**Paper.** Chen, Sun, Shi, Peng, Gu, Lo, Jiang, "Rethinking the Value of
Agent-Generated Tests for LLM-Based Software Engineering Agents," arXiv 2026
([arXiv](https://arxiv.org/abs/2602.07900),
[PDF](https://arxiv.org/pdf/2602.07900),
[local extract](../related-work/extract/chen2026-rethinking-agent-tests/html/2602.07900.md);
cited as RT).

**Paper.** Ahmed, Ganhotra, Shinnar, Hirzel, "Investigating Test Overfitting
on SWE-bench," FSE Companion 2025
([arXiv](https://arxiv.org/abs/2511.16858),
[PDF](https://arxiv.org/pdf/2511.16858),
[local extract](../related-work/extract/ahmed2025-test-overfitting/html/2511.16858.md);
cited as OF).

**Paper.** Tao, Peng, Wang, Wang, Cheng, Yao, Wu, Ge, Li, Gao, "ExecCritic:
Learn to Test, Test to Improve for Coding Agents," arXiv 2026
([arXiv](https://arxiv.org/abs/2609.09133),
[PDF](https://arxiv.org/pdf/2609.09133),
[local extract](../related-work/extract/tao2026-execcritic/tao2026-execcritic.md);
cited as EC).

**Paper.** Tan, Yang, Yang, Yao, Kang, Wang, Zhao, Zhang, Ma, Lin, Rajmohan,
Zhang, "Beyond Fail-to-Pass: Iterative Hardening of Co-Generated Bug
Reproduction Tests and Fixes," arXiv 2026
([arXiv](https://arxiv.org/abs/2607.19843),
[PDF](https://arxiv.org/pdf/2607.19843),
[local extract](../related-work/extract/tan2026-coharden/tan2026-coharden.md);
cited as CH).

**Paper.** Chen, Tao, Zhang, Zhou, Gu, He, Zhang, Cai, Zhao, Jin, "Revisit
Self-Debugging with Self-Generated Tests for Code Generation," ACL 2025
([arXiv](https://arxiv.org/abs/2501.12793),
[PDF](https://arxiv.org/pdf/2501.12793),
[local extract](../related-work/extract/chen2025-revisit-self-debug/chen2025-revisit-self-debug.md);
cited as SD).

## Method

### Rethinking agent-written tests

Six top SWE-bench Bash-Only model families run under mini-SWE-agent on
SWE-bench Verified (500 tasks). The scaffold is bash-only and testing is
optional (RT:59-65). Claude Opus 4.5 resolved 74.4%, Gemini 3 Pro 74.2%,
GPT-5.2 71.8%, Kimi K2 Thinking 63.4%, MiniMax M2 61.0% and DeepSeek v3.2
Reasoner 60.0%. Agent-written tests are new `test_*`/`*_test.py` files
written during the trajectory (RT:69). RQ1 compares resolved and unresolved
trajectories descriptively. RQ2 classifies assertions and value-revealing
prints by AST rules. RQ3 is the causal probe: the prompt is edited to require
at least one new test file (GPT-5.2, Gemini 3 Pro) or to forbid new test files
(Kimi K2, DeepSeek v3.2). Outcomes are compared per task with an exact
McNemar test (RT:693-710). Total API spend was about $1,600 (RT:73).

### Test overfitting

Agentless (Claude-3.7 Sonnet or GPT-4o) supplies the patch and e-Otter++
supplies a generated reproduction test from the issue, on the 449 TDD-Bench
Verified instances (OF:102, 158). A patch *overfits* when it passes the
generated test but fails the hidden golden or regression tests. A refinement
loop of up to 15 iterations lets a critic choose whether to edit the code or
the test, scored by fail-before, pass-after and changed-line coverage
(OF:144-154). The generated tests come from a separate tool, but the same LLM
drives the patch, the test and the refinement.

### ExecCritic: a separate, frozen tester

ExecCritic argues that when one trajectory writes both patch and test,
"their errors can agree and create false confidence" (EC:9, 41). It splits
the roles. A Test agent sees only the issue and the buggy checkout and
submits a repository-native test, a run command and a behaviour contract. A
fail-closed harness admits the test only if it fails cleanly on the buggy
code, then freezes it. A Repair agent revises source only, for up to 5
feedback rounds, and may not edit the test (EC:53-61, 75, 94-108). Test
quality is measured offline as *Base-to-Gold* success: the test fails on the
buggy code and passes on the reference fix (EC:77-82). Both roles use
Qwen-3.5-35B-A3B and are trained separately on SWE-ReBench, the tester by
SFT plus 200 GRPO steps rewarded for discriminating candidate patches, the
repairer by 100 RL steps. GPT-5.6-sol is a stronger-model reference
(EC:146-152).

### CoHarden: rigorous vs lax reproduction tests, co-generation coupling

CoHarden grades a generated bug-reproduction test (BRT) beyond
fail-to-pass. An LLM mutates the golden fix into plausible-but-incorrect
fixes (symptom suppression, incomplete fix, input-specific shortcut,
behaviour substitution). A fail-to-pass test is *Lax* if it accepts more
than \(\tau = 0.202\) of these mutants that the golden test rejects,
*Rigorous* otherwise. A test that fails the golden fix is *Misaligned*
(CH:43-65). The study has two arms with OpenHands + GPT-5-mini on SWT-bench.
In BRT injection, tests from four separate generators (LogicStar, e-Otter++,
AssertFlip, OpenHands) guide a fix agent (CH:69-71). In co-generation
(COGEN), one trajectory writes fix and test together (CH:89-91). The
CoHarden method writes the test first, without source edits (*lax-init*),
then hardens the test-fix pair for up to 5 rounds against 12 fresh mutants
of the current fix. A round is accepted when the new test's laxity
relative to the previous round's test falls below 0.2 (CH:109-137).

### Self-debugging with self-generated tests (function level)

GPT-4o, Claude-3.5-Sonnet, Llama-3-70B and Qwen2.5-Coder-7B each write a
program and their own test suite, then debug from the results. Two
paradigms are compared. *Post-execution* feeds back pass/fail labels or
detailed failures. *In-execution* feeds back intermediate states per basic
block, without the pass/fail verdict (SD:37, 57-65, 250). Benchmarks are
HumanEval(+), MBPP(+) and LiveCodeBench (SD:77).

## Evidence

### Prompted test volume barely moves outcomes (RT)

- **Frequency:** GPT-5.2 wrote tests in 3 of 500 tasks (0.6%) yet resolved
  71.8%, 2.6 points behind Claude Opus 4.5, which wrote tests in about 83%
  of tasks (RT:33, 240). Within each model, resolved and unresolved tasks
  had similar test-writing rates. Unresolved tasks ran tests more often (mean
  6.52 vs 4.89 executions, significant) (RT:543).
- **Content:** value-revealing prints outnumber assertions for every model.
  For Claude 4.5 there were about 25 prints vs 5 asserts per task with tests
  (RT:591). Assertions are mostly property (34-41%) or exact-value (35-43%)
  checks; relational checks are 3-8% (RT:628). The tests act as
  observation channels more than oracles.
- **Intervention:** the prompts flipped test status in 64.4% of GPT-5.2
  tasks, 37.0% of Gemini, 68.4% of Kimi and 75.2% of DeepSeek tasks. On
  average 83.2% of tasks kept the same outcome, and no model's shift was
  significant (all McNemar p > 0.05) (RT:726-728). Net resolved-task changes
  were GPT-5.2 0, Gemini -5, Kimi -13 and DeepSeek -9 (RT:714, 754).
- **Cost:** forcing tests on GPT-5.2 added 5.5% API calls and 19.8% output
  tokens with no gain. Suppressing tests cut Kimi's input tokens by 49.0% and
  calls by 35.4%, and DeepSeek's input tokens by 32.9%, for 2.6- and
  1.8-point drops in resolution (RT:754-760). Grade: `single-source`.
- **Where tests may matter:** 8 issues flipped in both directions with test
  presence (gained with forced tests, lost with suppressed tests). They were
  mostly small correctness bugs with explicit reproduction or edge-case
  conditions (RT:736). The sample is exploratory only.

### Passing your own generated test is weak evidence (OF)

- **No refinement:** of 229 Claude-3.7 patches that passed the generated test,
  50 failed the golden test, a 21.8% overfitting rate. GPT-4o's rate was 33.0%
  (OF:226).
- **Refinement makes it worse:** refining the 220 failing patches against the
  generated test produced 22 new passes, 14 of which failed the golden test.
  The overfitting rate rose to 25.5% (64/251). The apparent +8 resolutions
  netted +5 after 1 already-resolved case and 2 regressions (OF:230, 323).
  Hiding the test and exposing only pass/fail reduced overfitting but also
  reduced golden passes (OF:232).
- **Even golden tests overfit a little:** refining against the revealed
  golden tests still broke regression tests in 5.8% (Claude) and 11.3%
  (GPT-4o) of passing cases (OF:327).
- **Self-trust:** when refinement succeeded, the models mostly edited the
  code rather than the test, treating the test as correct (OF:348). Overfitted
  patches had lower changed-line coverage (median under 0.8 vs 1.0) (OF:462).
  Grade: `single-source`.

### A separate tester helps only if it is good (EC)

All results are SWE-bench Verified resolved rates averaged over three repair
runs.
- **Tester quality decides the sign:** with the untrained Qwen repairer
  fixed at 61.2% (no test), feedback from Qwen-written tests *lowered* it to
  57.3%. GPT-5.6 tests raised it to 65.3%, and an oracle fail-to-pass test
  to 69.4% (EC:164). For GPT-5.6 as repairer, its own separately generated
  tests raised Verified from 81.5% to 85.7% but SWE-bench Pro only from 61.6%
  to 62.3%, against 73.4% with the oracle test. Pro has more fail-to-pass
  tests per instance (mean 14.43 vs 3.03), so one generated test covers
  less of what is required (EC:162).
- **Training the tester:** Base-to-Gold success rose from 22.2% (base) to
  39.6% (SFT) to 62.2% (RL), level with Codex-5.3 (61.0%) and 25.6 points
  below GPT-5.6 (EC:168).
- **Composition:** the trained repairer alone reaches 68.3%. With trained
  tests it reaches 72.6% (+4.3), 11.4 points above the original baseline. An
  oracle test gives 77.6%. Swapping base for trained tests adds 6.8-8.0
  points for either repairer (EC:193, 206). Revision cost an average of 13
  extra turns for the 120 trajectories that entered repair (EC:208).
  Training the repairer on generated rather than oracle feedback ended 1.7
  points lower (70.9% vs 72.6%) (EC:244). Grade: `single-source`.
- ExecCritic does not include an arm where the repair trajectory writes
  its own tests. Its baseline is *no* test feedback, so it isolates tester
  quality and role separation, not self-written vs separately written tests.

### Only rigorous tests help; co-generated tests share the fix's errors (CH)

- **Injection:** 1,104 fail-to-pass separately generated tests lift
  Resolved from 68.4% to 72.6% (+4.3). 474 non-fail-to-pass tests drop it
  from 44.5% to 40.9% (-3.6) (CH:73). Within the fail-to-pass pool the
  Rigorous half gives +8.5 and the Lax half 0.0 (CH:27, 75), and the pattern
  holds per generator.
- **Co-generation:** one trajectory writing both beats the test-only agent
  on fail-to-pass (72.3%, +11.8) but beats the fix-only agent by only +3.0
  on Resolved (61.7%) (CH:93). In 80 of 166 unresolved COGEN instances
  (48.2%), the agent's own test passed the golden fix *and* its wrong fix,
  and the agent stopped (CH:95). Joint failure was 19.9%, 1.87x the 10.6%
  expected if errors were independent. P(fix wrong | test wrong) was 71.7%
  (CH:97).
- **CoHarden:** 69.4% Resolved and 78.9% fail-to-pass on the SWE-bench ∩
  SWT-bench Verified subset, +8.0 Resolved over same-backbone COGEN, at $0.84
  per instance vs $0.77-0.88 for other co-generation methods (CH:29, 143-145,
  174). Margins are +2.7 with GPT-5.4 and +4.0 with Claude Opus 4.5, on 433
  instances (CH:178), and +5.6 over COGEN on Lite (CH:180). Removing either
  phase (lax-init or hardening) leaves 61.0-62.4% Resolved, near the
  61.4% with both removed (CH:191-198). Grade: `single-source`.

### Self-generated tests hurt simple tasks, help hard ones (SD)

- **Test quality:** GPT-4o's self-generated test inputs are 97.6% valid but
  outputs only 89.8% correct, and only 59.2% of HumanEval suites (58.7% MBPP)
  are fully correct (SD:151, 187-189).
- **Post-execution:** with oracle tests, GPT-4o rises from 92.1 to 95.1 on
  HumanEval (SD:87-91). With its own tests it falls to 91.5 (labels) or 89.0
  (detailed feedback), and Claude-3.5 falls from 94.5 to 87.2 (SD:123-132).
  The cause is false negatives: correct programs fail wrong tests, and the
  model "repairs" them (SD:205-209). On LiveCodeBench, label feedback lifts
  GPT-4o from 46.0 to 49.3 overall (SD:166-167), because there negative
  labels more often reflect real bugs.
- **In-execution:** intermediate-state feedback improves GPT-4o MBPP+ from
  76.5% to 79.1% over two iterations, and helps all models on LiveCodeBench,
  with some degradations (SD:252-254). Grade: `single-source`.

## Decision edge and limits

**Where implementing-agent test compute pays off.** In these regimes, little.
Frontier agents on SWE-bench Verified in a bash-only scaffold resolve about
as well with or without self-written tests, and test writing is mostly a
model-specific style. The exploratory exception is narrow, reproducible
correctness bugs where precise expected behaviour is checkable (RT:736).
Separating the tester pays when the tester is strong. Frozen tests from a
separate, stronger or RL-trained tester add 4-8 points on Verified (EC), and
training the tester is worth as much as training the repairer (6.8-8.0 vs
7.3-8.5 points). The gain shrinks when one test cannot cover the requirement
(Pro: +0.7). Rigour, not fail-to-pass, is what counts: only rigorous
reproduction tests help (+8.5 vs 0.0 for lax, CH). Co-generation pays when
the test is written before the fix and then hardened against mutants of
the fix, which buys +8.0 over plain co-generation at similar cost. On
function-level tasks, self-written tests help only where the model's
programs are often wrong (LiveCodeBench) or when feedback avoids the
pass/fail verdict (in-execution). For other separate-tester setups that
pay, see
[generated-tests-as-verifiers](generated-tests-as-verifiers.md) and
[trained-testers](trained-testers.md).

**Neutral.** Encouraging tests in a model that rarely writes them changes
cost, not outcome (GPT-5.2: 0 net, +20% output tokens).

**Harmful.** Refining code until it passes a model-generated test raises the
overfitting rate (21.8% to 25.5% for Claude-3.7) and buys few net
resolutions. The implementing model trusts its test and edits the code to
fit, so the test is a target rather than a check. This is the same failure
that [test-gaming-and-oracles](test-gaming-and-oracles.md) measures under
adversarial conditions. A weak separate tester is also harmful: Qwen tests
cost the Qwen repairer 3.9 points (EC:164), so separation alone does not
help. Misaligned tests subtract (-3.6, CH:73). In plain co-generation the
agent's test shares its fix's misreading (1.87x joint failure) and passes
the wrong fix in almost half of failures, ending the search early. On easy
function-level tasks, debugging against one's own tests lowers pass@1 for
every model (SD:123-132). Suppressing tests in test-heavy models saves
33-49% of input tokens for a statistically insignificant 2-3-point drop.

**Limits.** The repository-level studies all use Python SWE-bench
derivatives, and the Verified split is itself criticised for contamination
(RT:778). SD is function-level only. RT's intervention changes test
*volume* via prompt, not test *quality* or tester independence. ExecCritic
compares separate testers of different quality against no tests. CoHarden
is the closest to a self-vs-separate comparison: co-generated tests
(COGEN) and separately generated injected tests both appear, but with
different fix pipelines and no equal-compute control. CoHarden's
rigorous/lax grading needs the golden fix and golden test; in-loop it uses
the previous round's test as the reference.
