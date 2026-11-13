**Source:** *Fast and Accurate Capitalization and Punctuation for Automatic Speech Recognition Using Transformer and Chunk Merging* — [PDF](https://arxiv.org/pdf/1908.02404) · [arXiv](https://arxiv.org/abs/1908.02404)

## 2026-11-13 — fable-5.2, full text

Purpose: choosing form, size and data for a Vietnamese case+punctuation restorer for words-only phone ASR output.

### Claims

- A sequence-to-sequence model (LSTM or Evolved Transformer, 6 layers,
  embedding 256) maps lowercased unpunctuated English to formatted text, or
  to a six-symbol code of U/L case plus none/period/comma/question
  (extract/nguyen2019-chunk-merging/html/1908.02404.md:68, :111-115).
- Long input is split into chunks of k words advanced by k/2; in each
  overlap the last `min_words_cut` words of the earlier chunk are dropped
  and the later chunk's kept (:78-80).
- British National Corpus, 6M training sentences, 67 thousand test sentences
  (:121). Evolved Transformer F1 with vs without merging: upper-case 0.87 vs
  0.81, period 0.73 vs 0.61, comma 0.56 vs 0.41, question 0.71 vs 0.56
  (:229-272). Seq2seq LSTM: 0.62 / 0.42 / 0.19 / 0.30 with merging, 0.01–0.02
  lower without (:164-207).
- Plain-text output beats the six-symbol code: comma 0.56 vs 0.44, period
  0.73 vs 0.67, upper-case 0.87 vs 0.84 (:313-357).
- Best cut point is mid-overlap (4–10 of 15 words); case is insensitive to
  it, question marks sensitive (:146, :363).
- Comma is the hardest class and is mostly confused with no mark (:280).

### Meaning for our purpose

- Direct evidence that window-edge predictions are worse and that
  overlapping windows with a mid-overlap cut repair it: 6 to 15 F1 points
  per class for a Transformer. Cheap to adopt in a tagger: tag overlapping
  windows, keep each word's label from the window where it is most central.
- The authors are a Vietnamese ASR company (VAIS), but nothing here is
  Vietnamese: no data, no scores.
- The seq2seq form is a poor fit for the phone: autoregressive decoding and
  the risk of changing words; the paper notes its model always emits a word
  for a word (:280) but does not measure word fidelity.

### What it does not show

- No tagger baseline and no pretrained encoder; absolute scores (comma 0.56)
  are far below later taggers, so the size of the merging gain for a strong
  tagger is unknown.
- "Fast" is asserted (:365); no timing is given.
- U merges first-letter and all-upper (:123); no mixed case.
- ASR output is simulated by stripping text (:84); no recognition errors.
- Chunk size used in the main tables is not stated; one corpus, one run.
- Trained 200 epochs on 500 MB of text for 20 hours (:68); no data-size
  study.

### Leads worth fetching

- Cho, Niehues, Waibel 2017, NMT-based segmentation and punctuation
  insertion for real-time spoken language translation: source of the
  encoded-label format (:381).
- Tilk and Alumäe 2015/2016, the LSTM and BiRNN baselines every later paper
  compares against (:377).
