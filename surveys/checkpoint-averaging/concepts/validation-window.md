# Validation window — SWAD-style eligibility

> Read-backed digest (cluster A, trust `single-source`; domain-generalization
> evidence, not direct multilingual tagging evidence).

**Paper.** Cha et al., “SWAD: Domain Generalization by Seeking Flat Minima,”
NeurIPS 2021 ([HTML](https://arxiv.org/html/2102.08604),
[PDF](https://arxiv.org/pdf/2102.08604),
[local extract](../related-work/extract/cha2021-swad/html/2102.08604.md)).

## Mechanism

SWAD averages densely along a trajectory but uses validation loss to define
when averaging begins and when a sustained degradation ends the window. The
intent is to include the flat plateau and exclude underfit early states and an
overfit tail.

## Evidence

On the paper's domain-generalization benchmarks, the plateau/loss-tolerance
rule outperformed ordinary SWA and a window chosen by exhaustive validation
fit. The latter is an important negative result: directly optimizing the
averaging interval against one validation set can itself overfit.

## Decision edge and limits

Validation loss is useful as a binary eligibility signal because it is smoother
than exact task F1. The threshold and patience must be predeclared. This does
not support continuous weighting by validation F1 or searching many windows on
the final confirmation view. A contiguous eligible window is easier to audit
than a top-*K* set of noisy peaks.
