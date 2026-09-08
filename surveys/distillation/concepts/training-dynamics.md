# Training dynamics distinguish kinds of difficulty

**Source:** Swayamdipta et al., EMNLP 2020, *Dataset Cartography: Mapping and
Diagnosing Datasets with Training Dynamics*.
[Full text](https://arxiv.org/html/2009.10795) ·
[local extract](../related-work/extract/swayamdipta2020-cartography/html/2009.10795.md).
Read: definitions, controlled subset comparisons, optimization failure, and
label-noise experiment.

For each labeled example, record the student's probability assigned to its
observed label across epochs. The mean is confidence; the standard deviation
is variability. These differ from maximum predicted probability on an unlabeled
example. Consistently high confidence indicates easy examples, variability
indicates model-dependent ambiguity, and consistently low confidence identifies
hard examples—including some bad labels. Only student outputs are needed.

**Effectiveness: single-source.** With RoBERTa-large, controlled one-third
subsets of WinoGrande, SNLI, MultiNLI, and QNLI often retain in-distribution
performance and improve reported out-of-distribution performance when selected
for variability. For WinoGrande, all-ambiguous subsets of 17% or less can fail
to optimize; replacing a tenth of that subset with easy examples restores
learning. This directly bounds “train only on what is hard.” The source's
tables mix mean-over-seed and best-over-seed reporting; they should not be
treated as a uniform statistical comparison.

**Probe proposal:** compute span-boundary, type, and omission stability, with
separate summaries for outside tokens. Discover a candidate rule on old
trajectories; freeze it and predict response to an unseen intervention.
Correlating difficulty with errors on the same training history is diagnostic,
not prospective validation. A consistently hard label should trigger review
before extra weight. A consistently easy label need not be removed from the
stream that supports optimization and domain coverage.
