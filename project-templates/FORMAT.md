# Project template format

This is the agreed content/composition contract for the initial library.
The checked-in manifests remain draft while their instruction review is open.
`composition.py` implements local source validation and composition, and
`project-template.py` exposes validation, inspection, and creation for authors.
YA implements remote source settings and combined-source validation;
project creation and preparation through YA remain under integration.

## Library and source boundary

A configured source identifies a local repository or a GitHub repository/ref,
plus its **relative content root**. YA defaults to GitHub repository
`https://github.com/graehl/agents` and `project-templates`; the local authoring
tools use this checkout. An empty content root means the repository root.
The directory contains `library.json`:

```json
{
  "formatVersion": 1,
  "bases": ["base"],
  "templates": ["app-canvas"]
}
```

Each entry resolves to `bases/<id>/template.json` or
`templates/<id>/template.json`. IDs are lowercase letters/digits separated by
single hyphens, beginning with a letter. IDs must be unique across both lists.
Only templates can be selected to create projects; `base` is reserved for the
universal base. Listing reads this finite inventory and creates nothing.

A source is admitted only after verifying the configured content directory,
inventory, manifests, inheritance graph, and referenced files. A missing
directory is a configuration error, checked on the local filesystem or in the
selected GitHub revision before saving/enabling the source. An unavailable
GitHub source is a validation failure, not an empty library. Resolve a remote
ref to a fixed revision for validation and use that same snapshot for creation;
do not validate one revision and execute another. Never execute setup scripts
while listing or validating configuration.

All `from` paths are relative to the manifest that contains them. Relative
`../` references and source symlinks are allowed, but every resolved target
must stay within the source repository. Absolute paths, broken links, symlink
cycles, escapes from the repository, and references into Git's private
metadata are errors. GitHub sources follow the same rule using the snapshot's
tree and symlink contents, not the consumer's host filesystem. Validate again
when reading a mutable local source for creation. Draft files are validated
too; draft status is not permission for dangling source references.

YA reads local directories directly, without copying or rewriting their files.
If a local directory belongs to a Git worktree, that worktree is its source
boundary and its HEAD is informational provenance. Otherwise the selected
directory is the boundary and there is no commit SHA. Every manual update
revalidates local files; an unchanged HEAD does not imply unchanged working
content. GitHub and local directories may both be supplementary overlays.

YA combines an ordered list of sources: later base or template definitions
replace earlier definitions with the same ID, without changing their kind.
Base IDs in `extends` resolve in that combined inventory, so community
templates can reuse YA-default bases. Source-file references still resolve
within the repository that owns the winning definition. Definition replacement
does not relax the project-file collision rules below.

A saved creation selection must identify its effective source as well as its
template ID; adding another source must not silently redirect a limited user's
allowed template. The local Python authoring tools still validate a single,
self-contained library. Combined-source validation is provided by YA, not by
those tools. Every source must include its own file dependencies within its
repository boundary.

## Manifest shape

Every manifest has this shape; `kind` is `base` or `template` and `status` is
`draft` or `ready`:

```json
{
  "formatVersion": 1,
  "kind": "template",
  "status": "draft",
  "id": "app-canvas",
  "title": "App canvas",
  "description": "A static TypeScript canvas app; add a server later.",
  "extends": ["base"],
  "files": [],
  "overrides": []
}
```

Fields are explicit; unknown fields, invalid kinds/statuses, or a mismatch
between the inventory entry and manifest ID/kind are errors. `extends`,
`files`, and `overrides` are ordered arrays. A base has an empty `overrides`
array. `draft` means usable for authoring/composition inspection, not project
creation. A ready template cannot depend on a draft base.

A file contribution is `{ "to": "instructions/testing.md",
"from": "files/testing.md", "executable": false }`. Each source is one
file; there are no implicit directory walks, globs, token substitutions, or
deep merges of JSON. `executable` is optional and defaults to false, independent
of source permissions. Destinations are normalized project-relative POSIX
paths: no absolute paths, empty/`.`/`..` segments, backslashes, or `.git`
segments. Reject file/directory prefix collisions and case-folded name
collisions for portability, rather than overwriting by platform accident.

## Template preview

A template may contribute `.project-template/preview.svg` through its ordinary
file map. This optional illustration evokes the template's purpose; it is not
a screenshot or promise of the finished app. The chooser reads the composed
asset without executing setup, and instantiation vendors it like other files.
Normal collision and override rules apply. With no preview, show the template's
title and description without inventing an asset dependency.

