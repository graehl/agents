# activation-decoding — reading an activation into natural language

> Read-backed digest (cluster G1, trust `single-source` each). Read 2026-07-31
> from `related-work/extract/chen2024-selfie/` and `.../pan2024-latentqa/`
> (Activation Oracles + NL-Autoencoders from the anchor's citations). Part of the
> [J-space lineage](../survey.md); **J-lens's nearest live sibling family**.

**Papers.**
- **SelFIE** — Chen, Vondrick, Mao, "Self-Interpretation of LLM Embeddings,"
  ICML 2024 (arXiv 2403.10949).
- **LatentQA** — Pan, Chen, Steinhardt, "Teaching LLMs to Decode Activations Into
  Natural Language," 2024 (arXiv 2412.08686).
- **Activation Oracles** — Karvonen et al. 2025; **Natural Language Autoencoders**
  — Fraser-Taliente, Kantamneni, et al. 2026 (co-author Kantamneni is also a
  J-space author).

## What it is

Decode an internal activation **into free text** rather than a token score.
- **SelFIE** feeds an embedding *back into the model* with a template and lets it
  **explain itself** in natural language — no training. It surfaces internal
  reasoning (ethical decisions, internalized prompt injection, recalled harmful
  knowledge) and enables **Supervised/Reinforcement Control** to edit concepts.
- **LatentQA** trains a **decoder** to answer natural-language *questions* about
  activations, then uses it to **read** and **control** behavior.
- **Activation Oracles** train general-purpose activation explainers; **NL
  Autoencoders** produce *unsupervised* NL explanations through a text bottleneck.

## Anchor edge (how it feeds J-space) — the defining contrast

The anchor places J-lens at the **cheap-and-grounded** end of *this exact*
spectrum of activation readers. The trade-off axis is **expressivity vs. causal
faithfulness**:
- These decoders produce **free text** — multi-token, relational, expressive —
  but at higher cost and with a real **confabulation** risk (the explanation may
  be fluent but not grounded in the activation).
- **J-lens** produces a **ranked single-token disposition** with a first-order
  **causal** guarantee (`∂output/∂activation`), one matmul per layer, but cannot
  name multi-token concepts.

The anchor calls them **complementary, not competitive** — a SelFIE/LatentQA
description can articulate what a J-lens readout of `prompt` + `injection` only
gestures at, while the J-lens guarantees its readout reflects the activation's
actual causal role.

## Limits

`single-source` each; recent and largely un-reproduced across labs; free-text
explainers risk confabulation and are costlier. **No local deep read yet of
Activation Oracles / NL-Autoencoders** — those two are summarized from the
anchor's citations, not their own full text (grounded pass still queued).
