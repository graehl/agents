# Rethinking the Evaluation of Harness Evolution — matched-budget and held-out audit

Read method: full read of the committed Markdown extract, 2026-09-25.
Full text: [HTML](https://arxiv.org/html/2607.12227) ·
[PDF](https://arxiv.org/pdf/2607.12227) ·
[local extract](../related-work/extract/rethinkhe2026/html/2607.12227.md).
arXiv 2607.12227 (extract is v2). Wang, Zhu, Hu, Yuan, Chen, Senthil,
Hajishirzi, Tsvetkov, Dasigi, Xiao (AI2 / UW).

**What it is.** An evaluation critique, not a new evolver. It argues that
harness evolution is itself iterative search with verifier feedback, so it
must be compared with test-time scaling (TTS) given the same feedback and
rollout budget, and that evolving and reporting on the same benchmark
invites overfitting. Four arms share a budget of K=5 rollouts per task:
parallel sampling, sequential refinement, harness evolution (AHE,
arXiv 2604.25850, with its benchmark-harness-retrieving explore agent
disabled; m=1 rollout per task per round), and "harness scaling" (a
per-instance harness rewrite, i.e. TTS wearing harness clothes).

**Evidence and regime.** Terminal-Bench 2.1 (89 tasks; 28 repaired vs
2.0). Claude Opus 4.6, GPT-5.4, GPT-5.4 mini (mini only in the no-tests
table); the same model plays policy, debugger, and meta-agent. Seed
harness: one bash tool. Every number is the mean of two independent runs.
No CIs, no significance tests, no per-run spread. The held-out study uses
a single random 45/10/34 train/val/test split and only two models.

**Generalization / anti-overfitting findings** (all `single-source`).
- No unit tests, pass@1 averaged over three models: direct 68.2; parallel
  sampling with self-judge 72.3; sequential refinement 69.3; harness
  evolution 67.4 (below direct; GPT-5.4 75.3→69.7); harness scaling 71.8.
- With unit tests, averaged over Opus/GPT-5.4: direct 72.9; harness
  evolution pass@1 75.8 / pass@5 86.2; parallel sampling 86.0; sequential
  refinement pass@5 91.8; harness scaling 82.6 / 89.3. The authors conclude
  that evolution's benefit shows up only when several attempts can be
  selected, so its gain is repeated attempts rather than a better harness.
- On the disjoint split (evolve on 45, select on 10, test on 34), the gain
  is Opus 63.3→64.5 (+1.2), GPT-5.4 72.1→72.1 (+0.0), average +0.6. With
  68 rollouts per cell, +1.2 is about one rollout.
- Edit audit: harness evolution adds sensible rules (budget awareness,
  finalization gates, output truncation). Harness scaling mostly writes
  task-specific facts: file paths, command sequences, known bugs, and
  verifier-mimicking checks. The authors summarize: "most edits memorize
  fixes rather than distilling strategies." The hard-failure core stays
  unsolved, and accumulated prompt text adds context bloat.
- They suggest Terminal-Bench may be harness-insensitive: a shell plus a
  basic prompt already solves most of what the model can solve.

**Bearing on RRSI and on memorization.** This paper supports the user's
suspicion more than any other audit here, with one caveat. The
held-out null comes from edits that were *generic* rules, not leaked task
entities. Blocking task-entity names, as RRSI's leakage critic does, would
not have changed that result. Overfitting here means selecting on a small,
noisy, harness-insensitive signal, not only memorizing named facts. For
RRSI the paper asks for two missing controls: (1) a matched-compute TTS arm
(parallel sampling or refinement on the evaluation suites themselves), and
(2) the unregularized evolver's held-out score with run-to-run spread, so
that a "regularized > unregularized" held-out gap can be compared with
noise. A discriminating test would use several evolution seeds per arm,
held-out deltas with CIs, and ablations of each RRSI regularizer. If the
leakage critic's held-out effect is indistinguishable from zero while the
noise-band floor carries the gain, the benefit comes from better
selection, not from preventing memorization.

**Methodological weaknesses.** Evolution budget is tiny (K=5, m=1), far
below published Meta-Harness/AHE runs, so "does not beat TTS" may not
carry to long searches. The "pass@1" label under oracle selection for the
TTS arms is really best-of-K, so it is not comparable to the evolved
harness's single-rollout pass@1. The GPT-5.4 direct baseline differs between
Table 1 (75.3) and Table 2 (75.9). The claimed "sharp contrast" between
in-sample and held-out gains is small: +2.9 in-sample pass@1 against
+0.6 held-out, both plausibly within two-run noise on this many tasks.
There is one benchmark, one evolver, and one split.

**Relation to a practitioner-maintained instruction corpus.** The corpus
is edited from observed incidents, which makes it "harness scaling" across
sessions, the exact regime where this paper sees task-specific fact
memorization. The corpus's defense is structural: the evidence ledger
records the incident class, and a rule must name a failure class, not a
path or command. The paper's null result is a warning for the planned
ablation. On a harness-insensitive task mix, removing rules may show no
effect whether or not they are useful. The ablation needs tasks where the
rules' target failures actually recur, and a same-model rerun noise floor
estimated before any delta is read (two runs is what this paper had, and
it could not separate +1.2 from zero).
