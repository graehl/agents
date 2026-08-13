# late-task-fusion — attach a task probe to frozen states

> Read-backed digest (cluster E, trust `single-source`). EMBER demonstrates a
> cheap task-specific span path that consumes frozen LM states and joins only at
> the task output.

**Paper.** Popovic and Färber, “Embedded Named Entity Recognition using Probing
Classifiers,” EMNLP 2024. **Full text:**
[ACL page](https://aclanthology.org/2024.emnlp-main.988/) ·
[PDF](https://aclanthology.org/2024.emnlp-main.988.pdf).

## Mechanism and evidence

A token-type probe over hidden states proposes entity labels and an
attention-based span probe groups them. The roughly 11.5M-parameter addition is
reported at about 1% streaming overhead. Its English NER F1 is roughly 80--85,
below the greater-than-90 scores of fine-tuned encoder baselines.

## Design edge and limits

The useful precedent is procedural: cache/freeze an expensive semantic model,
train a small span module, and compose at the decision surface. EMBER uses a
causal decoder and is not itself a competitive redaction model. Grade
`single-source`.
