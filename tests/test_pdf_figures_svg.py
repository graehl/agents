#!/usr/bin/env python3
"""Tests for scripts/pdf-figures-svg — marker figure crops recut as vector SVG.

The fixture PDF and crops are built here from stdlib bytes rather than
committed, so the test states the geometry it is asserting on: a page whose
vector content sits at a known rectangle, and crops whose pixel dimensions
either agree with that rectangle or deliberately do not.

The tool itself runs through its `uv run --script` shebang, which is the only
way it gets PyMuPDF; without `uv` on PATH the tests report a skip rather than
a failure.
"""

from __future__ import annotations

import json
import shutil
import struct
import subprocess
import sys
import tempfile
import time
import traceback
import zlib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOL = REPO_ROOT / "scripts" / "pdf-figures-svg"

# The fixture page, in PyMuPDF's top-left-origin points. The filled rectangle
# is the only mark on it, so every other region is empty by construction.
PAGE = (200, 100)
VECTOR_BOX = [20.0, 20.0, 120.0, 60.0]
EMPTY_BOX = [140.0, 10.0, 190.0, 40.0]


def _assert(cond, msg="assertion failed"):
    if not cond:
        raise AssertionError(msg)


def filled_rect(box: list[float]) -> str:
    """A PDF fill operator for `box` in top-left points; PDF y grows upward,
    so the box is stated flipped about the page height."""
    x0, y0, x1, y1 = box
    return f"{x0:.2f} {PAGE[1] - y1:.2f} {x1 - x0:.2f} {y1 - y0:.2f} re f\n"


def dense_marks(box: list[float], count: int) -> str:
    """`count` tiny filled squares scattered deterministically over `box`,
    each its own path, the way a plotting library draws scatter markers."""
    x0, y0, x1, y1 = box
    marks = []
    for i in range(count):
        x = x0 + (i * 7919 % 1000) / 1000 * (x1 - x0 - 0.8)
        y = y0 + (i * 104729 % 1000) / 1000 * (y1 - y0 - 0.8)
        marks.append(filled_rect([x, y, x + 0.8, y + 0.8]))
    return "".join(marks)


def make_pdf(path: Path, stream: str | None = None) -> None:
    """A one-page PDF; by default its only content is a filled rectangle at
    VECTOR_BOX."""
    stream = (
        "0 0 0 rg " + filled_rect(VECTOR_BOX) if stream is None else stream
    ).encode()
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {PAGE[0]} {PAGE[1]}] "
        f"/Contents 4 0 R /Resources << >> >>".encode(),
        b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"endstream",
    ]
    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for number, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += b"%d 0 obj\n" % number + body + b"\nendobj\n"
    xref = len(out)
    out += b"xref\n0 %d\n" % (len(objects) + 1)
    out += b"0000000000 65535 f \n"
    for offset in offsets:
        out += b"%010d 00000 n \n" % offset
    out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (
        len(objects) + 1,
        xref,
    )
    path.write_bytes(bytes(out))


def make_png(path: Path, width: int, height: int) -> None:
    """A solid PNG of the requested pixel size — only its dimensions matter."""

    def chunk(kind: bytes, payload: bytes) -> bytes:
        return (
            struct.pack(">I", len(payload))
            + kind
            + payload
            + struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF)
        )

    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    rows = b"".join(b"\x00" + b"\x80\x80\x80" * width for _ in range(height))
    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", header)
        + chunk(b"IDAT", zlib.compress(rows))
        + chunk(b"IEND", b"")
    )


def make_extract(
    directory: Path,
    crops: dict[str, tuple[int, int]],
    blocks: list[dict],
    stream: str | None = None,
) -> Path:
    """Lay out one marker-shaped extract; return the markdown path."""
    directory.mkdir(parents=True, exist_ok=True)
    make_pdf(directory / "source.pdf", stream)
    for name, (width, height) in crops.items():
        make_png(directory / name, width, height)
    (directory / "blocks.json").write_text(
        json.dumps(
            [
                {
                    "page_id": 0,
                    "polygon": {"bbox": [0.0, 0.0, float(PAGE[0]), float(PAGE[1])]},
                    "children": blocks,
                }
            ]
        )
    )
    markdown = directory / "paper.md"
    markdown.write_text(
        "# Paper\n\n" + "\n\n".join(f"![]({name})" for name in crops) + "\n"
    )
    return markdown


