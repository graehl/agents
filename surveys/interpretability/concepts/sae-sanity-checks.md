# High SAE scores do not certify semantic recovery

Grounded; evidence grade: `single-source`. Main text through conclusion read;
appendices not exhaustively read.

[Anton Korznikov, Andrey Galichin, Alexey Dontsov, Oleg Y. Rogov,
Ivan Oseledets, and Elena Tutubalina, *Sanity Checks for Sparse Autoencoders:
Do SAEs Beat Random Baselines?* (2026), full text](https://arxiv.org/html/2602.14111v1)
tests both synthetic recovery and real LM activations. Its Gemma-2-2B
experiments use layers 12 and 19, 500M OpenWebText tokens, context length 512,
and dictionaries expanded 32-fold.

The synthetic setup has 3,200 known directions in 100 dimensions. In the
variable-frequency condition, a BatchTopK SAE recovers about 9% of directions
at cosine similarity above 0.8 despite explaining 71% of activation variance.
On real activations, partially frozen SAEs achieve competitive automated
interpretability, sparse-probing, and RAVEL editing scores. The strongest
baseline permits decoder learning within cosine 0.8 of initialization;
it is not an entirely untrained random model. Strict frozen-decoder RAVEL
scores are roughly 0.57–0.62 against 0.72–0.74 for trained SAEs. RAVEL also
learns an intervention mask and scores both targeted changes and preservation
of other attributes.

The nearest alternative explanation is that a large dictionary plus learned
selection can support useful predictions and edits without recovering a
unique underlying feature decomposition. This is compatible with successful
causal interventions: controlling a variable does not establish that the
chosen coordinates are its natural representation.

The result is bounded by the tested architectures, training regime, and
metrics; it does not evaluate transcoders. The paper's Llama checkpoint naming
is inconsistent, so the model-specific account here uses Gemma. Its synthetic
feature distribution is a controlled recovery test, not measured ground
truth for an LM.

A practical falsifier of the skeptical interpretation is a trained dictionary
that reliably surpasses matched frozen and random alternatives on held-out,
selective interventions, with the improvement tied to the proposed semantic
decomposition. Compare the same number of candidate directions and the same
supervised selection budget. Also test the feature description on difficult
negatives; reconstruction improvement alone leaves the central question open.
