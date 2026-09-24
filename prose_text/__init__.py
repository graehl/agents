"""prose_text — the prose a reader reads, extracted from Markdown, Quarto, text, or PDF.

Tools that measure writing (style lints, readability checks, word counts)
should see sentences, not the code, paths, citations, and markup around
them. `load(path)` returns a `Prose` whose `lines` keep the source line
numbering and column offsets: every skipped span is replaced by spaces of
the same length, so a match in `line.text` points at the same place in the
source file.

Skipped: YAML front matter; fenced code (including Quarto chunks) and
inline code; display and inline math; HTML comments; URLs and link targets;
Quarto div fences, attribute blocks, and shortcodes; file paths, file
names, snake_case identifiers, and `--flags`; citations (pandoc `@key` and
`[@key]`, numeric `[1-3]`, author-year `(Smith et al., 2020)`, LaTeX
`\\cite{}`); and References/Bibliography sections. Figure lines keep their
caption as prose but get their own line kind.

PDF input is read with poppler's `pdftotext`, a deliberate lightweight
choice for statistics over prose, where layout loss matters less than for
reading a paper (`topics/pdf.md` routes reading to marker-pdf). Repeated
running headers and footers and bare page numbers are dropped. `Prose.notes`
carries the disclaimer a report should show, and `Prose.locator` renders
`p<page>:<line>` for PDF lines.
"""

from __future__ import annotations

import re
import shutil
import subprocess
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

__all__ = [
    "WORD",
    "Block",
    "ExtractionError",
    "Line",
    "Prose",
    "blocks",
    "from_markdown",
    "from_pdf",
    "load",
    "sentences",
]

WORD = re.compile(r"[A-Za-z][A-Za-z'’-]*")


class ExtractionError(Exception):
    """The input could not be turned into prose (missing tool, unreadable file)."""


@dataclass
class Line:
    number: int  # 1-based line in the source (or in the extracted PDF text)
    kind: str  # heading | bullet | table | quote | figure | text | blank
    text: str  # skipped spans blanked to spaces; same length as the source line
    page: int | None = None  # PDF only
    page_line: int | None = None  # PDF only: line within its page


@dataclass
class Prose:
    lines: list[Line]
    format: str  # "markdown" or "pdf"
    notes: list[str] = field(default_factory=list)
    _pages: dict[int, tuple[int, int]] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._pages = {
            line.number: (line.page, line.page_line)
            for line in self.lines
            if line.page is not None and line.page_line is not None
        }

    def words(self) -> int:
        return sum(
            len(WORD.findall(line.text))
            for line in self.lines
            if line.kind not in {"blank", "table"}
        )

    def locator(self, number: int) -> str:
        """`p<page>:<line>` for PDF-extracted lines, else the source line number."""
        if number not in self._pages:
            return str(number)
        page, page_line = self._pages[number]
        return f"p{page}:{page_line}"


# --- Span patterns (each match is blanked) ---------------------------------------

FENCE = re.compile(r"^\s{0,3}(```+|~~~+)")
DISPLAY_MATH_FENCE = re.compile(r"^\s*\$\$\s*$")
HEADING = re.compile(r"^\s{0,3}(#{1,6})\s+(.*?)\s*#*\s*$")
BULLET = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
TABLE = re.compile(r"^\s*\|")
QUOTE = re.compile(r"^\s{0,3}>\s?")
FIGURE = re.compile(r"^\s*!\[")
DIV_FENCE = re.compile(r"^\s*:::+")
HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)

