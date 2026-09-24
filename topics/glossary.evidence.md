# Glossary system evidence

## 2026-09-24 — `Glossary: omit` opt-out for common-word topic basenames

Contributing-model: fable-5.1.

User-directed. graehl asked to re-title the `writing` glossary row so YA
glossary hints stop annotating the common word "writing" in ordinary prose,
and allowed omitting the row outright if dispatch to `topics/writing.md`
exists independently of the glossary. Session:
`63b5dd3a-a496-4957-9334-3002cda9a13f`.

Why omission rather than re-title: the requested label "document writing"
collides with the existing `document-writing` topic (source-of-truth and
renderer choice for research documents), and the 1:1 owned-row contract
would have regeneration re-add a `writing` row anyway. Dispatch exists:
`technical-writing`, `story-writing`, and `story-project-layout` link the
doc, and it carries its own read-trigger sentence. So the row was removed
and the contract gained an explicit opt-out marker in the topic doc, which
regeneration honors.

YA matching fact checked in `~/ya/topics/glossary-tooltips.md`: inline
code in the term cell contributes its visible text, and an all-lowercase
alternative matches case-insensitively, so `writing` annotated every
occurrence of the word.

graehl also asked whether topics get glossary rows routinely because of an
instruction here. Yes: § Contracts "owned topic rows correspond 1:1 to
non-companion docs" plus § Regeneration, with `topic-doc-format` calling
the lede "the canonical one-sentence definition consumed by GLOSSARY.md".
He did not intend that unless the glossary is the main read-trigger
mechanism; it is not. Read triggers are `AGENTS.global.md` routes, topic
cross-links, and skills. Left as 1:1-with-opt-out rather than opt-in,
pending his call.