def run(markdown: Path, *argv: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [
            str(TOOL),
            "--pdf",
            str(markdown.parent / "source.pdf"),
            "--blocks",
            str(markdown.parent / "blocks.json"),
            "--markdown",
            str(markdown),
            "--compact",
            *argv,
        ],
        capture_output=True,
        text=True,
    )


def rows(proc: subprocess.CompletedProcess) -> dict[str, dict]:
    parsed = [json.loads(line) for line in proc.stdout.splitlines() if line.strip()]
    return {row["figure"]: row for row in parsed}


def test_vector_region_becomes_svg():
    with tempfile.TemporaryDirectory() as tmp:
        markdown = make_extract(
            Path(tmp) / "paper",
            {"_page_0_Figure_1.png": (200, 80)},
            [{"block_id": 1, "polygon": {"bbox": VECTOR_BOX}}],
        )
        proc = run(markdown)
        _assert(proc.returncode == 0, proc.stderr)
        row = rows(proc)["_page_0_Figure_1.png"]
        _assert(row["status"] == "vector", row)
        _assert(row["bbox"] == VECTOR_BOX, row)

        svg = (markdown.parent / "_page_0_Figure_1.svg").read_text()
        # The rendering contract wants the figure's own size on the root, in
        # points, not a bare viewBox (topics/pareto-figures.md).
        _assert('width="100pt"' in svg and 'height="40pt"' in svg, svg[:200])
        _assert('viewBox="0 0 100 40"' in svg, svg[:200])

        text = markdown.read_text()
        _assert("](_page_0_Figure_1.svg)" in text, text)
        _assert(".png)" not in text, text)
        # The raster crop stays as a fallback rather than being replaced.
        _assert((markdown.parent / "_page_0_Figure_1.png").exists())


def test_empty_region_keeps_the_raster_crop():
    with tempfile.TemporaryDirectory() as tmp:
        markdown = make_extract(
            Path(tmp) / "paper",
            {"_page_0_Figure_2.png": (100, 60)},
            [{"block_id": 2, "polygon": {"bbox": EMPTY_BOX}}],
        )
        proc = run(markdown)
        _assert(proc.returncode == 0, proc.stderr)
        _assert(rows(proc)["_page_0_Figure_2.png"]["status"] == "raster", proc.stdout)
        _assert("](_page_0_Figure_2.png)" in markdown.read_text())
        _assert(not (markdown.parent / "_page_0_Figure_2.svg").exists())


def test_crop_aspect_disagreeing_with_the_bbox_is_refused():
    """Geometry that does not describe this crop must not silently ship."""
    with tempfile.TemporaryDirectory() as tmp:
        # VECTOR_BOX is 100x40 (2.5); a 60x60 crop cannot have come from it.
        markdown = make_extract(
            Path(tmp) / "paper",
            {"_page_0_Figure_1.png": (60, 60)},
            [{"block_id": 1, "polygon": {"bbox": VECTOR_BOX}}],
        )
        proc = run(markdown)
        _assert(proc.returncode == 0, proc.stderr)
        _assert(
            rows(proc)["_page_0_Figure_1.png"]["status"] == "geometry-mismatch",
            proc.stdout,
        )
        _assert("](_page_0_Figure_1.png)" in markdown.read_text())


def test_short_edge_quantization_still_matches():
    """A 3px-tall strip's aspect is only known to a third; do not refuse it."""
    with tempfile.TemporaryDirectory() as tmp:
        strip = [20.0, 20.0, 120.0, 23.0]  # 100x3 pt, aspect 33.3
        markdown = make_extract(
            Path(tmp) / "paper",
            {"_page_0_Figure_1.png": (100, 3)},
            [{"block_id": 1, "polygon": {"bbox": strip}}],
        )
        proc = run(markdown)
        _assert(proc.returncode == 0, proc.stderr)
        _assert(rows(proc)["_page_0_Figure_1.png"]["status"] == "vector", proc.stdout)


def test_missing_geometry_is_named_not_skipped():
    with tempfile.TemporaryDirectory() as tmp:
        markdown = make_extract(
            Path(tmp) / "paper",
            {"_page_0_Figure_7.png": (200, 80)},
            [{"block_id": 1, "polygon": {"bbox": VECTOR_BOX}}],
        )
        proc = run(markdown)
        _assert(proc.returncode == 0, proc.stderr)
        _assert(
            rows(proc)["_page_0_Figure_7.png"]["status"] == "no-geometry", proc.stdout
        )


