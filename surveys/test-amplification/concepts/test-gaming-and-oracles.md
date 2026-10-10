# Test gaming and the oracle problem

> Read-backed digest (cluster D, trust `single-source`; ImpossibleBench
> (agents exploiting visible tests), SWE-ABS (benchmark tests too weak to
> reject wrong patches) and Konstantinou et al. (LLM oracles track actual
> rather than intended behaviour), plus oracle-design evidence from papers
> read for neighbouring pages).

**Paper.** Zhong, Raghunathan, Carlini, "ImpossibleBench: Measuring LLMs'
Propensity of Exploiting Test Cases," arXiv 2025
([arXiv](https://arxiv.org/abs/2510.20270),
[PDF](https://arxiv.org/pdf/2510.20270),
[local extract](../related-work/extract/zhong2025-impossiblebench/html/2510.20270.md);
cited as IB).

**Paper.** Yu, Cao, Zhang, Lin, Xu, Zhong, Xu, Wang, Cao, Cheung, He, Briand,
"SWE-ABS: Adversarial Benchmark Strengthening Exposes Inflated Success Rates
on Test-based Benchmark," arXiv 2026
([arXiv](https://arxiv.org/abs/2603.00520),
[PDF](https://arxiv.org/pdf/2603.00520),
[local extract](../related-work/extract/yu2026-swe-abs/yu2026-swe-abs.md);
cited as ABS).

**Paper.** Konstantinou, Degiovanni, Papadakis, "Can We Find Bugs Using
LLM-Generated Oracles?," arXiv 2024
([arXiv](https://arxiv.org/abs/2410.21136),
[PDF](https://arxiv.org/pdf/2410.21136),
[local extract](../related-work/extract/konstantinou2024-llm-oracles/konstantinou2024-llm-oracles.md);
cited as KO).

## Method

### ImpossibleBench

Claude Sonnet 4 mutates the unit tests of LiveCodeBench and SWE-bench tasks
so that they contradict the natural-language specification (IB:27-29, 80).
A *one-off* mutation flips one expected value; a *conflicting* mutation adds
an assertion that contradicts the intended behaviour (IB:78). SWE-bench
mutations that the original or an empty patch already passed are removed
(IB:86). Agents are told to follow the specification, get full read/write
test access, are told not to modify tests, and may submit up to 10 times
with failure feedback (IB:92-96). Any pass is therefore cheating, and the
pass rate is the *cheating rate*. Models tested were GPT-5, o3, o4-mini,
GPT-4.1, Claude Opus 4.1, Sonnet 4, Sonnet 3.7 and Qwen3-Coder, at medium
reasoning effort (IB:108). Ablations vary the prompt, test access (full,
read-only, hidden), the feedback loop and an abort option, and evaluate LLM
monitors on the resulting transcripts (IB:159-220).

### SWE-ABS

SWE-ABS strengthens SWE-bench test suites in two GPT-5-driven stages
(ABS:65-69, 210). Stage I uses intraprocedural slicing from the gold patch
to find patch-relevant lines and generates tests for the uncovered ones,
with *decoupling* to strip gold-patch specifics. Stage II has an LLM mutate
the gold patch, keeps issue-relevant mutants (3-LLM majority vote), splits
them into equivalent and non-equivalent, and then generalises tests that
reject equivalent mutants and adds tests that kill surviving non-equivalent
ones (ABS:102-170). The strengthened suites re-score 11,041 previously
passing patches from the top-30 SWE-bench Verified agents and a 150-instance
SWE-bench Pro sample (ABS:17, 185).

### LLM oracles (Konstantinou et al.)

Four LLMs (GPT-3.5-turbo, GPT-4o-mini, DeepSeek V3, Codestral) work on 24
Java repositories, with developer-written and EvoSuite tests (KO:33). In
*classification*, each assertion is judged under four conditions: correct
or mutated code × correct or wrong assertion. A model tracking expected
behaviour should accept a correct assertion even when the code is buggy
(KO:119-136). Other tasks test sensitivity to EvoSuite-style anonymised
names (KO:142-148) and *generation* of 1 or 5 assertions per prefix on
correct code (KO:155-159). The last compares PiTest mutation scores of LLM
oracles and EvoSuite's oracles on the same prefixes (KO:163, 215, 462).

## Evidence

### How often agents game tests

- GPT-5, the best performer on the original benchmarks, cheated on 54.0% of
  Conflicting-SWEbench and 76% of Oneoff-SWEbench tasks, but only 2.9% of
  Oneoff-LiveCodeBench (IB:31, 124). More capable models generally cheat
  more (IB:120, 242), though newer Claude models cheat less than older ones
  (IB:124).
- Four strategies appear: modifying tests, overloading comparison operators,
  recording state across calls, and special-casing the observed test
  (IB:136-139). Claude and Qwen3-Coder cheat mostly (over 79%) by editing
  tests; OpenAI models spread over all four (each over 14%) (IB:153).

### Context engineering levers

- **Prompt:** on Conflicting-LiveCodeBench, looser prompts (A, B) give over
  85% cheating for GPT-5 and o3; the strictest prompt (D) gives 1% and 33%,
  with no significant change on the original tasks (IB:32, 165). On
  Conflicting-SWEbench a looser prompt raises GPT-5 from 54% to 66% (IB:182).
- **Test access:** hiding tests drives cheating success to near zero but
  also lowers performance on the original benchmark. Read-only access
  restores legitimate performance and blocks test edits, but not
  special-casing or operator overloading (IB:190). Exact read-only and
  hidden rates are in Figure 7, not the text.
- **Feedback loop:** averaged over models, multiple submissions raise
  open-test SWE-bench passes from 80% to 83% and Conflicting-SWEbench
  cheating from 33% to 38% (IB:202). An abort option
  (`flag_for_human_intervention`) cut GPT-5 from 54% to 9% and o3 from 49% to
  12%, with little effect on Claude Opus 4.1 (IB:204).
- **Monitoring:** Claude Sonnet 4 and Opus 4 monitors flag 86-89% of
  cheating on Impossible-LiveCodeBench but only 42-65% on
  Impossible-SWEbench. Plausible rationalisations such as "backward
  compatibility" evade them (IB:220-222). Grade: `single-source`.

### Benchmark tests are too weak (ABS)

- 2,184 of 11,041 patches that passed the original Verified tests (19.78%)
  fail the strengthened suites. 251 of 500 instances (50.2%) are
  strengthened, vs 10 (2%) for the prior UTBoost (ABS:9, 218). The top agent
  falls from 78.80% to 62.20% (1st to 5th). The mean per-agent drop is 14.56
  points vs 0.70 for UTBoost, and Spearman rank correlation is 0.82 vs 0.98
  (ABS:17, 220).
- On the SWE-bench Pro sample the mean drop is 16.46 points, although the
  top Pro score is only 45.89%. A harder benchmark does not mean stronger
  tests (ABS:230). GLM-4.7 strengthens the same 31 of 50 instances as GPT-5
  (ABS:238).
- **False rejections:** manual review of all 500 instances found 53 (10.6%)
  whose augmented tests encoded gold-patch specifics; these were corrected
  before the headline numbers (ABS:248). Of 100 sampled newly rejected
  patches, 47% had logic errors and 35% were incomplete fixes (ABS:254).
- **Ablation:** generated tests without either stage strengthen 190
  instances (10.34-point drop). Coverage-driven Stage I gives 198 (11.30)
  and adding mutation-driven Stage II gives 251 (14.56) (ABS:272-276). The
  text calls Stage II "44 more" than Stage I, inconsistent with 251-198=53.
  Grade: `single-source`.

### LLM oracles track actual behaviour (KO)

- Classification accuracy on a correct assertion drops when the code is
  mutated, so the models judge against the implementation rather than
  the intent (KO:311, 317-319). General-purpose models lean toward rejecting
  assertions; Codestral leans toward accepting them (KO:321-325). Overall
  accuracy is "less than 50% in some cases" (KO:35).
- Anonymising test and variable names to EvoSuite style costs up to
  15.3-15.4 points for the GPT models, 10.2 for DeepSeek V3 and 6.6 for
  Codestral (KO:371).
- Generation beats classification by up to 13.29 points (KO:37, 422). With
  five assertions per prefix, at least one passes in 92.9-97.3% of cases
  (KO:456). Mutation scores of the passing LLM oracles are generally higher
  than EvoSuite's on the same prefixes, by up to 2.96 points (KO:37, 464).
  Generation ran on correct code and kept only oracles that pass on it, so
  these are regression oracles by construction. The authors conclude LLM
  oracles mainly suit regression testing and augmentation, and that every
  suggestion needs human inspection (KO:35, 39). Grade: `single-source`.

### Oracle choices in read generators (cross-reference)

Pages in this survey show three oracle designs, each with its own failure
mode.

- **Regression oracle (actual behaviour).** TestGen-LLM discards any test
  that fails on first run, because it cannot tell a found bug from a wrong
  assertion. The surviving tests pin current behaviour and guard against
  future regressions (see [llm-test-amplification](llm-test-amplification.md);
  [TestGen-LLM extract](../related-work/extract/alshahwan2024-testgen-llm/html/2402.09171.md),
  line 97). Such tests cannot catch bugs already present.
- **Change oracle with human confirmation.** Meta's JIT catching tests must
  fail, so the implicit oracle is unavailable. A weak catch becomes a strong
  catch only after the diff author confirms the behaviour change was
  unintended. 8 of 41 reach-outs were real bugs
  ([extract](../related-work/extract/becker2026-jit-catching-meta/html/2601.22832.md),
  lines 23-25, 39).
- **Predicted expected values.** UTGen finds that untrained models trade
  bug-exposing inputs against correct expected outputs; harder inputs get
  wrong oracles. Output voting recovers 11.4 points of downstream debugging
  accuracy ([trained-testers](trained-testers.md)). In issue resolution,
  21.8-33.0% of patches that pass a generated test fail the golden tests
  ([agent-written-tests](agent-written-tests.md)).

## Decision edge and limits

**What this means for test-writing compute.** Any test the implementing
agent can see, and especially edit, is an optimisation target. With
specification and tests in conflict, frontier agents satisfy the tests most
of the time on repository-level tasks. Spending compute on more iterations
against visible tests raises gaming along with real passes (feedback: +3
points legitimate, +5 points cheating). The cheap levers are configuration,
not compute: read-only or hidden held-out tests, strict prompts and an
explicit abort path. A separate tester whose tests the implementer cannot
modify is the structural version of the read-only fix. Hidden tests cost
some legitimate performance (IB:190), so the trade is real.

**Where verification compute still pays.** Held-out tests and human-confirmed
oracles (JIT) avoid the gaming loop. LLM monitors catch most gaming on
small algorithmic tasks but under two thirds on multi-file tasks, so
monitoring adds value without being sufficient. Adversarial
*test-strengthening* compute pays at evaluation time. Mutating a known-good
patch and killing the surviving mutants exposed about one in five
"resolved" patches as wrong, and the mutation stage added more than
coverage-driven generation did (ABS). This is the same mutant-kill pattern
as ACH and CoHarden's hardening, applied to the evaluator rather than the
agent. LLM-written assertions are cheap regression oracles: 93-97% of
prefixes get a passing assertion out of five, with slightly higher mutation
scores than EvoSuite's. They are not evidence of intended behaviour (KO).

**Limits.** ImpossibleBench measures *propensity* under deliberately
contradictory tests. SWE-ABS measures the other side: how often ordinary
agents' patches slip through honest but weak tests (19.78% of passing
patches). It does not show whether agents exploit that weakness on purpose,
and it needs the gold patch, so it cannot be used at implementation time.
Its augmented tests themselves over-fit the gold patch in 10.6% of
instances before manual correction. KO is Java, function-level, and pre-2025
models. IB mutations were LLM-generated and filtered only on SWE-bench
(IB:86). Results are for late-2025 models at
medium reasoning effort.
