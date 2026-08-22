# Trajectory averaging — SWA and the width claim

> Read-backed digest (cluster A, trust `reproduced` for the practical
> averaging effect; `contested` for a universal wider-optimum explanation).

**Papers.** Izmailov et al., “Averaging Weights Leads to Wider Optima and
Better Generalization,” UAI 2018
([HTML](https://arxiv.org/html/1803.05407),
[PDF](https://arxiv.org/pdf/1803.05407),
[local extract](../related-work/extract/izmailov2018-swa/html/1803.05407.md));
Guo, Jin, and Liu, “Stochastic Weight Averaging Revisited,” Applied Sciences
2023 ([HTML](https://arxiv.org/html/2201.00519),
[PDF](https://arxiv.org/pdf/2201.00519),
[local extract](../related-work/extract/guo2022-swa-revisited/html/2201.00519.md)).

## Mechanism

SWA begins from a conventionally trained model, continues with a constant or
cyclic learning rate, samples several high-performing parameter states, and
averages them uniformly. The nonvanishing learning rate is meant to traverse a
connected region instead of collapsing immediately to one endpoint. The mean
often lies nearer the center of that region and costs one model at inference.

## Evidence

Izmailov et al. report improved test accuracy and calibration across several
vision architectures relative to the terminal SGD checkpoint. Their geometric
account is that SGD samples lie near the boundary of a broad high-performing
region while their mean is more central. Later work re-evaluates several
flatness measures and finds that averaging can reduce variance and improve
generalization without consistently producing a measurably wider optimum.

The robust claim is therefore procedural: averaging compatible trajectory
points often smooths optimization noise. “It always finds a wider minimum” is
too strong. The practical effect has been repeated across independent task
families; the exact geometric explanation is contested.

## Decision edge and limits

A mean over late checkpoints from an ordinary decay-to-zero schedule is a
checkpoint average, not a full SWA test. To attribute an effect to SWA, retain
a same-budget nonaveraged continuation and deliberately sample under a small
nonzero constant or cyclic learning rate. Batch-normalized networks require
statistics recomputation after parameter averaging; LayerNorm-based
transformers do not.