INLINE_CODE = re.compile(r"(`+)(?:(?!\1).)+?\1")
URL = re.compile(r"(?:https?://|www\.)\S+")
EMAIL = re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b")
LINK_TARGET = re.compile(r"\]\([^)]*\)")
MATH = re.compile(
    r"\$\$.+?\$\$"
    r"|(?<![\\$\w])\$(?=\S)(?:\\\$|[^$\n])+?(?<=\S)\$(?!\d)"
    r"|\\\(.+?\\\)|\\\[.+?\\\]"
)
QUARTO_ATTRS = re.compile(r"\{[#.=][^{}\n]*\}")
SHORTCODE = re.compile(r"\{\{[<%].*?[>%]\}\}")
FOOTNOTE_REF = re.compile(r"\[\^[^\]\s]+\](?!:)")
CITE_BRACKET = re.compile(r"\[[^\[\]\n]*-?@[A-Za-z_][^\[\]\n]*\]")
CITE_BARE = re.compile(r"(?<![\w.@/])-?@[A-Za-z_][\w:.#$%&+?<>~/-]*(?<![.:])")
CITE_NUMERIC = re.compile(r"\[\d+(?:\s*[-–,]\s*\d+)*\]")
CITE_LATEX = re.compile(
    r"\\(?:cite[tp]?|citep|citet|citeauthor|citeyear|autocite|parencite|textcite)"
    r"\*?(?:\[[^\]]*\])*\{[^}]*\}"
)
_AUTHOR = r"[A-Z][\w'’-]+(?:\s+(?:et\s+al\.?|and|&)(?:\s+[A-Z][\w'’-]+)?)?"
CITE_AUTHOR_YEAR = re.compile(
    r"\((?:(?:see|e\.g\.,?|cf\.|i\.e\.,?)\s+)?"
    + _AUTHOR
    + r",?\s+(?:19|20)\d{2}[a-z]?"
    + r"(?:\s*[;,]\s*(?:"
    + _AUTHOR
    + r",?\s+)?(?:19|20)\d{2}[a-z]?)*"
    + r"(?:,\s*(?:p|pp)\.\s*[\d–-]+)?\)"
)
CITE_YEAR_ONLY = re.compile(r"(?<=\s)\((?:19|20)\d{2}[a-z]?\)")
ET_AL = re.compile(r"\bet\s+al\.")
_EXT = (
    r"(?:md|qmd|rmd|py|pyi|ipynb|ts|tsx|js|mjs|json|jsonl|ya?ml|toml|ini|cfg|txt|csv|tsv|"
    r"pdf|html?|tex|bib|sh|bash|zsh|c|cc|cpp|cxx|h|hpp|rs|go|java|kt|rb|lua|sql|lock|log|"
    r"parquet|png|jpe?g|svg|gif)"
)
PATH_CANDIDATE = re.compile(r"(?<![\w/@.])(?:~/|\.{1,2}/|/)?(?:[\w.-]+/)+[\w.-]*")
FILE_NAME = re.compile(r"(?<![\w/])[\w-]+(?:\.[\w-]+)*\." + _EXT + r"\b")
FILE_EXT_END = re.compile(r"\." + _EXT + r"$")
SNAKE_IDENT = re.compile(r"\b[A-Za-z]\w*_\w+\b")
CLI_FLAG = re.compile(r"(?<![\w-])--[a-z][\w-]*")

REFERENCES_TITLE = re.compile(
    r"^(?:\d+(?:\.\d+)*\.?\s+)?(?:references|bibliography|works cited|literature cited|"
    r"reference list|citations)\s*$",
    re.IGNORECASE,
)
REFS_DIV = re.compile(r"^\s*:::+\s*\{#refs\b")


def _spaces(match: re.Match[str]) -> str:
    return " " * len(match.group(0))


