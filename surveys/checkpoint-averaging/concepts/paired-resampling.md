# Paired resampling — uncertainty for structured F1

> Read-backed digest (cluster D, trust `reproduced` for the general paired-
> bootstrap procedure; calibration remains dataset dependent).

**Papers.** Berg-Kirkpatrick, Burkett, and Klein, “An Empirical Investigation
of Statistical Significance in NLP,” EMNLP-CoNLL 2012
([ACL page](https://aclanthology.org/D12-1091/),
[PDF](https://aclanthology.org/D12-1091.pdf),
[local extract](../related-work/extract/bergkirkpatrick2012-significance/bergkirkpatrick2012-significance.md));
Dror et al., “The Hitchhiker's Guide to Testing Statistical Significance in
Natural Language Processing,” ACL 2018
([ACL page](https://aclanthology.org/P18-1128/),
[PDF](https://aclanthology.org/P18-1128.pdf),
[local extract](../related-work/extract/dror2018-significance-guide/dror2018-significance-guide.md)).

## Mechanism

A paired bootstrap resamples evaluation units with replacement, keeps both
systems' outputs paired on every sampled unit, recomputes the complete metric,
and records the difference. It needs no closed-form distribution for a
nonlinear metric such as F1.

For span tagging, the sampling unit must preserve dependence. If sentences
come from one intake document, resample the document and carry all of its
sentences, gold spans, and both prediction sets together. Resampling individual
spans treats correlated errors as independent and overstates information.

## Evidence

Berg-Kirkpatrick et al. empirically study significance tests over NLP metrics
and find paired bootstrap applicable to complex metrics including F1, while
also showing that test calibration changes under domain shift. Dror et al.
recommend nonparametric sampling tests for F-score because its sampling
distribution is not safely assumed; they emphasize paired design and the loss
of power with small test sets.

## Decision edge and limits

For mixture-weighted evaluation, resample provenance clusters within source
strata and restore the target source weights before pooling TP/FP/FN. Report an
interval for the paired delta and a practical-equivalence margin. A bootstrap
on a development set does not undo adaptive checkpoint selection, and
significance on one domain is not evidence for transfer to a fresh domain.
