# byte-local-global — hierarchical bytes with hashed n-gram features

> Read-backed digest (cluster F, trust `single-source`). BLT separates cheap
> byte-local processing from expensive global latent computation.

**Paper.** Pagnoni et al., “Byte Latent Transformer: Patches Scale Better Than
Tokens,” ACL 2025. **Full text:**
[ACL page](https://aclanthology.org/2025.acl-long.453/) ·
[PDF](https://aclanthology.org/2025.acl-long.453.pdf).

## Mechanism

A local byte encoder forms dynamic patches, a global transformer operates on
patch latents, and a local decoder returns to bytes. Inputs combine learned byte
embeddings with hashed byte n-grams and local attention; cross-attention links
local and global paths.

## Evidence and design edge

The reported scaling experiments show byte-patch models can match or exceed
token models at sufficient scale. Hashed n-grams produce large bits-per-byte
gains, with lengths 3--5 carrying much of the benefit and diminishing returns
from longer ranges. For a PII sidecar, short hashed character n-grams are the
transferable motif; BLT's full generative hierarchy is not a relevant first
implementation. Grade `single-source`.

