# HarnessCompass — gated, feedback-enriched, two-track harness evolution

Read method: full read of the committed Markdown extract, 2026-09-25.
Full text: [HTML](https://arxiv.org/html/2608.01918) ·
[PDF](https://arxiv.org/pdf/2608.01918) ·
[local extract](../related-work/extract/harnesscompass2026/html/2608.01918.md).
arXiv 2608.01918 (v1; no venue stated). Zhang, Zhou, Song, et al. (12
authors; Beijing Institute of Technology, CityU Hong Kong).

**What it is.** An AHE-style evaluate→analyze→improve loop over a coding
harness (seven component types from AHE), started from a bash-only seed,
with three additions: (1) a *generalization gate* in the meta-agent's
system prompt; (2) *proactive feedback* — the task model gives a blind
(verdict-withheld) and a hindsight report on harness friction, reconciled
and then kept only if an analyzer finds trajectory support; (3) two
parallel tracks per round (structural code vs guidance text), winner by
sample Pass@1, loser's edits salvaged by an LLM "R3" merge
(revise/recombine/refine, deleting advisory text that duplicates a
deterministic mechanism). Accept if winner beats the previous round.

**Anti-overfitting mechanism.** Content rule, not data split: the gate
bans task ids, test names, private symbols/paths of the task-under-test,
keyword-matching code branches, and "iteration N showed task X" recitals;
every retained lesson must carry an applicability criterion ("would this
help a library I have never seen?"). Memory entries must be merged into a
single deciding criterion when they conflict and pruned each round. It is
enforced only by prompting the same model that writes the edit — no
separate critic, no automatic check. Selection uses the 50-task evolution
set itself (no inner validation split). Isolation: the ablation is
cumulative (seed → +gate → +feedback → +R3); there is no
full-system-minus-gate row. The closest gate ablation is "+gate" (AHE
loop plus gate, per "holding the loop fixed") vs AHE: held-out 58.4 vs
54.7. Appendix C gives a qualitative ungated-vs-gated memory comparison:
ungated memory holds recipes naming `django__django-13158` and
`Vector.__add__` (answer keys); gated memory holds conditional rules.

**Evidence and regime.** SWE-bench Verified only; random 50-task
evolution set, 450 held-out tasks. GPT-5.4 (non-thinking) for every role;
cross-model eval on Claude Sonnet 4.6 with the harness frozen. k=2
rollouts per task; one evolution run per arm; no CIs, seeds, or
significance tests. Headline (Pass@1): seed 54.0/51.6 (sample/held-out),
AHE 63.0/54.7 at 20 turns, HarnessCompass 66.0/60.4 at 5 turns. Ablation
held-out: +gate 58.4 (2 turns), +feedback 55.8 (12 turns; sample rises to
66.0), +R3 60.4. Sonnet 4.6 transfer: 70.0→73.8 total, uneven by repo
(astropy +18.1, pytest −10.5, sphinx −4.5). All `single-source`.

**Weaknesses.** Sample Pass@1 is both the acceptance criterion and a
reported column (winner's curse); sample differences (66 vs 63) are 3
tasks on 50. Held-out 5.7 pp over AHE at n=450, k=2 is likely beyond
evaluation noise but not beyond evolution-run variance, which is
unmeasured (one run). AHE reproduced in-house. Turn count to "reach" a
peak is read off a single noisy curve. SWE-bench Verified is a
contamination-prone public set; the held-out split shares repos with the
evolution split, so "held-out" is in-distribution. Reference list cites
Sonnet 4.5 and the GPT-5 card for Sonnet 4.6 / GPT-5.4.

**Bearing on RRSI and on memorization.** Its gate is the prompt-level
cousin of RRSI's leakage critic (RRSI adds a separate critic call). The
cumulative ablation supports the user's suspicion from an unexpected side:
the one component that *enriches* evidence (first-person feedback) cut
held-out by 2.6 pp while raising sample score — richer per-task evidence
is a memorization channel even under the gate. R3's recovery is not
explained mechanistically. Appendix C shows that the gate changes *what
the artifact looks like*; it does not show that the gate removes
task-specific benefit, since abstractly phrased rules can still be
derived from and fitted to 50 tasks. It does not compare against RRSI,
GSQD/HarnessBank, or ModularRSI.

**Relation to a practitioner-maintained instruction corpus.** The gate
prompt restates this repo's authoring discipline almost verbatim: global
rules with a trigger/applicability condition, no incident-specific
recitals in instruction text, merge contradictions into one deciding
criterion, prune. The repo keeps incident specifics in the append-only
evidence ledger instead of the rule text, which is the same separation
Appendix C argues for. The blind/hindsight self-report, grounded against
the trace, is published precedent for producer-side introspective
evidence in the planned differential diagnosis — with the caution above
that it was the overfitting-prone component. The uneven Sonnet transfer
(`single-source`) is weak support for model-scoped supplements over a
single shared corpus. Nothing here resembles a same-model rerun noise
floor or pre-registered patch hypotheses (manifests carry
`predicted_fixes`, inherited from AHE, but no outcome audit is reported).
