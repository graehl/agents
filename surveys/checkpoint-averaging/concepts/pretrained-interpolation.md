# Pretrained interpolation — WiSE-FT

> Read-backed digest (cluster C, trust `single-source`; vision robustness
> evidence addressing a different objective from tail smoothing).

**Paper.** Wortsman et al., “Robust fine-tuning of zero-shot models,” CVPR 2022
([HTML](https://arxiv.org/html/2109.01903),
[PDF](https://arxiv.org/pdf/2109.01903),
[local extract](../related-work/extract/wortsman2021-wiseft/wortsman2021-wiseft.md)).

## Mechanism

WiSE-FT linearly interpolates the parameters of a pretrained zero-shot model
and its fine-tuned descendant. Because both endpoints share a lineage, the
straight path can remain useful. The coefficient explicitly trades the
fine-tuned endpoint's in-domain specialization against capabilities retained
from pretraining.

## Evidence

The paper reports improved distribution-shift robustness for vision-language
models while retaining much of fine-tuned in-domain accuracy. An interpolation
coefficient of 0.5 is a robust recommendation in its tested vision regime when
no target-domain information is available, not a universal coefficient for
other architectures or tasks.

## Decision edge and limits

This is not checkpoint-tail smoothing. It is appropriate only when retaining a
measurable pretrained/zero-shot capability is part of the objective. A
multilingual tagger that compares nearby continuation checkpoints should not
borrow the 0.5 rule. If catastrophic specialization is a live concern, add the
pretrained endpoint and its retained-capability metric as a separate,
predeclared interpolation arm.
