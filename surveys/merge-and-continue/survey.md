# Merge and continue: cross-model alignment, layer-limited transfer, and warm continuation

**Mode: grounded-initial. Coverage cutoff: 2026-11-26.**
Scope: aligning independently trained models—or a new encoder revision with an
existing downstream head—via closed-form orthogonal/PCA/kernel maps or
permutation/activation matching, then **warm-continuing training** (including
head concatenation, averaging, or survival-of-the-fittest pruning). Sibling of
[checkpoint-averaging](../checkpoint-averaging/survey.md) (same-trajectory /
common-start averaging) and [interpretability](../interpretability/survey.md)
(cross-model representation geometry).

## Decision summary

1. **Plugging an old head into a new encoder revision (layer-limited transfer):**
   fit a closed-form **source-centred orthogonal Procrustes** (or PCA-truncated
   Procrustes) map on ~5,000 unlabeled paired examples at the transferred layer,
   fold the linear map into the head's input projection ($W_{\text{head}}' =
   W_{\text{head}} R$), and warm-continue training. In retrieval, this takes
   0.34 s on CPU, retains 82–84% of target quality zero-shot, and beats ridge
   regression, RBF kernel ridge, and SGD MLPs (`hanxiao2026-eca`).
2. **Joining two independently trained models + continued training:** naive
   weight averaging fails across basins; aligning residual streams via
   Procrustes (or neurons via Git Re-Basin / ZipIt!) gives a warm-start where
   concatenating attention heads (or wide-merging followed by
   survival-of-the-fittest pruning) plus continued training lets the optimizer
   resolve residual alignment error rather than forcing zero-shot perfection.
3. **Pre-fit diagnostics matter:** rotation-invariant CKA does *not* predict
   zero-shot frame compatibility ($r = -0.073$); frame correlation $\rho$
   ($r = +0.951$) and source anisotropy $\kappa_s$ ($r = +0.882$ with affine
   gain over pure rotation) do (`hanxiao2026-eca`).

## A. Layer-limited embedding / representation transfer (old head → new encoder)

- **Embedding Compatibility Adapters (`hanxiao2026-eca`, 2026; [repo](https://github.com/hanxiao/embedding-compatibility-adapters), [report.pdf](https://github.com/hanxiao/embedding-compatibility-adapters/blob/main/report.pdf)):**
  - *Mechanism:* closed-form **source-centred Procrustes**
    $\hat{z} = \text{norm}((z - \mu_x) R_c)$ fit on 5,000 unlabeled paired
    texts (0.34 s on CPU; 76 µs/query). Tested across 8 embedding models / 6
    families (56 directed pairs) on 13 NanoBEIR tasks.
  - *Key result:* zero-hyperparameter source-centred Procrustes reaches
    **0.5336 nDCG@10** (82.2% of target; val-selected Plato's Key affine
    reaches **0.5462**, 84.2%), beating ridge regression (0.5029), RBF kernel
    ridge (0.4549), and SGD 3-layer MLP (0.5301).
  - *Anisotropy pitfall:* blindly adding $+\mu_y$ back hurts anisotropic targets
    by −0.0807 nDCG@10 (hubness bias); omitting $+\mu_y$ fixes it.
  - *Generalization beyond IR:* for **arbitrary downstream heads** (span
    taggers, classifiers, CTC/TDT heads, projectors) plugged into a new encoder
    revision, fitting a Procrustes or PCA-truncated linear map *limited to the
    transferred layer* initializes the new-encoder→old-head interface in seconds
    before warm-continuing training—avoiding cold-start head re-training and
    forgetting.
- **Plato's Key (`cheng2026-platos-key`, Hazy Research blog, 2026-11-25):**
  - Closed-form semi-orthogonal Procrustes + global scale
    $\hat{z}_B = \mu_B + sR(z_A - \mu_A)$ across 12 base LLMs (1.5B–27B) on
    factual-recall keys. 41% median transfer accuracy (vs. 55% self-swap);
    **256 principal components retain 74%** of full-rotation accuracy,
    confirming that low-rank PCA-limited transfer captures most of the usable
    signal.
- **Model Stitching (`bansal2021-stitching`, NeurIPS 2021, arXiv:2106.07682):**
  - Foundational demonstration that a single linear layer (stitch) can connect
    layer $\ell$ of model A to layer $\ell+1$ of independently trained model B
    with minimal accuracy loss.

## B. Kernel / contrastive alignment (UniCon)

- **UniCon (`unicon-iclr`, ICLR 2026, arXiv:2604.16678; Hangke Sui, Yuqing Wang, Minh N. Do):**
  - *Unified Framework for Efficient Contrastive Alignment via Kernels*: introduces
    the contrastive similarity weight matrix $S(\gamma)$ to enable closed-form
    global solutions that provably replace minibatch back-propagation with exact
    updates across linear and nonlinear encoders (one-to-one and many-to-many
    alignments). Framed in reproducing kernel Hilbert spaces (RKHS), it unifies
    contrastive alignment and connects it to spectral methods.
  - *Role in merge+continue:* the natural nonlinear/contrastive upgrade when
    linear Procrustes underfits a layer boundary (e.g., across larger
    architectural or pretraining-objective gaps).

## C. Full-model merging + continued training

- **Git Re-Basin (`ainsworth2023-gitrebasin`, ICLR 2023, arXiv:2209.04836):**
  - Aligns independently trained models modulo hidden-unit permutation
    symmetries (activation matching, weight matching, straight-through
    estimator) to remove the linear-interpolation loss barrier before averaging.
- **ZipIt! (`stoica2024-zipit`, ICLR 2024, arXiv:2305.03053):**
  - Merges models trained on *different tasks* without training by zipping
    correlated features both within and across models.
- **Head-concat / survival-of-the-fittest + warm-continue (proposed direction):**
  - Instead of destructive 1:1 weight averaging, align two independently
    trained models' residual streams (Procrustes per layer or at key
    boundaries), **join their attention heads** (concatenation, or averaged +
    pruned survival-of-the-fittest), and **warm-continue training**. Because
    continued training heals residual mismatch, the alignment only needs to
    put the joined network in a good optimization basin, not achieve zero-shot
    parity.

## D. Practical pitfalls

- **Mixing native and adapted representations raw crashes performance:**
  `hanxiao2026-eca` shows a −0.247 nDCG@10 crash at 25% progressive migration
  under raw cosine because adapted vectors have lower background cosine and
  attenuated peaks; per-shard top-100 z-scoring restores monotonicity.
- **Single-layer vs. multi-layer consistency:** aligning one layer's residual
  stream (Plato's Key, ECA) is trivial in closed form; aligning *all* layers
  simultaneously for full-model merging requires keeping $W_Q, W_K, W_V, W_O$
  and MLP gates consistent across consecutive layers.

<!-- reviewed 2026-11-26 (Neon) -->
