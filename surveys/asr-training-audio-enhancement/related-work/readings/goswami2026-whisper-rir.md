**Source:** *Whisper-RIR-Mega: A Paired Clean-Reverberant Speech Benchmark for ASR Robustness to Room Acoustics* — [HTML](https://arxiv.org/html/2603.02252v3) · [arXiv](https://arxiv.org/abs/2603.02252v3)

# goswami2026-whisper-rir

2026-11-21, sonnet-5.5. Purpose: how much reverberation costs Whisper (the
ceiling of what dereverberation could recover). Read: whole paper (short).

**Claims.** Whisper tiny to large-v3 on 1,600 LibriSpeech test-clean
utterances convolved with one measured room impulse response each:
reverberation adds 15.50 (tiny), 11.44, 7.44, 5.94, 2.31 (large-v3)
WER points ([extract](../extract/goswami2026-whisper-rir/html/2603.02252v3.md):57-63).
No dereverberation front end is tested.

**Reliability caveat (ours).** The reported clean WERs (29.0% for
large-v3; 54.9% for tiny) are far above published LibriSpeech test-clean
figures for these models, and CER is oddly non-monotone (large-v3 CER 3.07
exceeds medium 1.90). The scoring or decoding setup (CPU, beam 5,
normalization) is probably faulty; the monotone size trend is plausible
but the absolute numbers should not be quoted as Whisper accuracy.
Single-author, no prior review known.

**Means for us.** Only supports "bigger Whisper tolerates synthetic
reverberation better". It does not bear on whether WPE helps.
