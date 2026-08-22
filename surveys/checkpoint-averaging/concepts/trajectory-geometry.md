# Trajectory geometry — diversity and fast ensembles

> Read-backed digest (cluster B, trust `single-source`; foundational geometry
> and output-ensemble evidence).

**Paper.** Garipov et al., “Loss Surfaces, Mode Connectivity, and Fast
Ensembling of DNNs,” NeurIPS 2018
([HTML](https://arxiv.org/html/1802.10026),
[PDF](https://arxiv.org/pdf/1802.10026),
[local extract](../related-work/extract/garipov2018-mode-connectivity/html/1802.10026.md)).

## Mechanism

The paper constructs low-loss curves between independently trained optima and
introduces Fast Geometric Ensembling (FGE): use a cyclic learning rate to visit
separated accurate points, then ensemble their outputs. The ensemble preserves
each function instead of assuming that coordinate-wise parameter means are
valid.

## Evidence

Reported FGE ensembles improve over individual snapshots and can approach much
more expensive independent ensembles. The gain depends on useful prediction
disagreement among accurate members, not merely Euclidean parameter distance.
The existence of a nonlinear low-loss curve does not imply that the straight
midpoint is low loss.

## Decision edge and limits

A logit ensemble is a diagnostic upper bound when candidates are materially
divergent: it answers whether their errors are complementary before investing
in parameter alignment. It costs one inference pass per member, so a
same-trajectory near-tie with a weight mean is a reason to stop. For deliberate
SWA/FGE continuations, cyclic learning rate and spacing are mechanisms that
must be compared with an ordinary same-budget continuation.
