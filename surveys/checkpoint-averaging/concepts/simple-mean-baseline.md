# Simple mean baseline — elaborate weights rarely pay

> Read-backed digest (cluster B, trust `single-source`; transformer NMT is a
> close procedural analogue to sequence tagging).

**Paper.** Gao, Herold, Yang, and Ney, “Revisiting Checkpoint Averaging for
Neural Machine Translation,” Findings of AACL-IJCNLP 2022
([ACL page](https://aclanthology.org/2022.findings-aacl.18/),
[PDF](https://aclanthology.org/2022.findings-aacl.18.pdf),
[local extract](../related-work/extract/gao2022-checkpoint-averaging/gao2022-checkpoint-averaging.md)).

## Comparisons

The paper compares ordinary last-*K* and top-*K* means with development-
perplexity weighting, gradient-based adjustment, and learned interpolation
weights. These alternatives try to reward apparently healthier checkpoints or
optimize the mixture directly.

## Evidence

Simple checkpoint averaging is robust across the reported NMT setups. The
extra weighting and gradient/mixture optimization add complexity without a
reliable improvement over the mean. The authors find a relatively flat region
around the simple solution, which helps explain why estimated continuous
coefficients are unstable and unnecessary.

## Decision edge and limits

For nearby checkpoints, the burden of proof belongs to health weighting. Use
objective faults to exclude a checkpoint, then weight the eligible states
equally. A top-*K* rule selected by the same development curve inherits peak-
selection noise. A materially different task/domain mixture or divergent
fine-tunes could motivate another study, but does not weaken the simple mean as
the control.
