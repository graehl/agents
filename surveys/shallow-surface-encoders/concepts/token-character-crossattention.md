# token-character-crossattention — a narrow character branch can matter

> Read-backed digest (cluster C, trust `single-source`). Strawberry studies a
> lightweight character branch coupled to a token model through cross-attention.

**Paper.** Cosma et al., “The Strawberry Problem: Emergence of Character-level
Understanding in Tokenized Language Models,” EMNLP 2025. **Full text:**
[ACL page](https://aclanthology.org/2025.emnlp-main.1434/) ·
[PDF](https://aclanthology.org/2025.emnlp-main.1434.pdf).

## Mechanism and evidence

A one-layer character transformer with intra-token positions exchanges
information with the token stream through block-causal cross-attention. The
character branch is about 1M parameters (dimension 256 versus token dimension
512). On synthetic character tasks, shrinking it to 12.5% of the main width
does not materially change learning curves; middle-layer fusion is strongest.

## Design edge and limits

This is current evidence that a narrow character module can change what a token
model learns without matching its width. The tasks are synthetic and
generative, not multilingual NER; repeated middle-layer fusion also defeats the
cheap cached-sidecar property. Use it as a later scale-up motif. Grade
`single-source`.
