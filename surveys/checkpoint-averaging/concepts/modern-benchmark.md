# Modern benchmark — when, where, and why averaging helps

> Read-backed digest (cluster A, trust `benchmark-reported`; one coordinated
> study spanning seven heterogeneous workloads and a language-model case).

**Paper.** Ajroldi, Orvieto, and Geiping, “When, Where and Why to Average
Weights?,” ICML 2025
([PMLR page](https://proceedings.mlr.press/v267/ajroldi25a.html),
[PDF](https://raw.githubusercontent.com/mlresearch/v267/main/assets/ajroldi25a/ajroldi25a.pdf),
[local extract](../related-work/extract/ajroldi2025-when-where-why/ajroldi2025-when-where-why.md)).

## Scope and mechanism

The study adds LAWA or EMA to strong NadamW/AdamW baselines across seven
AlgoPerf workloads and a 124M-parameter language-model run. It varies averaging
horizon, checkpoint frequency, learning-rate schedule, and optimizer while
measuring both steps-to-target and final validation quality.

## Evidence

Across the benchmark, averaging reached target scores earlier; the paper
estimates a 12% GPU-hour reduction for the suite. LAWA and EMA were similar when
their horizons were tuned. Final generalization improvements were mild overall,
with larger task-specific effects such as WMT. In the language-model experiment
both reduced steps-to-target by roughly 30%, but the final validation-loss gain
was minimal. Moderate horizons worked; extreme short/long settings failed.

The benefit shrank when the learning rate was already annealed to zero.
Averaging approximated some effect of a shorter decay but did not generally
replace a tuned learning-rate schedule; combining averaging and annealing was
best. The paper's practical examples often favor a horizon around 1% of total
training budget, but it explicitly shows workload and sampling-frequency
dependence, so 1% is a starting point rather than a law.

## Decision edge and limits

The strongest general expectation for a mature, fully annealed checkpoint is a
minor final gain. Larger benefits concern access to a good model earlier during
training. Averaging normally tracks rather than rescues a bad baseline
trajectory. For a new run, compare one moderate uniform window and one matched
EMA; for an existing late tail, do not justify a large hyperparameter sweep.
