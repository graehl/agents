# Meta-Harness — end-to-end search over harness code with full-history access

Read method: full read of the saved source HTML (converted locally; committed
extract pending a fidelity-gate failure), 2026-09-25.
Full text: [HTML](https://arxiv.org/html/2603.28052) ·
[PDF](https://arxiv.org/pdf/2603.28052) ·
[saved HTML](../related-work/extract/metaharness2026/html/2603.28052.html).
arXiv 2603.28052v1 (cs.AI, 30 Mar 2026). Lee, Nair, Zhang, K. Lee, Khattab,
Finn (Stanford / KRAFTON / MIT). Preprint; no venue stated.

**What it is.** An outer loop in which a coding-agent proposer (Claude Code,
Opus 4.6) writes whole single-file Python harnesses (prompting, retrieval,
memory, orchestration) and reads a growing filesystem of every prior
candidate's source, scores, and raw execution traces via grep/cat. No
parent-selection rule, no mutation operators; a Pareto frontier is kept and
the final frontier is scored on test. A typical run is ~60 harnesses over 20
iterations; the proposer reads a median of 82 files per iteration (41% code,
40% traces), up to ~10M tokens of diagnostic context per evaluation.

**Anti-overfitting / generalization evidence.** The only structural guard is
the split: the proposer sees search-set results only, never test results.
The paper asserts that code-space search is "a natural regularization bias"
(coding models propose coherent algorithms, not hard-coded solutions) and
that code overfitting is "more inspectable" — asserted, not measured. The
TerminalBench-2 run searches and evaluates on the *same* 89 tasks (framed as
a "discovery problem"); the overfitting check there is manual inspection
plus a regex audit for task-specific string leakage. Transfer evidence: (a)
text classification discovered on 3 datasets, evaluated on 9 unseen
datasets (OOD avg 73.1 vs ACE 70.2, best on 6/9, worse than ACE on FiNER
67.0 vs 74.0); (b) one math-retrieval harness selected on GPT-OSS-20B, run on
4 unseen models. Interface ablation (Table 3): scores-only 34.6 median / 41.3
best, scores+summary 34.9 / 38.7, full traces 50.0 / 56.7 — about
proposer information, not about generalization.

**Evidence and regime.**
- Text classification (GPT-OSS-120B executor; LawBench, Symptom2Disease,
  USPTO-50k; 40 candidates): 48.6 avg vs ACE 40.9 (+7.7), MCE 40.0, at
  11.4K vs 50.8K context. Search sets 50–100 examples.
- Versus text optimizers at equal evaluation budget: median/best GEPA
  32.6/40.2, Best-of-N 34.0/44.2, OpenEvolve 39.1/43.3, TTT-Discover
  34.1/45.6, Meta-Harness 50.0/56.7.
- Math retrieval (250-problem search set, 109 candidates, 535K-problem
  decontaminated corpus): 200 IMO-level problems, 3 samples per problem,
  avg 38.8 vs no-retrieval 34.1 (+4.7) but only +1.3 over plain BM25 (37.5).
- TerminalBench-2: Opus 4.6 76.4% vs Terminus-KIRA 74.7% (+1.7 pp, about
  1.5 tasks of 89); Haiku 4.5 37.6% vs KIRA 33.7%, Goose 35.5%. Wins on 7/89
  tasks; the winning edit is an ~80-line environment-snapshot bootstrap.
  During search the KIRA baseline scored 64.4%, not 74.7%, so run-to-run or
  configuration variance is at least the size of the claimed gain.
- One search run per setting; no seeds, CIs, or repeated searches; baseline
  numbers partly taken from the leaderboard. Grade: `single-source`.

**Bearing on RRSI and on memorization.** Meta-Harness is the natural
"unregularized" baseline that RRSI regularizes: full per-item traces, no edit
budget, no leakage filter, no noise floor, and on TerminalBench-2 no
held-out split at all. RRSI's report that it is strongest on the evolve split
and weak OOD is consistent with that design. The Delta-Attribution blog
([delta-attribution](delta-attribution.md)) reruns this framework and finds
that the coding proposer *does* write hard-coded controllers (ALFWorld
zero-LLM lookup tables, LiveMath answer-phrase matching). That contradicts
the "code-space regularization" claim. Its own qualitative log shows the
proposer isolating a confounded prompt edit and then adopting an additive,
task-agnostic mechanism (the environment bootstrap). That is one plausible
reusable mechanism, but it rests on a +1.7 pp single-run gain.

**Relation to a practitioner-maintained instruction corpus.** Same loop
shape (read traces, diagnose, edit the text/code around a fixed model), but
the unit of change is a whole rewritten program selected by aggregate score.
There is no per-edit hypothesis, no clause-level attribution, and no ledger
beyond the filesystem. Two points transfer. (1) The confound episode, where
two regressions share one prompt rewrite, is the single-clause attribution
problem the repo's differential protocol targets. Meta-Harness resolves it
informally inside the proposer; the repo wants it resolved by pre-registered
reruns. (2) Appendix D's "iterating on the skill text had a larger effect
than iteration count" shows that the proposer's own instruction file is a
dominant, unablated variable. That is the same object this repo maintains
by hand.
