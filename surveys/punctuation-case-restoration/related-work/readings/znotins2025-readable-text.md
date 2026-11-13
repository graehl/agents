**Source:** *From Conversational Speech to Readable Text: Post-Processing Noisy Transcripts in a Low-Resource Setting* — [PDF](https://aclanthology.org/2025.wnut-1.15.pdf)

## 2026-11-13 — fable-5.2, full text

Purpose: choosing form, size and data for a Vietnamese case+punctuation
restorer for words-only phone ASR output. Line citations are to
`extract/znotins2025-readable-text/znotins2025-readable-text.md`.

### Claims

- **Data.** LATE-Media, about 70 hours of conversational Latvian broadcast
  speech, more than 250 speakers; test has 1,595 commas, 2,389 periods, 419
  question marks, 3,257 title-case and 78 all-caps tokens, 7.2 words per
  sentence. Exclamation marks, ellipses and dashes are mapped to periods;
  colons and semicolons dropped (`:47`, `:51`, `:59-64`).
- **Two test conditions:** reference transcripts, and the output of a
  Latvian-fine-tuned Whisper large-v3 at 12.7 WER (`:85`, `:117`).
- **Recognizer output, punctuation F1 / capitalization F1:** XLM-RoBERTa
  (off the shelf, Europarl-trained) 75.1 / 78.9; GPT-4o 78.2 / 81.3; GPT-4o
  mini 75.8 / 79.7; GPT-4o fine-tuned 81.5 / 84.4; GPT-4o mini fine-tuned
  79.3 / 82.4; EuroLLM-1.7B fine-tuned 79.0 / 82.7; Gemma-2-2B fine-tuned
  79.1 / 81.9; the fine-tuned Whisper's own formatting 78.3 / 81.8
  (`:117-126`).
- **Reference transcripts:** XLM-R 77.4 / 84.3; GPT-4o fine-tuned 85.1 /
  91.8; Gemma-2-2B fine-tuned 81.6 / 88.3 (`:128-135`).
- **Question marks on recognizer output:** Whisper-lv 72.1, GPT-4o
  fine-tuned 68.9, Gemma 63.2, XLM-R 57.5 (`:117-126`).
- **Word changes** (share of utterances changed): XLM-R 0.0%; GPT-4o 16.4%;
  GPT-4o mini 24.6%; fine-tuned GPT-4o 1.4%, GPT-4o mini 1.5%, Gemma 1.7%,
  EuroLLM 2.7% (`:165-172`). WER introduced on reference text: GPT-4o 3.0,
  GPT-4o mini 4.7, fine-tuned models 0.3–0.4 (`:130-135`).
- **Error analysis of 100 mismatches:** 57 real errors, 43 valid
  alternatives; 21 needed the audio to decide (`:147-155`).
- About 50% of annotated mispronunciation, number and written-form
  corrections were made by the LLMs; the authors call the test set too small
  (`:157`).

### Meaning for our purpose

- The only source here with capitalization and with real recognizer output.
  At 12.7 WER punctuation loses 2–4 F1 and capitalization 5–7 F1 against
  reference text; evaluation on reference text overstates what users see.
- Roughly 70 hours of formatted conversational transcripts sufficed to
  bring 2B models to within 2.5 F1 of fine-tuned GPT-4o. The data
  requirement for an in-domain model is modest.
- A regenerating model, even fine-tuned, still changes words in 1.4–2.7% of
  utterances; a tagger changes none. For a restorer that must not alter the
  transducer's words, this decides the output form.
- 43% of counted "errors" were acceptable alternatives, so F1 near 80
  against one reference is close to what the metric can resolve.
- Question marks are where audio helps (72.1 vs 57.5–68.9). A text-only
  Vietnamese restorer should expect its weakest mark to be the question mark
  unless questions are lexically marked.

### What it does not show

- No encoder tagger trained on the same data. The XLM-R baseline was
  trained on Europarl by others, so the 4–6 F1 lead of fine-tuned LLMs on
  recognizer output mixes model form with in-domain training.
- The zero-shot prompt asks for grammar and mispronunciation corrections
  and number conversion (`:91`), so zero-shot change rates include requested
  edits.
- One language, one corpus, one recognizer, one WER; no variance; all-caps
  scores rest on 78 tokens.
- No speed, memory or model-size measurement; no agreement statistic behind
  the "inter-annotator disagreement" remark (`:176`).

### Leads worth fetching

- Guhr, Schumann, Bahrmann, Böhme 2021, *FullStop: multilingual deep models
  for punctuation prediction* — the XLM-R tagger family used as baseline.
- Alam, Khan, Alam 2020, *Punctuation restoration using transformer models
  for high- and low-resource languages* (W-NUT) — augmentation that
  simulates recognizer errors.
- Fu et al. 2021, *Improving punctuation restoration for speech transcripts
  via external data* — domain-adaptive sampling.
- Polácek et al. 2023, *Online punctuation restoration using ELECTRA model
  for streaming ASR systems*.
- Varavs and Salimbajevs 2018, *Restoring punctuation and capitalization
  using transformer models* — joint case and punctuation in a morphologically
  rich low-resource language.
