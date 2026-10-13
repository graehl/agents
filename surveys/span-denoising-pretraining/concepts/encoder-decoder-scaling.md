# Encoder-decoder vs decoder-only at scale — RedLLM

> Read-backed digest (cluster: decoder-to-encoder-decoder adaptation, trust
> `single-source`). The extract garbled one scaling table; those exponents
> were read from the fetched HTML source. Translation values are read
> approximately from a chart.

**Paper.** Zhang, Cheng, Shakeri, Wang, Ma and Firat, “Encoder-Decoder or
Decoder-Only? Revisiting Encoder-Decoder Large Language Model,” arXiv 2025
([HTML](https://arxiv.org/html/2510.26622v1),
[PDF](https://arxiv.org/pdf/2510.26622v1),
[local extract](../related-work/extract/zhang2025-redllm/zhang2025-redllm.md)).
The arXiv comment calls it “the scaling study inspiring T5Gemma”; the paper
body does not mention T5Gemma.

## Mechanism

The paper trains both architectures from scratch under one recipe, sizes 150M
to 8B. The decoder-only model (DecLLM) uses causal LM. The encoder-decoder
(RedLLM) uses prefix LM: each 2,048-token sequence is split into a 1,024-token
input and a 1,024-token target. Encoder and decoder have equal depth, with
rotary positions on all attention and fully tied embeddings.

- **Data.** RedPajama V1 (about 1.6T tokens, 32K vocabulary), then FLAN
  instruction tuning.
- **Compute accounting.** Models are compared by parameter count and by
  training FLOPs, not by the older convention of giving the encoder-decoder
  twice the parameters. At equal parameters, DecLLM spends about twice the
  training FLOPs per example.

## Evidence

- **Pretraining.** Against parameters, DecLLM scales better. Against training
  FLOPs the curves nearly overlap, and DecLLM owns the compute-optimal
  frontier as compute grows. Pretrained RedLLM trails clearly on zero- and
  few-shot downstream averages, even at matched perplexity. Few-shot at 8B is
  35.13 vs 43.37 (`single-source`).
- **After instruction tuning.** RedLLM is about level at equal parameters,
  59.69 vs 58.26 zero-shot at 8B, and nearly dominates when quality is
  plotted against inference FLOPs. DecLLM fine-tuned with bidirectional
  attention over its input beats RedLLM in 9 of the 10 table cells: 63.03 at
  8B zero-shot (`single-source`).
- **Throughput.** At 8B and batch 1, RedLLM's inference throughput is about
  1.8× DecLLM's (chart-read, `single-source`).
- **Length extrapolation.** DecLLM is stable to twice its training length and
  then diverges. RedLLM degrades more smoothly but is often worse below 4K
  tokens (`single-source`).
- **Translation** (WMT En–De and En–Zh chrF, chart-read). Decoder-only leads
  throughout:
  - Pretrained few-shot at 8B: about 38.5 vs 29.5.
  - After instruction tuning, few-shot at 8B: about 37 vs 31.5.
  - Matched inference FLOPs: DecLLM-4B (about 34) is still above RedLLM-8B
    (`single-source`).

  The corpus's language mix is not characterized, and with a 32K vocabulary
  it is probably English-heavy.

## Decision edge and limits

This is the cleanest from-scratch architecture comparison in the survey, and
for translation it favors decoder-only. The instruction-tuning advantage is
what [T5Gemma](encoder-decoder-adaptation.md) set out to inherit cheaply by
adaptation. The bidirectional-input decoder-only control sets the bar: a gain
credited to the encoder must beat a decoder-only model given a bidirectional
mask over its prompt at fine-tuning time. Only balanced depth, one objective
pair, and sizes up to 8B were tested.