def test_dry_run_writes_nothing():
    with tempfile.TemporaryDirectory() as tmp:
        markdown = make_extract(
            Path(tmp) / "paper",
            {"_page_0_Figure_1.png": (200, 80)},
            [{"block_id": 1, "polygon": {"bbox": VECTOR_BOX}}],
        )
        before = markdown.read_text()
        proc = run(markdown, "--dry-run")
        _assert(proc.returncode == 0, proc.stderr)
        _assert(rows(proc)["_page_0_Figure_1.png"]["status"] == "vector", proc.stdout)
        _assert(
            markdown.read_text() == before, "markdown was rewritten under --dry-run"
        )
        _assert(not (markdown.parent / "_page_0_Figure_1.svg").exists())


def test_second_run_reports_the_links_it_already_converted():
    with tempfile.TemporaryDirectory() as tmp:
        markdown = make_extract(
            Path(tmp) / "paper",
            {"_page_0_Figure_1.png": (200, 80)},
            [{"block_id": 1, "polygon": {"bbox": VECTOR_BOX}}],
        )
        _assert(run(markdown).returncode == 0)
        again = run(markdown)
        _assert(again.returncode == 0, again.stderr)
        _assert(
            rows(again)["_page_0_Figure_1.svg"]["status"] == "already", again.stdout
        )


# A dense "scatter" fills DENSE_BOX, with an axis rule along its bottom edge
# inside FIGURE_BOX; OTHER_BOX holds a second dense plot elsewhere on the page.
FIGURE_BOX = [10.0, 10.0, 130.0, 90.0]
DENSE_BOX = [20.0, 15.0, 120.0, 75.0]
AXIS_BOX = [15.0, 80.0, 125.0, 81.0]
OTHER_BOX = [140.0, 10.0, 195.0, 90.0]
FIGURE_CROP = (240, 160)  # FIGURE_BOX is 120x80 pt, aspect 1.5


def dense_figure_stream() -> str:
    return (
        "0 0 0 rg "
        + dense_marks(DENSE_BOX, 3000)
        + filled_rect(AXIS_BOX)
        + dense_marks(OTHER_BOX, 3000)
    )


def dense_extract(tmp: str) -> Path:
    return make_extract(
        Path(tmp) / "paper",
        {"_page_0_Figure_1.png": FIGURE_CROP},
        [{"block_id": 1, "polygon": {"bbox": FIGURE_BOX}}],
        dense_figure_stream(),
    )


def test_recut_omits_drawings_outside_the_figure():
    """MuPDF's SVG device writes the whole page's drawings under a clip; the
    figure must carry only its own."""
    with tempfile.TemporaryDirectory() as tmp:
        markdown = dense_extract(tmp)
        proc = run(markdown)
        _assert(proc.returncode == 0, proc.stderr)
        _assert(rows(proc)["_page_0_Figure_1.png"]["status"] == "vector", proc.stdout)
        svg = (markdown.parent / "_page_0_Figure_1.svg").read_text()
        # 3000 in-figure marks plus the axis; the other plot's 3000 are gone.
        paths = svg.count("<path")
        _assert(3000 <= paths < 4000, f"{paths} paths in the figure SVG")


def test_figure_over_budget_rasterizes_only_its_dense_region():
    with tempfile.TemporaryDirectory() as tmp:
        markdown = dense_extract(tmp)
        full = rows(run(markdown, "--dry-run"))["_page_0_Figure_1.png"]["svg_bytes"]
        budget = full // 3
        proc = run(markdown, "--budget-bytes", str(budget))
        _assert(proc.returncode == 0, proc.stderr)
        row = rows(proc)["_page_0_Figure_1.png"]
        _assert(row["status"] == "windowed", row)
        _assert(row["svg_bytes"] <= budget, row)
        _assert(0 < row["raster_fraction"] < 1, row)

        svg = (markdown.parent / "_page_0_Figure_1.svg").read_text()
        _assert("<image" in svg, "no bitmap window in the SVG")
        _assert("<!-- figure_shrink: " in svg[:2000], svg[:2000])
        # Not everything became a bitmap: some marks stay vector paths.
        _assert(svg.count("<path") > 0, "the whole figure was rasterized")
        _assert("](_page_0_Figure_1.svg)" in markdown.read_text())


