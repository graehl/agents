# Prompted concept features have precedents; internal concept counts do not follow

Grounded, selective primary-source reading through 17 October 2026. These
methods represent or cluster inputs using model outputs. They give practical
precedents for no-internals discovery without establishing that their feature
axes are the model's own semantic units. Effectiveness is author-reported,
not reproduced here.

## Question-answer embeddings define interpretable axes

[Benara et al., *Crafting Interpretable Embeddings by Asking LLMs Questions*
(NeurIPS 2024; arXiv title)](https://arxiv.org/html/2405.16714) represent text by
answers to natural-language yes/no questions. GPT-4 generates candidate
questions; selection uses downstream prediction performance. The principal
features are binary responses, with probability-valued outputs in the
distilled implementation. Do not describe the entire method as logit-based.

Their language-neuroscience experiments compare prediction of human fMRI
responses against conventional embeddings. This validates useful semantic
features of text, not faithful descriptions of the answering LLM's internals.
Each question also costs an inference per input before caching, batching, or
distillation. For concept exploration, the transferable idea is a bank of
testable questions whose response vectors can be clustered and checked on new
examples. Giving those axes semantic names is built into their construction;
it does not independently validate the names.

## PromptReps directly uses next-token logits as a text representation

[Zhuang et al., *PromptReps* (EMNLP 2024)](https://arxiv.org/html/2404.18424v3)
ask for a single word representing a passage or query. The sparse branch
uses next-token logits, restricted to tokens occurring in the input, then
rectified, log-saturated, and pruned. Its dense branch instead uses a hidden
state and falls outside a no-internals interface.

On the paper's BEIR aggregate, Llama-3-8B-Instruct sparse-only retrieval scores
34.64 nDCG@10 versus BM25's 43.70; the 44.43 hybrid also uses internal states.
Evidence: `benchmark-reported`. This is a direct output-based representation
precedent, not evidence that logits alone beat inexpensive retrieval or
discover internal concept clusters. Moreover, rectifying raw logits is not
invariant to the additive shift introduced by log-probability normalization;
an API adaptation needs a specified alternative score and re-evaluation.

## Conditional likelihood can cluster knowledge components

[Wei, Carvalho, and Stamper, *KCluster* (EDM 2025)](https://educationaldatamining.org/EDM2025/proceedings/2025.EDM.long-papers.64/index.html)
use Phi-2 to cluster educational questions by their apparent shared knowledge
requirements. A directional similarity is

\[
\Delta(q_s,q_t)=\log P(q_s\mid q_t)-\log P(q_s),
\]

averaged with the reverse direction before affinity-propagation clustering.
The method generates descriptions for resulting clusters. Unlike an internal
embedding, this similarity uses only sequence likelihoods. It is therefore a
particularly close precedent for concept-like clustering from output scores.

The interface must score arbitrary supplied continuations, directly or through
repeated full-distribution prefix queries; top-probability readout alone is
not generally sufficient. All-pairs comparisons also
make the query burden quadratic in the number of questions. The discovered
groups describe educational items, and the clustering procedure's inferred
cluster count is not a count of Phi-2's internal concepts. Conditioning can
raise likelihood through wording and topic overlap as well as shared skill.

## A useful experiment separates discovery from mechanistic interpretation

Compare question-response vectors, prompted vocabulary profiles, and
conditional-likelihood similarities on the same held-out concept contrasts.
Include hard answers and simple lexical similarity so that richer outputs
must earn their cost. Count prompts, scored tokens, wall time, and upstream
training separately; a sparse final vector can still require expensive
construction. Test paraphrases, new entities, and lexical near misses before
interpreting clusters semantically.

For the user's proposed “surfaces,” distinguish lexical expressions of one
concept, stable context-dependent subdivisions, and independently manipulable
internal implementations. The first two can be investigated through text and
probabilities. The third needs additional access and controls. The
[open-model calibration design](../survey.md#calibrating-concept-surfaces-on-an-open-model)
freezes output-derived hypotheses before revealing internal measurements.
