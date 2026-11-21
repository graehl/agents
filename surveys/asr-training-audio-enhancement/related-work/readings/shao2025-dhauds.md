**Source:** *DHAuDS: A Dynamic and Heterogeneous Audio Benchmark for Test-Time Adaptation* — [PDF](https://arxiv.org/pdf/2511.18421) · [arXiv](https://arxiv.org/abs/2511.18421)

# shao2025-dhauds

2026-11-21, sonnet-5.5. Purpose: how existing ASR test-time adaptation papers
define their test conditions, and a benchmark with changing severity. Read:
abstract, introduction, Table 1, benchmark description; results not read.

**Claims.** The authors tabulate that prior audio TTA studies use fixed
corruptions: SUTA with Gaussian or CHiME-3 noise on LibriSpeech, SGEM at a
fixed 10 dB SNR (MS-SNSD), DSUTA at a fixed 5 dB SNR (MS-SNSD), none with
dynamic severity or heterogeneous noise mixtures
([extract](../extract/shao2025-dhauds/html/2511.18421.md):29-43). DHAuDS
proposes four corrupted audio-classification benchmarks (UrbanSound8K-C,
SpeechCommands V2-C, VocalSound-C, ReefSet-C) with dynamic severity,
heterogeneous noise and independent adaptation and evaluation sets.

**Means for us.** Confirms, from a third party, that the ASR TTA literature
tests at one noise level per condition; the benchmark that varies severity
is for audio classification, not ASR.

**Not shown.** Any ASR result.
