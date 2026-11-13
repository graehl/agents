**Source:** *A light-weight and efficient punctuation and word casing prediction model for on-device streaming ASR* — [PDF](https://arxiv.org/pdf/2407.13142) · [arXiv](https://arxiv.org/abs/2407.13142)

## 2026-11-13 — fable-5.2, full text

Purpose: choosing form, size and data for a Vietnamese case+punctuation restorer for words-only phone ASR output. Line citations are to
`extract/you2024-cnn-bilstm/you2024-cnn-bilstm.md`.

### Claims

- **Model.** 5000-piece BPE, 100-d embeddings, 3 residual 1-D conv layers,
  2 BiLSTM layers and 1 unidirectional LSTM (hidden 384), two heads: 4
  punctuation labels and 4 case labels (lower, all-upper, first-upper,
  mixed). Only each word's first subword enters the LSTMs (`:45-49`,
  `:107`). Loss = case + 0.7 × punctuation (`:79`, `:107`).
- **Data.** 55M English words: 57.6% Wikipedia, 25.3% interview
  transcripts, 17.1% TED; sentences with other marks discarded; 200-token
  sequences; 30 epochs in about 2 h on one GPU (`:87-97`, `:101`, `:107`).
- **IWSLT 2011 reference test, punctuation F1.** Comma 61.5 (P 71.5, R
  54.0), period 79.5, question 72.1, overall 71.0; CT-Transformer 69.3 /
  80.2 / 79.2 / 74.9; best earlier non-Transformer overall 65.1 (`:124-132`).
- **Case F1.** All-upper 98.9, first-upper 84.9 (P 85.4, R 84.4), mixed
  80.0, overall 87.8, against 82.4 for a 2017 BiRNN (`:139-142`).
- **Cost.** Quantized ONNX 7 MB and 10 ms for one paragraph on an Intel
  Core i5-1035G1 under sherpa-onnx; CT-Transformer 280 MB and 25 ms
  (`:167-170`, `:178`).
- An added attention layer lowered punctuation F1 to 69.6 (`:131`).
- Largest first-upper error is prediction as lower-case, attributed to
  missed sentence-final marks; 20% of mixed-case words predicted first-upper
  (`:186`).

### Meaning for our purpose

- This is the exact form sherpa-onnx already runs: a two-head first-subword
  tagger, trainable from scratch on tens of millions of words in hours. It
  is the floor to beat and a ready runtime target.
- Its weak point is comma recall (54.0). Period F1 is also about 7 below
  RoBERTa-base numbers from other papers on the same test, so "periods are
  easy for small models" is only relatively true.
- Sentence-initial capitals are not free: they inherit period errors.
- The Wikipedia share was chosen for proper nouns; a Vietnamese analogue
  needs a names-rich source.

### What it does not show

- No pretrained-encoder baseline (BERT, RoBERTa) and no distillation; the
  one Transformer compared is CT-Transformer, with scores quoted from its
  paper. No Transformer case baseline at all.
- Training-data confound: baselines trained on 2.1M-word IWSLT, this model
  on 55M words of other text.
- Not streaming in the model sense: bidirectional over 200 tokens; no
  limited-lookahead result.
- Parameter count absent; whether the scored model was the quantized one is
  not stated; one timing on a laptop, no phone.
- "I" is merged into all-upper, inflating that class; mixed-case surface
  recovery is not described.
- English only, clean reference transcripts only.

### Leads worth fetching

- Chen et al. 2020, *Controllable time-delay Transformer for real-time
  punctuation prediction and disfluency detection* (`:205`): the sherpa-onnx
  alternative and a real limited-lookahead design.
- Hentschel, Tsunoo, Okuda 2021, *Making punctuation restoration robust and
  fast with multi-task learning and knowledge distillation* (`:206`).
- Švec et al. 2021, *Transformer-based automatic punctuation prediction and
  word casing reconstruction of the ASR output* (`:220`).
- Pahuja et al. 2017 (`:219`), the joint BiRNN case baseline.
