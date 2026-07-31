# pre-verbalization-commitment — when the answer is fixed before it is said

> Read-backed digest (cluster I1, trust `single-source`). Read 2026-07-31 from
> `related-work/extract/zhang2026-pre-verbalization-commitment/`. Part of the
> [J-space lineage](../survey.md) as **independent concurrent work**: published
> two months before the anchor and uncited by it.

**Paper.** "When Does a Language Model Commit? A Finite-Answer Theory of
Pre-Verbalization Commitment," Long Zhang, Wei-neng Chen, Feng-feng Wei,
Zi-bo Qin, arXiv 2605.06723, **submitted 2026-05-07**.

**Full text:** [HTML](https://arxiv.org/html/2605.06723) ·
[PDF](https://arxiv.org/pdf/2605.06723).

## What it is

A model writes reasoning and then an answer, but the visible chronology need
not match the chronology of *preference*. If preference stabilizes early, the
rest of the visible reasoning happens in a **post-commitment regime** — which
is the mechanistic version of the CoT-faithfulness worry.

The paper's move is to avoid both greedy rollouts (tautological on
deterministic trajectories) and learned probes (which show accessible
information without defining current preference) by measuring a **narrow
computable object**: project the model's own continuation probabilities onto a
finite answer set. For binary tasks this is an exact log-odds code,

```
δ(ξ) = S_θ(yes | ξ) − S_θ(no | ξ)
```

from which parser-based answer onset, retrospective stabilization time, and
**lead** are all defined without a probe.

## Key results

- On controlled delayed-verdict tasks with **Qwen3-4B-Instruct**, the
  contextual finite-answer projection stabilizes *before* the answer is
  parseable, with a **17–31 token mean lead** in the main templates, and a
  positive but shorter lead in a parser-clean replication.
- The signal **tracks the model's eventual output, not the truth** — it is a
  preference code, not a correctness code.
- It is **linearly recoverable from compact hidden summaries**, partly
  separable from cursor progress, and transfers as shared information with no
  single invariant coordinate.
- **Negative result worth keeping:** exact steering shows local sensitivity of
  δ but *not* reliable generation control. Measuring commitment did not buy
  control of it.

## Convergence with the anchor

The anchor's J-lens answers "which tokens is the model *poised to verbalize*
right now?" — a spatial, whole-vocabulary question. This answers the temporal
one: "how far ahead of saying it is the answer already fixed?", and gives a
number. They are the same phenomenon measured on orthogonal axes, and neither
paper knows about the other.

That makes it a cheap discriminating check on the anchor's story: if J-space
contents are what get broadcast toward output, J-space occupancy should settle
on roughly the lead this paper measures. Nothing in either paper tests that
yet, and it is the most concrete cross-validation the map currently affords.

## Limits

One small open model (Qwen3-4B-Instruct); binary tasks only, with K>2 left to
future work; controlled delayed-verdict templates under deterministic greedy
decoding, which the authors note are simpler than open-ended or stochastic
generation. Lead magnitude depends on template geometry. The measured object is
**verbalizer-conditioned** and explicitly not unrestricted semantic belief, and
stabilization time is retrospective rather than an online detector.
