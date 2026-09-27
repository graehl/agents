# Multilingual retrieval and alignment

Wang et al., *Multilingual E5 Text Embeddings: A Technical Report* (2024).
[Full text](https://arxiv.org/html/2402.05672v1) ·
[local extract](../related-work/extract/wang2024-multilingual-e5/html/2402.05672v1.md).

**Read:** training methodology, experimental results and implementation appendix.
**Evidence:** benchmark-reported; no local reproduction.

E5 combines multilingual contrastive pretraining with supervised fine-tuning,
hard negatives and cross-encoder distillation. It evaluates multilingual
retrieval on MIRACL and cross-language alignment through bitext mining. These
two evaluations are not interchangeable. The report's small model trails its
larger models on bitext tasks; a broad language list does not guarantee equal
quality on every language pair.

The nearest confusable alternatives are a translation-pair specialist such as
LaBSE and a paraphrase-similarity encoder. Which is appropriate depends on
whether the target is translation equivalence, topical similarity, or relevance
to a query. The model cards specify different prefixes for asymmetric and
symmetric tasks; those belong in a pinned comparison.

**Decision changed:** keep the user's E5-base baseline and test smaller models
on cross-language candidate recall, not only aggregate embedding benchmarks.
This report provides no CPU-throughput ranking for the intended workload.
