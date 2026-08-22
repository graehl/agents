# Latest window — LAWA

> Read-backed digest (cluster A, trust `single-source` for the original method;
> independently bounded by the modern benchmark digest).

**Paper.** Kaddour, “Stop Wasting My Time! Saving Days of ImageNet and BERT
Training with Latest Weight Averaging,” 2022
([arXiv abstract](https://arxiv.org/abs/2209.14981),
[PDF](https://arxiv.org/pdf/2209.14981),
[local extract](../related-work/extract/kaddour2022-lawa/kaddour2022-lawa.md)).

## Mechanism

Latest Weight Averaging stores a rolling window of the last *K* checkpoints and
emits their equal parameter mean. Unlike cumulative averaging, stale early
states eventually leave the window. It can be computed offline from saved
checkpoints or online with a queue/running sum.

## Evidence

Kaddour reports earlier attainment of target quality in ImageNet and BERT
training. The appendix compares uniform and exponentially decayed weights;
there is no general reliable advantage for replacing the simple mean. Later
broad benchmarking reproduces the early-speed advantage while finding that
final gains after learning-rate decay are usually mild.

## Decision edge and limits

Window length has no meaning without save cadence: ten checkpoints saved every
100 updates represent a different horizon from ten saved every 1,000. Express
the horizon in optimizer steps or sentence/token exposure. A very short window
barely smooths; a very long one admits stale states. For an existing close tail,
uniform LAWA is the first baseline, not validation-weighted averaging.
