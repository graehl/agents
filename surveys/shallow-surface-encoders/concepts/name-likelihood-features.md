# name-likelihood-features — surface form as entity evidence

> Read-backed digest (cluster A, trust `single-source`). A direct precursor to
> a P1 surface sidecar: classify entityness from a token's characters, then add
> the score to a contextual NER system.

**Paper.** Yu, Mayhew, Sammons, and Roth, “On the Strength of Character
Language Models for Multilingual Named Entity Recognition,” EMNLP 2018.
**Full text:** [ACL page](https://aclanthology.org/D18-1345/) ·
[PDF](https://aclanthology.org/D18-1345.pdf).

## Mechanism

Train separate character language models on entity and non-entity token lists;
assign a token by likelihood or expose the two likelihoods as NER features. The
best model is a Witten--Bell-smoothed order-6 n-gram model. It sees no sentence
context and no fine entity type.

## Evidence

Across English, Amharic, Arabic, Bengali, Farsi, Hindi, Somali, and Tagalog, the
standalone n-gram reaches 92.8 token-level identification F1 in English and
70.5 averaged over the other seven languages. The contextual CogCompNER ceiling
is 96.5 and 76.8. Adding the simple features improves full NER in six of eight
languages and hurts Tagalog; unseen-entity effects are also mixed.

## Design edge and limits

This is the strongest direct evidence that shallow orthography can add P1
entityness across scripts, and it makes a cheap character n-gram score the
correct diagnostic baseline. It is an older, token-level evaluation with small
datasets and pre-transformer incumbents; it does not predict a gain over a
modern XLM-R tagger. Grade `single-source`.

