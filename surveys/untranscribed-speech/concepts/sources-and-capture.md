# Unlabeled archives and live capture

Grounded understanding from the release and API documentation linked below;
availability descriptions were checked, but no stream was recorded.

The important distinction is between a public dataset that contains unlabeled
speech, a labeled dataset usable after ignoring labels, and a public endpoint
that can supply future speech. These differ in population bias, update behavior,
and provenance. Combining them requires recording their source identities,
not just producing an anonymous directory of clips.

[VoxPopuli full documentation](https://github.com/facebookresearch/voxpopuli)
and [local extract](../related-work/extract/voxpopuli-release/facebookresearch/voxpopuli.md)
provide a large multilingual unlabeled broadcast base with a narrow
parliamentary domain. Its Ogg Vorbis release should not be described as Opus.
[Libri-Light's download documentation](https://github.com/facebookresearch/libri-light/blob/main/data_preparation/README.md)
and [local extract](../related-work/extract/libri-light-downloads/facebookresearch/libri-light/blob/main/data_preparation/README.md.md)
give English read speech with book/speaker metadata and separate duplicate
material. VAD-concatenated samples are a different temporal view from the raw
recording.

[YODAS2's full card](https://huggingface.co/datasets/espnet/yodas2) and
[local extract](../related-work/extract/yodas2-card/datasets/espnet/yodas2.md)
offer video-level unsegmented web audio with optional caption information.
Dropping text removes a runtime dependency, not the collection's caption-based
selection history. [MMS ulab v2's full card](https://huggingface.co/datasets/espnet/mms_ulab_v2)
adds much wider language breadth but religious-source bias. Neither makes
language labels infallible.

[Radio Browser's full API reference](https://docs.radio-browser.info/) and
[local extract](../related-work/extract/radio-browser-api/index.md)
support live endpoint discovery. A resolved URL is useful acquisition metadata;
it is not a speech-purity label, a verified current connection, or a reuse
license. [FFmpeg's protocol reference](https://ffmpeg.org/ffmpeg-protocols.html)
and [local extract](../related-work/extract/ffmpeg-protocols/ffmpeg-protocols.md)
cover transport retries. Sequence/clock discontinuities still need explicit
collector records, especially across HLS reconnects.

The decision implication is to combine static releases for controlled starting
coverage with separately tracked live acquisition for recency. Speech fraction,
language posterior and source/event grouping make both populations usable
without transcription. The [map](../survey.md#current-public-speech-discovery-and-live-edge-retrieval)
contains the operational boundaries and alternatives.

[YODAS v3's current full card](https://huggingface.co/datasets/espnet/yodas3)
and [local extract](../related-work/extract/yodas3-card/datasets/espnet/yodas3.md)
supersede the v2 starting recommendation for a new broad web-audio pool.
Caption-directory language, uploader locale and waveform LID must remain
distinct metadata. In particular, `unk` can contain useful tail-language audio;
absence of captions is not absence of identifiable speech. The existing
audio-shard/Parquet pairing is also a concrete instance of separating recording
bytes from a queryable catalog.
