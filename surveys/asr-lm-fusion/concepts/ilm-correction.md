# Internal-LM correction: density ratio, ILME, LODR and CTC priors

Grounded from fetched full text (2026-11-09) unless a line says otherwise.
Map node: [survey.md § Internal-LM correction](../survey.md#internal-lm-correction-at-decode-time).
Extends the speech-recognition program's
[decode-time baselines](https://gerrit.ad.ai.sdl.com/cgit/aip-draft.git/tree/research/speech-recognition/surveys/tts-for-asr/concepts/inj-fusion-baselines.md)
(draft repo `research/speech-recognition/surveys/tts-for-asr/concepts/inj-fusion-baselines.md`),
which already carries the ILME paper's main table; it is not repeated here.

**Sources read** (full text, local extracts):

- McDermott, Sak, Variani, ASRU 2019, *A Density Ratio Approach to LM
  Fusion in End-to-End ASR* — [HTML](https://arxiv.org/html/2002.11268) ·
  [extract](../related-work/extract/mcdermott2019-density-ratio/html/2002.11268.md)
- Meng et al., SLT 2021, *Internal Language Model Estimation* —
  [PDF](https://arxiv.org/pdf/2011.01991) ·
  [extract](../related-work/extract/meng2021-ilme/meng2021-ilme.md)
- Variani et al., ICASSP 2020, *Hybrid Autoregressive Transducer (HAT)* —
  [HTML](https://arxiv.org/html/2003.07705) (read from the saved HTML; the
  extract failed the fidelity check and is not committed)
- Zeyer et al., Interspeech 2021, *Librispeech Transducer Model with
  Internal LM Prior Correction* — [HTML](https://arxiv.org/html/2104.03006) ·
  [extract](../related-work/extract/zeyer2021-ilm-prior/html/2104.03006.md)
- Zhou, Zheng, Schlüter, Ney, ICASSP 2022, *On LM Integration for RNN
  Transducer based Speech Recognition* — [HTML](https://arxiv.org/html/2110.06841) ·
  [extract](../related-work/extract/zhou2022-lm-integration-rnnt/html/2110.06841.md)
- Zheng et al., Interspeech 2022, *An Empirical Study of LM Integration for
  Transducer based Speech Recognition* (LODR) —
  [HTML](https://arxiv.org/html/2203.16776) ·
  [extract](../related-work/extract/zheng2022-lodr/html/2203.16776.md)
- Das et al. (AWS), ICASSP 2023, *Mask The Bias: ILME for CTC* —
  [HTML](https://arxiv.org/html/2305.03837) ·
  [extract](../related-work/extract/das2023-mask-the-bias/html/2305.03837.md)
- Yang, Phan, Schlüter, Ney, Interspeech 2025, *Label-Context-Dependent ILM
  Estimation for CTC* — [HTML](https://arxiv.org/html/2506.06096) ·
  [extract](../related-work/extract/yang2025-ctc-ilm/html/2506.06096.md)

## Mechanism

Score \(\log P(y\mid x) + \lambda_E \log P_{\text{ext}}(y) - \lambda_I \log
P_{\text{ILM}}(y)\). The variants differ in how \(P_{\text{ILM}}\) is had:

| Variant | \(P_{\text{ILM}}\) | Applies to | Extra decode cost |
|---|---|---|---|
| Density ratio | separate LM trained on the ASR transcripts | any | a second LM step |
| LODR | bigram (low-order) LM on transcripts | transducer, studied; any in principle | a bigram lookup |
| ILME | the model itself with the encoder zeroed | AED, transducer | one predictor/decoder pass |
| HAT | built in: label distribution factored from blank | transducer trained as HAT | none |
| Frame-level prior | mean CTC posterior over training frames, blank removed | CTC | none (a vector) |
| Masked ILME | CTC posteriors on masked audio, \(K\) partitions | CTC | \(K\) extra encoder passes |
| Distilled ILM | small LSTM distilled from the CTC model | CTC | a second LM step |

Zhou et al. name two decode-time effects: the subtraction rebalances the
label distribution, and it raises labels against the (high) blank so the
external LM weight can grow without deletions. Part of the gain is the
second effect, which a length reward also gives.

## Effectiveness

| Claim | Setting | Numbers | Grade |
|---|---|---|---|
| Correction beats shallow fusion, transducer, in-domain | LibriSpeech RNN-T, test-other (Zhou) | no LM 9.5; SF 5.5; density ratio 5.2; zero-encoder ILM 4.8; exact-ILM training 4.6 | reproduced in direction (Zeyer: >14% over SF) |
| Same, cross-domain | LibriSpeech → TED-LIUM 2 (Zhou) | 20.3; SF 16.4; DR 15.0; ILM 14.4; exact 14.0 | single-source |
| Much of the gain is blank-vs-label balance | LibriSpeech dev-other (Zhou) | SF 5.1 → SF + length reward 4.8 → ILM 4.4 | single-source |
| A bigram is enough as the subtracted prior | LODR, transducer, 4 corpora | LibriSpeech avg: SF 3.04, DR 3.00, ILME 2.99, LODR 3.01; WenetSpeech → AISHELL-1: 5.26, 5.28, 5.18, 4.95; a bigram from external text works as well as one from transcripts | single-source |
| Density ratio helps most with little target audio | YouTube RNN-T → Voice Search | no fine-tuning 17.5: SF 14.5, DR 12.5; with 10 h: 12.5 → 11.0 → 10.1; 1,000 h: 9.5 → 8.8 → 8.5; 21k h: 7.8 → 7.7 → 7.4 | single-source |
| CTC has an internal LM worth removing | 12-layer conformer CTC, 10k BPE, LibriSpeech (Yang) | test-other: no LM 7.2; external LM 5.3; + frame-level prior 4.9; + distilled ILM 4.8–4.9 | single-source |
| Context-dependent CTC ILM matters cross-domain | LibriSpeech → TED-LIUM 2 (Yang) | 18.7; ELM 15.9; frame prior 14.7; unigram 14.9; transcript LM 14.5; distilled ILM with smoothing 13.8 | single-source |
| Masked CTC ILME beats SF out of domain | conformer CTC, 4 out-of-domain sets (Das) | target-LM SF → ILME: LibriSpeech test-clean 3.2 → 2.9, test-other 6.6 → 6.5, VoxPopuli 7.9 → 7.9, Wikipedia 9.5 → 9.3, WSJ 3.2 → 2.9 | single-source |
| HAT's factored output makes ILM subtraction work | Google phoneme models, 40M utterances | first pass RNN-T 8.0 vs HAT 6.6; best ILM weight ≈0.95 against external weight 2.5 | single-source |

## Contested and quiet results

- In-domain the corrections are small and nearly interchangeable (LODR's
  LibriSpeech row: 2.99–3.04 across all four methods); the large gains are
  cross-domain.
- The program's TTS survey records ILME hurting a Whisper fine-tune by
  +8.0 WER on average with a trigram LM
  ([inj-fusion-baselines](https://gerrit.ad.ai.sdl.com/cgit/aip-draft.git/tree/research/speech-recognition/surveys/tts-for-asr/concepts/inj-fusion-baselines.md)).
- No located paper applies any of these to a character-level CTC model with
  a character LM, or to a low-resource language.

## What transfers to our setting

- **CTC students (w2v-BERT 0.6B, omniASR-CTC-1B):** the frame-level prior is
  free on the phone (one vector subtraction per frame, on label columns
  only) and carried most of Yang's in-domain gain (5.3 → 4.9). A transcript
  char n-gram as density ratio costs one KenLM lookup. Masked ILME costs
  \(K\) encoder passes and is out of the phone budget.
- **Zipformer transducer:** the icefall predictor is stateless, an
  embedding plus a kernel-2 convolution, so two tokens of context (as
  described in the Libriheavy paper, draft repo
  `research/speech-recognition/surveys/transcript-audio-alignment/related-work/extract/kang2024-libriheavy/`).
  Zero-encoder ILME is then one predictor-plus-joiner pass, and LODR's
  bigram matches what that predictor can represent.
- **Oswald / Qwen3-ASR AED:** ILME applies as in Meng et al.; its decoder is
  a full LM, so the ILM is strong and the correction more likely to matter.
- Our fusion grids already tune a length bonus β, which captures part of
  the label-vs-blank effect; the remaining gain is the rebalancing term.
