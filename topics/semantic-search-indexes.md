# Semantic search indexes

> Local vector and lexical indexes for retrieving agent context, with package
> choices, capacity accounting, and a separation between search and memory policy.

Topic: `semantic-search-indexes`
Glossary: semantic search indexes

## Local packages are the default

graehl does not want to pay for a hosted semantic-search service for personal
use and does not have a terabyte-scale corpus. Start with local packages such
as FAISS; consider a managed service only if a changed requirement justifies
reopening that choice. This is a deployment preference, not a measured claim
that a particular package meets every workload.

This topic is a practical selection note based on documentation checked on
2026-10-16, not a package benchmark or a new field survey. The existing
[domain-adaptive retrieval survey](../surveys/domain-adaptive-retrieval/survey.md)
owns the broader encoder, index-family, corpus-sizing and adaptation discussion.

## Choose the retrieval components separately

An embedding model defines the representation; a vector index searches that
representation. Text, paths, revisions and other metadata need an addressable
store. An agent then decides which retrieved material to read and use.

- **FAISS** is the natural vector-index baseline when the application already
  owns document storage and updates. Its exact Flat indexes provide a reference
  before introducing approximate nearest-neighbor search. HNSW trades graph
  memory for search speed; IVF searches selected clusters; product quantization
  compresses vectors at a potential accuracy cost. Choice depends on query
  volume, latency and memory, including index-building cost. See the
  [FAISS selection guide](https://github.com/facebookresearch/faiss/wiki/Guidelines-to-choose-an-index)
  and the survey's
  [index-family comparison](../surveys/domain-adaptive-retrieval/survey.md#index-technology-and-the-cost-of-a-coarse-stage).
- **SQLite FTS5** supplies a local lexical-search baseline with BM25 ranking.
  It can complement a FAISS index while SQLite holds chunk IDs, text and
  metadata. That pairing leaves synchronization and hybrid ranking to the
  application. [FTS5 documentation](https://sqlite.org/fts5.html)
- **LanceDB's open-source embedded library** is a candidate when maintaining
  separate vector and text stores would add unnecessary plumbing. It supports
  local vector and full-text search; verify the required update and filtering
  behavior before selecting it.
  [Project description](https://github.com/lancedb/lancedb),
  [full-text search documentation](https://github.com/lancedb/docs/blob/main/docs/search/full-text-search.mdx)

Lexical retrieval remains useful for identifiers, literal error messages and
rare names. Semantic retrieval can find relevant passages whose wording differs
from the query. A hybrid candidate pool can combine both; raw BM25 and vector
scores are not automatically comparable. Rank fusion or a second-stage
reranker is a choice to evaluate, not a prerequisite for the first useful tool.

## Size by chunks and vectors, then measure the actual task

Source-file bytes alone do not determine index size. Chunking and overlap set
the number of vectors; dimension and representation determine their payload.
For float32 vectors, payload alone is \(4Nd\) bytes for \(N\) vectors of
dimension \(d\). One million 768-dimensional vectors therefore occupy
3.072 GB in decimal units, before graph edges, IDs, text, metadata, build
scratch or model memory. This is arithmetic, not a RAM measurement.

Start with exact search when its measured latency is adequate. Introduce an
approximate or compressed index when a concrete capacity or latency constraint
requires it. The existing survey covers
[larger single-host sizing](../surveys/domain-adaptive-retrieval/survey.md#one-host-corpus-scale-accounting);
being below a terabyte does not by itself guarantee a RAM-resident index.

Separate three evaluation questions:

1. **Index accuracy:** does approximate search recover the exact neighbors in
   the same embedding space? Hold the vectors and eligible corpus fixed.
2. **Retrieval usefulness:** do those neighbors contain the needed evidence?
   An exact index cannot repair an unsuitable embedding model or chunk policy.
3. **Agent benefit:** does access to retrieval improve task success, time or
   token use compared with the existing grep, navigation and curated-context
   baseline?

Include filtered queries, updates and deletions in a realistic check. Filtering
only after retrieving a small global candidate set can discard every hit even
when useful eligible documents exist. Record cold and warm latency when caching
matters, plus build time and resident memory. No universal corpus-size threshold
or cross-package winner has been established here.

## Keep the index rebuildable and memory policy explicit

Treat the index as a derived view of authoritative content. Stable document and
chunk IDs should resolve to a source and revision. Record the embedding model
revision, query/document formatting, normalization and chunking policy so a
rebuild produces compatible vectors. A model change generally requires
re-embedding; matching dimensions alone does not establish compatibility.

Edits, deletions and failed indexing attempts need explicit handling so stale
chunks are not silently presented as current evidence. For a small corpus,
rebuilding and replacing an index can be simpler than maintaining complicated
incremental machinery; the acceptable rebuild time decides.

Agent memory additionally needs rules for what to retain, provenance, recency,
contradictions, superseded facts and context selection. Storing conversation
chunks and retrieving similar ones supplies a search facility; it does not
decide which past statement remains authoritative.

## Turbopuffer illustrates a different deployment need

[Turbopuffer](https://turbopuffer.com/docs/architecture) stores durable state on
object storage and caches active data in RAM and NVMe. Its centroid-based vector
index reduces object-storage roundtrips. That architecture is relevant to many
large, intermittently accessed collections, where keeping every collection
resident would be expensive. Cold latency and consistency remain material
[tradeoffs](https://turbopuffer.com/docs/tradeoffs).

The personal-use decision is to use local packages, even though the hosted
architecture has technical substance. Its cost and latency claims do not
establish better semantic relevance. Likewise, Cursor's
[semantic-search evaluation](https://cursor.com/blog/semsearch) tests access to
semantic retrieval with its custom embedding model and pipeline; it does not
isolate a benefit from choosing turbopuffer over another vector index.

A future agent-retrieval survey would ask when semantic or hybrid search adds
value over grep, file navigation and curated memory. A search-engine survey
would instead compare storage, filtering, update and serving costs. Neither
survey nor a tool implementation is implied by this topic's creation.
