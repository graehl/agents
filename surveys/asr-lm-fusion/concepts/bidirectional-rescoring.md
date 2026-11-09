# Bidirectional and discriminative n-best rescoring

Grounded from fetched full text (2026-11-09) unless a line says otherwise.
Map node: [survey.md § Rescoring](../survey.md#bidirectional-and-discriminative-rescoring).

**Sources read** (full text, local extracts):

- Salazar, Liang, Nguyen, Kirchhoff, ACL 2020, *Masked Language Model
  Scoring* — [HTML](https://arxiv.org/html/1910.14659) ·
  [extract](../related-work/extract/salazar2020-mlm-scoring/html/1910.14659.md)
- Xu et al. (Amazon), ICASSP 2022, *RescoreBERT* —
  [PDF](https://arxiv.org/pdf/2202.01094) ·
  [extract](../related-work/extract/xu2022-rescorebert/xu2022-rescorebert.md)
- Futami et al., ASRU 2021, *ASR Rescoring and Confidence Estimation with
  ELECTRA* — [HTML](https://arxiv.org/html/2110.01857) ·
  [extract](../related-work/extract/futami2021-electra-rescoring/html/2110.01857.md)
- Udagawa et al. (IBM), Interspeech 2022, *Effect and Analysis of
  Large-scale LM Rescoring on Competitive ASR Systems* —
  [HTML](https://arxiv.org/html/2204.00212) ·
  [extract](../related-work/extract/udagawa2022-large-lm-rescoring/html/2204.00212.md)
  (its main WER table did not survive HTML conversion; claims below are from
  its text and lexical-analysis table)
- Gandhe and Rastrow (Amazon), ICASSP 2020, *Audio-attention discriminative
  LM for ASR rescoring* — [HTML](https://arxiv.org/html/1912.03363) ·
  [extract](../related-work/extract/gandhe2020-audio-attention-dlm/html/1912.03363.md)
- Li et al. (Google), Interspeech 2020, *Parallel Rescoring with Transformer
  for Streaming On-Device Speech Recognition* —
  [HTML](https://arxiv.org/html/2008.13093) ·
  [extract](../related-work/extract/li2020-parallel-rescoring/html/2008.13093.md)
- Kannan et al. 2018 and Toshniwal et al. 2018 for rescoring against fusion
  ([causal LMs](causal-fusion-lms.md), [LM-aware training](lm-aware-training.md)).
- Xu et al., ICASSP 2018, *A Pruned RNNLM Lattice-Rescoring Algorithm* —
  [PDF](https://www.danielpovey.com/files/2018_icassp_lattice_pruning.pdf):
  **not read** (PDF-only, no extract). A web-search snippet attributes to
  it a 4× speedup over n-gram-approximation lattice rescoring with better
  accuracy; unverified here. Lattice rescoring matters for hybrid
  WFST decoders; our CTC prefix beam produces n-best lists, not lattices.

## Mechanisms

- **Pseudo-log-likelihood (PLL):** mask each token in turn and sum the
  masked-token log-probabilities, one encoder pass per token.
- **Distilled single-pass score:** regress a sentence score from the
  `[CLS]` vector onto the teacher's PLL (Salazar's sentence-level
  finetuning; RescoreBERT's MLM distillation, MD).
- **Discriminative rescoring:** train that score with MWER or MWED over
  first-pass n-best lists (RescoreBERT), or train a replaced-token detector
  (ELECTRA) so one pass yields per-token error probabilities.

## Effectiveness

| Claim | Setting | Numbers | Grade |
|---|---|---|---|
| PLL rescoring is large over a weak first pass | LibriSpeech LAS, 100-best, test-clean/other 7.26/20.37 | BERT-base trained on LibriSpeech text 4.79/16.50; adapted 4.58/15.96; GPT-2 117M 5.39/16.81 (dev); oracle 2.81/12.85 | single-source; weak baseline |
| Single-pass distillation keeps most of it | same | maskless sentence-level finetune 4.61/15.53 dev vs 4.37/15.17 PLL | reproduced in direction (RescoreBERT MD 4.67/16.15 vs PLL 4.54/16.08 on test) |
| Discriminative training adds a little more | same | MD-MWED 4.36/15.60 (−6.6%/−3.4% relative to MD) | single-source |
| A tiny distilled BERT beats a tiny LSTM rescorer, at lower latency | Alexa en/ja internal sets, vs a 4M NCE LSTM | 5M BERT: −3.1 / −7.8 / −7.8% relative; 170M: −6.6 / −12.0 / −12.7%. CPU, 2 threads, batch of 5 hypotheses, 16 tokens: LSTM 9.7 ms, BERT-5M 7.6, 17M 17.5, 170M 180 | single-source |
| Bidirectional single-pass ≈ causal Transformer rescoring | LibriSpeech CTC, 5.80/13.46 | Transformer LM 4.08/10.45 (×1.0 time); BERT PLL 4.02/10.25 (×27.1); finetuned P-ELECTRA 4.00/10.42 (×0.8) | single-source |
| Bidirectional helps a strong first pass where GPT-2 does not | Switchboard Conformer transducer, 100-best | BERT/RoBERTa PLL consistently reduce errors; GPT-2 trades deletions for insertions with no net gain | single-source |
| Rescoring recovers less than fusion | WSJ LAS (Kannan) | n-best rescoring gave "some reduction" but less than shallow fusion: correct prefixes are pruned before the list forms | single-source; also Toshniwal: shallow fusion raises oracle WER, so a second pass after it gains least |

## Cost on device (our arithmetic plus the one measured point)

- RescoreBERT's 5M model rescoring 5 hypotheses of 16 tokens took 7.6 ms
  on 2 CPU threads (server CPU, unspecified). An n-best of 16 per utterance
  is about 25 ms per utterance, a negligible real-time factor for
  multi-second clips even if the phone is 3× slower.
- PLL with masking costs one pass per token: 30–100 passes for a
  character-level hypothesis, which rules it out on a phone. Distilled or
  ELECTRA scoring is one pass.
- Units: every rescoring result here is word- or wordpiece-level on
  English or Japanese. A character-level MLM over Lao or Sinhala would be
  long-sequence; scoring in subwords is possible because rescoring, unlike
  fusion, does not have to match the recognizer's units.

## What transfers to our setting

- Rescoring cannot recover hypotheses the beam (16–32) already lost, and
  every comparison located shows fusion ≥ rescoring with the same LM. A
  bidirectional rescorer is therefore a second-pass add-on after fusion, not
  a replacement for the fusion LM.
- The add-on is cheap enough on device in the distilled or ELECTRA form.
  The gains located are 3–13% relative over a small LSTM rescorer, on
  large-text English or Japanese domains; no low-resource-language result
  was found.
- It needs n-best lists from our own decodes for discriminative training,
  which the logprob cache already makes cheap.
