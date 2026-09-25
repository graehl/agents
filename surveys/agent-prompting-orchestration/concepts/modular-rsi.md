# ModularRSI — benchmark-disjoint, contrastive, module-scoped harness evolution

Read method: full read of the committed Markdown extract, 2026-09-25.
Full text: [HTML](https://arxiv.org/html/2609.14857) ·
[PDF](https://arxiv.org/pdf/2609.14857) ·
[code](https://github.com/IQuestLab/ModularRSI) ·
[local extract](../related-work/extract/modularrsi2026/html/2609.14857.md).
arXiv 2609.14857 (v1; no venue stated). Wu, Ren, Li, et al. (14 authors;
Manchester, IQuest Research, Beihang, M-A-P, Langboat, Hohai).

**What it is.** Terminus-2 (Harbor) refactored into five modules — Agent
Loop, Tool Use, Observation Management, Context Management, Task
Completion Detection — each evolved independently for three epochs, then
merged by one cross-module "integration run-in" epoch. Tasks are rolled
out K times and bucketed: mixed pass/fail (contrastive: diff a passing and
failing rollout of the same task), all-fail (pair with a historical
success from trajectory memory, else one-sided diagnosis), all-pass
(efficiency). Findings are clustered and ranked by the number of distinct
tasks supporting them; a per-function evolution history is shown to the
editor. Gates: static program checks, an LLM diff review, and a 2-task
smoke run. An LLM composer activates a task-relevant subset of evolved
functions at run time. The agent under evolution is also the editor.

**Anti-overfitting mechanism.** Primarily a data split: 2,000 executable
tasks curated from external sources (GitHub, Hugging Face, Kaggle, kernel
docs), guided only by benchmark *category* labels, filtered by LLM
semantic-similarity screening against the eval benchmarks; 120 TB-related
or 120 SWE-related tasks are used per run. Evaluation is on TB2 and
SWE-bench Verified, so memorizing evolution tasks cannot directly inflate
the reported score. Secondary: cross-task vote ranking; module-restricted
scope; a reward-blind diff review (same model, self-review) that rejects
task names, task-specific files/outputs, and constants tuned to one task —
RRSI's leakage critic in all but name. Isolation: modular vs non-modular
vs joint evolution is ablated (TB2 only); the diff review, vote ranking,
and contrastive analysis are **not** ablated (the paper says so for the
last).

**Evidence and regime.** DeepSeek-V4-Flash (Preview; 0731 for the
baseline comparison). K=3 rollouts, one evolution run per arm, no CIs or
significance tests. TB2 (89 tasks) Acc: 47.57 → 52.43 in-domain (≈13 of
267 trials), SWE-evolved → 49.40 out-of-domain (Pass^3 unchanged at
30.34). SWE-bench Verified: 73.40 → 76.45 in-domain, 75.80 from
TB-evolved. Non-modular 46.44 and joint 44.19 fall below baseline;
single-module variants 49.4–50.6. Frozen-harness transfer on TB2:
GLM-5.2 +2.25, MiniMax-2.5 +3.37. Versus reproduced baselines under the
disjoint protocol (baseline 61.79): Meta-Harness 62.92, AHE 62.54,
ModularRSI 67.42. All `single-source`.

**Weaknesses.** Test-set selection: the Medium-centered difficulty
distribution is chosen by its SWE-bench Verified score (76.45 vs 74.25),
and that configuration is the reported headline; Appendix F tracks every
generation on TB2. At 89 tasks a 2–5 pp difference is within plausible
evaluation noise, and evolution-run variance is unmeasured. Baselines are
in-house adaptations run for 16 epochs on 120 tasks — a regime unlike
their papers'. The diff reviewer is the author of the diff. The
out-of-domain SWE→TB2 result is close to null. Benchmark-category
guidance for curation is deliberate distribution-level transfer.

**Bearing on RRSI and on memorization.** This is the design that most
directly answers the memorization worry, and it answers it by
measurement, not prevention: evolution tasks never overlap evaluation, so
whatever is memorized is simply not rewarded. RRSI evolves and evaluates
on different suites too; ModularRSI's addition is an external evolution
pool instead of a benchmark subset. Its striking side result is that
AHE and Meta-Harness gain ≈1 pp once benchmark data is withheld — a
`single-source` hint that much reported harness-evolution gain is
benchmark adaptation. It cites HarnessBank (as non-disjoint) and
"Rethinking the Evaluation of Harness Evolution"; it does not cite or
compare HarnessCompass or RRSI.

**Relation to a practitioner-maintained instruction corpus.** Its
contrastive pairs are same-model reruns with differing outcomes — the
planned same-model noise-floor reruns double as a source of such pairs
rather than only a variance estimate; the planned two-model differential
is the cross-model analog. Vote ranking by distinct supporting tasks
matches requiring a pattern to recur across incidents before a rule is
written. Its per-function evolution history plays the role of the
append-only evidence ledger (both expose prior edits to prevent
oscillation). The composer that activates task-relevant functions is the
analog of trigger-scoped instruction routing. Self-review by the editing
model is the weakest part, and it is the same weakness as a practitioner
reviewing their own rule.
