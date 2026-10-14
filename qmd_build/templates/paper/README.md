# {{title}}

Owning program: [{{program}}]({{program}}). Proposal card: [{{proposal}}]({{proposal}}).
Scaffolded by `~/agents/scripts/paper-new` on {{date}}; the process is
`~/agents/topics/paper-projects.md`.

## Layout

- `index.qmd`: root; front matter and the ordered `{{< include >}}` list.
- `sections/_NN-name.qmd`: one fragment per section.
- `related-work/papers.bib`: bibliography; `figures/`: generated figures and
  their scripts.
- `CHANGELOG.md`: one entry per release, never rendered.

## Build

```bash
quarto render                                  # _build/index.html and _build/paper.pdf (US Letter)
~/agents/scripts/qmd-html --config qmd-html.json   # receipted static HTML + browser-print PDF
~/agents/scripts/qmd-arxiv .                    # _build/arxiv/: source bundle, clean pdfLaTeX check
```

A venue profile (for example ACL) is added only when submitting there; see
`~/agents/topics/document-writing-printable.md` § Scripted venue build.
