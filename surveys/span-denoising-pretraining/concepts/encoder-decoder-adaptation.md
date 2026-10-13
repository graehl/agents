# Encoder-decoder adaptation — T5Gemma

> Read-backed digest (cluster: decoder-to-encoder-decoder adaptation, trust
> `single-source`; the authors evaluate their own Gemma 2 derivatives).

**Paper.** Zhang et al., “Encoder-Decoder Gemma: Improving the
Quality-Efficiency Trade-Off via Adaptation,” arXiv 2025
([HTML](https://arxiv.org/html/2504.06225v1),
[PDF](https://arxiv.org/pdf/2504.06225v1),
[local extract](../related-work/extract/zhang2025-t5gemma/html/2504.06225v1.md)).

## Mechanism

Start from a pretrained decoder-only model and build an encoder-decoder whose
blocks are copies of it. The encoder is the decoder-only stack with causal
self-attention switched to bidirectional; each decoder block keeps the
original self-attention and feed-forward weights and gains a cross-attention
over the full encoder output. In a balanced pair (2B-2B, 9B-9B) the
cross-attention is initialized from the self-attention weights. In an
unbalanced pair (9B encoder, 2B decoder) it starts from scratch and is trained
alone for 1,000 steps before everything is unfrozen. All parameters are then
trained again on up to 2T tokens of the Gemma 2 pretraining data, either as
prefix language modeling with the original model's logits as a distillation
target (PrefixLM+KD, a 4,096/4,096 input/target split) or as UL2 denoising
(8,192/8,192). Instruction tuning then follows the Gemma 2 recipe.

The point of copying the decoder rather than training an encoder-decoder from
scratch is to inherit its knowledge cheaply. The unbalanced pair is the
efficiency lever: a large encoder reads the input once in parallel, while
the cost of each generated token is set by the small decoder.

## Evidence

- **Aggregate quality.** At matched size the adapted model scores about the
  same as the original before instruction tuning and clearly higher after it:
  2B-2B PrefixLM 49.7 vs Gemma 2 2B 47.9 on the pretraining suite, and 46.4
  vs 39.0 on the instruction-tuned suite. At 9B-9B the figures are 63.1 vs
  61.7 and 62.9 vs 59.6 (`single-source`).
- **Translation is the exception.** On WMT23 (5-shot, BLEURT, instruction
  tuned) the adapted models trail their decoder-only source: 2B-2B 59.9 vs
  Gemma 2 2B 65.2, and 9B-9B 71.1 vs Gemma 2 9B 72.0. The 9B-2B pair (65.3)
  only matches Gemma 2 2B. The authors flag this case explicitly as a task
  where the decoder-only model still wins (`single-source`).
- **Not just extra compute.** Training Gemma 2 2B on another 6T tokens
  reaches only 48.57 on the pretraining suite, below the adapted 49.7
  (`single-source`).
- **Bidirectional attention carries most of the gain.** A 2B-2B adaptation
  with a causal encoder scores 45.6 before and 41.7 after instruction tuning,
  4.1 and 4.7 points below the bidirectional one (`single-source`).
- **The objective sets the strength.** UL2 yields better encoder
  representations (higher SuperGLUE); PrefixLM+KD yields the better
  generator, by up to 3.6 points at 9B-2B. Averaging a PrefixLM model with a
  UL2 model fails; switching objective for the last 10% of training gives
  mixed results (`single-source`).
- **Adapting beats training from scratch** beyond about 100M parameters, even
  when the from-scratch encoder-decoder sees 8T tokens (`single-source`).
- **Latency.** On GSM8K at batch 1, 9B-2B runs at about Gemma 2 2B's latency
  with clearly higher accuracy, and the balanced pairs match their source's
  latency (`single-source`).

## Decision edge and limits

The paper supports adaptation as a cheap way to get a general-purpose
encoder-decoder that instruction-tunes well. It does not support a
translation-specific advantage. The one MT row favors the decoder-only model,
and no task is fine-tuned on parallel data. Within one model size, the
correlation between pretraining score and instruction-tuned score is weak
(Spearman \(\rho\) 0.42), so checkpoint choice needs downstream evaluation.
Successor: [T5Gemma 2](t5gemma-2.md).
