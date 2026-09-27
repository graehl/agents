# The value of within-batch randomness is task-dependent

[Gonzalez, Alstrøm and May, ICASSP 2023, full text](https://arxiv.org/html/2301.10587v2).
[Local extract](../related-work/extract/gonzalez2023-batching/html/2301.10587v2.md).

Compares random, sorted and bucket batches for a Conv-TasNet speech
enhancer, including fixed and dynamic batch sizes, five training seeds,
and matched/mismatched evaluation conditions. Buckets use ten uniformly
spaced duration ranges. Batches are shuffled between epochs.

Effectiveness: **single-source** for these speech-enhancement conditions.
Sorted and bucket batching reduce padding and training time while giving
similar performance to random batching. Smaller batches improve several
generalization measures. This bounds the inference from the older
ASR/NMT studies: fixed co-residency is not established to harm every task.

This is an independent related study, not a replication of Ge's
semi-sorted Tacotron experiment. It does not supply row-weight or
logical-step guarantees. Its padding ratio uses added padding divided by
original length, whereas Ge's per-batch ratio uses padded capacity as the
denominator; normalize definitions before comparing numbers.
