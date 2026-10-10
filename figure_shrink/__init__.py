"""figure_shrink — byte limits for survey extract figures.

This package's top level is dependency-free so `scripts/related-work`, which
runs on a bare Python, can enforce the same limits it states. The fitting
itself, which needs PyMuPDF and NumPy, is in `figure_shrink.raster_windows`.
Contract: topics/research-survey.md (extract figures).
"""

# A figure at or under this size keeps its full vector form; a larger one is
# fitted under it by rasterizing its densest regions (user-set, 2026-10-10).
BUDGET_BYTES = 10_000_000
# No committed extract asset may exceed this. Twice the budget leaves room
# for source-faithful assets the budget does not rewrite, and stays far
# under GitHub's 100 MB push limit and 50 MB warning.
ASSET_CEILING_BYTES = 20_000_000
