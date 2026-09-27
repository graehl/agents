# Traits can transfer through semantically unrelated training outputs

Cloud et al., *Subliminal Learning* (2025).
[Full text](https://arxiv.org/html/2507.14805v1) ·
[local extract](../related-work/extract/cloud2025-subliminal/html/2507.14805v1.md).
Read: experimental setup, numeric transfer, cross-model and ICL tests, discussion.

A prompted or fine-tuned teacher generates constrained outputs; a student
starting from the reference model is fine-tuned on those outputs after filtering
explicit trait references. The main animal/tree experiment samples 30,000
completions, filters and subsamples to 10,000, and trains for ten epochs.
The control uses outputs from the teacher without the trait prompt.

**Effectiveness: single-source.** GPT-4.1-nano students shift toward teacher
preferences compared with the reference and ordinary-number controls. Other
experiments use code and reasoning traces. These are behavioral preference
readouts, not creative-quality judgments. Some traits fail for some models.

Two negative arms are particularly relevant. In §5.2, presenting examples in
context does not reproduce the fine-tuning effect, even with the full dataset.
In §5.1, mismatched model pairs generally do not transfer reliably; GPT-4o and
GPT-4.1 are an exception. The paper's shared-initialization explanation for
that exception is not independently verified here.

The proposal should cross generator and recipient lineage, retain a neutral
teacher control, and separate weight-training from prompt-only use. A failed
prompted detector bounds that detector, not all possible readouts. The paper
does not establish arbitrary-string one-shot transmission, internal style
localization, or worthwhile creative transfer.
