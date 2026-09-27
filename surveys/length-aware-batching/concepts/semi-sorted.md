# Semi-sorted batching

[Ge, Kaushik, Omote and Kumar, Interspeech 2021, full text](https://www.isca-archive.org/interspeech_2021/ge21_interspeech.pdf).
[Local extract](../related-work/extract/ge2021-semi-sorted/ge2021-semi-sorted.md).

Sort examples by a perturbed length, then form contiguous physical batches.
The key is `length + Uniform(-a/2, a/2)`, with
`a = r * (maximum_length - minimum_length)`. The local randomization factor
`r` controls the padding/randomness tradeoff. Batch order is randomized,
and preparation is repeated each epoch. This is a simple published answer
to the physical-batching question; it does not require each optimizer step
to be sampled independently first.

Compared with fixed length buckets, perturbation avoids fixed boundaries;
compared with shuffled-window sorting, it perturbs the sort directly.
The additive noise scale depends on the corpus range, so an extreme outlier
changes its meaning. Log-length noise would be a relative-width adaptation,
not the paper's algorithm.

Effectiveness: **single-source**. On LJSpeech with a modified Tacotron2,
semi-sorting plus batch-order randomization reduces minutes per epoch by
29.98% against random fixed-size batching. Adding dynamic batch sizes raises
the reported reduction to 41.25%. The combined setting slightly improves
validation loss; semi-sorting alone is not shown to match random batching
on every quality measure. Human listening scores were deferred. These are
2017-era GPU/model conditions, not a prediction for a modern encoder.

The paper's comparison includes bucket batching and alternated sorting at
similar padding rates; their performance is similar. Its contribution is
the simple continuous control, not demonstrated dominance over bucketing.

No arbitrary row-weight treatment, logical-step stream quotas, repeat-gap
test, or bounded streaming startup guarantee is established here. Applying
this arrangement to a previously sampled weighted multiset preserves that
multiset, but that composition is our inference.

Extraction caveat: marker merges rows in Tables 1 and 2. The percentages
above come from the intact Table 3 and adjacent prose; consult the PDF for
fine-grained table comparisons. Source-faithful extraction is retained.
