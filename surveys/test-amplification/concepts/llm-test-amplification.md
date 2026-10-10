# LLM test amplification: filters, mutants, diffs and coverage feedback

> Read-backed digest (cluster D, trust `single-source`; the three Meta
> deployments come from one group and report self-measured acceptance rates
> with no external replication; CoverUp and Cleverest are single academic
> evaluations with public artifacts; TestGenEval is the benchmark authors'
> own runs. TestGen-LLM's abstract and body disagree on one headline number,
> noted below).

**Framing.** Danglot, Vera-Pérez, Yu, Zaidman, Monperrus, Baudry, "A
Snowballing Literature Study on Test Amplification," JSS 2019
([arXiv](https://arxiv.org/abs/1705.10692),
[PDF](https://arxiv.org/pdf/1705.10692),
[local extract](../related-work/extract/danglot2019-amplification-snowball/html/1705.10692.md);
cited as DA). Test amplification exploits the inputs and oracles already
embedded in a human-written suite to improve it toward an engineering goal
(DA:43). Its four categories are `AMP_add` (new tests as variants of existing
ones, usually for coverage, DA:84), `AMP_change` (new tests that cover or
observe a specific code change, DA:202), `AMP_exec` (modify the harness or
execution to learn more, DA:358) and `AMP_mod` (modify existing test bodies,
e.g. sharper oracles, DA:388). The survey predates LLMs; it supplies the
taxonomy only, not effectiveness evidence. In its terms TestGen-LLM, ACH and
CoverUp are `AMP_add`; JIT catching and Cleverest are `AMP_change`.

**Paper.** Alshahwan, Chheda, Finegenova, Gokkaya, Harman, Harper, Marginean,
Sengupta, Wang, "Automated Unit Test Improvement using Large Language Models
at Meta," FSE Companion (Industry) 2024
([arXiv](https://arxiv.org/abs/2402.09171),
[PDF](https://arxiv.org/pdf/2402.09171),
[local extract](../related-work/extract/alshahwan2024-testgen-llm/html/2402.09171.md);
cited as TG).

**Paper.** Foster, Gulati, Harman, Harper, Mao, Ritchey, Robert, Sengupta,
"Mutation-Guided LLM-based Test Generation at Meta," FSE Companion (Industry)
2025 ([arXiv](https://arxiv.org/abs/2501.12862),
[PDF](https://arxiv.org/pdf/2501.12862),
[local extract](../related-work/extract/harman2025-ach-meta/html/2501.12862.md);
cited as ACH).

**Paper.** Becker, Chen, Cochran, Ghasemi, Gulati, Harman, et al.,
"Just-in-Time Catching Test Generation at Meta," FSE Companion (Industry)
2026 ([arXiv](https://arxiv.org/abs/2601.22832),
[PDF](https://arxiv.org/pdf/2601.22832),
[local extract](../related-work/extract/becker2026-jit-catching-meta/html/2601.22832.md);
cited as JIT).

**Paper.** Altmayer Pizzorno, Berger, "CoverUp: Effective High Coverage Test
Generation for Python," Proc. ACM Softw. Eng. (FSE) 2025
([arXiv](https://arxiv.org/abs/2403.16218),
[PDF](https://arxiv.org/pdf/2403.16218),
[local extract](../related-work/extract/pizzorno2024-coverup/html/2403.16218.md);
cited as CU).

**Paper.** Liu, Lee, Losiouk, Böhme, "Evaluating LLM-Based Regression Test
Generation," ACM FSE 2026
([PDF](https://mboehme.github.io/paper/FSE26-llmtesting.pdf),
[local extract](../related-work/extract/liu2026-llm-regression-testgen/liu2026-llm-regression-testgen.md);
cited as LIU).

**Paper.** Jain, Synnaeve, Rozière, "TestGenEval: A Real World Unit Test
Generation and Test Completion Benchmark," ICLR 2025
([arXiv](https://arxiv.org/abs/2410.00752),
[PDF](https://arxiv.org/pdf/2410.00752),
[local extract](../related-work/extract/jain2024-testgeneval/jain2024-testgeneval.md);
cited as TGE).

## Method

### TestGen-LLM (Meta, Kotlin, 2023)

Two internal LLMs extend existing human-written test classes. Every candidate
must build, pass five consecutive runs (flakiness filter) and add line
coverage over all test classes under the same build target; anything else is
discarded (TG:95-103). Later versions also drop syntactic duplicates, because
samples were either near-identical or very different (TG:371-375). Survivors
go to engineers as one diff per test case.

### ACH (Meta, privacy hardening)

An LLM writes faults specific to a concern (privacy) into a class, an LLM
judge discards equivalent mutants, and a modified TestGen-LLM writes tests
that kill the surviving mutants (ACH:105-113). All agents used Llama 3.1 70B
(ACH:95). Mutation stops at the first building, passing mutant per class
(ACH:121).

### Just-in-time catching tests (Meta, backend diffs)

The tests are meant to fail on a proposed diff and pass on its parent, so the
generator cannot rely on the implicit oracle (JIT:23-25). The "dodgy diff"
workflow treats the diff as a mutant of its parent; the intent-aware workflow
asks the LLM for the diff's risks from code, title and summary, builds mutants
from them, and runs mutation-guided generation (JIT:69-91). Rule-based and
LLM-as-judge assessors score each weak catch before a human reaches out to the
author (JIT:258-303).

### CoverUp (Python, GPT-4o)

CoverUp prompts with the code segments lacking coverage, gives the model a
`get_info` tool for more context, and continues the chat (up to two more
prompts) when a test fails or adds no coverage (CU:290-294, 418, 938).

### Cleverest (structured-input C programs)

Cleverest treats regression test generation as translation from commit
message plus diff into an input file (JavaScript, XML, PDF, ...). An execution
analyzer runs the input on both revisions and feeds back reach, output-change
and sanitizer results for up to five iterations (LIU:76-103). It ran on 72
bug-introducing and bug-fixing commits in eight programs, ten repetitions each
(LIU:133-135).

### TestGenEval (benchmark, vanilla prompting)

TestGenEval has 1,210 code/test file pairs (68,647 tests) from 11 SWE-bench
repositories. Its tasks are full-suite generation from the file under test
and completion of the first, last or an extra test in an existing human
suite. It scores coverage and cosmic-ray mutation score (TGE:9, 49, 589-591).
Models are prompted once with the code (no execution feedback); pass@5
samples at temperature 0.8 (TGE:178, 508).

## Evidence

### Filter funnels and acceptance

- **TestGen-LLM, 86 Instagram components:** 75% of *test classes* had at
  least one generated test that built, 57% one that also passed reliably,
  25% one that also added coverage (TG:226-231). These are per-class
  rates. Per generated test, only about 4% clear every filter (TG:250;
  Table 3: 490/8,996 Facebook, 831/23,535 Instagram, TG:309-313).
- **Deployment:** 196 of 1,979 classes improved (TG:303), i.e. about 10%. The
  abstract says 11.5% (TG:49); the body's contribution list says 10% (TG:78).
  73% of recommendations were accepted. Facebook test-a-thon: 144 of 280 diffs
  accepted, 61 never reviewed (TG:290-295). Grade: `single-source`.
- **ACH:** 10,795 classes yielded 9,095 mutants that build and pass, 25% of
  them syntactically identical to the original (ACH:123). 4,660 (51%) were
  judged non-equivalent (ACH:257) and produced 571 tests. 277 of those 571
  would have been discarded by a coverage-only filter (ACH:65). Engineers
  accepted 73% and rated 36% privacy-relevant (ACH:67, 554). Acceptance varied
  by team, 56% at WhatsApp vs 89% at Messenger (ACH:571). The equivalence judge
  had precision 0.79 and recall 0.47, or 0.95 and 0.96 with comment stripping
  and lexical dedup (ACH:69, 717). Grade: `single-source`.

### Change awareness

- **JIT, 22,126 tests:** the weak-catch rate per generated test was 0.2% for
  tests that coincidentally fail on the diff, 2.0% for coverage-free
  TestGen-LLM, 0.9% for coverage-requiring TestGen-LLM, 0.8% for ACH, 2.5% for
  dodgy-diff and 6.4% for intent-aware (JIT Table 1, lines 100-209). The
  abstract's "4x over hardening, 20x over coincidental" rounds these. Per diff,
  intent-aware caught 7.9% of diffs vs 3.6% for the best diff-unaware baseline
  (JIT:224).
- **Review load and outcomes:** the assessors cut human review by about 70%
  on 600 weak catches (JIT:35, 303). 41 reach-outs yielded 8 strong catches
  (19.5%), 4 of them severe (JIT:39). The body also says "7 issues from 41"
  (JIT:240) and quotes 43% severe for 4 of 8 (JIT:236). Both are internal
  inconsistencies; 8/41 = 19.5% matches the abstract. Grade: `single-source`.
- **Cleverest:** with GPT-4o it found 7 of 36 bugs in bug-introducing
  commits and reproduced 13 of 36 bug-fixing commits (LIU:180). Most runs took
  under a minute and cost about $0.2 (LIU:194). On the 50 commits WAFLGo could
  run, it beat WAFLGo on reproduction (11 vs 8 of 24) and lost on finding (7 vs
  10 of 26), using minutes against WAFLGo's 24-hour campaigns (LIU:357-359).
  Seeding 24-hour AFL++ runs with its near-miss inputs (ClevFuzz) found 20 of
  26 and 18 of 24 (LIU:365). Dropping commit information cut bugs from 20 to 4
  (LIU:407-411). Expanding uninformative commit messages by about 17 words
  improved 17 of 29 commits (LIU:11, 276). Grade: `single-source`.

### Coverage feedback vs plain prompting

- **CoverUp vs CodaMosa (CM suite, 425 modules):** median per-module
  line+branch coverage was 80% for CoverUp, 55% for CodaMosa-gpt4o and 47% for
  CodaMosa-codex. Whole-suite coverage was 60% vs 49% and 45% (CU:662).
  Against MuTAP on the MT suite it reached 89% vs 77% overall (CU:23).
- **Ablation (same model, same prompt, no tooling):** 60% vs 34% overall and
  80% vs 39% median (CU:813). 40% of successful tests came from the
  second or third prompt (CU:938). Removing error-fixing loses 14-37 points and
  removing code context 7-16. Removing the coverage hint costs at most 2
  points, but the model then writes 52% more test functions (11,222 vs 7,366)
  (CU:1094-1096).
- **Cost:** $399 and 4 h for CoverUp, $265 and 71 h for CodaMosa-gpt4o, $75
  for the ablated version (CU:960). Grade: `single-source`.
- **TestGenEval, no tools:** the best model, GPT-4o, reaches 35.2% coverage
  and 18.8% mutation score when generating whole suites for real files
  (TGE:27, 174). When completing the last test of an existing human suite,
  every model adds "virtually no" coverage (under 1%) (TGE:27, 198). For
  Llama 3.1 8B, coverage@k keeps rising through k=20 for suite generation,
  while completion pass@k plateaus after about k=20 (TGE:222). Grade:
  `single-source` (benchmark authors' own runs).

## Decision edge and limits

**Where amplification compute pays off.** The common pattern is a cheap
generator inside a strict execution filter. Raw generation is cheap but low
yield: about 4% of TestGen-LLM trials survive. The filters (build, repeat-pass,
coverage or mutant kill) are what make human review cheap enough for
acceptance near 73%. Tool feedback beats vanilla prompting: CoverUp's
loop and context tools nearly double coverage at about 5x the token cost of
plain prompting. Change awareness concentrates the yield: intent-aware JIT
tests produce weak catches about 30x more often per test than coincidental
failures, and Cleverest's commit message is worth roughly 5x the bugs of
undirected generation. Mutation guidance keeps tests that a coverage filter
would drop (277 of 571 in ACH).

**Where it is neutral or harmful.** Coverage gains are logarithmic in tests
generated, so later trials yield less (TG:323). Vanilla one-shot prompting
on a mature human suite adds almost nothing (TestGenEval: under 1% coverage
for a final test). Amplification compute pays only with execution feedback
and filtering, or where coverage is thin. Coverage-only prompting
inflates suite size without matching coverage (CU:1096). Hardening tests
almost never catch a later arbitrary diff (about 0.01 probability per test,
JIT:218), so pre-generating suites is a poor catch strategy. For catching
tests the bottleneck is false-positive triage rather than generation; that is
why assessors and the "is this change intended?" reach-out format dominate the
JIT design (JIT:246-252). Cleverest fails on strict binary formats (Poppler)
and on terse commit messages (Z3 "fix #N"), so intent-based generation needs
expressive change descriptions.

**Limits.** None of these papers compares an implementing agent's own tests
against a separate tester; every generator here is a separate tool run
after a human wrote the code. Meta acceptance rates are reviewer-cultural
(56% vs 89% across teams) and test-a-thon contexts are favourable. Most
metrics are coverage, kills or catches rather than field faults.
