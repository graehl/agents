# Span-denoising pretraining and encoder-decoder LLMs

> **Mode:** grounded field survey. **Coverage cutoff:** 2026-10-13.
> **Scope:** sequence-to-sequence denoising objectives (MASS, T5 span
> corruption, BART text infilling, the UL2 mixture), decoder-only infilling
> (fill-in-the-middle), the 2025 revival of encoder-decoder LLMs adapted from
> decoder-only checkpoints (T5Gemma, T5Gemma 2), and the architecture-scaling
> studies that bear on machine translation. `[G]` marks a fetched and read
> primary source; every concept page links its local Markdown extract.

## Decision summary

For machine translation (MT) with modern pretrained models, no source here
shows an encoder-decoder beating a matched decoder-only LLM:

- **Old models.** The 2019–2022 evidence favoring encoder-decoders for MT
  comes from models of 220M–412M parameters, either without pretraining or
  pretrained on English only.
- **Pretrained LLMs.** With multilingual pretraining at 1–9B parameters,
  every comparison goes the other way or ties. A from-scratch study trails on
  WMT. T5Gemma's adapted encoder-decoders trail their own Gemma 2 source on
  WMT23. T5Gemma 2 ties Gemma 3 at 4B on WMT24++ and wins only at 1B and
  below [G].
- **Untested.** No paper fine-tunes an adapted encoder-decoder LLM on
  parallel data against its decoder-only source. That is the comparison an
  MT practitioner needs ([frontier](frontier.md)).

The encoder-decoder LLMs' measured advantages lie elsewhere:

- higher instruction-tuned aggregate scores;
- better long-context retrieval (T5Gemma 2);
- stronger encoder representations for classification;
- an inference-FLOP lever, by pairing a large encoder with a small decoder.

The last applies to translation only if the decoder can be made smaller than
the source model without losing quality. Of the released checkpoints, only
T5Gemma (v1, 9B-2B) offers such an unbalanced pair. T5Gemma 2 ships only
balanced 270M-270M, 1B-1B and 4B-4B pretrained models [G].

On objectives, the T5 and UL2 ablations agree that, for a given architecture,
the masking recipe moves translation quality far less than the architecture
and the pretraining data do [G]. Span length and corruption rate matter for
understanding and in-context benchmarks, not WMT BLEU.

## Grounding and coverage

Nine primary full texts were fetched, read and distilled into concept pages.
The search started from the three objective-defining papers the question
named (T5, BART, UL2). It added MASS as the single-span precursor and FIM as
the decoder-only analogue. It followed T5Gemma and T5Gemma 2 back to their
from-scratch scaling study (RedLLM) and to the 2022 MT architecture study
both cite.

Not covered:

- multilingual variants (mT5, mBART, ByT5);
- dedicated MT models (NLLB, MADLAD-400);
- ELECTRA's replaced-token detection;
- GLM;
- Wang et al. 2022 on architecture and objective for zero-shot
  generalization (cited by T5Gemma, not fetched).

The MT-relevant region stopped adding new evidence after the 2025 adaptation
papers.

## Reading list

Each row gives the best introduction to its method: the original publication,
read as fetched.

| method | paper | concept page | local Markdown |
|---|---|---|---|
| MASS: one masked span, predicted by the decoder | Song et al., ICML 2019 | [mass](concepts/mass.md) | [extract](related-work/extract/song2019-mass/html/1905.02450v5.md) |
| T5: span corruption, text-to-text | Raffel et al., JMLR 2020 | [span corruption](concepts/span-corruption.md) | [extract](related-work/extract/raffel2020-t5/html/1910.10683v4.md) |
| BART: text infilling, full reconstruction | Lewis et al., ACL 2020 | [text infilling](concepts/text-infilling.md) | [extract](related-work/extract/lewis2020-bart/html/1910.13461v1.md) |
| UL2: mixture of denoisers | Tay et al., ICLR 2023 | [mixture of denoisers](concepts/mixture-of-denoisers.md) | [extract](related-work/extract/tay2023-ul2/html/2205.05131v3.md) |
| FIM: infilling for decoder-only | Bavarian et al., 2022 | [fill-in-the-middle](concepts/fill-in-the-middle.md) | [extract](related-work/extract/bavarian2022-fim/html/2207.14255v1.md) |
| MT architecture scaling from scratch | Zhang et al., ICML 2022 | [MT architecture scaling](concepts/mt-architecture-scaling.md) | [extract](related-work/extract/zhang2022-mt-architectures/html/2202.00528v3.md) |
| RedLLM: from-scratch LLM comparison | Zhang et al., 2025 | [encoder-decoder scaling](concepts/encoder-decoder-scaling.md) | [extract](related-work/extract/zhang2025-redllm/zhang2025-redllm.md) |
| T5Gemma: adapting a decoder LLM | Zhang et al., 2025 | [encoder-decoder adaptation](concepts/encoder-decoder-adaptation.md) | [extract](related-work/extract/zhang2025-t5gemma/html/2504.06225v1.md) |
| T5Gemma 2 | Zhang et al., 2025 | [T5Gemma 2](concepts/t5gemma-2.md) | [extract](related-work/extract/zhang2025-t5gemma2/html/2512.14856v2.md) |

