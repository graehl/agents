# Compression and storage as independent choices

Grounded source facts: [Xiph's full Opus settings](https://wiki.xiph.org/Opus_Recommended_Settings)
([local extract](../related-work/extract/opus-settings/Opus_Recommended_Settings.md))
recommend 24 kb/s for mono audiobook/podcast material and lossless formats
for lossless archiving. [MLS's release page](https://www.openslr.org/94/)
([local extract](../related-work/extract/mls-downloads/94/index.md))
provides both FLAC and smaller Opus downloads. These facts support considering
Opus, not declaring it equivalent for every learning objective.

An acoustic-domain encoder may attend to exactly the noise/reverb/spectral
detail that a codec changes. A semantic encoder can tolerate that detail while
still failing on lexical content. Test both representations against their own
target metrics before choosing a corpus-wide rate. Preserve compressed source
bytes to avoid unnecessary tandem encoding; FLAC cannot reverse upstream loss.

The storage proposal separates source audio from derived intervals and vector
geometry. [Parquet's format documentation](https://parquet.apache.org/docs/file-format/)
describes a columnar batch representation; [WebDataset](https://github.com/webdataset/webdataset)
describes a sequential sample-shard layout; [pgvector](https://github.com/pgvector/pgvector)
provides database vector indexing. They solve different access patterns and do
not replace one another. These pages were read online, not accepted into the
local extraction corpus.

Retain immutable recording identities and checksums, a catalog of segment
sample coordinates with conversion recipes, and separately versioned embeddings.
Training shards and nearest-neighbor indexes are rebuildable views. Codec
seek/pre-roll and arbitrary segment requests must be addressed before assuming
one long compressed recording has the random-access behavior of clip files.

The [map's accounting](../survey.md#compression-intelligibility-is-not-representation-preservation)
gives payload sizes and explicit unmeasured candidate rates. Its
[database section](../survey.md#database-and-training-storage) gives the proposed
entity relationships and vector-size arithmetic. No storage throughput or
retrieval-performance result is claimed.
