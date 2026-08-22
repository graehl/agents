# Exponential averaging — online recency smoothing

> Read-backed digest (cluster A, trust `single-source` for the broad controlled
> analysis; corroborated by the modern benchmark digest).

**Paper.** Morales-Brotons, Vogels, and Hendrikx, “Exponential Moving Average
of Weights in Deep Learning: Dynamics and Benefits,” TMLR 2024
([HTML](https://arxiv.org/html/2411.18704),
[PDF](https://arxiv.org/pdf/2411.18704),
[local extract](../related-work/extract/moralesbrotons2024-ema/html/2411.18704.md)).

## Mechanism

EMA updates an auxiliary model as
`average <- beta * average + (1 - beta) * current`. Its weights decay
geometrically with checkpoint age. The effective half-life is
`log(0.5) / log(beta)` EMA updates, so update frequency and beta jointly define
the represented optimizer interval.

## Evidence

The study analyzes EMA across image workloads and reports smoother training,
better consistency/calibration, and compatibility with higher learning rates.
Sparse EMA updates (every 16 optimizer steps in their tested setting) retained
the reported behavior. Useful beta values were task dependent; a nominal range
such as 0.9--0.9999 is not a transferable tuning answer. Starting new live SGD
optimization from the EMA parameters did not add value in their tested setup.

## Decision edge and limits

EMA is the clean online choice when checkpoints are frequent or storage is
limited. Predeclare its half-life and retain a matched uniform-tail control.
Do not choose beta from the confirmation set. BatchNorm statistics can be a
practical complication for long-horizon averages; it does not apply to an
XLM-R encoder built around LayerNorm. The paper's calibration results are not
direct token-tagging evidence.
