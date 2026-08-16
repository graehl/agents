---
slug: related-work-cross-survey-reuse
noticed: 2026-08-16
where: scripts/related-work (verb_fetch, audit_findings), topics/research-survey.md
---

**Gap:** A survey has no way to say "this paper's full text is already committed
in a sibling survey; read it there, do not fetch it again." `related-work fetch
--all` treats every manifest entry without a local extract as pending, so it
re-downloads and re-extracts papers the author deliberately marked
`grounded: false` with a `source:` pointing at another survey's
`extract/<key>/`. Building `surveys/tokenizer-free-span-tagging` this way
duplicated `gillick2016-multilingual-bytes` and started on `clark2022-canine`
before the run was stopped and the duplicate directories removed by hand; the
remaining fetch had to be driven with an explicit 15-key list instead of
`--all`.

The audit side is honest but lossy: those entries must stay `grounded: false`
(no local sentinel), which understates the survey's real grounding — the
tokenizer-free survey reports 19 grounded of 27 manifested when all 27 were in
fact read from committed full text in this repository.

**Noticed while:** Creating `surveys/tokenizer-free-span-tagging` as a sibling of
`surveys/shallow-surface-encoders`, which already holds CANINE, ByT5,
Charformer, Gillick, Cao, Sun, Flair and CharacterBERT extracts.

**Fix sketch:** Add a manifest field naming the owning survey for a shared
paper (`extract_from: surveys/<slug>`, defaulting to the current survey).
`fetch` skips such an entry as satisfied-elsewhere rather than pending; `audit`
resolves the sentinel and tracked-markdown checks against the named survey's
extract and fails if that path is missing, so the pointer cannot rot silently;
`status` reports the borrowed count separately from locally grounded. The
`topics/research-survey.md` contract gains one line stating that extraction
caches are never duplicated across surveys.
