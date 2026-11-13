# End-to-end formatted ASR: training the recogniser to emit punctuation and case

Grounded from fetched full text (2026-11-13). Every number below is quoted
from a local extract and cited as `tag:line`. No figure comes from recall.

**Sources read** (full text; `tag` is the citation prefix used below):

- `M` — Meister et al. (NVIDIA), ASRU 2023, *LibriSpeech-PC: Benchmark for
  Evaluation of Punctuation and Capitalization Capabilities of end-to-end ASR
  Models* — [HTML](https://arxiv.org/html/2310.02943) ·
  [PDF](https://arxiv.org/pdf/2310.02943) ·
  [extract](../related-work/extract/meister2023-librispeech-pc/html/2310.02943.md)
- `K` — Kim, Seo, Lee, Baek (NAVER), 2023, *Improved Training for End-to-End
  Streaming ASR Model with Punctuation* —
  [HTML](https://arxiv.org/html/2306.01296) ·
  [PDF](https://arxiv.org/pdf/2306.01296) ·
  [extract](../related-work/extract/kim2023-e2e-streaming-punct/html/2306.01296.md)
- `Y` — You, Li, Zerhouni (Cisco), 2025, *Enhancing Fully Formatted End-to-End
  Speech Recognition with Knowledge Distillation via Multi-Codebook Vector
  Quantization* — [PDF](https://arxiv.org/pdf/2512.18967) ·
  [arXiv](https://arxiv.org/abs/2512.18967) ·
  [extract](../related-work/extract/you2025-formatted-e2e-distill/you2025-formatted-e2e-distill.md)
- `Ko` — Koluguri et al. (NVIDIA), 2024, *Longer is (Not Necessarily)
  Stronger: Punctuated Long-Sequence Training for Enhanced Speech Recognition
  and Translation* — [HTML](https://arxiv.org/html/2409.05601) ·
  [PDF](https://arxiv.org/pdf/2409.05601) ·
  [extract](../related-work/extract/koluguri2024-punctuated-long-seq/html/2409.05601.md)
- `G` — Gris et al., 2023, *Evaluating OpenAI's Whisper ASR for Punctuation
  Prediction and Topic Modeling of life histories of the Museum of the
  Person* — [HTML](https://arxiv.org/html/2305.14580) ·
  [PDF](https://arxiv.org/pdf/2305.14580) ·
  [extract](../related-work/extract/gris2023-whisper-punct/html/2305.14580.md)

Metric names (PER, WER C, WER PC, zero-WER F1) are defined in
[evaluation-metrics.md](evaluation-metrics.md). The acoustic-versus-text
question for a separate restorer is in
[acoustic-features.md](acoustic-features.md).

## What it is

The recogniser's output vocabulary includes punctuation marks and mixed-case
tokens, and it is trained on audio paired with cased, punctuated transcripts,
so no second model runs after it. The alternative is a cascade: a words-only
recogniser followed by a text model that inserts punctuation and case.

All five sources are English or Portuguese. None is Vietnamese, none starts
from an all-uppercase recogniser, and none handles spelled-out numbers.

## Recipes

| Source | Model | Output units | Training data | What is added to plain training |
|---|---|---|---|---|
| Meister | Conformer-CTC large, 115M, offline; fine-tuned 100,000 steps from a words-only LibriSpeech checkpoint (`M:267`, `M:323`) | SentencePiece unigram, 128 tokens; only `. , ?` kept, each separated from words by a space (`M:251-252`, `M:267`) | LibriSpeech-PC train, about 874 h (449.10 + 333.13 + 91.61, `M:162-164`) | nothing; optional 7-gram token LM over punctuated cased text in beam search (`M:371-379`) |
| You | Zipformer-medium transducer, 65M, offline and streaming variants (`Y:85`, `Y:129`, `Y:149-151`) | SentencePiece unigram, 500 tokens covering upper and lower case plus `, . ?` (`Y:87`) | LibriSpeech-PC, 30 epochs on four V100 (`Y:79`, `Y:87`) | auxiliary loss, weight 0.1, making encoder layer 11 predict 16 codebook indexes of layer 36 of HuBERT-XL fine-tuned on LibriSpeech (`Y:85`, `Y:87`); optional 3×1024 LSTM LM, 25M, on LibriSpeech-PC transcripts by shallow fusion (`Y:91`, `Y:131`) |
| Kim | 12-layer, 256-wide Transformer CTC, about 18M, streaming with 1 s chunks, 2 s left and 1 s right context (`K:232`, `K:240`) | 2000 wordpieces, **lowercase** with `' , . ?` (`K:228`, `K:234`) | MuST-C English (TED), at least 385 h (`K:226`) | pairs of random utterances concatenated in audio and label; second CTC loss on chunk-wise emissions, interpolation 0.5 (`K:71`, `K:108`, `K:234`) |
| Koluguri | FastConformer-XXL, 1.1B, hybrid TDT + CTC (CTC weight 0.3), offline full attention, fine-tuned 25,000 steps (`Ko:213`) | cased, punctuated (vocabulary size not stated for ASR) | 18–31k h of internal plus public data with punctuation and case (`Ko:107`, `Ko:125-128`) | adjacent segments joined into complete sentences; training segments up to 40 s or 60 s (`Ko:85`, `Ko:97`) |
| Whisper (as evaluated by Gris) | Whisper large multilingual, 1550M, offline (`G:213`) | unnormalised text | 680,000 h weakly labelled web audio, about 9,000 h Portuguese (`G:121`) | nothing reported |

Notes on the recipes:

- **The distillation in You et al. is from a speech model, not a text model.**
  The teacher is HuBERT fine-tuned on normalised (words-only) transcripts
  (`Y:85`, `Y:162`). The authors' explanation is that it improves word
  accuracy, and that the transducer's punctuation then benefits because each
  token is conditioned on previously emitted tokens (`Y:162`). None of the six
  extracts distils a text restorer into a recogniser.
- **Intermediate CTC on unpunctuated labels** (Nozaki et al. 2022) is the
  auxiliary loss both Kim and You cite as prior art (`K:244`, `Y:67`). Kim's
  reimplementation in a streaming CTC model made things worse (below).
- **A token LM trained on cased punctuated text** is a cheap add-on for an
  already formatted recogniser; a web-text-only LM hurt punctuation (below).

## Effect on plain WER

Plain WER here means WER after removing punctuation and case from both
sides.

| Claim | Setting | Numbers | Grade |
|---|---|---|---|
| Fine-tuning a words-only recogniser to emit punctuation and case changes plain WER by a few tenths in either direction | LibriSpeech-PC, Conformer-CTC 115M; the cascade's recogniser is the checkpoint the formatted model was fine-tuned from | test-clean 2.60 words-only (`M:303`) → 2.83 formatted (`M:325`); test-other 5.79 (`M:307`) → 5.65 (`M:329`) | single-source; one run each, no variance reported |
| Training on punctuated cased labels does not raise plain WER when everything else is matched | Earnings-21/22 long-form, FastConformer 1.1B, same complete-sentence 0–60 s data, with and without punctuation and case in the labels | 11.63 vs 11.71 (Earnings-21), 14.15 vs 14.69 (Earnings-22), formatted model lower (`Ko:265-266`) | single-source; the cleanest matched comparison in this set |
| Complete-sentence formatted training roughly ties a strong words-only model on short lowercase benchmarks | nine Open ASR Leaderboard sets, Whisper normalisation, greedy TDT | average 6.95 for the reference row vs 6.82 (0–20 s), 6.73 (0–40 s), 6.81 (0–60 s) (`Ko:198-201`); per-set movement is mixed: LibriSpeech clean 1.62 → 1.74, TED-LIUM 3.42 → 3.90, Common Voice 8.68 → 7.71 (`Ko:198-199`) | single-source; the reference row is footnoted as the published `parakeet_tdt_1.1b` (`Ko:205`), so the rows may differ in more than label format |
| With an LM over formatted text, the formatted recogniser's plain WER falls below the words-only greedy number | LibriSpeech-PC, 7-gram token LM | 2.22 / 4.67 with the LibriSpeech-PC + Common Crawl LM (`M:358`, `M:362`) against 2.60 / 5.79 words-only greedy | single-source; not matched, since the words-only model gets no LM |

The table in Meister lists the tuned cascade's plain WER as 2.86 / 6.26
(`M:314`, `M:318`) against 2.60 / 5.79 for the base cascade, although the
text describes the two as differing only in the text model (`M:263`). The
extract does not explain the difference.

No source in this set measures the plain-WER effect for a small streaming
transducer: You et al. report formatted models only, with no words-only
Zipformer row (`Y:126-131`, `Y:147-151`), and Kim et al. have no words-only
baseline either (`K:173-216`).

## Punctuation and case quality against a cascade

| Claim | Setting | Numbers | Grade |
|---|---|---|---|
| A formatted recogniser beats words-only ASR plus an in-domain fine-tuned BERT tagger | LibriSpeech-PC test-clean / test-other; cascade = Conformer-CTC 115M + BERT 109M with punctuation and case heads, the tagger fine-tuned 3 epochs on in-domain text (`M:261-263`) | PER 36.60 / 37.42 cascade (`M:313`, `M:317`) vs 29.48 / 27.37 formatted (`M:324`, `M:328`); WER PC 9.45 / 12.90 (`M:316`, `M:320`) vs 8.11 / 10.48 (`M:327`, `M:331`); WER C 5.09 / 8.66 (`M:315`, `M:319`) vs 4.72 / 7.57 (`M:326-330`) | single-source; `Y` reuses these numbers rather than rerunning the cascade |
| The same holds on utterances both systems recognise perfectly, where the gap is mostly punctuation | zero-WER utterances, each system's own subset | punctuation F1 84.75 vs 87.40 test-clean, 83.40 vs 88.27 test-other; capitalisation F1 94.47 vs 94.85 and 94.53 vs 95.50 (`M:196-242`) | single-source; subsets differ per system (`M:391`) |
| An out-of-domain text tagger is far worse than either | same benchmark, same tagger before fine-tuning | WER PC 26.36 / 29.96 (`M:305`, `M:309`) against 9.45 / 12.90 after 3 epochs of in-domain tuning; PER moves only 38.38 → 36.60 (`M:302`, `M:313`) | single-source |
| On long-form business speech a formatted recogniser beats a cascade with an off-the-shelf tagger | Earnings-21 / Earnings-22, about 17-minute segments (`Ko:152-153`); cascade = matched words-only FastConformer 1.1B + NeMo BERT tagger trained on LibriSpeech and Fisher text (`Ko:272`) | punctuated cased WER 23.44 vs 18.86 and 26.71 vs 22.40; case-only 19.60 vs 17.09 and 22.76 vs 20.54; punctuation-only 16.20 vs 13.65 and 18.81 vs 16.38 (`Ko:315-324`, `Ko:342-351`) | single-source; the tagger was not adapted to the domain, which by the Meister row above is a large handicap |
| A 65M transducer reaches the same punctuation quality as the 115M CTC model | LibriSpeech-PC, Zipformer with distillation, no LM | PER 29.74 / 28.18, WER PC 7.58 / 10.21, plain WER 2.20 / 5.23 (`Y:129`) against 29.48 / 27.37, 8.11 / 10.48, 2.83 / 5.65 (`Y:127`) | benchmark-reported (two groups on one public test set; neither result independently rerun) |
| Streaming costs words, not punctuation | LibriSpeech-PC, Zipformer without distillation, offline vs streaming | PER 30.23 → 30.01 and 29.51 → 29.05; plain WER 2.42 → 3.13 and 5.55 → 7.85 (`Y:147`, `Y:150`) | single-source; the streaming latency configuration is not stated in the extract |
| Whisper-large is no better at punctuation than a small specialised model | LibriSpeech-PC | Whisper-large 1550M: PER 30.52 / 30.55, WER PC 8.60 / 11.29 (`Y:128`); Whisper-base 74M: PER 36.97 / 40.27 (`M:291`, `M:295`) | benchmark-reported |

Size of the auxiliary gains in You et al.: distillation changes PER from 30.23
to 29.74 and 29.51 to 28.18 offline, and 30.01 to 28.74 and 29.05 to 28.81
streaming, for 12 extra GPU hours on 152 or 188 (`Y:147-151`, `Y:164`). The
loss weight barely matters: WER PC 7.62, 7.58, 7.67 for 0.05, 0.1, 0.2
(`Y:158-160`). The LSTM LM moves PER from 29.74 to 27.24 and 28.18 to 26.55
(`Y:129`, `Y:131`), a larger step than distillation.

Absolute level, per mark, for the formatted Conformer on test-clean (the
table does not name the model; it follows the formatted-model results):
period PER 24.01%, comma 33.26%, question mark 15.99%; commas are mostly
inserted (18.23%) or deleted (13.53%), and 9.93% of periods come out as commas
(`M:417-426`).

## Long-sequence and complete-sentence training

| Claim | Setting | Numbers | Grade |
|---|---|---|---|
| Training on segments that are complete sentences, instead of fragments that start or stop mid-sentence, is the largest single lever on formatted quality | FastConformer 1.1B, equal total duration, 0–20 s segments, Earnings-21 / Earnings-22 | punctuated cased WER 24.86 → 19.96 and 30.19 → 23.58; plain WER 12.44 → 12.12 and 15.60 → 14.72 (`Ko:239-240`, `Ko:244-245`) | single-source |
| Extending segments to 40 s adds a little; 60 s adds nothing | same | 19.96 → 18.98 → 18.86 and 23.58 → 22.62 → 22.40 punctuated cased; plain WER 12.12 → 11.61 → 11.63 (`Ko:240-242`, `Ko:245-247`) | single-source |
| For a streaming CTC model, concatenating two unrelated utterances in training raises sentence-final punctuation recall on long audio | MuST-C tst-COMMON whole talks (11 minutes average, `K:238`), 18M model | period F1 41.0 without concatenation vs 46.6 with; average F1 over `, . ?` 41.7 vs 45.1; plain WER 16.0 vs 15.8 (`K:313-332`) | single-source |
| Concatenation alone breaks word accuracy; the chunk-wise loss is what makes it safe | same, concatenation without the chunk loss | plain WER 21.3 against 15.8; period F1 52.9, question F1 25.8 (`K:320-325`) | single-source |
| Intermediate CTC on unpunctuated labels does not help a streaming model | same, Kim's reimplementation of Nozaki et al. | average F1 36.1 against 40.0 baseline on whole talks, 28.7 against 34.4 on segments; plain WER 18.5 against 18.2 (`K:173-201`, `K:272-284`) | failed-replication in the streaming regime (one reimplementation); Nozaki's own offline figures, 61.1 / 92.5 / 74.1 F1 for comma / period / question, are quoted second-hand at `G:73` |

The reason both papers give is the same: in segmented corpora sentence-final
marks sit at the end of the training target, so a model learns "end of input
means period" and has no evidence for a period in the middle of a stream
(`K:71`, `Ko:85`).

## Data requirements

- **Audio with cased, punctuated transcripts is required, and both NVIDIA
  papers name its scarcity as the main obstacle** (`M:22`, `Ko:22`,
  `Ko:107`). Most public corpora ship already normalised.
- **Recovering formatting for an existing corpus is possible when the source
  text exists.** LibriSpeech-PC was made by aligning transcripts to the
  original books, keeping over 90% of each split (`M:143`, `M:160-168`).
  Dropped: non-standard Unicode, more than two words of mismatch, clips under
  one second, all-uppercase samples (`M:147-150`).
- **Amounts actually used:** about 874 h (Meister, You), at least 385 h (Kim),
  18,000–31,000 h (Koluguri). No source trains a formatted recogniser on less
  than 385 h, and none studies the amount as a variable.
- **Only three marks are learned.** Meister and You drop everything but
  `. , ?` "due to their limited presence" (`M:251`, `Y:81`); Kim keeps the
  same three plus the apostrophe and lowercases everything (`K:228`).
- **Whisper is the weak-supervision route:** unnormalised web transcripts at
  680,000 h (`G:121`), with the per-mark results below.

## Failure modes

- **Sentence-final marks collapse in streaming on unsegmented audio.** Kim's
  baseline recalls 23.6% of periods and 25.1% of question marks on whole
  talks; the proposed training reaches 33.6% and 29.4% (`K:173-216`). Best
  period F1 is 46.6 on whole talks and 27.3 on 5.8-second segments
  (`K:203-216`, `K:286-291`).
- **Commas are the worst of the three common marks** for a formatted
  recogniser on read speech: 33.26% PER against 24.01% for periods
  (`M:426`).
- **Rare marks are not learned even from 680,000 h.** Whisper-large on
  Portuguese interviews: exclamation F1 5.1, ellipsis 17.4, and it emitted no
  semicolon or colon at all against 83 and 651 in the reference (`G:394-408`,
  `G:496-503`).
- **Over-segmentation.** Whisper produced 26.6% more sentences than the human
  transcript (11,062 against 8,740) and 3,146 more commas (`G:227`,
  `G:256-259`, `G:283-286`, `G:308`).
- **Punctuation depends on the audio segmentation fed to the model.**
  Diarising first changed 12 marks in one short excerpt, including turning a
  question into a statement (`G:428-433`).
- **An LM built only from web text hurts punctuation while helping words:**
  PER 29.48 → 32.40 and 27.37 → 31.78 with the Common Crawl 7-gram, although
  plain WER improves 2.83 → 2.24 (`M:324-331`, `M:346-351`).
- **Training cost and memory.** Kim's method doubles sequence length and adds
  chunk-wise forward passes (`K:342`); Koluguri fits batch size 2 at 60 s
  and 8 at 40 s on an 80 GB GPU for the 1.1B model (`Ko:219`).

## What this does not show

- **Nothing for Vietnamese, tonal languages, or uppercase-only output.**
  Whether case and punctuation tokens cost a small Vietnamese transducer
  word accuracy is unmeasured here.
- **No formatted-versus-words-only comparison for a small streaming
  transducer.** The two matched comparisons are a 115M offline CTC model
  (one run) and a 1.1B offline model.
- **No cascade with a strong, domain-matched, large-data text model.** The
  cascades are one BERT-base tagger: fine-tuned for 3 epochs in Meister (the
  extract does not name the tuning text, `M:263`; LibriSpeech-PC transcripts
  are the evident candidate and are called "in-domain" on this page on that
  reading), and unadapted in Koluguri. No cascade here uses a
  text model trained on large in-domain written text, a larger encoder, or
  ASR-error augmentation, so "formatted ASR beats a cascade" is established
  only against that tagger.
- **No low-resource result.** The smallest formatted training set is 385 h of
  clean TED speech with professional transcripts.
- **No number formatting.** Koluguri converts reference numerals to words
  before scoring (`Ko:138`); nobody evaluates digits, dates or currency.
- **No latency or on-device measurements** for formatted output in any
  source, and no seeds or confidence intervals anywhere.
- **LibriSpeech-PC is read literary text**; Koluguri argues its truncated
  segments are unlike conversational speech (`Ko:134`).

## Per-paper reading notes

[meister2023-librispeech-pc](../related-work/readings/meister2023-librispeech-pc.md) ·
[kim2023-e2e-streaming-punct](../related-work/readings/kim2023-e2e-streaming-punct.md) ·
[you2025-formatted-e2e-distill](../related-work/readings/you2025-formatted-e2e-distill.md) ·
[koluguri2024-punctuated-long-seq](../related-work/readings/koluguri2024-punctuated-long-seq.md) ·
[gris2023-whisper-punct](../related-work/readings/gris2023-whisper-punct.md) ·
[zhu2022-unipunc](../related-work/readings/zhu2022-unipunc.md)
