**Source:** *How to Evaluate Speech Translation with Source-Aware Neural MT Metrics* — [PDF](https://arxiv.org/pdf/2511.03295) · [arXiv](https://arxiv.org/abs/2511.03295)

Extract: [`../extract/cettolo2026-sourceaware-st/html/2511.03295.md`](../extract/cettolo2026-sourceaware-st/html/2511.03295.md)
(arXiv v3 HTML; the journal page at DOI 10.1162/COLI.a.627 returned 403).

## 2026-11-24 — fable-5.2 — full read of the body, tables skimmed

Purpose: explain the paper to graehl, pin down what the "7 WER points" from
boundary refinement measures, and decide what transfers to the speech
program's ASR→MT scoring. Line numbers below are in the extract.

### What it claims

- **Problem.** COMET and MetricX score a translation from (source text,
  hypothesis, reference). In speech translation the source is audio; a
  benchmark may have no transcript, or a transcript not segmented like the
  references (:18–22). IWSLT ranks by COMET without saying what source it
  feeds it (:18).
- **Two stand-in sources:** an ASR transcript of the audio, or a
  back-translation (BT) of the reference into the source language (:55–67).
- **Success criterion is agreement with the same metric fed the manual
  transcript**, as segment-level Pearson correlation, per system and
  language pair (:152–154). Human judgments enter only in §5.6.
  System-level rank correlation is above 0.99 for every method (:154), so
  the paper's differences are all at segment level.
- **Both stand-ins work.** MuST-C: COMET r > 0.99 always, MetricX ≥ 0.93
  but one case; Europarl-ST minima 0.978 (COMET), 0.888 (MetricX) (:190).
- **COMET-22 barely reads the source.** Fed a *shuffled* source it still
  correlates ≥ 0.979 with itself; MetricX-24-Hybrid-XL drops to as low as
  0.4185 (:202). The paper therefore analyses MetricX only from §5.2 on
  (:206).
- **ASR beats BT below 20% WER.** ASR wins 78.6% of ASR-vs-BT comparisons
  overall, 87.4% at WER ≤ 20%; above 20% BT wins 85.5% (:216). In the
  resegmented, automatically segmented setting: 61.2%, 74.7%, 85.5% (:1436).
  WER here is lowercase, no punctuation (:144, :1909).
- **Bias when the source comes from the system under test.** If the ASR
  source is the cascade's own ASR output (or the direct model's own ASR
  mode), correlation with the manual-source metric *drops*; for a cascade
  the metric "assesses the MT component rather than evaluating the whole
  pipeline" (:204). These cases are excluded from aggregates.
- **Direct versus cascade.** Six systems, three direct (Whisper, OWSM,
  SeamlessM4T in translation mode) and three cascades of the same models'
  ASR with MADLAD (:582–590). ASR sources win for both architectures,
  slightly more for direct (86% vs 74%; :216). Nothing in the method
  depends on the evaluated system's architecture: it only consumes the
  system's text output.
- **Human validation** (:1770–1780): Hearing-to-Translate, 304 items, five
  pairs, three systems (a cascade, SeamlessM4T v2, the SpeechLLM Voxtral).
  Pearson with direct-assessment scores, averaged over systems: COMET
  manual 0.5549, COMET with Whisper ASR 0.5614 (:1802, :1809); synthetic
  variants beat the reference-only variants and the three QE metrics. One
  margin is nil (COMET-BT 0.5474 vs COMET-ref 0.5471).

### The re-segmentation algorithm and the WER number

- **Why.** Systems translate automatically segmented audio (SHAS). The
  references are segmented by sentence. Hypotheses are already re-cut to
  the reference segments by minimum edit distance (Matusov et al. 2005;
  here the `mweralign` reimplementation, called L-Segmenter) — same
  language on both sides (:71). A source-aware metric also needs the
  *source* cut the same way, and an ASR transcript is in another language
  than the reference (:73).
- **Step 1, XL-Segmenter:** back-translate each reference segment into the
  source language, then run the monolingual edit-distance segmenter between
  the ASR transcript and that back-translation (:73).
- **Step 2, boundary refinement (XLR):** edit distance misplaces words at
  segment boundaries that have no surface match. For each adjacent pair,
  concatenate the two source segments, hold the reference split fixed, and
  choose the source split that minimises crossing word alignments
  (SimAlign over mBERT) or mean LaBSE cosine distance between each source
  half and its reference segment (:101–126).
- **What the WER measures.** Table 11 (:1026): segment-level WER of the
  re-segmented ASR transcript against the *manually segmented reference
  transcript*. A word placed in the neighbouring segment counts as a
  deletion in one and an insertion in the other, so this WER is
  recognition errors plus boundary misplacement. Refinement moves it "up
  to more than 7 absolute points (from WERnp=20.92 to 13.84 for
  Whisper/NLLB on Europarl-ST)" (:1259). The floor — the same ASR on
  manually segmented audio — is 10.40 there and 6.97 on MuST-C, against
  13.49 and 11.61 after refinement (:1265). So refinement recovers most,
  not all, of the misplacement; the residue is mostly source words the
  reference translation omitted (:1265).
- **No timestamps anywhere.** The alignment is text to text, for scoring
  only. It does not align output to audio regions.
- Cost: BT is "at least 2–8 times faster" than ASR plus re-segmentation
  (:2039).

### What it does not show

- That synthetic-source MetricX tracks *human* judgment at scale: 304
  items, and the manual-source metric itself reaches only ~0.55 (:1927).
- That the 7-point WER gain changes any metric score much: the downstream
  effect is a correlation staying above 0.92 (:1432). The in-the-wild
  correlation tables use only the refined (SimAlign) sources (:1428), so
  the paper never reports metric agreement with and without refinement.
- Anything about noisy or multi-speaker audio (:1929), unwritten languages
  (:1923), or metrics beyond COMET-22 and MetricX-24 (:1931).
- BT with a weak MT model, except one Bemba–English case (:1933).

### Leads

Sperber et al. 2024 (human scores for IWSLT 2023 after re-segmentation),
Post and Hoang 2025 (effect of the hypothesis aligner on metrics), Han et
al. 2024 (audio-input quality estimation), Papi et al. 2025 (the human
set used in §5.6), Dale and Costa-jussà 2024 (BLASER 2.0).
