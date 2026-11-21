# Non-stationary conditions, benchmarks, and narrowband/codec augmentation

[G] `single-source` per result. Full texts: Shah et al. 2024
([PDF](https://arxiv.org/pdf/2403.07937v3)), Tuttosi et al. 2025
([HTML](https://arxiv.org/html/2505.00059v2)), Liu et al. 2025
([HTML](https://arxiv.org/html/2505.20606v1)); related: Mantena et al. 2019
and Tipaksorn et al. 2025 on the
[other pages](condition-side-information.md). Notes in
[readings](../related-work/readings/).

## Non-stationary conditions on a handheld

What the read benchmarks measure:

| Benchmark | Condition | Recognizers and result | Gap |
|---|---|---|---|
| [Speech Robust Bench](../related-work/readings/shah2024-speech-robust-bench.md) | 114 scenarios: real noise at 10 to 40 dB SNR over whole utterances, echo and room impulse responses, gain, resampling, lowpass, highpass, tempo, speed, pitch, effects, adversarial | Whisper large-v2 most robust; wav2vec 2.0 and HuBERT "severely lack robustness" on accents, social settings and spatial acoustics; larger models more robust | noise is steady and fixed-level; no event noise, no moving source, no path switch in the parts read |
| [BERSt](../related-work/readings/tuttosi2025-berst.md) | smartphone recordings at 19 static positions, 98 homes, shouted and spoken | Whisper medium.en 24.93% near body, 27.00% at 1-2 m, 35.02% other side of room, 45.10% outside the room; wav2vec 2.0 base 76.21% overall | one position per recording; 3.75 h; scripted English |

Searches for a benchmark of noise as events (vehicles, children) with a
start and end, a continuously moving microphone, or a mid-recording
path switch did not surface a primary paper that I could fetch and read.
Search summaries named a far-field benchmark with moving talkers (FFASR,
arXiv 2609.38897) and CHiME-3; neither was fetched. The evidence on
changing conditions that was read is [Lin et al. 2024](carried-state-and-adaptation.md)
(noise type switching along a stream), which is synthetic.

## Narrowband and codec augmentation for training

No primary ASR paper on band-limited or codec-simulated copies of wideband
training audio for a modern recognizer was located and read. What was read:

- Mantena et al. 2019 (hybrid DNN, 3,400 h wideband plus 600 h narrowband):
  naive mixing hurt narrowband (26.2 vs 21.0 narrowband-only); upsampling
  to a common rate plus a bandwidth flag reached 18.2; wideband stayed
  12.9 to 13.4 against 13.1 wideband-only.
- Tipaksorn et al. 2025: room-impulse augmentation of a single-microphone
  fine-tune cut far-field WER 79.54 to 65.39 on a Thai Whisper; SpecAugment
  alone reached 67.15 (same table).
- Liu et al. 2025: SpecAugment improved a Whisper-base pretrain on
  out-of-domain sets (LibriSpeech other 29.00 to 24.41; L2-ARCTIC 56.57 to
  46.11) but acoustic-centric augmentation (pitch, duration, accent-like)
  did better on several sets; neither covers codecs.
- SRB includes low-pass and resampling scenarios, giving a test for a
  band-limited input, though the per-scenario numbers were not read.

Whether generic spectrogram masking already covers narrowband input is
not answered by anything read: masking frequency bands during training is
not the same as a systematic 4 to 8 kHz absence, and Mantena shows the
naive handling of the sampling-rate mismatch is what hurts. Search
summaries (not read) point to a 2026 deepfake-source-tracing study where
telephony codec simulation (G.711) plus quantization and noise injection
beat training on real telephone data, and to a speech-enhancement paper
reporting Opus hurting ASR at very low bit rates; neither is an ASR
augmentation study. The cost of band-limited copies on clean wideband
input and the right mixing share for a modern recognizer are open in the
read literature.

## How often phone or Bluetooth paths deliver band-limited speech

Only web-page and developer-list material (not primary papers) was found:
Bluetooth hands-free profile links use narrowband CVSD at 8 kHz or
wideband mSBC at 16 kHz; mSBC is mandatory from HFP 1.6, but some
phone and headset combinations negotiate CVSD even when mSBC is offered.
These pages give no share of calls or sessions and none is cited as
evidence here; no peer-reviewed measurement was found. A pipeline should
expect 8 kHz input from some paths.

## Inverse direction (text toward audio as a recognizer-independent score)

Found in passing: none that scores a transcript by a text-to-speech
likelihood. The closest read result is [Fang et al. 2026](../related-work/readings/fang2026-asr-tra.md),
which scores candidate transcripts with CLAP, a general audio-text
embedding, as a reward independent of the recognizer's confidence; it
worked better than confidence on Whisper-Tiny with noise. Search
summaries reported CTC-score-based and speech-translation likelihood
filters (recognizer-dependent) and an unexplored TTS-likelihood filter;
none of these was fetched.
