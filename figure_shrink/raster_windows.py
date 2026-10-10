"""figure_shrink.raster_windows — fit an oversized vector figure under a byte
budget by rasterizing only its densest regions.

A figure recut from a PDF as SVG can be enormous when it draws hundreds of
thousands of marks (a dense scatter plot is the usual case), while the same
figure's axes, labels and sparse marks cost almost nothing. Rasterizing the
whole figure throws away the zoomable part to save bytes that part never
cost. This module instead charges the figure's drawing operations to a grid,
turns the regions with the highest cost per unit area into embedded bitmap
windows, and leaves every other region vector. It needs no understanding of
what the marks mean.

Two stages, cheapest first:

1. `isolated_figure` drops drawings that lie wholly outside the figure.
   MuPDF's SVG device clips to the crop box but still writes every drawing
   on the page, so this alone can shrink a figure several-fold, losslessly.
2. `shrink_figure`, only for a figure still over budget, rasterizes windows.
   A result is accepted only after rendering it against the source at
   `CHECK_DPI`: a window may lose detail beyond its own raster resolution,
   never content visible at print resolution.

Callers need PyMuPDF and NumPy; `scripts/pdf-figures-svg` declares both.
Contract: topics/research-survey.md (extract figures).
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass

import numpy as np
import pymupdf

from figure_shrink import BUDGET_BYTES

__all__ = [
    "BUDGET_BYTES",
    "CHECK_DPI",
    "RASTER_DPI",
    "FigureFidelity",
    "ShrunkFigure",
    "figure_svg",
    "isolated_figure",
    "measure_fidelity",
    "shrink_figure",
]

# Windows are rasterized at print resolution, and the check renders at the
# same resolution, so a window's bitmap maps onto check pixels one to one.
RASTER_DPI = 300
CHECK_DPI = RASTER_DPI
# MuPDF grid-fits a placed image to whole device pixels, shifting its edges
# by up to a pixel against the vector drawing it replaced. The check forgives
# a shift of this many pixels in any direction; a missing or altered mark has
# no nearby pixel that explains it and still counts.
SHIFT_TOLERANCE = 1
# Cost is charged on a GRID x GRID lattice over the figure: fine enough to
# separate a plot's interior from its axes and labels on every fixture seen,
# coarse enough that window bookkeeping stays negligible.
GRID = 32
# Acceptance, after the shift tolerance: mean absolute channel error
# (diffuse degradation), the share of pixels whose worst channel differs by
# more than VISIBLE_DELTA, and the worst BLOCK x BLOCK pixel block's mean
# error (one lost mark). Calibrated on the densest fixture, a 9-panel
# scatter plot of 86k markers: rasterizing it whole at RASTER_DPI scores
# mean 0.0020, visible 0.0000, block 0.042, while deleting the marks in one
# 40x100 pt window without a bitmap scores visible 0.0037, block 0.750, and
# a 200-dpi bitmap scores block 0.117.
MAX_MEAN_ERROR = 0.005
VISIBLE_DELTA = 0.25
MAX_VISIBLE_FRACTION = 0.001
BLOCK = 8
MAX_BLOCK_ERROR = 0.1
# Projected sizes aim this far under the budget, because the projection
# prices bitmaps by area and drawings by operation count.
PROJECTION_MARGIN = 0.9
# Measured exports allowed before giving up; each one grows the window set.
MAX_EXPORTS = 4
# A drawing this large is the page's background or frame, not figure content.
BACKGROUND_AREA_FRACTION = 0.9

_SVG_ROOT_SIZE = re.compile(r'(<svg\b[^>]*?)width="([\d.]+)"\s+height="([\d.]+)"')


@dataclass(frozen=True)
class FigureFidelity:
    """How closely a rewritten figure renders like its source region."""

    mean_error: float
    visible_fraction: float
    worst_block: float

    @property
    def accepted(self) -> bool:
        return (
            self.mean_error <= MAX_MEAN_ERROR
            and self.visible_fraction <= MAX_VISIBLE_FRACTION
            and self.worst_block <= MAX_BLOCK_ERROR
        )

    def describe(self) -> str:
        return (
            f"mean={self.mean_error:.4f} "
            f"visible={self.visible_fraction:.4f} "
            f"block={self.worst_block:.3f}@{CHECK_DPI}dpi"
        )


@dataclass(frozen=True)
class ShrunkFigure:
    """An SVG that fits the budget, and the bitmap windows that got it there."""

    svg: str
    windows: list[pymupdf.Rect]
    raster_fraction: float
    fidelity: FigureFidelity


def _size_in_points(svg: str) -> str:
    """Restate the root width/height in points (topics/pareto-figures.md):
    MuPDF writes them unitless, which a browser reads as CSS pixels."""
    return _SVG_ROOT_SIZE.sub(r'\1width="\2pt" height="\3pt"', svg, count=1)


def figure_svg(page: pymupdf.Page, rect: pymupdf.Rect) -> str:
    """The page region `rect` rendered through MuPDF's SVG device."""
    cropbox = pymupdf.Rect(page.cropbox)
    try:
        page.set_cropbox(rect)
        return _size_in_points(page.get_svg_image(text_as_path=True))
    finally:
        page.set_cropbox(cropbox)


