# Segment boundaries, pauses and limited right context

Grounded from fetched full text (2026-11-13). Every number below is from the
cited extract line; nothing is from recall. Map node: `../survey.md` (not yet
written when this page was created).

**Sources read** (full text, local extracts). Citations below use
`<key>:<lines>`, meaning lines of the extract file linked here.

- Behre, Tan, Varadharajan, Chang (Microsoft), 2022, *Streaming Punctuation
  for Long-form Dictation with Transformers* —
  [arXiv](https://arxiv.org/abs/2210.05756) · [PDF](https://arxiv.org/pdf/2210.05756) ·
  [extract](../related-work/extract/behre2022-streaming-dictation/behre2022-streaming-dictation.md)
  (`extract/behre2022-streaming-dictation/behre2022-streaming-dictation.md`, key `behre22`) ·
  [reading note](../related-work/readings/behre2022-streaming-dictation.md)
- Behre, Tan, Varadharajan, Chang (Microsoft), IJNLC 2022 / arXiv 2023,
  *Streaming Punctuation: A Novel Punctuation Technique Leveraging
  Bidirectional Context for Continuous Speech Recognition* —
  [arXiv](https://arxiv.org/abs/2301.03819) · [PDF](https://arxiv.org/pdf/2301.03819) ·
  [extract](../related-work/extract/behre2023-streaming-punct/behre2023-streaming-punct.md)
  (`extract/behre2023-streaming-punct/behre2023-streaming-punct.md`, key `behre23`) ·
  [reading note](../related-work/readings/behre2023-streaming-punct.md).
  This is the journal version of the 2022 paper: same systems, same result
  tables, plus one cross-segment context experiment.
- Woo, Kang, Kim, 2026, *Efficient Punctuation Restoration via Weighted
  Lookahead Scoring Method for Streaming ASR Systems* —
  [HTML](https://arxiv.org/html/2606.05179) · [PDF](https://arxiv.org/pdf/2606.05179) ·
  [extract](../related-work/extract/woo2026-lookahead-scoring/html/2606.05179.md)
  (`extract/woo2026-lookahead-scoring/html/2606.05179.md`, key `woo`) ·
  [reading note](../related-work/readings/woo2026-lookahead-scoring.md)
- Pang et al. (Meta), 2024, *LLaMA based Punctuation Restoration With
  Forward Pass Only Decoding* —
  [HTML](https://arxiv.org/html/2408.11845) · [PDF](https://arxiv.org/pdf/2408.11845) ·
  [extract](../related-work/extract/pang2024-llama-fpod/html/2408.11845.md)
  (`extract/pang2024-llama-fpod/html/2408.11845.md`, key `pang`) ·
  [reading note](../related-work/readings/pang2024-llama-fpod.md)
- Znotins, Gruzitis, Dargis, W-NUT 2025 (Latvian) —
  [PDF](https://aclanthology.org/2025.wnut-1.15.pdf) ·
  [extract](../related-work/extract/znotins2025-readable-text/znotins2025-readable-text.md)
  (`extract/znotins2025-readable-text/znotins2025-readable-text.md`, key `znotins`) ·
  [reading note](../related-work/readings/znotins2025-readable-text.md)
- Liu and Beigi, 2024 (SponSpeech) —
  [HTML](https://arxiv.org/html/2409.11241) · [PDF](https://arxiv.org/pdf/2409.11241) ·
  [extract](../related-work/extract/liu2024-sponspeech/html/2409.11241.md)
  (`extract/liu2024-sponspeech/html/2409.11241.md`, key `liu`) ·
  [reading note](../related-work/readings/liu2024-sponspeech.md)

## The failure: a pause-cut segment punctuated on its own

In Behre et al.'s production pipeline the recognizer cuts text into
segments, mainly at 500 ms of silence and otherwise at 40 seconds, and a
tagger punctuates each segment alone (`behre23:19-21`, `behre23:157`).
People dictating pause to think, so a segment often ends mid-sentence, and
any prefix of a sentence can look complete: "It can happen." / "It can
happen in New York." / "It can happen in New York City, right?"
(`behre23:78-87`). The tagger then puts a period at the segment end. The
paper's example is "I. Just have to share the view" (`behre23:268`). The
signature is sentence-boundary precision below recall.

| Claim | Setting | Numbers | Grade |
|---|---|---|---|
| Per-segment punctuation over-segments | Mixed long-form English set, transformer tagger, sentence-boundary metric (period and question mark merged, commas ignored) | In-segment context only: P 64, R 82, F1 72, F0.5 67 (`behre23:68`) | single-source, private data |
| Appending the previous segment as left context does almost nothing | same | P 64, R 84, F0.5 67; +0.4% relative F0.5 (`behre23:69`, `behre23:74`) | single-source |
| Appending the next segment as right context fixes most of it | same | P 80, R 69, F1 74, F0.5 78; +15.8% relative F0.5 (`behre23:70`, `behre23:74`) | single-source |

## Streaming re-punctuation with a dynamic window

**Scheme.** Keep a buffer of text for which no sentence boundary has been
found. When a new segment arrives, punctuate buffer plus segment together.
If the tagger places at least one sentence boundary inside the window, emit
every complete sentence and keep the remainder as the new buffer. The
recognizer's own segment ends are ignored; a sentence is finalized only once
the start of the next one has been seen (`behre23:91`, `behre23:99`).

**Models.** A 12-layer transformer tagger (16 heads, width 1024, feed-forward
4096) and a 1-layer LSTM tagger (512-dimensional embeddings, 1024 hidden
units) with a 4-word lookahead, both over 32k BPE units, trained on
paragraphs up to 250 BPE tokens (`behre23:159-161`). Baseline (BL) is
per-segment punctuation; streaming (ST) is the scheme above with the same
tagger.

**Test sets.** All start from audio and are long-form: 100 dictation
sessions averaging 180 s (Dict-100), 10 hours of earnings calls with
disfluencies removed from the reference (MAEC), 100 European Parliament
sessions (EP-100), and 20 hours of NPR podcasts averaging 15 minutes per
session (NPR-76) (`behre23:145-153`).

| Claim | Setting | Numbers | Grade |
|---|---|---|---|
| Streaming raises sentence-boundary precision at a smaller cost in recall | Dict-100, transformer | Boundary P 66 → 79, R 74 → 69, F0.5 67 → 77 (+13.8% relative) (`behre23:208-209`) | single-source, private data |
| Same direction on every set | transformer, boundary F0.5 | MAEC 70 → 78; EP-100 57 → 67; NPR-76 74 → 84 (`behre23:212-221`) | single-source |
| Average gains | four sets | Transformer: +13.9% boundary F0.5, +4.3% punctuation F1. LSTM with 4-word lookahead: +12.2%, +2.1% (all relative) (`behre23:173`) | single-source |
| The gain is in periods and question marks; commas do not move | Dict-100, transformer | Period F1 72 → 76 (P 69 → 81, R 76 → 71); question mark F1 64 → 82 (P 50 → 82, R 88 → 82); comma F1 59 → 59 (`behre23:188-189`) | single-source |
| A small LSTM with 4 words of lookahead also benefits, less | Dict-100 | Boundary F0.5 63 → 71; overall punctuation F1 61 → 62 (`behre23:186-187`, `behre23:206-207`) | single-source |
| Better boundaries help translation | EP-100 English audio to seven languages, Azure translator | Mean BLEU +0.66 (transformer), +0.33 (LSTM); German +1.1, Greek +1.4, French +0.1 (`behre23:179`, `behre23:227`, `behre23:237-246`) | single-source |

The absolute level stays modest after the fix: overall punctuation F1 is
67 on dictation, 66 on earnings calls, 62 on parliament and 75 on podcasts,
with comma F1 between 55 and 65 (`behre23:189-201`).

## How much right context is enough

| Claim | Setting | Numbers | Grade |
|---|---|---|---|
| With no right context a causal scorer fails; one subword token recovers most of it | IWSLT 2017 English (TED talks, clean text), LoRA-tuned Llama-3.2-1B used as a per-boundary scorer, \(K\) = subword tokens of lookahead | 4-class macro F1 / punctuation-only macro F1: \(K=0\) 0.646 / 0.543; \(K=1\) 0.927 / 0.909; \(K=2\) 0.937 / 0.920; \(K=3\) 0.935 / 0.918; \(K=4\) 0.930 / 0.911; \(K=5\) 0.932 / 0.914 (`woo:398-405`) | single-source |
| What the first token of lookahead fixes | same, confusion counts | Missed commas 5,046 → 2,466 → 2,010 for \(K=0,1,2\); commas where the reference has a period 935 → 33 → 15; periods where the reference has nothing 3,400 → 10 → 23 (`woo:416-449`) | single-source |
| An encoder at the same two-token lookahead | same; ELECTRA-small | comma 0.752, period 0.992, question 0.925 (`woo:276-291`) | single-source |
| A full next segment of right context, against none across the segment end | Behre et al., long-form audio | boundary F0.5 67 → 78 (`behre23:68-70`) | single-source |

Woo's numbers overstate what a short lookahead buys in deployment. The
prefix is reset at each reference sentence boundary and the lookahead is
truncated at the sentence end (`woo:60`, `woo:157`), so for \(K\ge 1\) an
empty lookahead identifies a sentence end. That is our reading of the
protocol; it explains the jump in period recall from 6,338 of 10,153 to
10,006 of 10,153 (`woo:420`, `woo:434`). The comma counts are not affected
by this and still improve with \(K\).

Woo et al. also relay, from Polacek et al., that one future word is
insufficient and a 4-word lookahead recovers most of offline quality for a
lightweight ELECTRA restorer (`woo:40`). That is a second-hand claim here;
the Polacek papers were not read for this page.

## Latency

No source read here reports a latency measurement.

- Behre et al. assert that the dynamic window adds no user-perceived
  latency because hypothesis buffers are still produced continuously
  (`behre23:99`). The design nevertheless delays the *final* punctuation of
  a sentence until the next sentence has begun (`behre23:157`); the size of
  that delay is not reported.
- Woo et al. bound the wait at \(K\) subword tokens per boundary by design
  and leave latency and memory measurement to future work (`woo:28`,
  `woo:457`).
- Pang et al. report throughput only: 1,760.30 tokens/s single-pass and
  959.1 tokens/s for the two-pass variant on 5-minute inputs, for a 13B
  model on unstated hardware (`pang:243`, `pang:288`).

## Long-form against short clips

- **Short single utterances are the easy case for per-segment
  punctuation.** Behre et al. say the two-stage setup "works well for
  single-shot use cases such as voice assistant or voice search" and fails
  on long-form dictation (`behre23:21`). No number accompanies the
  short-clip half of that statement.
- **Recognizers with built-in punctuation degrade on long input.** On 1.2k
  video utterances averaging 5 minutes, an RNN-T with 1B parameters scores
  F1 0.63 / 0.68 / 0.40 (question / period / comma) and Whisper large v2
  0.58 / 0.65 / 0.46 (`pang:262-270`, `pang:288`). Behre et al. report, as
  a preliminary observation without numbers, that end-to-end recognizers
  punctuate better out of the box but still over-segment (`behre23:280`).
- **A causal LM tagging in one pass loses commas, and feeding its own marks
  back helps most on long input.** Single-pass FPOD scores comma F1 0.66 on
  LibriSpeech-PC against 0.74 autoregressive; on the 5-minute set, comma
  0.63 single-pass and 0.87 with the second pass (`pang:227-243`,
  `pang:272-280`). The authors' explanation is that in one pass each
  prediction conditions on an unpunctuated history (`pang:134`). Long input
  is handled by a sliding window with padding (`pang:138`).
- **Short test sentences.** The Latvian test set averages 7.2 words per
  sentence (`znotins:64`), and the prompt describes inputs as under 30
  seconds (`znotins:91`). SponSpeech utterances are cut at reference full
  stops and question marks, 1.6 s minimum, 11.6 s mean, 45.0 s maximum
  (`liu:74`, `liu:128`), so every test utterance ends at a true sentence
  end and the hardest boundary decision is given away.

## Pauses as a cue

- In dictation, pauses mislead. Behre et al. argue that prosody-aware
  models "may cause regressions" where pauses do not correspond to
  punctuation, and their fix is text-only (`behre23:29`, `behre23:99`).
  They did not test a prosody-aware model; this is an argument, not a
  measurement.
- In conversational Latvian broadcast speech, 21 of 100 manually analysed
  mismatches could only be resolved by listening, and the authors conclude
  that pauses and intonation "remain a crucial signal" (`znotins:155`,
  `znotins:182`).
- On English podcasts, a model that adds acoustic embeddings to BERT
  (EfficientPunct) does not beat text-only BERT overall: 73.3 vs 75.4 F1
  (`liu:362-374`, `liu:390-402`). Details are on
  [spoken-vs-written](spoken-vs-written.md).

## What this does not show

- No latency in milliseconds or words for any scheme, and no measurement
  of how long a sentence stays unfinalized under the dynamic window.
- No behaviour of the dynamic window when the tagger never predicts a
  boundary (buffer growth) and no maximum-window rule; the 2022 and 2023
  papers do not discuss it.
- No test on short clips. The claim that per-segment punctuation suffices
  for single utterances is asserted, not measured.
- No comparison of the dynamic window against a fixed word lookahead on the
  same data; Behre's LSTM has a 4-word lookahead inside both baseline and
  streaming arms, so the two mechanisms are never separated.
- Behre's test data and two of four test sets are private, English only,
  from a hybrid recognizer; the paper gives relative gains for a system whose
  absolute comma F1 is 55–65.
- Woo's lookahead ablation is on clean TED text with oracle sentence
  boundaries, for a causal LM. It does not say how much lookahead a
  bidirectional tagger needs on unsegmented recognizer output.
- Nothing here covers capitalization under limited right context, or a
  language written without word-level case cues from the recognizer.
