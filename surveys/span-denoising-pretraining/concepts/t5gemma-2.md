# T5Gemma 2 — UL2 adaptation of Gemma 3

> Read-backed digest (cluster: decoder-to-encoder-decoder adaptation, trust
> `single-source`; the authors evaluate their own Gemma 3 derivatives).

**Paper.** Zhang et al., “T5Gemma 2: Seeing, Reading, and Understanding
Longer,” arXiv technical report, 2025
([HTML](https://arxiv.org/html/2512.14856v2),
[PDF](https://arxiv.org/pdf/2512.14856v2),
[local extract](../related-work/extract/zhang2025-t5gemma2/html/2512.14856v2.md)).

## Mechanism

T5Gemma 2 applies the [T5Gemma adaptation](encoder-decoder-adaptation.md) to
Gemma 3, using UL2 only, with no distillation, on about 2T tokens with inputs
and targets of up to 16K tokens each. The text mixture has five denoisers, in
ratio 1:1:1:1:4:

| mean span | corruption rate | spans |
|---|---|---|
| 3 | 0.15 | many |
| 12 | 0.5 | many |
| 32 | 0.15 | many |
| 32 | 0.5 | many |
| \(\frac{3}{4}L\) | 0.75 | one |

The last denoiser is prefix-style continuation and carries half of the
mixture. Image data uses prefix language modeling only.

Two changes reduce parameters:

- **Tied embeddings.** The encoder input, decoder input and output softmax
  share one embedding table, a 10.5% parameter cut.
- **Merged attention.** Each decoder block uses one attention module over the
  concatenation of the decoder states and the encoder output, with a joint
  softmax, instead of separate self-attention and cross-attention. This cuts
  6.5% of parameters at a cost of about 0.3 points.

Applying cross-attention only on the global-attention layers lost 1.3 points
and was rejected. A frozen 400M SigLIP encoder feeds 256 image tokens to the
text encoder.

The released checkpoints are pretrained only: 270M-270M, 1B-1B and 4B-4B. The
paper's post-trained rows come from a light supervised distillation without
reinforcement learning, which the authors call a lower bound. 4B-4B holds
3.2B encoder and 3.2B decoder non-embedding parameters, 675M of embeddings and
the 417M vision encoder: about 7.5B in total, against about 4.3B for Gemma 3
4B. The per-token decode cost is comparable to the 4B decoder alone.

## Evidence

- **Multilingual and translation.** On WMT24++ (chrF, pretrained models) the
  gains are large at small sizes and vanish by 4B (`single-source`):

  | size | Gemma 3 | T5Gemma 2 |
  |---|---|---|
  | 270M | 18.3 | 26.9 |
  | 1B | 36.7 | 40.9 |
  | 4B | 48.4 | 49.2 |

  FLORES (pretrained) follows the same pattern: 39.2 vs 41.8 at 4B. After the
  light post-training, 4B-4B trails Gemma 3 4B IT, 46.5 vs 47.0 WMT24++ chrF;
  Gemma 3 IT also had reinforcement-learning post-training. For reference,
  T5Gemma (v1) reached 51.5 at 9B-9B pretrained.
- **Long context.** 4B-4B pretrained scores 81.7 on RULER 32K against Gemma 3
  4B's 66.8, despite pretraining on 16K sequences. Both T5Gemma (v1) models
  are near zero there (`single-source`).
- **Aggregate.** Pretrained 4B-4B is close to Gemma 3 4B: 60.8 vs 62.4 on
  the reasoning and factuality average, 33.2 vs 32.8 on STEM and code.
  Post-trained 4B-4B is ahead on most groups (`single-source`).
- **Objective.** At 1B-1B or below, UL2 alone beats PrefixLM+KD (39.8 vs 38.8
  at 1B-1B on the T5Gemma pretraining suite). Adding distillation to UL2
  helps by about 0.4 at 1B-1B but was dropped as too costly (`single-source`).

## Decision edge and limits

For translation, T5Gemma 2's own numbers show an advantage only below 4B.
At 4B, few-shot translation is at parity with Gemma 3 and the post-trained
model is slightly behind. The case for using it as an MT starting point
therefore rests on two untested claims: that the encoder-decoder fine-tunes
better on parallel data, and that its decode is cheaper. The paper fine-tunes
nothing on parallel text. Its parameter count also exceeds the matching Gemma
3 size, so a fair comparison should state both the parameter count and the
measured decode throughput.
