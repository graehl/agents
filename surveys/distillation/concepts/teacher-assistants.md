# Intermediate teachers and the capacity-gap hypothesis

**Source:** Mirzadeh et al., AAAI 2020, *Improved Knowledge Distillation via
Teacher Assistant*. [Full text](https://arxiv.org/html/1902.03393) ·
[proceedings](https://ojs.aaai.org/index.php/AAAI/article/view/5963) ·
[local extract](../related-work/extract/mirzadeh2020-teacher-assistant/html/1902.03393.md).
Read: motivating teacher-size comparison, objective, assistant mechanism,
experimental setup, and main comparison table.

A larger teacher can have better accuracy yet produce a worse small student
under direct soft-target distillation. The proposed remedy first distills an
intermediate-sized assistant, then distills the final student from it. This
changes the supervision function as well as adding training compute.

**Effectiveness: single-source.** On CNN and ResNet image classification with
CIFAR and ImageNet, the reported assistant arm improves over direct
distillation. For the ImageNet ResNet comparison, Table 1 reports 66.60% for
direct distillation and 67.36% through an assistant. The methods section says
scores are top-1 test accuracy reached after 120 hyperparameter trials; this
selection protocol limits clean generalization claims from the best scores.

The authors offer competing mechanisms: teacher quality, capacity mismatch,
and overconfident soft targets. None demonstrates that a student cannot learn
correct hard labels from a much larger model. The paper therefore motivates a
capacity control, not substitution of a weaker annotator for Luna. A local
assistant could provide structured probabilities absent from Luna's interface,
but its added bias, errors, and compute must be evaluated against direct
hard-label training and the same additional student compute.
