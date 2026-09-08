# Patient optimization with consistent teacher inputs

**Source:** Beyer et al., CVPR 2022, *Knowledge Distillation: A Good Teacher
Is Patient and Consistent*. [Full text](https://arxiv.org/pdf/2106.05237) ·
[local extract](../related-work/extract/beyer2022-patient-consistent/beyer2022-patient-consistent.md).
Read: setup, matched-view and duration experiments, ImageNet scaling, and
optimization comparisons.

The teacher and student see the same augmented image, and the teacher supplies
fresh soft targets for that view. Strong augmentation broadens the input
support; very long optimization lets the smaller network approach the teacher.
This differs from repeatedly fitting one fixed prediction per original image.

**Effectiveness: single-source.** In BiT-ResNet-152x2 to ResNet-50 compression,
the paper tunes learning rate, weight decay, and temperature across small and
medium image datasets, then scales to ImageNet. Long matched-view training
improves generalization; the fixed-target ImageNet arm overfits after 600
epochs. The authors also show that method rankings at short durations can
reverse with longer training. Large compute is part of the result.

**Decision consequence:** failure at one training budget is not a capacity
bound. However, this paper does not justify replaying cached hard annotations
indefinitely. We lack Luna's soft targets and cannot assume a modified sentence
retains its old label. In text, inspect whether the teacher saw contextual
sentences unavailable to the student. A controlled longer run and a matched
context comparison are distinct experiments; combining them would obscure
which restriction mattered.
