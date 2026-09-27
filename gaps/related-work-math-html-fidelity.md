---
slug: related-work-math-html-fidelity
noticed: 2026-09-27
where: scripts/related-work HTML derivation fidelity gate
---

**Gap:** Two accessible mathematical papers could not be archived by the
shared extraction engine. The cause is untriaged: conversion loss and an
overstrict fidelity comparison remain possible. The affected survey honestly
retains their citations as verified but unextracted.

**Noticed while:** grounded length-aware batching and single-shuffle review.

`mishchenko2020-shuffle-once` failed 42 of 325 source blocks, with minimum
coverage 0; `yun2021-single-shuffle` failed 12 of 252, minimum 0.2. Both
arxiv.org/html and ar5iv.labs.arxiv.org/html sources failed. Example flagged
prose included “applying lemma 6 to 60 thus gives” and “for and the
conjectures 25 and 26 are true”. Full HTML remained readable through the web
tool; no `.fetched` sentinel or accepted Markdown was produced.

Reproduce with `uv run --with pyyaml python scripts/related-work --dir
surveys/length-aware-batching fetch mishchenko2020-shuffle-once
yun2021-single-shuffle` (join the displayed command onto one line).

**Fix sketch:** compare the exact failed source blocks with converted text
and math/link normalization before changing any acceptance threshold. Keep
failure atomic and preserve the fidelity requirement.

2026-09-27 — Contributing-model: 6-astra

## Creativity survey reproductions

2026-09-27 — Contributing-model: 6-Astra.

The initial creativity survey hit the same failure class on
`misaki2026-string-seed` (arXiv 2510.21150v3: 12/659 blocks failed, minimum
0.467) and `zhang2026-verbalized-sampling` (2510.01171v4: 14/1373 blocks,
minimum 0). Reproduce with `/usr/bin/python3 scripts/related-work --dir
surveys/generative-creativity fetch misaki2026-string-seed
zhang2026-verbalized-sampling` on one line. The map records primary HTML
readings but does not claim accepted local full-text extracts for these works.

The alternate `misaki2026-string-seed-blog` URL also failed, with “downloaded
page has no unambiguous HTML entry point”. This may be a separate entry-point
discovery issue and is untriaged. Neither failure was bypassed. Pending
manifest entries preserve exact source URLs for retry.
