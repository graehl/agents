# Frontier: asr-lm-fusion

Depth: analysis only (voids and their prior-art checks); no proposal
drafted. Map: [survey.md](survey.md). Coverage cutoff 2026-11-09.

## Void map

Axes: LM architecture × LM unit × decoder × regime (phone-size LM, low-
resource language). Only cells bearing on the program's bakeoff are listed.

| Cell | Status | Evidence |
|---|---|---|
| LSTM, character, CTC, phone-size, low-resource | filled | program bakeoff (Sinhala); Maas 2015 for CTC + char RNN LM (not read here) |
| Gated convolution, character, CTC-like letter AM, large | filled | Likhomanenko 2019 |
| Transformer, subword, AED, large | filled | Irie 2019 |
| Transformer, character, any decoder, phone-size | untried | none located |
| RWKV / Mamba / linear attention, any unit, fusion LM | untried | none located |
| LookupLM, wordpiece, transducer, server | filled | Huang 2021 |
| LookupLM, character, any decoder | untried | none located |
| ILM / prior correction, subword, CTC | filled | Yang 2025, Das 2023 |
| ILM / prior correction, character, CTC, low-resource | untried | none located |
| LM-aware MWER, transducer / AED | filled | Wang 2022, Meng 2021 |
| LM-aware MWER, CTC with fused LM | untried | none located |
| Bidirectional rescoring, low-resource language | untried | none located |

## Void: linear-recurrent char LMs in fusion

- **Why unexplored:** RWKV and Mamba were developed and evaluated as
  large pretrained LMs; ASR work uses them as encoders (RWKV streaming
  encoder, Mamba encoders/decoders), not as fusion LMs. For a small LM the
  incumbent LSTM already has the same constant-state inference property, so
  the selling point does not differentiate.
- **Prior art checked** (2026-11-09): web searches "Mamba language model
  shallow fusion speech recognition rescoring", "RWKV language model ASR
  shallow fusion on-device", "state space model S4 Mamba language model
  rescoring automatic speech recognition n-best", and a combined extended
  search over Mamba/RWKV/linear attention with shallow fusion and LSTM
  comparison. Found only encoder uses (arXiv 2309.14758, 2409.07273,
  2501.02832) and a 2025 Interspeech encoder comparison; no fusion LM.
- **Capstone value:** impact low-to-moderate (would tell whether gated
  linear recurrences beat LSTM per step at 5–50M); tractability high;
  novelty-confidence moderate (search was web-level, not a forward-citation
  crawl).

## Void: LM-aware MWER for CTC with a char LM

- **Why unexplored:** MWER papers target AED and transducers, whose
  decoders give per-label posteriors the LM can be combined with; CTC
  sequence training historically used lattice-free MMI with phone LMs.
- **Prior art checked:** web search "minimum word error rate training CTC
  with external language model shallow fusion during training" returned
  Meng 2021 (transformer transducers) and Lu et al. arXiv 2010.12673 (HAT),
  neither CTC. Yang 2023 trains transducers, not CTC.
- **Capstone value:** impact moderate (answers graehl's training question
  for the program's main recognizers); tractability moderate (n-best
  generation with the fused LSTM per update; frozen-encoder variant cheap);
  novelty-confidence moderate.

## Void: ILM correction with character CTC on low-resource languages

- **Why unexplored:** ILM work is on English/Mandarin subword models with
  large transcripts; low-resource work rarely tunes more than α and β.
- **Prior art checked:** web search "internal language model estimation
  CTC" found Yang 2025 and Das 2023, both subword English.
- **Cheapest discriminating check:** arm 1 of
  [§ Next bakeoff arms](survey.md#next-bakeoff-arms).

## Provisional claims

- **Claim:** context-dependent CTC ILM estimation by distillation beats
  shallow fusion by more than 13% relative cross-domain (Yang 2025).
  Incumbent: shallow fusion and frame-level prior. Regime: LibriSpeech →
  TED-LIUM 2, 10k BPE conformer CTC. Authors control training and
  evaluation; no independent reproduction located. Relevance: arm 1.
  Revisit: when arm 1 reports (unscheduled reminder).
