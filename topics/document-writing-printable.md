# Printable document writing

> Produce a stable PDF and, when required, a clean LaTeX submission package
> whose static figures, tables, citations, and claims preserve the canonical
> document without depending on browser interaction.

Topic: `document-writing-printable`

## Printable equivalent

Every claim exposed through browser interaction has a static printable
equivalent: the central view, a representative/default selection, or a compact
summary table. The paper may link the richer web artifact, but a referee or
archival reader must be able to evaluate the claim from the submitted document
alone. Use the same data and default comparison in both outputs.

For the Quarto default, render the working PDF and retain generated TeX when it
helps diagnose templates or prepare an archive; Quarto documents
[PDF output and `keep-tex`](https://quarto.org/docs/output-formats/pdf-basics/).
Generated TeX remains an output unless the explicit source-promotion rule in
[`document-writing`](document-writing.md) fires.

Follow [`document-writing-figures`](document-writing-figures.md) for the
matched-asset convention: a quantitative generator normally emits same-stem
SVG and PDF, and an extensionless Quarto image reference selects SVG for HTML
and PDF for LaTeX. The same script, data, dimensions, and comparison semantics
own both assets.

## Venue submission path

The current venue call and its exact current style/template are authoritative.
At submission time, verify page limit, anonymity, font and margin rules,
supplement policy, bibliography treatment, artifact links, accepted archive
type, and whether the venue expects source or only PDF. Do not freeze a
year-specific NeurIPS, ACL, OpenReview, or publisher procedure into this
cross-project topic.

The rendering feature already exists in Quarto, MyST, Pandoc, and related
systems: each can wrap or emit LaTeX. What may not exist is a maintained,
current, named ACL/NAACL/ICML-style adapter. Such an adapter is a compatibility
product rather than a copied style file. It must preserve the venue's title and
author modes, bibliography, floats and tables, page geometry, anonymity and
camera-ready switches, mandatory sections or checklists, and package
restrictions while tracking both renderer and yearly template changes. A
generic template hook proves customizability, not compliance.

Prefer a repeatable renderer adaptation in this order:

1. a venue-endorsed path or current cataloged renderer format, with its support
   level recorded;
2. an official LaTeX template wired as an audited local Quarto/Pandoc format;
3. a narrow filter or include for unsupported front matter or macros; then
4. explicit promotion to direct TeX only when the template cannot be produced
   reliably from the canonical source.

Render early enough to expose float, equation, reference, and page-limit
problems while the document structure is still easy to change. Never infer
submission compliance from the HTML rendering.

## Markdown-to-LaTeX refinement

Use one of three explicit authority states:

1. **Markdown-canonical:** Quarto, MyST, R Markdown, Manubot, or direct Pandoc
   owns the prose. TeX is regenerated, inspected, and never hand-edited.
2. **Cutover candidate:** the build emits a self-contained TeX tree and a clean
   compile exposes the remaining venue surgery. Edits still go upstream until
   a recorded cutover.
3. **LaTeX-canonical:** the cutover is committed; normal LaTeX tools and the
   official venue class own the working paper. The old Markdown is a frozen
   source snapshot or is clearly labeled as a derivative web source.

MyST's `format: tex`/`tex+pdf` route is especially amenable to state 2 because
it emits source, images, citations, and class files together. Direct Pandoc
with `--standalone --template` is the most transparent generic route. Quarto
can retain its generated TeX with `keep-tex`; R Markdown/rticles offers a
similar Pandoc-and-template route for R-centered work. These are pipeline
capabilities, not evidence that the desired venue adapter exists.

At cutover:

- pin the renderer, filters, official venue archive, and last Markdown commit;
- copy only the compiling TeX root, bibliography, figures, and required local
  style/class files into the working paper tree;
- replace generated-only paths and opaque build dependencies with documented,
  ordinary LaTeX inputs;
- compile anonymous/review and camera-ready modes as applicable and inspect
  page geometry, tables, floats, citations, and mandatory sections;
- record that TeX now owns wording and structure; and
- choose one web policy: derive HTML from LaTeX, freeze the earlier web
  version, or maintain a clearly scoped companion that does not claim to be a
  second current manuscript.

For a print-first paper, direct LaTeX is a valid early cutover rather than a
failure. [knitr](https://yihui.org/knitr/) with `.Rnw` keeps LaTeX structure
canonical while generating R results; Org's
[LaTeX exporter](https://orgmode.org/manual/LaTeX-Export.html) can target a
registered document class; and direct LaTeX can produce derivative HTML with
[lwarp](https://ctan.org/pkg/lwarp) or
[make4ht](https://ctan.org/pkg/make4ht). These choices favor exact print
control. They are weaker defaults for portable Markdown collaboration and do
not guarantee that a complex venue class converts cleanly to useful HTML.

## arXiv package

Recheck arXiv's current documentation immediately before submission. Its
current [submission overview](https://info.arxiv.org/help/submit/index.html)
prefers TeX/LaTeX when source exists and says not to submit a PDF produced from
TeX in place of that source. The current
[TeX guidance](https://info.arxiv.org/help/submit_tex.html) requires a
root-compilable source package with its figures and needed style/macro files,
and a bibliography supplied in the accepted source/compiled form.

Prepare a minimal archive in a clean directory:

- one obvious root document and no unused drafts, backups, caches, generated
  websites, or private notes;
- all required figures, bibliography material, style files, and local macros;
- relative, case-correct filenames that work on a clean Linux build;
- no JavaScript dependency or external runtime fetch for a claim-bearing
  object; and
- only public-safe source, paths, metadata, examples, and acknowledgments.

Compile the archive itself in an isolated clean directory rather than only the
working tree. Inspect the resulting PDF page by page for missing glyphs,
cropped figures, broken links/references, accidental annotations, anonymity
leaks, and stale supplemental material. Then inspect the platform-generated
PDF before final submission.

## Durable outputs

Record the source revision, renderer and TeX-engine versions, venue template
revision, exact render/archive command, and any accepted warnings. Keep vector
figures where supported and ensure fonts and text remain machine-readable.
Treat a PDF as an archival presentation artifact, not as a replacement for the
source and build record.
