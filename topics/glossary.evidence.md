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

## 2026-09-24 — split into human `GLOSSARY.md` and `GLOSSARY.agents.md`

Contributing-model: fable-5.1.

User-directed, same session. graehl identified two partly conflicting
roles in one file: a key-phrase surface that activates instruction reading
for agents, and an explanation surface for a person hovering a common
term. He approved a split and accepted the maintenance cost of introducing
a term in both files when both readers need it, for token efficiency and
freedom to shape the human tooltip experience with material inert for
agents.

Design points he set, each recorded because it overrides my first draft:

- The agent file is read *instead of* `GLOSSARY.md` (I had proposed
  layering). It is compressed: standard definitions omitted, a few
  sense-emphasized personal terms, and triggers to read topic guidance.
- A trigger is a scope or activity ("writing a document"), not a word
  occurrence. Encoded as `Governs: <activity>` metadata in each topic doc,
  regenerated into the agent file; a doc without one has no row.
- The human `GLOSSARY.md` is "what topics have scoped agent guidance" plus
  definitions he actually needs help recalling. He does not want human rows
  labeled `writing` or `glossary`; `Glossary: <label>` in the topic doc
  relabels the human row (`document writing`, `term glossary`), replacing
  the earlier `omit`-only marker. `document writing` sits next to the
  unrelated `document-writing` topic; he accepted that label knowingly.
- Because the agent file is short, it is read in full at project entry and
  on scope entry, replacing targeted lookup for that file. This is the
  payoff: it joins the routing layer.

Pass over this repo: 76 topic docs received a `Governs:` line; `cpp`,
`python`, and `typescript` also gained ledes and human rows they had
lacked; `software-aesthetic.coordinated` is covered by `software-aesthetic`;
`writing-practice`, `agents-bench`, `goal-distillation`, `ml-scaling`,
`user-authorization-attestation`, and the survey rows have no governs row
by design (not routed, proposals, or status notes). 29 sense rows were compressed
from the human file. Generator was a scratch script; the procedure in
§ Agent glossary is the durable spec. Other projects keep current behavior
until they get the same pass.
