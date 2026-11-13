**Source:** *Streaming Punctuation: A Novel Punctuation Technique Leveraging Bidirectional Context for Continuous Speech Recognition* — [PDF](https://arxiv.org/pdf/2301.03819) · [arXiv](https://arxiv.org/abs/2301.03819)

## 2026-11-13 — fable-5.2, full text

Purpose: choosing form, size and data for a Vietnamese case+punctuation
restorer for words-only phone ASR output. Line citations are to
`extract/behre2023-streaming-punct/behre2023-streaming-punct.md`. This is
the journal version of
[behre2022-streaming-dictation](behre2022-streaming-dictation.md); it adds
the cross-segment context study and an LSTM lookahead figure.

### Claims

- **Problem.** A recognizer cuts segments at 500 ms of silence (or at 40 s)
  and a tagger punctuates each segment alone; dictating users pause
  mid-sentence, so sentences are split and wrongly terminated (`:21`,
  `:78-87`, `:157`).
- **Context study** (mixed set, sentence-boundary metric): in-segment only
  P 64 / R 82 / F0.5 67; previous segment added as left context P 64 / R 84 /
  F0.5 67 (+0.4% relative); next segment added as right context P 80 / R 69 /
  F0.5 78 (+15.8%) (`:68-74`).
- **Streaming scheme.** Punctuate a window made of the not-yet-finalized
  buffer plus the new segment; emit complete sentences only when a sentence
  boundary appears inside the window; carry the rest forward (`:91`).
- **Taggers.** 12-layer transformer (16 heads, width 1024) and 1-layer LSTM
  (1024 hidden, 4-word lookahead), 32k BPE, four tags (comma, period,
  question mark, none), tag on the last BPE of each word (`:137`,
  `:159-161`).
- **Training data** is written-form paragraphs (52.8% OpenWebText, 31.5%
  Stack Exchange, 7.6% OpenSubtitles, 6.7% earnings calls, 1.4% NPR
  podcasts), stripped of punctuation and converted to spoken form with a WFST
  normalizer that keeps word alignments for the tags (`:119-123`,
  `:129-131`).
- **Results, transformer, baseline → streaming.** Sentence-boundary F0.5:
  dictation 67 → 77, earnings calls 70 → 78, parliament 57 → 67, podcasts
  74 → 84 (`:208-221`). Overall punctuation F1: 65 → 67, 65 → 66, 59 → 62,
  71 → 75 (`:188-201`). Averages: +13.9% boundary F0.5, +4.3% punctuation F1,
  relative (`:173`).
- **Per mark, dictation:** period P 69 → 81, R 76 → 71; question mark F1
  64 → 82; comma F1 59 → 59 (`:188-189`).
- **LSTM:** +12.2% boundary F0.5 and +2.1% punctuation F1 on average
  (`:173`).
- **Translation:** mean BLEU +0.66 over seven target languages (`:179`).
- Users are said to prefer precision over recall and sentence boundaries
  over commas, hence F0.5 on boundaries as the primary metric (`:171`).

### Meaning for our purpose

- If sherpa-onnx endpointing cuts long-form speech at pauses and each piece
  is restored alone, expect spurious sentence ends and capitals. The remedy
  costs no model change: re-run the tagger over carried-over text plus the
  new segment and finalize a sentence only once the next has started.
- Left context alone does not help the boundary decision; right context
  does. A unidirectional restorer needs lookahead or re-decoding.
- For short single utterances the per-segment setup is said to work
  (`:21`); the long-form path is where the buffer logic matters.
- The spoken-form training recipe (strip punctuation, normalize numbers to
  words, keep alignments) matches a recognizer that spells numbers out.
- The precision-weighted boundary metric is a reasonable primary metric for
  our evaluation as well.

### What it does not show

- No latency number; "no additional user-perceived latency" is asserted
  (`:99`), while final sentence output is delayed by design.
- No rule or measurement for a buffer that never closes.
- No prosody-aware comparison; the claim that pauses mislead rests on the
  baseline's behaviour, not on a test of an acoustic model.
- Absolute quality is low for a 12-layer model (comma F1 55–65, overall
  62–75), with training text only 15.7% speech-derived; no in-domain
  ablation.
- The dynamic window and a fixed word lookahead are never compared
  directly. English only, hybrid recognizer, two private test sets, no
  capitalization scores, no variance.
- One earnings-call reference set had disfluencies removed (`:149`).

### Leads worth fetching

- Behre et al. 2022, *Smart speech segmentation using acousto-linguistic
  features with look-ahead* (arXiv 2210.14446, reference [32]) — the segmenter
  side of the same system.
- Huang et al. 2022, *E2E Segmenter: joint segmenting and decoding for
  long-form ASR* (arXiv 2204.10749).
- Pappagari et al. 2021, *Joint prediction of truecasing and punctuation
  for conversational speech in low-resource scenarios* (ASRU) — joint case
  and punctuation, low resource.
- Żelasko et al. 2018, *Punctuation prediction model for conversational
  speech* (arXiv 1807.00543) — pause features on conversational data.
- Gale and Parthasarathy 2017, *Experiments in character-level neural
  network models for punctuation* (Interspeech).
