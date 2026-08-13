# character-cnn — word-local open-vocabulary lookup replacement

> Read-backed digest (cluster A, trust `single-source`). CharacterBERT replaces
> a vocabulary lookup with an ELMo-style character CNN for each whole word.

**Paper.** El Boukkouri et al., “CharacterBERT: Reconciling ELMo and BERT for
Word-Level Open-Vocabulary Representations From Characters,” COLING 2020.
**Full text:** [ACL page](https://aclanthology.org/2020.coling-main.609/) ·
[PDF](https://aclanthology.org/2020.coling-main.609.pdf).

## Mechanism

Encode each word's bytes with parallel width-1 through width-7 convolutions,
max-pool, apply two highway layers, and project to BERT's 768-dimensional input.
The resulting model has 104.6M parameters versus BERT-base's 109.5M because it
removes the large WordPiece table.

## Evidence

On English medical tasks, reported gains over matched BERT are generally about
0.5--2 points, and under 40% misspelling noise the advantage is about five F1
points. Pretraining is about 2.1 times slower; fine-tuning averages about 19%
slower, while inference is near parity in the reported setup.

## Design edge and limits

Parallel short convolutions plus pooling are a strong small surface-encoder
motif. CharacterBERT replaces the base input and requires new pretraining; it
does not test a residual sidecar on multilingual NER. Grade `single-source`.

