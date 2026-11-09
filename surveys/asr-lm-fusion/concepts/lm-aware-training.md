# Training the recognizer to expect the fused LM

Question (graehl, 2026-11-09): can the acoustic model's training objective
account for the LM it will be fused with? Grounded from fetched full text
(2026-11-09) unless a line says otherwise.
Map node: [survey.md § LM-aware training](../survey.md#lm-aware-training).
Decode-time correction is the separate [ILM-correction](ilm-correction.md)
page.

**Sources read** (full text, local extracts unless noted):

- Prabhavalkar et al., ICASSP 2018, *MWER Training for Attention-based
  Seq2Seq Models* — [HTML](https://arxiv.org/html/1712.01818) ·
  [extract](../related-work/extract/prabhavalkar2018-mwer/html/1712.01818.md)
- Meng et al., Interspeech 2021, *MWER Training with LM Fusion* —
  [arXiv](https://arxiv.org/abs/2106.02302): **abstract only** (neither
  HTML route converted; PDF not extracted)
- Wang et al. (Google), Interspeech 2022, *Improving Rare Word Recognition
  with LM-aware MWER Training* — [HTML](https://arxiv.org/html/2204.07553) ·
  [extract](../related-work/extract/wang2022-lm-aware-mwer/html/2204.07553.md)
- Yang, Zhou, Schlüter, Ney, ASRU 2023, *Effect of LMs in Sequence
  Discriminative Training for Neural Transducers* —
  [HTML](https://arxiv.org/html/2310.07345) ·
  [extract](../related-work/extract/yang2023-lm-seq-disc-transducer/html/2310.07345.md)
- Gulcehre et al. 2015 (deep fusion) — [HTML](https://arxiv.org/html/1503.03535) ·
  [extract](../related-work/extract/gulcehre2015-deep-fusion/html/1503.03535.md);
  Sriram et al., Interspeech 2018 (cold fusion) —
  [HTML](https://arxiv.org/html/1708.06426) ·
  [extract](../related-work/extract/sriram2018-cold-fusion/html/1708.06426.md);
  Toshniwal et al., SLT 2018 (comparison) —
  [HTML](https://arxiv.org/html/1807.10857) ·
  [extract](../related-work/extract/toshniwal2018-lm-integration/html/1807.10857.md);
  Kim et al. 2021 and Cabrera et al. 2021 (cold fusion for RNN-T; see
  [causal LMs](causal-fusion-lms.md)).
- Kubo, Karita, Bacchiani, ICASSP 2022, LM-embedding prediction as an
  auxiliary loss — [HTML](https://arxiv.org/html/2202.07894) ·
  [extract](../related-work/extract/kubo2022-lm-embedding-transfer/html/2202.07894.md)
- Component fusion (Shan et al., ICASSP 2019): **metadata only**, no open
  full text found.

## Two families

1. **Sequence-discriminative training with the LM in the loop** (MWER, MMI,
   MBR): decode n-best lists *with* fusion, then minimize expected word
   errors of the fused score. The recognizer stays separate from the LM, so
   the LM can still be swapped, at the cost of the learned weights matching
   it.
2. **Architectural fusion** (deep, cold, component): feed the frozen LM's
   state or logits into the decoder through a learned gate. Requires an
   autoregressive decoder (AED or transducer predictor); CTC has none.

## Effectiveness

| Claim | Setting | Numbers | Grade |
|---|---|---|---|
| N-best MWER beats sampling-based MWER; needs CE interpolation | Google LAS | qualitative in the read text | single-source |
| LM-aware MWER beats MWER under shallow fusion | 120M streaming HAT (stateless two-token predictor), Voice Search; 127M LSTM LM | VS: MLE 6.3, MWER 6.0, LM-aware 5.5–5.6; rare-proper-noun Maps set 10.3 / 10.0 / 8.9–9.1; similar with a 70M conformer LM | single-source |
| Learned weights transfer without re-sweeping | same | fixed training weights at inference: 5.5–5.6 VS vs 5.5–5.6 swept | single-source |
| MWER with ILME fusion beats MWER with SF | 30k-hour transformer transducers, 6 test sets (Meng, abstract) | −8.8% vs MWER, −5.8% vs MWER-SF, average relative | single-source, abstract only |
| The training LM's strength matters less than hypothesis quality | phoneme transducer, LibriSpeech MMI/MBR (Yang 2023) | test-other CE 4.6 → MMI with word 4-gram 4.1; generating hypotheses with a 1-gram vs 4-gram matters more than the LM used in the loss | single-source |
| Shallow fusion ≥ deep and cold fusion in first pass | Switchboard and Google LAS (Toshniwal) | Eval2000 22.6 → SF 21.1, deep 21.7, cold 21.8; VS 5.6 → 5.3 SF, 5.3 cold | reproduced in direction for LibriSpeech RNN-T (Kim: SF 8.6 vs CF 9.4) |
| Cold fusion wins for some transducers | Google multilingual RNN-T (Cabrera) | Norwegian 24.5 → SF 24.2, CF 22.4 | contested (Kim) |
| Cold fusion needs a trained recognizer first | LibriSpeech RNN-T (Kim) | from scratch: did not converge; finetuned 10 epochs with frozen LM: works; a 15M LM swapped into a 53M-trained model works without retraining | single-source |
| Cold fusion lowers oracle WER, so it pairs with a second pass | Google VS (Toshniwal) | after production-LM rescoring: cold 5.0 vs SF 5.3; SF raised oracle WER | single-source |

## Which apply to which decoder

| Method | CTC (our 0.6B / 1B students) | Transducer (Zipformer 68M) | AED (Oswald, Qwen3-ASR 0.6B) |
|---|---|---|---|
| MWER / MBR with fused n-best | no located CTC result with a fused LM; the loss is defined for any model with sequence scores | measured (HAT, transformer transducer) | measured (LAS) |
| ILM-aware MWER | needs a CTC ILM ([ILM page](ilm-correction.md)) | measured (Meng) | measured (Meng) |
| Cold / deep / component fusion | not applicable: no decoder state to gate | measured, contested vs SF | measured, ≤ SF in first pass |
| Auxiliary LM-embedding loss (Kubo) | not applicable as published | measured | measured |

## What transfers to our setting

- For the CTC students, the measured route that accounts for the fused LM
  at training time is sequence-discriminative training over n-best lists
  decoded *with* the char LM. Its CTC instance is a
  [frontier void](../frontier.md#void-lm-aware-mwer-for-ctc-with-a-char-lm).
  Cost: one fused beam decode per training utterance per refresh, which
  our cached CTC log-probabilities make cheap only for a frozen encoder.
- For Zipformer, LM-aware MWER is the measured analogue (Wang's HAT also
  has a two-token stateless predictor). For AED, MWER-ILME (Meng) is the
  closest; both are fine-tuning stages after a converged model.
- Cold fusion keeps the LM step inside the decoder at every label step, so
  it costs at least what shallow fusion costs. Alone it beat shallow fusion
  only in Cabrera's RNN-T; combined with shallow fusion it gained a little
  in Kim's (test-other 8.6 → 8.3). It is not a phone-side win.