def _page_copy(page: pymupdf.Page) -> pymupdf.Document:
    copy = pymupdf.open()
    copy.insert_pdf(page.parent, from_page=page.number, to_page=page.number)
    return copy


def _remove_covered_drawings(page: pymupdf.Page, regions: list[pymupdf.Rect]) -> None:
    """Remove the vector drawings each region wholly covers.

    Text and images stay: cutting glyphs that straddle a region edge would
    show as damage outside it, and a drawing that crosses the edge stays for
    the same reason.
    """
    regions = [region for region in regions if not region.is_empty]
    if not regions:
        return
    for region in regions:
        page.add_redact_annot(region, fill=False, cross_out=False)
    page.apply_redactions(
        images=pymupdf.PDF_REDACT_IMAGE_NONE,
        graphics=pymupdf.PDF_REDACT_LINE_ART_REMOVE_IF_COVERED,
        text=pymupdf.PDF_REDACT_TEXT_NONE,
    )


def isolated_figure(page: pymupdf.Page, rect: pymupdf.Rect) -> pymupdf.Document:
    """A one-page copy of `page` without the drawings wholly outside `rect`."""
    copy = _page_copy(page)
    full = copy[0].rect
    _remove_covered_drawings(
        copy[0],
        [
            pymupdf.Rect(full.x0, full.y0, full.x1, rect.y0),
            pymupdf.Rect(full.x0, rect.y1, full.x1, full.y1),
            pymupdf.Rect(full.x0, rect.y0, rect.x0, rect.y1),
            pymupdf.Rect(rect.x1, rect.y0, full.x1, rect.y1),
        ],
    )
    return copy


def _pixels(page: pymupdf.Page, rect: pymupdf.Rect) -> np.ndarray:
    pixmap = page.get_pixmap(clip=rect, dpi=CHECK_DPI, alpha=False)
    return np.frombuffer(pixmap.samples, dtype=np.uint8).reshape(
        pixmap.height, pixmap.width, pixmap.n
    )


