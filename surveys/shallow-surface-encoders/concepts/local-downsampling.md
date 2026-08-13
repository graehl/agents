# local-downsampling — shorten character streams before deep attention

> Read-backed digest (cluster B, trust `single-source` each). CANINE and
> Charformer make raw-character encoders tractable by combining cheap locality
> with early sequence compression.

**Papers.** Clark et al., “CANINE,” TACL 2022; Tay et al., “Charformer,” ICLR
2022. **Full text:** [CANINE page](https://aclanthology.org/2022.tacl-1.5/) ·
[CANINE PDF](https://aclanthology.org/2022.tacl-1.5.pdf) ·
[Charformer HTML](https://arxiv.org/html/2106.12672) ·
[Charformer PDF](https://arxiv.org/pdf/2106.12672).

## Mechanisms

CANINE hashes Unicode characters, applies a one-layer local transformer, uses a
stride-4 convolution before its deep stack, then upsamples and fuses shallow
character states for token predictions. Charformer's Gradient-Based Subword
Tokenization scores candidate contiguous byte blocks, softly combines them,
then mean-pools to a shorter sequence.

## Evidence

CANINE reports +2.5/+2.8 TyDi QA F1 over retrained mBERT, with larger gains from
character n-grams. Its plain NER is poor: 74.0 versus 87.8 CoNLL F1 and 65.5
versus 72.4 on Masakha; n-grams recover 86.7 and 76.8. Charformer is competitive
with multilingual token models and faster than uncompressed byte transformers;
its exact speed advantage is setup-sensitive.

## Design edge and limits

Locality, short n-grams, and early compression are reusable. A small sidecar
already has token-aligned length, so it need not inherit the complex
downsample/upsample machinery. Grades `single-source`.

