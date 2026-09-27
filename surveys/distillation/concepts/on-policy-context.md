# Turn context-conditioned behavior into parameter learning

Ye et al., *On-Policy Context Distillation for Language Models* (2026, v2).
[Full text](https://arxiv.org/html/2602.12275v2) ·
[local extract](../related-work/extract/ye2026-context-distillation/html/2602.12275v2.md).
Read: §§2–4, including model-size, self-distillation, and raw-trace ablations.

The student generates without context C; the teacher evaluates the same
prefixes with C. Training minimizes token-level reverse KL from student to
teacher, approximated over the student's top-k tokens. Thus the teacher's
temporary context-conditioned behavior supervises persistent student weights.
Teacher and student may have equal size. A frozen teacher and a continually
updated self-teacher are separate experimental configurations.

**Effectiveness: single-source.** Experiments cover Qwen mathematical reasoning
and text games, plus Qwen/Llama system-prompt distillation for medical questions
and safety classification. On the reported Qwen3-8B math test, ordinary context
distillation reaches 78.5 ± 0.5 accuracy and OPCD 79.7 ± 0.5, against a 75.0
base model. These are the paper's uncertainties, not a new significance test.
Training uses additional consolidation examples, so exceeding the context-only
teacher does not isolate a context-compression benefit.

The negative arms matter. Directly injecting a larger model's extracted
experience can hurt smaller models; raw prior solution traces hurt the math
context baseline. A moving self-teacher is worse than the frozen configuration
on the tested Sokoban/medical tasks. OPCD is not uniformly best: the safety
table gives Llama-3.2-3B 83.1 versus 83.3 for ordinary context distillation.

For a creative teacher, replace C with the tested creative prompt or stimulus
and measure held-out behavior after removing C. That is an extrapolated
experiment, not a result of this paper. Reverse KL's mode-seeking tendency
makes preservation of diverse alternatives an explicit outcome to test.
Internal trace matching and cross-tokenizer alignment are not supplied by
this output-distribution objective.
