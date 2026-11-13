**Source:** *Efficient Automatic Punctuation Restoration Using Bidirectional Transformers with Robust Inference* — [PDF](https://aclanthology.org/2020.iwslt-1.33.pdf)

## 2026-11-13 — fable-5.2, full text

Purpose: choosing form, size and data for a Vietnamese case+punctuation restorer for words-only phone ASR output. Line citations are to
`extract/courtland2020-robust-inference/courtland2020-robust-inference.md`.

### Claims

- **Model.** RoBERTa-base, then a per-token linear layer, then a layer over
  the concatenated states of the whole 100-token window that emits all the
  window's labels at once; trained only on IWSLT's 2.1M words (`:37-39`,
  `:70-72`, `:78`).
- **Aggregation.** Windows overlap; each token's pre-softmax activations are
  summed over the windows containing it. Overall F1 by predictions per
  token: 1 → 76.3, 2 → 79.4, 3 → 81.8, 6 → 83.2, 9 → 83.9, at CPU cost 1×,
  1.8×, 2.6×, 5.2×, 7.7× (`:92-99`). Summing activations beats averaging
  probabilities by 0.3 (`:107`).
- **Best result, IWSLT reference.** Comma 76.2, period 87.7, question 87.9,
  overall 83.9, against 68.6 for the previous best recurrent model (`:58-59`).
- **Encoders.** RoBERTa-large 83.5, XLNet-base 82.9, T5-base 81.9, BERT-base
  80.6, ALBERT-base 75.4, DistilRoBERTa 73.7 (`:61-66`). Large is about 1.5×
  slower with no gain; DistilRoBERTa about 1.2× faster (`:109`).
- Focal loss and class weighting did not beat cross-entropy (`:86`).
- Predicting one token per forward pass is over 15× slower for +2.2 over
  unaggregated parallel prediction (`:88`).

### Meaning for our purpose

- Overlap-and-sum is a cheap inference-time gain available to a teacher (to
  make better soft labels) and, at a 2–3× cost, to the phone model.
- Base-size is enough for a teacher on this evidence; plain cross-entropy
  is enough.
- Generic half-depth distillation loses about 10 F1 here, with comma (−9.1)
  and period (−6.9) both hit.

### What it does not show

- The unaggregated score (76.3) is below a plain per-token RoBERTa-base
  tagger in Alam et al. on the same test (80.3), so part of the aggregation
  gain may repair this paper's window-concatenation head. No plain-tagger
  control.
- Reference transcripts only; no ASR-output result, no case.
- No hyperparameter tuning and single runs (`:121`); the test set has 46
  question marks.
- The stated DistilRoBERTa loss (9.1) differs from the table (10.2); the
  "48.7% relative improvement" matches error reduction, 15.3 of 31.4, not
  relative F1 (our arithmetic from `:58-59`, `:117`).
- Window 100 in the best model, but the introduction's example is window 50
  step 20 (`:23`); the stride used for 9 predictions is not stated.

### Leads worth fetching

- Boháč et al. 2017, *Text punctuation: an inter-annotator agreement study*
  (`:136`): human agreement of about 76% on location and 70% on mark, the
  ceiling argument for comma F1.
- Tündik et al. 2018, on punctuation versus word error for readability
  (`:21`).
- Kim 2019, layer-wise attention recurrent model, the prior state of the
  art (`:58`).
