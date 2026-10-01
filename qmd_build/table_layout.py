"""Responsive table column widths chosen at build time.

A headless browser runs `table_widths.js` on a first render: for each band of
content-column width it estimates wrapped heights from font metrics, refines
with a few real-layout steps, and reports widths only where they render
shorter than automatic layout. The second render applies the decisions
through `table_widths.lua` (column specifications) and a generated band
stylesheet using container queries; below the narrowest band, and in any
band without a decision, tables keep automatic layout.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from .browser_print import DEFAULT_PLAYWRIGHT

PACKAGE = Path(__file__).resolve().parent
WORKER = PACKAGE / "table_widths.mjs"

# (lowest content-column width in CSS px, width the band is optimized at).
# 672 px is a US Letter page with 0.75 in side margins, so print uses it.
BANDS = [(420, 480), (600, 672), (760, 820)]


def choose_table_widths(
    html: Path, *, playwright: Path | None = None, log=None
) -> list[list[dict | None]]:
    """Per-table, per-band decisions from the headless chooser."""
    options = {"bandWidths": [width for _, width in BANDS]}
    output = subprocess.run(
        [
            "node",
            str(WORKER),
            str(html),
            str(playwright or DEFAULT_PLAYWRIGHT),
            json.dumps(options),
        ],
        stdout=subprocess.PIPE,
        stderr=log,
        text=True,
        check=False,
    )
    if output.returncode:
        raise ValueError(f"Table width chooser failed ({output.returncode}) for {html}")
    return json.loads(output.stdout)


def widest_band_widths(decisions: list[list[dict | None]]) -> list[dict | None]:
    """The AST width per table: the widest band that has a decision."""
    chosen = []
    for bands in decisions:
        decided = [band for band in bands if band]
        chosen.append({"widths": decided[-1]["widths"]} if decided else None)
    return chosen


def band_stylesheet(decisions: list[list[dict | None]]) -> str:
    """Container-query CSS giving each decided table its band's widths."""
    rules = [
        "main { container-type: inline-size; }",
        "table[data-table-widths] col { width: auto !important; }",
    ]
    uppers = [lower for lower, _ in BANDS[1:]] + [None]
    for position, ((lower, _), upper) in enumerate(zip(BANDS, uppers)):
        query = f"(min-width: {lower}px)"
        if upper:
            query += f" and (max-width: {upper - 0.02}px)"
        body = []
        for index, bands in enumerate(decisions):
            band = bands[position]
            if not band:
                continue
            table = f'table[data-table-widths="{index}"]'
            body.append(f"{table} {{ table-layout: fixed; width: 100%; }}")
            body += [
                f"{table} col:nth-child({column + 1}) {{ width: {100 * fraction:.2f}% !important; }}"
                for column, fraction in enumerate(band["widths"])
            ]
        if body:
            rules.append(f"@container {query} {{\n  " + "\n  ".join(body) + "\n}")
    return "\n".join(rules) + "\n"
