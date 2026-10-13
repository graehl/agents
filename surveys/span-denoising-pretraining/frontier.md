# Frontier — span-denoising pretraining and encoder-decoder LLMs

Fresh, decision-relevant claims that are not yet settled enough for
[survey.md](survey.md) to teach as established. Each entry states the claim,
its regime, independent-check status, and what would change it.

## Adapted encoder-decoder LLMs fine-tune better on parallel data

- **Claim (implied, not tested).** T5Gemma and T5Gemma 2 report much larger
  gains after instruction tuning than before it. The open claim is that an
  adapted encoder-decoder also gains more than its decoder-only source when
  fine-tuned on one language pair's parallel data.
- **Regime.** Balanced 1B-1B and 4B-4B pretrained T5Gemma 2 checkpoints
  against Gemma 3 1B and 4B base, fine-tuned on the same bitext.
- **Status.** No source fine-tunes either family on parallel data. The only
  MT rows in the papers are few-shot or general instruction-tuned, and they
  show parity at 4B and a decoder-only lead in T5Gemma (v1).
- **Local untuned check (2026-10-13; eng→zho FLORES-200 devtest, N=1,012).**
  Setup: one five-shot prompt, greedy decoding.
  - T5Gemma 2 4B-4B beats Gemma 3 4B base: MetricX-24 2.12 vs 2.42, COMET-22
    0.867 vs 0.856, both p<.01 by paired bootstrap; BLEU 38.3 vs 36.2.
  - At 1B the gap is wider: MetricX 3.16 vs 4.16.
  - Against MADLAD-400 3B zero-shot, 4B-4B wins on both neural metrics
    (MADLAD MetricX 2.45, COMET 0.857) but loses on BLEU (MADLAD 39.1).
  - Decoding speed: 4B-4B matches Gemma 3 4B under Hugging Face batched
    generation, at 1.5× the peak memory.

  The few-shot architecture gap here is larger than the paper's +0.8 WMT24++
  chrF at 4B. This is a single-direction, untuned result: it narrows but does
  not answer the fine-tuning question.
- **Revisit when** a matched fine-tuning comparison exists, scored with a
  neural metric and paired bootstrap on a held-out test set. It should report
  parameters and measured decode throughput, not size labels.

## Encoder-decoder inference is cheaper per translated token

- **Claim.** RedLLM reports about 1.8× decoder-only inference throughput at
  8B and batch 1. The 2022 MT study finds encoder-decoders need fewer FLOPs at
  equal quality.
- **Regime.** Measured at batch 1 on TPU, or estimated as FLOPs; balanced
  depth.
- **Status.** `single-source` per paper. Batched GPU serving is not covered.
  Serving stacks such as vLLM support decoder-only models first: the
  0.29-series build checked locally on 2026-10-13 registers no T5Gemma
  architecture.
- **Revisit when** a batched serving benchmark compares an encoder-decoder
  with its decoder-only source at matched quality.
