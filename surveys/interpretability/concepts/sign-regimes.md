# A positive SwiGLU output can have two different causes

For a gated MLP neuron, write its scalar activation as
\(a=\operatorname{SiLU}(g)v\). SiLU has the sign of its argument, so the
positive product contains both positive/positive and negative/negative inputs.
Recording only the product loses information about the computation. A negative
factor is a numerical sign, not a linguistic negation or necessarily a semantic
opposite.

Gerstner and Schütze's [*GLUScope*](https://arxiv.org/html/2602.23826)
(February 2026; [local extract](../related-work/extract/gerstner2026-gluscope/html/2602.23826.md))
records all four sign regimes, their frequencies, intermediate values, and
top examples. Its OLMo-7B-0424 neuron 31.9634 illustrates the cost of pooling:
negative/negative examples support an “again” interpretation even though the
strongest overall positive activations come from a different regime: the
positive extreme, 3.48, is positive/positive, while the negative/negative
activations reach at most 1.58 (the paper's §5). The tool
is evidence that sign-aware native-neuron investigation was already explicit
before Goodfire's October 2026 essay. It is not an exhaustive semantic audit of
OLMo or independent confirmation of Goodfire's Qwen claims.

The September successor [*Weakening Neurons*](https://arxiv.org/html/2609.18612v1)
(Gerstner, AlQuabeh, Inui, and Schütze; accepted EMNLP manuscript) studies
neurons whose input and output directions tend to oppose one another. It
includes conditional sign-regime ablations in OLMo-7B and Llama-3.2-3B,
compared with random neurons from corresponding layers. Negative-gate regimes
can materially affect outputs. Its limitations acknowledge that an upstream
ablation can alter downstream signs and hence which downstream interventions
occur; the intervention does not isolate every constituent mechanism.

These observations oppose treating a negative gate as simply inactive. They
also prevent conflating positive output with one homogeneous semantic role.
They do not imply that every sign regime has a clean label, that the two factors
always mean broad category and narrow subtype, or that removing negative-gate
activity improves a model.

For a candidate interpretation, compare quadrant-conditioned activity on held-out
natural prompts, then predict which regime-specific interventions should affect
which outputs. Failure of those predictions rejects the proposed role even if
the top examples look coherent. Evidence: `single-source` studies with related
authors, not independent replication. Reading coverage: primary main texts;
not all appendices. The original 2025 OpenReview version was inaccessible and
is not silently substituted for the September manuscript.
