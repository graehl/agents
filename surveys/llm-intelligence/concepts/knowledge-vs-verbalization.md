# knowledge-vs-verbalization — the split, found independently

> Read-backed digest (cluster I1, trust `single-source`). Read 2026-07-31 from
> `related-work/extract/xiros2026-knowledge-verbalization/`. Part of the
> [J-space lineage](../survey.md) as **independent concurrent corroboration**,
> not ancestry: submitted the same day the anchor published, so neither cites
> the other.

**Paper.** "Knowledge Knows, Verbalization Tells: Disentangling Latent
Directions for Mathematical Solvability in LLMs," Nikolaos Xiros,
Maria-Eleni Zoumpoulidi, Georgios Paraskevopoulos (Institute for Language and
Speech Processing, Athena Research Center, Greece), arXiv 2607.05013v1
[cs.CL], **submitted 2026-07-06**.

**Full text:** [HTML](https://arxiv.org/html/2607.05013) ·
[PDF](https://arxiv.org/pdf/2607.05013).

## What it is

Prior work on unsolvable-problem detection treated *verbalization* only
behaviorally — as something you read off the generated text. This paper probes
it as an **internal representation** instead, separately from the model's
*knowledge* that a problem is unsolvable, and asks how the two interact.

Two directions are probed per model: **knowledge** (does it internally
recognize unsolvability?) and **verbalization** (does it explicitly say so?).
The generated response typically follows the verbalization direction.

## Key results

- Knowledge and verbalization are **distinct, linearly decodable** directions
  across multiple LLMs — and **verbalization is consistently the easier of the
  two to decode**.
- **Fabrication is a misalignment phenomenon**: it correlates with reduced
  alignment between the two directions, and reflects a change in
  *verbalization* rather than in the underlying knowledge. The model largely
  still knows; it stops saying.
- Prompting with unsolvability cues reduces fabrication **mainly by shifting
  verbalization**, not by improving knowledge.
- In large reasoning models, internal reasoning traces and final output traces
  show distinct dynamics under prompt bias.
- Steering: ungated steering "severely compromises specificity," but **gated
  joint** steering of both directions beats steering either alone.

## Convergence with the anchor

This is the map's strongest external evidence that the J-space thesis is not an
artifact of one lab's method. The anchor reaches "verbalizable representations
form a distinct, functionally special subspace" via an averaged-Jacobian lens
on the whole vocabulary in a frontier model; this reaches "verbalization is a
separable linear direction from knowledge" via ordinary probing and steering on
math solvability in open models. Different method, different scale, different
domain, same structural claim — arrived at independently.

It also sharpens the anchor's alignment-auditing case from the other side: if
fabrication is a verbalization shift over intact knowledge, then reading the
verbalizable subspace is exactly where a hidden-objective audit should look.

## Limits

Mathematical solvability only; the authors explicitly leave open whether the
knowledge/verbalization split generalizes to open-domain QA. They also
distinguish their framing from classical faithfulness (representation-to-text)
and leave bridging the two to future work. Single-source, and the steering
result carries its own specificity caveat.

**Onward lead:** the paper credits Park et al. (2026) with applying the same
knowledge-vs-prediction framework to general multiple-choice QA — a further
uncited-by-the-anchor sibling worth fetching.
