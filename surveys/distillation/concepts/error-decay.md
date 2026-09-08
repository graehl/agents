# Predict improvement rather than current difficulty

**Source:** Chang et al., *Machine Learning*, 2020, *Using Error Decay
Prediction to Overcome Practical Issues of Deep Active Learning for Named
Entity Recognition*. [Full text](https://arxiv.org/html/1911.07335) ·
[local extract](../related-work/extract/chang2020-error-decay/html/1911.07335.md).
Read: motivation, error partitioning, curve construction, experimental setup,
main results, and limitations.

Error Decay on Groups (EDG) partitions tokens or sentences by features, fits
validation-error curves against the amount of labeled training support for
each group, and selects batches for predicted error reduction per token.
Variants use changes in predictions or uncertainty when validation labels or
probabilities are unavailable. Its black-box constraint concerns the *student
tagger*, not hidden states of an LLM annotator.

**Effectiveness: single-source.** Experiments use one synthetic task and three
real NER datasets: CoNLL-2003, NCBI disease, and MedMentions ST19. CNN taggers,
BiLSTM-CRF comparisons, and a large pseudo-labeled PubMed pool are included.
EDG beats diversification in several regimes; uncertainty can be more efficient
on clean data. Combining uncertainty with predicted decay helps some noisy
conditions. This directly precedes the idea of predicting which annotation
investment improves a tagger; the general idea is not novel.

The key approximation is that a group's error depends on training counts
within that group. Contextual interactions violate this in NER, a limitation
the paper explicitly acknowledges. Curve fit on observed points is also not
independent evidence of forecasting ability. Our useful extension question is
whether context-aware slices and independent forecast tests explain failure
of that assumption under broad multilingual annotation standards. This remains
unverified; start with the existing EDG idea and simple count/error baselines.
