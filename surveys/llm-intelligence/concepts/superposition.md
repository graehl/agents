# superposition — more features than dimensions

> Read-backed digest (cluster A2, trust `single-source` foundational). Read
> 2026-07-31 from `related-work/extract/elhage2022-superposition/` (transformer-
> circuits HTML). Part of the [J-space lineage](../survey.md); the premise
> J-space's sparse-overcomplete algebra rests on.

**Paper.** "Toy Models of Superposition," Elhage, Hume, Olsson, Schiefer,
Henighan, et al. (Anthropic), transformer-circuits.pub, 2022.
https://transformer-circuits.pub/2022/toy_model/index.html

## What it is

Small ReLU networks trained on synthetic data with **sparse** input features are
used to study how a model can represent **more features than it has dimensions**
— *superposition*. When features are sparse, the network packs them as an
**overcomplete set of near-orthogonal directions**, compressing beyond what a
linear model could, at the cost of **interference** that nonlinearity must filter
out.

## Key findings

- **Phase change.** As feature sparsity rises, the model transitions from a
  clean (one-feature-per-dimension) regime into superposition — a sharp change,
  not a gradient.
- **Geometry.** Superposed features arrange into structured polytopes
  (digons, triangles, pentagons…); importance and sparsity determine which
  features get dedicated dimensions vs. shared ones.
- **Privileged basis.** Superposition explains **polysemantic neurons** — a
  single neuron responding to several unrelated features — because features no
  longer align with the neuron basis.

## Anchor edge (how it feeds J-space)

The load-bearing premise. The anchor frames the residual stream, via the
superposition hypothesis, as decomposing into "sparse linear combinations drawn
from an overcomplete set of feature directions — a **sparse frame**." The J-lens
vectors are a **token-indexed subframe** of that frame, and the **J-space** is
the set of sparse nonnegative combinations of them. Superposition is also the
direct motivation for dictionary-learning SAEs ([sae](sae.md)), which try to
recover the underlying features.

## Limits

Evidence is from **toy models**; the open question the anchor and the SAE line
inherit is how faithfully this picture describes frontier-scale models. Grade
`single-source` (foundational, widely adopted framing; frontier fidelity
unproven).
