"""Cheap page-occupancy model from cached Markdown ASTs and figure sizes.

The model needs one full build first: TeX records the column geometry in
`<jobname>.layout` and each placed image box in `<jobname>.images`. Later
estimates reparse only changed fragments, reuse figure dimensions by content
hash, and scale text/table cost by a coefficient calibrated against the last
full build's measured main-body length.
"""

from __future__ import annotations

import json
import math
import re
import subprocess
from pathlib import Path

from .manuscript import digest, print_asset

TEX_POINTS_PER_INCH = 72.27


def load_cache(output: Path) -> dict:
    path = output / "estimate-cache.json"
    return json.loads(path.read_text()) if path.exists() else {}


def save_cache(output: Path, cache: dict) -> None:
    (output / "estimate-cache.json").write_text(
        json.dumps(cache, ensure_ascii=False) + "\n"
    )


def section_blocks(path: Path, quarto: str, cache: dict) -> list:
    """Pandoc AST blocks of one fragment, reparsed only when its hash changes."""
    sections = cache.setdefault("sections", {})
    fingerprint = digest(path)
    entry = sections.get(str(path))
    if not entry or entry["sha256"] != fingerprint:
        result = subprocess.check_output(
            [quarto, "pandoc", "--from=markdown", "--to=json", str(path)], text=True
        )
        entry = {"sha256": fingerprint, "ast": json.loads(result)["blocks"]}
        sections[str(path)] = entry
    return entry["ast"]


def image_sources(node) -> list[str]:
    found = []

    def visit(value):
        if isinstance(value, list):
            for child in value:
                visit(child)
        elif isinstance(value, dict):
            if value.get("t") == "Image":
                found.append(value["c"][2][0])
            visit(value.get("c", []))

    visit(node)
    return found


def inline_text(value):
    if isinstance(value, list):
        return "".join(map(inline_text, value))
    if not isinstance(value, dict):
        return ""
    kind, content = value["t"], value.get("c", [])
    if kind == "Str":
        return content
    if kind in {"Space", "SoftBreak", "LineBreak"}:
        return " "
    if kind in {"Code", "Math"}:
        return content[1]
    if kind == "Image":
        return ""  # Pandoc's Figure caption owns this text; image alt duplicates it.
    if kind in {"Link", "Cite", "Span"}:
        return inline_text(content[1])
    if kind in {"RawInline", "RawBlock"}:
        return ""
    return inline_text(content)


def figure_size(path: Path, cache: dict):
    key = str(path)
    fingerprint = digest(path)
    old = cache.get(key)
    if old and old["sha256"] == fingerprint:
        return old, True
    info = subprocess.check_output(["pdfinfo", "-box", str(path)], text=True)
    size = re.search(r"^Page size:\s+([\d.]+) x ([\d.]+) pts", info, re.MULTILINE)
    pages = re.search(r"^Pages:\s+(\d+)", info, re.MULTILINE)
    if not size or not pages or int(pages[1]) != 1:
        raise ValueError(f"Expected a one-page PDF figure: {path}")
    entry = {
        "sha256": fingerprint,
        "width_pt": float(size[1]),
        "height_pt": float(size[2]),
    }
    cache[key] = entry
    return entry, False


def read_geometry(output: Path, jobname: str) -> dict:
    path = output / f"{jobname}.layout"
    if not path.exists():
        raise ValueError(
            "Run one full build first to record the page and column geometry"
        )
    geometry = dict(line.split("=") for line in path.read_text().splitlines())
    return {key: int(value) / 65536 for key, value in geometry.items()}


