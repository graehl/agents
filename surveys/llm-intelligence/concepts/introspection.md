# introspection — concept-injection tests of self-awareness

> Read-backed digest (cluster F1, trust `single-source`/`contested`). Read
> 2026-07-31 from `related-work/extract/anthropic2025-introspection/`. Part of the
> [J-space lineage](../survey.md); the direct methodological precursor to the
> anchor's "verbal report" protocol.

**Paper.** "Emergent Introspective Awareness in Large Language Models," Anthropic,
transformer-circuits.pub, 2025 (published 2025-10-29).

**Full text:** [Emergent Introspective Awareness in LLMs](https://transformer-circuits.pub/2025/introspection/index.html) (transformer-circuits).

## What it is

You cannot test introspection by *asking* — a model can **confabulate** a
plausible self-report it learned to imitate. The method: **inject a known
concept's representation** into the model's activations (a steering vector for,
say, "bread"), then measure whether the model's **self-report** changes
accordingly. A genuine report should track the injection; a confabulation should
not.

## Key results

- Models can, **in some scenarios**, notice an injected concept and **correctly
  name it** — introspecting on a manipulation applied to their own activations.
- Some ability to **recall prior internal representations** and distinguish them
  from raw text input; strikingly, to use recalled **prior intentions** to tell
  their *own* outputs from artificial **prefills**.
- Models can **modulate** their activations when instructed/incentivized to
  "think about" a concept.
- **Claude Opus 4 / 4.1** show the most introspective awareness, but trends are
  complex and sensitive to post-training. The capacity is **highly unreliable and
  context-dependent**.

## Anchor edge (how it feeds J-space)

The **verbal-report** property of J-space is this experiment with a *mechanism*
attached. The anchor adapts the same **concept-injection** design (its
"injected thought" experiment), but where introspection measures the *behavioral*
self-report, J-space identifies the *representation* being reported — the injected
concept appears as a **J-lens vector**, and ablating the broadcast heads drops the
injected-thought report rate (0.54→0.09). Introspection asks "can it report?";
J-space answers "here is the thing it reports from."

## Limits

Self-access is real but **limited, unreliable, easy to over-read**; sensitive to
post-training. `single-source`/`contested`. Pairs with the F1 debate trio
(Ji-An positive, Song on privileged access, Comșa skeptical).
