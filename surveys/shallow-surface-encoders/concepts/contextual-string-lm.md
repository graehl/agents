# contextual-string-lm — pretrained character states for sequence labeling

> Read-backed digest (cluster A, trust `single-source`). Character-LM boundary
> states supply open-vocabulary local and contextual features to a tagger.

**Paper.** Akbik, Blythe, and Vollgraf, “Contextual String Embeddings for
Sequence Labeling,” COLING 2018. **Full text:**
[ACL page](https://aclanthology.org/C18-1139/) ·
[PDF](https://aclanthology.org/C18-1139.pdf).

## Mechanism

Pretrain forward and backward one-layer character LSTMs. For each word,
concatenate the forward state after its last character and the backward state
before its first; pass that vector, optionally with static word embeddings, to
a BiLSTM-CRF tagger. The character LM is separate from the task model.

## Evidence

The reported best system reaches 93.09 English and 88.32 German CoNLL-2003 NER
F1. Adding static word embeddings improves English NER from 91.97 to 93.07,
showing complementarity rather than a character-only replacement. A direct
linear map is much weaker than the BiLSTM-CRF, so the pretrained character
state does not eliminate task-local sequence modeling.

## Design edge and limits

The important precedent is a separately pretrained bidirectional surface model
whose states are consumed as features. Its 2048-state LSTMs trained for up to a
week per language, and its baselines predate XLM-R. A small task-trained sidecar
tests the same complementarity at far lower cost. Grade `single-source`.

