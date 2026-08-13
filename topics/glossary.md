# Glossary system

> Project-specific terminology lives in a hierarchy of `GLOSSARY.md` files:
> every named term is topic-like, references may name any canonical doc, and
> each glossary owns a local formal-topic collection regenerated from ledes.

Topic: `glossary`

## Contracts

- Each `GLOSSARY.md` contains one sorted markdown table with columns
  `| term | definition | topic / refs |` (plus any supported legacy or local
  scope declaration already in use).
- Every named row is topic-like. Its `topic / refs` cell may point to an
  arbitrary canonical doc; absence from `topics/` does not make the term less
  of a topic.
- A glossary owns a formal-topic collection: root `topics/` (or an established
  root `docs/topics/` alternate) for the project glossary, and sibling
  `topics/` for a scoped glossary. Owned topic rows correspond 1:1 to
  non-companion docs there, and their definitions come from the docs' `> `
  blockquote ledes.
- Other rows are curated. They survive regeneration verbatim, including
  arbitrary references and any `<!-- unconfirmed: YYYY-mm-dd -->` markers.
- A scope may carry an optional sibling `PROGRAM.md` containing its descriptive
  charter and optional binding `Program instructions` section. It is authored,
  never glossary-regenerated.
- Bar for a vernacular row: meaning in this repo is distinct from
  default agent usage. Generic terms an agent already understands
  do not belong.
- This topic doc holds the contribution and regeneration procedures.
  `GLOSSARY.md` itself stays free of build instructions for readers
  who only look up terms.

Read this topic before adding, regenerating, sorting, or promoting
glossary rows, creating scoped sub-glossaries, resolving ambiguous terms,
or deciding whether a vernacular row should become a topic doc.

## Scoped glossaries and topic location

Beyond the root `GLOSSARY.md`, a project may carry per-subtree
`GLOSSARY.md` files marking subsystem- or program-local vocabularies. The
active chain for a path runs from its nearest enclosing glossary outward
through the project glossary. `~/agents/GLOSSARY.md` is an additional outer
scope for general agent-workflow vocabulary, not the default home for project
terms.

- **Resolution**: resolve a named term at the nearest active glossary that
  defines it, then follow its existing canonical reference. Search outward
  only when that scope has no row. An existing doc wins over creating or moving
  one for layout consistency.
- **Placement**: choose the broadest active glossary scope where the term and
  its topic remain natural without pervasive subtree/program qualification.
  Default creation to the current project. Retain a local owner when a parent
  doc would mostly say `program-subdir/...`; promote as actual use widens across
  child scopes. Promote to `~/agents` only when the concern is clearly reusable
  general agent workflow or the user explicitly asks.
- **Creation**: if no canonical doc exists and a formal topic doc is warranted,
  create `<glossary-directory>/topics/<name>.md`. The project glossary uses its
  established root topic collection instead. Do not create a collection until
  it has a first doc.
- **Consultation**: before naming or paraphrasing in a subtree, consult the
  nearest-enclosing glossary and any parent needed to resolve the term. On
  first interpreting or changing a file at a new work site, locate that active
  chain even if no term is yet known to be unfamiliar. Targeted lookup is
  enough for awareness; a full glossary read is deferred until the work needs
  its broader vocabulary. On a glossary read, ensure its sibling `PROGRAM.md`,
  when present, has been read this session, so local vocabulary is interpreted
  under the scope's charter. The rule states the obligation; the agent picks
  the discovery mechanism.

Scope is declared by file placement, not by a path-pattern rule. A project
marks its cutpoints by where it places `GLOSSARY.md` files, not by directory
depth or naming conventions; layouts vary too much across projects to pin to a
generic pattern. Every such cutpoint may own a genuine formal-topic collection.

A sibling `PROGRAM.md` declares that the glossary directory also has a coherent
program-level aspiration. Its absence does not invalidate the glossary or topic
collection. Old research-program headers may remain in a glossary, but they do
not declare a program; discovery uses `PROGRAM.md` only. See
`~/agents/TOPICS.md § Program scope charters` for inference, update verbs, and
parent/child behavior. The directory path is the canonical program locator; an
optional first-line H1 supplies an alternative formal name.

## Topic-doc format the spec relies on

H1 stating the topic, blank line, `> ` blockquote lede (one or more
`> ` lines, nothing else between H1 and lede), blank line, optional
`Topic: <topic-name>` line, then body. See `topics/topic-doc-format.md`
for the auto-fix license that lets the agent normalize existing
docs into this format.

## Adding a term

Add a curated row when a term is truly project-specific — its meaning here is
distinct from default agent usage. Generic terms an agent would already
understand do not belong. Sort alphabetically by term. Leave `topic / refs`
empty when the definition is sufficient; otherwise link the already-canonical
doc or other useful references, regardless of their directory.

