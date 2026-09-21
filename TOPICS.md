# Topic vocabulary reference

This file is a granularity and scope anchor for topic docs in any project.
Read it when creating a new topic, reviewing whether an existing topic is
scoped correctly, choosing its owning glossary, or doing a periodic
global-consistency pass.

A topic spans a concern with consumers beyond one module's internals; a
module-only explanation usually belongs in its README. For examples of topic
names and field vocabulary, consult [`topic-definitions.md`](topic-definitions.md)
only when useful. That human reference is not a required read for placing a
topic or interpreting a program charter.

## Landing-site principles

Where a durable note lands — which doc, which section:

- Name the retrieval trigger first: who needs this fact, and what
  sends them looking? Land where that reader will look; if no
  trigger is nameable, reconsider landing it at all.
- Match the file's loading regime: decision surface in rule files
  (boot or topic), rationale and mental models in `.evidence.md`, dormant
  candidate designs in `.sketches.md`, intended future implementation in
  `gaps/sketches/`, unresolved defects or contract gaps in `gaps/`, and live
  continuity in program-scoped handoffs.
- One home plus pointers, never two homes for the same claim.
- Prefer the broadest active glossary scope where the note remains natural and
  unqualified. Default to the current project, retain subtree/program scope
  when a parent doc would mostly name qualified local paths or concepts, and
  promote when real utility widens. `~/agents` is reserved for clearly reusable
  general agent workflow or explicit user direction.

## Glossary-owned topic scopes

Every named term in an active `GLOSSARY.md` is topic-like. Its `topic / refs`
cell may point to any canonical doc; an existing proposal, draft, handoff, or
other doc wins over layout normalization. “The topic for X” therefore means:
resolve X through the nearest applicable glossary row, then follow its
canonical reference. Search outward through enclosing glossary scopes only
when the nearer scope does not define X.

When X needs a new formal topic doc, place it in the `topics/` collection owned
by the selected glossary. If the project has no root `GLOSSARY.md`, treat the
project root as the implicit scope for its first ordinary topic; it owns root
`topics/` (or the established `docs/topics/` alternate), and that first topic
does not by itself require creating a glossary. A project-root glossary, once
present, owns the same collection; a scoped glossary owns the sibling
`topics/` directory. A research-program glossary at
`research/pii/GLOSSARY.md`, for example, owns `research/pii/topics/`. A scope
that owns `topics/` may likewise own a sibling `gaps/`, created on first
need; root `gaps/README.md` governs its format and granularity.

Topic names keep owner context without exposing the mechanical collection
directory. A root topic uses its basename, while a scoped topic prefixes the
basename with the owning glossary's project-relative directory:

```text
topics/redaction.md              -> redaction
research/pii/topics/redaction.md -> research/pii/redaction
```

These names are used in `Topic:` commit trailers. Basenames need not be
project-wide unique, and an existing root topic name or historical trailer is
not migrated merely because scoped topics become available.

## Program scope charters

A program is a coherent subproject: related work with durable aspirations and
boundaries that give its topics a shared purpose. Software, research, writing,
and other projects all use this concept. A project may itself be one program
and may contain more specific programs; a directory alone does not establish
one. `PROGRAM.md` declares the scope. New handoffs belong to the most specific
program owning the work, with project root as the fallback; see
[handoffs](topics/handoffs.md).

A glossary scope may have a sibling `PROGRAM.md`. It is a concise durable
statement of the aspirations, themes, and boundaries spanning that scope—the
reason its topics form one program. Its presence declares a program scope and
is the sole declaration used for program discovery. Keep plans, current
status, per-topic summaries, run history, and handoff state in their existing
owners.

A title is optional. When the first line is an H1 of the form
`# Program <short name>`, it supplies an alternative formal name. The containing
directory path remains the program's canonical locator, and discovery never
depends on the title.

A nested `PROGRAM.md` specializes the nearest parent charter and should not
repeat it. Read the parent when interpreting or updating the child, except at
an explicit [self-rooted boundary](#self-rooted-programs). An old
`Research program: <slug>` glossary header may coexist as inert compatibility
metadata, but program discovery uses `PROGRAM.md` only.

### Program instructions

A Markdown heading at any level named exactly `Program instructions` marks a
binding section of `PROGRAM.md`. Its content and nested subsections govern work
in the directory containing that file and its descendants; the section ends at
the next heading of equal or higher level. Program instructions in ancestor
directories apply inward within the governing chain, and the nearer rule wins
when two conflict. They do not override applicable global or project agent
instruction files. Outside such sections, only the explicit self-rooted
declaration below changes program inheritance; other text is descriptive.

Create or revise program instructions only from explicit user direction. In
particular, inferring a missing charter or handling “update program scope” must
not invent, remove, or reinterpret them.

At project entry, discover project-owned `PROGRAM.md` paths. For a named scope,
fully read its governing chain: its own charter and every parent through the
nearest self-rooted declaration, or the project root when none exists. Parent
links are unnecessary. With no named scope, read the root charter when present.
Read all programs for project-wide orientation, scope selection across
programs, audits, or changes.
A root charter's optional child list is not authoritative; discovery still
scans for charters. Exclude vendored dependencies and external repositories.

On “update program scope,” choose the nearest applicable glossary scope and
reconcile its descriptive charter against, in order: explicit recent user
direction, the existing charter, glossary definitions and canonical topic docs,
and current repository evidence. If the file is absent, infer and create the
probable charter when those sources support a coherent program. Mark a
consequential uncertainty rather than converting it into false certainty.
“Update all program scopes” repeats this for every existing charter and every
glossary scope whose artifacts support such a program; a plain vocabulary
scope does not gain a charter merely to make the sweep exhaustive.

### Self-rooted programs

Only on an explicit user request to make a program self-rooted, place the
standalone line `Program root: self` near the top of its `PROGRAM.md`, outside
code examples. That charter becomes the program root for itself and descendants
until a deeper self-rooted declaration. Subsequent sessions stop program-parent
reads and inheritance there; they need not check parents for changes. Ordinary
scope inference or a convenience wish to shorten boot does not authorize the
declaration.

Before establishing the boundary, read the existing governing chain and compile
the inherited intent, applicable requirements, and needed vocabulary into the
subtree's charter and locally owned detail documents. Preserve trigger, action,
and persistence spans; record any deliberately omitted or changed requirement
and its user authorization. The resulting program must be usable without
parent-policy consultation. Do not add the declaration while that compilation
has unresolved dependencies. Historical source references may remain without
restoring inheritance; future parent changes apply only through a deliberate
update of the compiled context.

This boundary affects program context only. Global/project `AGENTS.md`, local
amendments, and other independently governing instructions still apply.
