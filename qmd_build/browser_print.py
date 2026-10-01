"""Print rendered HTML to PDF with headless Chromium, and count PDF pages.

One worker (`print_pdf.mjs`) serves every HTML document build: qmd-html's
`--print-pdf` and hand-assembled pages such as one-page highlights.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
WORKER = PACKAGE / "print_pdf.mjs"
# Any package directory whose node_modules resolve @playwright/test.
DEFAULT_PLAYWRIGHT = Path.home() / "ya/packages/client"


def print_pdf(
    html: Path,
    pdf: Path | None = None,
    *,
    playwright: Path | None = None,
    options: dict | None = None,
    log=None,
) -> Path:
    """Print `html` to `pdf` (default: same stem) and return the PDF path.

    `options` takes `format` (e.g. "A4", "Letter") and `margin`; CSS `@page`
    rules win when present. Worker output goes to `log` (default: inherited).
    """
    pdf = pdf or html.with_suffix(".pdf")
    result = subprocess.run(
        [
            "node",
            str(WORKER),
            str(html),
            str(pdf),
            str(playwright or DEFAULT_PLAYWRIGHT),
            json.dumps(options or {}),
        ],
        stdout=log,
        stderr=log,
        check=False,
    )
    if result.returncode:
        raise ValueError(f"Browser print failed ({result.returncode}) for {html}")
    if not pdf.read_bytes().startswith(b"%PDF-"):
        raise ValueError(f"Browser print produced no valid PDF: {pdf}")
    return pdf


def pdf_page_count(path: Path) -> int:
    info = subprocess.check_output(["pdfinfo", str(path)], text=True)
    match = re.search(r"^Pages:\s+(\d+)$", info, re.MULTILINE)
    if match is None:
        raise ValueError(f"pdfinfo reported no page count for {path}")
    return int(match[1])
