# RRSI — regularized recursive self-improvement of agent harnesses

Read method: full read of the committed Markdown extract, 2026-09-25.
Full text: [HTML](https://arxiv.org/html/2609.24972v2) ·
[PDF](https://arxiv.org/pdf/2609.24972) ·
[code](https://github.com/google-research/rrsi) ·
[local extract](../related-work/extract/rrsi2026/html/2609.24972.md).
arXiv 2609.24972 (v1 2026-09-21, v2 2026-09-23); Google Cloud AI Research
with Stanford, WashU, and UNC authors.

**What it is.** A generic harness-evolution loop, in which a proposer LLM
edits the harness from evolve-set feedback and a selector keeps the best
candidate, plus six constraints the authors call regularizers. The edit
space stays open: prompt, control flow, config, output plumbing, context
management, tools, skills, memory, and subagents.

- *Proposal side.* An edit-count budget per candidate, annealed on a cosine
  schedule from 3–4 edits down to 1 (called "L0-style"). An edit history of
  component, hypothesis, diff, ΔS, ΔC, and accepted/rejected goes back to
  the proposer. When progress stalls for w=3 rounds within the noise band,
  exploration slots are reserved for components that have not yet been
  exercised.
- *Selection side.* An LLM **leakage critic** reads each diff before
  evaluation and rejects task names, entity names, task-specific values,
  answers, and inert machinery. A **noise-band floor** comes from
  repeated runs of the base harness: a candidate needs Ŝ ≥ S* − δ. A
  cost rule requires ΔC ≤ β0 + β1·ΔS when ΔS > δ; inside the band a
  shaped rule credits lower cost and never-before-accepted *structural*
  component types. **Pruning** marks components that have had no positive
  measured gain over a 4–5-round window as deletion targets. The paper
  states that the L0/L1/L2 names are only analogies.

**Evidence and regime.** The frozen policy is Claude Opus 4.8, and the
same model serves as proposer, analyst, and critic. Setup per domain:

- *Evolve suites:* Terminal-Bench 2.1 (89 tasks, k=2), the 120-task Harvey
  LAB evolve split (k=2, ~14k rubric criteria judged by Gemini-3.5-Flash),
  and EngDesign (61 tasks, k=4, simulator-graded, no held-out split).
- *Transfer suites:* SWE-bench Verified; a 40-task Harvey held-out split;
  JobBench, GDPval, and APEX-Agents; Frontier-Eng (38 of 47 tasks
  scorable, with the domain that overlaps EngDesign excluded).
- *Baselines:* Meta-Harness, AHE, TTHE, and HarnessX, all started from the
  same H0 with the same candidate budget.
- *Uncertainty:* none reported. There is apparently one evolution run per
  arm, with no seeds, CIs, or run-to-run spread for the *search*; δ sizes
  only per-evaluation noise.

**Reported results** (`single-source`):

- *Workspace (Table 1).* RRSI has the smallest evolve gain (90.5 vs H0
  89.4; Meta-Harness 93.0) but the best OOD average (43.6 vs H0 39.7;
  Meta-Harness 40.6). AHE and TTHE end *below* H0 out of distribution.
- *Ablation (Table 2).* Unregularized evolution gets evolve 92.8 but OOD
  40.3 (+0.6 over H0) at 3.80M tokens per trial, against RRSI's 2.42M and
  H0's 1.56M. Removing the proposal-side group gives 41.9 OOD; removing
  the acceptance-side group gives 41.0. The critic, floor, cost rule,
  pruning, and exploration are **never ablated individually**.
- *Coding.* Terminal-Bench +6.0 transfers +1.8 to SWE-bench Verified under
  Opus 4.8. Under Gemini 3.5 Flash the numbers are +14.1 and +2.2. The
  Gemini-evolved harness gives +3.4 on Terminal-Bench (the evolve suite
  itself) when run under the unseen Gemini 3.1 Flash Lite.
- *Hyperparameters.* Stated as tuned without consulting held-out or OOD
  data.

**Bearing on memorization.** Only the leakage critic targets memorization
directly, and it catches *explicit* leakage: names, values, and answers
in the diff. Fitting to the evolve *distribution* through general-looking
prose passes it by design. Examples would be deliverable-format habits
that a particular rubric rewards, or judge-pleasing style. The other
five constraints control capacity (edits per round), noise-chasing, and
cost growth. Those are real generalization levers, but they are not
memorization screens. Four features weaken the transfer claim:

- *Selection reuses the feedback set.* The evolve set drives both proposal
  feedback and selection. The paper cites Dwork et al.'s reusable holdout
  but does not implement a separate selection split or Thresholdout-style
  noising.
- *Shared judge.* Harvey (evolve) and APEX (OOD) are both judged by
  Gemini-3.5-Flash, and JobBench averages Gemini with Opus. A harness that
  learns judge-preferred style can therefore "transfer" in the workspace
  domain. The simulator-graded engineering domain answers this only for
  engineering, and there the whole OOD evidence is Frontier-Eng on 38
  tasks.
- *Held-out beats evolve.* On Harvey, the held-out gain (+2.3) and the OOD
  gain (+3.9 average) both exceed the evolve gain (+1.1). A causal
  story is needed; plausible ones are generic deliverable completeness,
  judge style, or chance.
- *Loose writing.* §4.3 calls the edit budget "L1-style" (it is L0), and
  the introduction repeats a sentence. The mechanisms are ordinary
  engineering hygiene under regularization branding.

**Relation to a practitioner-maintained instruction corpus.** The
selection-side ideas map onto rules this repo already states but has not
measured:

| RRSI mechanism | This repo's counterpart | Status |
|---|---|---|
| Cost rule | Protected-token burden priced against reliability ([`AGENTS.md`](../../../AGENTS.md) § Design objective) | Stated, unmeasured |
| Pruning | Leave-one-out culling ([`instruction-ablation`](../../../topics/instruction-ablation.md)) | Unrun |
| Noise floor | A/A replay; same-producer rerun floor ([proposal](../../../research/differential-instruction-diagnosis/proposal.md)) | Unrun |
| Leakage critic | "One cheap retry need not buy a permanent paragraph" ([`agent-instructions`](../../../topics/agent-instructions.md) § Verifying instruction changes) | Stated |

The repo's planned guidance-evolution design is stricter than RRSI on
search/confirmation separation: it uses separate feedback, selection, and
sealed-confirmation pools, with shuffled-feedback and growth-ratchet
control arms ([sketch](../../../topics/instruction-ablation.sketches.md)
§ Separation of search from confirmation).
