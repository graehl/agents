# LLMs as punctuation and case restorers, against encoder taggers

Grounded from fetched full text (2026-11-13). Every number below is from the
cited extract line; nothing is from recall. Map node: `../survey.md` (not yet
written when this page was created).

**Sources read** (full text, local extracts). Citations below use
`<key>:<lines>`, meaning lines of the extract file linked here.

- Liu and Beigi, 2024 technical report, *Spontaneous Informal Speech Dataset
  for Punctuation Restoration* (SponSpeech) —
  [HTML](https://arxiv.org/html/2409.11241) · [PDF](https://arxiv.org/pdf/2409.11241) ·
  [extract](../related-work/extract/liu2024-sponspeech/html/2409.11241.md)
  (`extract/liu2024-sponspeech/html/2409.11241.md`, key `liu`)
- Pang, Paul, Jiang, Zhang, Lei (Meta), 2024, *LLaMA based Punctuation
  Restoration With Forward Pass Only Decoding* —
  [HTML](https://arxiv.org/html/2408.11845) · [PDF](https://arxiv.org/pdf/2408.11845) ·
  [extract](../related-work/extract/pang2024-llama-fpod/html/2408.11845.md)
  (`extract/pang2024-llama-fpod/html/2408.11845.md`, key `pang`)
- Woo, Kang, Kim (Korea University), 2026, *Efficient Punctuation Restoration
  via Weighted Lookahead Scoring Method for Streaming ASR Systems* —
  [HTML](https://arxiv.org/html/2606.05179) · [PDF](https://arxiv.org/pdf/2606.05179) ·
  [extract](../related-work/extract/woo2026-lookahead-scoring/html/2606.05179.md)
  (`extract/woo2026-lookahead-scoring/html/2606.05179.md`, key `woo`)
- Znotins, Gruzitis, Dargis, W-NUT 2025, *From Conversational Speech to
  Readable Text: Post-Processing Noisy Transcripts in a Low-Resource Setting*
  (Latvian) — [PDF](https://aclanthology.org/2025.wnut-1.15.pdf) ·
  [extract](../related-work/extract/znotins2025-readable-text/znotins2025-readable-text.md)
  (`extract/znotins2025-readable-text/znotins2025-readable-text.md`, key `znotins`)
- Suen, Chow, Lam (Fano), Interspeech 2025, *Cantonese Punctuation
  Restoration using LLM Annotated Data* —
  [PDF](https://www.isca-archive.org/interspeech_2025/suen25_interspeech.pdf) ·
  [extract](../related-work/extract/suen2025-cantonese-llm-annotated/suen2025-cantonese-llm-annotated.md)
  (`extract/suen2025-cantonese-llm-annotated/suen2025-cantonese-llm-annotated.md`, key `suen`)

Per-paper reading notes:
[liu](../related-work/readings/liu2024-sponspeech.md) ·
[pang](../related-work/readings/pang2024-llama-fpod.md) ·
[woo](../related-work/readings/woo2026-lookahead-scoring.md) ·
[znotins](../related-work/readings/znotins2025-readable-text.md) ·
[suen](../related-work/readings/suen2025-cantonese-llm-annotated.md).
Related pages: [segmentation-and-streaming](segmentation-and-streaming.md),
[spoken-vs-written](spoken-vs-written.md).

All F1 values are per punctuation mark at word boundaries unless a row says
otherwise. Liu and Suen report percentages; Pang and Woo report fractions.

## Four ways an LLM is used

1. **Prompted regeneration.** The model is asked to rewrite the transcript
   with punctuation. It can change words. (Liu: GPT-4 Turbo zero-shot;
   Znotins: GPT-4o, GPT-4o mini; Suen: five LLMs with three in-prompt
   examples; Woo: Llama-3.2-1B-Instruct as the baseline.)
2. **Fine-tuned regeneration.** Same output form after task fine-tuning
   (Znotins: GPT-4o, GPT-4o mini, EuroLLM-1.7B, Gemma-2-2B; Pang: LLaMA2 13B
   with LoRA, decoded autoregressively).
3. **Forward-pass-only tagging (FPOD).** The unpunctuated input is copied
   into the response slot of the fine-tuned prompt and run once; wherever the
   next-token prediction at a response position is a punctuation symbol, it is
   inserted. The words cannot change (`pang:62-66`, `pang:130`).
4. **LLM as scorer.** At each word boundary a causal LM scores "no mark",
   comma, period and question mark by a weighted sum of the mark's log
   probability given the prefix and the log likelihood of the next \(K\)
   subword tokens given the prefix plus that mark; a mark is inserted only if
   its margin over "no mark" exceeds a threshold. Weight and threshold are
   tuned on validation data; the words cannot change (`woo:140-176`).

A fifth use, the LLM as annotator of training data for a small tagger, is
the last section.

## Prompted LLMs against fine-tuned encoder taggers

| Claim | Setting | Numbers | Grade |
|---|---|---|---|
| A fine-tuned BERT tagger beats zero-shot GPT-4 Turbo on spontaneous English | SponSpeech test (podcasts, human subtitles as reference, 58 h); BERT trained on the 469 h train split (`liu:80-82`, `liu:506-511`) | Overall F1 BERT 75.4 vs GPT-4 Turbo 66.8. Comma 70.5 vs 61.1; full stop 82.4 vs 77.5; question 76.8 vs 74.0 (`liu:390-416`) | single-source |
| GPT-4 Turbo's deficit is comma over-insertion and missed full stops | same | Comma P 47.7 / R 85.0 (BERT 66.5 / 75.0); full stop P 87.0 / R 70.0 (BERT 82.4 / 82.3) (`liu:390-410`) | single-source |
| The same ordering holds on the more ambiguous split | SponSpeech test-amb (60 h) | Overall BERT 73.8 vs GPT-4 Turbo 66.4 (`liu:474-500`) | single-source |
| A small encoder beats prompted generation from a 1B LLM by a wide margin | IWSLT 2017 English, 10,799 test sentences, oracle sentence segmentation (`woo:188`, `woo:157`); ELECTRA-small with 2 subword tokens of right context vs Llama-3.2-1B-Instruct prompted, greedy | 4-class macro F1 0.913 vs 0.566; comma 0.752 vs 0.457; period 0.992 vs 0.699; question 0.925 vs 0.622 (`woo:259-291`) | single-source |
| Prompted LLMs over-insert commas in Cantonese too | HKCanCor (spontaneous speech and radio, 12,480 utterances), three in-prompt examples, temperature 0.1 (`suen:52-54`, `suen:91`) | Comma precision 39.4–46.3 across five LLMs with recall up to 80.4; best overall F1 73.6 (Qwen-2.5-72b), GPT-4o-mini 69.9, Llama-3.3-70b 62.7, Yi-1.5-34B 52.9 (`suen:38-42`). The prose says 35.8–46.3 (`suen:97`); the table's minimum is 39.4 | single-source |
| An off-the-shelf multilingual tagger is close to zero-shot GPT-4o mini and behind GPT-4o on Latvian ASR output | LATE-Media test, output of a fine-tuned Whisper large-v3 at 12.7 WER; XLM-RoBERTa trained on Europarl, not on this corpus (`znotins:37`, `znotins:85`) | Punctuation F1 XLM-R 75.1, GPT-4o mini 75.8, GPT-4o 78.2; capitalization 78.9, 79.7, 81.3 (`znotins:119-123`) | single-source |

The Latvian row is the only one where a prompted LLM beats the tagger, and
there the tagger was never trained on the target domain while every
fine-tuned LLM was. No source read here trains an encoder tagger and an LLM
on the same spoken data and compares them, except Woo's ELECTRA-small row
and Suen's students (below).

## Fine-tuned LLMs

| Claim | Setting | Numbers | Grade |
|---|---|---|---|
| Fine-tuning a 1.7–2B LLM on about 70 h of transcripts reaches GPT-4o-mini-fine-tuned quality | Latvian LATE-Media, ASR output; 3 epochs on the train split only (`znotins:47`, `znotins:99`) | Punctuation F1: GPT-4o FT 81.5, GPT-4o mini FT 79.3, Gemma-2-2B FT 79.1, EuroLLM-1.7B FT 79.0. Capitalization: 84.4, 82.4, 81.9, 82.7 (`znotins:122-126`) | single-source |
| Fine-tuned LLMs beat the off-the-shelf tagger by 4–8 punctuation F1 | same | XLM-R 75.1 vs 79.0–81.5 on ASR output; 77.4 vs 81.6–85.1 on reference transcripts (`znotins:119-135`) | single-source; confounded by in-domain training of the LLMs only |
| A Whisper model fine-tuned for the language, using audio, matches the 2B text LLMs without a second model | same | whisper-large-v3-lv: punctuation 78.3, capitalization 81.8, question mark 72.1 (highest of any system on ASR output; GPT-4o FT 68.9) (`znotins:117`, `znotins:122`) | single-source |
| A LoRA-tuned 13B LLaMA2 decoded autoregressively | LibriSpeech-PC test (read books), LoRA on 20k examples from train-clean-360 (`pang:204-208`) | F1 question 0.80, period 0.84, comma 0.74 (`pang:227-230`). No encoder-tagger baseline is reported | single-source |

## Constrained use: forward-pass tagging and scoring

| Claim | Setting | Numbers | Grade |
|---|---|---|---|
| FPOD keeps period and question quality and loses comma quality | LibriSpeech-PC test, LLaMA2 13B LoRA | FPOD 0.79 / 0.85 / 0.66 (question / period / comma) vs autoregressive 0.80 / 0.84 / 0.74 (`pang:227-243`) | single-source |
| A second pass that feeds back inserted marks ("recursive FPOD") recovers much more on long input | In-house video ASR set, 1.2k human-annotated utterances averaging 5 minutes; reference has 808 question marks, 9,837 periods, 6,457 commas (`pang:288`) | FPOD 0.79 / 0.82 / 0.63; recursive FPOD 0.93 / 0.95 / 0.87; RNN-T 1B with built-in punctuation 0.63 / 0.68 / 0.40; Whisper large v2 0.58 / 0.65 / 0.46 (`pang:262-280`) | single-source, private test set |
| A 1B causal LM used only as a scorer, with no fine-tuning, is within 0.02 macro F1 of a fine-tuned ELECTRA-small at equal lookahead | IWSLT 2017 English, oracle sentence segmentation, \(K=2\) subword tokens of right context | Llama-3.2-1B scoring, no fine-tuning: comma 0.790, period 0.932, question 0.871, macro 0.893. ELECTRA-small: 0.752, 0.992, 0.925, 0.913 (`woo:276-327`) | single-source |
| The same scorer after LoRA fine-tuning on 357,117 sentences beats ELECTRA-small | same | comma 0.840, period 0.986, question 0.935, macro 0.937 vs 0.913 (`woo:346-361`, `woo:216`) | single-source |
| The scorer needs right context | same, fine-tuned variant | \(K=0\): macro 0.646, punctuation-only macro 0.543; \(K=1\): 0.927 / 0.909; \(K=2\): 0.937 / 0.920; \(K=3\)–\(5\): 0.930–0.935 (`woo:398-405`) | single-source |

Our reading of Woo's protocol, not a statement in the paper: the prefix is
reset at reference sentence boundaries and the lookahead is truncated at
the sentence end (`woo:60`, `woo:157`), so a boundary with no following
tokens can only be a sentence end. That makes the period and question-mark
scores (0.93–0.99) easier than in deployment for every system in the table;
the comma column is the informative one, and there the ordering is
fine-tuned scorer 0.840 > untuned scorer 0.790 > ELECTRA-small 0.752.

## Model size and speed

Only Pang et al. measure speed, and no source measures a phone or a CPU.

- **LLaMA2 13B, autoregressive:** 88.72 tokens/s; with speculative decoding
  using a 350 MB distilled assistant, 173.43 tokens/s at identical F1; FPOD
  1,760.30 tokens/s, 19.84× the autoregressive rate (`pang:204`,
  `pang:208`, `pang:227-243`). Recursive FPOD on the 5-minute inputs runs at
  959.1 tokens/s, 10.8× (`pang:288`). The hardware is not stated.
- **Long input for FPOD** uses a sliding window with padding, because the
  authors expect LLM quality to fall on very long context (`pang:133`,
  `pang:138`).
- **Woo et al.** use a 1B-parameter model and state that latency and memory
  were not measured (`woo:26`, `woo:457`). The method scores four hypotheses
  over \(K\) lookahead tokens at every word boundary.
- **Znotins et al.** give sizes only by name (1.7B, 2B, GPT-4o) and no
  timing; **Suen et al.** give the student shape (12 layers, hidden size 768,
  `suen:117`) against 34B–72B annotator LLMs and no timing; **Liu and Beigi**
  give neither size nor timing for BERT or GPT-4 Turbo.

## Do LLMs change the words, and what stops them

| Evidence | Setting | Numbers | Grade |
|---|---|---|---|
| Prompted LLMs change words in a sixth to a quarter of utterances | Latvian test split; share of utterances with any word change | GPT-4o 16.4%, GPT-4o mini 24.6%, XLM-R tagger 0.0% (`znotins:165-169`) | single-source |
| Fine-tuning cuts that by about ten times but not to zero | same | GPT-4o FT 1.4%, GPT-4o mini FT 1.5%, Gemma-2-2B FT 1.7%, EuroLLM-1.7B FT 2.7% (`znotins:168-172`) | single-source |
| Word error added on clean reference text | same; WER of the output against the reference words | GPT-4o 3.0, GPT-4o mini 4.7; fine-tuned models 0.3–0.4; XLM-R 0.0 (`znotins:128-135`) | single-source |
| Type of change | manual review of up to 100 changed utterances per model | GPT-4o: 42% substitutions, 21% inflection changes, 29% deletions, 8% insertions. Gemma-2-2B FT: 47 / 27 / 20 / 7 (`znotins:167`, `znotins:172`) | single-source |
| With a "do not change words" prompt, temperature 0.1 and up to three retries, a residue still fails | Cantonese HKCanCor | Discard rate below 0.7% for most models, about 5% for Yi-1.5-34B (`suen:54`, `suen:81`) | single-source |
| A 1B instruction model ignores the same kind of prompt | IWSLT 2017 | Example output puts a comma after every word; the base model repeats the prompt. No rate is given (`woo:200-204`) | single-source, qualitative |

Two cautions on the Latvian change rates. The zero-shot prompt asks the
model to "correct grammar, mispronounced words, and abbreviations" and to
convert numbers (`znotins:91`), so part of the 16–25% is requested editing,
not disobedience. And the paper's qualitative examples of unrequested edits
are deletions of words judged superfluous, added connectives, meaning-changing
substitutions, and, for GPT-4o mini, non-existent words (`znotins:107-109`,
`znotins:139`); fine-tuned 2B models "rarely alter transcripts" and their
errors are ungrammatical forms (`znotins:141`).

Controls used across the sources:

- **Prompt constraint plus low temperature plus retry-and-discard**
  (`suen:54`, `suen:62-65`).
- **Fine-tuning on the task** (`znotins:141`).
- **WER of the output against the input words as a check**, with fuzzy
  alignment for number and abbreviation forms (`znotins:87`).
- **Structural prevention:** FPOD copies the input and only inserts marks
  (`pang:130`); the scorer chooses among a closed set of marks (`woo:62`).
  Both make a word change impossible by construction, as a tagger does.
  FPOD's algorithm does delete a space before a predicted digit
  (`pang:88-90`).

Pang et al. name hallucination as a problem of autoregressive LLaMA
(`pang:11`) but report no rate for it.

## LLMs as annotators; students trained on their labels

Suen et al. transcribe 237 hours of Cantonese YouTube video with a
proprietary ASR model, punctuate the transcripts with the best prompted LLM
(Qwen-2.5-72b), and fine-tune 12-layer encoder taggers on the result:
130,888 utterances, 3.1M words (`suen:92`, `suen:101-105`). The test set is
HKCanCor, human-punctuated spontaneous speech.

| Claim | Setting | Numbers | Grade |
|---|---|---|---|
| The student matches its annotator | HKCanCor overall F1 (micro over three marks) | XLM-RoBERTa-Base, Wikipedia then YouTube: 74.0; Qwen-2.5-72b: 73.6 (`suen:41`, `suen:153`, `suen:167`) | single-source |
| LLM-labelled speech transcripts beat three times as much written text | same; Cantonese Wikipedia is 301,521 sentences, 9.1M words (`suen:93`) | YouTube-only vs Wikipedia-only overall F1: BERT-Base-Chinese 73.4 vs 72.4; multilingual BERT 72.9 vs 69.4; XLM-R 73.4 vs 72.7 (`suen:143-152`) | single-source |
| Written text first, then LLM-labelled speech, adds a little | same | +0.2 to +0.6 F1 over YouTube-only (`suen:165`) | single-source |
| The student inherits the annotator's comma habit | same | Student comma P 46.6–47.7 / R 71.8–73.9 after YouTube training, against P 50.1–50.3 / R 48.2–55.0 from Wikipedia only; Qwen comma P 46.3 / R 72.7 (`suen:41`, `suen:143-153`) | single-source |

The margin is small: a tagger trained on Wikipedia alone is already within
0.9 F1 of the 72B annotator (72.7 vs 73.6). Znotins et al. propose the same
use, fine-tuned LLMs adding formatting to an existing 35-hour
orthographically transcribed corpus, as work in progress with human
verification to follow (`znotins:182-184`).

## What this does not show

- No comparison of a tagger and an LLM both trained on the same in-domain
  spoken data with full right context. Liu's LLM is zero-shot; Znotins's
  tagger is off-the-shelf; Woo's comparison is at two tokens of lookahead on
  TED talks with oracle sentence boundaries.
- No Vietnamese result, and no result for a tonal or syllable-spaced
  language other than Cantonese.
- Capitalization is measured only by Znotins et al.; the other four sources
  score punctuation only.
- No measurement of any of these models on a phone, on a CPU, or in memory.
  Pang's speeds are for a 13B model on unstated hardware.
- No rate of word changes for LoRA-tuned autoregressive LLaMA, and no rate
  for GPT-4 Turbo on SponSpeech; Liu and Beigi do not say how changed words
  were handled in scoring.
- Woo et al. evaluate on clean reference text only and say so (`woo:457`);
  Pang et al. also punctuate reference text, not recognizer output
  (`pang:200`).
- Suen's table has internal inconsistencies (a question-mark F1 of 71.7 from
  P 68.7 / R 70.2 at `suen:145`; an overall F1 of 69.4 from P 69.4 / R 67.2 at
  `suen:147`), so its second decimal should not carry a decision.
