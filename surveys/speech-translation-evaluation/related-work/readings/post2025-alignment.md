**Source:** *Effects of Automatic Alignment on Speech Translation Metrics* — [PDF](https://aclanthology.org/2025.iwslt-1.7.pdf)

Extract: [`../extract/post2025-alignment/post2025-alignment.md`](../extract/post2025-alignment/post2025-alignment.md) (marker-pdf).

## 2026-11-24 — fable-5.2 — prose read in full; tables 3, 5, 7 not read cell by cell

Purpose: how much does re-cutting hypotheses to reference segments hurt a
neural metric. Followed from cettolo2026-sourceaware-st §3.2, which uses
this paper's tool for its first step.

### What it claims

- **The standard aligner** (Matusov et al. 2005, "AS-WER", shipped as the
  `mwerSegmenter` binary) is edit distance between the system's token
  stream and the concatenated reference, recombined at reference sentence
  ends; monotone (:61). Its core weakness is hypothesis tokens matching
  nothing in the reference at a boundary (:73); tokenization for unspaced
  scripts was unspecified (:75).
- **`mweralign`:** the original source, modernised, wrapped for Python,
  with built-in subword tokenization and a penalty for splitting a word
  across a reference boundary (:81–85).
- **Experiment is on text MT, not speech:** WMT24 system outputs in eleven
  language pairs, merged per domain and re-aligned, because no speech data
  has system-level human judgments collected by current conventions (:97,
  :119–121). Limitation stated (:304).
- **Scores move, rankings do not.** Re-alignment changes COMET-22 system
  scores much more than BLEU (:180), yet correlation of COMET-22 with human
  system rankings is "sometimes better, sometimes worse" than with the
  original segments and always far above BLEU on the original segments
  (:186, :236, :240). Tokenizer choice hardly matters (:182).
- **Prior dissent:** Macháček et al. 2023 recommended against
  `mwerSegmenter` with COMET, since neural metrics are trained on whole
  sentences (:39).

### Meaning for the purpose

Re-alignment noise is tolerable for system ranking with COMET-22, the
metric the source-aware paper found nearly source-blind. Absolute scores
on re-aligned output are not comparable to scores on given segments.

### Does not show

Speech systems; segment-level validity; a source-sensitive metric such as
MetricX.

### Leads

Macháček, Bojar and Dabre 2023, "MT metrics correlate with human ratings
of simultaneous speech translation" (IWSLT) — the dissent, unread.
