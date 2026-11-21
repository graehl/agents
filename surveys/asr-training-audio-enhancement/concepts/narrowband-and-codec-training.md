# Narrowband, codec and band-limited training data

[G] `single-source` per result. Full texts: Zhuang et al. 2017
([PDF](https://www.isca-archive.org/interspeech_2017/zhuang17_interspeech.pdf)),
Seltzer and Acero 2007
([PDF](https://microsoft.com/en-us/research/wp-content/uploads/2007/01/2007-mseltzer-taslp.pdf)),
Mantena et al. 2019 ([HTML](https://arxiv.org/html/1909.02667v1)), Hsu et al.
2021 ([PDF](https://arxiv.org/pdf/2104.01027)), Sukhadia and Umesh 2023
([HTML](https://arxiv.org/html/2211.01669)), Borodin et al. 2026
([HTML](https://arxiv.org/html/2609.37014)). Notes in
[readings](../related-work/readings/).

This page replaces the earlier statement that no paper on band-limited or
codec-simulated training copies had been found.

## What was found

| Question | Source | Recognizer | Result |
|---|---|---|---|
| Are band-limited wideband copies a usable stand-in for real narrowband (Bluetooth) data in newer languages? | [Zhuang 2017](../related-work/readings/zhuang2017-bluetooth-narrowband.md) | Apple hybrid DNN; Dutch, Portuguese, Thai, Turkish; 4 h Bluetooth test sets | band-limited wideband (400 to 600 h) 25.7 / 33.0 / 38.9 / 42.8 WER vs real narrowband (50 to 260 h) 24.0 / 26.1 / 29.8 / 38.4; initializing from the band-limited model and retraining on 20 h of Bluetooth: 17.4 / 23.5 / 20.7 / 29.8; up to 45% relative with cross-lingual initialization |
| Mixing a little wideband with narrowband data | [Seltzer 2007](../related-work/readings/seltzer2007-mixed-bandwidth.md) | GMM-HMM, WSJ0 12 h | at 10% wideband plus 90% narrowband: 13.9% (EM) vs 18.3% (feature imputation); full wideband 10.4% |
| Pooling 8 kHz with 16 kHz audio, and flagging the channel | [Mantena 2019](../related-work/readings/mantena2019-bandwidth-embeddings.md) | hybrid DNN | naive mixing hurt narrowband (26.2 vs 21.0 narrowband-only); upsample to a common rate (20.9); add a flag embedding (18.2) |
| The same in a self-supervised encoder | [Sukhadia 2023](../related-work/readings/sukhadia2023-channel-aware.md) | HuBERT-style encoder-decoder, 100 h fine-tune | narrowband test 16.8 (narrowband-only pretrain) vs 13.2 (pooled) vs 12.6 (pooled with channel indicator); wideband test-clean 11.5 vs 8.2 vs 7.6 |
| What large recipes do | [Hsu 2021](../related-work/readings/hsu2021-robust-w2v2.md) | wav2vec 2.0 base and large | resample every corpus, including 8 kHz Switchboard and Fisher, to 16 kHz and pool; telephone data in pre-training closes 66 to 73% of the in-domain gap; multi-domain pre-training 35 to 50% relative on unseen domains |
| Codec and band-limit augmentation share | [Borodin 2026](../related-work/readings/borodin2026-redimnet2plus.md) | speaker verification (adjacent), ReDimNet2 | 30% of examples codec-processed (MP3, Opus, AAC, AMR-NB, G.722, G.723.1, Speex, A-/mu-law, at 8 and 16 kHz), 30% waveform-only; SpecAugment and CutMix at 0.2 afterwards; stress-test EER 7.21 to 1.99 but confounded |

## Answering the wanted quantities

- **Share of degraded copies:** the only explicit recipe is Borodin's 0.5 /
  0.2 / 0.2 / 0.1 (keep / codec / waveform / both), for speaker
  verification, with no ablation. For recognition, no paper read gives a
  share; Zhuang and Mantena use whole datasets (transfer, or pooled sets).
- **Cost on clean wideband:** Mantena's embedding models keep wideband WER
  (12.9 and 13.0 vs 13.1 wideband-only) in a hybrid DNN; Sukhadia's pooling
  improves wideband (the pooled model also has more data). Borodin's first
  step worsened clean EER but is confounded. No isolated ablation was found.
- **Versus SpecAugment-style masking:** not compared in any read paper;
  Borodin applies both; Liu 2025 ([nonstationary page](nonstationary-and-augmentation.md))
  finds masking insufficient for out-of-domain acoustics in a small
  pretraining setting but does not test bandwidth.

## Search record (third pass)

Queries on mixed-bandwidth and multi-rate end-to-end ASR, codec
augmentation for ASR and speaker verification, Whisper or wav2vec telephony
fine-tuning, and a forward-citation pass from Mantena 2019 via OpenAlex. The
forward-citation list returned a super-resolution speaker-verification
paper, a unified mixed-bandwidth speaker embedding (arXiv 2012.00486),
HiFiTTS-2 (a high-bandwidth speech dataset), a bioacoustic mixed-sample-rate
transformer, Sampling Rate Adaptive Speaker Verification, and Sukhadia 2023
(read). No paper on Whisper or Conformer fine-tuning for telephone audio
with codec augmentation was found after two rounds of queries; a lossy-voice-coding
spoken-intent paper (journal, no open copy) and a codec source-tracing
paper were found but not read. What looks genuinely unexplored after this
effort: an ablation of codec or band-limit share on ASR WER for a
pretrained encoder, with clean wideband cost measured. "Searched and found
nothing" applies to that ablation; "not searched" applies to the call-centre
industrial literature behind paywalls.
