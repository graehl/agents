**Source:** *Moonshine: Speech Recognition for Live Transcription and Voice Commands* — [HTML](https://arxiv.org/html/2410.15608v2) · [arXiv](https://arxiv.org/abs/2410.15608v2)

# jeffries2024-moonshine

2026-11-21, sonnet-5.5. Purpose: loudness / gain sensitivity and input
length handling of small on-device recognizers. Read: the Whisper
zero-padding discussion and the robustness section.

**Claims.** On LibriSpeech test-clean, scaling the input level shows that
both Whisper (tiny.en, base.en) and Moonshine tolerate a wide range of
linear gain; Moonshine's WER rises above Whisper's only when the signal is
attenuated below about -40 dB, and fan noise at 9 to 17 dB SNR (the range
measured in their tablet application) degrades both similarly
([extract](../extract/jeffries2024-moonshine/html/2410.15608v2.md):192, 202,
206). Results are in a figure; no numbers are tabulated. Whisper's encoder
expects exactly 30 s of zero-padded input; feeding shorter unpadded input
raises WER significantly (Figure 2, lines 43-49), which motivates a
variable-length encoder.

**Means for us.** Gain control is not a lever for these models except
under extreme attenuation (a negative-evidence statement from figures,
not a controlled study). The padding result is a reminder that
"input processing" for Whisper includes length handling, a recognizer
property rather than a signal operation.

**Not shown.** Clipping, loudness normalization, or any comparison with a
gain-controlled input; larger Whisper models.
