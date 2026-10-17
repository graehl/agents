# A convincing neuron description must survive counterexamples

A description inferred from strongly activating examples is a hypothesis about
a neuron's selectivity. Treating it as a functional explanation adds a second
claim: the neuron participates causally in computations that depend on that
concept. These claims require different tests.

[*Rigorously Assessing Natural Language Explanations of Neurons*](https://arxiv.org/html/2309.10312)
(Huang, Geiger, D'Oosterlinck, Wu, and Potts;
[BlackboxNLP 2023](https://aclanthology.org/2023.blackboxnlp-1.24/)) audits
GPT-4-generated descriptions of GPT-2 XL (1.5B) neurons. Across 300 highly
scored explanations, its observational audit reports precision 0.64 and recall
0.50. The causal study groups descriptions concerning numbers, verbs, temporal
expressions, and locations, covering approximately 80,000 descriptions. It
tests tasks such as unit conversion, tense, and capital retrieval through
interchange interventions. Neurons selected by explanation confidence perform
approximately like random selection on most tasks; a token-activation
correlation baseline is stronger. Numerical-expression explanations exceed
random selection but remain below that baseline.

The distinction matters when interpreting the result. The audit challenges a
particular automatic-description method and its confidence score. It does not
show that every inspected neuron lacks a useful interpretation, or that an
investigation using longer contexts, counterexamples, and causal experiments
must fail. Nor does a failed intervention on one task prove that a neuron never
uses the described information elsewhere.

For “almost one thing only,” an operational hypothesis should predict both
positive and negative cases. A putative Colorado-context neuron should be
tested on Colorado without hiking, hiking outside Colorado, unfamiliar
Colorado references, and comparable punctuation in unrelated text. These
contrasts separate semantic context from co-occurring words and token position.
Only after freezing that interpretation should new examples assess whether it
generalizes. Testing the same examples that suggested the label would mainly
measure the investigator's ability to fit a story.

Evidence status: one independent audit of the earlier explanation method,
not a replication of Goodfire's newer workflow. Reading coverage: primary
observational and intervention methods, results, and discussion inspected;
not every appendix item or implementation. No experiments were rerun here.
