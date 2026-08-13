# byte-ssm — recurrent-state alternative for long byte streams

> Read-backed digest (cluster F, trust `single-source`). MambaByte replaces
> attention over long byte sequences with a selective state-space model.

**Paper.** Wang et al., “MambaByte: Token-free Selective State Space Model,”
arXiv 2401.13660. **Full text:**
[HTML](https://arxiv.org/html/2401.13660) ·
[PDF](https://arxiv.org/pdf/2401.13660).

## Mechanism and evidence

The causal byte model maintains a fixed recurrent state at inference, avoiding
quadratic attention and tokenization. The paper reports competitive language
modeling and strong robustness to character noise relative to tested
token/byte baselines.

## Design edge and limits

A state-space block becomes relevant if a later character sidecar is dominated
by very long byte sequences or needs streaming operation. The live redaction
case is bidirectional, token-aligned, and short enough for a small convolution
or local-attention block. No encoder-only multilingual NER evidence is supplied.
Grade `single-source`.
