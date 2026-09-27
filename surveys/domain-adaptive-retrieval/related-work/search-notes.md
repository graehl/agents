# Search and source record

**Grounded, bounded search through 2026-09-27.** Anchors: multilingual E5,
GPL and test-time training on nearest neighbors (TTT-NN). Sources were primary
arXiv HTML, ACL Anthology, authors' model cards, official implementation
documentation and OpenAlex citation metadata. Search saturation was not reached;
this is an engineering-oriented slice, not an exhaustive review or a novelty
claim. No new performance measurements were made.

## Discovery and disconfirmation

OpenAlex resolved GPL through `filter=title.search:Generative Pseudo Labeling`.
The principal record was `W4200635123`; a second record, `W4303684020`, describes
the same work and was not counted as another paper. Citation counts are
discovery signals only. The principal record had 75 citations at lookup; other
papers' counts were not systematically collected.

The GPL forward pass queried both `cited_by_count:desc` and
`publication_date:desc`, 12 results each:

- [Impact-sorted citers](https://api.openalex.org/works?filter=cites:W4200635123&sort=cited_by_count:desc&per-page=12).
- [Recent citers](https://api.openalex.org/works?filter=cites:W4200635123&sort=publication_date:desc&per-page=12).

The impact pass surfaced HyDE, UDAPDR, COCO-DR and a dense-retrieval survey;
the recent pass included applied retrieval and synthetic-data/listwise
distillation work. These were discovery leads, not full-text evidence used to
rank methods here. Forward-citation coverage remains incomplete for the other
two anchors. Backward inspection followed E5's alignment/bitext comparisons,
GPL's query generation and false-negative baselines, and TTT-NN's dynamic
evaluation and retrieval-augmented comparators.

Fresh searches combined multilingual retrieval, small/CPU/static embeddings,
domain adaptation, nearest-neighbor test-time training, active fine-tuning,
replay and forgetting. They located SIFT, the TTT-NN reproduction and Bekko.
Microsoft's E5 work, the GPL authors' retrieval line and the Hardt/Sun and
Hübotter/Krause adaptation lines supplied relevant author/group anchors; their
identity is a relevance prior, not verification of a result.

The disconfirming pass examined GPL's false negatives, small-corpus and
unsupervised-training ablations; negative model/domain cells in the TTT-NN
reproduction; SIFT's distinction between ordinary nearest neighbors and the
pathological repeated-nearest comparator; replay's adaptation cost at fixed
tokens; and L2-SP's comparison with Fisher weighting. Model-card specifications
were checked separately from speed claims. No independent CPU comparison on
the user's workload was located or performed. This search does not establish
that newer or omitted models are inferior.

The user's one-GPU, few-hundred-GB scenario added a GPU-quality pass over the
Qwen3 Embedding primary report and E5-large card, plus current official FAISS
GPU documentation. This extended the map from cheap candidate generation to
up-front encoding versus query-time rescoring and caching. Qwen3's own
reranking table contains negative task/size comparisons; these bound the
larger-is-better interpretation. Corpus payload and break-even figures in the
map are explicitly derived scenarios, not measurements of FineWeb or FiNERweb.

## Accepted full texts and read scope

`papers.yaml` is the citation manifest. Each accepted text has an engine-written
`.fetched` record with source URL, extraction method, hashes and fidelity
validation. The concept pages identify the sections read; an accepted full-text
archive does not imply that every reference or table was exhaustively audited.
Qwen3's text and two scientific figures are archived; one branding logo is
omitted by the engine's escaped-alt image parser. The shared fidelity gap
records that limitation even though the engine's audit passes.

| Source | Contribution relative to the anchors | Main read scope |
|---|---|---|
| Multilingual E5 report | Establishes the incumbent family and distinguishes retrieval from cross-language alignment | Training, evaluation and implementation appendix |
| GPL | Retrieval-specific target-domain supervision from generated queries and teacher margins | Method, setup, baselines and ablations |
| TTT-NN | Uses retrieved text to adapt the downstream model per input | Index, update/reset protocol, evaluation and limitations |
| TTT-NN reproduction | Tests the original procedure and bounds its model/domain generality | Dataset coverage, result tables and extension limitations |
| Continual-pretraining study | Tests replay and learning-rate schedules beyond isolated episodes | Fixed-compute replay definition and weak/strong shift results |
| L2-SP | Formalizes a starting-weight prior distinct from ordinary weight decay | Regularizers, freezing/Fisher comparisons and discussion |
| Qwen3 Embedding | Adds a GPU-oriented encoder/reranker family and variable output dimensions | Architecture, training, evaluation settings, main tables and ablations |

The shared engine was invoked through
`uv run --with pyyaml scripts/related-work --dir surveys/domain-adaptive-retrieval`.
Use its `audit`, `status` and selective `fetch <key>` verbs to inspect or refresh
the corpus. The plain system-Python invocation lacked PyYAML in this session.

## Read online, not accepted as local extracts

- **SIFT:** full primary HTML read for selector, assumptions, experiments and
  nearest-neighbor controls. Extraction rejected 14/583 source blocks
  (minimum coverage 0.200).
- **Bekko:** primary HTML read for architecture, CPU comparison and limitations.
  Extraction rejected 6/430 blocks (minimum coverage 0).
- **EmbeddingGemma card:** primary model documentation read for dimensions,
  input length, formatting and supported precision. Extraction rejected 1/61
  blocks (minimum coverage 0.500), including navigation text.

These remain `grounded: false` in the manifest, with verified source links.
The failures are recorded in the shared
[fidelity gap](../../../gaps/related-work-math-html-fidelity.md). No gate was
weakened and no failed extraction was marked complete. Learning without
Forgetting was also read online for its frozen-output distillation principle;
local extraction was not attempted.

## Implementation sources

Living documentation was checked on 2026-09-27. These sources support interface
and representation specifications, not an independently reproduced speed or
quality ordering. Model names should be pinned to revisions in any experiment.

| Primary source | Used for |
|---|---|
| [E5-base card](https://huggingface.co/intfloat/multilingual-e5-base) and [E5-small card](https://huggingface.co/intfloat/multilingual-e5-small) | Dimensions, token limits, pooling, normalization and task prefixes |
| [E5-large card](https://huggingface.co/intfloat/multilingual-e5-large) | Larger incumbent-family comparison: dimensions and context limit |
| [Qwen3 0.6B card](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B) and [4B card](https://huggingface.co/Qwen/Qwen3-Embedding-4B) | Model sizes, variable dimensions, task formatting and GPU execution examples |
| [Multilingual MiniLM card](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2) | 384-dimensional output and configured 128-token limit |
| [Potion multilingual card](https://huggingface.co/minishlab/potion-multilingual-128M) | Static pooling, 256 dimensions and 101-language training claim |
| [EmbeddingGemma card](https://huggingface.co/google/embeddinggemma-300m) | Context length, Matryoshka dimensions, task formatting and numeric types |
| [BGE-M3 card](https://huggingface.co/BAAI/bge-m3) | Dense/sparse/multi-vector modes, dimensions and context window |
| [Sentence Transformers efficiency](https://sbert.net/docs/sentence_transformer/usage/efficiency.html) | ONNX/OpenVINO execution and quantization options |
| [FAISS documentation](https://faiss.ai/) | Exact and approximate index families, metrics and compression |
| [FAISS GPU documentation](https://github.com/facebookresearch/faiss/wiki/Faiss-on-the-GPU) | GPU index families, interoperability and scratch-memory requirements |
| [Google ScaNN introduction](https://research.google/blog/announcing-scann-efficient-vector-similarity-search/) | Approximate inner-product search and anisotropic quantization |
| [Microsoft DiskANN project](https://www.microsoft.com/en-us/research/project/project-akupara-approximate-nearest-neighbor-search-for-large-scale-semantic-search/) | SSD-backed large-scale approximate search |
| [Qdrant filtering documentation](https://qdrant.tech/documentation/search-patterns/vector-search-filtering/) | Metadata-filtered vector search |

## Local context

The user identified multilingual E5-base into FAISS as the earlier baseline.
Read-only inspection of `~/draft` confirmed it at revision
`a4d2334e9e6590403f431b5f5632ea99541861f1`:

- `scripts/pii_overlap_neighbors.py`: `DEFAULT_MODEL`,
  `build_faiss_database`, and index/search arguments. The builder uses
  `IndexHNSWFlat` with inner product and converts stored embeddings to float32.
- `data/pii-annotations/overlap-audits/openner-commercial-core-conservative-lineage-v1/README.md`:
  historical audit distinguishes HNSW candidate lookup from final blocked exact
  cosine scoring. Its timings are historical measurements, not this survey's
  benchmarks and not a domain-acquisition acceptance threshold.
- `research/pii/frontier/gaps/multilingual-domain-intake-and-retrieval.md`:
  owns the proposed native-language acquisition and two-stage retrieval tests,
  including MAPA alignment checks and stronger rescoring. Those proposals and
  the program's existing human-gold mix remain in their owning project.

This survey changes no draft implementation, dataset, queue or run policy.
