# Non-stationary conditions, benchmarks, and how often phone paths are band-limited

[G] `single-source` per result. Full texts: Shah et al. 2024
([PDF](https://arxiv.org/pdf/2403.07937v3)), Tuttosi et al. 2025
([HTML](https://arxiv.org/html/2505.00059v2)), Saini et al. 2026
([PDF](https://arxiv.org/pdf/2609.38897)), Barker et al. 2017
([PDF](https://eprints.whiterose.ac.uk/110977/1/barker_csl.pdf)), Vincent et
al. 2017 ([PDF](https://eprints.whiterose.ac.uk/111196/1/vincent_CSL16.pdf)),
Shao et al. 2025 ([PDF](https://arxiv.org/pdf/2511.18421)), Liu et al. 2025
([HTML](https://arxiv.org/html/2505.20606v1)). Notes in
[readings](../related-work/readings/). Narrowband and codec training data
has its own page: [narrowband-and-codec-training](narrowband-and-codec-training.md).

## Non-stationary and handheld conditions

| Benchmark | Condition | Result | What it does not measure |
|---|---|---|---|
| [Speech Robust Bench](../related-work/readings/shah2024-speech-robust-bench.md) | 114 scenarios; real noise at 10 to 40 dB SNR over whole utterances, echo and room impulse responses, gain, resampling, lowpass and highpass, tempo, speed, pitch, effects, adversarial | Whisper large-v2 most robust; wav2vec 2.0 and HuBERT "severely lack robustness" on accents, social and spatial scenarios | steady noise at a fixed level; no event noise, moving source or route switch in the parts read |
| [BERSt](../related-work/readings/tuttosi2025-berst.md) | smartphone clips at 19 static positions in 98 homes | Whisper medium.en 24.93% near body, 27.00% at 1-2 m, 35.02% other side of room, 45.10% outside the room | one position per recording |
| [FFASR](../related-work/readings/saini2026-ffasr.md) | simulated far field; static and moving talker at matched SNR; interferers include directional transient sources | 15 systems: near field 4.4%; static high / mid / low SNR 10.1 / 20.5 / 41.3%; moving 11.5 / 23.2 / 43.5% (penalty 1.3 / 2.7 / 2.2 points) | moving talker with a static microphone, not a handheld microphone; transients are not a separate condition |
| [CHiME-3](../related-work/readings/barker2017-chime3.md) | tablet held by the talker in bus, cafe, street, pedestrian area; time-varying impulse responses model motion in simulated training | the street is the least stationary background (a passing vehicle changes the level within an utterance); microphone failures in channels 3 to 5 and in non-seated environments | participants' WER outcomes not read |
| [Vincent 2017](../related-work/readings/vincent2017-mismatches.md) | CHiME-3 environment, microphone and simulation mismatches | training on several environments and different microphones "barely affects" ASR; only the number of microphones matters; most methods behave alike on real and simulated data | end-to-end models |
| [DHAuDS](../related-work/readings/shao2025-dhauds.md) | audio-classification benchmark with dynamic severity and heterogeneous noise | tabulates that ASR TTA studies use fixed levels (SUTA, SGEM 10 dB, DSUTA 5 dB) | ASR |

This page replaces earlier statements that no benchmark with moving talkers
and no handheld mobile-device benchmark was located; FFASR and CHiME-3 were
fetched and read. Still not found after wider search: a benchmark whose
variable is noise as events with a start and end for ASR, a continuously moving handheld
microphone, or a mid-recording switch between the phone microphone and a
Bluetooth path. Search queries covered CHiME-3 to 8, DiPCo, VOiCES, AMI, DNS
Challenge, egocentric and wearable sets (the CHiME-8 MMCSG task was
identified, with its baseline using about 8 h of glasses data; not read),
in-car, impulsive and transient noise, sound-event overlap and VoIP packet-loss
benchmarks. The two nearest hits not read are the MMCSG glasses task and
packet-loss work already in the first pass (Dissen 2024). "Searched
widely, found nothing": event-noise ASR benchmarks and route-switch
benchmarks. "Not searched": CHiME-6 and DiPCo results, VoIP jitter corpora.

## Generic masking versus targeted augmentation

[Liu 2025](../related-work/readings/liu2025-acoustic-aware-augmentation.md):
in a Whisper-base pretraining on LibriSpeech-960 h, SpecAugment improved
LibriSpeech other from 29.00 to 24.41 and L2-ARCTIC from 56.57 to 46.11 but
acoustic-centric augmentation (pitch, duration, accent-like) did better on
several out-of-domain sets. It does not test bandwidth or codecs, so whether
masking already covers band-limitation is still not answered by it; see the
[narrowband page](narrowband-and-codec-training.md) for the nearest results.

## How often real phone paths are band-limited

No peer-reviewed measurement of the share of recordings or sessions that
reach a recognizer band-limited was found. Quantified or semi-quantified
statements, with source type:

| Statement | Source type |
|---|---|
| Users mostly speak to the assistant through wideband microphones; "a small fraction of usage happens over narrowband (8 kHz) Bluetooth headsets", no number | Industry research paper (Apple), read: [Zhuang 2017](../related-work/readings/zhuang2017-bluetooth-narrowband.md) |
| Bluetooth hands-free links use narrowband CVSD at 8 kHz or wideband mSBC at 16 kHz; mSBC is mandatory in HFP 1.6; some device pairs negotiate CVSD although mSBC is offered | Developer and vendor documentation (Espressif, Microchip, an ITU-T test methodology page, Apple developer mailing-list threads), seen only as search summaries, not read |
| Crowd-sourced phone corpora: Common Voice in 48 kHz MP3 source, other corpora 22.05 to 48 kHz and typically resampled to 16 kHz | Dataset papers, seen only as search summaries |
| VoLTE share of calls at one US operator, "nearly 40%" in one snippet and "well over half" in the headline of the same news article; VoLTE is not the same as wideband | Industry news, one search result; page not retrievable (HTTP 403), not read |

## Inverse direction

Moved to [carried state and adaptation](carried-state-and-adaptation.md):
READ (a TTS-likelihood score of a transcript against the audio) was found and
read in this pass, overturning the earlier "none located" statement.
