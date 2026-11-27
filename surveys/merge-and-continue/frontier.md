# Frontier: merge and continue

Overlay on [survey.md](survey.md) (2026-11-26).

## Open experiments / voids

1. **Old head → new encoder revision via layer-limited Procrustes/PCA + warm-continue:**
   - *Test:* take a trained downstream head (e.g., PII span-tagging head or
     ASR CTC/TDT head) from encoder revision $E_1$, fit a closed-form
     source-centred Procrustes (and top-$k$ PCA-truncated) adapter from $E_2$
     to $E_1$ on 5,000 unlabeled examples, fold it into the head's input
     projection, and compare warm-continued steps-to-quality vs. cold-start
     head training on $E_2$.
2. **Procrustes-aligned head concatenation + survival-of-the-fittest pruning + continued training:**
   - *Test:* join two independently trained (or differently specialized)
     transformers by aligning residual streams, concatenating attention heads
     (or wide-merging), and warm-continuing with structured head-pruning
     pressure vs. Git Re-Basin averaging vs. training from the stronger parent.
3. **UniCon vs. source-centred Procrustes on encoder-revision transfer:**
   - Compare UniCon (`unicon-iclr`, ICLR 2026, arXiv:2604.16678) kernel
     contrastive alignment against source-centred Procrustes on the
     encoder-revision transfer test, especially when the new encoder changes
     architecture or pretraining objective enough that linear Procrustes
     underfits.
