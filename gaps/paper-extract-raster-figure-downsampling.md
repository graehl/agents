---
slug: paper-extract-raster-figure-downsampling
noticed: 2026-08-06
where: scripts/pdf-figures-svg, scripts/related-work run_marker
---

**Gap:** a figure whose PDF original is a *placed bitmap* still reaches the
extract downsampled, and by a large factor. marker crops figure regions out
of a page rendered at 192 dpi, which is unrelated to the resolution the
bitmap was embedded at. In `alain2016-probes`,
`_page_8_Figure_2.jpeg` is 261×198 for an image embedded at 2000×1500 —
a 7.7× linear loss — and `_page_3_Figure_3.jpeg` is 518×322 for a 1920×1200
original. The vector pass (`scripts/pdf-figures-svg`) correctly leaves these
regions as raster, since wrapping the same pixels in SVG buys nothing; it
reports the placed image's native size on the `raster` row, which is where
these numbers came from.

**Noticed while:** adding the vector-figure recut that closed
`paper-extract-vector-figures`.

**Fix sketch:** the geometry is already in hand. On a `raster` row where one
placed image covers the region and its native pixels exceed the crop's,
extract that image object at native resolution
(`pymupdf.Document.extract_image(xref)`) instead of keeping marker's crop —
after checking the image's placement is not itself a crop of a larger
original, in which case the region must be cut from the native pixels rather
than taken whole. Keep marker's crop as the fallback, same as the SVG path.
Two cases to leave alone: a region covered by several placed images (the
composite is what the figure is), and an image whose native resolution is at
or below the crop's, where marker's render is already the better artifact.

**Related, same seam:** marker's figure bbox can sit *inside* the artwork.
`_page_3_Figure_1`'s bbox is 102.5–289.5 pt where the placed image spans
101.3–292.9 pt, which is why that crop shears the top row off a hex listing.
Padding the bbox would fix the shear and would equally risk pulling a
neighbouring caption's glyph row into a tight two-column layout, so
`pdf-figures-svg` deliberately has no `--pad`. Extracting the placed image
whole, as above, sidesteps the question for the raster case.
