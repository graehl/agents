# arXiv submission

> arXiv compiles submitted TeX with pdfLaTeX and enforces metadata and
> rendering limits that a locally clean PDF does not reveal; build the source
> bundle with `qmd-arxiv`, compile it in an empty directory, and check the
> limits below before uploading.

Topic: `arxiv-submission`
Governs: preparing or uploading an arXiv submission

arXiv is the common release target for this user's papers; a conference venue
format (for example ACL) is an extra profile only when submitting there. Every
generated PDF uses US Letter (graehl, 2026-10-14). The general clean-archive
checklist is in [`document-writing-printable`](document-writing-printable.md)
§ arXiv package; this topic holds arXiv's own limits and the tool.

## Build

`~/agents/scripts/qmd-arxiv <paper-dir>` (papers scaffolded by `paper-new`;
see [`paper-projects`](paper-projects.md)) renders the PDF with kept TeX,
flattens the TeX and every `\includegraphics` file into `_build/arxiv/src/`,
rejects host paths and hidden files, compiles the bundle twice with pdflatex in
an empty directory, and writes `arxiv-source.zip`, `check.pdf` and a hash
receipt with page count, US Letter check, abstract length and warnings. Upload
the zip; inspect `check.pdf` page by page first.

## Limits and pitfalls

Documented by arXiv (checked 2026-10-14; recheck before each submission):

- **Engine:** arXiv documents pdfLaTeX (plus plain TeX and DVI LaTeX) and
  does not mention XeLaTeX or LuaLaTeX
  ([TeX guidance](https://info.arxiv.org/help/submit_tex.html)). Papers
  scaffolded here set `pdf-engine: pdflatex`. Non-Latin text (Arabic, Lao,
  CJK, Vietnamese diacritics) therefore needs pdfLaTeX-compatible packages or
  figures; test such text in the clean compile, not just locally.
- **TeX Live:** 2025 by default (2023 selectable); with biblatex, only `.bbl`
  format 3.3. A supplied `.bbl` must share the main `.tex` file's name and come
  from the same program. Quarto's citeproc writes references into the TeX, so
  scaffolded papers need no `.bbl`.
- **Layout:** compilation runs from the bundle root; do not ship `.aux`/`.pdf`
  files for the source `.tex`; hidden files and directories are deleted at
  announcement.
- **Abstract:** at most 1,920 characters
  ([preparation guide](https://info.arxiv.org/help/prep.html)); `qmd-arxiv`
  warns. Titles should avoid all-caps, Unicode and opaque macros.

Observed by graehl (not documented on the pages above):

- **Comments field:** has a maximum length of roughly 300 characters. Keep it
  to page and figure counts plus venue status.
- **HTML rendering of figures:** arXiv's HTML view constrains image size and
  aspect, which stretched or padded figures. Give figures explicit widths and
  natural aspect ratios, avoid extreme aspect ratios, and check the HTML view
  after upload as well as the PDF.

Add new observations here with their date and source.
