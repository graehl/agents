**Source:** *Evaluating OpenAI's Whisper ASR for Punctuation Prediction and Topic Modeling of life histories of the Museum of the Person* — [PDF](https://arxiv.org/pdf/2305.14580) · [arXiv](https://arxiv.org/abs/2305.14580)

## 2026-11-13 — fable-5.2, full text

Purpose: choosing form, size and data for a Vietnamese case+punctuation
restorer for words-only phone ASR output. Line citations are to
`extract/gris2023-whisper-punct/html/2305.14580.md`.

### Claims

- **Setup.** Whisper large multilingual (1550M), language forced to
  Portuguese, temperature 0.15, conditioning on previous text (`:213`), on
  10 Brazilian Portuguese life-history interviews, 16:48:34 h, 1,349 turns
  of spontaneous speech with human punctuation in seven marks (`:219-225`).
  Audio diarised first, then transcribed, then aligned to the reference by a
  custom segment aligner; 85.44% of reference segments aligned (`:426`,
  `:464-472`). WER 14.50%, CER 8.13% on the aligned part (`:474`).
- **Per-mark F1 (P / R):** comma 77.5 (78.1 / 77.0); question 68.0 (71.5 /
  64.9); full stop 63.9 (59.4 / 69.2); ellipsis 17.4; exclamation 5.1 (17.2
  / 3.0); semicolon and colon never produced; macro F1 46.4 ± 32.7
  (`:496-503`).
- **Style mismatch.** Whisper wrote 11,062 sentences against 8,740 in the
  reference (26.6% more), average length 13.02 vs 15.79 words; 18,100 vs
  14,954 commas and 10,904 vs 8,350 full stops (`:227`, `:256-264`,
  `:283-291`, `:308-309`). Reference has 651 colons and 83 semicolons;
  Whisper 0 (`:394-408`).
- **Segmentation sensitivity.** Running on diarised segments changed 12
  marks in one short excerpt (`:428`).
- **Downstream.** A punctuation-segmented video summary scored higher BLANC
  than an unpunctuated one in 9 of 10 videos (`:560-596`).
- **Second-hand results quoted in related work** (not verified against the
  originals): RoBERTa-large with ASR-error augmentation on IWSLT 2011,
  overall F1 82.9 on reference text and 74 on ASR text (`:59`); a
  word-plus-speech-embedding model 72.9 and 68.8 (`:65`); BiLSTM with timing
  on Fisher 66.1 / 67.3 / 59.2 (`:69`); MuSe on Fisher 75.6 / 75.6 / 81.3
  with wav2vec features best (`:71`); Nozaki's end-to-end CTC on MuST-C 61.1
  / 92.5 / 74.1 (`:73`).

### Meaning for our purpose

- Whisper-large is the obvious teacher or pseudo-labeller for a language
  without formatted audio. On spontaneous non-English speech its commas are
  usable (77.5 F1) but full stops are 63.9 and anything beyond comma, full
  stop and question mark is absent or near zero. A restorer trained on
  Whisper output inherits a three-mark inventory and a short-sentence style.
- Much of the "error" is convention: the human reference uses longer
  sentences. A Vietnamese evaluation needs a reference whose punctuation
  style matches what we want the product to output.
- The IWSLT figures give the size of the reference-text to ASR-text drop for
  a strong text tagger: about 9 overall F1, 24 on question marks.

### What it does not show

- No comparison system: no text restorer on the same audio, no other
  recogniser, no cascade. "State of the art" is asserted across datasets
  the authors themselves call not comparable (`:77`).
- Case is not scored, only counted in one example (`:195-205`).
- Marks appear to be scored at aligned segment ends, with 14.56% of segments
  dropped; the aligner is described only in outline.
- Internal inconsistencies: the summary table gives 77.3 / 62.3 / 67.6
  (`:99`) against 77.5 / 63.9 / 68.0 in the results table; the female
  exclamation row (P 31.2, R 0.4, F1 6.8, `:518`) is arithmetically
  impossible.
- Portuguese only; 10 interviews.

### Leads worth fetching

- Alam, Khan, Alam, W-NUT 2020, *Punctuation restoration using Transformer
  models for high- and low-resource languages* (`:615`): text-only
  pretrained taggers, ASR-error augmentation, and a low-resource language
  (Bangla). The most directly relevant unfetched paper for our default
  route.
- Sunkara et al., Interspeech 2020, *Multimodal semi-supervised learning
  framework for punctuation prediction in conversational speech* (`:647`):
  the with/without-audio numbers over BERT that this extract lacks.
- Nozaki et al., Interspeech 2022 (`:637`).
- Păiş and Tufiş 2022, *Capitalization and punctuation restoration: a
  survey* (`:642`).
- Żelasko et al., Interspeech 2018 (`:655`): timing features only, the
  cheap acoustic variant.
- Yi and Tao, ICASSP 2019 (`:654`).
