# HarnessBank (v1 title: gated semantic quality-diversity) — pathology-keyed archive plus significance-gated screening

Read method: full read of the committed Markdown extract, 2026-09-25.
Full text: [HTML](https://arxiv.org/html/2607.13683) ·
[PDF](https://arxiv.org/pdf/2607.13683) ·
[local extract](../related-work/extract/gsqd2026/html/2607.13683.md).
arXiv 2607.13683. The extract is v2, titled "HarnessBank: Semantic
Gene-Bank Search with Gated Verification for Agent-Harness
Self-Evolution"; papers.yaml carries the older title "Self-Evolving Agent
Harnesses via Gated Semantic Quality-Diversity". Authors (v2 order): Luo,
Xue, Wang, Hu, Deng (EverMind AI, Shanda Group). No venue stated.

**What it is.** A task agent (frozen Qwen3.6-27B) plus a separate evolver
(Claude Opus 4.8). A MAP-Elites-style bank keyed by (where ∈ {prompt,
knowledge, runtime, config}) × (why = LLM-inferred failure pathology,
e.g. `thinking-runaway`); one elite per cell. The parent each round is
the train-best harness; offspring are reinvented from failure traces or
recombined across cells. Offspring pass four gates on a random training
subset — validity (infra failures retried), activation (a deterministic
beacon must fire at least once), paired significance (per-task paired
difference vs parent, z ≥ 1.96), gain — then are scored on the full
training set to compete for their cell. Stops at R rounds or P rounds
with no cell update; the train-argmax harness is scored once on a sealed
test split.

**Anti-overfitting mechanism.** No content/leakage check of any kind.
Protection is structural: (1) cells are keyed by pathology, not task ("an
archive keyed on tasks … overfits by construction"); (2) the paired z-gate
rejects gains indistinguishable from task-level noise; (3) the activation
gate rejects inert patches; (4) disjoint train/test splits with a single
final test comparison. Isolation: only the z-gate is ablated, on TB2 only
— removing it left the deployed harness and its test score **unchanged**
(train-argmax already picked the same one); it added 2–3 noise elites and
prevented the stop rule firing (phantom progress in 62–76% of
post-convergence rounds). The archive is argued from two anecdotes, not
ablated.

**Evidence and regime.** Seven domains: TB2, LiveCode, Omni-MATH,
BrowseComp+, GDPval, SWE-bench (the latter five via EvoAgentBench),
AppWorld. K=3 attempts; paired z on test; one evolution run per domain.
Test Pass@1 gains: TB2 +9.3, LiveCode +13.7, Omni-MATH +11.7, BrowseComp+
+13.9, GDPval +9.2, AppWorld +15.4 (z=6.44, n=168), SWE-bench +5.1
(n=26, z=0.78, not credited). Baselines GEPA and DGM are credited on 0
and 1 of five domains; DGM shipped a regression on Omni-MATH (−1.1).
Cross-model: pathology→patch "matching law" (Table 2): matched patch
+11 to +15.4, mismatched ≈ 0, and a Qwen-evolved "stop overthinking" fix
is harmful for Gemini (−1.5; −15.7 stacked). All `single-source`.

**Weaknesses.** Baselines use Qwen3.6-27B as their proposer while
HarnessBank uses Opus 4.8 as evolver — the method comparison confounds
search design with proposer strength. Test split sizes are unstated except
SWE-bench (26) and AppWorld (168). Vanilla train and test scores diverge
sharply (Omni-MATH 78.4 vs 54.3, GDPval 73.6 vs 43.7), so splits are not
exchangeable and "retention" ratios are uninterpretable (the authors
concede the ratio point). z ≥ 1.96 on a subset, repeated over many
offspring, has a sizable family-wise false-pass rate; the full-train
rescore mitigates but is not corrected. "Every gain clears 2σ" is stated
beside a SWE-bench result that does not. Most wins are one runtime
recovery for one model quirk (thinking runaway), so breadth across seven
domains is partly one mechanism seven times.

**Bearing on RRSI and on memorization.** It is the closest published
analog to RRSI's noise-band acceptance floor, and its own ablation says a
noise gate protects archive hygiene and stopping, not the deployed
result. The harness it finds is a model-pathology repair (recover after
runaway thinking, verify before finalizing), which by construction does
not encode task answers — so the paper shows what non-memorizing gains
look like more than it shows the gates preventing memorization. A second
lesson: "train selection is a lower bound" — on GDPval a lower-train
variant scored higher on test. Compared against GEPA and DGM, not RRSI,
HarnessCompass, or ModularRSI.

**Relation to a practitioner-maintained instruction corpus.** The
matching law is the strongest `single-source` support in this cluster for
routing model-specific content into model-scoped supplements and for a
two-model differential: the same symptom class calls for opposite
corrections in different families. The paired per-task z-test against the
parent is the formal version of the planned same-model rerun noise floor;
the activation beacon corresponds to verifying that an instruction was
actually consulted before crediting it. "Why" labels are hypotheses
whose credit comes only from the gate — the stance of pre-registered patch
hypotheses. Where HarnessBank can rescore on hundreds of tasks, an
incident-driven corpus has one incident per rule, so its gates would
rarely have power; that argues for batching incidents into recurring
pathologies before editing.
