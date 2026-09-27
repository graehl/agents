# Replay, starting-point priors and short trajectories

Ibrahim et al., *Simple and Scalable Strategies to Continually Pre-train Large
Language Models* (2024): [full text](https://arxiv.org/html/2403.08763v4),
[local extract](../related-work/extract/ibrahim2024-continual/html/2403.08763v4.md).
Li, Grandvalet and Davoine, *Explicit Inductive Bias for Transfer Learning with
Convolutional Networks* (ICML 2018):
[full text](https://arxiv.org/html/1802.01483),
[local extract](../related-work/extract/li2018-l2sp/html/1802.01483.md).

**Read:** compute-equivalent replay and replay results; L2-SP/Fisher definitions,
comparison with freezing and discussion. **Evidence:** single-source within
each paper's regime, not a reproduced recipe for text retrieval.

The continual-pretraining study mixes old data into a fixed total token budget.
Stronger English-to-German shift requires more replay for comparable retention
than English-to-English shift. Its chosen comparisons use 5% and 25%, while
the full study varies the fraction more widely. Even small replay helps;
large fractions trade away adaptation. This supports measuring the frontier
rather than prescribing one percentage.

L2-SP penalizes distance from the starting weights, unlike decay toward zero.
Its vision-transfer study finds no significant target-accuracy advantage from
Fisher weighting over isotropic L2-SP. Early stopping and explicit proximity
are distinct controls and can coexist.

**Decision changed:** begin with replay and short updates, then compare a
starting-point penalty if retention remains poor. Evaluate behaviors on
disjoint, multilingual anchors; parameter distance alone cannot certify them.
