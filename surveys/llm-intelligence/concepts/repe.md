# repe — representation engineering (top-down transparency)

> Read-backed digest (cluster C2, trust `single-source`). Read 2026-07-31 from
> `related-work/extract/zou2023-repe/`. Part of the [J-space lineage](../survey.md);
> the systematized reading/steering family J-lens's probe and steering modes sit in.

**Paper.** "Representation Engineering: A Top-Down Approach to AI Transparency,"
Zou, Phan, Chen, Campbell, Guo, Ren, Pan, ... et al., 2023 (arXiv 2310.01405).
Code: github.com/andyzoujm/representation-engineering.

**Full text:** [HTML](https://arxiv.org/html/2310.01405) · [PDF](https://arxiv.org/pdf/2310.01405).

## What it is

Put **representations** (not neurons or circuits) at the center of analysis.
RepE derives **reading vectors** and **control vectors** from *contrastive
stimulus sets* — e.g. Linear Artificial Tomography (LAT): collect paired
activations for a concept present vs. absent across many stimuli, take a
principal direction. Then **read** (is the concept active? how strongly?) or
**steer** (add/subtract the control vector) high-level cognitive properties.

## Key results

Simple but broadly effective traction on safety-relevant axes: **honesty and
hallucination**, utility, **power-aversion**, risk, **emotion**, harmlessness,
fairness/bias, knowledge editing, and memorization — presented with baselines as
an initial characterization of the area, arguing for "top-down" transparency over
bottom-up circuit tracing.

## Anchor edge (how it feeds J-space)

RepE is the **supervised-by-contrast** systematization of steering:
[actadd](actadd.md) hand-picks a direction from *one* prompt pair; RepE extracts
it from a *stimulus set*; an [sae](sae.md) extracts directions *unsupervised*.
J-lens's **per-token probe** mode ("read the score of `h_ℓ` against a chosen
`v_t`") and its steering interventions are the same read/write moves, but on a
**causal, output-disposition** basis derived analytically rather than from
labeled contrasts. RepE's honesty / eval-awareness axes also **prefigure the
anchor's alignment-auditing use** (cluster H).

## Limits

`single-source`; demonstrated control of honesty/harmfulness/emotion axes, but
generality is contested and effects are α-/layer-sensitive. A read/steer
framework, not a benchmarked result.
