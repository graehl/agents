---
slug: document-authoring-toolchain-bakeoff
noticed: 2026-08-12
where: topics/document-writing.md
---

**Gap:** The document-writing guidance has a grounded Markdown-plus default and
an explicit one-way LaTeX promotion rule, but the off-the-shelf renderer survey
and end-to-end bake-off remain incomplete. The inspected current
[Quarto journal listing](https://quarto.org/docs/extensions/listing-journals.html),
[MyST TeX template catalog](https://github.com/myst-templates/templates/blob/main/data/tex.yml),
and [rticles format list](https://pkgs.rstudio.com/rticles/reference/index.html)
did not supply named ACL/NAACL/ICML adapters. Their generic template facilities
must not be reported as current venue support. MyST exposes an unusually clean
TeX bundle; direct Pandoc exposes the least hidden migration; Quarto remains
the strongest current web-first default. Manubot, Org export, knitr `.Rnw`, and
LaTeX-first HTML via lwarp/make4ht have only been bounded, not comparatively
exercised.

**Noticed while:** Expanding paper/blog authoring guidance to cover both rich
static-web output and strict conference LaTeX, after the first recommendation
treated customizability as if it answered named venue-template support.

**Fix sketch:** On the first representative paper, render the same short
manuscript—with citations, equations, two-column tables/floats, appendix,
anonymous/camera-ready front matter, executable result, one extensionless
dual SVG/PDF figure produced by a pre-render script, one Mermaid/Graphviz
diagram, and one interactive web fallback—through Quarto, MyST, and direct
Pandoc. Exercise external-data freshness with and without Quarto freeze. Add R
Markdown/rticles or Manubot only when their ecosystem benefit is real for
that program. Test the current official ACL/NAACL and ICML templates, classify
every adapter using
`topics/document-writing.md`, and measure how much generated TeX must be
changed before it becomes an ordinary compiling working paper. Separately test
lwarp or make4ht after a direct-LaTeX cutover. Close this gap by recording the
reproducible sample, versions, template revisions, output diffs, maintenance
burden, and selected default/cutover criteria in the document-writing topics.

**Partial progress, 2026-08-12:** Quarto 1.9.38 is now installed in the user's
home-scoped command path. A disposable HTML render exercised a caption
footnote, `fig-alt`, image title, cross-references, subfigures, and lightbox;
the expected semantic HTML was present and the basic installation check
passed. This narrows the remaining gap but does not exercise PDF/LaTeX, a real
venue class, external plotting packages, source freshness, or the comparative
MyST/Pandoc paths above.
