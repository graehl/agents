---
slug: extract-source-location-links
noticed: 2026-09-30
where: scripts/related-work (_verify_visible_blocks, run_marker), scripts/pdf-figures-svg
---

# Link suspicious extract regions to their place in the original

User-raised. Contributing-model: opus-5.5.

An extract region that may be wrong should carry a link to the exact spot in
the original, so a reader can check it in one click instead of hunting
through the paper. Regions in scope: a block the fidelity gate tolerated but
flagged, a figure or table that could not be preserved, a missing image, or
any text the converter could not place. Today the whole extract gets one
source link at the top (`**Source:**`, see `topics/research-survey.md`), and
the location of a tolerated block is lost.

## Where the locations come from

- **PDF path.** marker already dumps per-block geometry (`blocks.json`: page
  and polygon for every block), which `pdf-figures-svg` uses to recut vector
  figures. The same geometry gives each block a page number, so a link can
  be `…/pdf/<id>#page=<n>`. PDF viewers honor `#page`; a highlighted region
  would need a rendered crop, which `pdf-figures-svg` can already produce.
- **HTML path.** arXiv's LaTeXML HTML gives nearly every paragraph, list
  item, figure and table a stable `id` (`S1.I1.i1.p1`, `S4.F10`). The
  fidelity gate scores source blocks one by one, so it knows each flagged
  block's id and can link `https://arxiv.org/html/<id>#<anchor>`. Other HTML
  sources have fewer ids; the nearest ancestor with an id is the fallback.

## Shape

- Flagged or placeholder regions get a short inline marker after the region:
  `[check original](…#anchor)` or `[PDF p. 7](…#page=7)`.
- The `.fetched` fidelity record lists the flagged anchors, so an audit or a
  reader can find them without scanning the Markdown.
- Unflagged prose gets no per-paragraph links; the aim is to point at doubt,
  not to annotate everything.

## Open decisions

- Whether tolerated blocks should be marked in the Markdown itself or only
  listed in the record.
- Whether marker's per-block confidence or OCR-error flags are worth
  surfacing the same way.
- How to keep the marker text short enough not to disrupt reading.
