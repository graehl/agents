# research-survey sketches

Dormant or candidate designs for the survey system; not current guidance.

## High-fidelity rendered html→md (user-proposed 2026-08-15)

The shared `scripts/related-work` engine now owns the basic derivation; this is
the fidelity-preserving variant, parked as not worth heavy investment now.

**Proposal.** Derive the searchable `.md` from fetched HTML; for any
*over-spanned* region — markup that does not map well to markdown — render
the region and embed it as SVG (raster fallback) sized to similar
end-visual bounds, with the region's full text as alt text so search
fidelity survives rasterization.

**Design notes (2026-08-15):**

- Per-block classifier, not per-page: map LaTeXML block classes
  (`ltx_para`, sections, lists, simple tables) to md; route to the render
  path only blocks failing a mappability test (tag-to-text ratio or
  nesting depth over threshold, interactive elements, layout-bearing
  markup).
- arXiv shrinks the problem: LaTeXML embeds the source TeX per equation
  (`annotation encoding="application/x-tex"`; measured 84 equations in
  the GEPA extract), so math extracts losslessly as `$...$`, and figures
  are already image assets to copy and link. The over-spanned set is
  nearly empty for arXiv; the render path is the general-web fallback
  (blog posts, interactive pages, monster tables).
- Rendering: headless-browser snapshot of the block's layout box at a
  fixed CSS pixel width — that fixed width is what "similar end-visual
  bounds" pins down; prefer vector output where the region is vector,
  raster otherwise (same philosophy as `scripts/pdf-figures-svg` for
  marker extracts).
- Alt text: whitespace-normalized textContent of the region; overflow
  long text into an adjacent `<details>` block so `rg` still reaches it.
- No silent caps: the tool names every region it rendered rather than
  passing over it (`pdf-figures-svg` precedent).
- Measured motivation for md at all: arXiv HTML runs ~4.5× text bytes
  (harnessfix extract: 408 KB html, 90 KB stripped text, 3227 lines, max
  line 1807 chars) — fine for `rg`, wasteful for full agent reads;
  uniform md also gives downstream applications one chunking and link
  format.

Wake conditions: an application that needs format uniformity across
extracts (corpus feeding, stable chunking), or a survey ingesting
non-arXiv sources where the over-spanned set is non-trivial.
