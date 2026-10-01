# Untranscribed speech: sources, live capture, storage, and domain representations

Grounded field survey. Coverage cutoff: **2026-10-01**. Scope: multilingual
public speech, approximately 10⁴–10⁶ hours, collection without transcription,
and embeddings computed directly from audio. The target is **trainable audio
for tail-language ASR**, especially languages with few high-quality official
transcript hours. Language identification must be good enough for that use.
Legal analysis is outside scope. Primary dataset/model cards,
protocol documentation, and selected speech-representation papers were read.
Sixteen of twenty-two manifested sources have accepted local full-text extracts;
six were verified online but failed local extraction. See [retrieval and
limits](#retrieval-and-limits) for the exact boundary. No audio collection,
codec experiment, or embedding benchmark was run.

## Decisions this survey supports

For the stated tail-language objective, prioritize **MMS ulab v2 for a broad
language seed**, **regional/community radio and local-language web channels
for additional natural speech**, and **YODAS v3 for existing varied web audio**.
VoxPopuli and Libri-Light are useful control populations, with much narrower
language reach. These cover different populations; hours are not interchangeable.
Use a station directory to discover live endpoints rather than scraping player
pages as the primary collector.

Maintain two related products: a representative source-recording pool and
versioned span views for clean single-speaker, clean alternating-speaker, and
mixed-condition speech. Music/noise/event sounds are conditions to detect and
stratify, not reasons to discard every affected recording. See
[condition detection and span views](#condition-detection-and-span-views).

Preserve the source's compressed audio when possible. For an intentionally
re-encoded speech archive, **mono Opus at 24–32 kb/s** is a defensible initial
candidate, not an established training-quality threshold. Keep recording bytes
immutable, segments as offsets, operational metadata in a relational catalog,
batch metadata in Parquet, and embeddings in versioned arrays/indexes.

Represent **acoustic domain** separately from **subject matter**. A pooled
self-supervised speech encoder is a baseline for the former. SONAR-like direct
speech embeddings address the latter without running ASR, but their training
geometry depends on text. No located evidence establishes one universal vector
as a reliable replacement for both representations in long, noisy live speech.
These architectural choices are synthesis, not measured superiority claims.

Concept notes: [sources and capture](concepts/sources-and-capture.md),
[condition views](concepts/condition-views.md),
[compression and storage](concepts/storage-and-compression.md),
[audio domain representations](concepts/audio-domain-representations.md).
Fresh claims and unresolved tests are isolated in [frontier.md](frontier.md).

## What “no-transcript” and “domain” mean here

Three constraints have materially different solution sets:

1. **No transcript required from the data source.** Some usable releases have
   transcripts that can be ignored; others supply genuinely unlabeled audio.
2. **No ASR in the embedding execution path.** Waveform → encoder → vector is
   allowed even if pretraining used speech/text pairs.
3. **No transcript-derived training geometry.** An audio-only self-supervised
   checkpoint qualifies; a speech encoder distilled toward a text teacher does
   not. An ASR-fine-tuned checkpoint also changes this answer.

Acoustic domain comprises room, microphone, channel, noise, speaking style and
related recording conditions. Semantic domain comprises subject matter and
intent. Language, accent and speaker identity can either be targets or
confounders. Calling all of them “domain” without specifying the desired
invariances makes retrieval quality impossible to judge.

## Downloadable archives and corpora

Counts below are publisher-reported release descriptions, not independently
audited usable-speech totals. A language tag is a prior, not proof that every
window contains that language. The operative criterion is useful training
speech with sufficiently reliable language labels; legal analysis is omitted.

| Source | Audio and language coverage | Transcript dependence / bias | Retrieval / practical boundary |
|---|---|---|---|
| [YODAS v3](https://huggingface.co/datasets/espnet/yodas3) | Newly released, reported 1.1M h, 48 kHz multichannel web audio; 100+ languages. | Optional captions on about 75% of recordings. File-level caption and uploader-locale language labels differ; no-caption recordings are grouped under `unk`. | Opus/WebM in WebDataset tar shards plus per-shard Parquet metadata. Inspect metadata before deciding language-specific acquisition. Current release is a stronger representative-web starting point than v2, not a validated clean-span corpus. |
| [VoxPopuli](https://github.com/facebookresearch/voxpopuli) | Headline 400k hours, 23 languages; detailed unlabeled table totals about 384k hours. Parliamentary recordings, 16 kHz mono Ogg Vorbis. | Unlabeled release. Formal politics, interpretation, correlated events across languages; not general conversational coverage. | Direct download scripts; 400k subset about 6.4 TB. Repository archived in 2023. Limited tail-language coverage. |
| [Libri-Light](https://github.com/facebookresearch/libri-light/blob/main/data_preparation/README.md) | Nominal 60k hours English audiobooks; listed main subsets sum to 57,704 h, roughly 3.4 TB. FLAC plus book/speaker JSON. | Unlabeled read speech. Separate duplicate subset should not silently count as new coverage. Optional VAD concatenation changes the timeline. | Direct tar archives. English control population. FLAC conversion does not restore fidelity lost in original MP3s. |
| [YODAS2](https://huggingface.co/datasets/espnet/yodas2) | Video-level, unsegmented 24 kHz audio from the YODAS collection. Original [YODAS release](https://huggingface.co/datasets/espnet/yodas) describes 369,510 h in 149 languages. | Captions may be ignored. Broad topics and acoustic conditions, but selection is caption/YouTube conditioned. Internal `video_id` is not the original YouTube identifier. | HF downloadable data. Dataset streaming reads an existing archive, not current live speech. Loading-script requirements warrant checking before choosing an ingestion library. |
| [MMS ulab v2](https://huggingface.co/datasets/espnet/mms_ulab_v2) | 8,900 h raw unsegmented 16 kHz mono; reported 4,023 languages and 189 families. | Genuinely unlabeled. Global Recordings Network religious material, strongly narrow subject matter. Unknown and malformed language values appear in preview metadata. | ESPnet reproduction/extension of MMS unlabeled data. About 6,700 h after segmentation used for XEUS is not the raw-release duration. |
| [VoxLingua107](https://cs.taltech.ee/staff/tanel.alumae/data/voxlingua107/) | Reported 6,628 h in 107 languages, YouTube-derived. | Language-ID-oriented clips; heuristic labels and web selection. Useful LID material, not a balanced source of semantic domains. | Official downloads. Local extraction failed, so this row is online-source verification. |
| [Multilingual LibriSpeech](https://www.openslr.org/94/) | Eight languages, read audiobooks. English downloadable release offers FLAC 2.4 TB or Opus 651 GB. | Already transcribed; ignoring transcripts meets constraint 1 but not “never transcribed.” | OpenSLR resource **94**. Codec alternatives provide a practical released storage comparison, not proof of equal learning quality. |
| [Emilia](https://huggingface.co/datasets/amphion/Emilia-Dataset) | 101.7k h original plus 113.9k h Emilia-YODAS; six languages. | TTS-oriented processed/filtered utterances with generated text. Useful audio, but ASR and quality selection already affected the population. | Downloadable processed web speech; limited tail-language reach, useful clean-span comparator. |

**Collection opportunities beyond packaged corpora.** Internet Archive has
radio, lectures, oral histories, sermons and other heterogeneous recordings.
Its [item metadata API](https://archive.org/developers/metadata.html) gives
`GET /metadata/{identifier}`, item metadata and file records; retain original
file selection, checksums and item-level rights metadata. It is an item API,
not a wildcard collection download. The [Library of Congress JSON/YAML
API](https://www.loc.gov/apis/json-and-yaml/requests/) supports `fo=json` on
supported collections, including paths useful for oral-history discovery;
access and API coverage vary. These are discovery channels, not a verified
uniformly downloadable corpus of a stated size.

RSS podcast enclosures and newly released LibriVox books provide ongoing
archive growth. Program/feed metadata supplies cheap subject hints without ASR.
Neither is inherently live: a newly published file may contain old speech.
Avoid “web scale” totals that mix collected pools, filtered releases,
transcribed subsets, duplicate encodings and model pretraining hours. In
particular, a model's millions of training hours do not imply those hours are
publicly downloadable.

**YODAS v3 changes the acquisition order.** Its current card distinguishes 102
caption-language directories plus `unk` from 146 distinct locale-language
codes; the paper's 147-language framing is a different accounting view. For
tail-language mining, search the locale metadata and `unk` pool as well as
caption directories, then perform waveform LID. The card's audio is packaged
in roughly 8 GB tar shards with matching metadata Parquet files keyed by
recording ID. Effective bandwidth/channel estimates are useful condition
metadata, not guarantees of intelligibility or correct per-sentence language.
The [September 27 release announcement](https://huggingface.co/blog/espnet/yodasv3)
confirms 48 kHz Opus and the million-hour scope. See the
[frontier release boundary](frontier.md#yodas-v3-release-and-language-accounting).

## Current public speech: discovery and live-edge retrieval

### Direct radio is the simplest sustained starting point

[Radio Browser](https://docs.radio-browser.info/) exposes station search and
records with `stationuuid`, `url`, `url_resolved`, language fields, tags,
codec and check timestamps. `url_resolved` accounts for playlist/redirect
resolution. Use documented mirror discovery rather than permanently pinning
one mirror; the API supplies a server-list fallback. A representative search
path is `/json/stations/search?language=english&tag=news&hidebroken=true`.
Directory metadata is weak supervision: a “news” station can play music or ads,
and a successful periodic check does not establish availability now.

The recording path is directory → resolved HTTP/ICY or HLS endpoint → demux →
immutable audio chunks → VAD / LID / quality metadata. Prefer retaining the
incoming codec with a remux (`-c:a copy`) to repeated lossy encoding. Keep the
station UUID, original/resolved URL, metadata snapshot, observed connection
time, codec and discontinuities. Source URLs may expire or change.

### HLS and platform adapters

HLS can capture the **latest published stream edge**, not zero-latency reality.
Encoder buffering and segment publication are already upstream delays. A
collector should track sequence numbers, discontinuities and initialization
segments, and preserve `EXT-X-PROGRAM-DATE-TIME` when provided. Otherwise
receive UTC is an observation time, not verified broadcast UTC. Record gaps
across reconnects; don't fabricate continuity by joining timestamps blindly.

[FFmpeg's HTTP protocol](https://ffmpeg.org/ffmpeg-protocols.html) documents
`reconnect`, `reconnect_streamed`, `reconnect_at_eof` and
`reconnect_delay_max`; applicability differs for endless HTTP streams and HLS
playlist refresh. `rw_timeout` is in microseconds. Treat retry policy and
timestamp preservation as collector behavior, not merely a shell command.

For supported site players, [Streamlink](https://streamlink.github.io/cli.html)
can resolve a media URL with `--stream-url`, and retry stream discovery with
`--retry-streams`. [yt-dlp](https://github.com/yt-dlp/yt-dlp) documents
`--no-live-from-start` for current-time downloading; the opposite
`--live-from-start` is experimental on a limited platform set. Plugin coverage,
signed URLs and changing platforms make these adapters a maintenance surface.
They should follow direct endpoints in the acquisition priority. Neither tool
is a promise that every public live page is capturable.

### Transcript-free enrichment

Run speech/non-speech detection before interpreting hours as speech. Store
speech fraction, music/overlap indicators, language posterior and confidence,
and enough source metadata to inspect errors. A dedicated waveform LID model
can label windows without transcription; preserve unknown/mixed outcomes.
Station-level language is a prior, especially with interpreted programs and
code switching. Group train/evaluation splits by source/program/event and
duplicates, not random neighboring windows.

No endpoint was recorded in this survey: “live” above is a documented capability,
not measured present uptime or latency.

## Tail-language LID and acquisition priorities

[MMS LID 4017](https://huggingface.co/facebook/mms-lid-4017) is a direct
waveform language classifier with 4,017 output classes, based on a one-billion
parameter speech encoder. This coverage makes it a more relevant starting point
for the tail than the [VoxLingua107 ECAPA classifier](https://huggingface.co/speechbrain/lang-id-voxlingua107-ecapa),
whose class set contains only 107 languages. The latter remains a useful
comparison where coverage overlaps. Class-count coverage is not proof of
accurate web-audio identification for every dialect or recording condition.

For each target language, map source labels and model classes explicitly:
ISO codes, dialect labels and naming conventions can differ. Gather source
priors from regional stations, local-language channels, community programming,
podcasts and existing language-tagged archives. Prioritize **retained,
nonduplicate, correctly language-identified speech hours**, not raw bytes or
headline language counts. A religious seed can support initial LID checking
while leaving everyday conversational and broadcast coverage badly incomplete.

Apply LID to speech-bearing spans and neighboring windows, retaining top-k
probabilities, margin, cross-window consistency and the source prior. Preserve
unknown/mixed/review states. Agreement between models is supporting evidence,
not independence if their training populations overlap. Calibration needs a
small language-speaker-verified sample of accepted and rejected web spans,
including related languages, dominant-language contamination, singing and
background speech. This can be audited without producing full transcripts.

Rare-language base rates make false positives consequential. For illustration,
if true target speech is 0.1% of a pool, a detector with 90% recall and 1%
false-positive rate has precision about **8.3%**:
`0.001 × .90 / (0.001 × .90 + .999 × .01)`. These are hypothetical rates, not
MMS measurements. Source narrowing plus calibrated rejection can matter more
than another percentage point of closed-set accuracy. Restricting a classifier
to plausible labels without an unknown check can force contaminants into a
tail language.

“Quality speech” here means useful for training a model that performs ASR. It
does not mean exclusively studio-clean audio. Acoustic self-supervision can
consume broader speech; pseudo-labeling and supervised adaptation are more
sensitive to incorrect labels and severe interference. Retain condition
strata so these learning regimes can choose different subsets. Model-utility
validation will eventually require held-out target-language task evidence;
collection and condition labeling need not use ASR or text-domain embeddings.

## Condition detection and span views

### Preserve the web-audio population before selecting clean spans

Create an immutable source-recording pool with a documented sampling frame:
languages, regions, source/program families, dates and durations. A CC-captioned
YouTube release, a radio-only crawl and a religious archive are all biased
populations. “Representative web audio” must therefore name its target
population and sampling weights; it is not established by a large total.
Retain no-speech/music-only intervals where useful for condition modeling,
while counting training speech hours separately.

Derive overlapping, versioned views from that pool. Label independent axes
rather than making one mutually exclusive class per recording:

| Axis | Span-level evidence to retain | Decision supported |
|---|---|---|
| Speech presence | VAD posterior, speech duration/fraction, boundary uncertainty | Count usable speech; avoid treating music/noise as speech |
| Speakers | Framewise active-speaker count, local identity/turn boundaries, overlap probability | Separate one-speaker spans, alternating turns, and simultaneous speech |
| Background | Music/event/noise multi-label scores and coincidence with speech | Distinguish speech over a music bed, crowd/traffic/incident sound, and clean speech |
| Recording condition | Clipping, loudness, estimated interference, reverb/channel features, dropout | Filter corruption and stratify natural difficulty |
| Language | Per-span posterior, code-switch/mixed flags, temporal consistency | Select target-language training views |
| Provenance | Original versus enhanced/separated audio, every model/threshold version | Keep raw mixtures distinct from synthetic cleaned views |

Three main products follow:

* **Clean single-speaker speech spans:** one active speaker, little detected
  overlap/interference, acceptable signal quality and reliable language.
  This is an interval property, not a claim that its whole recording has one
  speaker. Boundary padding should preserve phonetic context.
* **Clean multi-speaker alternating speech spans:** retain longer sequences
  with multiple speakers across time, mostly one active speaker at a time.
  Preserve turns, gaps and ordering; concatenating unrelated isolated turns
  is not the same training object. Overlap within a short boundary can be
  retained and marked or excluded by the view's stated policy.
* **Mixed-condition speech spans:** speech with music, commentary over event
  audio, ambient/incident noise, reverberation, overlap, or combinations.
  Keep the conditions and severity estimates so training can control its mix.

### Models that support those decisions without an ASR cascade

[pyannote Community-1](https://huggingface.co/pyannote/speaker-diarization-community-1)
is a current local diarization candidate. Use its **regular** diarization and
overlap evidence for corpus-condition labeling. Its additional **exclusive**
diarization supplies a one-speaker-at-a-time reconciliation view; that view
cannot certify absence of real overlap. Benchmark results on known datasets
are **benchmark-reported**, not validation for unseen tail-language web audio.
Automatic channel averaging also warrants attention when channels contain
different speech/background mixtures.

[PANNs](https://github.com/qiuqiangkong/audioset_tagging_cnn) supplies audio
tagging, embeddings and framewise sound-event detection for particular
checkpoints. The [AudioSet ontology](https://research.google.com/audioset/ontology/)
includes speech, music, narration, environmental events and acoustic-condition
categories. An event model is therefore a useful companion to speech SSL
features for explicit condition labels. Clip-level speech and music scores
only show co-presence somewhere; time-resolved coincidence is needed to infer
speech **over** music rather than a music interlude between speech turns.

[DNSMOS's implementation](https://github.com/microsoft/DNS-Challenge/blob/master/DNSMOS/dnsmos_local.py)
provides nonintrusive speech/background/overall quality estimates. Use them as
additional measurements, not a universal intelligibility oracle or a tail-
language pass/fail threshold. Rejection can favor familiar languages, voices
and recording styles; audit retained/rejected proportions by language and
condition. Estimated SNR is model-dependent in an unseparated real mixture.

Audio alone supports labels such as “speech concurrent with crowd and impact
sounds.” It does not always establish the visual relation “commentary over
event footage.” Source/video metadata can supply that provenance without
ASR; separate observed acoustic coincidence from inferred program type.

Enhancement and source separation create **derived** clean-looking audio.
They can distort phonetic information or remove speech. Keep originals and
mark these views; don't relabel them as naturally isolated recordings. Natural
mixtures and controlled synthetic mixtures are complementary, not equivalent.

### Validation and sampling

Audit small stratified samples for LID, turn/overlap boundaries and background
coincidence; labels for this audit need not include transcripts. Measure clean-
span precision and retained speech-hour yield together. Report speaker leakage,
language confusion and condition-specific false rejections. An aggressive
“clean” threshold can erase most useful material for exactly the tail languages
being targeted. Use a condition-balanced pool plus a high-precision clean view,
with quotas/caps per source and speaker to avoid endless repeated broadcasts.

The proposed selector combines explicit condition attributes, source priors,
and audio-native representations. Pooled multilingual SSL features address
speech variation; PANNs-like scene features address music/events/background.
Keep their geometry separate or learn a projection against the desired
condition labels. ASR-derived text segment/document embeddings are unnecessary
for these tasks. Semantic SONAR remains optional for subject-matter coverage,
not the central tail-ASR collection mechanism.

A useful first representation is deliberately factorized: pooled multilingual
speech features over VAD-selected frames; a whole-window scene embedding;
time-weighted music/event scores; speech and overlap fractions; turn-count and
turn-duration statistics; and quality/channel measurements. Keep these blocks
independently queryable before fitting an audio-derived projection. Masking to
speech alone can erase the environmental condition; whole-window pooling alone
can bury quiet speech under loud music. Compare both against explicit condition
labels and target-language training utility. This is a proposed baseline,
not a reported model result.

## Compression: intelligibility is not representation preservation

[Xiph's recommended settings](https://wiki.xiph.org/Opus_Recommended_Settings)
put mono audiobooks/podcasts at 24 kb/s and conversational voice around
10–24 kb/s; they recommend FLAC for lossless archiving. Those are codec/listening
recommendations. They do not establish an SSL training or domain-embedding
threshold.

My proposed default is **preserve already compressed originals**. If reducing
storage deliberately, evaluate **24 and 32 kb/s mono Opus** for predominantly
speech recordings, with **48–64 kb/s** as conservative candidates for difficult
mixed audio. Preserve separate channels when channel separation or spatial
information matters. Keep a higher-fidelity validation subset before choosing
one rate. This bitrate ladder is an unmeasured recommendation.

Decode/resample into the encoder's required format on read: a 16 kHz speech
model does not require that every archive lose its higher-frequency content.
Model-specific views should record resampling, downmixing and decoder settings.
Converting a lossy source into FLAC enlarges it without recovering its original
waveform. Neural codec tokens are useful derived representations, but adopting
them as the only archive adds decoder/model dependence and possible generative
distortion to the corpus.

| Representation | Decimal MB/hour | Decimal TB / 100k hours |
|---|---:|---:|
| Opus 16 kb/s | 7.2 | 0.72 |
| Opus 24 kb/s | 10.8 | 1.08 |
| Opus 32 kb/s | 14.4 | 1.44 |
| Opus 48 kb/s | 21.6 | 2.16 |
| Opus 64 kb/s | 28.8 | 2.88 |
| PCM, mono 16 kHz × 16 bit | 115.2 | 11.52 |
| PCM, mono 48 kHz × 16 bit | 345.6 | 34.56 |

These are payload arithmetic, `MB/hour = kb/s × 0.45`; no replicas, container
overhead or silence removal. At 32 kb/s, one million hours is 14.4 TB and
100 continuously recorded streams produce 34.56 GB/day.

**The deciding check:** encode matched source windows at each rate, then measure
LID changes, embedding-neighbor agreement and downstream selection quality.
Stratify noise, accent, music, overlap and source codec. Compare within-source
codec perturbations against actual between-domain differences: an embedding
that mostly retrieves compression artifacts is not the intended domain index.
ASR word error alone would not validate the acoustic-domain objective.

## Database and training storage

There is no single “speech DB format.” Separate immutable bytes, queryable
metadata, training layout, and similarity index. The following is a proposed
architecture, not a benchmark result.

| Layer | Suggested format | Why / trade-off |
|---|---|---|
| Source archive | Immutable objects/files, original codec or evaluated Opus | Cheap bytes, independent of changing segmenters and encoders. Checksum and source provenance are part of the record. |
| Operational catalog | PostgreSQL; SQLite for a small single-host installation | Transactions, concurrent ingest and source/rights/time filtering. Large audio `bytea` is possible, but is not my default multi-TB media design. |
| Batch catalog | Versioned [Parquet](https://parquet.apache.org/docs/file-format/) with ZSTD; [DuckDB](https://duckdb.org/docs/stable/data/parquet/overview) for inspection | Column projection and filtering for training snapshots; preserve schema and recipe versions. |
| Sequential training distribution | [WebDataset](https://github.com/webdataset/webdataset) uncompressed tar shards | Stream samples sequentially. Start around 512 MB–1 GiB per shard and tune; this is a packaging heuristic, not a query database. Avoid gzip over already compressed audio when seeking matters. |
| Embedding values | Contiguous float16/float32 arrays or Parquet vectors, explicitly versioned | Keep authoritative vectors separate from a rebuildable ANN index. Quantization requires recall validation. |
| Similarity index | [pgvector](https://github.com/pgvector/pgvector) for an operational index; FAISS or a dedicated distributed index when measured scale requires it | HNSW/IVF/PQ choices trade recall, RAM, filtering and rebuild cost. No universal corpus-size crossover was measured here. |

Store recordings once and refer to segments by offsets unless independent
clip files materially improve training access. Random clip reads need a codec
seek/pre-roll strategy or a derived shard layout: a byte range alone is not
necessarily a decodable Opus segment. Offset coordinates must name their
decoded sample rate and conversion recipe.

Minimal entity relationships:

```text
source(source_id, canonical_url, metadata_snapshot, rights, language_prior)
recording(recording_id, source_id, object_uri, content_hash,
          codec, sample_rate, channels, capture_utc, clock_mapping, gaps)
segment(segment_id, recording_id, start_sample, end_sample, view_recipe,
        speech_fraction, language_posterior, quality, segmentation_version)
condition_track(recording_id, start_sample, end_sample, attribute,
                score, model_version, threshold_recipe)
speaker_turn(recording_id, start_sample, end_sample, local_speaker_id,
             overlap_score, diarization_version)
span_view(segment_id, view_name, selection_recipe, parent_recording_id)
embedding(segment_id, kind, checkpoint_hash, layer, pooling, normalization,
          dimension, dtype, vector_location, encoder_recipe)
split_group(segment_id, source_group, event_group, speaker_group, dedup_group)
```

Use deterministic identities from the recording and segment recipe/interval;
do not identify clips only by rounded wall-clock timestamps. Keep original
language tags and normalized labels separately. Changes to VAD/LID/encoder
should create new derived versions, not silently rewrite provenance.

The index itself becomes a material storage item: 100k hours segmented into
10-second windows yields 36 million vectors. At 512 dimensions float16 that is
36.864 GB; 1024 dimensions doubles it. One million hours yields 368.64 GB at
512 dimensions, before ANN overhead. Frame features are much larger: 768
dimensions × float16 × 50 frames/s is 276.48 MB/hour. Persist pooled vectors by
default and regenerate frame features unless a demonstrated workload needs
them.

## Audio-native domain embeddings

### Acoustic conditions: audio-only SSL features

[WavLM Base Plus](https://huggingface.co/microsoft/wavlm-base-plus) is a
16 kHz pretrained speech encoder, with masked prediction and denoising over
a mixture of speech corpora. Use hidden states, not a transcription head.
Its published pretraining mixture is English-oriented; don't assume a
multilingual domain representation from its speech scale alone.

An initial acoustic index can pool mean and standard deviation over speech
frames, compare a few fixed layers, and optionally fit a low-dimensional PCA
projection on a representative training sample. This projection is learned
from audio features, not segment/document text. Pooling, layer selection and
projection dimension are experiment choices; the card does not validate them
for domain retrieval. [XEUS](https://huggingface.co/espnet/xeus) is a candidate
when broad multilingual pretraining is important. Confirm the exact base SSL
checkpoint rather than substituting an ASR-fine-tuned derivative.

Speaker embeddings are a confusable alternative: speaker similarity can be
excellent while ranking room or subject matter badly. Likewise, robustness
augmentation changes the desired invariance. If room is the target domain,
training invariance to reverb can remove the signal you wanted to index.
Weak source/program labels can train an audio projection without transcripts,
but positive pairs across speakers and held-out broadcasters are necessary to
test whether it learned domain rather than station codec or voice identity.

**Evidence grade:** the proposed domain index is untested synthesis. General
speech-encoder evaluations do not constitute an effectiveness claim for it.

### Subject matter: direct speech-to-semantic vectors

[SONAR](https://github.com/facebookresearch/SONAR) supplies direct speech
encoders into a multilingual sentence space, with released speech support
for 37 languages and a much broader text side. It meets “no ASR in the execution
path,” but not “no text-derived training geometry.” The semantic target comes
from paired/transcript supervision. Use it only if that distinction is
acceptable; don't disguise it as acoustic-domain SSL.

[Omnilingual SONAR](https://arxiv.org/html/2603.16606v1) extends this direction
with one speech encoder trained for 177 languages and attention pooling over
speech features. It is again trained toward transcript-derived text embeddings.
Its sentence-level results do not settle long live-stream topic retrieval.
See [the frontier entry](frontier.md#omnilingual-sonar) before relying on its
coverage or superiority claims.

CLAP-like caption-aligned audio embeddings are another direct path, primarily
suited to sounds/scenes and language-described audio events. “Semantic audio”
does not establish sensitivity to the lexical distinction between a medical
discussion and financial discussion in the same room. Keep such vectors as
an optional scene/event channel, not an assumed substitute for speech meaning.

### Preserve multiple resolutions and nuisance controls

Store acoustic and semantic vectors with distinct `kind` values. Use language,
time, source rights and freshness as explicit filters; don't ask a vector to
enforce them. For current streams, short windows and longer rolling aggregates
answer different questions. Candidate windows of 10–30 seconds and aggregate
contexts of 1–5 minutes are starting hypotheses, not validated optima.

A recording/program representation can aggregate window means or prototypes
while retaining dispersion. One mean hides topic changes, callers, music and
recording transitions. Weight speech-bearing windows and retain individual
neighbors for audit. Never mix vectors from different checkpoints or pooling
recipes in the same metric space without an explicit alignment.

## Contested results, negative findings, and baseline sensitivity

The central disputed inference is that avoiding ASR automatically improves
semantic retrieval. The 2026 [MSEB LLM comparison](https://arxiv.org/html/2605.04556v1)
does not establish that: audio-native LLMs did not show a clear spoken-retrieval
advantage over transcript-cascade alternatives in that setup. Its retrieval
candidate generation and reranking design constrain the conclusion. This is
**single-source** evidence bounding a claim, not a finding that direct speech
embeddings universally fail.

[MSEB](https://arxiv.org/html/2602.07143v1) offers multiple speech/audio
embedding tasks and conditions. Reported results are **benchmark-reported**;
they are not an independent evaluation of the particular domain index proposed
here. Speech-to-text document retrieval is also a different objective from
audio-to-audio acoustic-domain selection.

No independent replication was located establishing a universal Opus bitrate
threshold for these embeddings. Low-bitrate intelligibility and codec benchmark
scores leave that question unresolved. No negative replication of the proposed
pooled-SSL domain baseline was located either: it has not been run here.

Baselines that can invalidate an elaborate embedding solution are source/feed
metadata, language and source-stratified random sampling, simple audio
statistics, and speaker/scene representations. Evaluate target-domain
retrieval on held-out speakers and sources, then evaluate the actual learner's
benefit at equal selected hours and diversity. Audit near duplicates, events,
codec and temporal leakage. An attractive cluster plot is not sufficient.

## Retrieval and limits

Anchors were WavLM and SONAR. OpenAlex forward citations were queried on
2026-10-01 using both publication-date and citation-count sorts. WavLM resolved
to `W3209984917`, with roughly 1,883 citations and 1,871 returned citing works;
the two eight-result slices exposed CLAP and broader representation surveys.
SONAR resolved to `W4386185606`, but its five indexed citers were poorly matched
to this task. These counts are database observations, not paper impact claims.
Backward references and targeted searches for “audio domain embeddings,”
“acoustic data selection,” “speech semantic embeddings,” MSEB and current
multilingual releases supplemented the citation path. Saturation was **not**
reached.

The [manifest](related-work/papers.yaml) records twenty-two extracted/attempted
sources. Sixteen entries have accepted Markdown/provenance and linked assets.
Three 2026 arXiv sources failed SVG extraction; VoxLingua107 and CLAP failed
prose-fidelity checks; MMS ulab v2 failed on an audio-preview element. They
remain source-verified online with
`grounded: false` for local-extract completeness. The shared extractor's
[existing regression gap](../../gaps/related-work-rich-derivation-regressions.md)
records this limitation. Additional linked primary API/model/storage pages
were read online; they do not pretend to be accepted local extracts.

This is a practical map, not an exhaustive corpus inventory. Source counts
are release descriptions; storage costs are arithmetic; codec rates, schema,
embeddings and validation design are
explicit recommendations awaiting matched-data tests.
