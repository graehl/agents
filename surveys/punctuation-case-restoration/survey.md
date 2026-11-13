# Restoring punctuation and case to words-only speech recognition output

**Grounding:** grounded. 24 manifested papers: 22 with committed full-text
extracts, each read by a delegated reader (fable-5.2) who wrote a
[reading note](related-work/readings/) and the concept pages; 2 Vietnamese
papers read only as a web page or abstract and marked so below. The
[manifest](related-work/papers.yaml) marks each entry. Numbers in this map
were taken from the reading notes; three headline tables were rechecked
against the extracts by the synthesizing session.
**Coverage cutoff:** 2026-11-13. **Search scope:** arXiv (cs.CL, eess.AS),
ACL Anthology and ISCA proceedings through web search; Semantic Scholar
forward citations and OpenAlex title search for snowballing; the arXiv API
and ACL Anthology BibTeX for citation checks. Query terms: punctuation
restoration, capitalization or truecasing restoration, punctuation
prediction for ASR, Vietnamese punctuation, on-device or lightweight
punctuation, LLM punctuation restoration, end-to-end ASR with punctuation.
**Anchors:** Păiș and Tufiș 2021 (survey), Uyen 2022 (Vietnamese joint
model), You and Li 2024 (compact on-device model), Meister 2023
(LibriSpeech-PC), Behre 2022 (streaming).
**Saturation:** not reached. Each reader returned 10 or more cited, unread
papers ([leads](#unread-leads)).

Question (graehl, 2026-11-13): what form and size should a Vietnamese
punctuation and case restoring model take, for a recogniser whose output
is words only?

Setting the answers are judged against (speech-recognition program, draft
repository `research/speech-recognition/vi/`): `gipformer1.5-68M-rnnt`, a
68M Zipformer transducer run in sherpa-onnx on a phone. Its 2,000-piece
vocabulary is all uppercase with no punctuation and no digits, so it
writes `VĂN HÓA VÀ BỘ LẠC CỔ XƯA ...` and spells numbers out. Clips are
single utterances of a few seconds to tens of seconds. Raw Vietnamese
Wikipedia and FineWeb-2 text (5.7 GB) is on hand; FLEURS references are
cased and punctuated.

## Summary

| Question | Answer from the sources | Grade |
|---|---|---|
| Form | A per-word tagger with two heads, case and following mark, over the recogniser's words. It cannot change a word. A plain linear head is enough. | reproduced across languages for the form; single-source for Vietnamese joint heads |
| Ceiling size | A base-size pretrained encoder (about 110–280M). Large over base is worth +2.1 F1 in one paper and −0.4 in another. | contested |
| Phone size | A 7 MB CNN-BiLSTM runs in sherpa-onnx today, but trails RoBERTa-base on the same English test by 13–15 comma F1 and 7–8 period F1. A 10M distilled encoder kept 95% of its teacher's F1 in Chinese. | single-source each; the cross-paper gap is our comparison |
| Hard classes | Commas everywhere. Periods are also lost by small models. Much comma "error" is valid alternative punctuation. | reproduced |
| Training text | Written text alone transfers poorly to speech: news-trained Bangla comma F1 fell 81 → 38 on speech transcripts. Punctuating real recogniser transcripts with an LLM and training a tagger on them beat three times as much Wikipedia. | single-source each |
| LLM as restorer | Prompted LLMs lose to taggers and change words in 16–25% of utterances. Fine-tuned 2B LLMs beat an off-the-shelf tagger but still change 1–3%. | single-source, confounded |
| Pauses and prosody | +1.4 to +1.5 overall F1 over BERT-base, mostly question marks. | single-source |
| Not post-processing at all | On English, a recogniser trained to write case and punctuation beat a words-only recogniser plus tuned BERT tagger, at no cost in word errors, including at 65M Zipformer size. A Vietnamese 68M transducer was trained this way on about 1,000 h. | benchmark-reported (English); abstract only (Vietnamese) |

## The tagger formulation

Detail: [tagger formulation](concepts/tagger-formulation.md).

Input is the lowercased, unpunctuated word sequence. Each word's first
subword carries two labels: a case class and the mark that follows it.
The compact English model uses comma, period, question or none, and
all-upper, capitalised, mixed or lower (You 2024). ViCapPunc uses
capitalised and all-capitals with comma, period and question (Uyen 2022).
The nearest alternatives are a sequence-to-sequence rewriter, which can
change words, and a recogniser that writes the marks itself
([below](#the-recogniser-writes-case-and-punctuation-itself)).

- **Joint heads beat separate models** on Vietnamese medical question
  text with a vELECTRA encoder: case F1 86.75 against 83.53, punctuation
  80.10 against 78.65. `single-source`, single runs (Uyen 2022).
- **A plain linear head is enough.** It matched or beat BiLSTM-CRF in 7
  of 8 matched Vietnamese pairs (PhoPunct), and a CRF added nothing on
  English (82.4 against 82.4, Alam 2020). Uyen 2022 reports +1.39 from a
  CRF, so this is `contested` for Vietnamese.
- **The pretrained encoder carries the result.** Replacing it with
  FastText embeddings dropped Vietnamese case F1 to 60.73 and punctuation
  to 49.47 (Uyen 2022). On English speech, BERT was 7–12 F1 above models
  without pretrained encoders, audio included (Zhu 2022).
- **Overlapped windows help long input.** Summing predictions over 9
  overlapping windows raised English F1 76.3 → 83.9 at 7.7× the CPU cost
  (Courtland 2020). Merging overlapped chunks raised comma 0.41 → 0.56 in
  a sequence-to-sequence model (Nguyen 2019). Both are `single-source`.
- **Right context matters and left context does not.** Adding the next
  segment raised sentence-boundary F0.5 from 67 to 78; adding the previous
  one gave +0.4% (Behre 2023). A causal scorer went from macro F1 0.646
  with no lookahead to 0.927 with one token (Woo 2026). For single clips
  this means tagging once the clip is complete.
  Detail: [segmentation and streaming](concepts/segmentation-and-streaming.md).

## Vietnamese

Detail: [Vietnamese](concepts/vietnamese.md).

- **No Vietnamese paper read here evaluates on recogniser output.** Both
  test on clean written text.
- **Data.** ViCapPunc is the only case-labelled set: 425,350 medical
  question-and-answer sentences (Uyen 2022). The News and Novels corpus
  (Pham 2020, as cited) has 22.1M tokens with 7 punctuation labels and no
  case.
- **Scores.** On News and Novels, macro F1 over six marks is 61.35 /
  48.97 for PhoBERT-large with BiLSTM-CRF and 58.62 / 50.18 for XLM-R
  base with CRF (PhoPunct, single runs). Macro F1 there is depressed by
  rare marks: the Novels test set has 6 semicolons. No per-class numbers
  are in the text.
- **PhoASR (Vu 2026, read as a web page only).** Qualcomm punctuated and
  cased a 500 h Vietnamese speech set with a fine-tuned BARTpho-syllable
  base rewriter trained on 5M news samples, keeping only `, . ! ?`, and
  discarded outputs whose words changed. It reports no accuracy for that
  restorer. Its cased, punctuated word error rate shows how much format
  matters: PhoWhisper-small scores 33.90% against 8.97% normalised.
- **A formatted 68M Vietnamese transducer exists (Huyen 2026, abstract
  only).** It adds punctuation and case to the vocabulary of a VietASR
  68M model and fine-tunes on about 1,000 h of formatted speech, reporting
  6.41% WER on VIVOS and punctuation micro-F1 0.94. No cascade comparison
  and no capitalisation score are in the abstract.

## Compact models

Detail: [compact models](concepts/compact-models.md).

- **CNN-BiLSTM, 7 MB as ONNX (You 2024).** This is the model sherpa-onnx
  runs for English online punctuation and casing. On IWSLT 2011: comma F1
  61.5 (recall 54.0), period 79.5, overall 71.0; capitalised-word F1 84.9.
  It takes 10 ms against 25 ms for a 280 MB CT-Transformer on a laptop
  CPU. Its training code is public (Apache-2.0).
- **Baseline sensitivity.** That paper compares against no BERT-class
  tagger and no Transformer case baseline, and trains on 55M words where
  its baselines used the 2.1M-word IWSLT set. Against RoBERTa-base on the
  same test set (Alam 2020, Courtland 2020) it is 12.8–14.7 comma F1 and
  6.7–8.2 period F1 behind. That gap is our cross-paper comparison.
- **Distillation.** A 10.3M student kept 85.74 of its teacher's 90.68
  overall F1 on Chinese medical text: comma −4.96, period −4.17. A 10.5M
  ALBERT scored 87.54, above both distilled students (Ling 2023).
  `single-source`.
- **Unmeasured:** case quality of a small model against a large one, and
  any Vietnamese compact model.

## Written text is not speech

Detail: [spoken versus written](concepts/spoken-vs-written.md).

- **Register costs more than recognition errors.** A Bangla tagger trained
  on news scored F1 87.0 on news, 68.8 on manual speech transcripts and
  63.2 on recogniser output; comma went 81.2 → 38.1 → 36.9 (Alam 2020).
- **Recognition errors still cost.** English RoBERTa-large fell 82.4 →
  71.3 on recogniser output, and token-noise augmentation recovered 74.0
  (Alam 2020). At 12.7% word error rate, Latvian systems lost 2–4
  punctuation F1 and 5–7 capitalisation F1 (Znotins 2025).
- **Scripted to spontaneous** English costs 2.3–4.0 overall F1, mostly
  commas (Liu 2024).
- **Punctuating real transcripts with an LLM and training a tagger on
  them** gave an XLM-R base student 74.0 F1 against its Qwen-72B
  annotator's 73.6 on human-labelled spoken Cantonese. It beat three
  times as much Wikipedia by 0.7–3.5 F1, with comma recall rising from
  48–55 to 72–74. Wikipedia had 757 question marks against 19,826 in the
  speech set (Suen 2025). `single-source`.
- **A ceiling exists.** Of 100 mismatches examined on Latvian, 43 were
  valid alternatives and 21 needed the audio to decide (Znotins 2025).

## LLMs as restorers

Detail: [LLM restoration](concepts/llm-restoration.md).

- **Prompted LLMs lose to taggers.** On English podcasts a BERT tagger
  scored overall F1 75.4 against zero-shot GPT-4 Turbo's 66.8, with GPT-4
  comma precision 47.7 (Liu 2024). A prompted 1B LLM scored macro F1
  0.566 against ELECTRA-small's 0.913 (Woo 2026).
- **They change words.** GPT-4o changed words in 16.4% of utterances and
  GPT-4o mini in 24.6%; the tagger in 0.0%. Fine-tuned LLMs still changed
  1.4–2.7% (Znotins 2025). That prompt asked for corrections, so some of
  it was requested.
- **Fine-tuned LLMs can be more accurate.** Fine-tuned 1.7–2B LLMs
  reached punctuation F1 79.0–79.1 and fine-tuned GPT-4o 81.5, against
  75.1 for an off-the-shelf, Europarl-trained XLM-R tagger on Latvian
  recogniser output (Znotins 2025). The tagger was not trained on the
  same data, so the comparison is confounded.
- **An LLM can be constrained to tagging.** Forward-pass-only labelling
  with LLaMA2-13B is 19.84× faster than generation and leaves words
  unchanged, with comma F1 falling 0.74 → 0.66 (Pang 2024). A LoRA-tuned
  1B LLM used as a scorer beat ELECTRA-small on commas, 0.840 against
  0.752 (Woo 2026, oracle sentence boundaries).

## Pauses and prosody

Detail: [acoustic features](concepts/acoustic-features.md).

Adding audio to fine-tuned BERT-base raised overall F1 77.1 → 78.5–78.6
on MuST-C reference text: question +5, full stop +1, comma +2 (Zhu 2022).
`single-source`. On English podcasts an acoustic-plus-text model scored
73.3 against BERT's 75.4 (Liu 2024). On Latvian, fine-tuned Whisper
reached question-mark F1 72.1 against 68.9 for the best text-only system
(Znotins 2025). The evidence supports audio for question marks only.

## The recogniser writes case and punctuation itself

Detail: [end-to-end formatted ASR](concepts/end-to-end-formatted-asr.md).

- **It beat a tuned cascade on English.** On LibriSpeech-PC test-clean /
  test-other, a 115M Conformer trained on formatted transcripts scored
  punctuation error rate 29.48 / 27.37 and cased, punctuated WER 8.11 /
  10.48. A words-only 115M recogniser plus a tuned 109M BERT tagger
  scored 36.60 / 37.42 and 9.45 / 12.90 (Meister 2023).
  `benchmark-reported`.
- **Word error cost is about zero** at 115M (2.60 → 2.83 clean, 5.79 →
  5.65 other; Meister 2023) and at 1.1B (Koluguri 2024).
- **It works at this size.** A 65M Zipformer transducer with a 500-token
  cased vocabulary reached punctuation error rate 29.74 / 28.18 and WER
  2.20 / 5.23 (You 2025).
- **Case is the easy half** for both routes: capitalisation F1 94.5–95.5,
  punctuation F1 84.75 against 87.40 (Meister 2023).
- **Limits.** It needs speech with formatted transcripts; the sources use
  385 h to 31,000 h. An 18M streaming model scored period F1 27.3 on
  segments (Kim 2023). The cascade's tagger was BERT-base, untuned to
  speech; no source tests a tagger trained on large speech-like text.

## Evaluation

Detail: [evaluation metrics](concepts/evaluation-metrics.md).

- **Score on recogniser output.** F1 on reference text overstates: a
  RoBERTa-large tagger fell from 82.9 to 74 overall and from 87.8 to 63.4
  on question marks (as relayed by Gris 2023).
- **Do not score only perfectly recognised utterances.** They were
  48–67% of LibriSpeech-PC utterances (Meister 2023).
- **Report per-class precision, recall and F1 without the no-mark
  class.** FullStop's micro F1 of 0.983 includes it; the macro is 0.789
  (Vandeghinste 2023).
- **Add a single readability number:** cased, punctuated WER beside
  normalised WER, or punctuation error rate after aligning words.

## Contested results

- **Cascade or formatted recogniser.** English evidence favours the
  formatted recogniser (Meister 2023, Koluguri 2024). The cascades it
  beat used a BERT-base tagger trained on written text. A small streaming
  recogniser alone is poor at sentence ends (Kim 2023).
- **Tagger or LLM.** Prompted LLMs lose (Liu 2024, Woo 2026); fine-tuned
  ones win against an unmatched tagger (Znotins 2025).
- **Large or base encoder.** +2.1 F1 (Alam 2020) against −0.4 (Courtland
  2020) on the same English test set.
- **CRF head.** No gain (Alam 2020, PhoPunct) against +1.39 (Uyen 2022).

## Negative and quiet results

- BiLSTM and CRF layers over a pretrained encoder did not help in 7 of 8
  Vietnamese pairs (PhoPunct).
- Attention added to the CNN-BiLSTM lowered question-mark F1 from 72.1 to
  56.8 (You 2024).
- Recognisers with built-in punctuation did poorly on 5-minute inputs:
  comma F1 0.40 for a 1B transducer and 0.46 for Whisper large v2 (Pang
  2024).
- Whisper-large on Portuguese interviews produced no colons or
  semicolons, scored 5.1 F1 on exclamation marks and wrote 26.6% more
  sentences than the human reference (Gris 2023).
- Naively concatenating utterances to train a streaming formatted
  recogniser raised WER from 15.8 to 21.3 (Kim 2023).

## Baseline sensitivity

- The compact model's "9% relative improvement" is over non-Transformer
  models; against RoBERTa-base it is 13–15 comma F1 behind.
- Audio gains are measured over BERT-base on reference text, not over a
  tagger trained on speech transcripts.
- The formatted recogniser's win is over a BERT-base cascade.
- PhoBERT-large's News lead comes with a size change; PhoBERT base was
  not run.

## Disconfirming pass

The pass tested four parts of the starting hunch.

| Hunch | Outcome |
|---|---|
| A two-head per-word tagger is the right form | Held for a post-processor. Not held as the best route overall: the formatted recogniser beat it on English. |
| Periods and sentence-initial capitals are easy | Not held for small models: periods lose 4–8 F1, and missed periods cause most capitalisation errors (You 2024). |
| Commas and proper-name capitals separate small from large | Commas: held. Proper-name capitals: no paper measures them apart from sentence-initial ones. |
| Pauses add little | Held for commas and full stops, not for question marks. |

Searches run to refute: LLM against encoder comparisons, distillation
gaps, acoustic gains over pretrained text models, and forward citations
of the five anchors on both recency and citation count.

## Reading for the stated setting

This is our inference from the map, not a source's claim.

1. **Two routes are live.** A text tagger is cheap and needs no formatted
   speech. A formatted recogniser needs a new vocabulary and formatted
   Vietnamese speech; the PhoASR 500 h set and the Huyen 2026 result say
   that this is feasible at 68M.
2. **For the tagger, train on speech-like text.** Punctuate and case real
   transcripts of Vietnamese speech with a strong model, add written text
   for names, and verbalise numbers so the input matches the recogniser.
3. **Train a base-size encoder first as the ceiling, then a small
   student.** The 7 MB CNN-BiLSTM is the form that deploys in sherpa-onnx
   without new runtime code. Expect it to trail on commas and periods.
4. **Evaluate on real recogniser output,** per class, with cased,
   punctuated WER beside it.

## Unread leads

Cited by the read papers and not fetched:

- Polacek and Cerva 2025, lightweight online punctuation and
  capitalisation for streaming ASR; Polacek 2023, ELECTRA with lookahead.
- Hentschel, Tsunoo and Okuda 2021, multi-task learning and distillation
  for a fast restorer.
- Nozaki 2022, end-to-end speech to punctuated text; Zhou 2022, on-device
  punctuation with a separate decoder.
- Sunkara 2020, two papers: medical truecasing with recogniser-aligned
  augmentation, and multimodal semi-supervised punctuation.
- Vietnamese: Pham 2020 (the News and Novels corpus), Tran 2021, T. T. H.
  Nguyen 2021 (IEICE), O. T. Tran 2021, T. B. Nguyen 2020.
- Guhr 2021 (FullStop), Zhong and Sun 2025 (BERT against LLMs), Pappagari
  2021 (joint truecasing and punctuation for conversational speech).
- Boháč 2017, inter-annotator agreement on commas.

## Retrieval and limits

- arXiv papers with an HTML view were derived from it; older ones and the
  four ACL and ISCA papers went through marker-pdf.
- Vu 2026 and Huyen 2026 were read through a page fetch and an abstract.
  Their claims here are not citation-checked against a committed extract.
- The cross-paper gap between the CNN-BiLSTM and RoBERTa-base assumes the
  same IWSLT 2011 test set and scoring in both papers.
- No source reports phone latency or memory for a tagger.
