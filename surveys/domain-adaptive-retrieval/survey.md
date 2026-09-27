# Multilingual retrieval for domain and input-specific adaptation

**Mode: grounded, bounded field survey. Coverage cutoff: 2026-09-27.**
Seven primary texts have accepted local full-text extracts; additional primary
papers and model documentation were read online. `[G]` means a read source with
an accepted local extract; `[R]` means an online reading without one. Three
attempted extractions failed the shared fidelity check and remain explicitly
unarchived. These marks describe source access, not replication. The
[search record](related-work/search-notes.md) gives anchors, citation searches,
source coverage and exclusions. No embedding benchmark or adaptation experiment
was run for this survey.

## Start from multilingual E5-base and FAISS

The existing baseline is **`intfloat/multilingual-e5-base` → FAISS**. Keep it
as the reference while testing cheaper candidate generators. Its purpose here
is to retrieve useful training or annotation material, potentially conditioned
on a new document or a user's interests across documents. A high-recall rough
stage can tolerate irrelevant candidates if later selection is cheap relative
to the annotation or training it avoids. Missing a useful region entirely is
harder to repair.

The local `draft` implementation confirms E5-base and a FAISS HNSW index using
inner product over normalized vectors. Its overlap-audit notes distinguish
interactive approximate lookup from final exact cosine neighbors. That is a
useful precedent, not a requirement that domain acquisition be exact. The
[local-context record](related-work/search-notes.md#local-context) identifies
the implementation and the existing domain-intake proposal. That proposal
already owns any PII experiment; this survey supplies reusable literature.

**Sizing scenario:** a few hundred GB of text, indexed on one host with one
GPU available. GPU acceleration and a better, more expensive encoder than
E5-base are in scope. The bytes refer to text for planning, not a verified
size of an entire named dataset release. The linked local proposal concerns
FineWeb-2; corpus selection and actual decompressed/chunked counts remain
inputs to the cost model below.

**Suggested comparison, not an executed result:** retain E5-base, including
an efficient GPU execution of that same model. Compare a cheap-index route
(E5-small or static multilingual pooling plus stronger rescoring) with a
better-encoder route (E5-large, BGE-M3 dense, or Qwen3-Embedding-0.6B indexed
up front). A Qwen3 4B/8B model is a quality-oriented extension if measured
benefit justifies its build cost or small-pool reranking cost. Use the same
corpus, segmentation and query set. Measure independently judged usefulness
as well as agreement with E5; the incumbent is not ground truth. Choose
between these routes against query volume, refresh frequency and useful yield,
using the [corpus-scale accounting](#one-host-corpus-scale-accounting).

## Three different things can adapt

| Adapted object | Signal and purpose | Consequence for stored vectors |
|---|---|---|
| Query or user profile | New document, explicit query, recent interests, relevance feedback | Frozen corpus vectors remain usable |
| Downstream annotator, tagger or language model | Retrieved text, trusted labels or teacher supervision | Unchanged if the retrieval encoder is separate and frozen |
| Retrieval encoder itself | Query–passage pairs, similarity supervision, teacher scores | New document representations normally require re-embedding and rebuilding the index |

A changed query encoder can deliberately search a frozen document space, but
it must be trained against that space. Updating both sides and querying old
vectors silently changes the scoring problem. A shared change of basis can
preserve new–new similarities while destroying new–old compatibility; good
freshly rebuilt retrieval scores therefore do not certify index compatibility.

This makes **frozen retrieval plus short downstream adaptation** the cleaner
first micro-adaptation test. Independently improving the retriever is a later
intervention whose rebuild cost belongs in its accounting.

## Embedders: multilingual capability is task-dependent

A multilingual encoder is not automatically a well-aligned cross-lingual
retriever. Test both same-language retrieval and queries in language A against
documents in language B. MIRACL evaluates retrieval across a collection of
languages, predominantly with same-language query/corpus pairs; bitext mining
tests a different property. E5's report includes both retrieval and bitext
evaluations. Its small variant trails the larger variants on bitext mining,
so preserving multilingual average retrieval is not sufficient evidence of
preserved cross-language alignment. See the [E5 digest](concepts/multilingual-space.md)
`[G]` and [model cards](related-work/search-notes.md#implementation-sources).

The following are candidates and verified representation specifications, not
a throughput ranking. Language counts are authors' coverage claims.

| Candidate | Representation and input limit | Role relative to E5-base | Main qualification |
|---|---|---|---|
| multilingual E5-base | 768 dimensions; 512 tokens | Existing contextual baseline | Preserve pooling, normalization and task prefixes |
| multilingual E5-small | 384 dimensions; 512 tokens | First smaller contextual comparison | Same 12-layer depth does not imply equal compute; measure cross-language recall separately |
| multilingual E5-large | 1024 dimensions; 512 tokens | Larger member of the incumbent family, GPU-oriented comparison | More encoding and vector-storage cost; reported family gains do not establish this workload's gain |
| paraphrase-multilingual-MiniLM-L12-v2 | 384 dimensions; configured 128-token sequence length | Older short-sentence alternative | Paraphrase similarity training and short truncation differ from passage retrieval |
| Model2Vec `potion-multilingual-128M` | Static token embeddings, pooled to 256 dimensions; 101 training languages | CPU-oriented coarse candidate generator | No contextual attention; an unlimited accepted input length does not imply preserved long-document detail |
| EmbeddingGemma-300m | 768 dimensions, supported 512/256/128 truncations; 2048 tokens; 100+ languages | Compact contextual alternative with a smaller-index option | Matryoshka truncation mainly reduces vector/search cost; use its task formatting and supported numeric types |
| BGE-M3 | 1024-dimensional dense vectors; up to 8192 tokens; 100+ languages | Stronger long-input or hybrid reference | Dense, sparse and token-level multi-vector modes have different costs and index needs |
| Qwen3-Embedding 0.6B / 4B / 8B | Up to 1024 / 2560 / 4096 dimensions; 32K context; variable output dimensions | GPU quality/cost ladder for corpus encoding or selective document rescoring | Long context and larger vectors are optional costs; follow its query instructions and last-token pooling |
| Bekko a8m | Compact contextual encoder; author emphasizes 7.7M non-embedding active parameters | Recent CPU candidate | Active parameters exclude the large vocabulary table; evidence remains author-reported; see [frontier](frontier.md#compact-contextual-embedders) |

**Effectiveness grades.** E5's benchmark tables are `benchmark-reported`;
the other model-card comparisons are author-reported, not local reproduction.
Static pooling is a credible speed mechanism, but this survey establishes no
particular speedup or acceptable loss for the user's languages. Bekko's measured
CPU comparison does not include E5-base, so it cannot establish a direct win
over the incumbent. The [Qwen3 digest](concepts/gpu-quality-encoders.md) `[G]`
adds a GPU-oriented family with `benchmark-reported` multilingual results.
Those results motivate a comparison; they do not establish a gain over
E5-base on acquired training data or justify encoding every document with 8B.

**CPU cost has several independent levers.** Shorter valid chunks, length-aware
batching, a smaller contextual network, and an attention-free static model
change encoding work. ONNX/OpenVINO and weight quantization change execution.
Lower-dimensional or quantized output vectors change storage and search work.
Do not report an index compression ratio as an embedding speedup. Sentence
Transformers' [efficiency documentation][efficiency] documents the backend
options; numerical parity and end-to-end recall still need checking on the
selected model. For example, the EmbeddingGemma card explicitly excludes
float16 activations.

## Sentence, paragraph and document retrieval

**Proposed default:** index paragraph-sized chunks that fit the encoder, retain
sentence offsets and parent-document identity, and retrieve with several chunks
from the new document. Sentence vectors expose local terminology and specific
examples; paragraph vectors retain more context. One document mean is cheap
but can erase a rare relevant section. A long context window avoids some
truncation, but does not remove the information bottleneck of a single vector.

Keep aggregation explicit. A maximum over query-chunk similarities detects
one strong match but favors long documents with many opportunities. A mean
requires broad similarity and can suppress a small relevant passage. Top-few
chunk aggregation and a per-parent candidate cap are useful controls. These
are design choices to test, not a literature-established best policy.

For interest across documents, compare individual exemplar queries and a small
set of interest prototypes before averaging every document into one centroid.
Combine a persistent profile with the current document, and retain an
exploration/random component so weakly represented interests can still enter.
Recency weights and negative feedback change the target; merely opening a
document is ambiguous evidence of preference. Embedding arithmetic across
queries must stay inside one compatible model space.

E5 distinguishes asymmetric retrieval (`query:` versus `passage:`) from
symmetric similarity (the card specifies `query:` on both sides). A document
used to find training text might be either. Preserve the existing baseline
first, then test that choice explicitly; do not silently change prefixes while
claiming to compare encoders.

## Index technology and the cost of a coarse stage

FAISS is an index library, not an embedder or a complete document store.
Its [documentation][faiss] covers exact search, graph search, inverted lists,
product quantization and binary vectors. Keep text, provenance and metadata
addressable by stable IDs outside the vector payload.

| Index family | Suitable starting regime | What to measure or preserve |
|---|---|---|
| FAISS Flat inner product | Bounded corpus; exact reference; batched search | Full-vector scan cost; with normalized vectors this ranks cosine similarity |
| FAISS HNSW | RAM-resident approximate retrieval; existing local implementation | Graph memory, build cost, search breadth and recall against Flat |
| FAISS IVF-Flat | Larger corpus with representative clustering/training data | Number of lists searched versus recall; full vector storage remains |
| FAISS IVF-PQ | Vector payload is a memory bottleneck | Both coarse-list misses and quantization error; retain original vectors for short-list rescoring if affordable |
| ScaNN | CPU approximate maximum-inner-product search alternative | Benchmark the actual workload and backend; anisotropic quantization is its distinguishing approach |
| DiskANN | Corpus too large for economical RAM-only serving | SSD I/O, cache, build resources and tail latency |
| Qdrant | A service needs metadata filtering and vector search together | Filter-aware recall, persistence and operational cost; it changes the serving layer as well as search |

The ScaNN, DiskANN and Qdrant rows are supported by their
[primary implementation descriptions](related-work/search-notes.md#implementation-sources)
`[R]`; no cross-library winner is claimed. Tight filtering deserves its own
test: retrieving globally and discarding forbidden languages or sources can
leave too few valid candidates. Partitioning or filter-aware search changes
that behavior.

**Derived payload sizes:** one million 768-dimensional float32 vectors occupy
3.072 GB; 384-dimensional float32 vectors occupy 1.536 GB; 768-dimensional
int8 vectors occupy 0.768 GB. These decimal byte calculations exclude graph
edges, IDs, quantizer tables, allocator overhead, text and metadata. Saving
float16 embeddings on disk does not imply a float16 FAISS index: the existing
local HNSW builder converts its inputs to float32.

Distinguish two losses: approximate search may miss neighbors in a *fixed*
space; a cheaper encoder may rank different neighbors even with exact search.
Measure them separately before measuring their combined cascade. Recomputing
scores can fix approximate distances among retrieved items; it cannot recover
items the candidate generator never returned.

## One-host corpus-scale accounting

**Derived sizing example, not a dataset inventory:** 300 GB of decompressed
text divided into chunks averaging 2,000 UTF-8 bytes gives about 150 million
vectors before overlap. The bytes/token ratio varies by language and tokenizer;
compressed download size is not interchangeable with text size. Deduplication,
short-document tails and chunk overlap can materially change the count. Count
actual post-policy chunks in a representative streamed sample before extrapolating.

| Stored representation | Bytes per vector | Payload at 150 million vectors |
|---|---:|---:|
| E5-base float32 | 3,072 | 460.8 GB |
| E5-base float16 sidecar | 1,536 | 230.4 GB |
| 256-dimensional float16 sidecar | 512 | 76.8 GB |
| 64-byte PQ code plus 64-bit ID | 72 | 10.8 GB |

These are decimal payload arithmetic, excluding index metadata, coarse
centroids, search/build scratch, allocator overhead and the source text. The
float16 sidecars are storage choices, not promises that every index consumes
that representation directly. A default full-vector HNSW index adds a graph
to an already large payload; it is not the natural starting assumption for
the full scenario. IVF-PQ or a disk-backed index deserves the first full-scale
capacity analysis. PQ code length is a recall/capacity choice to validate;
64 bytes is illustrative, not an established setting.

**One GPU need not hold the corpus.** Stream text through a GPU encoder,
persist sharded vectors and IDs, and use CPU RAM/SSD for the index and optional
full-vector sidecars. Train IVF/PQ on a representative language/domain sample,
then add shards incrementally. Preserve document and chunk locators so a hit
does not require rescanning compressed corpus files. Checkpoint encoding by
stable shard/chunk IDs with model revision and segmentation metadata; this
turns an interrupted build into resumable work instead of a complete rebuild.
These are proposed engineering choices, not an implementation landed here.

FAISS [GPU documentation](https://github.com/facebookresearch/faiss/wiki/Faiss-on-the-GPU)
describes Flat and IVF-family GPU indexes, host/device input interoperability
and temporary GPU memory. A compressed index may fit alongside the encoder,
but the payload estimate alone does not prove that fit. Reserve memory for
weights, activations and scratch; serializing encoding and index building may
be preferable on one GPU. CPU search with GPU encoding/reranking is also valid.
GPU Flat is an exact reference or batched scan option, not automatically a
low-latency full-corpus service. Measure transfers and SSD reads as well as
kernels. Actual VRAM, host RAM and SSD capacity remain unspecified.

**Build-time accounting:** let T be the encoder's actual processed token count,
including overlap, and R its measured end-to-end tokens/second at the chosen
batching, precision and length distribution. Encoding time is approximately
T/R; add source reading, tokenization, vector writes and index construction
where they are not overlapped. A GPU upgrade over a CPU E5 baseline is an
execution comparison; changing to another encoder is a separate quality
comparison. Do not multiply a short-sentence benchmark rate by long web-text
volume without a representative throughput measurement.

### When to pay for quality up front

Compare **H**, a high-quality corpus encoder indexed up front, with **L**, a
cheap corpus encoder followed by high-quality document embedding on retrieved
candidates. Use one cost unit consistently: elapsed time under a stated
schedule, GPU-hours, or money. The following additive model is a planning
approximation, not a throughput measurement:

```text
C_H(Q) = B_H + Q * l_H
C_L(Q) = B_L + U(Q) * c_H + Q * l_L
```

B includes corpus encoding and index construction. Q counts retrieval requests
over the index's useful lifetime (including multiple query chunks per input).
c_H is the cost of strongly embedding one candidate chunk. U(Q) counts distinct
candidate chunks needing that work after cache hits. l includes query encoding,
search, fetch, score computation and any pairwise reranking, excluding the
separately counted strong document encoding. For L, query encoding includes
both spaces if needed. With a complete persistent cache,
U(Q) ≤ min(N, QK), where N is corpus chunks and K is candidates per request;
eviction or encoder revisions can cause recomputation.

Without caching, U(Q)=QK. When l_L + K*c_H > l_H, the break-even query count is
approximately (B_H−B_L)/(l_L + K*c_H−l_H). If the denominator is nonpositive,
there is no eventual amortization advantage for H from this model alone.
Rebuilds shorten the amortization horizon; repeated interests and a growing
cache can greatly extend it. Account for shared GPU contention with annotation
or training rather than treating its time as free.

**Illustrative algebra:** ignoring other costs and cache hits, let N=150M,
K=2,000 and the cheap encoder cost one tenth as much per chunk as the strong
one. Then Q* ≈ N*(1−0.1)/K = 67,500 requests. This is not a forecast: every
cost ratio, candidate count and workload assumption needs measurement. With
caching, strong-encoding work instead approaches corpus coverage; a narrow
interest distribution can keep U(Q) far below N even over many queries.

A cross-encoder's joint query–document scores usually cannot use that document
embedding cache across different queries. Charge their pairwise cost per
request in l, and use the same reranking policy in a fair comparison unless
the better index demonstrably allows a smaller pool. A fully strong index can
still benefit from reranking. Conversely, lazy strong embeddings improve only
the cheap index's returned pool: they do not recover globally missed regions.
Compare costs at matched useful yield and retention, not merely at equal K.

**Practical routes:** infrequent queries or rapidly changing interests favor
testing cheap indexing with cached strong rescoring. Repeated broad queries
against a stable corpus make up-front strong encoding more plausible. A
middle route uses a strong encoder once, compresses its index aggressively,
and retains higher-precision vectors on SSD for rescoring. This separates
semantic quality from RAM footprint. Matryoshka output truncation offers a
similar storage/search trade-off without eliminating the initial transformer
forward pass. Exact rescoring of PQ candidates still cannot fix candidate
misses, so evaluate the full cascade.

## Spend expensive checks on marginal usefulness

The proposed cascade is:

1. Cheap multilingual retrieval of a generous candidate pool, optionally
   unioned with lexical or metadata retrieval to recover rare terms.
2. Cheap language, extraction, source, duplicate and parent-document checks.
3. E5-base or a stronger encoder rescoring; optionally a multilingual
   cross-encoder on the remaining pool.
4. Redundancy-aware selection and task-relevant utility checks before buying
   annotation or running adaptation.
5. Short downstream adaptation with a frozen control and retention checks.

A cross-encoder jointly reads query and passage. It may improve relevance
ranking but does not directly estimate training benefit. In a span-tagging
application, domain similarity alone also misses whether a passage contains
useful entity types, boundary cases, label support or errors the model can
learn to repair. The [distillation survey](../distillation/survey.md) owns the
adjacent acquisition and learnability literature.

**Noise tolerance is stage- and objective-dependent.** Irrelevant rough
candidates mainly waste rescoring. Some off-domain training examples may add
coverage. Wrong pseudo-labels, systematic language omissions and repeatedly
selected near-duplicates can instead reinforce errors or concentrate updates.
Do not infer equal tolerance from the word “noise.” Retain a random control
and inspect score-stratified samples rather than only the most convincing hits.

For a candidate (x), the decision quantity is approximately expected
downstream gain per annotation-plus-update cost, including redundancy with
already selected examples. Cosine relevance is a cheap proxy for one component.
Deduplicated nearest neighbors are therefore a stronger baseline than raw
top-k. A relevance–diversity trade-off can be tested before a more elaborate
selector.

[SIFT][sift] `[R]` formalizes selection as reducing uncertainty at the target
in a fixed embedding surrogate, rather than repeatedly choosing highly similar
examples. Its Pile language-modeling experiments report an advantage over
nearest-neighbor selection (`single-source`). The repeated-nearest-example
failure control is deliberately pathological and should not be confused with
ordinary deduplicated top-k. The surrogate assumptions and bits-per-byte
evaluation do not establish the best selector for multilingual annotation.

## Adapting the retrieval encoder

[GPL](concepts/retriever-adaptation.md) `[G]` is the central label-scarce
reference: generate queries for domain passages, mine candidate negatives,
score query–passage pairs with a cross-encoder, and fit the bi-encoder to teacher
score margins. This is more specific than continued language-model training
on domain text. Its six-domain DistilBERT evidence is `single-source` and does
not establish an incremental gain over current multilingual E5-base.

Its negative results matter: hard negatives hurt the simpler query-generation
baseline when treated as certainly irrelevant; the teacher's soft relevance
scores address false negatives. Several generic unsupervised pretraining
recipes did not improve retrieval under the paper's setup. A lower masked-LM
loss is consequently not enough to qualify a better retriever.

With trusted local query–passage or preference labels, direct contrastive or
ranking fine-tuning is simpler. With only a new document, self-supervision can
be too weak or too narrow; prefer a frozen query/profile change or a temporary
downstream adapter first. Avoid training the retriever solely to reproduce its
own nearest-neighbor decisions. When multilingual preservation matters, retain
cross-language positive pairs and non-domain retrieval examples, not just
unlabeled general text with an unrelated objective.

## Per-input and across-document micro-adaptation

[TTT-NN](concepts/retrieved-test-time-training.md) `[G]` retrieves neighboring
texts, takes a short sequence of language-model updates, evaluates, and resets
the model for the next input. It supplies direct prior art for adapting on
retrieved data. The original study evaluates Pile language-model likelihood;
the [later reproduction][ttt-repro] confirms gains in a subset of that regime
but also reports degradations for some GPT-Neo/domain combinations. The
qualified claim is `reproduced` for selected language-modeling settings,
not for arbitrary tasks or persistent personalization.

Compare three lifetimes explicitly:

- **Per-document reset:** start from the same model and optimizer state;
  adapt on retrieved training material; process the document; discard changes.
- **Session/user adapter:** carry small updates across documents; periodically
  test retention, decay or reset; isolate it from the shared base.
- **Persistent domain update:** consolidate only after validation across the
  intended domain, languages and general capabilities.

Adapters/LoRA reduce trainable state and make reset or routing convenient;
their active outputs can still forget. An immutable base is a fallback, not
proof that an enabled adapter preserves every skill. Short trajectories reduce
exposure but do not bound damage unless learning rate, repeated examples and
update norm are also controlled.

**Prediction boundary:** for causal continuation, retrieve using only the
available prefix, never the future suffix being scored. For full-document
tagging, the input document is available, but its held-out labels are not.
Transductive use of evaluation text to choose training data must be declared
and compared separately from source-disjoint acquisition. TTT-NN explicitly
tests a prefix-retrieval/suffix-evaluation variant; its main whole-sequence
results should not be silently relabeled as that variant.

## Anchors against forgetting

Keep the original model θ₀ fixed as the reference. A useful comparison family is

\[
L(\theta)=(1-r)L_{\rm domain}+rL_{\rm general}
 +\lambda_w\sum_i a_i(\theta_i-\theta_{0i})^2
 +\lambda_f\,\mathbb E_{x\sim A}D(f_{\theta_0}(x),f_\theta(x)).
\]

Here (r) is the general-data share under a declared sampling/loss convention;
(a_i=1) gives an isotropic starting-point penalty, and importance weights
give an EWC-style alternative. (A) is a function-anchor set. This is a menu
of controls, not a proposal to turn every penalty on simultaneously.

| Control | What it protects | Principal limitation |
|---|---|---|
| General-data replay | Behaviors actually exercised by the sampled data and objective | English-heavy or task-mismatched replay does not protect all languages/tasks |
| L2-SP: distance from θ₀ | Parameter proximity to the pretrained model | Weight proximity is only a proxy for retained behavior; ordinary decay toward zero is different |
| EWC/Fisher-weighted proximity | Parameters important under an old-task importance estimate | Estimation/storage cost and an approximate local curvature model |
| Frozen-teacher output anchors | Predictions on the anchor distribution | Cannot protect unsupported regions; teacher mistakes are also preserved |
| Embedding/score anchors | Old coordinates or old rankings on selected pairs | Pairwise geometry alone can permit a rotation incompatible with a frozen index |
| Short, resettable trajectory | Limits duration and prevents accumulation across episodes | A few aggressive updates can still hurt within an episode |
| Base–adapted interpolation | A post-training adaptation/retention trade-off | Must validate the interpolation; see [checkpoint averaging](../checkpoint-averaging/survey.md) |

The [replay and parameter-anchor digest](concepts/forgetting-controls.md) `[G]`
separates the evidence: Ibrahim et al. study large continual language-model
pretraining, whereas Li et al.'s L2-SP experiments are convolutional vision
transfer. Neither directly establishes a multilingual retrieval recipe.
[Learning without Forgetting][lwf] `[R]` supplies the frozen-output principle;
its original setting is also vision. For embeddings, use a suitable vector or
ranking loss rather than applying KL divergence to arbitrary coordinates.

**Replay baseline:** compare (r=0), a modest share such as 5%, and a larger
share such as 20% if retention degrades. These are proposed starting contrasts,
not a universal optimum. The continual-pretraining study explicitly compares
several shares and uses 5% and 25% in its selected weak- and strong-shift
conditions. Hold total training tokens/compute fixed when asking about the
trade-off; otherwise replay buys extra compute. Report actual sampled tokens
as well as nominal mixture weights. The PII program's existing human-gold
share is a separate contract and is not replaced by this survey's example.

For retention across languages, stratify anchors by language, domain, length
and task; include cross-language pairs and useful negatives. Keep a disjoint
retention evaluation set: repeatedly fitting anchors and evaluating those same
items establishes memorization of the anchor set. For old-index compatibility,
evaluate new query vectors against the actual frozen old document vectors.

## Contested results, negative results and baseline sensitivity

- **Nearest neighbors versus useful adaptation data.** TTT-NN establishes
  benefits in selected likelihood tasks; its reproduction also has negative
  cells. SIFT attacks redundancy. These concern different claims, rather than
  proving that nearest-neighbor adaptation always works or always fails.
- **Dense semantics versus lexical coverage.** GPL's original MS-MARCO-trained
  dense baseline was weak under domain shift. Its gains cannot be transferred
  numerically to E5-base. Include lexical retrieval, a frozen modern encoder,
  random draws and deduplicated top-k before crediting a new selector.
- **More adaptation can be worse.** GPL's small-corpus ablation includes a
  condition below its zero-shot baseline; false hard negatives hurt QGen.
  TTT-NN's dynamic-evaluation comparator overfits after a few steps. These are
  concrete counterexamples to “short” or “domain data” guaranteeing benefit.
- **More elaborate anchors are not automatically better.** L2-SP's vision
  study did not find a significant target-accuracy advantage from Fisher
  weighting over its isotropic penalty. It did not settle retention for text
  embedders; keep the cheap baseline in that comparison.
- **Leaderboard means can conceal the failure of interest.** Translation-pair
  alignment, native domain retrieval, rare-language coverage and downstream
  annotation yield are different outcomes. Inspect each; no universal
  embedder/index ranking is established here.
- **Larger models and reranking have task-specific losses.** Qwen3's own
  reranking comparison includes code-retrieval loss for its small reranker and
  an instruction-following result where 4B exceeds 8B. See the
  [GPU-family digest](concepts/gpu-quality-encoders.md); better corpus coverage
  and better reranking are separate hypotheses.

## A bounded test that could change the choice

This is an evaluation design, not a launched or selected program recipe.

1. **Freeze the population and baseline.** Pin E5-base revision, prefixes,
   pooling, truncation, normalization, segment IDs, FAISS type/parameters and
   source exclusions. Use exact E5-base search on the bounded evaluation slice
   to isolate approximate-index loss.
2. **Test languages and granularity.** Include same-language and cross-language
   queries, short sentences and mixed-topic documents, high- and low-resource
   languages, and rare relevant passages. In the existing PII proposal, MAPA
   is useful for parallel alignment, but its translations must be grouped by
   original document; it is not evidence of native clinical/legal diversity.
3. **Measure the cascade.** Compare candidate counts (K/k=2,5,10) for a final
   selection of (k); count both E5 reference-neighbor coverage and judged
   useful material. Audit downstream cost at matched useful yield. The proposed
   10–50% keep fraction is a test range, not an established threshold.
4. **Separate acquisition from adaptation.** First compare random versus
   retrieved-versus-diversified data with the same downstream update recipe
   and annotation-token budget. Then compare no update versus short resettable
   updates. Only then test persistence and retention controls.
5. **Report the costs actually paid.** Cold and warm encoding, tokens/second,
   batch-one latency, resident memory, bytes/vector, index build/search,
   rescoring, annotation and training; state hardware, threads, backend,
   precision and sequence-length distribution. Include re-embedding amortized
   over the query/update horizon if the retriever changes. Extrapolate chunk
   count, build time and RAM/SSD/VRAM from a representative streamed sample;
   evaluate lifetime cost over several Q values and cache-hit rates, including
   cheap-index, strong-index and strong-compressed-index routes.
6. **Select against joint constraints.** Require acceptable downstream gain,
   general retention and per-language floors on disjoint data. Use paired
   per-document comparisons and uncertainty estimates, grouping translations
   and correlated chunks. Publish positive and negative strata together.

Language-centering, using the tagger's pooled hidden states, and learning a
user-specific query projection remain ablations. In particular, subtracting
per-language means can remove useful semantics or move the spaces apart; do
not treat it as an automatic repair for language-dominated neighbors.

[efficiency]: https://sbert.net/docs/sentence_transformer/usage/efficiency.html
[faiss]: https://faiss.ai/
[sift]: https://arxiv.org/html/2410.08020v3
[ttt-repro]: https://arxiv.org/html/2511.16691v1
[lwf]: https://arxiv.org/html/1606.09282
