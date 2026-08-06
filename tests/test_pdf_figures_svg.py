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


def make_pdf(path: Path) -> None:
    """A one-page PDF whose only content is a filled rectangle at VECTOR_BOX.

    PDF y grows upward, so the rectangle's `re` operator states the box
    flipped about the page height.
    """
    x0, y0, x1, y1 = VECTOR_BOX
    stream = f"0 0 0 rg {x0} {PAGE[1] - y1} {x1 - x0} {y1 - y0} re f\n".encode()
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


def make_extract(directory: Path, crops: dict[str, tuple[int, int]], blocks: list[dict]) -> Path:
    """Lay out one marker-shaped extract; return the markdown path."""
    directory.mkdir(parents=True, exist_ok=True)
    make_pdf(directory / "source.pdf")
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
            "--pdf", str(markdown.parent / "source.pdf"),
            "--blocks", str(markdown.parent / "blocks.json"),
            "--markdown", str(markdown),
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
            rows(proc)["_page_0_Figure_1.png"]["status"] == "geometry-mismatch", proc.stdout
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
        _assert(rows(proc)["_page_0_Figure_7.png"]["status"] == "no-geometry", proc.stdout)


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
        _assert(markdown.read_text() == before, "markdown was rewritten under --dry-run")
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
        _assert(rows(again)["_page_0_Figure_1.svg"]["status"] == "already", again.stdout)


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
        _assert(json.loads(proc.stderr)["error"]["code"] == "not_found", proc.stderr)


def test_help_advertises_the_acli_capability_line():
    proc = subprocess.run([str(TOOL), "--help"], capture_output=True, text=True)
    _assert(proc.returncode == 0, proc.stderr)
    _assert("acli: 1 complete" in proc.stdout, proc.stdout[-300:])
    _assert("# acli: 1 complete" in TOOL.read_text()[:1024], "marker must sit in the first 1 KiB")


def _collect_tests():
    return [(name, fn) for name, fn in sorted(globals().items()) if name.startswith("test_")]


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
            print(f"PASS  {name}" if verbose else ".", end="" if not verbose else "\n", flush=True)
        except Exception:
            failed += 1
            failures.append((name, traceback.format_exc()))
            print(f"FAIL  {name}" if verbose else "F", end="" if not verbose else "\n", flush=True)
    if not verbose:
        print()
    for name, tb in failures:
        print(f"\n--- {name} ---\n{tb}")
    print(f"\n{passed} passed, {failed} failed in {time.time() - start:.2f}s")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