Keep the SVG self-contained: no scripts, external resources or embedded HTML.
Consumers display it as an image, not inline markup or an embedded document.
Its `viewBox` allows responsive scaling; the chooser supplies accessible text
from the template title. Authoring sources conventionally keep `preview.svg`
beside `template.json`; the explicit file map remains authoritative.

## Project-visible skills

Bases and templates may contribute skills through ordinary file mappings into
the supported harness's conventional project discovery directory, for example
`.agents/skills/<name>/SKILL.md`. List each skill's supporting instructions,
scripts and resources explicitly. These files follow the same source-boundary,
vendoring and collision rules as other content; installation must not depend
on the template author's global skill directory or an external symlink.

Use the normal harness discovery and invocation conventions, not a YA-only
skill registry. Declare any additional harness-specific discovery paths
explicitly and verify discovery in the supported harnesses. Root `AGENTS.md`
may point to the available skills without inlining their complete bodies.
The project README should briefly introduce bundled skills, when they help,
and how to invoke them. Beginner onboarding should teach that skills exist,
including for limited users, without requiring knowledge of their file layout.

The universal base supplies `redoc` for autonomous documentation maintenance,
including a project-specific README SVG brand. Its
[identity reference](bases/base/redoc/references/project-identity.md) defines
the optional project-root `.project-identity.json` record for later human
name/description edits. Creation does not write that record or protect initial
intent. Redoc respects this specific exception without tracking authorship of
ordinary documentation. The template chooser's preview and the project's
evolving `docs/brand.svg` are separate assets.

## Multiple bases

Both bases and templates may extend an ordered list of bases. The transitive
closure is a directed graph, not a single-parent chain. Resolve all dependencies
before materializing anything; missing bases, cycles, and inconsistent ordering
are errors. Reaching a shared ancestor through several paths applies it once.

The linear order must respect dependency-before-dependent and the left-to-right
order of each `extends` list. Use a stable topological order, breaking otherwise
unconstrained ties by first encounter during a left-to-right depth-first walk
from the selected template. This permits interleaving dependencies when needed;
blindly emitting depth-first postorder and rejecting the result is insufficient.
The selected template contributes last.

For example, bases A and B can both extend `base`. A template extending
`[A, B]` yields `[base, A, B, template]`. If A demands `[X, Y]` and B demands
`[Y, X]`, fail with the conflicting order constraints. Do not silently discard
one ordering to make the composition succeed.

## File union and harmless collisions

For every destination **except root `AGENTS.md`**, base composition is an
ordinary union:

- Same path, same bytes, same executable mode: keep one file and retain all
  contributors in composition diagnostics. Source path and symlink spelling
  do not matter.
- Same path, different bytes or executable mode: report a conflict with the
  destination and contributors. There is no implicit last-writer-wins rule.
- Different paths, identical content: retain both paths; their locations may
  matter to imports or instruction routing.

Compare source bytes without whitespace, newline, Unicode, or Markdown
normalization. A content hash can accelerate comparison. Nested `AGENTS.md`
files are ordinary files: only the exact destination `AGENTS.md` is special.
The selected template's ordinary `files` use the same rule; deliberate changes
to inherited files belong in `overrides`.

### Root AGENTS.md

Visit root instruction contributions in resolved base order, then manifest
`files` order, then the selected template's contributions. Hash each whole
fragment's original bytes with SHA-256. Keep its first occurrence and skip
subsequent fragments with that hash. Deduplication is by content, not by source
path, base name, heading, paragraph, or semantic similarity. Equal text at two
different source paths therefore appears once. All fragments must be valid
UTF-8 text and non-executable.

Concatenate the retained fragments in that order. Preserve their bytes and
insert only enough LF bytes at each boundary to supply a blank line (two LF
bytes across the end/start boundary). An empty fragment contributes nothing.
Hash before inserting separators. Different whitespace means different content
and is not automatically deduplicated. Do not rewrite relative links: fragments
must already address their declared vendored destinations from project root.

Example: fragments `[A, B, A, C]` produce `[A, B, C]`, with blank lines between
them. Reordering to `[B, A, C]` changes instruction order deliberately; adding
another path to the same A content changes neither content nor multiplicity.

