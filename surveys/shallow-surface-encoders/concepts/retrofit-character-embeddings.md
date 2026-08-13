# retrofit-character-embeddings — add character inputs after pretraining

> Read-backed digest (cluster D, trust `single-source`). XRayEmb retrofits an
> existing token model with a small character encoder instead of retraining the
> whole architecture from scratch.

**Paper.** Pinter et al., “Learning to Look Inside: Augmenting Token-Based
Encoders with Character-Level Information,” arXiv 2108.00391. **Full text:**
[HTML](https://arxiv.org/html/2108.00391) ·
[PDF](https://arxiv.org/pdf/2108.00391).

## Mechanism

XR-Enc applies parallel width-2/3/4 character convolutions, max pooling, and a
projection to the base embedding width; it has roughly 1M parameters. Policies
select which multi-token words use XR-Enc rather than the original lookup. A
second pretraining phase aligns character and token embeddings and acclimates
the transformer; an optional character decoder supplies cycle losses.

## Evidence

Across BERT, GPT-2, and RoBERTa, the best effects occur on word-level and noisy
domain tasks. RoBERTa's gains are inconsistent and much of the aggregate gain
is reproduced by domain-adaptive pretraining without character inputs. Using
XR-Enc for every word is noncompetitive; freezing the model during downstream
training also hurts.

## Design edge and limits

The small CNN and selective retrofit are close precedents. XRayEmb replaces
inputs and requires model acclimation; a late P1 residual is cheaper and cannot
corrupt the semantic input stream. English only. Grade `single-source`.

