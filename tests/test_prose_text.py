#!/usr/bin/env python3
"""Tests for prose_text: what counts as prose in Markdown, Quarto, and PDF."""

from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from prose_text import WORD, from_markdown, load


def words(source: str) -> list[str]:
    prose = from_markdown(source)
    return [w for line in prose.lines for w in WORD.findall(line.text)]


class Markdown(unittest.TestCase):
    def test_lines_keep_source_length_and_numbers(self) -> None:
        source = "Intro with `code` and https://x.test/a.\n\nSecond [@key] line.\n"
        prose = from_markdown(source)
        raw = source.split("\n")
        for line in prose.lines:
            self.assertEqual(len(line.text), len(raw[line.number - 1]))

    def test_quarto_markup_is_not_prose(self) -> None:
        source = (
            "---\ntitle: Paper\n---\n\n"
            "::: {.callout-note}\n"
            "The loss $\\mathcal{L}$ falls {{< include _x.qmd >}} fast.\n"
            ":::\n\n"
            "$$\nE = mc^2\n$$\n\n"
            "Heading text {#sec-x .unnumbered} here.\n\n"
            "```{python}\nprose_inside_code = 1\n```\n"
        )
        self.assertEqual(
            words(source), ["The", "loss", "falls", "fast", "Heading", "text", "here"]
        )

    def test_citations_are_not_prose(self) -> None:
        cases = {
            "As shown [@smith2020; @lee2019, p. 3] it holds.": [
                "As",
                "shown",
                "it",
                "holds",
            ],
            "As @smith2020 argues, it holds.": ["As", "argues", "it", "holds"],
            "It holds [3, 5-7].": ["It", "holds"],
            "It holds (Smith et al., 2020; Lee 2019).": ["It", "holds"],
            "It holds \\citep{smith2020}.": ["It", "holds"],
            "Smith et al. (2020) show it.": ["Smith", "show", "it"],
        }
        for source, expected in cases.items():
            with self.subTest(source=source):
                self.assertEqual(words(source), expected)

    def test_prices_and_slashed_words_stay_emails_go(self) -> None:
        self.assertEqual(
            words("It costs $5 and $10 and/or mail a@b.org now."),
            ["It", "costs", "and", "and", "or", "mail", "now"],
        )

    def test_paths_identifiers_and_flags_are_not_prose(self) -> None:
        source = (
            "Run scripts/not-ai-lint on ~/agents/topics/writing.md with --limit "
            "and load_lexicon from README.md, then stop."
        )
        self.assertEqual(
            words(source), ["Run", "on", "with", "and", "from", "then", "stop"]
        )

    def test_references_section_is_skipped_until_next_peer_heading(self) -> None:
        source = (
            "## Results\n\nIt works.\n\n## References\n\nSmith, J. A tapestry. 2020.\n\n"
            "### Extra refs\n\nLee. Delve. 2019.\n\n## Appendix\n\nMore prose.\n"
        )
        prose = from_markdown(source)
        self.assertEqual(
            [w for line in prose.lines for w in WORD.findall(line.text)],
            ["Results", "It", "works", "Appendix", "More", "prose"],
        )
        self.assertTrue(any("References" in note for note in prose.notes))

    def test_quarto_refs_div_is_skipped(self) -> None:
        source = "Body text.\n\n::: {#refs}\nSmith. A tapestry.\n:::\n\nAfter.\n"
        self.assertEqual(words(source), ["Body", "text", "After"])

    def test_figure_caption_is_prose_of_its_own_kind(self) -> None:
        prose = from_markdown("![A cache diagram](fig.png){#fig-cache}\n")
        self.assertEqual(prose.lines[0].kind, "figure")
        self.assertEqual(WORD.findall(prose.lines[0].text), ["A", "cache", "diagram"])


def _minimal_pdf(pages: list[list[str]]) -> bytes:
    """A valid PDF with one Helvetica text line per list item on each page."""
    objects = ["<< /Type /Catalog /Pages 2 0 R >>", None]
    font_id = 3
    objects.append("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    kids = []
    for lines in pages:
        ops = ["BT /F1 12 Tf 72 720 Td 16 TL"]
        ops += [f"({line}) Tj T*" for line in lines]
        ops.append("ET")
        stream = "\n".join(ops)
        objects.append(f"<< /Length {len(stream)} >>\nstream\n{stream}\nendstream")
        content_id = len(objects)
        objects.append(
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            f"/Resources << /Font << /F1 {font_id} 0 R >> >> /Contents {content_id} 0 R >>"
        )
        kids.append(f"{len(objects)} 0 R")
    objects[1] = f"<< /Type /Pages /Kids [{' '.join(kids)}] /Count {len(kids)} >>"
    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for number, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += f"{number} 0 obj\n{body}\nendobj\n".encode("latin-1")
    xref = len(out)
    out += f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode()
    for offset in offsets:
        out += f"{offset:010d} 00000 n \n".encode()
    out += (
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n"
    ).encode()
    return bytes(out)


@unittest.skipUnless(shutil.which("pdftotext"), "pdftotext not installed")
class Pdf(unittest.TestCase):
    def test_pdf_pages_locators_headers_and_references(self) -> None:
        pages = [
            ["Journal of Tests", "The first page has prose.", "1"],
            ["Journal of Tests", "The second page has prose.", "2"],
            [
                "Journal of Tests",
                "Final words here.",
                "References",
                "Smith. A tapestry.",
                "3",
            ],
        ]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp, "paper.pdf")
            path.write_bytes(_minimal_pdf(pages))
            prose = load(path)
        text = " ".join(line.text for line in prose.lines)
        self.assertEqual(prose.format, "pdf")
        self.assertNotIn("Journal", text)
        self.assertNotIn("tapestry", text)
        self.assertIn("second page", text)
        second = next(line for line in prose.lines if "second page" in line.text)
        self.assertEqual(prose.locator(second.number), f"p2:{second.page_line}")
        self.assertTrue(prose.notes[0].startswith("PDF text extracted with pdftotext"))


if __name__ == "__main__":
    unittest.main()