def _blank_paths(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        token = match.group(0)
        # One slash between plain words is prose ("and/or", "client/server").
        if (
            token.startswith(("~/", "./", "../", "/"))
            or token.count("/") >= 2
            or FILE_EXT_END.search(token)
            or re.search(r"[\d_.-]", token)
        ):
            return " " * len(token)
        return token

    return PATH_CANDIDATE.sub(replace, text)


def clean_inline(text: str, *, markdown: bool = True) -> str:
    """Blank every non-prose span on one line, preserving its length."""
    if markdown:
        text = INLINE_CODE.sub(_spaces, text)
        text = LINK_TARGET.sub(lambda m: "]" + " " * (len(m.group(0)) - 1), text)
        text = SHORTCODE.sub(_spaces, text)
        text = QUARTO_ATTRS.sub(_spaces, text)
        text = FOOTNOTE_REF.sub(_spaces, text)
    text = URL.sub(_spaces, text)
    text = EMAIL.sub(_spaces, text)
    text = MATH.sub(_spaces, text)
    for pattern in (CITE_LATEX, CITE_BRACKET, CITE_NUMERIC, CITE_AUTHOR_YEAR):
        text = pattern.sub(_spaces, text)
    text = CITE_BARE.sub(_spaces, text)
    text = CITE_YEAR_ONLY.sub(_spaces, text)
    text = ET_AL.sub(_spaces, text)
    text = _blank_paths(text)
    text = FILE_NAME.sub(_spaces, text)
    text = SNAKE_IDENT.sub(_spaces, text)
    return CLI_FLAG.sub(_spaces, text)


def _classify(text: str) -> str:
    if not text.strip():
        return "blank"
    if HEADING.match(text):
        return "heading"
    if TABLE.match(text):
        return "table"
    if FIGURE.match(text):
        return "figure"
    if BULLET.match(text):
        return "bullet"
    if QUOTE.match(text):
        return "quote"
    return "text"


# --- Markdown / Quarto / text ----------------------------------------------------


def from_markdown(source: str) -> Prose:
    """Markdown, Quarto, or plain text (plain text passes through unchanged)."""
    source = HTML_COMMENT.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), source)
    raw = source.split("\n")
    start = 0
    if raw and raw[0].strip() == "---":
        for i in range(1, len(raw)):
            if raw[i].strip() in {"---", "..."}:
                start = i + 1
                break
    lines: list[Line] = []
    fence: str | None = None
    in_math = False
    refs_level: int | None = None  # inside a References heading's section
    refs_div = False
    skipped_refs = 0
    for index, text in enumerate(raw[start:], start=start):
        number = index + 1
        opened = FENCE.match(text)
        if fence is not None:
            if (
                opened
                and opened.group(1)[0] == fence[0]
                and len(opened.group(1)) >= len(fence)
            ):
                fence = None
            continue
        if opened:
            fence = opened.group(1)
            continue
        if DISPLAY_MATH_FENCE.match(text):
            in_math = not in_math
            continue
        if in_math:
            continue
        heading = HEADING.match(text)
        if refs_level is not None:
            if heading and len(heading.group(1)) <= refs_level:
                refs_level = None
            else:
                skipped_refs += bool(text.strip())
                continue
        if refs_div:
            if DIV_FENCE.match(text):
                refs_div = False
            skipped_refs += bool(text.strip())
            continue
        if REFS_DIV.match(text):
            refs_div = True
            continue
        if heading and REFERENCES_TITLE.match(re.sub(r"[*_`]", "", heading.group(2))):
            refs_level = len(heading.group(1))
            continue
        if DIV_FENCE.match(text):
            lines.append(Line(number, "blank", " " * len(text)))
            continue
        cleaned = clean_inline(text)
        lines.append(Line(number, _classify(cleaned), cleaned))
    notes = []
    if skipped_refs:
        notes.append(f"Skipped a References section ({skipped_refs} lines).")
    return Prose(lines, "markdown", notes)


# --- PDF -------------------------------------------------------------------------

PAGE_NUMBER = re.compile(
    r"^\s*(?:page\s+)?\d{1,4}(?:\s*(?:/|of)\s*\d{1,4})?\s*$", re.IGNORECASE
)
PDF_DISCLAIMER = (
    "PDF text extracted with pdftotext: hyphenated line breaks, multi-column "
    "reading order, and leftover headers or captions can add or hide flags. "
    "Locators are p<page>:<line> in the extracted text."
)


def _edge_key(text: str) -> str:
    return re.sub(r"\d+", "#", text.strip().lower())


