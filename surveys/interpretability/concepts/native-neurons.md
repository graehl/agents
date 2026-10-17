# Native neurons can have selective roles

Grounded; evidence grade: `single-source` for the experiments below. Main
methods, results, and discussion read; appendices not exhaustively read.

[Gurnee et al., *Finding Neurons in a Haystack: Case Studies with Sparse
Probing* (2023), full text](https://arxiv.org/html/2305.01610v2) studies seven
Pythia V0 language models, from 70M to 6.9B parameters. Sparse linear probes
predict over 100 binary properties across ten categories from MLP activations.
The input collections include natural-language documents, code, compound
words, linguistic annotations, and factual properties of people.

Some middle-layer neurons selectively track context. In Pythia-1B,
`L6.N3108` distinguishes `return` in Go code from its occurrence in other
languages. Zeroing context neurons preferentially worsens language-model loss
in their associated contexts. At 6.9B, ablating one French-context neuron
increases average French-sequence loss by 0.2%. Other features require
combinations: individually polysemantic neurons jointly discriminate a
compound expression. These findings support both selective neurons and
distributed representations within the same model family.

The nearest alternative is a learned feature basis, such as an SAE, rather
than the model's existing MLP coordinates. A sparse probe can discover a
useful native coordinate without training that additional dictionary. Its
label still needs scrutiny: the paper finds that apparent athlete detectors
often track broader sports contexts, and scaling sometimes splits a broad
feature into several narrower ones.

For this survey, the methodological consequence is to keep three claims
separate: a coordinate predicts a property; changing it affects a behavior;
and the property explains its entire role. The experiments support particular
instances of the first two. They do not establish the third over all possible
inputs or all model families.

A practical falsifier of an “only French” interpretation is a held-out search
for strong activations in non-French material, followed by matched
interventions. Include French names, quotations, code, and ambiguous tokens;
check whether effects follow language context or a narrower correlate. This
test can refine the interpretation even when the original probe stays
accurate.