## Concept map

### One family: corrupt the input, predict what is missing

Every objective here is “noise the text, train the model to undo it”. They
differ in what is noised and in what the model must emit. UL2 makes that
explicit by writing each as span corruption with a mean span length, a
corruption rate and a span count [G].

| objective | noise | model emits | nearest confusable |
|---|---|---|---|
| BERT masked LM | 15% of single tokens | the masked tokens, independently, from an encoder | MASS at \(k=1\) |
| causal LM | everything after position \(t\) | the next token, left to right | MASS at \(k=m\); UL2 S-denoiser |
| MASS | one contiguous span, about 50% of the sentence | that span, left to right, from a decoder that cannot see the rest | T5 with a single long span |
| T5 span corruption | 15% of tokens in spans of mean length 3, each replaced by a sentinel | only the dropped spans, each led by its sentinel | BART text infilling |
| BART text infilling | spans of Poisson(3) length, each replaced by one unlabeled [MASK], plus sentence permutation | the whole original text | T5 span corruption |
| UL2 | a mixture: T5-like (R), long or dense spans (X), prefix continuation (S), selected by a mode token | the dropped spans or the continuation | a weighted multi-task mix of the above |
| FIM | one cut, reordered to prefix, suffix, then middle | the middle, left to right, in a decoder-only model | T5 or MASS with one span |

“Masking and reproducing” is the special case of noising and denoising in
which the noise is deletion or replacement of spans [G]. BART also tried
noise that deletes nothing: sentence permutation and document rotation. On
their own both were poor; rotation dropped SQuAD to 77.2 [G].

### Why a separate encoder and decoder

An encoder reads the whole input with bidirectional attention once. A decoder
generates with causal attention plus cross-attention to the encoder states.
When input and output differ, as in translation, summarization or
span-filling, this separates understanding the input from producing the
output. It also lets the two stacks have different sizes.

MASS's design argument is that the decoder should be forced to use the
encoder: mask the decoder's view of everything the encoder can see [G]. For
masked-LM-style training this answers why an MLM would want a decoder at all.
A separate decoder turns “fill in tokens” into generation, so the same
pretrained network can be fine-tuned for sequence-to-sequence tasks without
an untrained decoder bolted on.

Decoder-only models reach most of the same behavior without a second stack:

- **Prefix LM:** bidirectional attention over the input [G].
- **FIM:** infilling through data reordering [G].
- **Bidirectional input mask at fine-tuning:** in RedLLM, giving the
  decoder-only model a bidirectional mask over its input at fine-tuning beat
  the encoder-decoder in 9 of 10 instruction-tuned table cells [G].

### Encoder-decoder LLMs by adaptation

Training a large encoder-decoder from scratch is expensive and, at matched
compute, loses to a decoder-only model in pretraining [G]. T5Gemma instead
copies a pretrained decoder-only model into both stacks:

1. Make the encoder's attention bidirectional.
2. Add cross-attention in the decoder.
3. Continue training on about 2T tokens of the original pretraining data.

Adaptation beats more decoder-only training and beats from-scratch
encoder-decoder pretraining beyond about 100M parameters [G]. T5Gemma 2
repeats the recipe on Gemma 3 with UL2. It ties all embeddings and merges
the decoder's self- and cross-attention into one module, and adds a frozen
vision encoder [G].

## Machine translation: what the evidence says

- **Small models trained from scratch.** EncDec ≥ PrefixLM > CausalLM, with
  the gap narrowing as models grow; EncDec is cheaper per unit of quality.
  The authors recommend EncDec for major-pair products and small on-device
  models [G]
  ([MT architecture scaling](concepts/mt-architecture-scaling.md);
  `single-source`).
- **T5 at 220M, English-only pretraining.** The encoder-decoder beats prefix
  LM and causal LM on WMT validation BLEU at equal FLOPs: EnFr 39.82 vs 37.98
  vs 35.28. T5-11B still trailed back-translation and cross-lingual systems on
  WMT test sets [G] ([span corruption](concepts/span-corruption.md);
  `single-source` and `benchmark-reported`).
