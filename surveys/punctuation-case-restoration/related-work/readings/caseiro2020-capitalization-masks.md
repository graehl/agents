**Source:** *Mixed Case Contextual ASR Using Capitalization Masks* — [PDF](https://www.isca-archive.org/interspeech_2020/caseiro20_interspeech.pdf) · [ISCA page](https://www.isca-archive.org/interspeech_2020/caseiro20_interspeech.html)

## 2026-11-14 — fable-5.2, sections 1–5 (contextual-biasing detail in 3.4 and 4.2–4.3 skimmed)

Purpose: we are fine-tuning gipformer, a Vietnamese transducer whose word
pieces are single-case, to write case and punctuation by adding a few
marker outputs instead of cased copies of every piece. Is there precedent,
and what did they choose?

**Claims** (line numbers in `extract/caseiro2020-capitalization-masks/caseiro2020-capitalization-masks.md`)

- A word is written as its single-case form followed by an optional
  *capitalization mask*: one bit per character, grouped four at a time into
  one of 16 control tokens, trailing zeros dropped. `MacGyver` is
  `macgyver` plus the tokens for `1001 0000` (`:54-56`). So the mask comes
  **after** the word and can express any mixed case.
- The word-piece vocabulary is built from lower-cased text plus those 16
  entries; no piece spans letters and mask characters; 4,096 pieces
  (`:76-86`).
- Streaming RNN-T (8 LSTM encoder layers, 2 prediction layers), trained
  from scratch on 184M English utterances, mostly mixed-case references
  (`:64`, `:72`).
- Voice-search test: WER 6.5 for both the cased-vocabulary baseline and
  the mask model, 6.4 for a lower-case model; capitalization error rate
  13.4 against 13.1 in the mask model's favour (Table 3).
- The mask model writes about 44% more upper-case characters than the
  cased baseline and is better on named entities; first-word
  capitalization is unchanged (`:188`).
- Their own framing: "a form of sequential multi-task modeling", the two
  tasks interleaved in one output sequence instead of separate heads
  (`:192`).
- The motive was contextual biasing: case variants multiply entries in the
  biasing model; with masks the biasing model ignores mask tokens.

**Meaning for our purpose**

- Direct precedent for markers instead of cased pieces, on a transducer,
  with no word-accuracy cost against a cased vocabulary and slightly
  better capitalization.
- Their mask follows the word; our first design puts the marker before
  it. After the word, the model has already committed to the word when it
  decides case, and the prediction network conditions on it. Worth an
  arm.
- Their per-character mask handles mixed case, which our two markers do
  not; Vietnamese does not need it.

**What it does not show**

- Punctuation: not in the paper.
- Moving a trained single-case model to the mask vocabulary: they train
  from scratch, so nothing on how to start the new outputs.
- Small data: 184M utterances.
- A comparison with a text tagger after recognition.

**Leads**

- Their reference [6] for the capitalization error rate metric.
