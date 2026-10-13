# UL2 — a mixture of denoisers with mode tokens

> Read-backed digest (cluster: mixture of denoisers, trust `single-source`;
> English-only pretraining, no translation ablation).

**Paper.** Tay et al., “UL2: Unifying Language Learning Paradigms,” ICLR 2023
([HTML](https://arxiv.org/html/2205.05131v3),
[PDF](https://arxiv.org/pdf/2205.05131v3),
[local extract](../related-work/extract/tay2023-ul2/html/2205.05131v3.md)).

## Mechanism

UL2 writes every objective as span corruption with three parameters: mean
span length \(\mu\), corruption rate \(r\) and number of spans \(n\). Causal
LM is one span covering everything (\(\mu=L, r=1, n=1\)). Prefix LM is one
span that must run to the end of the sequence. Within that family, training
mixes three kinds of denoiser:

| denoiser | settings | what it trains |
|---|---|---|
| R (regular) | T5-style, \(\mu\) 3 or 8, \(r=0.15\) | knowledge-heavy local fill-in |
| X (extreme) | \(\mu\ge 12\) or \(r\ge 0.3\); here \(\mu\) 3, 8 or 64 at \(r=0.5\), or \(\mu=64\) at \(r=0.15\) | long generation from little context |
| S (sequential) | prefix LM, one span covering the last part | continuation, the in-context and few-shot regime |

A paradigm token, [R], [X] or [S], is prepended in pretraining, and the user
picks one at fine-tuning or prompting time (“mode switching”).

**Masking/reproducing vs noising/denoising.** These name one thing at two
levels of generality. Masking spans and having the model reproduce them is
one kind of noise. UL2's contribution is to parameterize the noise so that
MLM-like, T5-like and LM-like objectives are points in one space, then train
on a mixture. The bidirectional-context vs left-to-right choice becomes a
mixing weight instead of an architecture decision.

## Evidence

- **Compute-matched ablations** at small scale (encoder-decoder 335M vs
  decoder 167M, about 32B C4 tokens). On fine-tuned SuperGLUE, UL2 on an
  encoder-decoder gets 73.10 against 72.00 for T5 span corruption and 69.30
  for prefix LM. One-shot XSum is 11.51 against T5's 7.49. The
  “+43.6% over T5” headline is a normalized average dominated by one-shot
  and perplexity columns where baselines are near zero (`single-source`).
- **Denoiser over architecture.** UL2 helps both backbones; the decoder arms
  used here are prefix-LM decoders. The authors find the denoiser choice
  matters more than the architecture, yet still recommend encoder-decoders
  unless parameter storage is the constraint (`single-source`).
- **The S denoiser carries in-context ability.** Removing S lifts
  fine-tuned SuperGLUE to 73.7 but drops one-shot XSum to 2.6. X alone is
  insufficient (`single-source`).
- **At about 1B parameters** UL2 loses fine-tuned SuperGLUE to T5 (83.3 vs
  84.7) while being 2–4× better in context (`single-source`).
- **20B.** Zero-shot SuperGLUE 63.0 vs GPT-3 175B's 61.2. Fine-tuned
  SuperGLUE 90.7 vs T5-11B's 89.9. The 20B run had unmitigated loss spikes,
  and fine-tuning was stopped per task once it hit the state of the art
  (`single-source`).
- **Translation.** There is no MT ablation. The only MT number is a WMT19
  De→En human-evaluation score of 67.0 against a best of 71.0, using English-only
  C4 pretraining with no German data or back-translation (`single-source`).

## Decision edge and limits

UL2 is the objective that [T5Gemma 2](t5gemma-2.md) uses to turn Gemma 3
into an encoder-decoder. It also explains why that model still prompts like
an LM: half its mixture is the S (prefix) denoiser. It gives no evidence
about translation, and its released 20B model used different mode tokens.
For a decoder-only model the analogous move is
[fill-in-the-middle](fill-in-the-middle.md): add infilling to the data, not
the architecture.
