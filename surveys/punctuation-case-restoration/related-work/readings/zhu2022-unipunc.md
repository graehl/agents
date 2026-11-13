**Source:** *Unified Multimodal Punctuation Restoration Framework for Mixed-Modality Corpus* — [PDF](https://arxiv.org/pdf/2202.00468) · [arXiv](https://arxiv.org/abs/2202.00468)

## 2026-11-13 — fable-5.2, full text

Purpose: choosing form, size and data for a Vietnamese case+punctuation
restorer for words-only phone ASR output. Line citations are to
`extract/zhu2022-unipunc/html/2202.00468.md`.

### Claims

- **Setup.** Punctuation as per-word tagging with comma, full stop,
  question mark, none (`:36`). BERT-base uncased text encoder plus wav2vec
  2.0 base audio encoder, convolutional downsampling, two cross-attention
  fusion layers; a learned 5-vector "virtual embedding" stands in when a
  sample has no audio (`:56-60`, `:334`). Data: MuST-C English (99,381
  samples with audio) plus text-only sentences from mTEDx (142,441 total),
  10–30 s samples, reference transcripts (`:106-119`, `:330`).
- **Audio test set, F1 comma / full stop / question / overall.** Text-only
  BERT 72.1 / 82.8 / 75.5 / 77.1; MuSe 73.2 / 83.6 / 79.4 / 77.9;
  UniPunc trained on audio samples 74.2 / 83.7 / 80.8 / 78.5; UniPunc
  trained on audio plus text-only samples 74.5 / 83.8 / 80.4 / 78.6
  (`:181-249`).
- **Mixed test set (most sentences without audio).** BERT 70.8 / 81.8 /
  77.4 / 75.7; UniPunc 72.1 / 82.2 / 76.1 / 76.5 (`:298-324`).
- **Non-pretrained baselines on the audio test set.** LSTM with timing
  features 65.1 overall; attention with word and speech embeddings 69.7
  (`:153-179`).
- **TTS audio for text-only samples** (MuSe+TTS): 77.8 overall, full stop
  78.8 (`:209-221`).
- **Grafting.** BiLSTM 53.7 → 56.6 overall but question 50.1 → 46.5;
  content-dropout BERT 76.1 → 76.9, question 69.7 → 76.7 (`:358-361`).

### Meaning for our purpose

- Against a fine-tuned BERT-base, hearing the audio is worth about 1.5
  overall F1 on clean reference text, almost all of it on question marks
  (+5); full stops gain 1 point. This supports "acoustic features add
  little over a pretrained text model" for commas and full stops, and
  contradicts it for question marks.
- The price is a second pretrained encoder of BERT-base size at inference,
  which is not plausible on a phone next to the recogniser. The relevant
  cheap variants (pause durations from recogniser timestamps, or reusing
  the recogniser's encoder states) are not tested here.
- A pretrained text encoder matters far more than audio: BERT is 7–12
  points above the non-pretrained multimodal baselines.
- Text-only data in training barely moved the multimodal model (78.5 →
  78.6).

### What it does not show

- Scored on reference transcripts, not recogniser output; no word errors.
- Text baseline is BERT-base only; one run each; differences of 0.1–1.5 F1
  without variance. The stated margin is 0.8 in the abstract and 0.7 in the
  results (`:9`, `:348`).
- No ablation of pause vs pitch vs learned features; no parameter count,
  latency or memory.
- English TED talks only (prepared speech); a multilingual case study is
  mentioned without numbers (`:365`). No tonal language. No case.
- Test-set statistics in Table 1 are inconsistent (490 sentences, 120,940
  audio, `:118`).

### Leads worth fetching

- Sunkara et al., Interspeech 2020, MuSe (`:389`): the original with/without
  audio comparison over BERT on conversational speech.
- Soboleva et al., ICASSP 2021, *Replacing human audio with synthetic audio
  for on-device unspoken punctuation prediction* (`:397`): on-device
  punctuation with acoustic input and TTS-generated training audio.
- Silva, Theobald, Apostoloff, ICASSP 2021, *Multimodal punctuation
  prediction with contextual dropout* (`:390`).
- Courtland, Faulkner, McElvain, IWSLT 2020, *Efficient automatic
  punctuation restoration using bidirectional transformers with robust
  inference* (`:384`): efficient text-only restorer.
- Klejch, Bell, Renals, ICASSP 2017, *Sequence-to-sequence models for
  punctuated transcription combining lexical and acoustic features*
  (`:387`).
- Tündik et al., Interspeech 2018, *User-centric evaluation of automatic
  punctuation in ASR closed captioning* (`:379`): human readability
  evaluation, missing from the metrics page.
