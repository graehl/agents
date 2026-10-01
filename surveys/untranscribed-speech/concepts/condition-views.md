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
