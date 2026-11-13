**Source:** *FullStop:Punctuation and Segmentation Prediction for Dutch with Transformers* — [PDF](https://arxiv.org/pdf/2301.03319) · [arXiv](https://arxiv.org/abs/2301.03319)

## 2026-11-13 — fable-5.2, full text except the appendix precision/recall tables

Purpose: choosing form, size and data for a Vietnamese case+punctuation restorer for words-only phone ASR output. Line citations are to
`extract/vandeghinste2023-fullstop-dutch/html/2301.03319.md`.

### Claims

- **Model.** Token classifier on RobBERT (Dutch) or xlm-roberta-base
  (Dutch, English, German, French, Italian), labels `: - , ? .` and none;
  3 epochs, lr 4e-5, batch 8; trained on Europarl and/or the SoNaR corpus,
  75/25 split (`:128`, `:156-164`).
- **Input keeps true case** because the target ASR system emits it (`:126`).
- **In-domain per-class F1, Dutch Europarl model.** Period 0.961, comma
  0.811, question 0.849, dash 0.462, colon 0.655; macro 0.789; micro 0.983
  including the no-mark class at 0.994 (`:191-198`). SoNaR model: period
  0.855, comma 0.721, question 0.687 (`:192-194`).
- **Multilingual model, comma F1 by language.** English 0.798, German
  0.937, French 0.811, Italian 0.778, Dutch 0.813 (`:242`).
- **Stream segmentation.** A 200-word window slides over the text; a
  boundary is accepted if predicted in more than a fraction θ of the windows
  covering the word. On 1000 out-of-domain subtitle sentences, boundary F1
  0.8742 (SoNaR model, period only) and 0.9053 (period or question), against
  0.4219 for a seq2seq Transformer baseline with recall 0.2986 (`:308-326`).
  θ has no significant effect; adding the question mark is significant only
  at p < 0.10 (`:401-403`).
- XLM-R base 270M, large 550M parameters; a 5% macro-F1 gain from large is
  estimated, not run (`:234`).
- Released on Hugging Face under `oliverguhr` with a helper library (`:177`).

### Meaning for our purpose

- A plain token classifier with voting over sliding windows segments an
  unpunctuated stream well out of domain, and a seq2seq formulation fails on
  recall. Supports the tagger form and overlapped inference.
- Training-corpus register decides out-of-domain quality: the model trained
  on mixed-genre text beats the Europarl one on subtitles (0.874 vs 0.822)
  despite lower in-domain scores.
- Micro F1 that includes the no-mark class is uninformative; report
  per-class and say what is averaged.
- German comma F1 0.937 against 0.78–0.81 elsewhere shows comma difficulty
  depends on how rule-governed the language's commas are; Vietnamese is
  untested.
- The released checkpoints do not include Vietnamese.

### What it does not show

- No case restoration, and scores rely on cased input: not transferable to
  all-upper input.
- No real ASR output; the out-of-domain test is subtitle text.
- No small model, no timing; the baseline is one weak seq2seq system.
- Models trained on different corpora are scored on different test sets in
  the in-domain table (`:202`).
- Out-of-domain evaluation is sentence boundaries only; comma is not scored
  there.

### Leads worth fetching

- Guhr et al. 2021, the SEPP-NLG 2021 FullStop paper this extends
  (multilingual token classification; base-vs-large numbers).
- The SEPP-NLG 2021 shared-task overview (`:99`), for the CRF and GRU
  comparisons quoted at `:108`.
- Vandeghinste et al. 2018, Dutch punctuation as machine translation
  (`:97`).
