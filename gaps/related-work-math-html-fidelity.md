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

## Domain-adaptive retrieval survey reproductions

2026-09-27 — Contributing-model: 6-Astra.

The retrieval survey reproduced the fidelity failure on `hubotter2025-sift`
(arXiv 2410.08020v3: 14/583 blocks failed, minimum 0.200),
`tateno2026-bekko` (2607.25180v1: 6/430, minimum 0), and
`google2025-embeddinggemma-card` (Hugging Face: 1/61, minimum 0.500).
The last case includes model-card navigation text, so this failure class is
not limited to mathematical prose. Exact source URLs remain in
`surveys/domain-adaptive-retrieval/related-work/papers.yaml`; those entries
remain verified but unextracted. Primary pages were readable online.

Reproduce with `uv run --with pyyaml scripts/related-work --dir
surveys/domain-adaptive-retrieval fetch hubotter2025-sift tateno2026-bekko
google2025-embeddinggemma-card` on one line. No extraction sentinel was created
and the acceptance threshold was not bypassed.

The accepted `zhang2025-qwen3-embedding` extract exposes a separate asset
discovery issue: Markdown contains an image with escaped brackets in its alt
text (`[Uncaptioned image]`). `_local_markdown_assets` does not recognize that
link, so `modelscope-logo.png` exists in the ignored source cache but is not
staged, and `audit` still passes. The two scientific figures are staged. This
is a branding-image omission, not missing result evidence. Reproduce through
that paper's `stage`/`audit` and inspect the Markdown image links against
`git ls-files`; fix escaped-alt parsing and add a regression check before
claiming complete linked-asset coverage. No manual force-add bypass was used.
