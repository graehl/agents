# Small multilingual translation systems

Decoder-only models dominate recent WMT submissions. Small encoder–decoders
still lead some multilingual evaluations, including a 3B system from Meta
and a 1.3B adaptation for English→Ladin and Ligurian. These comparisons
evaluate systems with different training recipes. They establish feasible
quality at a given scale and language mix.

## alastruey2026-omt

Meta's 3B OMT-NLLB starts with OmniSONAR, a multilingual encoder. The first
stage trains a decoder to reconstruct text from a pooled cross-lingual
representation using monolingual data. Later stages give the decoder
token-level cross-attention and train the full system on bitext. Of 114
languages added to the autoencoding stage in one ablation, 105 improved and
mean chrF++ rose by 5.20. This supports the use of monolingual data to
expand source coverage under this recipe (`single-source`).

Tables 9.2–9.3 report aggregate chrF++ by non-English resource tier and
direction (`benchmark-reported`). BOUQuET contains 275 languages as of the
paper. The FLORES+ table omits the 3B decoder.

| System | BOUQuET | FLORES+ |
|---|---:|---:|
| OMT-NLLB 3B | 36.6 | 50.9 |
| OMT-LLaMA 1B | 33.5 | — |
| OMT-LLaMA 3B | 36.2 | — |
| OMT-LLaMA 8B | 36.7 | 49.4 |
| NLLB-200 3.3B | 34.6 | 48.6 |
| TranslateGemma 27B | 33.9 | 43.8 |

