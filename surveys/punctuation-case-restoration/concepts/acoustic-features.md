# What audio adds over text-only punctuation restoration

Grounded from fetched full text (2026-11-13). Every number below is quoted
from a local extract and cited as `tag:line`. No figure comes from recall.

**Sources read** (full text; `tag` is the citation prefix used below):

- `Z` — Zhu, Wu, Cheng, Wang (ByteDance), 2022, *Unified Multimodal
  Punctuation Restoration Framework for Mixed-Modality Corpus* (UniPunc) —
  [HTML](https://arxiv.org/html/2202.00468) ·
  [PDF](https://arxiv.org/pdf/2202.00468) ·
  [extract](../related-work/extract/zhu2022-unipunc/html/2202.00468.md)
- `G` — Gris et al., 2023, *Evaluating OpenAI's Whisper ASR for Punctuation
  Prediction and Topic Modeling of life histories of the Museum of the
  Person* — [HTML](https://arxiv.org/html/2305.14580) ·
  [PDF](https://arxiv.org/pdf/2305.14580) ·
  [extract](../related-work/extract/gris2023-whisper-punct/html/2305.14580.md).
  Used here for its related-work section, which quotes four multimodal and
  text-only papers that were not themselves read.
- `M` — Meister et al., ASRU 2023, *LibriSpeech-PC* —
  [HTML](https://arxiv.org/html/2310.02943) ·
  [PDF](https://arxiv.org/pdf/2310.02943) ·
  [extract](../related-work/extract/meister2023-librispeech-pc/html/2310.02943.md)
- `Ko` — Koluguri et al., 2024, *Longer is (Not Necessarily) Stronger* —
  [HTML](https://arxiv.org/html/2409.05601) ·
  [PDF](https://arxiv.org/pdf/2409.05601) ·
  [extract](../related-work/extract/koluguri2024-punctuated-long-seq/html/2409.05601.md)
- `K` — Kim et al., 2023, *Improved Training for End-to-End Streaming ASR
  Model with Punctuation* — [HTML](https://arxiv.org/html/2306.01296) ·
  [PDF](https://arxiv.org/pdf/2306.01296) ·
  [extract](../related-work/extract/kim2023-e2e-streaming-punct/html/2306.01296.md)
- `Y` — You et al., 2025, *Enhancing Fully Formatted End-to-End Speech
  Recognition with Knowledge Distillation via Multi-Codebook Vector
  Quantization* — [PDF](https://arxiv.org/pdf/2512.18967) ·
  [extract](../related-work/extract/you2025-formatted-e2e-distill/you2025-formatted-e2e-distill.md)

Only one of the six extracts (UniPunc) is a direct with-audio versus
without-audio experiment on a text restorer. The rest is second-hand or
indirect, and is labelled as such.

## What is being claimed

Pauses and intonation carry information the words do not: a comma that
changes meaning ("I don't want anymore kids" against "I don't want anymore,
kids"), and whether an utterance is a statement or a question (`Z:22-24`).
A multimodal restorer takes the words plus the audio, encodes each with a
pretrained model, and fuses them before a per-word tag classifier. The
alternative is a restorer that sees only words.

## Direct evidence: UniPunc on MuST-C

Setup: English TED talks, reference transcripts (not recogniser output),
re-partitioned to 10–30 s samples (`Z:106-108`, `Z:330`). Three marks plus
"none" (`Z:36`). Text baseline: BERT-base uncased, fine-tuned, which is a
pretrained encoder and the strongest text-only system in the paper
(`Z:334`, `Z:350`). Audio side: wav2vec 2.0 base, a two-layer convolutional
downsampler, and two cross-attention fusion layers (`Z:334`). 99,381 training
samples have audio; 43,060 more are text only (`Z:116-117`).

F1 on the audio test set, text-only BERT against models that also hear the
audio (`Z:181-249`):

| Model | Comma | Full stop | Question | Overall |
|---|---|---|---|---|
| BERT, text only, trained on all text | 72.1 | 82.8 | 75.5 | 77.1 |
| MuSe (earlier multimodal, wav2vec 2.0) | 73.2 | 83.6 | 79.4 | 77.9 |
| UniPunc, audio samples only | 74.2 | 83.7 | 80.8 | 78.5 |
| UniPunc, audio plus text-only samples | 74.5 | 83.8 | 80.4 | 78.6 |

| Claim | Baseline, benchmark, regime | Numbers | Grade |
|---|---|---|---|
| Audio adds about 1.5 overall F1 over a fine-tuned BERT-base | MuST-C English, reference words, 99k audio training samples | 77.1 → 78.5 or 78.6 (`Z:193`, `Z:235`, `Z:249`) | single-source; no seeds or significance test |
| The gain is concentrated in question marks | same | question +5.3 or +4.9 (75.5 → 80.8 / 80.4); comma +2.1 or +2.4; full stop +0.9 or +1.0 (`Z:184-190`, `Z:226-232`, `Z:240-246`) | single-source; differences are our subtraction |
| An earlier multimodal model gets about half of that | same | MuSe overall 77.9, +0.8 over BERT; question +3.9 (`Z:198-207`) | single-source (Zhu's reimplementation of MuSe with wav2vec 2.0, `Z:334`) |
| The audio gain changes the precision / recall balance more than the total | same | BERT overall P 81.5, R 73.5; UniPunc-audio P 80.3, R 76.8 (`Z:191-192`, `Z:233-234`) | single-source |
| Without a pretrained text encoder, multimodal models are far behind text-only BERT | same test set | attention model with word and speech embeddings 69.7 overall, LSTM with time features 65.1, against BERT 77.1 (`Z:164`, `Z:179`, `Z:193`) | single-source |
| Synthetic audio for text-only samples does not help overall | MuSe plus TTS audio | overall 77.8 against 77.9; comma 77.1 against 73.2 but full stop 78.8 against 83.6 (`Z:198-221`) | single-source |

## Negative and null results

- **On a test set where most sentences have no audio, the model that can use
  audio is worse than BERT on question marks:** 76.1 against 77.4, with
  overall 76.5 against 75.7 (`Z:298-324`). The benefit exists only when the
  audio is present at inference.
- **Grafting the audio path onto a BiLSTM lowers question-mark F1** from 50.1
  to 46.5 while raising overall from 53.7 to 56.6 (`Z:358-359`).
- **Adding text-only training data to the multimodal model is a wash:**
  78.5 → 78.6 overall, question 80.8 → 80.4 (`Z:226-249`).
- **A text-only pretrained model beats a multimodal model without
  pretraining across papers.** On IWSLT 2011 ASR transcripts, a
  RoBERTa-large tagger with error augmentation scores 74 overall F1 (Alam et
  al. 2020) against 68.8 for a self-attention model with GloVe and
  Speech2Vec embeddings (Yi and Tao 2019); the multimodal model is ahead only
  on question marks, 69.1 against 63.4 (`G:59`, `G:65`). Second-hand,
  different papers, same test set as described by Gris et al.
- **Whisper, which hears the audio, still fails on the mark usually tied to
  prosody.** Exclamation F1 5.1 with recall 3.0 on Portuguese interviews
  (`G:499`), and question-mark F1 68.0 (`G:500`). This is one model on one
  corpus with a human reference of different sentence style (`G:227`), not a
  controlled test of prosody.

## Second-hand and indirect evidence

| Claim | Source of the claim | Numbers available in our extracts | Grade |
|---|---|---|---|
| Any of pitch, mel spectrogram or wav2vec features improves all three marks over a truncated pretrained BERT; wav2vec is the best | Sunkara et al. 2020 (MuSe), Fisher conversational English, 348 h audio, as summarised at `G:71` | best per-mark F1 75.6 / 75.6 / 81.3 for comma / full stop / question (`G:71`, `G:97`); the text-only baseline figures are **not** in the extract | single-source, second-hand |
| Word timing features help a BiLSTM or CNN tagger | Zelasko et al. 2018, Fisher, as summarised at `G:69` | best with timing: comma 66.1, period 67.3, question 59.2; the without-timing figures are not in the extract; the baseline has GloVe embeddings, no pretrained encoder | single-source, second-hand |
| A recogniser trained to emit punctuation beats a text cascade "because" it has the audio | Koluguri et al. state the causal reading (`Ko:272`); Meister et al. report the same direction without it | Earnings-21 punctuation-only WER 16.20 cascade vs 13.65 end-to-end (`Ko:315-324`); LibriSpeech-PC PER 36.60 vs 29.48 (`M:313`, `M:324`) | single-source each; confounded: the two systems also differ in training data and domain match of the text model, so the gap is not an estimate of the acoustic contribution |
| Prosody distinguishes statements from questions | stated as motivation at `Y:19`, `Ko:22`, `Z:22` | none | folklore within these extracts (asserted, not measured, except by the UniPunc question-mark row above) |

Kim et al. show what the audio alone can do without a language model or a
pretrained text encoder, in streaming: an 18M CTC recogniser reaches comma
F1 50.8, period 46.6, question 37.9 on whole MuST-C talks (`K:203-216`),
against full stop 82.8 for text-only BERT on MuST-C reference text
(`Z:187`). The two are different test partitions and one is on recogniser
output, so this is an order-of-magnitude contrast, not a comparison.

## Cost

- **A second pretrained encoder at inference.** UniPunc runs wav2vec 2.0
  base alongside BERT-base, both at width 768 (`Z:334`). Parameter counts,
  latency and memory are not reported.
- **Paired data.** Audio aligned to punctuated transcripts is the scarce
  resource; UniPunc's design goal is to keep using text-only data alongside
  it (`Z:26-28`).
- **Audio must be available wherever the restorer runs.** The paper's own
  motivation is that it often is not (`Z:26`).
- **Training-time only costs** when the audio enters through the recogniser
  itself: no inference overhead for distillation (`Y:73`) or for Kim's extra
  loss (`K:342`).

## What this does not show

- **No measurement on recogniser output.** UniPunc is scored on reference
  words. Whether a 1.5-point gain survives word errors, or grows because the
  audio compensates for them, is not tested.
- **No baseline stronger than BERT-base.** No larger encoder, no
  domain-adapted text model, no text model trained on large written corpora
  with error augmentation in the same experiment.
- **No ablation of which acoustic cue helps.** Pause duration, pitch and
  learned wav2vec features are never separated in the direct evidence; the
  pitch-versus-wav2vec comparison exists only second-hand without baseline
  numbers.
- **No cheap-feature variant.** Nothing tests giving a text model only the
  inter-word gaps that a recogniser's timestamps already provide, which is
  the form relevant to a phone pipeline.
- **English TED talks and English telephone speech only.** Nothing on a
  tonal language, where lexical tone occupies the pitch channel that English
  uses for question intonation. UniPunc mentions a multilingual case study
  with no numbers in the paper (`Z:365`).
- **No case restoration.** Every acoustic result here is punctuation only.
- **One run per configuration**, with gains of 0.1 to 1.5 F1 reported
  without variance.

## Per-paper reading notes

[zhu2022-unipunc](../related-work/readings/zhu2022-unipunc.md) ·
[gris2023-whisper-punct](../related-work/readings/gris2023-whisper-punct.md) ·
[meister2023-librispeech-pc](../related-work/readings/meister2023-librispeech-pc.md) ·
[koluguri2024-punctuated-long-seq](../related-work/readings/koluguri2024-punctuated-long-seq.md) ·
[kim2023-e2e-streaming-punct](../related-work/readings/kim2023-e2e-streaming-punct.md) ·
[you2025-formatted-e2e-distill](../related-work/readings/you2025-formatted-e2e-distill.md)
