# Prompted encoder–decoder translation

An encoder–decoder can condition on target language, domain, style, and
example translations in its source stream. The decoder still generates
the translation autoregressively. The interface ranges from a forced
target-language token to natural-language instructions the encoder learned
to interpret.

## Language and domain tags

Johnson et al. used a source-side target-language token to control a single
multilingual GNMT encoder–decoder and demonstrated zero-shot directions.
MADLAD-400 uses the same interface idea in a Transformer. A WMT22 study of
mBART-large adds domain tags alongside language identifiers. Its Table 4
shows a tradeoff for the encoder-tag variant: mean BLEU rises from 6.80 to
21.72 on unseen combinations in the authors' single-domain multilingual
test, while falling from 41.40 to 37.25 on seen language/domain pairs against
single-domain training (`benchmark-reported`). A tag can request a domain
independently of the target language, including ones with little paired
in-domain text. [Johnson et al.](https://aclanthology.org/Q17-1024/)
· [Multilingual domain adaptation](https://aclanthology.org/2022.wmt-1.34/)

Garcia and Firat train mT5 to take a natural-language target name. The
unadapted model scores near zero BLEU on their initial translation probe.
The trained model can use some previously unseen dialect names, with small
gains on TED English→Canadian French and English→Taiwan Mandarin and flat
results on Brazilian Portuguese and mainland Mandarin (`single-source`).
[Garcia and Firat](https://arxiv.org/abs/2202.11822)

## raunak2024-instruction-nmt

Raunak et al. fine-tune a 225M Marian Transformer-Big for English→German
with delimited natural-language instructions before the source. Roughly 30
tasks cover formality, domain, terminology, length, literalness, and other
controls. The recipe mixes task supervision with plain bitext. Plain WMT20
chrF2 rises from 61.6 to 61.9. On the external IWSLT22 formality test,
formal/informal accuracy reaches 94.7%/98.5% versus 95.5%/95.0% for
zero-shot GPT-3.5-Turbo. Unseen combinations of individually trained
instructions sometimes work and sometimes fail. The evidence applies to a
trained family of controls in one translation direction (`benchmark-reported`).
[Paper, §§4–6](https://arxiv.org/html/2410.05553v1)
· [Local extract](../related-work/extract/raunak2024-instruction-nmt/html/2410.05553v1.md)

## Multilingual formality and gender

Jauregi Unanue et al. fine-tune NLLB-600M with special tokens for formality
and gender, then optimize contrastive preferences. On CoCoA-MT their
synthetic-preference model reaches 0.701 strict formality accuracy and
0.839 COMET, versus 0.674 and 0.839 for the corresponding Qwen3-8B arm.
Claude 3 Sonnet with 16 examples scores 0.703 and 0.863. On the harder
PREF-FAME-MT evaluation the synthetic-preference NLLB trails Qwen on both
metrics (0.501 vs 0.517 accuracy, 0.837 vs 0.850 COMET). The study
fully tunes NLLB and uses LoRA on Qwen. Preferences from original
contrastive data can trade translation quality for attribute accuracy, so
report both metrics (`benchmark-reported`). [EACL 2026](https://aclanthology.org/2026.findings-eacl.209/)

## Glossaries and translation memories

Dinu et al. train the encoder to use terminology supplied with the source.
This is learned lexical guidance. An application that requires exact terms
can also apply constrained decoding or verify the output. Xu et al. train a
Transformer to use retrieved translation-memory examples. These two inputs
vary per sentence and support controls beyond a fixed tag vocabulary. A
WMT25 study comparing retrieved examples and glossary constraints in OPUS
Transformers and Gemma 3 finds rankings that vary with the metric and the
kind of retrieval (`contested` for cross-system superiority).
[Terminology](https://aclanthology.org/P19-1294/)
· [Translation memories](https://aclanthology.org/2020.acl-main.144/)
· [WMT25 retrieval comparison](https://aclanthology.org/2025.wmt-1.20/)

Hy-MT2 supplies a current decoder-only reference for instruction following.
Its 1.8B dense checkpoint scores 69.36 on the authors' IFMTBench aggregate,
versus 83.14 for their 7B model. The benchmark covers glossary, style,
background context and formatting, among other controls. The reported table
does not include an encoder–decoder (`benchmark-reported`).
[Hy-MT2, Table 5](https://arxiv.org/html/2605.22064)

## luo2025-lamate

LaMaTE turns Llama 3 8B into the source and prompt processor. A small
bidirectional stack combines its representations and a separate shallow MT
decoder cross-attends to them. Table 4 reports 82.32 COMET for the full
model, 82.02 without the bidirectional stack, and 81.66 when the decoder
uses a prefix in place of cross-attention. The authors report 2.4–6.5×
inference speedups and 75% less KV cache versus Llama 3 8B in their setup.
Its total size remains above 8B, and mT5-large beats it in the low and
very-low resource bins of the multilingual comparison. This is evidence
for reusing a large pretrained model on the source side with a cheaper
autoregressive path (`single-source`). [ACL Findings 2025](https://aclanthology.org/2025.findings-acl.490/)
· [Local extract](../related-work/extract/luo2025-lamate/html/2503.06594v2.md)
