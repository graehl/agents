# Divergent merging — Fisher weights and permutation alignment

> Read-backed digest (cluster C, trust `single-source` for each mechanism).

**Papers.** Matena and Raffel, “Merging Models with Fisher-Weighted Averaging,”
NeurIPS 2022 ([HTML](https://arxiv.org/html/2111.09832),
[PDF](https://arxiv.org/pdf/2111.09832),
[local extract](../related-work/extract/matena2021-fisher-merging/html/2111.09832.md));
Ainsworth, Hayase, and Srinivasa, “Git Re-Basin: Merging Models modulo
Permutation Symmetries,” ICLR 2023
([HTML](https://arxiv.org/html/2209.04836),
[PDF](https://arxiv.org/pdf/2209.04836),
[local extract](../related-work/extract/ainsworth2022-git-rebasin/ainsworth2022-git-rebasin.md)).

## Mechanisms

Fisher-weighted merging approximates each fine-tune's local posterior with a
diagonal Fisher information matrix and gives parameters more weight where a
task is estimated to be sensitive. Git Re-Basin instead treats hidden-unit
permutations as coordinate symmetries and aligns models before interpolating or
averaging them.

## Evidence

Fisher merging reports better capability retention than a plain mean for
models adapted to different tasks/domains, at the cost of estimating Fisher
statistics and tuning calibration choices. Git Re-Basin shows that a large
part of the apparent barrier between independently initialized networks can be
removed by permutation alignment, but thin, early, or otherwise unfavorable
settings are not universally solved.

## Decision edge and limits

Neither method is justified for checkpoints from one uninterrupted transformer
trajectory: their coordinates and classifier are already aligned, and a
uniform mean is the stronger cheap baseline. For independent or deliberately
displaced branches, first test whether a logit ensemble has a practically
meaningful advantage and whether the raw linear path has an error barrier.
Only then pay for alignment or curvature estimation. Function-aligned affine
repair is a research arm, not a harmless averaging option.
