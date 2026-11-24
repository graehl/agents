# Glossary: speech-translation evaluation

Terms as used under this survey directory.

| Term | Meaning here |
|---|---|
| speech translation (ST) | Speech in one language to text in another. |
| cascade | A recognizer followed by a text translator (MT model or LLM). |
| direct model | One model mapping speech to translated text with no transcript handed between components; includes Whisper, SeamlessM4T and OWSM in translation mode. |
| speech LLM | A text LLM given a speech encoder and adapter; a direct model whose decoder is a general LLM. |
| source-aware metric | A learned MT metric that takes the source text as well as hypothesis and reference (COMET, MetricX, xCOMET). |
| quality estimation (QE) | Scoring a translation from source and hypothesis with no reference. |
| stand-in source | Text given to a source-aware metric in place of a human transcript: an ASR transcript or a back-translation of the reference. The anchor paper says "synthetic source". |
| back-translation (BT) | Here: machine translation of each reference segment into the source language. |
| re-cutting (re-segmentation) | Reassigning a system's output tokens, or a source transcript's, to the reference's sentence segments so segment-level metrics can be computed. Text to text; no timestamps. |
| boundary refinement | The anchor paper's second step: moving the split between two adjacent re-cut source segments using cross-lingual word alignment or sentence embeddings. |
| WERnp / WERwp | The anchor paper's WER ignoring case, without / with punctuation as tokens. On re-cut text it charges both recognition errors and words placed in the wrong segment. |
| direct assessment (DA) | A 0–100 human rating of one translation; "source-based" when the rater sees the source and no reference. |
| XSTS | A 1–5 human rating of cross-lingual meaning similarity; BLASER's training target. |