class SectionMeter:
    """Column occupancy of one fragment's text, tables, and figures."""

    def __init__(self, geometry, settings, span, resource_dirs, figures, model):
        self.geometry, self.settings, self.span = geometry, settings, span
        self.resource_dirs, self.figures, self.model = resource_dirs, figures, model
        self.chars_per_line = geometry["column"] / settings["char-advance-pt"]
        self.lines_per_column = geometry["height"] / geometry["baseline"]
        self.float_width = span * geometry["column"] + (span - 1) * geometry["gap"]
        self.images = []

    def measure(self, path: Path, blocks: list) -> dict:
        self.path = path
        self.stats = {
            "section": str(path),
            "words": 0,
            "characters": 0,
            "text_lines": 0.0,
            "table_columns": 0.0,
            "figure_columns": 0.0,
        }
        self.visit(blocks)
        stats = self.stats
        stats["text_columns"] = stats.pop("text_lines") / self.lines_per_column
        return stats

    def count(self, text):
        self.stats["words"] += len(text.split())
        self.stats["characters"] += len(text)

    def visit(self, node):
        if isinstance(node, list):
            for child in node:
                self.visit(child)
            return
        if not isinstance(node, dict):
            return
        kind, content = node["t"], node.get("c", [])
        if kind == "Cite":
            self.visit(content[1])
            return
        if kind == "Note":
            return  # Its words are already included in the containing paragraph.
        if kind == "Div" and "content-hidden" in content[0][1]:
            return
        if kind == "Table":
            self.table(content)
            return
        if kind in {"Para", "Plain", "Header", "CodeBlock"}:
            self.text_block(kind, content)
            # Find images and display math without counting inline prose again.
        if kind == "Image":
            self.image(content[2][0])
            return
        if kind == "Math" and content[0]["t"] == "DisplayMath":
            self.stats["text_lines"] += 2
        self.visit(content)

    def table(self, content):
        # Pandoc table: attr, caption, colspecs, head, bodies, foot.
        span, chars_per_line = self.span, self.chars_per_line
        caption = inline_text(content[1][1])
        self.count(caption)
        rows = list(content[3][1]) + list(content[5][1])
        for body in content[4]:
            rows.extend(body[2])
            rows.extend(body[3])
        ncols = len(content[2])
        row_lines = 0
        for row in rows:
            heights = []
            for cell in row[1]:
                text = inline_text(cell[4])
                self.count(text)
                heights.append(
                    max(
                        1,
                        math.ceil(
                            len(text) / (chars_per_line * span / ncols * cell[3])
                        ),
                    )
                )
            row_lines += max(heights, default=1) + 0.3
        self.stats["table_columns"] += (
            span
            * (row_lines + len(caption) / (span * chars_per_line) + 2)
            / self.lines_per_column
        )

    def text_block(self, kind, content):
        text = (
            content[1]
            if kind == "CodeBlock"
            else inline_text(content[2] if kind == "Header" else content)
        )
        self.count(text)
        lines = max(1, math.ceil(len(text) / self.chars_per_line)) if text else 0
        if kind == "Header":
            lines += 1.5
        elif kind == "CodeBlock":
            lines = (
                sum(
                    max(1, math.ceil(len(line) / self.chars_per_line))
                    for line in text.splitlines()
                )
                + 1
            )
        else:
            lines += 0.2 if text else 0
        self.stats["text_lines"] += lines

    def image(self, source):
        asset = print_asset(source, self.resource_dirs)
        if asset is None:
            raise ValueError(f"Missing print figure for {source} in {self.path}")
        size, hit = figure_size(asset, self.figures)
        if size.get("measured_model") == self.model:
            height, basis = size["measured_height_pt"], "last full build"
        elif self.settings.get("image-height-in"):
            height = self.settings["image-height-in"] * TEX_POINTS_PER_INCH
            basis = "configured fixed image height (not yet measured)"
        else:
            height = size["height_pt"] * self.float_width / size["width_pt"]
            basis = "natural aspect at float width (not yet measured)"
        used = (
            self.span * (height + self.geometry["baseline"]) / self.geometry["height"]
        )
        self.stats["figure_columns"] += used
        self.images.append(
            {
                "source": str(self.path),
                "figure": source,
                "height_pt": round(height, 2),
                "width_columns": self.span,
                "column_heights": round(used, 3),
                "cached": hit,
                "height_basis": basis,
            }
        )


def estimate(build, *, calibrate_pages: float | None = None) -> dict:
    """Estimate main-body pages without invoking TeX.

    `build` supplies `main`, `output`, `jobname`, `quarto`, `resource_dirs`,
    `model_inputs`, `columns`, `float_columns`, and `settings`.
    """
    geometry = read_geometry(build.output, build.jobname)
    settings = build.settings
    columns, span = build.columns, build.float_columns
    cache = load_cache(build.output)
    # A model/style change invalidates calibration, not the PDF dimensions.
    model = {str(path): digest(path) for path in build.model_inputs}
    model["geometry"] = geometry
    model["settings"] = settings
    if cache.get("model") != model:
        cache.pop("calibration", None)
    cache["model"] = model
    figures = cache.setdefault("figures", {})
    if calibrate_pages is not None:
        images = build.output / f"{build.jobname}.images"
        for line in images.read_text().splitlines():
            path, width, height = line.rsplit("|", 2)
            entry, _ = figure_size((build.output / path).resolve(), figures)
            entry["measured_height_pt"] = int(height) / 65536
            entry["measured_width_pt"] = int(width) / 65536
            entry["measured_model"] = model
    meter = SectionMeter(geometry, settings, span, build.resource_dirs, figures, model)
    sections = []
    source_hashes = {}
    for path in build.main:
        blocks = section_blocks(path, build.quarto, cache)
        source_hashes[str(path)] = cache["sections"][str(path)]["sha256"]
        sections.append(meter.measure(path, blocks))
    images = meter.images
    figure_columns = sum(item["figure_columns"] for item in sections)
    nonfigure_columns = sum(
        item["text_columns"] + item["table_columns"] for item in sections
    )
    title_columns = settings["title-columns"]
    if calibrate_pages is not None:
        factor = (
            columns * calibrate_pages - figure_columns - title_columns
        ) / nonfigure_columns
        if factor <= 0:
            raise ValueError(
                "Figure estimate exceeds measured pages; cannot calibrate text/layout cost"
            )
        cache["calibration"] = {
            "factor": factor,
            "main_pages": calibrate_pages,
            "sources": source_hashes,
        }
    calibration = cache.get("calibration")
    factor = calibration["factor"] if calibration else 1.0
    pages = (nonfigure_columns * factor + figure_columns + title_columns) / columns
    save_cache(build.output, cache)
    return {
        "mode": "fast-estimate",
        "estimated_pages": round(pages, 3),
        "words": sum(item["words"] for item in sections),
        "characters": sum(item["characters"] for item in sections),
        "text_and_table_pages": round(nonfigure_columns * factor / columns, 3),
        "figure_pages": round(figure_columns / columns, 3),
        "title_pages": round(title_columns / columns, 3),
        "calibrated": calibration is not None,
        "layout_factor": round(factor, 3),
        "calibration_pages": calibration["main_pages"] if calibration else None,
        "sections": sections,
        "figures": images,
        "caveat": "Heuristic occupancy, not pagination; float packing and line wrapping can differ. Full build decides fit.",
    }
