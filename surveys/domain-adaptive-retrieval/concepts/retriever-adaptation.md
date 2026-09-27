# Teaching retrieval with generated queries and soft relevance

Wang, Thakur, Reimers and Gurevych, *GPL* (NAACL 2022).
[Full text](https://ar5iv.labs.arxiv.org/html/2112.07577) ·
[local extract](../related-work/extract/wang2022-gpl/html/2112.07577.md).

**Read:** method, experimental setup, baselines, results and analyses of corpus
size, query quality and initialization. **Evidence:** single-source for the
six-domain DistilBERT comparison; not a result on multilingual E5.

GPL generates queries from target-domain passages, mines negatives and obtains
cross-encoder scores. A dense retriever learns the teacher's positive–negative
score margins. This differs from treating every generated query as valid and
every mined neighbor as irrelevant.

The paper finds that false hard negatives hurt its simpler QGen baseline;
soft supervision makes GPL more robust to generated-query noise. Generic
unsupervised representation training alone is weak in this retrieval setup.
The Robust04 corpus-size ablation includes a small-data condition below
zero-shot performance. Its substantial training schedule is not evidence for
effective single-document micro-adaptation.

**Decision changed:** if adapting the embedder, test retrieval-specific
supervision and retain a strong frozen baseline. Audit the teacher in each
language/domain, and account for rebuilding the corpus vectors. A teacher's
relevance margin does not itself predict downstream annotation value.
