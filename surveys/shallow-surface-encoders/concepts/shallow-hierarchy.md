# shallow-hierarchy — small intra-word, deep inter-word processing

> Read-backed digest (cluster C, trust `single-source`). Hierarchical Language
> Modeling (HLM) isolates a shallow surface encoder below a deep semantic one.

**Paper.** Sun et al., “From Characters to Words: Hierarchical Pre-trained
Language Model for Open-vocabulary Language Understanding,” ACL 2023.
**Full text:** [ACL page](https://aclanthology.org/2023.acl-long.200/) ·
[PDF](https://aclanthology.org/2023.acl-long.200.pdf).

## Mechanism

A four-layer character transformer operates within each whitespace word. A
learned `[WORD_CLS]` state aggregates it, a twelve-layer transformer models the
word sequence, and downstream tasks concatenate low- and high-level features.

## Evidence

The reported model improves open-vocabulary and noisy English tasks, including
86.4 versus BERT's 83.8 NCBI disease NER and 47.9 versus 45.7 WNUT16. Its
inference is 90.3 samples/s versus BERT's 93.8 and CharacterBERT's 78.4. A
learned aggregate beats average or max pooling.

## Design edge and limits

The paper shows a shallow surface stage can coexist with near-token-model
throughput. It relies on English word segmentation and expensive new
pretraining, so it is not directly portable to Chinese/Japanese or a retrofit.
Grade `single-source`.

