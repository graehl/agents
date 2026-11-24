**Source:** *BLASER 2.0: a Metric for Evaluation and Quality Estimation of Massively Multilingual Speech and Text Translation* — [PDF](https://aclanthology.org/2024.findings-emnlp.943.pdf)

Extract: [`../extract/dale2024-blaser2/dale2024-blaser2.md`](../extract/dale2024-blaser2/dale2024-blaser2.md) (marker-pdf).

## 2026-11-24 — fable-5.2 — sections 1–3.3, conclusions and limitations read; filtering experiment skimmed

Purpose: the one metric that takes source audio directly; how good is
it. Followed from cettolo2026-sourceaware-st §2.2.

### What it claims

- **Design:** SONAR sentence embeddings of source (speech or text),
  translation and optional reference, combined by elementwise products
  and differences and fed to a three-layer perceptron that predicts an
  XSTS semantic-similarity rating, 1–5. 57 speech languages, 202 text;
  audio over 30 s excluded in training (:35–43).
- **On its own task** (SeamlessM4T human XSTS ratings, 123,260
  translations, 46 directions): item-level Spearman with humans averages
  45% (15–85%); 76% over modality × direction × system means (:80–84).
- **As a text metric:** WMT23 Metrics average correlation 0.711 against
  0.825 for the best metric and 0.696 for BLEU (:121). As QE it matches
  CometKiwi-22 at detecting hallucinations (:119).
- **Stated limits:** trained for accuracy only, not fluency (:205);
  inherits SONAR's blind spots and may favour SONAR-based systems (:207).

### Meaning for the purpose

A single pooled sentence vector per side is a much weaker reader than a
cross-encoder metric: on text it sits near BLEU. Its use is coverage
(speech in, no transcript) and coarse failures such as hallucination,
not fine ranking.

### Does not show

A comparison with ASR-then-text-metric on the same speech items.
