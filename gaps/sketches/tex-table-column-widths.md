---
slug: tex-table-column-widths
noticed: 2026-10-01
where: qmd_build/table_layout.py, qmd_build/venue_pdf.py
---

# Choose table column widths for LaTeX/PDF builds

User-raised. Contributing-model: opus-5.5.

The `memo` HTML style chooses table column widths at build time per band of
content-column width (`qmd_build/table_layout.py`; see
`topics/document-publishing.md`). LaTeX venue builds (`qmd-venue-pdf`) get
no such choice: tables take the pipe-table dash-count widths or Quarto's
defaults, and a cramped two-column page wraps short tokens badly.

TeX supports a better scoring layout than the browser loop. With exact font
metrics and TeX's own line breaker, a candidate width set can be scored by
total table height plus penalties for hyphenated breaks inside short tokens,
over the one known column width of the venue page. Its natural parameters
differ from the HTML search (fixed geometry, `p{}` versus `X` columns,
`\raggedright` versus justified cells), so it should not reuse the HTML
decisions verbatim. The HTML choice at the nearest band width is still a
cheap first candidate.

Fix sketch: a `print.lua`-adjacent filter that receives per-table widths, a
measurement pass that typesets each table alone at the venue column width
across a few candidate width sets, and a receipt entry recording the choice.
