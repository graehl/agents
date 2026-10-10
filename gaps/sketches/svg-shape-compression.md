---
slug: svg-shape-compression
noticed: 2026-10-10
where: figure_shrink/raster_windows.py, scripts/pdf-figures-svg
---

**Outcome:** an oversized vector figure shrinks by replacing shapes with
fewer or cheaper shapes, staying vector everywhere, before any region is
rasterized. The current regional rasterization (`figure_shrink.raster_windows`)
is acceptable as the standard fallback — it looks fine on a printed page and
never rasterizes the whole figure indiscriminately — but bitmaps stop
zooming past their 300 dpi (user-directed, 2026-10-10).

**Approach:** stages that keep vector form, each accepted by the same
render check the windows use (`measure_fidelity`: 300-dpi render, one-pixel
shift tolerance, mean / visible-pixel / worst-block error), run before
windows and only on figures still over budget.

1. *Invisible-mark culling.* Remove drawings that change no pixel at
   300 dpi: marks wholly hidden under later opaque marks, and marks below
   pixel size that later marks overwrite. One pass finds them with an ID
   buffer: redraw every drawing in painting order with a unique flat colour
   and antialiasing off, read back the 300-dpi image, and keep only drawings
   whose ID wins at least one pixel. Antialiased edges make a drawing that
   wins no pixel in the aliased pass still contribute a fraction of one, so
   the render check, not the ID pass, decides acceptance. Dense scatter
   plots overplot heavily, so this may remove most markers with no visible
   change.
2. *Marker deduplication.* MuPDF already emits glyphs once as `<defs>` and
   `<use>`; scatter markers come out as a full path per mark. Detect paths
   that are translations of one shape and rewrite them as one `<symbol>`
   plus a `<use x= y=>` per mark, which cuts each mark's bytes several-fold
   losslessly.
3. *Coordinate precision.* Round coordinates to the precision that changes
   no pixel at the check resolution (two decimals of a point is under a
   tenth of a 300-dpi pixel), as `svgo`/`scour` do with a fixed precision.
4. *Mass-preserving merge (needs marker recognition).* Within a cell
   smaller than a pixel at the check resolution, replace overlapping
   identical markers with one marker at their mass-weighted centre.

**Unresolved decisions:**

- Whether to operate on PyMuPDF drawings before export (stages 1, 4) or on
  the exported SVG (stages 2, 3), or both; pre-export keeps one geometry
  model with the windows, post-export reaches the `<use>` rewriting.
- How to render the ID buffer: redraw through PyMuPDF `Shape` on a blank
  page, or a separate rasterizer.
- Whether stage order should be cost-driven (try the cheapest that fits)
  or fixed.

**Prior art** (web search 2026-10-10, not read in full): no located tool
compresses SVG lossily under a rasterized-error bound; icon pipelines run
`svgo`/`scour` and pixel-diff by hand
([KDE D29072](https://phabricator.kde.org/D29072),
[Wikimedia T162319](https://phabricator.wikimedia.org/T162319),
[grida](https://grida.co/docs/wg/feat-svg/testing)). Raster-loss
optimization of vector content: diffvg (Li et al., SIGGRAPH Asia 2020,
[project](https://people.csail.mit.edu/tzumao/diffvg)) and LIVE (Ma et al.,
CVPR 2022,
[paper](https://openaccess.thecvf.com/content/CVPR2022/html/Ma_Towards_Layer-Wise_Image_Vectorization_CVPR_2022_paper.html)).
Curve simplification with a geometric error, lossless removals first
([Wang et al. 2023](https://cims.nyu.edu/gcl/papers/2023-Bezier-Simplification.pdf)).
Appearance-preserving scatterplot sampling, which selects points rather
than merging them ([PAwS, arXiv 2504.20369](https://arxiv.org/abs/2504.20369);
[VMV 2023](https://diglib.eg.org/server/api/core/bitstreams/b1c3dee4-1c29-49a8-af9c-0cbd3fee4307/content);
[pyramid sampling, Vis 2021](http://www.yunhaiwang.net/Vis2021/progressive-sampling/progressive_sampling.pdf)).

Contributing-model: opus-5.5
