# encoder-recipe — controlled character-encoder comparison

> Read-backed digest (cluster B, trust `single-source`). A matched study
> separates architecture choices that earlier character-model comparisons
> confounded with scale and training.

**Paper.** Cao, “What is the best recipe for character-level encoder-only
modelling?”, ACL 2023. **Full text:**
[ACL page](https://aclanthology.org/2023.acl-long.326/) ·
[PDF](https://aclanthology.org/2023.acl-long.326.pdf).

## Result

Under a controlled recipe, Charformer downsampling plus CANINE upsampling is
the best tested combination: 78.76 TyDi QA versus 76.97 for BERT, and 90.65
WikiANN versus 90.29. The character model runs at about 0.68 times the token
baseline's throughput and 2.70 times its FLOPs.

## What mattered

Learned character embeddings stabilize training; hash-only inputs can have
catastrophic TyDi variance. Locality priors help. Token-level prediction targets
and masking are more data-efficient than insisting on token-free objectives.
NER remains sensitive to memorization, so character modeling is not uniformly
superior.

## Design edge and limits

The paper supports learned surface inputs and local blocks while warning against
architecture purity. Its full character encoder is much more expensive than a
token-aligned sidecar. Grade `single-source`.

