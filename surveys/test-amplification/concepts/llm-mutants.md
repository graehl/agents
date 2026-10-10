# LLM-generated mutants: realism against validity and cost

> Read-backed digest (cluster B, trust `single-source`; one large
> comparative study. The extract is arXiv v5 (2025), and its headline numbers
> differ from earlier circulated versions).

**Paper.** Wang, Chen, Deng, Lin, Harman, Papadakis, Zhang, "A Comprehensive
Study on Large Language Models for Mutation Testing," ACM TOSEM (arXiv
2024; extract v5, 2025)
([arXiv](https://arxiv.org/abs/2406.09843),
[PDF](https://arxiv.org/pdf/2406.09843),
[local extract](../related-work/extract/wang2024-llm-mutation-study/html/2406.09843.md)).

## Method

The study compares four traditional generators with three LLM-based ones.
The traditional ones are PIT and Major, which apply fixed rules, and LEAM
and μBERT, which use small trained models. The LLM-based ones are BugFarm,
LLMorpheus ported to Java, and the authors' own few-shot prompt, LLMut. The
LLM approaches run on GPT-4o and DeepSeek-V3-671B, and LLMut also on five
other models (line 63).

The bugs are 851 real Java bugs: 605 from 12 Defects4J 2.0 projects and 246
ConDefects contest bugs collected after most of the models were released,
to limit training-data leakage (lines 41, 312). Every generator mutates the
*fixed* version, and only within the code surrounding each real bug,
1 to 3 lines. All generators get the same snippets (lines 222, 445, Table
15). This is mutation at a known fault site.

Metrics (lines 336-439):

- **Real bug detection rate:** the share of bugs for which some mutant is
  killed by the tests that reveal the real bug.
- **Ochiai similarity:** how closely a mutant's set of failing tests matches
  the bug's.
- **Coupling rate:** the share of mutants killed by bug-triggering tests.
- **Validity:** compilability, duplicates, and equivalence. Equivalence is
  judged manually on samples, with Cohen's \(\kappa = 0.8\).
- **Cost:** seconds and tokens per mutant.

## Evidence

Headline numbers from the abstract (line 41): LLM-based approaches detect
76.47% of real bugs against 44.15% for rule-based ones, an absolute gain of
32.99 points and 1.75x. They are worse on non-compilability, duplication
and equivalence by 32.73, 9.38 and 3.64 points. The per-tool rows of
Table 4 give a clearer picture (lines 459-475):

| Generator | Mutants | Real-bug detection | Coupling | Compiles | Duplicates | s/mutant |
|---|---|---|---|---|---|---|
| PIT | 340,728 | 40.1% | 23.5% | 100% | 0.0% | 0.02 |
| Major | 20,831 | 66.9% | 38.9% | 97% | 0.0% | 0.08 |
| LEAM | 36,505 | 63.9% | 38.1% | 44.5% | 2.3% | 3.06 |
| LLMorpheus (DS-671b) | 21,356 | 69.3% | 52.0% | 68.1% | 6.9% | 5.44 |
| LLMut (GPT-4o) | 31,945 | 89.9% | 50.6% | 76.4% | 7.8% | 1.31 |
| LLMut (DS-671b) | 33,596 | 91.1% | 50.8% | 77.6% | 7.5% | 2.57 |
| LLMut (StarChat-16b) | 28,058 | 38.5% | 34.0% | 16.4% | 12.8% | 7.53 |

- **Equal mutant counts.** When every generator is subsampled to 11,397
  mutants, LLMut (DS-671b) still detects 89.2% of bugs, against 68.8% for
  Major and 31.6% for PIT. LLMorpheus has the highest coupling rate, 51.3%
  (Table 18, lines 1170-1192).
- **Equivalent mutants.** The manually estimated equivalent-mutant rate is
  1.0% for PIT and 2.1% for Major. For GPT-4o and DeepSeek-class LLM
  approaches it is 3.1-6.3%, and 10.6% for the weakest model (Table 10,
  lines 698-716).
- **Token cost.** LLMut uses about 126 input and 58-63 output tokens per
  mutant. BugFarm returns whole methods and uses about 366 output tokens
  (Table 11, lines 734-752).
- **Why mutants survive.** For PIT and Major, about 46% of surviving
  non-equivalent mutants are on code no test covers. For LLMut and BugFarm
  it is 54-80% (Table 13, lines 905-926). So LLM mutants survive more
  because their sites are uncovered, and less often because a covered
  change escapes the test oracle.
- **Training-data leakage.** Exact syntactic matches with the real fixes
  occur for every tool. LEAM has the most on Defects4J (287), and Major has
  92 on ConDefects (line 1324). Leakage is a confound for all tools, not
  only for the LLMs.

## Decision edge and limits

Per mutant, LLM generation buys realism: the share of bugs it reproduces
rises about 20 points over Major when counts are matched. It costs
16-113x more generation time per mutant than Major (1.31-9.06 s against
0.08 s). Even with the strongest models, 22-24% of its mutants do not
compile. Those still pay
for a build attempt before they can be thrown away.

This favours LLM mutants where the mutant budget is small and placement is
already narrow. That is framing (a), mutating only a diff or a suspected
fault region, which is exactly the regime evaluated here: 1-3 lines around
a known bug. Rule-based generators stay ahead where volume, guaranteed
compilation and low equivalence matter. Bulk whole-program mutation
(framing c) is the clearest case: a 0.02 s/mutant generator with 100%
compilability is hard to beat when the cost is in test execution.

The high share of uncovered surviving LLM mutants means a coverage filter
before execution, as in [predictive-mutation](predictive-mutation.md) and
[targeted-mutation](targeted-mutation.md), would remove much of the extra
LLM output cheaply. Free-form LLM edits do not have a fixed set of mutation
operators, so the per-operator suppression rules Google uses do not carry
over directly. The study does not evaluate schemata, split-stream or other
batched execution of LLM mutants (framing b).

Limits. Java only. The evaluation assumes a clean program, because it
mutates fixed versions (line 1326). Each real bug is detected or not by "at
least one mutant at the bug site", which rewards generators that produce
many varied mutants. Subsuming-mutant analysis is listed as future work
(line 1310). I could not reproduce the abstract's pooled 44.15% and 76.47%
by simple averaging of Table 4's rows; use the per-tool rows for
comparisons.
