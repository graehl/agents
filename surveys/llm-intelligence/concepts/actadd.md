# actadd — activation addition / steering vectors

> Read-backed digest (cluster C1, trust `single-source`). Read 2026-07-31 from
> `related-work/extract/turner2023-actadd/`. Part of the
> [J-space lineage](../survey.md); the causal-intervention form J-space uses to
> test its properties.

**Paper.** Turner, Thiergart, Udell, Leech, Mini, MacDiarmid, arXiv **2308.10248**
— **renamed across versions**: original v1 "Activation Addition: Steering Language
Models Without Optimization"; current arXiv title "Steering Language Models With
Activation Engineering." (The anchor cites the original title; both are the same
paper. An earlier survey pass wrongly flagged the old title as an error.)

**Full text:** [HTML](https://arxiv.org/html/2308.10248) · [PDF](https://arxiv.org/pdf/2308.10248).

## What it is

**Activation engineering** = inference-time modification of activations to steer
outputs. **ActAdd**: take a **contrast prompt pair** (e.g. "Love" vs "Hate"),
compute the **difference of their activations** at some layer → a **steering
vector** `v`, then add `h ← h + αv` during the forward pass. No optimization, no
fine-tuning, a **single pair** of data points — the vectors act as "virtual bias
terms."

## Key results

State-of-the-art **negative→positive sentiment** shift and **detoxification** on
LLaMA-3 and OPT, while **preserving off-target task performance**. Lightweight and
iterable (a new steering axis is one prompt pair away). The motivating intuition:
activation engineering can elicit capability combinations no *prompt* can (their
"eloquent mathematician" argument — the training distribution assigns such text
low probability, so no prompt elicits it, but the internal circuitry can be
co-activated).

## Anchor edge (how it feeds J-space)

J-space uses **exactly this intervention form** as its causal test harness. To
establish the five workspace properties it steers along **J-lens vectors**
(`h ← h + αv_t`), ablates (negative α, or projecting out `v_t`), and patches lens
coordinates to swap one concept for another. So ActAdd is the "write" primitive
of the J-lens toolkit; the novelty in the anchor is *which* vectors it steers
(causal, output-disposition, single-token) and using steering as *evidence* for a
workspace rather than as an end in itself.

## Limits

Works cleanly for some concepts, brittle/off-target for others; **α- and
layer-sensitive**; a fair baseline is prompt-only control, against which some
steering wins are narrow. Grade `single-source`.
