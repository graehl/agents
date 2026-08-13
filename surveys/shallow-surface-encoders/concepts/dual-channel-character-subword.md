# dual-channel-character-subword — repeated character/token interaction

> Read-backed digest (cluster D, trust `single-source`). CharBERT carries
> character and subword states through the full encoder and fuses them after
> every transformer block.

**Paper.** Ma et al., “CharBERT: Character-aware Pre-trained Language Model,”
COLING 2020. **Full text:**
[ACL page](https://aclanthology.org/2020.coling-main.4/) ·
[PDF](https://aclanthology.org/2020.coling-main.4.pdf).

## Mechanism

A bidirectional GRU runs over the whole character stream; first/last character
states form each token representation. After every transformer block, token
and character channels are projected, locally convolved together, then split
back into residual channel-specific states. A noisy-language-model objective
reconstructs words after character edits.

## Evidence

Reported clean CoNLL NER rises from 91.24 to 91.81 over BERT and from 92.22 to
92.49 over RoBERTa. Under synthetic character attacks, BERT falls to 60.79 while
CharBERT reaches 76.14. The character channel adds about 5M parameters but the
system uses 320,000 continued-pretraining steps on 12GB of English Wikipedia.

## Design edge and limits

Character information is most helpful on split words and noise, and the clean
gain shrinks against the stronger baseline. Repeated interaction is a useful
ceiling but is too training-intensive for the first sidecar pilot. Grade
`single-source`.

