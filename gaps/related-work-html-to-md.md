# related-work: no md derivation from HTML extracts

2026-08-15. `scripts/related-work fetch`'s arxiv-html method saves the raw
HTML page (`extract/<key>/html/<id>.html`) and never derives the searchable
`.md` that `topics/research-survey.md` names as the extraction target
(HTML-sourced md preferred over marker pdf→md; a distinct HTML copy kept
only for elements that don't map to markdown). Every HTML-fetched extract
is therefore `rg`-able only as raw HTML.

The fidelity-preserving variant (render over-spanned regions as SVG with
full-text alt) is sketched in `topics/research-survey.sketches.md`; the
close below is the plain derivation, which arXiv's embedded per-equation
TeX annotations make nearly lossless on their own.

Close by extending the engine (never a survey-local script): an html→md
derivation step for HTML-method fetches, applied to existing extracts on a
revalidate-style pass; drop the saved HTML where the md carries everything,
keep it where presentation/interactive elements survive only there. First
affected survey: `surveys/agent-prompting-orchestration/` (ten HTML
extracts, 2026-08-15).

Proved out 2026-08-15 (`uvx html2text --body-width=0` on the gepa2025 and
harnessfix2026 extracts): structure and prose convert cleanly — numbered
section headers survive as `##`, claims stay greppable ("reflectively
attribute", "HTIR"), harnessfix 408 KB html → 118 KB md with only 5 lines
of `ltx_` residue. One systematic defect: LaTeXML math emits doubled —
rendered Unicode glyphs immediately followed by the embedded TeX
annotation (`Φ=(M,C,𝒳,𝒴)\Phi=(M,C,\mathcal{X},\mathcal{Y})`) — searchable
in both forms but ugly and size-inflating (math-heavy gepa: 535 KB md).
The engine extension therefore needs one small preprocessing step: strip
the MathML rendered children and keep the `application/x-tex` annotation
as `$...$`. With that, html2text (pure python, uvx-runnable) is a
sufficient conversion core.
