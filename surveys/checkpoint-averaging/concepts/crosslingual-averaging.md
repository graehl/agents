# Cross-lingual averaging — XLM-R NER and POS evidence

> Read-backed digest (cluster B, trust `single-source`; closest located
> architecture/task family to multilingual PII span tagging).

**Paper.** Schmidt, Vulić, and Glavaš, “Free Lunch: Robust Cross-Lingual
Transfer via Model Checkpoint Averaging,” ACL 2023
([ACL page](https://aclanthology.org/2023.acl-long.314/),
[HTML](https://arxiv.org/html/2305.16834),
[PDF](https://aclanthology.org/2023.acl-long.314.pdf),
[local extract](../related-work/extract/schmidt2023-crosslingual/html/2305.16834.md)).

## Mechanism

The study averages epoch checkpoints from XLM-R fine-tuning and tests
zero-shot/few-shot cross-lingual transfer on NER, POS, natural-language
inference, and question answering. It also studies averaging across runs.

## Evidence

On zero-shot NER, the reported mean rises from 47.1 ± 0.9 for the last
checkpoint to 49.3 ± 0.9 for checkpoint averaging; a target-development oracle
is 51.0 ± 1.4. Across tasks, averaging generally improves mean transfer quality
and reduces variance without target-language development selection. Few-shot
NER also benefits. Poor early checkpoints can hurt on small/unusual datasets,
so “average everything” is not universal.

When combining independent runs, randomly initialized classifier heads break
coordinate compatibility even though the encoder starts from the same
pretrained model. The authors freeze or otherwise align the head to make run
averaging meaningful.

## Decision edge and limits

This is direct evidence that simple XLM-R checkpoint averaging is useful for
cross-lingual token classification. It supports averaging sensible contiguous
checkpoints without target-domain tuning. It also gives a hard warning against
raw averaging of independently randomized heads. The paper reports mean task
metrics rather than native exact typed PII micro-F1; local confirmation remains
necessary.
