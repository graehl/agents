# Dynamic selection for distillation

**Source:** Li et al., EMNLP 2021, *Dynamic Knowledge Distillation for
Pre-trained Language Models*. [Full text](https://arxiv.org/html/2109.11295) ·
[local extract](../related-work/extract/li2021-dynamic-kd/html/2109.11295.md).
Read: methods, classification experiments, analyses, and discussion.

The paper separates three changes: choosing the teacher, choosing examples,
and adjusting the loss. These are investigated independently. Student entropy,
margin, or least confidence selects a fraction of each candidate batch for
teacher queries. A random subset is the important control. Selection itself
needs only student predictions; the training uses teacher logits, and one
separate arm also uses intermediate states.

**Effectiveness: single-source.** On original classification datasets at a
50% selection rate, random sampling is competitive with uncertainty sampling.
On training sets expanded twenty-fold with masked-LM augmentation, selecting
10% by entropy gives average test accuracy 77.7 versus TinyBERT's 78.0 and
random selection's 76.5 (Table 4). The reported per-instance computation is
4.65 versus 24.9 billion operations for full distillation; random selection
costs less still. The headline “10% is enough” therefore concerns a redundant
augmented pool, not arbitrary removal of 90% of scarce human annotations.

**What changes a decision:** active acquisition is worth a controlled trial
when labels are expensive and candidate text is abundant. It is not evidence
that repeatedly sampling the largest losses from an already small labeled
pool will help. For span labeling, length normalization, missed-entity recall,
and abundant outside tokens require an explicitly different acquisition score.
Replacing the paper's soft-target loss with hard teacher spans is a proposed
adaptation, not a reproduced result.
