**Source:** *Cantonese Punctuation Restoration using LLM Annotated Data* — [PDF](https://www.isca-archive.org/interspeech_2025/suen25_interspeech.pdf)

## 2026-11-13 — fable-5.2, full text

Purpose: choosing form, size and data for a Vietnamese case+punctuation
restorer for words-only phone ASR output. Line citations are to
`extract/suen2025-cantonese-llm-annotated/suen2025-cantonese-llm-annotated.md`.

### Claims

- **Pipeline.** Transcribe 237 hours (1,487 videos, 4 channels) of Cantonese
  YouTube with a proprietary recognizer; punctuate the transcripts with a
  prompted LLM; fine-tune a 12-layer, 768-wide encoder as a 4-class token
  tagger on the result (`:101-105`, `:111`, `:117`).
- **Choosing the annotator** on HKCanCor (human-punctuated spontaneous
  speech and radio; 12,480 utterances after cleaning), overall F1:
  Qwen-2.5-72b 73.6, GPT-3.5-turbo 70.1, GPT-4o-mini 69.9, Llama-3.3-70b
  62.7, Yi-1.5-34B 52.9 (`:38-42`, `:91`). Comma precision is 39.4–46.3 for
  every LLM (`:38-42`).
- **Word-preservation control.** Prompt forbids edits and demands JSON;
  temperature 0.1; up to three retries, then discard. Discard rate below
  0.7% for most models, about 5% for Yi-1.5-34B (`:54`, `:62-65`, `:81`).
- **Corpora.** YouTube 130,888 utterances, 3.1M words, 19.0% code-mixed,
  19,826 question marks; Cantonese Wikipedia 301,521 sentences, 9.1M words,
  757 question marks (`:92-93`).
- **Students on HKCanCor, overall F1** (Wikipedia / YouTube / Wikipedia
  then YouTube): BERT-Base-Chinese 72.4 / 73.4 / 73.6; multilingual BERT
  69.4 / 72.9 / 73.2; XLM-RoBERTa-Base 72.7 / 73.4 / 74.0 (`:143-153`).
- The best student, 74.0, exceeds its 72B annotator's 73.6 (`:167`).
- Comma recall rises from 48.2–55.0 (Wikipedia) to 71.9–73.9 (YouTube) at
  slightly lower precision (`:143-152`).
- Text cannot separate statement from question when the difference is the
  tone of a final particle (`:175`).

### Meaning for our purpose

- This is the recipe closest to our situation: run the deployed recognizer
  over real speech, have a large LLM punctuate its words-only output, train
  a small tagger. The student equals the annotator on a human-labelled
  spoken test set, so the LLM is needed only offline.
- Running the labelling on the recognizer's own output means training input
  carries the recognizer's vocabulary and errors. For Vietnamese the same
  applies to its uppercase, numbers-spelled-out form.
- Written text alone was already within 0.9 F1 of the annotator for two of
  three encoders; the benefit of LLM-labelled speech is 0.7–3.5 F1 and is
  largest where the written-text model is weakest (multilingual BERT,
  question marks 58.0 → 70.3).
- The student copies the annotator's comma density. Prompt examples should
  encode the comma convention we want, or thresholds should be tuned
  afterwards.
- The tonal-particle limitation is specific to Cantonese writing; Vietnamese
  orthography marks tone, so that particular ambiguity does not carry over.
  (Our inference, not the paper's.)

### What it does not show

- No capitalization (Chinese script) and no number formatting.
- No test on recognizer output: HKCanCor is human transcription.
- No student smaller than a 12-layer base encoder; no speed or memory.
- No check of label quality on the YouTube data itself, and no comparison
  with human-labelled speech of the same size.
- Table 3 has inconsistent cells (F1 71.7 from P 68.7 / R 70.2 at `:145`;
  overall F1 69.4 from P 69.4 / R 67.2 at `:147`) and the prose range for
  comma precision (35.8–46.3, `:97`) does not match Table 1. Differences of a
  few tenths are not reliable; single run, no variance.
- The prompt was not aligned to HKCanCor's punctuation style (`:173`), so
  both LLM and student scores partly measure convention mismatch.

### Leads worth fetching

- Nguyen et al. 2021, *Toward human-friendly ASR systems: recovering
  capitalization and punctuation for Vietnamese text* (IEICE Trans. Inf.
  Syst. 104(8)) — Vietnamese, both tasks.
- Nguyen et al. 2020, *Improving Vietnamese named entity recognition from
  speech using word capitalization and punctuation recovery models*
  (Interspeech) — Vietnamese downstream effect.
- Ling et al. 2024, *A small and fast BERT for Chinese medical punctuation
  restoration* (Interspeech) — small-tagger design.
- Li et al. 2023, *PunCantonese: a benchmark corpus for low-resource
  Cantonese punctuation restoration from speech transcripts* (Interspeech).
- Lai et al. 2023, *Boosting punctuation restoration with data generation
  and reinforcement learning* (Interspeech) — synthetic text as the
  alternative to LLM labelling.
- Hlubík et al. 2020, *Inserting punctuation to ASR output in a real-time
  production environment* (TSD).
