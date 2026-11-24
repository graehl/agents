**Source:** *Evaluating Machine Translation Output with Automatic Sentence Segmentation* — [PDF](https://aclanthology.org/2005.iwslt-1.19.pdf)

Extract: [`../extract/matusov2005-mwersegmenter/matusov2005-mwersegmenter.md`](../extract/matusov2005-mwersegmenter/matusov2005-mwersegmenter.md) (marker-pdf).

## 2026-11-24 — fable-5.2 — abstract, sections 1–3.1 read; experiments not read

Purpose: the origin of re-cutting system output to reference sentences,
which every later paper in this survey uses.

### What it claims

- **Motivation:** scoring speech translation by forcing the recognizer to
  the human transcriber's segment times "does not reflect real-life
  conditions"; a real system segments automatically (:21).
- **Method:** align the whole candidate document to the reference
  document by Levenshtein distance and copy the reference's segment
  boundaries onto the candidate through the alignment (:78–82); extended
  to several references by padding them to equal segment length and
  recombining at segment ends (:84–92). The resulting score is called
  automatic-segmentation WER.
- **Why not score the whole document as one segment:** document-level
  BLEU, NIST and position-independent error rate match n-grams across
  unrelated sentences and come out too optimistic (:62, :74).
- **Headline:** metrics on the automatic segmentation correlate with
  human judgment at least as well as on manual boundaries (abstract :13;
  Chinese–English and Spanish–English, per post2025-alignment :39).

### Does not show

Anything about learned metrics or source text; the experiments section
was not read for this pass.
