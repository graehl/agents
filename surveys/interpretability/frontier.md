# Provisional interpretability claims

Grounded, selective overlay on [survey.md](survey.md), searched through
17 October 2026. These are unresolved claims worth discriminating, not
established research gaps or a ranked set of novel projects. No experiments
were run for this survey.

## Native-neuron investigation may resolve much apparent polysemanticity

[Goodfire's essay](https://already-clean.goodfire.com/) argues that native
mechanisms become broadly legible with better tools and context, challenging
the necessity of a learned decomposition as a first step. Its language-model
cleanliness claims remain preliminary and depend on thresholds and explanatory
granularity. The authors conduct and evaluate the investigations; an independent
audit was not located. The essay's technical companion is described as
forthcoming in the inspected version.

The discriminating check is a preregistered, random neuron sample with matched
budgets for native-neuron and SAE-based investigation, untouched evaluation
contexts, explicit near misses, and intervention predictions. Report failures
and search effort as well as successful labels. Count positive and negative
poles consistently. These controls address a moving definition of “one thing,”
selection bias, and explanations broadened after seeing counterexamples.

Revisit on release of the companion methods/artifacts or an independent random
sample audit. Until then, use the workflow as a candidate research method;
do not promote a whole-network conclusion. Unscheduled review reminder:
2027-01-17.

## Sign-aware interpretation has prior art; prevalence remains model-specific

[GLUScope](https://arxiv.org/html/2602.23826) and
[Weakening Neurons](https://arxiv.org/html/2609.18612v1) establish prior
published attention to negative-gate and double-negative behavior. They do not
resolve how frequently particular sign regimes dominate across modern
architectures, nor the effects of removing them from a given Qwen checkpoint.
The latter needs explicit checkpoint, task, sample, intervention, and baseline
details. Conditional ablation may itself change downstream sign membership.

The cheapest check is to reproduce one documented neuron and then repeat the
quadrant analysis on a fixed random sample, comparing semantic predictions
and output effects with and without pooling signs. Revisit when the Goodfire
companion makes those claims reproducible. No absence-of-prior-work claim is
made; the targeted prior-art search found directly relevant work.

## SAE evaluation may reward useful control without unique decomposition

[Korznikov et al.](https://arxiv.org/html/2602.14111v1) challenge existing
metrics using constrained-random baselines. The strongest baselines still
learn parameters and intervention masks. This is a warning about what a metric
identifies, not a proof that learned dictionaries are useless.

The positive counterpoint [Jørgensen and Hansen](https://arxiv.org/html/2605.31183v1)
reports improved SAE steering with supervised labels and feature-specific
selection/tuning on Gemma-2-9B. It changes the research pipeline and candidate
pool, so it is not a matched rerun of every weaker SAE baseline. Its main
text was read online; it is outside this pass's local extraction set. Both
preprints remain `single-source` in this map.

A useful comparison fixes labels, discovery data, selection budget, intervention
strength tuning, and held-out outcomes across native coordinates, supervised
directions, SAEs, and constrained-random dictionaries. Evaluate both desired
effects and preserved attributes. Revisit on independent matched-budget
replication, rather than treating either headline as a settled verdict.
