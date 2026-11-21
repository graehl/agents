# Enhancement in front of a large recognizer at inference

[G] `single-source` per result, with one pattern replicated across
independent papers (below). Full texts: Islam et al. 2026
([HTML](https://arxiv.org/html/2603.04710v2)), Chondhekar et al. 2025
([PDF](https://arxiv.org/pdf/2512.17562v1)), Wang et al. 2024
([HTML](https://arxiv.org/html/2406.12699v1)), Zhu et al. 2022
([PDF](https://arxiv.org/pdf/2205.13293v1)), Dissen et al. 2024
([HTML](https://arxiv.org/html/2406.18928v1)). Per-paper notes in
[readings](../related-work/readings/).

## The question and the owner's prior

Does a front end that enhances the audio before a large pretrained or
large-supervised recognizer reduce WER? The prior tested: the fitted
encoder layers already do whatever audio-space enhancement could do.

## What the located evidence shows

| Operation | Recognizer, condition | Effect on WER | Source |
|---|---|---|---|
| Separation-style denoiser before recognition | Whisper tiny to large-v3 zero-shot; Bengali YouTube and English MS-SNSD | Worse for every size; large-v3 Bengali 0.658 to 0.774 | [islam2026](../related-work/readings/islam2026-sam-audio-whisper.md) (several raw baselines exceed 100% WER) |
| MetricGAN+ denoiser | Whisper large-v3, Parakeet, Gemini Flash, medical-tuned model; 500 English clips, synthetic noise | Worse in 40 of 40 cells, mean +7.8 points; +2.1 on unmodified clips | [chondhekar2025](../related-work/readings/chondhekar2025-denoising-hurts.md) |
| Four pretrained enhancers (CMGAN, MP-SENet, DEMUCS, SEMamba) | Whisper base and large-v3; LibriSpeech with DNS noise | Worse than noisy: large-v3 15.4% noisy vs 22.8 to 39.9% enhanced | [wang2024](../related-work/readings/wang2024-bridging.md) |
| Observation adding (weighted mix of noisy and enhanced) | same | Recovers the loss; large-v3 14.4 to 15.5% vs 15.4% noisy; best case 6.5% relative | wang2024 |
| Enhancement trained jointly with a wav2vec 2.0-base model, noisy+enhanced fused | 100 to 460 h pre-training, 100 h labelled, synthetic noise | 16.23 to 14.55 average WER over noise sets vs noisy-only variant | [zhu2022](../related-work/readings/zhu2022-joint-se-ssl.md) |
| Front end trained through frozen Whisper's loss | Whisper base/large-v2; simulated packet loss | base 24.0 to 18.1%; large-v2 15.4 to 14.2% | [dissen2024](../related-work/readings/dissen2024-packet-loss.md) |

Baseline sensitivity within these papers: Wang et al. report that higher
PESQ and STOI did not predict lower WER; enhancement hurts most at low
SNR for the large model (-12 dB, large-v3: 44.3% noisy vs 69.1% CMGAN)
and little at 12 dB.

## Verdict on the prior

Supported for standalone enhancement, with evidence stronger than a prior
alone: three independent groups (different enhancers, languages and
recognizers) find that enhancement placed before Whisper-class models
raises WER, and the one result with the mildest recognizer-aware repair
(observation adding) only recovers to about parity or a small gain. The
located positive results are either (a) a front end trained against the
recognizer's loss for a specific defect the recognizer was not trained on
(packet loss), or (b) a joint training setup with a small labelled set and
a smaller pretrained model. Not supported as stated: "no enhancement can
help"; the packet-loss and joint-training results are counterexamples in
conditions where the recognizer cannot absorb the defect.

Mechanism: the evidence is consistent with the authors' account that the
enhancer's artifacts are a mismatch to what the recognizer saw in
training, but none of these papers tests it by probing the encoder.
Gong et al. (see [condition side information](condition-side-information.md))
supply the nearest direct evidence that the encoder carries noise
information itself.

## Caveats

The two papers with the cleanest "enhancement hurts" statements add
synthetic noise to clean clips and apply off-the-shelf enhancers trained
on different noise; none tests low-resource languages in a controlled
way (Islam et al.'s Bengali baselines are too broken to read for most
models). The 2025 and 2026 reports are preprints.
