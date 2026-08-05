---
slug: paper-extract-vector-figures
noticed: 2026-08-05
where: scripts/related-work run_marker
---

**Gap:** figures come out of PDF extraction as raster, even when the source
is vector. marker rewrites each figure region to a JPEG crop, so
`surveys/llm-intelligence/related-work/extract/alain2016-probes/` holds
`_page_3_Figure_1.jpeg` at 499×287 for a figure whose PDF original is
resolution-free. Whether that crop happens to be readable is luck of the
draw — `_page_12_Figure_1.jpeg` at 893×1000 reads fine, while the 499×287
one renders a hex listing at the edge of legibility and clips its top row —
and it is decided once, at extraction time, by marker's chosen resolution.
No later zoom recovers what the crop did not capture, which is the one thing
a durable full-text extract is there to protect. Vector figures keep that
detail for free, and would also render inline at full quality in YA's doc
view (`topics/pareto-figures.md` § Rendering contract).

**Noticed while:** adding inline SVG sizing to YA's markdown render, then
checking whether the paper-retrieval helper could feed it vector figures.

**Fix sketch:** the block geometry is already available — `marker_single
--output_format json` returns per-block `bbox`/`polygon` for each figure —
so the pass is: run the JSON renderer alongside markdown, crop the source
PDF page to each figure's bbox, convert that region to SVG, and rewrite the
markdown link to the `.svg` when the conversion produced real vector content
(a page that is itself a scan yields one big embedded image, where the JPEG
is the honest artifact and the SVG buys nothing). Keep the JPEG as a
fallback rather than replacing it, since the sentinel treats a missing
figure as a fetched extract.

Blocked on tooling, not design: the crop-to-SVG step needs a vector-capable
PDF tool and this host has none — `pdftocairo`, `mutool`, `pdf2svg`, `qpdf`,
`inkscape` are all absent from `PATH`, and `fitz`/`pymupdf` does not import.
`pypdfium2` (already a marker dependency) renders but cannot emit SVG. The
least-friction unblock is `pip install pymupdf` for `page.get_svg_image()`,
weighed against its AGPL licensing; poppler or mupdf CLIs want a system
package. Do not add the pass while it would silently no-op on every host
that lacks the converter.
