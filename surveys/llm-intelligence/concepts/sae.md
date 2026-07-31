# sae — sparse dictionary learning of features

> Read-backed digest (cluster A3, trust `contested`→capped `single-source`).
> Read 2026-07-31 from `related-work/extract/bricken2023-monosemanticity/` and
> `.../templeton2024-scaling-mono/` (transformer-circuits HTML); Cunningham 2023
> from its abstract + the anchor's citations. Part of the
> [J-space lineage](../survey.md); the sparse-overcomplete sibling of J-space.

**Papers.**
- Bricken et al. (Anthropic), "Towards Monosemanticity: Decomposing Language
  Models With Dictionary Learning," transformer-circuits.pub, 2023.
- Cunningham, Ewart, Smith, Huben, "Sparse Autoencoders Find Highly Interpretable
  Model Directions," 2023 (arXiv 2309.08600) — concurrent, same core idea.
- Templeton et al. (Anthropic), "Scaling Monosemanticity: Extracting Interpretable
  Features from Claude 3 Sonnet," transformer-circuits.pub, 2024.

**Full text:** Bricken → [Towards Monosemanticity](https://transformer-circuits.pub/2023/monosemantic-features/index.html) · Cunningham → [PDF](https://arxiv.org/pdf/2309.08600) (no arXiv HTML view) · Templeton → [Scaling Monosemanticity](https://transformer-circuits.pub/2024/scaling-monosemanticity/index.html).

## What it is

Train an **overcomplete sparse autoencoder (SAE)** on a model's activations: an
encoder maps an activation to a high-dimensional, **sparse, nonnegative** code,
and a decoder reconstructs the activation from it. Because superposition packs
many features into few dimensions, the SAE's job is to **un-mix** them — each
sparse code entry is a candidate **monosemantic feature** (a single
human-interpretable concept), read off via its top-activating examples.

## Key results

- **Bricken 2023** extracts thousands of interpretable features from a *one-layer*
  transformer, far more monosemantic than the raw neurons.
- **Cunningham 2023** independently shows SAE directions are highly interpretable
  and causally relevant.
- **Templeton 2024** scales to **Claude 3 Sonnet**: millions of features
  including abstract, multimodal, and safety-relevant ones (e.g. the "Golden Gate
  Bridge" feature), with dictionary-size scaling behavior.

## Anchor edge (how it feeds J-space) — the key "don't conflate"

J-space shares the SAE **algebra** (sparse nonnegative combination of an
overcomplete set) but differs in *basis and objective*:
- **SAE features** are **reconstructive / input-side**: fit to *reconstruct the
  activation*, unsupervised, with no reference to the output.
- **J-lens vectors** are **causal / output-side**: ranked by *first-order effect
  on what the model will say*.

This is the single most important distinction in the survey. The anchor also
*uses* SAEs: it stratifies SAE features by their **J-lens kurtosis** and finds the
highest-κ SAE features are broadcast even more strongly than J-lens vectors —
evidence the J-lens (limited to single tokens) only *partially* captures the
"true" workspace, which the SAE features may approximate more closely.

## Limits

Whether SAE features are the **right causal units** (vs. probing/steering
baselines) is under active dispute (2024–25); training dictionaries is expensive;
each feature needs a separate interpretation step. Grade `contested`, capped
`single-source` here pending independent re-check.
