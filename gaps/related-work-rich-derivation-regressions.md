---
slug: related-work-rich-derivation-regressions
noticed: 2026-09-30
where: scripts/related-work derive_saved_html, preprocess_html (rich-visual derivation from 3403c43)
---

**Gap:** the rich-visual HTML derivation (commit 3403c43, which closed
`paper-html-markdown-conversion`) rejects sources the previous derivation
extracted. When the speech surveys in the draft project
(`research/speech-recognition/surveys/`) were rebuilt, 58 + 72 extracts
re-derived cleanly and 14 failed. A fresh online `--refetch` recovered
2; 12 still fail. Their older text-only extracts survive, and `audit`
reports them as `html-derivation` drift. Page chrome and one broken
source asset should not reject a paper whose body converts.

**Noticed while:** adding the contextual-biasing cluster to the compact ASR
survey and rebuilding extracts after 3403c43, 2026-09-30.

| Key | Source | Failure after online refetch |
|---|---|---|
| yao2024-zipformer | arXiv 2310.11230 | source HTML has no auditable visible text block |
| babu2021-xlsr | arXiv 2111.09296 | same |
| gandhi2023-distilwhisper | arXiv 2311.00430 | same |
| yao2025-crctc | arXiv 2410.05101 | same |
| sekoyan2025-canaryv2 | arXiv 2509.14128 | same |
| koduru2026-heard | arXiv 2609.00727 | same |
| koshkin2026-hikari | arXiv 2603.11578 | mismatched tag inside SVG visual |
| liu2026-hear2act | arXiv 2608.19515v2 | mismatched tag inside SVG visual |
| papi2025-hearing | arXiv 2512.16378 | visual download failed: `https://arxiv.org/html/logo.png` 404 (site logo) |
| gsmarena2020-galaxys20 | web | unsupported visual content: iframe |
| xda2019-snapdragon865 | web | fidelity 1/32 flagged, total 0.967 < 0.98 (page shrank to 32 blocks) |
| agranovich2024-simultron | arXiv 2406.02133 | fidelity 3/49 flagged, total 0.939, one block of `relatedworkmathtoken…` |

Two more failed offline (`--derive-only`) on page-chrome images missing from
the saved page and passed online: a Hugging Face avatar (Qualcomm card), a
SpeechBrain avatar. `zhu2024-ge2ekws` (arXiv 2410.16647) failed because
arXiv's own HTML links a figure that returns 404
(`latex/pics/a_ge2e2.png`); it extracted from PDF.

Probable causes, untriaged:

- The "no auditable visible text block" cases are all papers that extracted
  under v1. Protecting rich content before scoring probably removes the
  prose blocks the gate needs, or the arXiv page layout now hides them
  inside a protected container.
- Logos, avatars and iframes are treated as paper figures.
- A single 404 asset on the source server rejects the whole paper.
- Inline math placeholder tokens leak into scored prose.

Reproduce from the draft project root:

```bash
uv run --with pyyaml ~/agents/scripts/related-work \
  --dir research/speech-recognition/surveys/compact-asr-training \
  fetch --refetch yao2024-zipformer gsmarena2020-galaxys20
```

**Fix sketch:**

- Separate page chrome (site logos, avatars, nav icons, iframes outside the
  article) from paper visuals, and preserve only visuals inside the
  article or figure containers.
- Record a missing or 404 source asset as a named gap in the fidelity
  result instead of rejecting the paper.
- Find why prose blocks disappear from scoring on the six arXiv papers.
- Add each case above as a regression fixture.

2026-09-30 — Contributing-model: opus-5.5

## Full rebuild under html-md-v4, 2026-09-30

After the list-item fix (7d24445), every extract in all 11 `~/agents`
surveys and both draft speech surveys was rebuilt offline from saved pages,
with an online `--refetch` for failures. 252 rebuilt offline and 7 more
online. 34 still fail and keep their earlier text-only derivation; audit
reports them as `html-derivation` drift. Every remaining doubled list label
(381 lines of `1. 1.` or lone `• `) is in one of these 34 extracts.

| Count | Failure |
|---:|---|
| 14 | source HTML has no auditable visible text block |
| 9 | mismatched tag inside SVG visual |
| 4 | fidelity failed after rebuild (total below 0.98) |
| 3 | unsupported visual content: iframe |
| 1 | visual download failed (404) |
| 1 | SVG visual has an external CSS dependency |
| 1 | invalid visual data URI |
| 1 | invalid SVG visual: not well-formed |

Per-survey rows and keys are in the `fetch` output; rerun the rebuild to
regenerate them. Commands and reasons match the table above the fix
sketch.

**Refetch can swap a good source for a worse one.** `elhage2022-superposition`
(llm-intelligence) was extracted from the Transformer Circuits HTML page
(378/378 blocks). Its offline rebuild failed on an inline data-URI image.
`fetch --refetch` then followed the manifest's arXiv id to the PDF and
replaced the HTML extract with a marker conversion. The HTML extract was
restored by hand. A refetch should retry the source the sentinel recorded
before switching route, and should not replace a completed extract with a
different method unless asked.

2026-09-30 — Contributing-model: opus-5.5

## Fresh untranscribed-speech sources, 2026-10-01

The grounded `surveys/untranscribed-speech/` pass accepted fifteen of
twenty-one attempted sources. Six new sources have no accepted local
Markdown/sentinel; they were read through primary-source web views and
remain marked locally ungrounded in the manifest.

| Key | Failure |
|---|---|
| omnisonar2026 | mismatched tag inside SVG visual |
| heigold2026-mseb | mismatched tag inside SVG visual |
| allauzen2026-mseb-llms | mismatched tag inside SVG visual |
| voxlingua107-downloads | fidelity: 1/1 flagged blocks, total 0.385 |
| clap-release | fidelity: 2/44 flagged blocks (one tolerated), total 0.993 |
| mms-ulab-v2-card | unsupported visual content: audio (dataset preview) |

Reproducer from `~/agents`:

```bash
uv run --with pyyaml scripts/related-work \
  --dir surveys/untranscribed-speech fetch --no-stage \
  omnisonar2026 heigold2026-mseb allauzen2026-mseb-llms \
  voxlingua107-downloads clap-release mms-ulab-v2-card
```

The audio-preview failure extends the page-chrome boundary problem: a
dataset card's prose should remain extractable when an unrelated preview
player is outside the substantive card. No extractor repair was attempted
as part of the survey.

2026-10-01 — Contributing-model: 6.1-Sol

A follow-up pass hit the same audio-preview failure on two more Hugging
Face dataset cards, `omniasr-corpus-card` and `fleurs-card`; both were read
from the cards' raw `README.md` instead. Reproduce with the command above,
substituting those keys.

2026-10-01 — Contributing-model: opus-5.5
