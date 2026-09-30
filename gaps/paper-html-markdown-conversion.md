---
slug: paper-html-markdown-conversion
noticed: 2026-09-30
where: scripts/related-work derive_saved_html, _run_html2text, preprocess_html
---

**Gap:** the survey engine's HTML→Markdown path (pinned `html2text` after
`preprocess_html`) is too weak for scientific papers and model cards. Visual
content that Markdown cannot express is flattened into text soup or dropped
instead of being kept as a figure asset, and loss is detected only through
the text-fidelity check. The goal: every extract keeps its figures, charts,
complex tables and other visual content as linked SVG (or native raster when
the original is a bitmap), whether the source is HTML or PDF. Prose, math and
simple tables stay Markdown. The PDF path already recuts vector figures as SVG
(`scripts/pdf-figures-svg`); the HTML path has no equivalent.

**Noticed while:** grounding the draft speech-recognition surveys
(`research/speech-recognition/surveys/` in the draft project), 2026-09-30.

## Evidence

**Visual content lost in accepted extracts.** In MMS (arXiv 2305.13516v1,
`pratap2023-mms`), the Markdown has no image links at all:

- Figure 1 is an HTML `<object>` and was dropped, leaving only its caption.
- Figure 10 is inline `<svg>` and became run-together axis text:
  `300M1B\(12\)\(14\)\(16\)\(18\)CERXLS-RMMS Figure 10: …`.
- Figure 11 became a 60-language label string
  (`amhlaomalnyaswhfulkorpan…`).

The engine's own presentation notes flag the same class on many fetches:
`kept (ignored source cache; object, spanning table, svg)`. The notes show
that the source had those elements; the committed Markdown does not carry
them.

**Tables.** In TDT (2304.06795v2), LaTeX equation arrays arrive as
pipe-table rows (`| \(\displaystyle=\) | … | (1)`). Tables with row or
column spans are flattened.

**Rejected extracts.** Before 2026-09-30 the fidelity gate required every
visible block to keep 90% of its five-word sequences. These ten sources
failed on one or two blocks:

| Key | Failed / blocks | Worst | Failing text |
|---|---|---|---|
| xu2023-tdt | 2/163 | 0.839 | worked-example paragraph |
| pratap2023-mms | 2/356 | 0.818 | data paragraph |
| qualcomm2026-aihubwhisper (HF card) | 1/101 | 0.400 | page controls ("like 0 follow") |
| xda2019-snapdragon865 (web) | 1/63 | 0.676 | spec table run together ("adreno 650vulkan") |
| papi2025-hearing | 1/175 | 0.571 | title block |
| speechbrain-langid-ecapa-card (HF card) | 1/28 | 0.667 | card header |
| chen2021-pseudoref | 1/90 | 0.886 | alignment paragraph |
| sasu2025-pitch-accent | 1/44 | 0.500 | figure caption ("figure 1 joint prosody asr model") |
| hannan2026-dld | 1/38 | 0.886 | results paragraph |
| saif2025-objsoups | 2/243 | 0.625 | sentence with notation |

The gate now tolerates a few short flagged blocks (see
`topics/research-survey.md` § Design decisions). All ten were extracted
after that change, but their flagged blocks are still mis-converted in the
committed Markdown. The math-dense rejections in
[related-work-math-html-fidelity](related-work-math-html-fidelity.md)
(up to 42/325 blocks) are probably the same converter weakness at larger
scale; that gap's block-level triage would confirm it.

**PDF path.** PDF fallback also failed twice in the same pass:

- TDT's downloaded "PDF" failed PDFium with "Data format error".
- MMS reported "pdf download failed".

The cause is untriaged; the downloaded file was not kept. Two further
"pdf download failed" rows came from unquoted arXiv ids that YAML read as
floats (`2110.01900` → `2110.019`). The manifest loader now rejects
non-string `arxiv` values.

Reproduce from the draft project root. The tool prints one JSON row per
source, and its `html` field lists the elements it could not carry, for
example `object, spanning table, svg`:

```bash
uv run --with pyyaml ~/agents/scripts/related-work \
  --dir research/speech-recognition/surveys/compact-asr-training \
  fetch --refetch pratap2023-mms
```

After that, inspect `extract/pratap2023-mms/html/2305.13516v1.md` around
Figures 1, 10 and 11.

## Fix sketch

- **Figures from HTML.** In `preprocess_html`, save each inline `<svg>` and
  each `<object>`/`<embed>` data file as a figure asset, and replace it with
  a Markdown image link carrying the caption. Handle `<img>` already present
  the same way the PDF path does, and stage the result through the existing
  asset staging. Exclude figure-internal text from the fidelity blocks, so
  axis labels no longer count as lost prose.
- **Tables.** Emit tables with row or column spans as HTML tables inside
  the Markdown, which renders on GitHub and in Quarto, or as figure assets
  when they carry layout. Leave LaTeX equation arrays as display math, not
  pipe rows.
- **Converter choice.** Compare a stronger paper converter against the
  current pinned `html2text`: pandoc HTML→GFM with raw-HTML fallback,
  arXiv's LaTeXML structure, or marker on the PDF with the SVG recut. Pick
  per source type by measured fidelity and asset completeness, not by
  preference.
- **Acceptance.** Extend the fidelity result to count figures and tables in
  the source against assets and tables in the Markdown, so a dropped figure
  is reported the way a dropped paragraph is.
- **PDF downloads.** Record the actual content type and first bytes of a
  failed PDF download before retrying, so rate-limit or HTML error pages
  are diagnosable.

2026-09-30 — Contributing-model: opus-5.5
