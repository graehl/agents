---
slug: term-hints-implicit-emphasis-overlinks
noticed: 2026-11-10
where: qmd_build/term_hints.lua (discover, prose)
---

**Gap:** with `term-hints-implicit: true`, every bold or italic span becomes
a term and every plain occurrence of it is linked. "This is *not* a toy and
the *a* case holds" produced ten links across two sentences, and a bold
table score such as `**14.19**` becomes a term. Run with `quarto pandoc`.

**Noticed while:** the automatic strict review of
`1e439e95a14a..ee441c86d0b2`.

**Fix sketch:** an implicit emphasis entry links only other formatted
occurrences of the same span, never plain words; exclude numeric spans.
