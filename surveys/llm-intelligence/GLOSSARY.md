# Glossary — surveys/llm-intelligence

Survey-scoped vocabulary. Applies by path to every doc under
`surveys/llm-intelligence/` (survey.md, `concepts/*`, related-work notes) —
the same governing rule as a research program's `GLOSSARY.md`. General
contribution/regeneration rules: [`~/agents/topics/glossary.md`](../../topics/glossary.md).
Node refs point into [`survey.md`](survey.md).

| term | definition | ref |
|---|---|---|
| J-space | The workspace object: points expressible as sparse nonnegative combinations of J-lens vectors (~10–25 active/position, overcomplete, <10% of activation variance, middle layers). The anchor concept | ANCHOR |
| J-lens | Averaged-Jacobian causal lens, `E[∂h_final/∂h_ℓ]`, mapping an activation to the vocabulary tokens it is *disposed to make the model say*. Causal, unlike the (correlational) logit/tuned lens | ANCHOR |
| verbalizable representation | Content the model *could* report as a token — a J-space/J-lens vector — whether or not it is actually emitted | ANCHOR |
| global workspace (GWT) | Neuroscience import (Baars; Dehaene): a limited-capacity workspace broadcasts selected content to many consumers = conscious *access*. Used as a functional template, not an architecture claim | F2 |
| access vs phenomenal | Access = functional, reportable, broadcast (what the survey studies); phenomenal = subjective experience (Block 1995). The anchor takes no position on phenomenal | F2 |
| superposition | With sparsity, a model packs more features than dimensions as an overcomplete set of near-orthogonal directions | A2 |
| feature (interpretability) | A direction in activation space encoding a concept; the unit lenses/probes/SAEs read | A |
| dictionary learning / SAE | Sparse autoencoder extraction of interpretable features; *reconstructive / input-side* — contrast J-lens (causal / output-side) | A3 |
| logit lens | Unembedding matrix applied to an intermediate residual stream; correlational readout, brittle in early layers | B2 |
| tuned lens | Per-layer learned affine lens to logits; more predictive/reliable than logit lens, still correlational | B3 |
| steering vector / ActAdd | `h ← h + αv`: add a scaled direction to steer behavior (Turner et al. 2023). The causal intervention the anchor's tests use | C1 |
| representation engineering (RepE) | Top-down reading/control vectors from contrastive prompt sets (Zou et al. 2023) | C2 |
| residual stream | The shared linear channel attention/MLP heads read from and write to; where lensable/steerable directions live | D1 |
| attribution graph | Causal input→intermediate→output pathway map over CLT features (Anthropic 2025); causal-interp sibling of J-lens | D2 |
| cross-layer transcoder (CLT) | Sparse interpretable-feature replacement for MLP activations; the nodes of an attribution graph | D2 |
| chain-of-thought (CoT) | Verbalized step-by-step reasoning (the "motor"/written side), vs the latent workspace | E1 |
| CoT (un)faithfulness | The written CoT need not be the *cause* of the answer; said ≠ used reasoning (Turpin 2023; Lanham 2023) | E2 |
| concept-injection introspection | Inject a known concept's representation into activations, measure its effect on self-report (Anthropic 2025); the anchor's protocol precursor | F1 |
| short handle | Our per-concept name and file/link key (e.g. `j-space`); may only vaguely resemble the paper title | survey policy |
| `[G]` / `[R]` | Node grounding tag: grounded (source fetched/read) vs recall-pending (verify on a grounded pass) | banner |
| seed set | The anchor(s) whose backward citation chains define the survey's declared scope | seed section |
