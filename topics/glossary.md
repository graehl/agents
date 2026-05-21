# Glossary system

> Project-specific terminology lives in `GLOSSARY.md` at repo root:
> one sorted table whose topic-linked rows are autopopulated from
> `topics/<name>.md` ledes and whose vernacular rows are curated.

Topic: `glossary`

## Contracts

- `GLOSSARY.md` at repo root, one sorted markdown table, columns
  `| term | definition | topic / refs |`.
- Topic-linked rows correspond 1:1 to non-companion `topics/<name>.md`
  files; their definition is the doc's `> ` blockquote lede.
- Vernacular rows are curated. They survive regeneration verbatim,
  including any `<!-- unconfirmed: YYYY-mm-dd -->` markers.
- Bar for a vernacular row: meaning in this repo is distinct from
  default agent usage. Generic terms an agent already understands
  do not belong.
- This topic doc holds the contribution and regeneration procedures.
  `GLOSSARY.md` itself stays free of build instructions for readers
  who only look up terms.

## Topic-doc format the spec relies on

H1 stating the topic, blank line, `> ` blockquote lede (one or more
`> ` lines, nothing else between H1 and lede), blank line, optional
`Topic: <name>` trailer, then body. See `AGENTS.md § Project topics`
for the auto-fix license that lets the agent normalize existing
docs into this format.

## Adding a term

Add a vernacular row when a term is truly project-specific — its
meaning here is distinct from default agent usage. Generic terms an
agent would already understand do not belong. Sort alphabetically by
term; leave `topic / refs` empty unless the row corresponds to a
`topics/<name>.md`.

For a row added during conversation as a tentative resolution of
ambiguity, flag with `<!-- unconfirmed: YYYY-mm-dd -->`. The user
confirms by removing the marker or prunes the row; either way the
marker survives regeneration until acted on.

## Regeneration

Scan `topics/*.md` from repo root, excluding `*.evidence.md`
companion files. For each topic doc, read the `> ` blockquote lede
immediately after the H1 — multi-line `> ` lines are space-joined
into one sentence — and use it as the definition of the row whose
`topic / refs` column links the corresponding `topics/<name>.md`.
When a topic doc lacks a `> ` lede, synthesize one from its first
body paragraph and apply the fix as part of regeneration (per the
topic-doc auto-fix license in `AGENTS.md § Project topics`).

Vernacular rows (no `topic / refs` link) are preserved verbatim on
regeneration, including `<!-- unconfirmed -->` markers. Do not pull
rows from `~/agents/topic-definitions.md` — that file is a
multi-field reference, deliberately not loaded per conversation.

## Design decisions

- **Location at repo root** (vs. `topics/README.md`): prioritizes
  top-level discovery and avoids duplicating what the glossary
  already does; accepts losing co-location with topic-doc inputs.
- **`GLOSSARY.md` holds only the table** (vs. embedding the regen
  spec inline): prioritizes signal for everyday readers who only
  look up terms; accepts that contributors must navigate to
  `topics/glossary.md` for build/contribution rules.
- **One sorted table** (vs. sectioned by kind): prioritizes
  mechanical name-based lookup; accepts losing at-a-glance grouping
  by category.
- **No `type` column** (vs. tagging rows by kind): prioritizes
  visual cleanliness — topic-vs-vernacular is implicit in whether
  the `topic / refs` column has a link; accepts losing programmatic
  filtering by kind.
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

## Ambiguity-resolution behavior

When a user phrase is ambiguous against the glossary, see
`AGENTS.md § Project glossary` for the checkpoint protocol: state
the inferred meaning plus 1–2 alternatives, continue at normal pace
when the fork is minor or cheaply reversible, hold for the reply
when proceeding wrong would waste significant work. On resolution,
propose adding a row flagged `<!-- unconfirmed: YYYY-mm-dd -->`.