For a row added during conversation as a tentative resolution of
ambiguity, flag with `<!-- unconfirmed: YYYY-mm-dd -->`. The user
confirms by removing the marker or prunes the row; either way the
marker survives regeneration until acted on.

Most glossary rows never need a formal topic doc; they are still topic-like and
resolvable through the glossary. Create a formal doc only when the concern
meets the cross-cutting bar and needs a dedicated decision surface under
`~/agents/TOPICS.md`.

## Regeneration

Regeneration targets one glossary and only the topic collection it owns. Scan
its main `topics/*.md` docs, excluding recognized companion files
(`*.evidence.md`, `*.bearings.md`, `*.testing.md`, and `*.sketches.md`). For
the project glossary, use the established `docs/topics/*.md` alternate when
root `topics/` is absent.

For each owned topic doc, read the `> ` blockquote lede immediately after the
H1 — multi-line `> ` lines are space-joined into one sentence — and use it as
the definition of the basename row. Refresh the owned-doc link while
preserving additional references in that cell. The usual relative link form is
`[<name>](topics/<name>.md)`; the root alternate uses
`[<name>](docs/topics/<name>.md)`. A collision with a curated row naming a
different canonical doc is a scope error to resolve, not a row to overwrite.
When a topic doc lacks a `> ` lede, synthesize one from its first body paragraph
and apply the fix as part of regeneration (per the topic-doc auto-fix license
in `topics/topic-doc-format.md`).

Rows without an owned-topic link are preserved verbatim on regeneration,
including arbitrary refs and `<!-- unconfirmed -->` markers. Do not pull rows
from `~/agents/topic-definitions.md` — that file is a multi-field reference,
deliberately not loaded per conversation.

## Design decisions

- **Root glossary at repo root** (vs. `topics/README.md`): prioritizes
  top-level discovery and avoids duplicating what the glossary already does;
  scoped glossaries regain co-location with their topic-doc inputs.
- **Scoped sub-glossaries declared by placement** (vs. a path-
  pattern rule like `*/GLOSSARY.md`): prioritizes per-project
  freedom — subsystem cutpoints vary too much across projects to
  pin to a depth or naming convention; accepts that the agent must
  discover sub-glossary locations rather than infer them from
  convention.
- **Declarative scope phrasing** (vs. a procedural "scan for missing
  sub-glossaries" recipe): prioritizes the resolution, placement, creation,
  and consultation invariants that produce create-as-you-go behavior
  organically; accepts that the agent picks the discovery mechanism rather
  than following a prescribed walk.
- **Every glossary owns topics** (vs. root-only generation and pure-vernacular
  sub-glossaries): keeps program context visible and permits repeated basenames
  without forcing qualified program details into the project-wide collection;
  accepts a hierarchy of collections rather than one flat listing.
- **`GLOSSARY.md` holds only the table** (vs. embedding the regen
  spec inline): prioritizes signal for everyday readers who only
  look up terms; accepts that contributors must navigate to
  `topics/glossary.md` for build/contribution rules.
- **One sorted table** (vs. sectioned by kind): prioritizes
  mechanical name-based lookup; accepts losing at-a-glance grouping
  by category.
- **No `type` column** (vs. tagging rows by kind): prioritizes visual
  cleanliness. Every row is topic-like; the `topic / refs` cell communicates
  its canonical document surface when one exists, without classifying the
  term itself.
- **`> ` blockquote lede** (vs. YAML frontmatter or first-paragraph
  extraction): prioritizes greppability, reformat-survival, and
  parser-freedom; accepts losing the structured fields frontmatter
  would carry.
- **Vernacular rows curated, not auto-generated** (vs. mining
  commits or code for repeated phrases): prioritizes signal on the
  truly-project-specific bar (a human judgment); accepts losing
  comprehensive coverage of every recurring phrase.
- **Don't pull from `~/agents/topic-definitions.md`** (vs. inlining
  its rows per project): prioritizes per-conversation context
  economy (the global file is a multi-field generic reference);
  accepts that general-domain terms must be looked up there rather
  than seen inline.
- **Topic-doc auto-fix license** (vs. gated edit): prioritizes
  ergonomics on mechanical body-preserving normalization (missing
  lede, stray trailer); accepts losing per-edit human review.

Candidate extensions are kept in [glossary sketches](glossary.sketches.md).

## Ambiguity-resolution behavior

When a user phrase is ambiguous against the glossary, see
`AGENTS.global.md § Project glossary` for the checkpoint protocol: state
the inferred meaning plus 1–2 alternatives, continue at normal pace
when the fork is minor or cheaply reversible, hold for the reply
when proceeding wrong would waste significant work. On resolution,
propose adding a row flagged `<!-- unconfirmed: YYYY-mm-dd -->`.