## Explicit template overrides

After composing the base union and the template's contributions, apply the
selected template's `overrides` in listed order:

| Operation | Required fields | Effect |
|---|---|---|
| `replace` | `op`, `to`, `from`; optional `executable` | Replace the inherited file or create a new one. |
| `prepend` | `op`, `to`, `from` | Prepend UTF-8 text to an existing file. |
| `append` | `op`, `to`, `from` | Append UTF-8 text to an existing file. |
| `omit` | `op`, `to` | Remove the inherited destination from the result. |

For example:

```json
[
  { "op": "omit", "to": "instructions/deploy.md" },
  { "op": "replace", "to": "README.md", "from": "files/README.md" },
  { "op": "append", "to": "AGENTS.md", "from": "files/project-notes.md" }
]
```

Append/prepend preserve executable mode and insert one LF only when both
nonempty sides otherwise join without a newline. Replace uses its declared
mode, defaulting to non-executable. Omit and text operations require an existing
destination. Omit accepts no source; text operations accept no executable flag.
Binary files support replace/omit only. Template overrides are intentional
edits, not base contributions, so they are not hash-deduplicated.

An ordinary-file union conflict may be resolved by a template whose first
override for that destination is replace or omit: either operation needs no
choice of inherited content. An append/prepend cannot resolve a conflict,
because there is no single inherited file to edit. Absent explicit resolution,
report the conflict before writing anything. This keeps normal base overlay
trivial while retaining deliberate template exceptions. A replacement followed
by append is legal; an omit followed by append fails because no file remains.

## Vendoring and later capabilities

Instantiation copies the selected payload into a fresh project as ordinary
files; authoring symlinks are dereferenced. No runtime path, instruction route,
import, or script may depend on the source checkout. Explicitly selected
instruction routes must resolve to included files. A README lede describes the
actual project; the preparation turn refines it from the entered intent and
the ongoing documentation instruction keeps it current.

A capability offered for later use, initially the optional server, includes
its instructions, configuration, scripts, and required source files in the
vendored inventory without activating the capability. Later application must
preserve customized project files; the fresh-directory union is not permission
to overwrite an existing project. The add-on application contract and concrete
payload layout remain implementation work, and the first template must not
claim that later-server path works until it is tested without this repository.

Copying a boot file whose internal links point back to this repository does
not satisfy vendoring. The initial seed intentionally demonstrates that gap,
rather than pretending the global boot is already a portable universal base.

## Runtime configuration

The App canvas vendors `.project-template/app.json`: `kind` is initially
`static`, `dir` is `dist`, and `setup`, `build`, `test`, and `preview` are argv
arrays executed from project root, without shell interpolation. `prepare` names
the vendored first-turn prompt; `addons.server` names its activation command.
The authoring CLI currently consumes `setup` only. The server add-on changes
`kind` to `server` and adds `start`; neither operation contacts YA.

The materializer reserves `.project-template/project.json` for project name,
description, and composition provenance (base order, file hashes, and source
paths relative to the source repository). Setup uses that data to seed the
README without source token substitution. An already customized README is
preserved on a later setup run. Runtime and publishing actions remain separate:
creating a project does not authorize publication.

## Conformance cases

The consumer's tests must cover these observable cases, through its actual
composition/materialization path rather than a second implementation in tests:

| Input | Expected result |
|---|---|
| Diamond inheritance with a shared `base` | Shared ancestor applied once. |
| Consistent interleaved dependency ordering | Valid stable topological order, not a false cycle. |
| Opposing sibling-order constraints or inheritance cycle | Error naming the conflicting nodes. |
| Two files at one path with identical bytes/mode | One file, both sources in diagnostics. |
| Same path with differing bytes or executable mode | Conflict unless explicitly replaced/omitted by the template. |
| Root fragments A, B, A from distinct paths | A then B, A only once. |
| Two different nested `AGENTS.md` files at one destination | Ordinary-file conflict, not concatenation. |
| Equal content at two different destinations | Both files retained. |
| Omit then append at one destination | Error; no absent-file fallback. |
| Repository-contained `../` reference or symlink | Bytes copied; output has no source symlink. |
| Missing source root, broken link, or escaping target | Error before creation or script execution. |
| Draft template or ready template with draft dependency | Refused for creation. |
| Source repository removed after instantiation | Build/test/run and supported add-ons still work. |
