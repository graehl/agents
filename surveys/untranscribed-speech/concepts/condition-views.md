# Web audio and speech-span views

Grounded understanding from [MMS LID's card](https://huggingface.co/facebook/mms-lid-4017),
[pyannote Community-1's card](https://huggingface.co/pyannote/speaker-diarization-community-1),
[PANNs documentation](https://github.com/qiuqiangkong/audioset_tagging_cnn),
and [DNSMOS inference source](https://github.com/microsoft/DNS-Challenge/blob/master/DNSMOS/dnsmos_local.py).
Accepted local extracts are [MMS LID](../related-work/extract/mms-lid-card/facebook/mms-lid-4017.md),
[pyannote](../related-work/extract/pyannote-community-card/pyannote/speaker-diarization-community-1.md),
[PANNs](../related-work/extract/panns-release/qiuqiangkong/audioset_tagging_cnn.md),
and [DNSMOS](../related-work/extract/dnsmos-implementation/microsoft/DNS-Challenge/blob/master/DNSMOS/dnsmos_local.py.md).

The corpus goal and the clean-span goal differ. Preserve a source pool whose
sampling population is stated, then derive independently versioned condition
tracks and selection views. Clean single-speaker speech, alternating-speaker
conversation and natural speech/music/event mixtures are all useful populations;
one universal quality score cannot preserve these distinctions.

Language classification, active-speaker/overlap segmentation, sound-event
tagging and estimated quality can run directly on audio. Their outputs are
measurements with model-dependent uncertainty. A clean single-speaker interval
can belong to a many-speaker recording. Likewise, a diarizer's forced exclusive
output does not prove the physical recording has no overlapping voices.

Sound co-presence and sound coincidence are different: a music intro and a
spoken segment should not automatically label the speech as music-covered.
“Commentary over event footage” also includes a visual/provenance relation that
an audio event tag alone cannot prove. Retain time-resolved tracks and source
metadata rather than collapsing everything into one clip tag.

The rare-language base-rate problem connects selection quality to source
narrowing and calibrated rejection. Class coverage alone cannot certify
correct tail-language labels. Validate accepted/rejected speech by language,
speaker and condition; do not let clean-audio selection eliminate the tail.
Keep separated/enhanced mixtures as derived views alongside their originals.

These are architectural recommendations, not a reproduced classifier or
selection result. The [map](../survey.md#condition-detection-and-span-views)
provides the condition axes, view definitions, and proposed deciding checks.

## Data quality observations for deferred intake

Focused grounded extension, searched 2026-10-02. Anchors: DNSMOS P.835,
NISQA and Emilia-Pipe. DNSMOS inference source and Emilia full text have local
extracts; NISQA and the DNSMOS paper were checked at abstract level. OpenAlex
resolved DNSMOS to W4225302959 (243 indexed citations) and returned ten citers
under each of recency and citation-count sorting. Emilia and Torchaudio-SQUIM
were relevant descendants; SQUIM remains a reading lead. This bounded pass did
not reach field saturation or validate any scorer on Arabic.

[DNSMOS P.835](https://arxiv.org/abs/2110.01763) predicts speech, background
and overall perceptual quality from human ratings. Retain all three outputs;
an overall mean hides whether noise or speech distortion drives it.
[NISQA](https://arxiv.org/abs/2104.09494) instead provides overall quality plus
noisiness, coloration, discontinuity and loudness, targeting communication
network distortions. These are candidates for acoustic usability, not evidence
of transcript correctness or learning utility. Published effectiveness remains
single-source here; neither was reproduced in this extension.

[Emilia-Pipe](https://arxiv.org/html/2501.15907#S3.SS0.SSS0.P6)
combines language-ID confidence, DNSMOS and within-recording text-duration
outliers. Its six languages exclude Arabic, and the task is speech generation.
The [local extract](../related-work/extract/he2025emilia/html/2501.15907.md),
section “Filtering”, alternates character and phone duration terminology;
check the implementation before copying that rule. Its reported DNSMOS increase
after DNSMOS-based filtering is not independent evidence of better ASR training.
Do not adopt its 3.0 threshold as an Arabic admission criterion.

For ASR intake, preserve three groups of observations:

| Group | Initial signals | Interpretation limit |
|---|---|---|
| Acoustic usability | decode success, finite samples, duration, rate, clipping, RMS, DC; later VAD/overlap and DNSMOS components | Near-zero samples are not a VAD; challenging noise may be useful training data |
| Reference reliability | missing/empty reference, normalized characters per voiced second, alignment coverage, independent recognizer disagreement, repetition | Agreement can share errors; disagreement may reflect accent difficulty or transcription conventions |
| Task fit | language posterior/entropy, source genre, speaker/accent-space coverage, exact/approximate duplication | Confidence is not calibrated correctness; diversity is not quality |

This separation is a design recommendation. Start with cheap waveform
observations, then calibrate learned signals against a small stratified human
audit. Include high/low-score examples from each source and diversity cluster,
plus missing-score cases; estimate whether suspect references actually need
correction. For dev, retain hard but correctly labelled speech and repair or
exclude demonstrably unusable references with recorded reasons.

Store model/revision, audio hash/span, time, raw values and missingness separately
from any decision. Track per-source and rolling-window quantiles, rejected or
deferred fractions, and human-confirmed reference-error rates. Compare the
representation distribution before and after a proposed filter. Low ASR
confidence as a universal rejection rule could remove exactly the tail speech
the program targets; the disconfirming search found accent-dependent ASR error
literature, but no validated universal Arabic quality threshold.

Priority may delay similar high-quality segments without deleting them. Reserve
some oldest-first service, keep the original source order, and compare eventual
consumption against intake. Learned quality scorers, Arabic calibration and
quality-versus-downstream-WER contrasts remain unrun.
