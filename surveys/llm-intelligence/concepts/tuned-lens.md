# tuned-lens — a trained per-layer lens for latent predictions

> Read-backed digest (cluster B3, trust `benchmark-reported`). Read 2026-07-31
> from `related-work/extract/belrose2023-tuned-lens/`. Part of the
> [J-space lineage](../survey.md); the correlational refinement J-lens improves on.

**Paper.** "Eliciting Latent Predictions from Transformers with the Tuned Lens,"
Belrose, Furman, Smith, Halawi, Ostrovsky, McKinney, Biderman, Steinhardt, 2023
(arXiv 2303.08112). Code: github.com/AlignmentResearch/tuned-lens.

## What it is

For each layer ℓ, train an **affine map** (a "translator") so that
`unembed(translator(h_ℓ))` matches the model's *final* logits, under a
distillation loss. Composed with `W_U` this is a probe from any hidden state to a
vocabulary distribution. The translators correct for **representational drift** —
the fact that a concept's direction changes basis across layers — which is
exactly what the logit lens ignores.

## Key results

Tested on autoregressive LMs up to **20B params**: more **predictive, reliable,
and unbiased** than the logit lens (lower per-layer perplexity across model
families). Where the logit lens fails to produce interpretable predictions
before ~layer 21 (GPT-Neo-2.7B), the tuned lens succeeds. **Causal** experiments
show the tuned lens uses features similar to the model's own. The per-layer
**prediction trajectory** also detects anomalous/"malicious" inputs with high
accuracy.

## Anchor edge (how it feeds J-space)

The nearest predecessor the anchor positions J-lens against. The tuned lens is
trained to match the **output** distribution — a *correlational* objective — so
on prompts involving unverbalized intermediate computation it tends to
**"skip ahead"** to the final token rather than surface the intermediate concept
in play. J-lens instead uses a **mean Jacobian** (analytic, not a trained
predictor); the anchor states this choice is *empirically important* to its
results, because the Jacobian surfaces the latent intermediate the tuned lens
jumps past. Same "correct the logit lens per layer" goal, opposite (causal vs
correlational) construction.

## Limits

Correlational (predicts the output, not the intermediate); requires training a
translator per layer per model; inherits the single-vocabulary readout ceiling.
Grade capped at `single-source` in the survey pending an independent re-check.
