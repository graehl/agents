**Source:** *Investigation of Whisper ASR Hallucinations Induced by Non-Speech Audio* — [HTML](https://arxiv.org/html/2501.11378v1) · [arXiv](https://arxiv.org/abs/2501.11378v1)

# baranski2025-whisper-hallucination

2026-11-21, sonnet-5.5. Purpose: voice-activity trimming as input
processing for Whisper-class recognizers. Read: setup, experiments 4-7,
Table VII and conclusions.

**Claims.** Whisper large-v3 hallucinates on non-speech audio (40.3% of
301,317 non-speech inferences produced text; a few phrases such as
"thanks for watching" dominate). For 80 Common Voice clips (about 10 s)
padded with up to 30 s of non-speech before and/or after, at 9 dB SNR,
non-overlapping (NO) and overlapping (OL) noise, Table VII
([extract](../extract/baranski2025-whisper-hallucination/html/2501.11378v1.md):336-402)
gives WER: no processing 104.8 (NO) / 112.0 (OL); beam size 1: 107.2 /
112.3; hallucination-silence threshold 20: 39.8 / 53.7; WebRTC VAD 68.3 /
75.4; Silero VAD 8.0 / 10.8; delooping plus a bag-of-hallucinations filter
17.1 / 21.1; Silero VAD plus the filter 6.5 / 9.4. Denoising with DCCRN
"did not help with hallucinations" (line 334).

**Means for us.** For a large Whisper model on audio with long non-speech
stretches, a good VAD before recognition removes most of a very large
error; a poor VAD (WebRTC) helps much less. The test is built for the
failure (long padding), so the size of the gain says what happens in that
condition, not on ordinary utterances.

**Not shown.** Effect of VAD on tightly endpointed single utterances
(the phone case); any non-Whisper recognizer (CTC and transducer models do
not hallucinate this way); low-resource languages; the paper tests only
English Common Voice clips. Trimming mistakes that clip speech are not
measured beyond the WER.
