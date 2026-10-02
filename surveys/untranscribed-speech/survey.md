# Untranscribed speech: sources, live capture, storage, and domain representations

Grounded field survey, coverage cutoff 2026-10-01, with a focused speaker/accent
diversity extension searched through 2026-10-02. Scope: multilingual public
speech at roughly 10⁴–10⁶ hours, collected without transcription, with
embeddings computed directly from audio. The goal is trainable audio for
tail-language ASR, meaning languages with few high-quality transcribed hours,
with language identification reliable enough for that use. Legal analysis is
out of scope.

Primary dataset and model cards, protocol documentation, and selected
speech-representation papers were read; twenty-one of thirty-one sources have
accepted local full-text extracts ([retrieval and
limits](#retrieval-and-limits)). No audio was collected and no codec or
embedding experiment was run. Source sizes are publisher-reported, storage
figures are arithmetic, and the recommended codec rates, storage
architecture, condition selector, and embedding index are untested synthesis.

## Decisions this survey supports

For tail-language ASR, start with MMS ulab v2 as a broad language seed, add
regional and community radio and local-language web channels for natural
speech, and mine YODAS v3 for existing varied web audio. VoxPopuli and
Libri-Light serve as control populations with much narrower language reach.
These sources sample different populations, so their hours are not
interchangeable. Discover live endpoints through a station directory rather
than scraping player pages.

Maintain two products: a representative pool of source recordings, and
versioned span views over it for clean single-speaker, clean
alternating-speaker, and mixed-condition speech. Music, noise, and event
sounds are conditions to detect and stratify; a recording containing them
still has usable speech
([condition detection](#condition-detection-and-span-views)).

Keep the source's compressed audio when possible. If re-encoding a speech
archive, mono Opus at 24–32 kb/s is a reasonable first candidate, not an
established training-quality threshold. Store recording bytes immutably,
segments as offsets, operational metadata in a relational catalog, batch
metadata in Parquet, and embeddings in versioned arrays and indexes.

Represent acoustic domain separately from subject matter. A pooled
self-supervised speech encoder is the baseline for acoustic domain; the
Omnilingual ASR wav2vec 2.0 encoders, pretrained on over 1,200 languages, are
the widest-coverage released candidates.
SONAR-style speech embeddings capture subject matter without running ASR,
but their geometry is trained toward text. No source located here shows a
single vector serving both purposes on long, noisy live speech.

Concept notes: [sources and capture](concepts/sources-and-capture.md),
[condition views](concepts/condition-views.md),
[compression and storage](concepts/storage-and-compression.md),
[audio domain representations](concepts/audio-domain-representations.md),
[measuring speaker/accent diversity](concepts/speaker-accent-diversity.md).
Recent claims and open tests are in [frontier.md](frontier.md).

## What “no-transcript” and “domain” mean here

“No transcript” can mean three constraints, each admitting different
solutions:

1. The data source need not supply transcripts. Some releases have
   transcripts that can be ignored; others are unlabeled audio.
2. No ASR runs when computing an embedding. Waveform → encoder → vector
   qualifies even if the encoder was pretrained on speech/text pairs.
3. The embedding's training geometry is not derived from transcripts. An
   audio-only self-supervised checkpoint qualifies; an encoder distilled
   toward a text teacher, or fine-tuned for ASR, does not.

Acoustic domain covers room, microphone, channel, noise, speaking style, and
similar recording conditions. Semantic domain covers subject matter and
intent. Language, accent, and speaker identity can be targets or confounders
depending on the task, so a retrieval system's quality can be judged only
against a stated set of desired invariances.

## Downloadable archives and corpora

Hour counts are release descriptions, not audited totals of usable speech.
A language tag is a prior; any given window may hold another language.

| Source | Audio and language coverage | Transcript dependence and bias | Retrieval and practical limits |
|---|---|---|---|
| [YODAS v3](https://huggingface.co/datasets/espnet/yodas3) | New release; over 1.1M h of 48 kHz web audio, over 70% with two distinct channels; 100+ languages. | Captions on about 75% of the data. Caption language and uploader-locale language are separate file-level labels; recordings without captions are grouped under `unk`. | Opus/WebM in WebDataset tar shards with per-shard Parquet metadata; inspect metadata before acquiring by language. A better representative-web starting point than v2; not a validated clean-span corpus. |
| [VoxPopuli](https://github.com/facebookresearch/voxpopuli) | Headline 400k h in 23 languages; the detailed unlabeled table sums to about 384k h. European Parliament recordings, 16 kHz mono Ogg Vorbis. | Unlabeled release. Formal political speech and simultaneous interpretation, with the same events across languages; little conversational speech. | Download scripts; the 400k subset is about 6.4 TB. Repository archived October 2023. Few tail languages. |
| [Libri-Light](https://github.com/facebookresearch/libri-light/blob/main/data_preparation/README.md) | Nominally 60k h of English audiobooks; the main subsets sum to 57,704 h, about 3.4 TB. FLAC plus book and speaker JSON. | Unlabeled read speech. The separate duplicate subset should not count as new coverage. Optional VAD concatenation alters the timeline. | Direct tar archives. English control population. The FLAC files descend from LibriVox MP3s, so they carry the original lossy artifacts. |
| [YODAS2](https://huggingface.co/datasets/espnet/yodas2) | Unsegmented 24 kHz audio, one file per video. The original [YODAS release](https://huggingface.co/datasets/espnet/yodas) describes 369,510 h in 149 languages. | Captions can be ignored, but selection depended on YouTube and caption availability. The internal `video_id` is not the YouTube identifier. | Hugging Face download; streaming reads the archive, not live speech. Check its loading-script requirements before choosing an ingestion library. |
| [MMS ulab v2](https://huggingface.co/datasets/espnet/mms_ulab_v2) | 8,900 h raw, unsegmented, 16 kHz mono; reported 4,023 languages in 189 families. | Unlabeled. Global Recordings Network religious material, so subject matter is narrow. Preview metadata includes unknown and malformed language values. | ESPnet's reproduction and extension of the MMS unlabeled data. The roughly 6,700 h used for XEUS is the post-segmentation figure, not the raw duration. |
| [VoxLingua107](https://cs.taltech.ee/staff/tanel.alumae/data/voxlingua107/) | Reported 6,628 h in 107 languages, from YouTube. | Clips selected for language ID with heuristic labels. Useful LID material; not balanced across subject matter. | Official downloads. Verified online only; local extraction failed. |
| [Multilingual LibriSpeech](https://www.openslr.org/94/) | Read audiobooks in eight languages. The English release is offered as FLAC (2.4 TB) or Opus (651 GB). | Transcribed; ignoring the transcripts satisfies constraint 1, but the audio was selected for transcription. | OpenSLR resource 94. The two codec releases give a storage comparison, not evidence of equal training value. |
| [Emilia](https://huggingface.co/datasets/amphion/Emilia-Dataset) | 101.7k h original plus 113.9k h Emilia-YODAS, in six major languages. | Utterances processed and filtered for TTS, with ASR-generated text, so ASR and quality filters already shaped the population. | Downloadable. No tail-language coverage; useful as a clean-span comparator. |
| [CMU Wilderness](https://github.com/festvox/datasets-CMU_Wilderness) | 700+ languages, about 20 h each, of sentence-aligned New Testament readings from Bible.is. | Aligned text exists but can be ignored. Same narrow religious read-speech population as MMS ulab, with per-utterance alignment scores. | Audio is not redistributed: scripts download it from Bible.is and rebuild alignments from packed indices, about 30 minutes per language. Availability depends on Bible.is. |
| [Omnilingual ASR Corpus](https://huggingface.co/datasets/facebook/omnilingual-asr-corpus) | 3,350 h of prompted spontaneous speech in 348 under-served languages ([paper](https://arxiv.org/html/2511.09690), Table 3); FLAC. | Transcribed, with laughter, hesitation, and noise tags. Commissioned recordings answering conversational prompts, not web or broadcast audio. | CC-BY-4.0 on Hugging Face. Labels carry ISO 639-3, script, and Glottolog codes, useful for mapping tail-language labels. Verified online only; local extraction failed. |
| [FLEURS](https://huggingface.co/datasets/google/fleurs) | 102 languages, about 10 h of training speech each, reading the same 2,009 FLoRes sentences. | Transcribed read speech. Because content and recording setup are shared across languages, its language-ID split tests language rather than domain. | CC-BY. A language-ID evaluation set for the 102 covered languages, not a source of web conditions. Verified online only; local extraction failed. |

**Collections outside packaged corpora.** The Internet Archive holds radio,
lectures, oral histories, sermons, and other recordings. Its [item metadata
API](https://archive.org/developers/metadata.html) (`GET
/metadata/{identifier}`) returns item metadata and file records per item; it
has no wildcard collection download. Retain the original file choice,
checksums, and item-level rights metadata. The [Library of Congress JSON/YAML
API](https://www.loc.gov/apis/json-and-yaml/requests/) accepts `fo=json` on
supported collections, including oral-history paths, with uneven coverage.
Both are discovery channels, not corpora of known size.

RSS podcast enclosures and new LibriVox books keep growing, and program or
feed metadata supplies cheap subject hints without ASR. Neither is live: a
newly published file may contain old speech. When totaling hours, do not mix
collected pools, filtered releases, transcribed subsets, duplicate encodings,
and model pretraining hours. A model trained on millions of hours does not
make those hours downloadable: Omnilingual ASR's 4.3M-hour pretraining set
includes a large internal collection, and the project's new public audio is
its 3,350-hour commissioned corpus.

**Search YODAS v3 beyond its caption directories.** The card lists 102
caption-language directories plus `unk`, while the uploader-locale field has
146 distinct codes; the paper's 147-language count uses a different
accounting. To find tail-language audio, search the locale metadata and the
`unk` pool as well as the caption directories, then run waveform LID. Audio
ships in tar shards of about 8 GB, each with a Parquet metadata file keyed by
recording ID. The per-file effective bandwidth and channel estimates are
useful condition metadata but do not guarantee intelligibility or correct
per-sentence language. The [September 27 release
announcement](https://huggingface.co/blog/espnet/yodasv3) confirms 48 kHz
Opus and the million-hour scale; see the [frontier
entry](frontier.md#yodas-v3-release-and-language-accounting).

## Current public speech: discovery and live-edge retrieval

### Direct radio is the simplest sustained source

[Radio Browser](https://docs.radio-browser.info/) offers station search, with
records carrying `stationuuid`, `url`, `url_resolved` (after playlist and
redirect resolution), language fields, tags, codec, and last-check
timestamps. Discover mirrors through the documented server list rather than
pinning one. An example query is
`/json/stations/search?language=english&tag=news&hidebroken=true`. Directory
metadata is weak supervision: a “news” station can play music or ads, and a
passing periodic check does not mean the stream is up now.

The recording path is directory → resolved HTTP/ICY or HLS endpoint → demux
→ immutable audio chunks → VAD, LID, and quality metadata. Remux the incoming
codec (`-c:a copy`) rather than re-encoding. Record the station UUID,
original and resolved URLs, a metadata snapshot, connection time, codec, and
discontinuities, since source URLs expire and change.

### HLS and platform adapters

HLS delivers the latest published segment, already delayed by encoder
buffering and segment publication. A collector should track sequence
numbers, discontinuities, and initialization segments, and keep
`EXT-X-PROGRAM-DATE-TIME` when present. Without it, receive time in UTC is an
observation time, not broadcast time. Record gaps across reconnects instead
of joining timestamps as if the stream were continuous.

[FFmpeg's HTTP protocol](https://ffmpeg.org/ffmpeg-protocols.html) provides
`reconnect`, `reconnect_streamed`, `reconnect_at_eof`, and
`reconnect_delay_max`; they apply differently to endless HTTP streams and to
HLS playlist refresh. `rw_timeout` is in microseconds. Retry policy and
timestamp handling belong in the collector's logic, not only in a shell
command line.

For supported site players, [Streamlink](https://streamlink.github.io/cli.html)
resolves a media URL with `--stream-url` and retries discovery with
`--retry-streams`. [yt-dlp](https://github.com/yt-dlp/yt-dlp) downloads
livestreams from the current time by default (`--no-live-from-start`);
`--live-from-start` is experimental and limited to a few platforms. Plugin
coverage, signed URLs, and platform changes make both tools ongoing
maintenance, so use them after direct endpoints. Some public live pages will
not be capturable with either.

### Transcript-free enrichment

Run speech/non-speech detection before counting hours as speech. Store speech
fraction, music and overlap indicators, language posterior and confidence,
and enough source metadata to trace errors. A waveform LID model labels
windows without transcription; keep unknown and mixed outcomes. Treat
station-level language as a prior, especially for interpreted programs and
code switching. Group train/evaluation splits by source, program, event, and
duplicate cluster rather than splitting neighboring windows at random.

No endpoint was recorded for this survey; “live” here describes documented
capability, not measured uptime or latency.

## Tail-language LID and acquisition priorities

[MMS LID 4017](https://huggingface.co/facebook/mms-lid-4017) classifies
waveforms into 4,017 languages using a one-billion-parameter speech encoder.
That coverage makes it a better starting point for the tail than the
[VoxLingua107 ECAPA classifier](https://huggingface.co/speechbrain/lang-id-voxlingua107-ecapa)
with its 107 classes, which remains a useful comparison where the two
overlap. Omnilingual ASR released no standalone LID model: its LLM-ASR
decoder identifies language implicitly and accepts an optional language and
script code, which the authors added because related languages and
multi-script languages were confused without it.

Having a class for a language does not make identification accurate. In the
[ML-SUPERB 2.0 challenge](https://arxiv.org/html/2509.07139), the best
submitted system per metric reached about 89% LID accuracy on the standard
multilingual test set but about 57% on accented and dialectal speech; the
organizers' baselines (frozen SSL encoders with a small head trained on about
one hour per language, and zero-shot Whisper large-v3 and OWSM) ranged from
19% to 55% on the dialectal set (`externally-evaluated` on a hidden test
server). Labels on commissioned data are also
fallible: Omnilingual ASR's cross-vendor check of its commissioned recordings
found misattributed language codes in 20 of 206 languages checked.
[FLEURS](https://huggingface.co/datasets/google/fleurs) offers a controlled
LID test for 102 languages, since every language reads the same sentences;
most tail languages need their own speaker-verified samples.

Map source labels to model classes explicitly for each target language,
since ISO codes, dialect labels, and naming conventions differ. Gather source
priors from regional stations, local-language channels, community
programming, podcasts, and existing language-tagged archives. Measure
progress in retained, deduplicated, correctly identified speech hours rather
than raw bytes or headline language counts. A religious seed such as MMS
ulab or CMU Wilderness supports initial LID checks but leaves conversational
and broadcast speech largely uncovered. Omnilingual ASR measured the cost of
a narrow source with language coverage held fixed: a 1B CTC model trained
only on MMS-lab (high-quality recordings, a handful of speakers per language)
reached 35.7% CER on held-out FLEURS and 43.4% on Common Voice, against 21.0%
and 33.5% for models trained on all their other sources with the evaluated
corpus held out (`single-source`).

Apply LID to speech-bearing spans and their neighbors, keeping top-k
probabilities, margin, cross-window consistency, and the source prior, along
with unknown, mixed, and needs-review states. Two models agreeing is weaker
evidence when their training data overlap. Calibration needs a small sample
of accepted and rejected web spans checked by speakers of the language,
including related languages, contamination from the dominant regional
language, singing, and background speech. Speakers can label language
without producing transcripts.

Low base rates make false positives expensive. If target-language speech is
0.1% of a pool, a detector with 90% recall and a 1% false-positive rate has
about 8.3% precision: `0.001 × .90 / (0.001 × .90 + .999 × .01)`. These rates
are illustrative, not MMS measurements. Narrowing sources and rejecting
low-confidence windows can matter more than another point of closed-set
accuracy. Restricting a classifier to plausible labels without an unknown
option forces contaminants into a tail language.

Usable training speech for ASR need not be studio-clean. Self-supervised
acoustic pretraining tolerates more varied speech; pseudo-labeling and
supervised adaptation are more sensitive to wrong labels and heavy
interference. Keep condition strata so each training regime can select its
own subset. Judging a subset's value eventually requires held-out
target-language ASR results, but collection and condition labeling need
neither ASR nor text embeddings.

## Condition detection and span views

### Preserve the web-audio population before selecting clean spans

Build an immutable pool of source recordings with a documented sampling
frame: languages, regions, source and program families, dates, and
durations. A CC-captioned YouTube release, a radio-only crawl, and a
religious archive are each biased. “Representative web audio” has to name
its target population and sampling weights; size alone does not make a pool
representative. Keep no-speech and music-only intervals where they help model
conditions, but count training speech hours separately.

Derive overlapping, versioned views from the pool. Label independent axes
rather than assigning each recording one exclusive class:

| Axis | Span-level evidence to retain | Decision supported |
|---|---|---|
| Speech presence | VAD posterior, speech duration and fraction, boundary uncertainty | Count usable speech; keep music and noise out of speech totals |
| Speakers | Framewise active-speaker count, local identity and turn boundaries, overlap probability | Separate one-speaker spans, alternating turns, and simultaneous speech |
| Background | Music, event, and noise scores (multi-label), and their coincidence with speech | Distinguish clean speech, speech over a music bed, and speech over crowd, traffic, or incident sound |
| Recording condition | Clipping, loudness, estimated interference, reverb and channel features, dropouts | Filter corruption and stratify natural difficulty |
| Language | Per-span posterior, code-switch and mixed flags, temporal consistency | Select target-language training views |
| Provenance | Original versus enhanced or separated audio; version of every model and threshold | Keep raw mixtures distinct from synthetic cleaned views |

These axes yield three span views:

* Clean single-speaker spans: one active speaker, little detected overlap or
  interference, acceptable signal quality, and a reliable language label.
  This is a property of the interval; the rest of the recording may have
  other speakers. Pad boundaries enough to preserve phonetic context.
* Clean alternating-speaker spans: longer sequences in which several
  speakers take turns, mostly one at a time. Keep turns, gaps, and order;
  concatenated turns from unrelated recordings are a different training
  object. Brief overlap at turn boundaries is either kept and marked or
  excluded, per the view's stated policy.
* Mixed-condition spans: speech with music, commentary over event audio,
  ambient or incident noise, reverberation, overlap, or several of these.
  Keep the condition labels and severity estimates so training can control
  its mix.

### Models that support those decisions without an ASR cascade

[pyannote Community-1](https://huggingface.co/pyannote/speaker-diarization-community-1)
is a current local diarization option. Use its regular diarization and
overlap output for condition labeling. Its additional exclusive diarization
assigns one speaker at a time, so it cannot show that a span lacks overlap.
Its published benchmark scores do not validate it on unseen tail-language
web audio. It averages channels automatically, which matters when channels
carry different speech and background mixtures.

[PANNs](https://github.com/qiuqiangkong/audioset_tagging_cnn) provides audio
tagging, embeddings, and, for some checkpoints, framewise sound-event
detection. The [AudioSet ontology](https://research.google.com/audioset/ontology/)
covers speech, music, narration, environmental events, and acoustic
conditions, so an event model complements speech SSL features with explicit
condition labels. Clip-level speech and music scores show only that both
occur somewhere in the clip; telling speech over music from a music interlude
between turns needs time-resolved scores.

[DNSMOS](https://github.com/microsoft/DNS-Challenge/blob/master/DNSMOS/dnsmos_local.py)
estimates speech, background, and overall quality without a clean reference.
Treat its scores as additional measurements, not as an intelligibility test
or a pass/fail threshold for tail languages: rejection can favor familiar
languages, voices, and recording styles, so audit retained and rejected
proportions by language and condition. Its SNR estimate on a real,
unseparated mixture depends on the model.

Audio alone supports a label such as “speech concurrent with crowd and impact
sounds,” but not always “commentary over event footage.” Source or video
metadata can supply the program type without ASR; record observed acoustic
coincidence separately from inferred program type.

Enhancement and source separation produce derived audio that sounds clean
but can distort phonetic detail or remove speech. Keep the originals, mark
these views as derived, and do not relabel them as naturally isolated
recordings. Natural mixtures and controlled synthetic mixtures complement
each other; neither substitutes for the other.

### Validation and sampling

Audit small stratified samples for LID, turn and overlap boundaries, and
background coincidence; none of these audits needs transcripts. Measure
clean-span precision together with retained speech-hour yield, and report
speaker leakage, language confusion, and false rejections by condition. An
aggressive “clean” threshold can discard most of the material for exactly the
tail languages being targeted. Pair a condition-balanced pool with a
high-precision clean view, and cap hours per source and speaker so repeated
broadcasts do not dominate.

The proposed selector combines explicit condition attributes, source priors,
and audio-native representations. Pooled multilingual SSL features describe
speech variation; PANNs-style scene features describe music, events, and
background. Keep the two geometries separate, or learn a projection against
the desired condition labels. Text embeddings of ASR output are unnecessary
for these tasks; SONAR stays optional, for subject-matter coverage.

A first representation can be factorized into blocks: pooled multilingual
speech features over VAD-selected frames, a whole-window scene embedding,
time-weighted music and event scores, speech and overlap fractions, turn
count and duration statistics, and quality and channel measurements. Keep the
blocks independently queryable before fitting any projection across them.
Pooling only speech frames can erase the environmental condition; pooling the
whole window can bury quiet speech under loud music. Compare both against
explicit condition labels and against target-language training value.

## Compression: intelligibility is not representation preservation

[Xiph's recommended settings](https://wiki.xiph.org/Opus_Recommended_Settings)
give 24 kb/s mono for audiobooks and podcasts and 10–24 kb/s for VoIP, and
recommend FLAC for lossless archiving. These target listeners; they set no
threshold for SSL training or domain embeddings.

The proposed default is to keep already-compressed originals. When reducing
storage deliberately, evaluate mono Opus at 24 and 32 kb/s for mostly-speech
recordings, with 48–64 kb/s as a conservative choice for difficult mixed
audio. Keep separate channels when channel separation or spatial information
matters, and hold back a higher-fidelity validation subset before committing
to one rate.

Decode and resample to each encoder's input format on read; a 16 kHz model
does not require discarding higher frequencies from the archive. Each
model-specific view should record its resampling, downmixing, and decoder
settings. Converting a lossy source to FLAC enlarges it without restoring the
original waveform. Neural codec tokens are useful derived representations,
but storing only tokens makes the archive depend on a decoder model and adds
generative distortion.

| Representation | Decimal MB/hour | Decimal TB / 100k hours |
|---|---:|---:|
| Opus 16 kb/s | 7.2 | 0.72 |
| Opus 24 kb/s | 10.8 | 1.08 |
| Opus 32 kb/s | 14.4 | 1.44 |
| Opus 48 kb/s | 21.6 | 2.16 |
| Opus 64 kb/s | 28.8 | 2.88 |
| PCM, mono 16 kHz × 16 bit | 115.2 | 11.52 |
| PCM, mono 48 kHz × 16 bit | 345.6 | 34.56 |

Figures are payload only (`MB/hour = kb/s × 0.45`), without replicas,
container overhead, or silence removal. At 32 kb/s, one million hours is
14.4 TB, and 100 continuously recorded streams produce 34.56 GB/day.

The test that would settle the rate: encode matched source windows at each
rate, then measure changes in LID, embedding-neighbor agreement, and
downstream selection quality, stratified by noise, accent, music, overlap,
and source codec. Compare codec perturbations within a source against actual
differences between domains; an embedding whose neighbors are mostly
determined by compression artifacts is useless as a domain index. ASR word
error rate alone would not validate the acoustic-domain objective.

## Database and training storage

No single speech database format covers the need. Separate immutable bytes,
queryable metadata, training layout, and similarity index:

| Layer | Suggested format | Reason and trade-off |
|---|---|---|
| Source archive | Immutable objects or files, original codec or evaluated Opus | Cheap, and independent of changing segmenters and encoders. Checksum and source provenance are part of the record. |
| Operational catalog | PostgreSQL; SQLite for a small single-host setup | Transactions, concurrent ingest, filtering by source, rights, and time. Storing audio as `bytea` works but is a poor default at multi-TB scale. |
| Batch catalog | Versioned [Parquet](https://parquet.apache.org/docs/file-format/) with ZSTD; [DuckDB](https://duckdb.org/docs/stable/data/parquet/overview) for inspection | Column projection and filtering for training snapshots; record schema and recipe versions. |
| Sequential training distribution | [WebDataset](https://github.com/webdataset/webdataset) uncompressed tar shards | Sequential sample streaming. Start at 512 MB–1 GiB per shard and tune; this is packaging, not a query layer. Avoid gzip over already-compressed audio when seeking matters. |
| Embedding values | Contiguous float16/float32 arrays or Parquet vector columns, explicitly versioned | Keep authoritative vectors apart from a rebuildable ANN index. Validate recall after quantization. |
| Similarity index | [pgvector](https://github.com/pgvector/pgvector) for an operational index; FAISS or a distributed index when measured scale requires it | HNSW, IVF, and PQ trade recall, RAM, filtering, and rebuild cost. The corpus size at which to switch was not measured. |

Store each recording once and address segments by offset unless separate clip
files materially speed up training. Random clip reads need a codec seek and
pre-roll strategy or a derived shard layout, because an arbitrary byte range
is generally not a decodable Opus segment. Offsets must name their decoded
sample rate and conversion recipe.

Minimal entities:

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

Derive identities deterministically from the recording and the segment's
recipe and interval, never from rounded wall-clock timestamps alone. Store
original language tags and normalized labels side by side. A change to VAD,
LID, or an encoder creates new derived versions rather than rewriting
existing ones.

The embedding index is a significant storage item. 100k hours in 10-second
windows is 36 million vectors, or 36.864 GB at 512 dimensions in float16;
1024 dimensions doubles that. One million hours at 512 dimensions is 368.64
GB before ANN overhead. Frame features are much larger: 768 dimensions ×
float16 × 50 frames/s is 276.48 MB/hour. Persist pooled vectors and
regenerate frame features unless a workload demonstrably needs them stored.

## Audio-native domain embeddings

### Acoustic conditions: audio-only SSL features

[WavLM Base Plus](https://huggingface.co/microsoft/wavlm-base-plus) is a
16 kHz speech encoder pretrained with masked prediction and denoising on a
mixture of speech corpora. Use its hidden states, not a transcription head.
Its pretraining data are predominantly English, so its scale says nothing
about multilingual domain coverage.

A first acoustic index can pool the mean and standard deviation over speech
frames, compare a few fixed layers, and optionally fit a low-dimensional PCA
projection on a representative sample. The projection is learned from audio
features, not text. Pooling, layer, and projection dimension are
experimental choices that the model card does not validate for domain
retrieval. When broad multilingual pretraining matters, the candidates are
[XEUS](https://huggingface.co/espnet/xeus), the strongest baseline encoder
in the ML-SUPERB 2.0 challenge, and the [Omnilingual ASR
wav2vec 2.0 encoders](https://github.com/facebookresearch/omnilingual-asr)
(0.3B, 1B, 3B, and 7B parameters, Apache 2.0), pretrained on 3.84M hours in
1,239 identified languages plus 460k hours without language labels. After
ASR fine-tuning, the Omnilingual encoders gave lower average CER than XLS-R
and MMS encoders of equal size on most benchmarks the authors ran
(`single-source`); neither encoder family has been evaluated for domain
retrieval. Use the base SSL checkpoint, not an ASR-fine-tuned derivative.

Speaker embeddings are easily mistaken for domain embeddings: they can match
speakers well while ranking rooms or subject matter badly. Robustness
augmentation also changes what the model is invariant to; if room is the
target domain, training for reverb invariance removes the signal to be
indexed. Weak source or program labels can train an audio projection without
transcripts, but testing it needs positive pairs across speakers and
held-out broadcasters, to show it learned domain rather than station codec
or voice.

General speech-encoder benchmarks say nothing about this domain index's
effectiveness; it is untested.

### Subject matter: direct speech-to-semantic vectors

[SONAR](https://github.com/facebookresearch/SONAR) provides speech encoders
into a multilingual sentence-embedding space, with released speech encoders
for 37 languages and text support for 200. It satisfies constraint 2 (no ASR
when embedding) but not constraint 3: the speech encoders were trained
toward text embeddings of transcripts. Use it only where that is acceptable,
and do not present it as acoustic-domain SSL.

[Omnilingual SONAR](https://arxiv.org/html/2603.16606v1) extends this with a
single speech encoder trained for 177 languages and attention pooling over
speech features, again trained toward transcript-derived text embeddings.
Its sentence-level results do not settle topic retrieval over long live
streams. See [the frontier entry](frontier.md#omnilingual-sonar) before
relying on its coverage or superiority claims.

CLAP-style audio embeddings, aligned to captions, are another direct path,
suited mainly to sounds, scenes, and audio events that captions describe.
They are not shown to separate a medical discussion from a financial one
recorded in the same room. Keep them as an optional scene and event channel,
not as a stand-in for speech meaning.

### Multiple resolutions and nuisance controls

Store acoustic and semantic vectors under distinct `kind` values. Apply
language, time, source rights, and freshness as explicit filters rather than
expecting the vector to encode them. For current streams, short windows and
longer rolling aggregates answer different questions; windows of 10–30
seconds and aggregates of 1–5 minutes are starting guesses.

A recording or program representation can aggregate window means or
prototypes, but should keep a dispersion measure, since one mean hides topic
changes, callers, music, and recording transitions. Weight speech-bearing
windows and keep the individual windows' neighbors for audit. Never compare
vectors from different checkpoints or pooling recipes in one metric space
without an explicit alignment.

## Measuring speaker and accent coverage without complete metadata

The [focused survey](concepts/speaker-accent-diversity.md) separates voice
redundancy, accent-sensitive similarity and recording conditions. Its closest
data-selection evidence is Kim et al.'s English accent miner: clustering-selected
adaptation data improves Indian-English WER relative to random selection, but
the encoder was trained with other accent labels. Ghorbani and Hansen find
complementary accent information in language-ID and speaker embeddings.
Neither result validates Arabic source coverage.

The proposed screen compares equal-budget source samples in frozen embedding
spaces, reporting within-source concentration and incremental coverage of a
fixed audit pool. Vendi Score is an optional kernel-dependent summary;
nearest-pair listening and codec/channel controls determine what the numbers
mean. Implementation and Arabic validation remain open, without blocking the
interim source-balanced dev mix.

## Contested results, negative findings, and baseline sensitivity

The main disputed inference is that avoiding ASR improves semantic retrieval.
The 2026 [MSEB LLM comparison](https://arxiv.org/html/2605.04556v1) does not
support it: audio-native LLMs showed no clear spoken-retrieval advantage over
transcript-cascade alternatives in that setup, though its candidate
generation and reranking design limit the conclusion. This is a single source
bounding the claim, not evidence that direct speech embeddings fail in
general.

[MSEB](https://arxiv.org/html/2602.07143v1) covers several speech and audio
embedding tasks and conditions. Its results are the benchmark authors' own
and do not evaluate the domain index proposed here; its speech-to-text
document retrieval is also a different objective from audio-to-audio
selection by acoustic domain.

No independent work was located that establishes an Opus bitrate threshold
for these embeddings; intelligibility results at low bitrates and codec
benchmark scores leave the question open. No negative result for the
proposed pooled-SSL domain baseline was located either; it has not been run
here.

Simple baselines can beat an elaborate embedding: source and feed metadata,
random sampling stratified by language and source, simple audio statistics,
and speaker or scene representations. Evaluate target-domain retrieval on
held-out speakers and sources, then measure the downstream learner's gain at
equal selected hours and diversity. Audit near duplicates and leakage through
shared events, codec, and recording time. A well-separated cluster plot is
not evidence of downstream value.

## Retrieval and limits

Citation search started from WavLM and SONAR. OpenAlex forward citations were
queried on 2026-10-01, sorted both by publication date and by citation count.
WavLM resolved to `W3209984917`, with about 1,883 citations and 1,871 citing
works returned; the first eight results under each sort surfaced CLAP and
general representation-learning surveys. SONAR resolved to `W4386185606`,
whose five indexed citing works were poorly matched to this task. These are
database counts, not measures of impact. Backward references and targeted
searches for “audio domain embeddings,” “acoustic data selection,” “speech
semantic embeddings,” MSEB, and recent multilingual releases supplemented the
citation search. The search did not reach saturation.

A follow-up pass the same day added five sources found by targeted search
for tail-language corpora and language-ID evaluation: Omnilingual ASR and its
corpus, CMU Wilderness, FLEURS, and the ML-SUPERB 2.0 challenge.

The [manifest](related-work/papers.yaml) lists thirty-one sources.
Twenty-one have accepted Markdown extracts with provenance and linked assets.
Eight sources from the initial pass are marked `grounded: false` because local
extraction failed: three 2026 arXiv papers on SVG figures, VoxLingua107 and
CLAP on prose-fidelity checks, and the MMS ulab v2, Omnilingual ASR Corpus,
and FLEURS cards on audio-preview elements. The
extractor's [regression gap](../../gaps/related-work-rich-derivation-regressions.md)
tracks these failures. Additional API, model, and storage pages linked above
were read online without local extracts.

The 2026-10-02 [diversity extension](concepts/speaker-accent-diversity.md)
adds two accepted accent-paper extracts, a Vendi Score source whose local
derivation failed fidelity checks, and the x-vector probing paper checked at
abstract level. Its search trail and remaining Arabic validation are recorded
in that concept note.

This is a practical map, not an exhaustive inventory of corpora.