- **From-scratch LLMs to 8B (RedLLM).** The decoder-only model leads on WMT
  chrF before and after instruction tuning, and also at matched inference
  FLOPs [G] ([encoder-decoder scaling](concepts/encoder-decoder-scaling.md);
  `single-source`, chart-read).
- **Adapted from Gemma 2 (T5Gemma).** On WMT23 (instruction tuned, BLEURT),
  2B-2B scores 59.9 vs Gemma 2 2B's 65.2, and 9B-9B 71.1 vs 72.0. This is the
  only task the authors flag as still favoring decoder-only [G]
  ([encoder-decoder adaptation](concepts/encoder-decoder-adaptation.md);
  `single-source`).
- **Adapted from Gemma 3 (T5Gemma 2).** On WMT24++ chrF (pretrained) the
  encoder-decoder gains at 270M (+8.6) and 1B (+4.2) and ties at 4B (+0.8).
  After light post-training, 4B-4B is 0.5 behind Gemma 3 4B IT [G]
  ([T5Gemma 2](concepts/t5gemma-2.md); `single-source`).
- **Monolingual denoisers need help for MT.** BART improved RO→EN by about
  1.2 BLEU only with an extra source encoder and back-translation, and
  overfit without back-translation [G]
  ([text infilling](concepts/text-infilling.md); `single-source`).

## Contested results

- **Is the encoder-decoder better for translation?** Yes at 2019–2022 scale
  without multilingual LLM pretraining (T5, the 2022 MT study). No or tie
  with it (RedLLM, T5Gemma, T5Gemma 2). The disputed axes are pretraining
  data and model scale. All the later evidence comes from one Google group
  evaluating its own models (`contested`).
- **UL2 vs prefix LM as the adaptation objective.** T5Gemma found PrefixLM
  with distillation the better generator, by up to 3.6 points at 9B-2B. T5Gemma 2
  found UL2 better at 1B and below and dropped distillation. The authors
  attribute the difference to teacher and student capacity (`contested`,
  same authors).
- **The size of UL2's gain.** Its “+43.6% over T5” is a normalized average
  driven by one-shot and perplexity columns where baselines sit near zero. On
  fine-tuned SuperGLUE the encoder-decoder gain is 73.10 vs 72.00, and at
  about 1B UL2 loses to T5 on fine-tuned SuperGLUE (83.3 vs 84.7) [G].

## Negative / quiet results

- **Averaging PrefixLM and UL2 checkpoints** gave similar or much worse
  results. Switching objective for the last 10% of training was mixed [G].
- **Cross-attention on global layers only** (T5Gemma 2) lost 1.3 points and
  was rejected [G].
- **Converting grouped-query attention to multi-head attention in the
  encoder** raised pretraining score by 0.5 but cut instruction-tuned score
  by 2.9 [G].
- **A source-side LM loss on causal decoder-only MT** brought no gain and
  hurt low-resource transfer [G].
- **Retrofitting FIM by fine-tuning** needed 50% extra tokens at full learning
  rate to match FIM pretraining [G].
- **MASS-style single-span objectives** did not survive: BART found them
  weaker for understanding, and no current LLM uses them [G].

## Baseline sensitivity

- **T5's encoder-decoder advantage** depends on counting 2P parameters as
  equal compute to a P-parameter decoder. At equal parameters the shared
  encoder-decoder's EnRo lead over prefix LM is within noise [G].
- **Post-training recipes differ between the two papers.** In T5Gemma both
  architectures get the same Gemma 2 recipe: supervised fine-tuning, then RL
  from human feedback. In T5Gemma 2 the encoder-decoder gets only a light
  distillation pass, while Gemma 3 IT had full post-training. The authors
  call the post-trained T5Gemma 2 rows a lower bound, so its 0.5 chrF
  translation deficit at 4B is not a matched comparison [G].
- **RedLLM's instruction-tuned parity** disappears against the strongest
  decoder-only control: the same model with a bidirectional mask over its
  input at fine-tuning [G].
- **Parameter count.** T5Gemma 2 4B-4B has about 7.5B parameters including
  embeddings and the vision encoder, against about 4.3B for Gemma 3 4B. “4B”
  comparisons match the decoder, not the deployed size [G].

## Disconfirming pass

For the headline claim “encoder-decoders are the better MT architecture”, the
search looked for results that bound or refute it, not restatements. It
found the WMT23 row where T5Gemma trails Gemma 2, RedLLM's WMT curves, and
T5Gemma 2's 4B parity. For “adapted encoder-decoders fine-tune better”, it
looked for any parallel-data fine-tuning result and found none. Each paper's
own MT numbers and its stated limitations were also checked.
