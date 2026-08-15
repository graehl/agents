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
The engine extension therefore needs one small preprocessing step —
specified in the brief below — after which html2text (pure python,
uvx-runnable) is a sufficient conversion core.

## Implementer brief

Written 2026-08-15 so this file alone hands off to a fresh implementer.

- Engine: `scripts/related-work` (761-line python3 ACLI, single file);
  tests: `tests/test_related_work.py` — extend them, since the engine's
  guards grew from tested defects and this adds fetch behavior. Contract:
  `topics/research-survey.md` §Contracts (its extraction bullet names
  this gap; remove that parenthetical on close).
- Derived md placement: `extract/<key>/html/<id>.md`, beside the fetched
  `.html`, so html2text's relative asset links stay valid without
  rewriting (verified emitted form:
  `![Refer to caption](2606.06324v2/figure/distribution.png)`). Record
  the derivation (tool + version) in the `.fetched` sentinel or a
  sibling marker so `audit` can reconcile md presence for html-method
  extracts.
- Math preprocessing (the one required transform): for each `<math>`
  element, drop the rendered MathML children and emit the embedded
  `<annotation encoding="application/x-tex">` TeX. Delimiters: the
  backslash forms — `\(...\)` inline, `\[...\]` for
  `<math display="block">` — per the ~/ya convention, chosen for lower
  collision with shell fragments, which agent papers quote heavily.
  Implement via sentinel: emit a placeholder token pre-conversion and
  rewrite it to the final delimiters after html2text. Measured reason:
  html2text doubles exactly backslash-bracket sequences (`\[` → `\\[`)
  while passing backslash-letter TeX bodies (`\Phi`, `x_{1}`) through
  clean, so raw pre-inserted delimiters would arrive mangled. Literal-`$`
  escaping of prose was considered and rejected (mutates prose and shell
  snippets to protect an avoidable delimiter).
- Saved HTML disposition: after successful md derivation, drop the
  `.html` unless the extract carries elements that survive only there
  (interactive/presentation; the parked high-fidelity variant is
  `topics/research-survey.sketches.md`). Dropping is safe because
  extracts are reconstitutable: the `.fetched` sentinel records source
  URL and validators, and a revalidate-style fetch re-obtains.
- Dependency: html2text is pure python; pick the invocation per the
  engine's existing dependency conventions (uvx-pinned or vendored per
  `topics/vendoring.md`) — read the engine before assuming.
- Acceptance: run on the ten extracts of
  `surveys/agent-prompting-orchestration/related-work/`; one md per
  html-method extract with `audit` extended to check it and exiting
  clean; spot-greps pass ("reflectively attribute" in gepa2025, "HTIR"
  in harnessfix2026); math appears once, in backslash delimiters, with
  no doubled Unicode+TeX; `ltx_` residue ≈ 0; md size near
  stripped-text scale (harnessfix2026 ≈ 118 KB is right; gepa2025's
  535 KB doubled-math inflation is the failure signature).
- Close checklist: engine change + tests landed; ten extracts derived;
  the `topics/research-survey.md` gap parenthetical removed;
  concept-digest "local extract" links optionally repointed at the md;
  delete this file.
