**Source:** *PhoPunct: A Large-Scale Benchmark of Transformer Architectures for Vietnamese Punctuation Restoration* — [PDF](https://arxiv.org/pdf/2611.09107) · [arXiv](https://arxiv.org/abs/2611.09107)

## 2026-11-13 — fable-5.2, full text

Purpose: choosing form, size and data for a Vietnamese case+punctuation restorer for words-only phone ASR output.

### Claims

- Benchmark on the public News and Novels corpus of Pham et al. 2020:
  22,137,597 labelled tokens, News 19,902,295 and Novels 2,235,302, seven
  labels (O, Period, Comma, Colon, QMark, Exclam, Semicolon)
  (extract/nguyen2026-phopunct/html/2611.09107.md:53-63, :87).
- Per-word labels read from the first subword; input lowercased and stripped
  (:103-105).
- 16 models = 4 base encoders × 4 heads, plus PhoBERT-large + BiLSTM-CRF; all
  8 epochs, lr 2e-5, one run (:208-218, :323).
- Macro F1: PhoBERT-large+BiLSTM-CRF 61.35 News / 48.97 Novels; XLM-R+CRF
  58.62 / 50.18; XLM-R plain 58.25 / 49.79; ViBERT plain 57.47 / 49.82; mBERT
  plain 53.71 / 43.84; vELECTRA plain 53.80 / 40.70 (:244-260).
- A plain linear head matches or beats BiLSTM-CRF in 7 of 8 encoder–domain
  pairs, by up to 3.91 (ViBERT, Novels) (:272-281).
- Novels test has 320 colons and 6 semicolons; semicolon F1 is 0.00 for both
  leading systems (:89, :295).

### Meaning for our purpose

- Use a plain linear head; a CRF or BiLSTM on a pretrained encoder is not
  worth its cost under an ordinary fine-tuning budget.
- XLM-R base is a sound default teacher for punctuation; PhoBERT-large buys
  2.73 macro F1 on news and loses 1.21 on fiction.
- News and Novels is the large public Vietnamese punctuation corpus, and it
  has no case labels: if the files are lowercased, case must come from
  elsewhere.
- Rare marks (semicolon, colon in dialogue text) are not learnable from this
  data; a deployed label set of comma, period, question (perhaps
  exclamation) loses little.

### What it does not show

- No per-class numbers in the text (figure only), so comma and period
  accuracy for Vietnamese cannot be read off.
- No capitalisation, no ASR output, no conversational text (:323).
- One seed; small gaps are not established. Heads share the encoder's
  learning rate, which the authors say may under-train them (:307).
- PhoBERT-large was run with one head only, and size is confounded with
  encoder family (:121).
- Does not say whether tokens are syllables or segmented words, nor whether
  a word segmenter was applied for PhoBERT.
- No small model, no cost figures.

### Leads worth fetching

- Pham et al. 2020 (SOFSEM), the corpus paper: licence, tokenisation, whether
  case was kept (:347).
- Tran et al. 2021 (IEA/AIE), earlier encoder comparison on the same data,
  possibly with per-class scores (:348).
- Huyen et al. 2026, end-to-end Vietnamese ASR with punctuation and case for
  edge devices: the competing design for our deployment (:341).
- Vu, Nguyen, Nguyen 2026, *Vietnamese ASR: a revisit*: uses a fine-tuned
  text model for punctuation and case in a data pipeline (:351).
