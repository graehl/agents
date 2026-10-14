# Paper projects

> "Write a paper on X" is a repeatable process: place the paper under its
> owning research program with a proposal card, scaffold it with `paper-new`,
> write in ordered section fragments, build HTML and a US Letter PDF, package
> arXiv source with `qmd-arxiv`, and record each release in a changelog.

Topic: `paper-projects`
Governs: starting a new paper project or setting up its build

Read this when asked to write, start or set up a paper, survey paper or
technical report that will be built and shared as a document. The writing
itself follows [`paper-writing`](paper-writing.md) and
[`technical-writing`](technical-writing.md); choosing and promoting the paper
follows [`paper-drafting`](paper-drafting.md).

## Steps

1. **Place it.** Find the owning program: the most specific
   `research/<program>/PROGRAM.md` whose aspirations the paper serves (read
   its charter chain). A paper that fits no program prompts a question, not a
   new top-level directory. Add a card to the program's `paper-proposals.md`
   per `paper-drafting` (status, governing form, reader promise, central result
   or `TBD`). A program may hold several papers.
2. **Scaffold it.** `~/agents/scripts/paper-new research/<program> <slug>
   --title "..."` creates `research/<program>/papers/<slug>/`: root `index.qmd`
   (front matter and the ordered `{{< include >}}` list), `sections/_NN-*.qmd`
   fragments, `_quarto.yml` (US Letter, pdfLaTeX, kept TeX), bibliography,
   `figures/`, `CHANGELOG.md`, `qmd-html.json`, a README with build commands,
   and a `.gitignore` for `_build/`. It refuses an existing directory or a
   program without `PROGRAM.md`. Fragment and layout conventions:
   [`document-writing`](document-writing.md).
3. **Write.** Abstract first and revised last (`paper-writing`); one section
   per fragment; figures from versioned scripts beside the paper
   ([`document-writing-figures`](document-writing-figures.md)).
4. **Build.** `quarto render` in the paper directory gives
   `_build/index.html` (self-contained; serve `_build/`) and
   `_build/paper.pdf`. `qmd-html --config qmd-html.json` gives a receipted HTML
   with source maps and a browser-print PDF
   ([`document-writing-browser-interactive`](document-writing-browser-interactive.md)).
   `qmd-arxiv <paper-dir>` gives the arXiv bundle
   ([`arxiv-submission`](arxiv-submission.md)). Add a venue profile with
   `qmd-venue-pdf` only for a venue that requires its format
   ([`document-writing-printable`](document-writing-printable.md) § Scripted
   venue build).
5. **Release.** A release is a git commit; add its entry to the paper's
   `CHANGELOG.md` (beside the paper, never rendered). Before any submission or
   final release, pass the citation-retrieval gate in `paper-writing`.
6. **Optional companions.** A software or data release (its own repository or
   a tagged release) is linked from the paper and versioned with it.

## Defaults and their reasons

- **US Letter** for every generated PDF (graehl, 2026-10-14), including the
  browser-print path.
- **arXiv first**: it is the usual target; ACL and other venue formats are
  per-submission profiles.
- **pdfLaTeX**: the only engine arXiv documents.
- **Shared builders**: build logic lives in `~/agents` (`qmd_build`,
  `paper-new`, `qmd-html`, `qmd-venue-pdf`, `qmd-arxiv`). A project keeps only
  paper-specific steps; an older paper with its own builders (for example the
  PII paper in `~/draft`) is left as is rather than migrated mid-review.

## Worked examples

- `~/draft/research/pii/frontier/papers/multilingual-pii-redaction/`: the
  full flow with project-local builders (ACL review build, named preprint and
  arXiv bundle, source-anchored review comments, release links).
- `~/draft/research/speech-recognition/papers/weak7-compact-asr/`: a live
  meeting-draft paper with a changelog, built with plain `quarto render`.
