# Written-text training against spoken and recognized test data

Grounded from fetched full text (2026-11-13). Every number below is from the
cited extract line; nothing is from recall. Map node: `../survey.md` (not yet
written when this page was created).

**Sources read** (full text, local extracts). Citations below use
`<key>:<lines>`, meaning lines of the extract file linked here.

- Liu and Beigi, 2024 technical report, *Spontaneous Informal Speech Dataset
  for Punctuation Restoration* (SponSpeech) —
  [HTML](https://arxiv.org/html/2409.11241) · [PDF](https://arxiv.org/pdf/2409.11241) ·
  [extract](../related-work/extract/liu2024-sponspeech/html/2409.11241.md)
  (`extract/liu2024-sponspeech/html/2409.11241.md`, key `liu`) ·
  [reading note](../related-work/readings/liu2024-sponspeech.md)
- Suen, Chow, Lam (Fano), Interspeech 2025, *Cantonese Punctuation
  Restoration using LLM Annotated Data* —
  [PDF](https://www.isca-archive.org/interspeech_2025/suen25_interspeech.pdf) ·
  [extract](../related-work/extract/suen2025-cantonese-llm-annotated/suen2025-cantonese-llm-annotated.md)
  (`extract/suen2025-cantonese-llm-annotated/suen2025-cantonese-llm-annotated.md`, key `suen`) ·
  [reading note](../related-work/readings/suen2025-cantonese-llm-annotated.md)
- Znotins, Gruzitis, Dargis, W-NUT 2025, *From Conversational Speech to
  Readable Text* (Latvian) —
  [PDF](https://aclanthology.org/2025.wnut-1.15.pdf) ·
  [extract](../related-work/extract/znotins2025-readable-text/znotins2025-readable-text.md)
  (`extract/znotins2025-readable-text/znotins2025-readable-text.md`, key `znotins`) ·
  [reading note](../related-work/readings/znotins2025-readable-text.md)
- Behre et al. (Microsoft), 2022/2023, *Streaming Punctuation* —
  [arXiv](https://arxiv.org/abs/2301.03819) · [PDF](https://arxiv.org/pdf/2301.03819) ·
  [extract](../related-work/extract/behre2023-streaming-punct/behre2023-streaming-punct.md)
  (`extract/behre2023-streaming-punct/behre2023-streaming-punct.md`, key `behre23`) ·
  [reading note](../related-work/readings/behre2023-streaming-punct.md);
  conference version [arXiv](https://arxiv.org/abs/2210.05756) ·
  [reading note](../related-work/readings/behre2022-streaming-dictation.md)
- Pang et al. (Meta), 2024, *LLaMA based Punctuation Restoration With
  Forward Pass Only Decoding* —
  [HTML](https://arxiv.org/html/2408.11845) · [PDF](https://arxiv.org/pdf/2408.11845) ·
  [extract](../related-work/extract/pang2024-llama-fpod/html/2408.11845.md)
  (`extract/pang2024-llama-fpod/html/2408.11845.md`, key `pang`) ·
  [reading note](../related-work/readings/pang2024-llama-fpod.md)

## Size of the gap from scripted or written training data

| Claim | Setting | Numbers | Grade |
|---|---|---|---|
| Training on scripted talks costs 2.3–4.0 overall F1 on spontaneous podcasts | Train on MuST-C (TED talks) vs on SponSpeech train (469 h podcasts); test on SponSpeech test and test-amb; human subtitles as reference | BERT 71.4 vs 75.4 on test, 70.9 vs 73.8 on test-amb; EfficientPunct 70.5 vs 73.3 and 69.8 vs 72.1 (`liu:204-260`, `liu:362-402`, `liu:446-486`); the authors' summary is "about 2.3% to 4.0%" (`liu:330`) | single-source |
| The loss is concentrated in commas | BERT, SponSpeech test | Comma F1 64.7 (MuST-C-trained) vs 70.5 (in-domain); full stop 80.1 vs 82.4; question 74.3 vs 76.8 (`liu:219-231`, `liu:390-399`) | single-source |
| Spoken-domain training transfers back to scripted talks | Train on SponSpeech, test on MuST-C | Overall F1 BERT 72.7, EfficientPunct 74.5 (`liu:288-314`). No MuST-C-trained score on MuST-C is in the paper, so the size of this direction's gap is unknown | single-source |
| Written encyclopedia text is worse training data than a third as much LLM-punctuated speech transcript | Cantonese; test HKCanCor (human-punctuated spontaneous speech and radio); Wikipedia 9.1M words vs YouTube ASR transcripts 3.1M words labelled by Qwen-2.5-72b (`suen:91-93`) | Overall F1, Wikipedia-only → YouTube-only: BERT-Base-Chinese 72.4 → 73.4; multilingual BERT 69.4 → 72.9; XLM-R 72.7 → 73.4 (`suen:143-152`); summary "0.7 to 3.5" (`suen:163`) | single-source |
| The written-text tagger under-inserts commas on speech | same, comma recall | Wikipedia-only 48.2–55.0; YouTube-only 71.9–73.9, at precision 45.6–46.8 against 50.1–50.3 (`suen:143-152`) | single-source |
| Written text has almost no questions | Cantonese corpus statistics | Wikipedia: 757 question marks in 301,521 sentences; YouTube: 19,826 in 130,888 (`suen:92-93`). Question F1 from Wikipedia-only is 58.0 for multilingual BERT and 69.2–69.8 for the other two encoders, against 70.3–70.7 from YouTube (`suen:143-152`) | single-source |
| A tagger trained mostly on written web text reaches modest absolute scores on long-form recognizer output | English; training mix 52.8% OpenWebText, 31.5% Stack Exchange, 7.6% subtitles, 6.7% earnings calls, 1.4% podcasts, converted to spoken form by a WFST normalizer (`behre23:119-123`, `behre23:129-131`); 12-layer transformer, cross-segment decoding | Overall punctuation F1: dictation 67, earnings calls 66, parliament 62, podcasts 75; comma F1 55–65 (`behre23:189-201`) | single-source; no in-domain-trained comparison |
| Recognizers trained to emit punctuation do poorly on long video | English, 1.2k utterances averaging 5 minutes | RNN-T 1B comma F1 0.40, period 0.68; Whisper large v2 comma 0.46, period 0.65 (`pang:262-270`) | single-source, private test set |

The measured gaps are a few F1 points, not a collapse. Two of the three
gap measurements (Liu, Suen) use reference or near-reference words; only
the Latvian study below measures the added cost of recognition errors.

## Recognition errors

| Claim | Setting | Numbers | Grade |
|---|---|---|---|
| At 12.7 WER, punctuation F1 drops 2–4 points from reference text | Latvian LATE-Media test; recognizer is Whisper large-v3 fine-tuned for Latvian | XLM-R 77.4 → 75.1; GPT-4o FT 85.1 → 81.5; Gemma-2-2B FT 81.6 → 79.1; EuroLLM-1.7B FT 82.8 → 79.0 (`znotins:119-135`) | single-source |
| Capitalization is hit harder | same | XLM-R 84.3 → 78.9; GPT-4o FT 91.8 → 84.4; Gemma-2-2B FT 88.3 → 81.9 (`znotins:119-135`) | single-source |
| All-caps tokens (acronyms) suffer most | same; 78 such tokens in test (`znotins:63`) | XLM-R 72.7 → 46.2; GPT-4o FT 83.9 → 38.5; EuroLLM FT 90.3 → 53.8 (`znotins:119-134`) | single-source, very small count |
| The better system loses more | same | The fine-tuned GPT-4o lead over XLM-R shrinks from 7.7 to 6.4 punctuation F1 (our subtraction from `znotins:119-131`) | single-source |

Scoring on recognizer output needs an alignment step: the authors use a
heuristic fuzzy alignment for misrecognized words and for words whose
spoken and written forms differ, such as numbers and abbreviations
(`znotins:87`). They suggest injecting recognizer-like noise in training and
warn it may change meaning; they did not test it (`znotins:190`).

## Disfluencies

No source isolates the effect of disfluencies with a controlled comparison.
What the sources record:

- SponSpeech was built because TED-derived sets lack stutters, hesitations
  and interruptions (`liu:28-30`); the 2.3–4.0 F1 gap above is the nearest
  thing to a measurement and confounds disfluency with topic and style.
- The Latvian corpus keeps repetitions and truncated words (`znotins:49`);
  the authors' error analysis names "sentence boundary determination and
  disfluency handling" as recurring pitfalls without counts for the latter
  (`znotins:19`).
- One of Behre's test references (earnings calls) had disfluencies, false
  starts and repetitions removed by transcribers (`behre23:149`), so that
  set is not a test of disfluent input.
- HKCanCor keeps filler words in the transcripts (`suen:52`).

## How well-defined is the punctuation of speech

| Evidence | Setting | Numbers | Grade |
|---|---|---|---|
| Nearly half of system-reference mismatches are acceptable alternatives | Latvian; 100 manually analysed mismatched samples across models | 57 actual errors, 43 valid alternative formatting (`znotins:147-153`) | single-source |
| A fifth of mismatches cannot be decided from text | same | For 21 of the 100 the annotators had to listen to the audio, e.g. "Labi. Sakratīts ir." vs "Labi sakratīts ir." (`znotins:155`) | single-source |
| Marks beyond comma, period, question mark are too rare and too subjective to score | same | Exclamation marks, ellipses and dashes are mapped to periods; colons and semicolons dropped as "subjectively annotated" (`znotins:51`); results on a broader set are called unreliable, with "increased inter-annotator disagreement" (`znotins:159-176`). No agreement figure is given | single-source |
| Comma placement differs by convention, not only by error | Cantonese; five LLMs against HKCanCor | Comma precision 39.4–46.3 with recall up to 80.4; the authors attribute part of this to style, e.g. a comma after an initial "but" (`suen:38-42`, `suen:97`) | single-source |
| A test split selected for ambiguity is only slightly harder | SponSpeech test-amb vs test, in-domain training | BERT 73.8 vs 75.4; EfficientPunct 72.1 vs 73.3; GPT-4 Turbo 66.4 vs 66.8 (`liu:362-416`, `liu:446-500`). The ambiguity classifier was trained on 100 hand-labelled samples and was not evaluated (`liu:138`, `liu:322`) | single-source |

No source read here reports a human inter-annotator agreement number for
punctuation of speech. The qualitative agreement across the three is that
sentence boundary versus comma ("go there, but you" / "go there. But you",
`liu:155-159`), optional commas after sentence-initial connectives, and
statement versus question for particle-final or declarative-form questions
are the ambiguous decisions. Suen et al. give a tonal example: the same
written Cantonese string is a statement or a confirmation question depending
on the tone of its final particle, which text cannot show (`suen:175`).

## Does audio close the gap

| Claim | Setting | Numbers | Grade |
|---|---|---|---|
| Adding acoustic embeddings to BERT does not beat BERT on spontaneous speech | SponSpeech test; EfficientPunct and UniPunc use BERT plus Kaldi embeddings | Overall F1 BERT 75.4, EfficientPunct 73.3, UniPunc 65.3 (`liu:362-402`) | single-source; contradicts the same models' reported advantage on MuST-C, which the authors note (`liu:521`) |
| The acoustic model's advantage on question marks is 0.2–0.3 F1 | same | Question F1 EfficientPunct 77.0 vs BERT 76.8 on test; 75.3 vs 75.0 on test-amb; comma 67.4 vs 70.5 (`liu:362-399`, `liu:446-483`) | single-source |
| A recognizer fine-tuned to emit punctuation gets the best question marks | Latvian, recognizer output | whisper-large-v3-lv question F1 72.1; best text-only system 68.9 (GPT-4o FT); XLM-R 57.5 (`znotins:117-122`) | single-source |
| Its overall punctuation is level with 2B text LLMs and 3 points over the tagger | same | 78.3 vs 79.0–79.1 vs 75.1 (`znotins:117-126`) | single-source |

These two sources disagree in emphasis. Liu and Beigi find no benefit from
one particular way of adding acoustics; Znotins et al. find that a
recognizer with access to audio wins on question marks by 3–15 F1 and that
21% of analysed mismatches need audio. The cases are not the same design:
one fuses frame embeddings into a text tagger, the other lets the
recognizer itself emit marks.

## What closes the gap

- **In-domain spoken training data with human punctuation.** +2.3 to +4.0
  overall F1 over scripted-talk training (Liu, above). 469 hours were
  obtained by filtering Creative Commons podcast videos that have
  uploader-written subtitles (`liu:105`, `liu:80`).
- **Recognizer transcripts of real speech punctuated by an LLM.** +0.7 to
  +3.5 overall F1 over written text; written text first and then the
  LLM-labelled speech adds another 0.2–0.6 (`suen:163-165`). The resulting
  tagger copies the LLM's comma density (comma precision 46–48).
- **Fine-tuning on about 70 hours of formatted conversational transcripts.**
  Enough for 1.7–2B LLMs to reach 79 punctuation F1 on recognizer output
  (`znotins:47`, `znotins:125-126`).
- **Spoken-form conversion of written text.** Behre et al. strip
  punctuation and run a WFST text normalizer so training input looks like
  recognizer words, keeping alignments to place the tags
  (`behre23:129-131`). No ablation of this step is reported.
- **Simulated recognizer errors.** Cited by Znotins et al. and Suen et al.
  to Alam et al. 2020 as helpful (`znotins:35`, `suen:25`); not tested in
  any source read here.

## What this does not show

- No Vietnamese data. The written-to-spoken gap is measured for English
  (scripted talks to podcasts) and Cantonese (encyclopedia to broadcast and
  conversation), with reference-quality words.
- No controlled measurement of disfluency, and no test where recognition
  error rate is varied; one WER point (12.7) for one language.
- No human agreement figure, so no ceiling for F1 on speech.
- No capitalization evidence except Latvian, where case follows European
  conventions and acronyms were 78 test tokens.
- No evidence about number formatting; Latvian models were asked to convert
  numbers and "approximately 50%" of annotated corrections were made, on a
  test set the authors call too small (`znotins:157`).
- Liu's in-domain and cross-domain models differ in training-set size and
  style at once (MuST-C v1 is listed at 438 h, SponSpeech train at 469 h;
  `liu:58`, `liu:80`), and there is one run per cell with no variance.
- Suen's "written" baseline is Cantonese Wikipedia; the size of the gap for
  written text closer to speech (subtitles, forums) is not measured.