def test_figure_no_window_set_fits_keeps_its_raster_crop():
    with tempfile.TemporaryDirectory() as tmp:
        markdown = dense_extract(tmp)
        proc = run(markdown, "--budget-bytes", "1000")
        _assert(proc.returncode == 0, proc.stderr)
        row = rows(proc)["_page_0_Figure_1.png"]
        _assert(row["status"] == "oversize", row)
        _assert("](_page_0_Figure_1.png)" in markdown.read_text())
        _assert(not (markdown.parent / "_page_0_Figure_1.svg").exists())


FIDELITY_PROBE = """
import sys
sys.path.insert(0, sys.argv[2])
import pymupdf
import figure_shrink.raster_windows as fs

page = pymupdf.open(sys.argv[1])[0]
figure = pymupdf.Rect(*map(float, sys.argv[3].split(",")))
dense = pymupdf.Rect(*map(float, sys.argv[4].split(",")))
windowed = fs._rasterized_page(page, [fs._snap(dense, figure)])
dropped = fs._page_copy(page)
fs._remove_covered_drawings(dropped[0], [dense])
print(fs.measure_fidelity(page, windowed[0], figure).accepted)
print(fs.measure_fidelity(page, dropped[0], figure).accepted)
"""


def test_render_check_accepts_a_window_and_rejects_lost_marks():
    """The acceptance check must pass a faithful bitmap window and fail a
    region whose marks vanished with no bitmap in their place."""
    with tempfile.TemporaryDirectory() as tmp:
        pdf = Path(tmp) / "dense.pdf"
        make_pdf(pdf, dense_figure_stream())
        proc = subprocess.run(
            [
                "uv",
                "run",
                "--no-project",
                "--with",
                "pymupdf>=1.24",
                "--with",
                "numpy",
                "python3",
                "-c",
                FIDELITY_PROBE,
                str(pdf),
                str(REPO_ROOT),
                ",".join(map(str, FIGURE_BOX)),
                ",".join(map(str, DENSE_BOX)),
            ],
            capture_output=True,
            text=True,
        )
        _assert(proc.returncode == 0, proc.stderr)
        _assert(proc.stdout.split() == ["True", "False"], proc.stdout)


def test_missing_input_exits_not_found():
    with tempfile.TemporaryDirectory() as tmp:
        markdown = make_extract(
            Path(tmp) / "paper",
            {"_page_0_Figure_1.png": (200, 80)},
            [{"block_id": 1, "polygon": {"bbox": VECTOR_BOX}}],
        )
        (markdown.parent / "blocks.json").unlink()
        proc = run(markdown)
        _assert(proc.returncode == 4, (proc.returncode, proc.stderr))
        _assert(
            json.loads(proc.stderr.splitlines()[-1])["error"]["code"] == "not_found",
            proc.stderr,
        )


def test_help_advertises_the_acli_capability_line():
    proc = subprocess.run([str(TOOL), "--help"], capture_output=True, text=True)
    _assert(proc.returncode == 0, proc.stderr)
    _assert("acli: 1 complete" in proc.stdout, proc.stdout[-300:])
    _assert(
        "# acli: 1 complete" in TOOL.read_text()[:1024],
        "marker must sit in the first 1 KiB",
    )


def _collect_tests():
    return [
        (name, fn) for name, fn in sorted(globals().items()) if name.startswith("test_")
    ]


def main(argv: list[str]) -> int:
    if shutil.which("uv") is None:
        print("SKIP  uv not on PATH; pdf-figures-svg cannot resolve PyMuPDF")
        return 0
    verbose = "-v" in argv
    passed = failed = 0
    failures = []
    start = time.time()
    for name, fn in _collect_tests():
        try:
            fn()
            passed += 1
            print(
                f"PASS  {name}" if verbose else ".",
                end="" if not verbose else "\n",
                flush=True,
            )
        except Exception:
            failed += 1
            failures.append((name, traceback.format_exc()))
            print(
                f"FAIL  {name}" if verbose else "F",
                end="" if not verbose else "\n",
                flush=True,
            )
    if not verbose:
        print()
    for name, tb in failures:
        print(f"\n--- {name} ---\n{tb}")
    print(f"\n{passed} passed, {failed} failed in {time.time() - start:.2f}s")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