def measure_fidelity(
    page: pymupdf.Page, rewritten: pymupdf.Page, rect: pymupdf.Rect
) -> FigureFidelity:
    """Compare the region of a rewritten copy of `page` against the original.

    Both sides go through MuPDF's page renderer. Rendering the exported SVG
    instead would measure MuPDF's SVG interpreter against its PDF renderer,
    which disagree on an untouched figure (mean error 0.017 on a fixture)
    by more than the loss being bounded; the SVG export is the step every
    recut takes, rasterized or not.
    """
    reference = _pixels(page, rect)[..., :3].astype(np.int16)
    rendered = _pixels(rewritten, rect)[..., :3].astype(np.int16)
    reach = SHIFT_TOLERANCE
    padded = np.pad(rendered, ((reach, reach), (reach, reach), (0, 0)), mode="edge")
    height, width = reference.shape[:2]
    delta = np.full(reference.shape, 255, dtype=np.int16)
    for dy in range(2 * reach + 1):
        for dx in range(2 * reach + 1):
            shifted = padded[dy : dy + height, dx : dx + width]
            np.minimum(delta, np.abs(reference - shifted), out=delta)
    delta = delta / 255.0
    worst = delta.max(axis=2)
    rows, columns = (worst.shape[0] // BLOCK) * BLOCK, (worst.shape[1] // BLOCK) * BLOCK
    blocks = worst[:rows, :columns].reshape(
        rows // BLOCK, BLOCK, columns // BLOCK, BLOCK
    )
    return FigureFidelity(
        mean_error=float(delta.mean()),
        visible_fraction=float((worst > VISIBLE_DELTA).mean()),
        worst_block=float(blocks.mean(axis=(1, 3)).max()) if blocks.size else 0.0,
    )


class _FigureCosts:
    """Where a figure's drawing operations sit, for pricing window sets.

    Operation count stands in for SVG bytes because the SVG device writes
    one path command per drawing item.
    """

    def __init__(self, page: pymupdf.Page, rect: pymupdf.Rect):
        page_area = page.rect.get_area()
        boxes, costs = [], []
        for drawing in page.get_drawings():
            box = drawing["rect"]
            if box.get_area() < BACKGROUND_AREA_FRACTION * page_area and rect.contains(
                box
            ):
                boxes.append(tuple(box))
                costs.append(len(drawing["items"]))
        self.boxes = np.array(boxes, dtype=float).reshape(-1, 4)
        self.costs = np.array(costs, dtype=float)
        self.total = float(self.costs.sum())
        self.grid = np.zeros((GRID, GRID))
        if len(self.costs):
            centres_x = (self.boxes[:, 0] + self.boxes[:, 2]) / 2
            centres_y = (self.boxes[:, 1] + self.boxes[:, 3]) / 2
            columns = np.minimum(
                GRID - 1, ((centres_x - rect.x0) / rect.width * GRID).astype(int)
            )
            rows = np.minimum(
                GRID - 1, ((centres_y - rect.y0) / rect.height * GRID).astype(int)
            )
            np.add.at(self.grid, (rows, columns), self.costs)

    def removed(self, windows: list[pymupdf.Rect]) -> float:
        """Cost of the drawings some single window wholly covers."""
        covered = np.zeros(len(self.costs), dtype=bool)
        for window in windows:
            covered |= (
                (self.boxes[:, 0] >= window.x0)
                & (self.boxes[:, 1] >= window.y0)
                & (self.boxes[:, 2] <= window.x1)
                & (self.boxes[:, 3] <= window.y1)
            )
        return float(self.costs[covered].sum())


def _snap(window: pymupdf.Rect, rect: pymupdf.Rect) -> pymupdf.Rect:
    """Grow `window` to whole raster pixels, within the figure, so its
    bitmap is placed without resampling across a fractional pixel."""
    step = 72.0 / RASTER_DPI
    return pymupdf.Rect(
        max(rect.x0, math.floor(window.x0 / step) * step),
        max(rect.y0, math.floor(window.y0 / step) * step),
        min(rect.x1, math.ceil(window.x1 / step) * step),
        min(rect.y1, math.ceil(window.y1 / step) * step),
    )


def _windows(selected: np.ndarray, rect: pymupdf.Rect) -> list[pymupdf.Rect]:
    """Bounding boxes of the selected cells' connected regions, merged until
    none overlap. A box rather than the exact cell set, so a mark straddling
    two selected cells is wholly inside one window and gets removed."""
    labels = np.zeros(selected.shape, dtype=int)
    boxes: list[list[int]] = []
    for start in zip(*np.nonzero(selected)):
        if labels[start]:
            continue
        boxes.append([start[0], start[1], start[0] + 1, start[1] + 1])
        labels[start] = len(boxes)
        stack = [start]
        while stack:
            row, column = stack.pop()
            box = boxes[-1]
            box[0], box[1] = min(box[0], row), min(box[1], column)
            box[2], box[3] = max(box[2], row + 1), max(box[3], column + 1)
            for neighbour in (
                (row - 1, column),
                (row + 1, column),
                (row, column - 1),
                (row, column + 1),
            ):
                if (
                    0 <= neighbour[0] < GRID
                    and 0 <= neighbour[1] < GRID
                    and selected[neighbour]
                    and not labels[neighbour]
                ):
                    labels[neighbour] = len(boxes)
                    stack.append(neighbour)
    merged = True
    while merged:
        merged = False
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                a, b = boxes[i], boxes[j]
                if a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]:
                    boxes[i] = [
                        min(a[0], b[0]),
                        min(a[1], b[1]),
                        max(a[2], b[2]),
                        max(a[3], b[3]),
                    ]
                    del boxes[j]
                    merged = True
                    break
            if merged:
                break
    cell_w = rect.width / GRID
    cell_h = rect.height / GRID
    return [
        _snap(
            pymupdf.Rect(
                rect.x0 + c0 * cell_w,
                rect.y0 + r0 * cell_h,
                rect.x0 + c1 * cell_w,
                rect.y0 + r1 * cell_h,
            ),
            rect,
        )
        for r0, c0, r1, c1 in boxes
    ]


