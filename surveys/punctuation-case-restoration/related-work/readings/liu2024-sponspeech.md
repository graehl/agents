**Source:** *Spontaneous Informal Speech Dataset for Punctuation Restoration* — [PDF](https://arxiv.org/pdf/2409.11241) · [arXiv](https://arxiv.org/abs/2409.11241)

## 2026-11-13 — fable-5.2, full text

Purpose: choosing form, size and data for a Vietnamese case+punctuation
restorer for words-only phone ASR output. Line citations are to
`extract/liu2024-sponspeech/html/2409.11241.md`.

### Claims

- **Dataset.** 665 hours of English podcast speech from Creative Commons
  YouTube videos with uploader-written (not automatic) subtitles; train 469 h
  / 147,209 utterances, dev 79 h, test 58 h, test-amb 60 h (`:54`, `:80-83`,
  `:105`). Utterances are cut at reference full stops and question marks;
  1.6 s minimum, 11.6 s mean, 45.0 s maximum (`:74`, `:128`). Three marks
  only: full stop, comma, question mark.
- **In-domain baselines, test set, overall F1:** BERT 75.4, EfficientPunct
  (BERT plus acoustic embeddings) 73.3, GPT-4 Turbo zero-shot 66.8, UniPunc
  65.3 (`:362-416`).
- **Per mark, BERT vs GPT-4 Turbo:** full stop 82.4 vs 77.5; comma 70.5 vs
  61.1; question 76.8 vs 74.0. GPT-4 Turbo's comma precision is 47.7 at
  recall 85.0; its full-stop precision 87.0 at recall 70.0 (`:390-416`).
- **Acoustics:** EfficientPunct beats BERT only on question marks, 77.0 vs
  76.8, and loses on commas, 67.4 vs 70.5 (`:362-399`). The authors note the
  same multimodal models beat BERT on MuST-C (`:521`).
- **Cross-domain:** trained on MuST-C (TED talks), tested on SponSpeech
  test: BERT 71.4, EfficientPunct 70.5 (`:204-231`); the authors put the
  loss from not training in-domain at "about 2.3% to 4.0%" (`:330`). Trained
  on SponSpeech, tested on MuST-C: EfficientPunct 74.5, BERT 72.7
  (`:288-314`).
- **Ambiguous split:** test-amb overall BERT 73.8, EfficientPunct 72.1,
  GPT-4 Turbo 66.4 (`:446-500`).

### Meaning for our purpose

- A fine-tuned encoder tagger beat a zero-shot frontier LLM by 8.6 overall
  F1 on spontaneous speech, with the LLM over-inserting commas. This
  supports a tagger as the form.
- Training on scripted or prepared speech costs a few F1 points on
  conversational speech, mostly in commas (64.7 vs 70.5 for BERT, `:225`,
  `:396`). Vietnamese training text should include transcribed spontaneous
  speech, not only news or books.
- The construction recipe (videos with human subtitles, filtered for
  punctuation density, music and language) is reusable for Vietnamese.
- Fusing acoustic embeddings into the tagger bought nothing here; a
  text-only restorer after the recognizer is not obviously leaving accuracy
  behind on this evidence.

### What it does not show

- BERT's size and variant are not stated; no small or distilled tagger.
- GPT-4 Turbo is zero-shot with an unreported prompt, and the paper does not
  say how outputs with changed words were scored.
- References are human subtitles, not recognizer output; no recognition
  errors. No capitalization scores although casing is in the data.
- Every utterance ends at a true sentence end, so the test does not exercise
  unsegmented long-form input.
- One run per cell, no variance. The cross-domain comparison changes
  corpus size and style together. The ambiguity classifier behind test-amb
  was trained on 100 samples and not evaluated (`:138`, `:322`).

### Leads worth fetching

- Liu and Beigi 2024, *Efficient ensemble for multimodal punctuation
  restoration using time-delay neural network* (EfficientPunct) — the
  acoustic baseline and its claimed efficiency.
- Zhu et al. 2022, *Unified multimodal punctuation restoration framework for
  mixed-modality corpus* (UniPunc).
- Sunkara et al. 2020, *Multimodal semi-supervised learning framework for
  punctuation prediction in conversational speech* — Fisher results.
- Kang et al. 2024, *Libriheavy: a 50,000 hours ASR corpus with punctuation
  casing and context*.
- Tündik et al. 2018, *User-centric evaluation of automatic punctuation in
  ASR closed captioning* — what readers actually need.
