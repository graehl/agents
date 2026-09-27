# Distill feedback on the student's own continuations

Agarwal et al., *On-Policy Distillation of Language Models: Learning from
Self-Generated Mistakes* (ICLR 2024).
[Full text](https://arxiv.org/html/2306.13649) ·
[local extract](../related-work/extract/agarwal2024-on-policy/html/2306.13649.md).
Read: §3 method and §4 task evaluations, especially the diversity comparison.

Generalized Knowledge Distillation (GKD) varies two choices independently:
which prefixes receive supervision, and which distribution divergence is
minimized. It mixes fixed training sequences with student-generated sequences
and asks the teacher for next-token distributions at those prefixes. This
addresses the mismatch between teacher-written training trajectories and the
student's deployment trajectories. The student is already capable enough to
generate useful sequences; this is not a recipe for a random initialization.

**Effectiveness: single-source.** With a T5-XL teacher and smaller T5 students,
the paper reports improvements over sequence-level and supervised distillation
on XSum, WMT14 English–German, and GSM8K. Baselines begin from the same
supervised student checkpoint. Gains depend on divergence, size, task, and
decoding; teacher probability access is required by this recipe.

The creativity-relevant result is the quality/diversity tradeoff in XSum:
more mode-seeking divergences can improve quality while reducing diversity,
and decoding temperature changes the comparison. Self-BLEU is a diversity
proxy, not a measure of conceptual originality or useful creative panels.

For creative distillation, separate prefix distribution, loss direction, and
candidate curation. A good average imitation score does not establish coverage
of worthwhile alternatives. Teacher feedback on student drafts is a direct
methodological connection; transferring selected internal traces is a different
supervision channel not tested by these results.
