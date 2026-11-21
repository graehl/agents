# Other input operations and test-time adaptation

[G] `single-source` per result. Notes in [readings](../related-work/readings/);
full texts linked there. Many cells here have no primary paper on a large
pretrained recognizer; those are marked as gaps.

| Operation | Recognizer, condition | Located result | Grade, source |
|---|---|---|---|
| Test-time adaptation of the recognizer, one utterance | wav2vec 2.0 base fine-tuned on 960 h, CTC, no LM | test-other 8.6 to 7.3; CHiME-3 31.2 to 25.0; Common Voice 36.8 to 31.2; about 0.115 s per audio second for 10 steps on a 3090 | `single-source`, [lin2022](../related-work/readings/lin2022-suta.md) |
| WPE dereverberation, test side | Thai-tuned Whisper large-v3 fine-tuned on mixed-distance data | overall 38.33% to 48.00% (far field 49.54 to 56.12) | `single-source`, ambiguity over whether the model saw processed audio, [tipaksorn2025](../related-work/readings/tipaksorn2025-lotusdis.md) |
| Single-channel MMSE-LSA denoising, same | same | 38.33% to 42.89% | same |
| Room-impulse-response augmentation of training | same model, condenser-only fine-tune | far field 79.54 to 65.39 | same |
| Reverberation cost, no dereverberation | Whisper tiny to large-v3, LibriSpeech test-clean with one real RIR | +15.5 (tiny) to +2.3 (large-v3) WER points; absolute WERs implausibly high | unreliable benchmark, [goswami2026](../related-work/readings/goswami2026-whisper-rir.md) |
| Neural bandwidth extension, 800 to 2000 Hz input | Whisper | improved WER, numbers only in figures; mostly stop words | `single-source`, [liu2024](../related-work/readings/liu2024-low-frequency.md); far below telephone bandwidth |
| Voice-activity trimming | Whisper large-v3, speech padded with up to 30 s non-speech | WER 104.8 to 8.0 with Silero VAD; WebRTC VAD 68.3; denoising did not help | `single-source`, [baranski2025](../related-work/readings/baranski2025-whisper-hallucination.md); built-in failure case |
| Two-channel neural beamforming front end, trained jointly | proprietary far-field recognizer, large data | 10.3% relative (14.8% under 10 dB SNR) over single channel with twice the data | `single-source`, [keskin2021](../related-work/readings/keskin2021-one-or-two-mics.md) |
| Gain change | Whisper tiny.en/base.en and Moonshine, LibriSpeech test-clean | flat until about -40 dB attenuation; figure only | `single-source`, [jeffries2024](../related-work/readings/jeffries2024-moonshine.md) |

## Reading

Test-time adaptation is the one input-side alternative with sizeable gains
in a mismatch, but it was shown on a modest supervised CTC model, not on a
Whisper-class one. Classical single-channel processing in front of a model
fine-tuned for the target (Thai) hurt, and the paper's own remedy was
training-side augmentation. Voice-activity trimming helps one Whisper
failure (hallucination on long non-speech) a great deal. The jointly
trained two-channel front end shows a real gain but on a recognizer built
for it and at a scale a phone project will not have. Gain, clipping,
codec restoration, speaking-rate normalization and mid-bandwidth
(8 kHz) extension have no located controlled evidence on large recognizers
in this survey.
