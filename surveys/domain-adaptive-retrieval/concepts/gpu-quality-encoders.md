# GPU-oriented embedding and reranking

Li, Zhang et al., *Qwen3 Embedding: Advancing Text Embedding and Reranking
Through Foundation Models* (2025).
[Full text](https://arxiv.org/html/2506.05176v1) ·
[local extract](../related-work/extract/zhang2025-qwen3-embedding/html/2506.05176v1.md).

**Read:** architecture, training, evaluation settings, embedding/reranking
tables and ablations. **Evidence:** benchmark-reported, not locally reproduced.

The family separates independently encoded vectors from joint query–document
reranking. The latter scores relevance within an already retrieved pool.
The paper compares rerankers over the same top-100 pool, which helps isolate
reranking from candidate generation. Improvement is not universal: the 0.6B
reranker loses on code retrieval against its embedding baseline, and 8B trails
4B on instruction-following retrieval.

**Decision changed:** include stronger GPU models in the corpus-encoding
comparison, but measure task-specific yield and total lifetime cost. A larger
reranker is not automatically better. Reduced output dimensions can save index
space while leaving the transformer forward-pass cost largely intact.
