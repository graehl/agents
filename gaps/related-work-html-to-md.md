# related-work: no md derivation from HTML extracts

2026-08-15. `scripts/related-work fetch`'s arxiv-html method saves the raw
HTML page (`extract/<key>/html/<id>.html`) and never derives the searchable
`.md` that `topics/research-survey.md` names as the extraction target
(HTML-sourced md preferred over marker pdf→md; a distinct HTML copy kept
only for elements that don't map to markdown). Every HTML-fetched extract
is therefore `rg`-able only as raw HTML.

Close by extending the engine (never a survey-local script): an html→md
derivation step for HTML-method fetches, applied to existing extracts on a
revalidate-style pass; drop the saved HTML where the md carries everything,
keep it where presentation/interactive elements survive only there. First
affected survey: `surveys/agent-prompting-orchestration/` (ten HTML
extracts, 2026-08-15).
