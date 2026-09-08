# Select difficulty that has a credible target

**Source:** Udandarao et al., CVPR 2025, *Active Data Curation Effectively
Distills Large-Scale Multimodal Models*.
[Full text](https://arxiv.org/pdf/2411.18674) ·
[local extract](../related-work/extract/udandarao2025-active-curation/udandarao2025-active-curation.md).
Read: selection/objective definitions, experimental setup, main ablations, and
reported filtering limitations.

ACID selects image-text batches using a reference model. Easy-reference
selection favors low reference loss; learnability selection uses student loss
minus reference loss. The desired case is difficult for the student and
explainable by the reference. ACED combines that selection with explicit
contrastive distillation. This is more specific than selecting uncertain
examples or disagreements: the reference has a measurable loss, and the batch
selection accounts for contrastive interactions.

**Effectiveness: single-source.** In large image-text pretraining, with
DataComp-1B student data and typically three billion samples seen, the paper
compares reference sizes/datasets and several tuned distillation objectives.
It reports gains across its 27-evaluation aggregate, while selection alone
loses to ordinary distillation on four evaluations. Very aggressive filtering
has diminishing gains and a stated coverage concern. Selection and explicit
distillation can be complementary in this regime.

**Closed-teacher boundary:** Luna's emitted spans do not expose the reference
loss this method uses. A reviewed-reliability score combined with student
difficulty is an analogy, not ACID reproduced. A reliable annotation can also
be too difficult for a particular student; “teacher easy” does not prove
“student learnable.” Preserve random coverage and test the predicted response
to new labels rather than treating difficulty as value by definition.
