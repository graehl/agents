# Localizing factual recall and editing an answer are different tests

Causal tracing and weight editing establish different facts about a language
model. The first asks which restored activations recover a prediction after a
specified corruption. The second asks where a parameter change can redirect
the prediction. Success at the second does not establish where the original
answer was computed.

In [*Locating and Editing Factual Associations in GPT*](https://arxiv.org/html/2202.05262v5)
(Meng, Bau, Andonian, and Belinkov; NeurIPS 2022), causal tracing corrupts
subject embeddings, then restores cached internal activations. The main
localization study covers 1,000 factual statements in GPT-2 XL (1.5B), with
additional traces in GPT-J (6B) and GPT-NeoX (20B). Middle-layer MLP
computations at the final subject token substantially restore factual
predictions. Their Rank-One Model Editing method, ROME, changes an MLP weight
matrix to insert a selected association; evaluations include paraphrases and
neighboring facts in GPT-2 XL and GPT-J. This supports a role for distributed
MLP computations in factual recall. It does not identify a unique neuron for
each fact.

[*Does Localization Inform Editing?*](https://arxiv.org/html/2301.04213)
(Hase, Bansal, Kim, and Ghandeharioun; NeurIPS 2023) tests the inference from
localization to editing in GPT-J on CounterFact. Per-example causal-tracing
strength poorly predicts successful rewriting; the layer chosen is much more
predictive. Several editing formulations are examined, including amplification
and erasure. One formulation relates to tracing, but layer identity remains
the stronger predictor. This bounds ROME's interpretation without disputing
that its edits change answers.

For a proposed “Colorado neuron,” distinguish evidence that an activation
mediates a Colorado-dependent answer from evidence that injecting it can make
the model discuss Colorado. The latter can be useful control without
explaining the original computation. A stronger localization claim needs
matched input contrasts, predictable interventions on held-out contexts, and
evidence about the upstream computation and downstream use.

Evidence status: author-reported experiments; the localization-to-editing
inference is contested by a separate study. Reading coverage: fetched primary
full texts, with main causal-tracing, editing, and counterevidence sections
inspected; not every appendix or implementation was audited. No experiments
were rerun for this survey.