The 3B encoder–decoder beats the 3B decoder-only model in both BOUQuET
direction aggregates (41.3 vs 41.0 into English, 31.9 vs 31.3 out) while
individual resource tiers trade places. Some unsupported targets use proxy
language codes in the evaluation. OMT-NLLB covers roughly 1,600 source and
250 target languages, while the OMT-LLaMA family generates in roughly 1,000
and supports richer prompting. The two branches differ in initialization,
objectives, target coverage and allocation of training data. The expected
quality on a particular language and direction is more useful than the
aggregate lead. [Extended paper, §§7 and 9](https://arxiv.org/html/2603.16309v3)
· [Local extract](../related-work/extract/alastruey2026-omt/html/2603.16309v3.md)

## nguyen2026-edward

EDWARD-NMT trains nested-width subnetworks in one encoder–decoder. Its
Transformer uses rotary positions, RMS and query/key normalization, SwiGLU
and tied embeddings. A shared expert runs for every token. A learned
translation-direction embedding conditions the shared expert and the
threshold for routing tokens to additional experts. Shrinking the width
changes the deployed checkpoint as well as the arithmetic per token.

In Tables 12–13, the six-layer XL variant reports 34.28 average BLEU on
OPUS-16 at 226M total and 128M active parameters, versus 33.31 for THOR-MoE
and 32.71 for Lingual-SMoE. Those are supervised English-centric comparisons
with published encoder–decoder baselines. The paper also covers a bilingual
multi-domain setting. This establishes a compact modern MoE encoder–decoder
point, with no matched pretrained decoder-only comparison (`benchmark-reported`).
[Paper](https://arxiv.org/html/2610.32115v1)
· [Local extract](../related-work/extract/nguyen2026-edward/html/2610.32115v1.md)

## Scaling MoE and shrinking the decoder

- **NLLB-200.** The 54.5B model uses sparse top-two routing in both stacks.
  The 600M and 1.3B distilled releases are dense. A separate pruning study
  reports 35.74 chrF++ for the full MoE, 35.46 with roughly 80% of experts
  pruned using language-specific statistics and 34.64 for the 3.3B dense
  baseline over 40,602 FLORES-200 directions. This distinction matters if
  a service can load a direction-specific subnetwork, but active weights
  alone do not determine resident memory (`single-source` for pruning).
  [NLLB](https://doi.org/10.1038/s41586-024-07335-x) · [Pruning](https://aclanthology.org/2023.acl-long.198/)
- TaskMoE routes the decoder by target
  language or pair. At 533M its task-level routing gained 1 BLEU over
  equal-sized token routing across 30 pairs. Lingual-SMoE uses a language
  shortlist before token routing. THOR-MoE gives the router token-level
  context and a soft language representation, contributing the strongest
  published baseline in EDWARD's depth-aligned OPUS-16 table. Each study
  compares routing interventions within its own recipe (`benchmark-reported`).
  [TaskMoE](https://aclanthology.org/2021.findings-emnlp.304/) · [Lingual-SMoE](https://proceedings.iclr.cc/paper_files/paper/2024/hash/3b4e1336f775c3dba16ebbb8d2afd258-Abstract-Conference.html) · [THOR-MoE](https://aclanthology.org/2025.acl-long.1040/)
- **kudugunta2023-madlad.** MADLAD-400 prepends a `<2xx>` target-language
  token to a dense, symmetric T5 encoder–decoder: the 3B and 10.7B models
  each have 32 encoder and 32 decoder layers (paper §4.1; both released
  configurations agree). It does not shrink the decoder. SMaLL-100 does,
  with a 12:3 encoder–decoder allocation at 330M, and reports +3.1 spBLEU
  and 2.5× inference speed over M2M100-418M in its evaluation. Speed
  depends on batch, lengths and serving implementation (`single-source`).
  [MADLAD paper](https://arxiv.org/html/2309.04662) · [3B configuration](https://huggingface.co/google/madlad400-3b-mt/blob/main/config.json) · [SMaLL-100](https://arxiv.org/abs/2210.11621)
  · [Local extract](../related-work/extract/kudugunta2023-madlad/html/2309.04662v1.md)

## Small systems win in both directions

- **gritta2026-afrislm.** TranslatePsy-AfriSLM tunes Qwen3.5 decoder-only
  checkpoints with curated and synthetic text for 19 Sub-Saharan African
  languages. The 2B beats dense NLLB 3.3B on all five metrics in each of
  the three benchmarks in Table 23. The chrF++ margins are +0.24 on
  FLORES-200, +2.06 on BOUQuET and +0.57 on SMOL. The 0.8B trails NLLB on
  FLORES-200 chrF++ by 1.45 but ties on SSA-COMET. A focused data recipe can
  outweigh broader coverage and larger size (`benchmark-reported`).
  [Paper, Appendix E.2](https://arxiv.org/html/2608.18655v2)
  · [Local extract](../related-work/extract/gritta2026-afrislm/html/2608.18655v2.md)
- **LiLa at WMT26.** Fully fine-tuned NLLB 1.3B beats the strongest
  attempted Gemma 4 E4B LoRA in the system paper's English→Ladin FLORES+
  (55.24 vs 50.40 chrF++), English→Ligurian FLORES+ (57.40 vs 55.35) and
  English→Ligurian BOUQuET (53.98 vs 49.89). The NLLB arm uses beam search
  and the Gemma arm samples. The submitted NLLB-based pipeline placed in
  human rank group 2–3 on English→Ligurian (`externally-evaluated` for
  that ranking). 27 of 30 WMT26 general-task submissions involved LLMs.
  The submission mix shows adoption under a document task with style and
  formatting instructions. [LiLa system](https://aclanthology.org/2026.wmt-main.60/)
  · [WMT26 findings](https://aclanthology.org/2026.wmt-main.48/)
- **Prefix masking.** In Gao et al.'s supervised bilingual comparison,
  separate encoder–decoder, causal single-stack and bidirectional-source
  single-stack obtain 34.9, 34.4 and 35.0 BLEU on WMT German→English. The
  bidirectional single stack also matches the separate-stack result when
  both have 36.9M parameters. Qu et al. find that prefix masking helps the
  causal decoder in supervised multilingual MT. Their two-stage decoder
  and contrastive instruction loss also improve unseen directions. A
  source can be bidirectional within a single stack (`benchmark-reported`).
  [Gao et al.](https://aclanthology.org/2022.aacl-main.43/) · [Qu et al.](https://aclanthology.org/2025.mrl-main.13/)

## Large models against TranslateGemma 27B

- **NLLB-54.5B MoE** beats TranslateGemma 27B on spBLEU in three of four
  direction groups on the 46-language FLORES+ comparison in the MiLMMT
  report. The unweighted average of the four published group scores is
  31.79 vs 30.74. TranslateGemma leads on reference-based XCOMET in all
  four, including 93.46 vs 86.86 from English and 87.31 vs 65.31 into
  Chinese. The ranking depends on the metric (`benchmark-reported`).
  [MiLMMT report, Table 1](https://arxiv.org/html/2608.10812#S3.T1)
- **MADLAD-400 10.7B** trails TranslateGemma 27B on Meta's BOUQuET
  aggregate (31.3 vs 33.9 chrF++) and FLORES+ aggregate (41.4 vs 43.8).
  It wins some resource bins. In an independent Finnish↔Northern Sámi
  evaluation, zero-shot MADLAD-10B beats TranslateGemma 27B in both
  directions on both test sets. For example, the UiT general test gives
  24.24 vs 8.61 BLEU into Finnish and 9.04 vs 4.47 BLEU into Sámi. These
  are direction-specific results (`benchmark-reported`).
  [OMT, Tables 9.2–9.3](https://arxiv.org/html/2603.16309v3#S9)
  · [Sälevä and Lignos, Tables 2 and 6](https://aclanthology.org/2026.loreslm-1.42/)

The survey located no recent public 10B-plus encoder–decoder with a broad
multilingual win over TranslateGemma 27B on learned quality metrics or
human judgments. Google's report compares against Gemma 3 on WMT24++ and
WMT25. The broad OMT comparison uses chrF++ and finds its strongest
encoder–decoder result at 3B, for a model with no public checkpoint found.
[TranslateGemma report](https://arxiv.org/abs/2601.09012)

## Checkpoint availability and terms

Checked 2026-11-20 using author publications, project links and public model
registries. The terms in this table apply to specific published weights.

| System | Availability and terms | Source |
|---|---|---|
| OMT-NLLB and OMT-LLaMA | No official public weights or weight license found. The paper is CC BY-SA 4.0 and links public evaluation assets. | [Meta publication](https://ai.meta.com/research/publications/omnilingual-mt-machine-translation-for-1600-languages/) · [Paper](https://arxiv.org/html/2603.16309v3) |
| NLLB-200 | Official dense and distilled weights are CC BY-NC 4.0. Meta also describes the 54.5B MoE release as noncommercial. | [600M](https://huggingface.co/facebook/nllb-200-distilled-600M) · [1.3B](https://huggingface.co/facebook/nllb-200-distilled-1.3B) · [3.3B](https://huggingface.co/facebook/nllb-200-3.3B) · [MoE release](https://doi.org/10.1038/s41586-024-07335-x) |
| WMT26 LiLa | NLLB-derived checkpoint available. The derivative card leaves licensing blank, and the base checkpoint is CC BY-NC 4.0. | [Ligurian checkpoint](https://huggingface.co/ConseggioLigure/nllb1.3B-eng-lij) · [NLLB base](https://huggingface.co/facebook/nllb-200-distilled-1.3B) |
| EDWARD-NMT, THOR-MoE, Lingual-SMoE | No official public checkpoints found for the multilingual comparisons above. | [EDWARD-NMT](https://aclanthology.org/2026.findings-emnlp.1763/) · [THOR-MoE](https://aclanthology.org/2025.acl-long.1040/) · [Lingual-SMoE](https://proceedings.iclr.cc/paper_files/paper/2024/hash/3b4e1336f775c3dba16ebbb8d2afd258-Abstract-Conference.html) |
| Prompted Marian 225M and attribute-controlled NLLB 600M | No public tuned checkpoint found for either experiment. The NLLB study releases code and data. Its base weights are CC BY-NC 4.0. | [Marian paper](https://aclanthology.org/2024.wmt-1.114/) · [Attribute control artifacts](https://github.com/inigo-jauregi/act-po) · [NLLB base](https://huggingface.co/facebook/nllb-200-distilled-600M) |
| MADLAD-400 3B and 10B, SMaLL-100 330M | Public MADLAD weights labeled Apache 2.0. SMaLL-100 weights labeled MIT. | [MADLAD 3B](https://huggingface.co/google/madlad400-3b-mt) · [MADLAD 10B](https://huggingface.co/google/madlad400-10b-mt) · [SMaLL-100](https://huggingface.co/alirezamsh/small100/tree/main) |
| Hy-MT2 1.8B and AfriSLM 2B | Public weights labeled Apache 2.0. | [Hy-MT2](https://huggingface.co/tencent/Hy-MT2-1.8B) · [AfriSLM](https://huggingface.co/qvac/TranslatePsy-AfriSLM-2B) |
| T5Gemma 2 and TranslateGemma | Public weights under the custom Gemma terms, with use and redistribution conditions. | [T5Gemma 2](https://huggingface.co/google/t5gemma-2-1b-1b) · [TranslateGemma](https://huggingface.co/google/translategemma-4b-it) · [Gemma terms](https://gemma.ai/resources/terms/) |
| LaMaTE | Public weights. The card says MIT and identifies Llama 3 8B as the base. Evaluate the upstream Llama terms too. | [LaMaTE](https://huggingface.co/NiuTrans/LaMaTE) · [Llama 3 terms](https://huggingface.co/meta-llama/Meta-Llama-3-8B/blob/main/LICENSE) |

## From-scratch comparison

The closest test for an architecture decision would hold multilingual
training and distillation data, tokenizer and control supervision fixed. It
would include a causal single stack, a bidirectional-prefix single stack,
and a separate bidirectional encoder with a shallow decoder. Quality
comparisons need target coverage and resource tiers at each operating point.
Training FLOPs, resident bytes and measured serving latency answer different
questions. Separately measuring them lets an encoder-heavy allocation compete
on its smaller per-target-token cost.

With independent initialization and suitable training data, the most direct
design test starts with the dense encoder-heavy model and a causal decoder.
Use identical target-language tokens and matched domain, style and glossary
examples so control supervision is shared. Add the prefix mask to isolate
bidirectionality and a sparse feed-forward variant to isolate expert routing.
The OMT source-side monolingual objective is a separate data ablation. This
uses the published designs without needing the research checkpoints.
