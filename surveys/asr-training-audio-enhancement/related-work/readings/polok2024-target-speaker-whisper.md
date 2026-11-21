**Source:** *Target Speaker ASR with Whisper* — [HTML](https://arxiv.org/html/2409.09543v2) · [arXiv](https://arxiv.org/abs/2409.09543v2)

# polok2024-target-speaker-whisper

2026-11-21, sonnet-5.5. Purpose: source separation / target-speaker
extraction versus conditioning the recognizer, on overlapped speech
(meeting boundary case). Read: abstract, method summary, Table I.

**Claims.** Conditioning Whisper's encoder with frame-level diarization
probabilities (a per-class bias before each encoder layer, fine-tuned)
gives target-speaker ASR. Table I
([extract](../extract/polok2024-target-speaker-whisper/html/2409.09543v2.md):99-107):
with ground-truth segmentation the proposed system reaches 16.5 (AMI-sdm
ORC WER), 19.1 (NOTSOFAR-1 eval-small tcORC WER), 10.9 (Libri2Mix); a
"input masking" variant that zeroes audio outside the target speaker's
frames, then recognizes, gives 79.1, 76.6, 56.7 (the extract's table
does not make clear which of the two sections it belongs to, so compare
with 18.0/22.6/14.9 to 16.5/19.1/10.9). The abstract's "12.9%
absolute better than a separation-plus-diarization cascade" matches the
gap between 35.5 (Vinnikov et al., NOTSOFAR baseline) and the proposed
22.6 without ground-truth segmentation (line 101).

**Means for us.** Overlapped speech is handled better by telling the
recognizer who is speaking (side information into the encoder, trained)
than by cutting the audio first. Relevant to the side-information question
as a worked case; not relevant to single-speaker phone speech.

**Not shown.** Anything about single-speaker audio; comparison against a
strong modern separator front end trained jointly (the cascade numbers are
from other papers' systems, not rerun).
