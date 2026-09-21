# Story project layout

> Declarative file layout for a story project of any length, from one short
> story to a novel or screenplay: a premise file, a style sheet, `setting/`
> and `personae/` reference sheets that each own their facts, an outline of
> acts, optional beat sheets, chapters or scenes as the draft, and a
> continuity ledger. Directories are created on first need, never scaffolded
> empty.

Topic: `story-project-layout`

Read this before creating or reorganizing the files of a story, screenplay,
or world-building project, or when asked where a character, place, or plot
note belongs. Craft is in [`story-writing`](story-writing.md) and
[`writing`](writing.md).

## Principles

- **One owner per fact.** A character's eye color lives in that character's
  sheet; a town's founding date lives in the town's sheet; the draft quotes
  them. When the draft and a sheet disagree, the sheet is authority until the
  author decides otherwise, and then the sheet is updated first.
- **Reference sheets are compact.** A sheet holds what the story uses plus
  what keeps the writer consistent. It is not a wiki; length is a cost.
- **Create on first need.** A short story is one file. Add `personae/` when
  a second character needs a sheet; add `setting/` when a place has rules;
  add `beats/` when an act is being planned scene by scene. No empty
  directories.
- **Plain text, ordinary files.** Markdown for prose and sheets; Fountain
  for screenplays. Everything diffable, nothing that needs an application.
- **Status is visible.** The project's `README.md` (or `story/README.md`
  inside a larger project) says what exists, what is drafted, and what is
  next, so a fresh session can orient in one read.

## Layout

A standalone story project puts this at the root; a project that also
contains a web page or other work keeps it under `story/`. Paths below are
relative to that root.

```text
README.md            premise, logline, genre, audience, target length, status
prose-style.md       voice, register, point of view, tense, spelling, names
illustration-style.md  whether images are wanted, medium, palette, mood,
                       recurring subjects; absent means no images unasked
setting/
  README.md          index of places and systems; the world's few hard rules
  <place-or-system>.md   one sheet per location, faction, institution, magic
                         or technology system, era
personae/
  README.md          cast list: name, role, one line, arc in one line
  <character>.md     one sheet per character who recurs
outline.md           acts and their chapters/sequences, one line each
beats/
  act-1.md ...       optional scene-by-scene beat sheets per act or chapter
chapters/            the draft, one file per chapter: 01-<slug>.md
  (or scenes/ for a screenplay, or script.fountain as a single file)
continuity.md        ledger of facts asserted in the draft, with locations
research/            notes and sources the story draws on (optional)
```

For a screenplay, `treatment.md` (a prose synopsis) sits beside
`outline.md`, and the draft is `script.fountain` or `scenes/NN-<slug>.fountain`.

For interactive fiction, `scenes/` holds one file per node and `graph.md`
lists the edges (`from → choice → to`) and the state each choice reads or
sets.

A collection of short stories uses `stories/<slug>.md`, each with a short
premise header, and shares `prose-style.md` and, when characters or a world recur,
the same `personae/` and `setting/`.

## Sheets

Vendored projects carry fill-in starters for each sheet under
`instructions/writing-starters/`; copy one to its home and fill it in. The
two style records live at the project root even when the story sits under
`story/`, because a page and its story share one voice and one look; a
project with several unrelated works may keep per-work copies beside each
work's README, and the nearest one wins. Both are set with the author, not
inferred: ask what the prose should sound like and whether illustrations are
wanted and in what style, offering concrete alternatives, and record the
answers. The headings, and what each is for:

**README.md (premise):** title; logline (one sentence: when, who, must, or
else, but); premise (Egri's causal sentence); genre and audience; target
length and form; point of view in one line; the ending in one line (written
down early, changeable later); status table: acts or chapters with
planned/drafted/revised.

**prose-style.md:** voice in three words; register and reading level; point
of view and tense; how many point-of-view characters (usually one) and when
the story switches; the narrator's voice and whether the narrator is
reliable; spelling and punctuation conventions (dialogue quotes,
numbers, capitalization of invented terms); a names list with pronunciation
for invented names; words and habits the narrator uses or avoids; content bar
for this project (the default is all ages; see `story-writing`).

**illustration-style.md:** whether illustrations are wanted and how many
(none, a cover, one per chapter, as needed); medium; palette; line and shape;
mood in three words; the author's reference points, used as inspiration and
not as a living artist's signature style to copy; file format and where
images go; how images are made; a table of recurring subjects with the
details that must stay consistent; what is not wanted. Every placed image
gets alt text. When the file is absent, the project has no illustrations and
the agent asks before adding any.

How images are made is recorded so every image is produced the same way.
Prefer, in order, whatever is actually available in the session: a
purpose-built illustration model that accepts text context, fed the scene,
the relevant character and setting sheets, and the style record; the
harness's native image generation with the same context in its prompt; and
last, SVG drawn by the agent, which suits flat and line styles and stays
editable. Do not claim a generator is available without checking; record the
tool and the prompt template in the style file once it is chosen.

**personae/<character>.md:** name and any aliases; role (protagonist,
antagonist, ally, foil); one-line summary; want; need; the lie they believe;
ghost or wound; skill; flaw; contradiction; voice (how they talk, a sample
line); appearance tag (the two details the reader recognizes); relationships
(one line each, with how it changes); arc (start state to end state); first
and last appearance.

**setting/<place-or-system>.md:** name; what it is in one line; what the
story uses it for; sensory signature (the two or three details); rules and
costs (for a system: what it can do, what it cannot, what it costs, who
knows); history the story touches; who lives or works there; open questions.

**setting/README.md:** the world's hard rules in a short list (the things
that must never be contradicted), an index of sheets, and a timeline when
the story spans time the reader must track.

**outline.md:** for each act, its purpose in one line and the irreversible
turn it ends on; under each act, its chapters or sequences with a one-line
summary and the value that changes. The midpoint and the climax are marked.

**beats/<act-or-chapter>.md:** per scene: number, location, point-of-view
character, goal, conflict, outcome (yes-but or no-and), what the reader
learns, what is planted or paid off. A scene table is fine.

**continuity.md:** a table of facts asserted in the draft: fact, where
stated (chapter and paragraph or scene), owning sheet, status
(consistent, conflict, unresolved). Add rows during drafting; walk the table
during the continuity pass.

## Working rules

- Before drafting a scene, read the sheets of its point-of-view character and
  its location. After drafting, add the facts it asserted to `continuity.md`.
- When a character or world fact changes, change the owning sheet first,
  then search the draft for every place that fact appears, then update the
  ledger.
- A revision that changes structure updates `outline.md` in the same change.
  The outline describes the draft as it is, with planned chapters marked as
  planned.
- Keep the README status table current at milestones (act drafted, revision
  pass complete), not after every edit.
- Do not scaffold sheets for characters who appear once or places with no
  rules. A line in the cast list or the setting index is enough.
