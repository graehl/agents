# Spacing and learning rate — where averaging gets diversity

> Read-backed digest (cluster A, trust `single-source`; LLM pretraining evidence,
> not fine-tuning proof).

**Paper.** Sanyal et al., “Early Weight Averaging meets High Learning Rates for
LLM Pre-training,” NeurIPS WANT workshop 2023
([HTML](https://arxiv.org/html/2306.03241),
[PDF](https://arxiv.org/pdf/2306.03241),
[local extract](../related-work/extract/sanyal2023-early-averaging/html/2306.03241.md)).

## Mechanism

Parameter samples that are nearly identical contribute little beyond the last
checkpoint. A larger learning rate and wider save spacing can decorrelate
successive states while they remain in a connected high-performing region;
their mean then suppresses more trajectory noise.

## Evidence

In the reported decoder-only language-model pretraining runs, latest-window
averaging produced larger early gains at higher learning rates and with more
widely separated checkpoints, smoothed loss spikes, and reached useful quality
earlier. The advantage diminished late as the learning rate decayed. The 2025
multi-workload benchmark found the high-learning-rate benefit less universal,
so the broad claim is contested rather than a default recipe.

## Decision edge and limits

Spacing is a diversity control, not a reason to average arbitrarily distant
training phases. Measure parameter or prediction distance and retain a
same-budget control. On a fully annealed, close tail, a small effect is the
expected outcome. Deliberately increasing learning rate is a new continuation
experiment, not a post-hoc averaging tweak.