def from_pdf(path: str | Path) -> Prose:
    exe = shutil.which("pdftotext")
    if exe is None:
        raise ExtractionError(
            "pdftotext not found; install poppler-utils, or extract the text and pass it on stdin"
        )
    proc = subprocess.run(
        [exe, "-enc", "UTF-8", str(path), "-"],
        capture_output=True,
        text=True,
        check=False,  # a failure is reported below with pdftotext's stderr
    )
    if proc.returncode != 0:
        raise ExtractionError(f"pdftotext failed on {path}: {proc.stderr.strip()}")
    pages = proc.stdout.split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    # Running headers and footers: the same text (digits normalized) among the
    # first or last three nonblank lines of at least three pages.
    edges: Counter[str] = Counter()
    for page in pages:
        nonblank = [ln for ln in page.split("\n") if ln.strip()]
        edges.update({_edge_key(ln) for ln in nonblank[:3] + nonblank[-3:]})
    running = {key for key, n in edges.items() if n >= 3 and n >= 0.3 * len(pages)}
    lines: list[Line] = []
    number = 0
    in_refs = False
    skipped_refs = 0
    dropped_edges = 0
    for page_no, page in enumerate(pages, start=1):
        for page_line, text in enumerate(page.split("\n"), start=1):
            number += 1
            if in_refs:
                skipped_refs += bool(text.strip())
                continue
            if REFERENCES_TITLE.match(text.strip()):
                in_refs = True
                continue
            if text.strip() and (_edge_key(text) in running or PAGE_NUMBER.match(text)):
                dropped_edges += 1
                continue
            cleaned = clean_inline(text, markdown=False)
            kind = (
                "blank"
                if not cleaned.strip()
                else ("bullet" if BULLET.match(cleaned) else "text")
            )
            lines.append(Line(number, kind, cleaned, page_no, page_line))
    notes = [PDF_DISCLAIMER]
    if dropped_edges:
        notes.append(
            f"Dropped {dropped_edges} running-header, footer, or page-number lines."
        )
    if skipped_refs:
        notes.append(
            f"Skipped everything after the References heading ({skipped_refs} lines),"
            " including any appendix."
        )
    return Prose(lines, "pdf", notes)


def load(path: str | Path) -> Prose:
    """Dispatch on suffix: .pdf through pdftotext, everything else as Markdown/text."""
    path = Path(path)
    if path.suffix.lower() == ".pdf":
        if not path.is_file():
            raise FileNotFoundError(path)
        return from_pdf(path)
    return from_markdown(path.read_text(encoding="utf-8"))


# --- Structure -------------------------------------------------------------------


@dataclass
class Block:
    kind: str  # paragraph | bullet | heading | table | quote | figure
    lines: list[Line]

    @property
    def text(self) -> str:
        return " ".join(line.text.strip() for line in self.lines)


def blocks(lines: list[Line]) -> list[Block]:
    """Group lines into paragraphs, list items, and single-line units."""
    out: list[Block] = []
    current: Block | None = None
    for line in lines:
        if line.kind == "blank":
            current = None
        elif line.kind in {"heading", "table", "figure"}:
            out.append(Block(line.kind, [line]))
            current = None
        elif line.kind == "bullet":
            current = Block("bullet", [line])
            out.append(current)
        else:
            kind = "quote" if line.kind == "quote" else "paragraph"
            if current is not None and current.kind in {kind, "bullet"}:
                current.lines.append(line)
            else:
                current = Block(kind, [line])
                out.append(current)
    return out


SENTENCE_END = re.compile(
    r"(?<!\b[A-Z])(?<!\be\.g)(?<!\bi\.e)(?<!\betc)(?<!\bvs)[.!?]+[\"')\]’”]*"
    r"(?=\s+[\"'(\[“‘]?[A-Z0-9]|\s*$)"
)


def sentences(text: str) -> list[str]:
    parts: list[str] = []
    last = 0
    for match in SENTENCE_END.finditer(text):
        piece = text[last : match.end()].strip()
        if piece:
            parts.append(piece)
        last = match.end()
    tail = text[last:].strip()
    if tail:
        parts.append(tail)
    return parts
