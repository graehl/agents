**Source:** *Evaluating the IWSLT2023 Speech Translation Tasks: Human Annotations, Automatic Metrics, and Segmentation* — [PDF](https://arxiv.org/pdf/2406.03881) · [arXiv](https://arxiv.org/abs/2406.03881)

Extract: [`../extract/sperber2024-iwslt23eval/html/2406.03881.md`](../extract/sperber2024-iwslt23eval/html/2406.03881.md)

## 2026-11-24 — fable-5.2 — prose read in full; correlation tables not read cell by cell

Purpose: what human evidence exists that text MT metrics stay valid for
speech translation once outputs are re-segmented. Followed from
cettolo2026-sourceaware-st §2.2.

### What it claims

- **Protocol.** Offline and multilingual IWSLT 2023 tasks give unsegmented
  talks; each system segments the audio itself. Hypotheses are re-cut to
  the reference sentences with `mwerSegmenter` (word-level for German,
  character-level for Chinese and Japanese), and *both* the metrics and
  the human raters see the re-cut segments (:108, :112, :243).
- **Raters get the neighbouring segments** of the system output, because a
  re-cut segment can start or end mid-sentence (:247). Source-based direct
  assessment, 0–100, 77 professional translators, text source shown, no
  audio (:241, :249).
- **Metrics track the human scores at system level.** chrF and COMET-22
  both correlate highly with direct assessment; COMET is higher wherever
  both are significant (:578–580). Conditions have only 2–20 systems, and
  many were far apart, which the authors say explains near-perfect
  correlations (:572, :578).
- **Human scores cross-check:** direct assessment correlates 0.95 with
  continuous rating by listeners of simultaneous en→de, and negatively
  with MQM error counts on en→ja (:586–590).
- **COMET is more brittle across conditions.** Pooled across domains or
  target languages, chrF against the newer references stays strongly
  correlated while COMET does not (:865).
- Systems include cascades and end-to-end; the paper raises, and does not
  test, whether metrics are biased between the two paradigms (:237).

### Meaning for the purpose

This is the human evidence the source-aware paper leans on: system-level
only, English source, three target languages, strong separation between
systems. It supports "re-segment, then use an MT metric" for ranking
well-separated systems and says nothing at segment level.

### Does not show

Segment-level metric validity; any comparison of source choices (COMET-22
was run; the extract does not say which source text it was given); a
direct-versus-cascade bias test.
