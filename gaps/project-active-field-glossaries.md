---
slug: project-active-field-glossaries
noticed: 2026-09-21
where: AGENTS.global.md Project glossary; topics/glossary.md; GLOSSARY.md
---

**Gap:** projects cannot yet declare a small active set of field glossaries
with an established scoped-loading mechanism. The agents root glossary spans
many concerns; loading all of it for narrow work spends context on unrelated
terms. The user requested a design pass, not automatic splitting or a new
mandatory boot read.

**Current rules, verified 2026-09-21:** `AGENTS.global.md` § Project glossary
requires identifying the applicable glossary chain, permits targeted row
lookup/search, and requires a full read only when broader vocabulary matters.
`topics/glossary.md` treats `~/agents/GLOSSARY.md` as an additional outer scope
for general agent-workflow terms, not a mandatory full boot load. The root
glossary is 45,109 bytes; the separate human reference `topic-definitions.md`
is 79,672 bytes and is explicitly not loaded per conversation. A stale row in
`AGENTS.weak.md` named GLOSSARY at first tool use; this pass removed that stale
full-boot requirement without broadening the ordinary global rule.

**Noticed while:** the global boot/topic hierarchy pruning and scoping pass.

**Candidate:** let project guidance specify active field glossaries; encountering
a term could trigger retrieval of its row and needed local context rather than
the entire glossary. This is an untested hypothesis. Incidence alone may miss
synonyms, unfamiliar concepts an agent does not know to search for, or a needed
distinction before its term appears. Common-word matches may create irrelevant
loads. Scope precedence, aliases, and term/topic links must remain explicit.

**Next:** inspect existing project and field glossary owners before designing
new files or syntax. Compare explicit active-field selection plus row lookup
against term-incidence triggering on realistic prompts, including unseen terms,
ambiguous common words, and cross-field work. Record retrieval misses and
context cost; do not claim effectiveness from regex coverage alone.

**Closure:** an agreed project activation surface, one canonical owner per
term, tested retrieval behavior, and no unconditional full-global-glossary
load introduced by the mechanism. Related owner: [glossary](../topics/glossary.md).

Contributing-model: 6-Astra
