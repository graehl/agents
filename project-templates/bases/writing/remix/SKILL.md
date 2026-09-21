---
name: remix
description: Make an alternate version of this project's writing in its own subdirectory, without touching the original, by re-asking the core questions (who it is for, how it should sound, point of view and narrator, whether and how it is illustrated) and rewriting under the new answers. Use when the user invokes /remix or $remix, or asks for "a version for younger readers", "the same story in first person", "an illustrated version", or similar.
---

# Remix

A remix is the same work, re-made under different answers to the core
questions, kept beside the original. The original is never edited or
replaced by this skill. The end state is a subdirectory that holds its own
`audience.md`, `prose-style.md` and `illustration-style.md`, a README saying
what it is a remix of and what changed, and a complete alternate version
that any later session will keep consistent with those local records.

## Resolve the target

`/remix <target> <what to change>` names a work and, optionally, the change.
The target may be the whole project, `story/`, one document, or one
chapter. Bare `/remix` targets the most recently discussed work, else the
whole project's writing. If the target is unclear, ask which work, once.

Find the records that currently govern the target: the nearest `audience.md`,
`prose-style.md` and `illustration-style.md` walking up from the target to
the project root. Those are the baseline answers. If any is missing, the
baseline for that question is "not yet decided".

## Re-interview

Ask the core questions again, showing each current answer as the baseline
and, for each, a riff of three or four concrete alternatives to pick from
(use `.agents/skills/riff/SKILL.md` when it is available). The author may
keep any answer unchanged. In order:

1. **Who is this version for?** (age or reading level, what they know, what
   they come for, how they read it)
2. **How should it sound?** (register: plain, playful, formal, lyrical;
   reading level; sentence length; the rules of the house such as spelling
   and dialogue punctuation)
3. **Whose eyes, and what narrator?** (how many point-of-view characters,
   usually one; first or third person; past or present; the narrator's own
   voice; reliable or not) Explain each option with a one-line example, not
   the term alone.
4. **Pictures?** (none, a cover, one per chapter, as needed; medium, palette,
   mood; how they are made)

Explain a craft term once with a short example, then use plain words. With
a new or young writer, keep to these four questions. Stop asking when the
answers are in; do not add questions about plot or characters, which the
remix keeps unless an answer forces a change (a younger audience may need a
scene softened or cut; say so and ask).

## Create the remix directory

Choose a short slug from what changed: `for-younger-readers`,
`first-person`, `illustrated`, `formal`. Create `remixes/<slug>/` beside the
target's README (project root, or `story/` for a story under a larger
project). Never write into an existing remix without being asked; a second
remix with the same slug gets a numeric suffix.

Inside it, before any prose:

- `README.md`: "Remix of `<source path>`", the date, and a short table of
  what changed: question, original answer, this version's answer.
- `audience.md`, `prose-style.md`, `illustration-style.md`: copies of the
  governing records with the new answers filled in. These are now the
  nearest records for everything under the remix directory, so later edits
  there follow them automatically.

Shared canon stays shared: a story remix does not copy `setting/` or
`personae/`; it reads the originals. If an answer requires a canon change
(a character renamed for a younger reader), record it in the remix README
as a local deviation, not in the shared sheet.

## Produce the alternate version

Rewrite the target under the new records, file for file, keeping the source
layout and file names inside the remix directory so the two versions line
up. Keep the story's events, facts and structure unless a new answer
requires otherwise; a remix is not a rewrite of the plot. Apply the writing
guidance in `instructions/writing.md` and, for fiction,
`instructions/story-writing.md`, including the sweep for machine-prose
habits. Make illustrations only if the illustration record for the remix
asks for them, in the way it names.

For a long work, produce the first chapter or section, show it, and confirm
the direction before doing the rest; then finish the whole target. Do not
leave a remix half-made without saying so in its README.

## Report

Say where the remix is, what changed in one short table, and that the
original is untouched. Offer the next step (another remix, or promoting this
version) but do not promote, merge, or delete anything under this skill.
