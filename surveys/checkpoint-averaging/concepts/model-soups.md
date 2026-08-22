# Model soups — common-start fine-tunes

> Read-backed digest (cluster B, trust `single-source`; broad vision evidence
> with a smaller NLP text-classification section).

**Paper.** Wortsman et al., “Model soups: averaging weights of multiple
fine-tuned models improves accuracy without increasing inference time,” ICML
2022 ([PMLR page](https://proceedings.mlr.press/v162/wortsman22a.html),
[PDF](https://proceedings.mlr.press/v162/wortsman22a/wortsman22a.pdf),
[local extract](../related-work/extract/wortsman2022-model-soups/html/2203.05482.md)).

## Mechanism

All ingredients begin from the same pretrained model and are fine-tuned with
different hyperparameters. A **uniform soup** averages every ingredient. A
**greedy soup** considers models in validation-ranked order and keeps an
addition only if the new mean improves validation accuracy. A learned soup
fits continuous mixture weights.

## Evidence

The paper reports single-model accuracy and robustness gains without ensemble
inference cost, mainly on vision benchmarks; NLP text-classification gains are
smaller. Uniform soups fail when weak or high-learning-rate ingredients create
an error barrier along the interpolation path. Greedy selection limits that
failure. Learned weights add tuning and offer no general need over the simpler
recipes.

The paper relates weight averaging to logit ensembling: when endpoints are
close, confident, and connected by a locally linear function, the weight soup
can approximate the output ensemble. Soups do not automatically inherit the
calibration benefit of a true ensemble.

## Decision edge and limits

For one close trajectory, the uniform tail mean is the analogue. Greedy
validation admission is useful only for heterogeneous common-start branches
and requires a selector disjoint from confirmation. If the logit ensemble and
weight mean tie for close checkpoints, the result closes rather than motivates
the slower ensemble. A meaningful ensemble-only gain for divergent branches
is evidence to investigate barriers or alignment.
