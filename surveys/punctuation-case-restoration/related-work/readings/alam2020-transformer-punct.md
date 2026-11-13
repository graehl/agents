**Source:** *Punctuation Restoration using Transformer Models for High-and Low-Resource Languages* — [PDF](https://aclanthology.org/2020.wnut-1.18.pdf)

## 2026-11-13 — fable-5.2, full text

Purpose: choosing form, size and data for a Vietnamese case+punctuation restorer for words-only phone ASR output. Line citations are to
`extract/alam2020-transformer-punct/alam2020-transformer-punct.md`.

### Claims

- **Setup.** Pretrained encoder + BiLSTM + linear layer, 4 labels, 256-token
  sequences, 10 epochs; English IWSLT (2.1M training words; test 12,626
  reference and 12,822 ASR words) and a new Bangla set (1.38M news words;
  tests on news, manual transcripts and ASR output at 14.8% WER) (`:89-95`,
  `:116`, `:164`, `:209`).
- **Encoder comparison, English reference / ASR overall F1.** DistilBERT
  72.7 / 61.8; BERT-base 76.9 / 64.9; ALBERT-base 78.4 / 66.0; RoBERTa-base
  80.3 / 68.2; RoBERTa-large 82.4 / 71.3; mBERT 75.9 / 64.6; XLM-R-base 79.0
  / 67.7; XLM-R-large 81.8 / 70.6 (`:180-204`).
- **Augmentation** (random unknown-token substitution, deletion, insertion
  at rate 0.15): RoBERTa-large 82.4 → 82.9 reference, 71.3 → 74.0 ASR; ASR
  comma precision 56.6 → 64.1. Deletion alone gives 73.1 (`:150-156`,
  `:280-291`).
- **CRF** on RoBERTa-large: 82.4 vs 82.4 reference, 70.9 vs 71.3 ASR
  (`:270-271`).
- **Bangla, XLM-R-large.** News 87.0, manual transcript 68.8, ASR 63.2;
  comma 81.2 / 38.1 / 36.9. Distil-mBERT 70.1 / 47.6 / 47.5. Merging to
  mark-or-none lifts ASR from 64.0 to 80.6 (`:226-240`, `:255-257`).
- Monolingual beats multilingual at equal size; large beats base (`:217`).

### Meaning for our purpose

- The clean-to-ASR drop is large (11 F1) and concentrated in comma
  precision; cheap token-noise augmentation recovers about a quarter of it.
  Worth adopting, with realistic Vietnamese confusions added.
- The Bangla result is our situation in miniature: train on news, test on
  speech of another register, and comma F1 falls from 81 to 38 before any
  ASR error. Training-text register matters more than recognition errors.
- XLM-R-large is the strongest choice where no good monolingual encoder
  exists; for Vietnamese there are monolingual options, so this ranking
  need not hold.
- A generic distilled encoder loses 4–7 F1 with no task distillation; comma
  and period lose similar amounts.
- No CRF.

### What it does not show

- No case. No small non-Transformer model. No model sizes or timings.
- Single runs on a test set with 46 (reference) and 35 (ASR) question marks.
- WER of the English ASR test is not given; Bangla speech is 65 minutes of
  read stories.
- Augmentation was tuned on a clean development set and tested on one ASR
  set; its Bangla effect was marginal (`:248`).
- The BiLSTM on top of the encoder is never ablated.

### Leads worth fetching

- Yi et al. 2020, adversarial multi-task BERT with POS tagging (previous
  best on ASR output, comma F1 70.8; `:193`).
- Makhija et al. 2019, BERT + BiLSTM-CRF (`:178`).
- Che et al. 2016, source of the IWSLT split everyone uses (`:89`).
- Żelasko et al. 2018, punctuation for conversational speech (`:108`).