def _rasterized_page(
    page: pymupdf.Page, windows: list[pymupdf.Rect]
) -> pymupdf.Document:
    """A one-page copy of `page` whose windows show bitmaps rendered from the
    original in place of the drawings they wholly cover. A drawing crossing
    a window edge stays vector and is hidden inside the window by the
    opaque bitmap, which shows the same pixels."""
    copy = _page_copy(page)
    _remove_covered_drawings(copy[0], windows)
    for window in windows:
        bitmap = page.get_pixmap(clip=window, dpi=RASTER_DPI, alpha=False)
        # Place the bitmap on the pixel rectangle it was rendered from, which
        # rounding may have grown past `window`; stretching it onto `window`
        # instead shifts every edge by a fraction of a pixel.
        placed = pymupdf.Rect(bitmap.irect) * (72.0 / RASTER_DPI)
        copy[0].insert_image(placed, pixmap=bitmap, keep_proportion=False)
    return copy


def shrink_figure(
    page: pymupdf.Page,
    rect: pymupdf.Rect,
    svg_bytes: int,
    *,
    budget_bytes: int = BUDGET_BYTES,
) -> ShrunkFigure | None:
    """Rasterize the fewest densest windows that bring the figure under
    `budget_bytes`, or None when no window set fits and passes the check.

    `page` comes from `isolated_figure`, and `svg_bytes` is the size of its
    unshrunk export, so cost and budget both describe the figure alone.

    Cells are ranked by drawing cost. A binary search over how many top
    cells to rasterize runs on projected sizes, which are cheap; only the
    chosen window set is exported and measured, and a set that still
    exceeds the budget grows by a quarter and is measured again.
    """
    costs = _FigureCosts(page, rect)
    if not costs.total:
        return None
    order = np.argsort(costs.grid, axis=None)[::-1]
    ranked = [int(index) for index in order if costs.grid.flat[index] > 0]
    full_bitmap = page.get_pixmap(clip=rect, dpi=RASTER_DPI, alpha=False)
    # Bitmaps are embedded as base64 PNG: 4/3 of the PNG bytes.
    bitmap_bytes_per_area = len(full_bitmap.tobytes("png")) * 4 / 3 / rect.get_area()

    def windows_for(count: int) -> list[pymupdf.Rect]:
        selected = np.zeros(GRID * GRID, dtype=bool)
        selected[ranked[:count]] = True
        return _windows(selected.reshape(GRID, GRID), rect)

    def projected(windows: list[pymupdf.Rect]) -> float:
        vector = svg_bytes * (1 - costs.removed(windows) / costs.total)
        return vector + bitmap_bytes_per_area * sum(w.get_area() for w in windows)

    low, high, count = 1, len(ranked), len(ranked)
    while low <= high:
        middle = (low + high) // 2
        if projected(windows_for(middle)) <= PROJECTION_MARGIN * budget_bytes:
            count, high = middle, middle - 1
        else:
            low = middle + 1

    for _ in range(MAX_EXPORTS):
        windows = windows_for(count)
        rewritten = _rasterized_page(page, windows)
        svg = figure_svg(rewritten[0], rect)
        if len(svg.encode()) <= budget_bytes:
            fidelity = measure_fidelity(page, rewritten[0], rect)
            if not fidelity.accepted:
                return None
            area = sum(window.get_area() for window in windows)
            return ShrunkFigure(
                svg=svg,
                windows=windows,
                raster_fraction=area / rect.get_area(),
                fidelity=fidelity,
            )
        if count == len(ranked):
            return None
        count = min(len(ranked), math.ceil(count * 1.25))
    return None
