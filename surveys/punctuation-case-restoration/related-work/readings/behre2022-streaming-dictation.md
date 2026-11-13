**Source:** *Streaming Punctuation for Long-form Dictation with Transformers* — [PDF](https://arxiv.org/pdf/2210.05756) · [arXiv](https://arxiv.org/abs/2210.05756)

## 2026-11-13 — fable-5.2, full text

Purpose: choosing form, size and data for a Vietnamese case+punctuation
restorer for words-only phone ASR output. Line citations are to
`extract/behre2022-streaming-dictation/behre2022-streaming-dictation.md`.
The journal version,
[behre2023-streaming-punct](behre2023-streaming-punct.md), repeats every
result here and adds a cross-segment context study; read that note first.

### Claims

- **Problem.** Per-segment punctuation after pause-based segmentation works
  for single-shot voice search and fails for long-form dictation, where
  pauses fall mid-sentence (`:21`, `:51`).
- **Scheme.** A dynamic decoding window of unfinalized buffer plus the new
  segment; sentences are emitted only after a boundary is detected inside
  the window (`:62`). Decoder segment ends are discarded and boundaries are
  decided from text alone (`:68`).
- **Setup.** Baseline segments at 500 ms of silence, or 40 s; 12-layer
  transformer tagger (16 heads, width 1024) and 1-layer LSTM with 4-word
  lookahead; 32k BPE; training paragraphs up to 250 BPE tokens (`:124-128`).
- **Results** (identical to the journal version). Averages for the
  transformer: +13.9% sentence-boundary F0.5 and +4.3% punctuation F1,
  relative; LSTM +12.2% and +2.1% (`:142`). Dictation, transformer: boundary
  P 66 → 79, R 74 → 69, F0.5 67 → 77 (`:177-178`); question-mark F1 64 → 82,
  comma F1 59 → 59 (`:153-154`). Podcasts: boundary F0.5 74 → 84
  (`:190-192`).
- **Translation.** Mean BLEU +0.66 (transformer) and +0.33 (LSTM) over
  seven languages; German +1.1, Greek +1.4 (`:146`, `:198`).
- **Remark on end-to-end recognizers:** they punctuate better out of the
  box but still over-segment; no numbers (`:248`).

### Meaning for our purpose

Same as the journal version: on long-form input, re-punctuate across
endpointer cuts and finalize a sentence only after the next one starts;
expect the gain in periods and question marks, not commas. Nothing in this
version adds to that.

### What it does not show

- The context study that justifies right context over left context is only
  in the journal version.
- No latency measurement, no buffer bound, no prosody-aware comparison, no
  capitalization scores, English only, private dictation set, no variance.
- The extract's Table 4 is broken across two tables for the podcast rows
  (`:188-192`); the journal extract has the clean table.

### Leads worth fetching

- Shriberg, Stolcke, Hakkani-Tür, Tür 2000, *Prosody-based automatic
  segmentation of speech into sentences and topics* — the classical case
  for pause and prosody features that this paper argues against in
  dictation.
- Courtland, Faulkner, McElvain 2020, *Efficient automatic punctuation
  restoration using bidirectional transformers with robust inference*.
- Others as listed in the journal-version note.
