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
