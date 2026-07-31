# relation-jacobian — averaged Jacobians as linear relation maps

> Read-backed digest (cluster B4, trust `single-source`). Read 2026-07-31 from
> `related-work/extract/hernandez2024-relation-jacobian/`. Part of the
> [J-space lineage](../survey.md); the **direct methodological ancestor of J-lens**.

**Paper.** "Linearity of Relation Decoding in Transformer Language Models,"
Hernandez, Sharma, Haklay, Meng, Wattenberg, Andreas, Bau, Belinkov, ICLR 2024
(arXiv 2308.09124).

## What it is

Much of an LM's factual knowledge is relational: `(Miles Davis, plays instrument,
trumpet)`. The paper shows that, **for a subset of relations**, the map from a
subject representation to its object attribute is well-approximated by a **single
linear transformation** — obtained as a **first-order (Jacobian) approximation of
the LM from a single prompt**, averaged over a handful of examples. So a "plays
instrument" operator, derived from a few Jacobians, produces `trumpet` from
`Miles Davis`.

## Key result — and its honest limit

The linear relation representation exists across many factual, commonsense, and
linguistic relations. **But it is heterogeneously deployed**: there are many
relations the LM predicts accurately whose knowledge is *not* linearly encoded in
the subject representation. The finding is "a simple, interpretable, but
heterogeneously deployed knowledge representation strategy."

## Anchor edge (how it feeds J-space)

This is the construction J-lens generalizes — the anchor names it as its closest
precedent. Both approximate a transformer map by an **averaged Jacobian**:
- Hernandez: Jacobian of the **object attribute** w.r.t. the **subject
  representation**, averaged over a few examples, per relation.
- J-lens: Jacobian of the **output vocabulary** w.r.t. **internal activations**,
  averaged over ~1,000 prompts, per layer.

The anchor stresses that using a *mean Jacobian* (rather than a trained predictor
like the tuned lens) is empirically important — a point that traces straight to
this paper's method. Reading it is what makes "why an *averaged* Jacobian?"
concrete.

## Limits

Linear approximation holds only for a subset of relations; single-prompt /
per-relation (J-lens's corpus averaging and vocabulary-wide readout are the
generalization). Followed as a new seed 2026-07-31.
