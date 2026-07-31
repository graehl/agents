# attribution-graphs — circuit tracing via cross-layer transcoders

> Read-backed digest (cluster D2, trust `single-source`). Read 2026-07-31 from
> `related-work/extract/anthropic2025-circuit-tracing/` (methods) and
> `.../anthropic2025-biology/` (application). Part of the
> [J-space lineage](../survey.md); the causal-interpretability sibling of J-lens.

**Papers (companion pair, Anthropic, transformer-circuits.pub, 2025).**
- "Circuit Tracing: Revealing Computational Graphs in Language Models" (methods).
- "On the Biology of a Large Language Model" (application to Claude 3.5 Haiku).

## What it is

Build an interpretable **replacement model**: swap the MLPs for a **cross-layer
transcoder (CLT)** — a sparse, dictionary-learned feature layer trained to
approximate them. On a given prompt, trace the computation through the
replacement as an **attribution graph**: nodes are interpretable features, edges
are the (linear, per-prompt) causal contributions between them. A "wiring
diagram" of *this* computation, validated by perturbation experiments.

## Key results (the "Biology" case studies)

On Claude 3.5 Haiku, attribution graphs surface concrete mechanisms:
**multi-step reasoning**, **planning ahead** in poems (choosing a rhyme word
early), **multilingual** shared circuits, **addition** heuristics, **refusals**,
the "life of a **jailbreak**," **CoT (un)faithfulness**, and **uncovering hidden
goals** in a misaligned model — the last directly prefiguring the anchor's
auditing use.

## Anchor edge (how it feeds J-space)

The nearest causal-interpretability **sibling**, same lab. Both read the model
causally, but at different granularity:
- **Attribution graphs** map the **pathway between features** for one prompt
  (expensive, per-input, a full circuit).
- **J-lens** ranks a **single activation's general output-token disposition**
  (one precomputed matrix/layer, no per-prompt tracing).

CLT features (sparse, [sae](sae.md)-style) are the graph's nodes — so this is
where the SAE lineage (A3) and the circuits substrate (D1) fuse into a causal
tracer, the immediate methodological context J-space sits in. Design choice:
attribution graphs for "trace the whole circuit behind this output"; J-space for
"what latent, verbalizable concept is active here."

## Limits

`single-source`; per-prompt and expensive; the replacement model is an
approximation (reconstruction error, missing edges). Demonstrated on production
models, not independently reproduced.
