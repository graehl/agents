# Decoder-only vs encoder-decoder for supervised MT, trained from scratch

> Read-backed digest (cluster: MT architecture scaling, trust `single-source`;
> most comparisons are in figures, so few exact numbers survive in the
> extract).

**Paper.** Zhang, Ghorbani, Bapna, Cheng, Garcia, Shen and Firat, “Examining
Scaling and Transfer of Language Model Architectures for Machine
Translation,” ICML 2022
([HTML](https://arxiv.org/html/2202.00528v3),
[PDF](https://arxiv.org/pdf/2202.00528v3),
[local extract](../related-work/extract/zhang2022-mt-architectures/html/2202.00528v3.md)).

## Mechanism

The paper trains translation models from scratch on parallel data, with no
pretraining. It compares an encoder-decoder (EncDec) against single-stack
language-model variants that read the source and target concatenated:

- **PrefixLM:** bidirectional over the source, causal over the target.
- **CausalLM:** causal over everything, optionally with a source-side LM loss.
- **TopOnly:** the target attends to final-layer source states, as an EncDec
  does, instead of layer-by-layer.
- Each grown deeper or wider to match EncDec's parameter count.

Data are WMT14 En-Fr, WMT14 En-De, WMT19 En-Zh, an in-house web En-De corpus,
and OPUS-100, at up to about 412M non-embedding parameters.

## Evidence

- **Architecture matters most when small.** At small sizes, inductive biases
  that suit translation win: full source visibility, top-layer source
  encodings, and depth over width. As parameters grow, PrefixLM and EncDec
  converge to the same quality band, while CausalLM keeps a clear gap. The
  pattern holds across data regimes, test-set originality and sentence
  length (`single-source`; curves in figures).
- **Compute favors EncDec.** At equal quality, EncDec needs fewer FLOPs,
  though the gap narrows with scale. A decoder-only model gets no saving from
  sharing, because attention is quadratic over source plus target. EncDec
  also allows a shallow decoder for fast inference (`single-source`).
- **Supervised multilingual.** On OPUS-100 at about 412M parameters, EncDec
  beats the LM variants on supervised directions, most on low-resource and
  XX→En. PrefixLM comes within about 1 BLEU on average (`single-source`).
- **Zero-shot directions favor PrefixLM.** It sharply reduces off-target
  output (translating into the wrong language), even though its perplexity is
  worse than EncDec's. A source-side LM loss on CausalLM brings no gain and
  hurts low-resource transfer (`single-source`).
- **The authors' recommendation:** product systems for major language pairs
  and small on-device models should keep EncDec; LMs suit giant multilingual
  models aimed at zero-shot transfer.

## Decision edge and limits

This is the evidence behind the old default “an encoder-decoder for small,
supervised, single-pair MT”, and the authors state that default themselves.
It covers models without pretraining, at sub-billion scale. It does not
address the current question: whether a large multilingual LLM fine-tuned on
a pair beats an encoder-decoder built from the same LLM. The later work by
the same group ([RedLLM](encoder-decoder-scaling.md),
[T5Gemma](encoder-decoder-adaptation.md), [T5Gemma 2](t5gemma-2.md))
supplies that comparison with pretraining included, and on translation it
does not favor the encoder-decoder.
