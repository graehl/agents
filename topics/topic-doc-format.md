# Topic-doc format and companion vocabulary

> Layout of a `topics/<name>.md` doc — H1, blockquote lede,
> trailer, body — and the suffix vocabulary for companion
> artifacts (`.evidence.md`, `.runs/`, `.bearings.md`, `.testing.md`).
> Includes the glyph set for `.bearings.md` plan outlines.

Topic: `topic-doc-format`

## Main topic doc

H1 stating the topic, then a `> ` blockquote lede (one or more `> `
lines, no other content between H1 and lede; multi-line `> ` lines
are space-joined when consumed by glossary regeneration). The lede
is the canonical one-sentence definition consumed by `GLOSSARY.md`.
Then optional metadata such as a `Topic: <name>` trailer, then
body sections.

The agent may auto-edit existing topic docs to bring them into
this format without separate confirmation — synthesizing a missing
lede from the first body paragraph, moving stray trailers — as
long as the edit preserves body content faithfully.

## Companions

Structured ancillaries ride alongside the main topic doc as
`topics/<name>.<suffix>`. The suffix is either a `.<suffix>.md`
file or a `.<suffix>/` directory, by convention:

- `.evidence.md` — verification ledger, append-only. See
  `topics/evidence-ledger.md`.
- `.runs/` — curated run records. See `topics/runs-ledger.md`.
- `.bearings.md` — current orientation; see next section.
- `.testing.md` — optional rider: how to check a change to the
  topic's concern before committing. See
  `topics/testing-rider.md`.

The main topic doc stays free-form prose; concerns with their own
structure live in suffixed companions rather than dedicated
sections of the main doc.

## Bearings outline format

`topics/<name>.bearings.md` is a nested outline of plan items.
Each non-leaf node carries `> why: <one line>` so the chain of
"why we opened this" reconstructs by reading parent → child whys.
`> why:` is required where non-obvious, optional on self-evident
leaves.

Status markers per node:

| glyph | meaning |
|---|---|
| `[ ]` | planned |
| `[*]` | active |
| `[~]` | paused/blocked |
| `[x]` | done |
| `★` | high-value (optional adornment) |
| `‖` | plan boundary — a momentum checkpoint (see `AGENTS.md § Plan-boundary checkpoints`) |

The active backtrace is the chain of `[*]` from root to deepest
active leaf — a single highlighted spine through the tree.

## Epistemic labeling

An unlabeled claim means "plausible, not verified". Add an inline
HTML comment only when its absence would mislead:

- `<!-- verified: SHA abcdef0 -->` — confirmed by test, bisect, or
  audit.
- `<!-- assumed -->` — unverified design intent.

When a commit weakens a verified claim it touches, downgrade that
claim's marker rather than leaving it stale. Do not use
"last updated" dates.
