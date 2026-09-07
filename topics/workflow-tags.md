# Workflow tags

> Workflow tags are a reusable schema type in which bracketed key paths group
> subsequent agent activity and optionally tagged tool output into nested stages
> of an identified workflow.

Topic: `workflow-tags`

Status: Initial producer convention, 2026-09-07. A skill or project instruction
opts into it; this topic does not require tags for ordinary work. Renderer and
harness support are separate capabilities. Read this topic when adopting or
changing a `tagged-stages/1` workflow. This is one visualization schema type;
activation is separate from its outline/tag interpretation.

## Explicit activation

Ordinary bracketed text never activates a visualization. An activation record
consists of the uncommon, column-one marker `@@visualization-schema/1` followed
immediately by a fenced `json` block. Its payload is exactly one of:

- the complete declaration, identified by `type` and `id`;
- `{ "schema": "~/agents/path/to/schema.json" }`, a declaration pointer; or
- `{ "skillFile": "~/agents/skills/example/SKILL.md" }`, a pointer to a skill
  whose metadata supplies the declaration pointer described below.

The record must be surfaced in the current turn's agent output or a tool
result. Reading an opted-in skill can also activate through its metadata.
Having a schema file on disk, listing an installed skill, mentioning its name,
or seeing `[A]` in a log is insufficient.

The record's `type` selects the visualization contract; `id` identifies the
specific declaration. `tagged-stages/1` is the first predefined type, not the
meaning of every activation record. Other types may define different views
and update conventions. Unknown types remain readable data without activating
this tag parser. Conflicting declarations under the same schema ID are invalid.

The activation marker is outside the following JSON fence; examples quoting
the whole record are not activation. A producer can surface the record directly
or through skill/tool content, then refer to the resolved schema ID when
opening a workflow. Do not re-emit its full declaration at every stage.
Activation lasts for the current turn and does not itself execute anything.

`toolOutput.containsTags` and its whitelist govern stage-prefix recognition
after activation. They do not govern the separate activation record. Merely
printing a bracketed lifecycle-looking path in tool output is not activation.

## Skill metadata and file resolution

The skill-content field is **`metadata.visualization-schema`**, a string in
`SKILL.md` YAML frontmatter:

```yaml
---
name: example
description: Perform the example workflow.
metadata:
  visualization-schema: ./references/workflow.json
---
```

This is a proposed consumer convention using the Agent Skills specification's
[string-valued custom metadata](https://agentskills.io/specification#metadata),
not a claim that provider harnesses already interpret it. The named file
contains the complete visualization declaration, including its schema type.

YA's activation trigger would be an actual skill invocation resolved by the
provider, an observed read of its `SKILL.md` content carrying this metadata,
or the explicit activation record above. This includes agent-selected skills;
it does not require a user-entered slash command. Inventory discovery alone
does not activate every installed skill's visualization.

Resolve locations on the host that owns the session, through its existing
file-access path:

1. A provider-reported skill-definition path is authoritative for the resolved
   invocation. Otherwise use the observed skill-read tool's source path or an
   explicit `skillFile` pointer. A skill name alone is insufficient; do not
   invent precedence by searching guessed skill directories.
2. Absolute paths refer to that host. Expand `~/` using that session owner's
   home directory, never the browser's home or a different YA host's home.
   Thus `~/agents/...` explicitly names the shared agents checkout; it is not
   an implicit search root.
3. Inside skill metadata, resolve a relative pointer against the directory of
   the resolved skill file, following symlinks to its actual source. An
   installed alias therefore keeps the source skill's adjacent resources.
4. A standalone `schema` or `skillFile` pointer must be absolute or `~/`-relative.
   Reject an unbased `path/to/schema` rather than guessing between project cwd,
   home, and `~/agents`. A displayed `[path/to/schema]` is not itself activation.
5. A schema pointer names a JSON declaration or a document containing explicit
   activation/declaration blocks. A `#schema-id` fragment selects the exact
   declaration ID; without it, the document must contain exactly one declaration.
   For example, `~/ya/topics/publish-workflow.local.md#ya-publish/1` is explicit.
   Do not follow chains of pointer blocks as if they were declarations.

Instructions need not know the checkout's installation location. Prefer
skill-relative metadata when the schema travels with the skill. The provider's
resolved path or the agent's actual file-read path supplies the base; follow
installation symlinks rather than prepending a remembered `~/agents`. If files
were copied instead, adjacent resources belong to that installed package.
An agent that emits a standalone pointer should use the path it actually read,
optionally shortening a verified home prefix to `~/`. Injected text without
source provenance does not establish its own filesystem location.

If surfaced skill content has no recoverable location, an absolute or `~/`
metadata pointer still works; a relative one remains unresolved. Missing,
ambiguous, or unknown-type declarations retain the ordinary transcript and a
visible unresolved activation, rather than selecting another schema silently.
YA should retain the resolved declaration and source identity with the turn so
replay uses what activated then, not the latest contents of a mutable skill file.

## Fixed visualization-type dispatch

The viewer dispatches on a fixed inventory of supported `type` values. The
initial inventory here contains **`tagged-stages/1`**. Adding another type is
an explicit contract/renderer addition; an unknown name does not request HTML,
JavaScript, or an inferred outline. A type may describe a different kind of
visualization, rather than another presentation of tag spans.

Assistant and tool activities can surface the same activation records, including
automatic skill-like use without a composer invocation. Record the originating
activity along with the containing turn; a later activity-specific visualization
type can use that anchor. The current tag type opens its identified workflow
within the turn. Highlighting, linear outlining, and later regrouping are views
of this type, not separate interpretations accidentally selected from prose.

## Declaration

`tagged-stages/1` is a predefined workflow schema type. A particular workflow
declares its schema ID, root key, stage tree, and whether tool output contains
tags. Keep the declaration beside the skill or procedure, as JSON or one
identified JSON block in its documentation. The same declaration is intended
for the agent and a viewer; no generated renderer code is required.

```json
{
  "type": "tagged-stages/1",
  "id": "example-publish/1",
  "key": "publish",
  "title": "Publish",
  "toolOutput": { "containsTags": false },
  "stages": [
    { "key": "verify", "title": "Verify source" },
    {
      "key": "client",
      "title": "Publish hosted client",
      "toolOutput": {
        "containsTags": true,
        "view": "spans",
        "whitelist": ["[build][types]", "[build][bundle]", "[copy]", "[push]"]
      },
      "children": [
        {
          "key": "build",
          "title": "Build client",
          "children": [
            { "key": "types", "title": "Check types" },
            { "key": "bundle", "title": "Build bundle" }
          ]
        },
        { "key": "copy", "title": "Copy assets" },
        { "key": "push", "title": "Push assets" }
      ]
    }
  ]
}
```

`type`, `id`, `key`, `title`, and `stages` are required. Each stage requires
`key`; `title`, `children`, and `toolOutput` are optional. A component such as
`[B]` uses the title declared at that path, or displays `B` when none is given.
Keys are nonempty, case-sensitive strings without brackets or newlines, unique
among siblings.
The full key path is the stable stage identity. Array order is display order,
not an execution schedule. A schema ID identifies an immutable revision of its
interpretation. The root key `workflow` is reserved for agent lifecycle lines.

The declaration describes possible stages. A single opaque script can implement
a parent whose children are not individually observable yet. Unobserved children
remain unobserved, rather than becoming fictitious progress.

## Prefixes, lifecycle, and grouping

Open a workflow in agent-authored commentary with a fresh instance ID and the
declared schema ID. Emit fixed stage prefixes when entering stages, and close
with an explicit result:

```text
[workflow][start] id=publish-7 schema=example-publish/1
[publish][verify] Check the source change.
...agent commentary, tool calls, and their results...
[publish][client] Run the hosted-client publisher.
...one tool invocation, possibly containing tagged substeps...
[workflow][end] id=publish-7 status=completed Published the selected targets.
```

Instance and schema IDs are whitespace-free tokens. The instance ID is scoped
to the calling session and current turn; native harness knowledge is optional.
Version one permits one open workflow per calling session turn. A later turn
needs a fresh explicit opening; matching IDs alone do not imply continuation.

The prefix is the maximal sequence of adjacent `[key]` components starting at
column one. `[A][B]` selects B within A; `[A][C]` selects B's sibling. `[A]`
returns to A itself. A space ends the path: `[A] [B] text` has path `[A]` and
body ` [B] text`. No space is required between the prefix and its body.
Each path selects its full outline position; there is no closing-tag stack or
`[/A]` syntax to balance.

The tagged line and subsequent activity belong to that path until the next
recognized prefix in the same producer stream, workflow end, or stream end.
Selecting a child retains its ancestor groups; selecting a sibling ends the
previous child segment. Repeating a path starts another segment of the same
stage. Grouping is a projection: preserve the chronological source transcript.
For the initial linear outline, `[A]`, `[B]`, `[A]` remains three segments;
stable path identity does not by itself move the second A beside the first.

Agent commentary recognizes the declared root/stage paths and lifecycle lines;
quoted examples and code fences are not emitted markers. Other bracketed gate
checks remain ordinary commentary. The tool-output matching rule below is
deliberately broader when no whitelist is given.

Advancing to another stage is not a claim that the previous stage succeeded.
Report results in ordinary text. Terminal `status` is `completed`, `blocked`,
or `failed`, with a concise outcome; a turn ending without closure leaves an
incomplete or interrupted workflow. Tags do not create approval checkpoints
or change the procedure's authorization or stop rules.

Use prefixes at meaningful boundaries. They accompany normal progress
commentary and require neither extra model turns nor separate process launches
for each stage.

## Tool-output matching

`toolOutput.containsTags` is a Boolean, defaulting to `false`. A stage may
replace the nearest ancestor's complete `toolOutput` policy; otherwise it
inherits that policy from the root. Capture the effective policy and active
stage when a tool invocation starts.

| Effective policy | What matches in that invocation's output |
| --- | --- |
| `containsTags: false` | Nothing; all output is ordinary content, even if it resembles a prefix. |
| `containsTags: true`, whitelist absent | Every syntactically valid start-of-line bracketed path, including undeclared keys. |
| `containsTags: true`, whitelist present | Only complete bracketed paths exactly listed in the whitelist. An empty list matches nothing. |

Whitelist entries are literal paths such as `[build][types]`; they are not
regular expressions or implicit subtree prefixes. Listing `[build]` does not
match `[build][types]`. Entries need not be declared stages. A nonmatching
prefix remains content in the current span. Validate the declaration's field
types and path syntax; do not silently ignore an invalid whitelist.

Matching examines tool-output lines directly. Without a whitelist, a line
beginning `[INFO]` or `[link](url)` also starts a span; surrounding log content
or a code fence does not suppress it. Choose a whitelist when those should
remain ordinary output. Leading whitespace prevents a column-one match.

## Tool substeps and concurrent activity

Tool paths are relative to the stage captured at invocation start. A publisher
launched under `[publish][client]` can emit `[build][types]` and then `[push]`;
these become `publish/client/build/types` and `publish/client/push` in the
outline, all within one tool invocation. Declared descendants supply titles.
An undeclared path creates observed child groups named by its component keys.

Each invocation has its own tag cursor, initially at its captured parent. Tool
tags refine that invocation's content; they do not move the agent's cursor.
Lifecycle-looking prefixes from a tool are also just relative child paths
when they match, never commands to open or close the calling workflow.

Separate invocations keep separate cursors. Late output from a background
command stays attached to the stage where that command started even after
the agent emits another prefix. The workflow's final result does not invent
successful outcomes for unfinished calls.

Tool-output parsing needs complete lines, source boundaries, and invocation
identity from the harness. A merged stdout/stderr stream may use its observed
order; independently delivered streams retain independent cursors. If those
boundaries are unavailable, retain ordinary output rather than guessing tool
substeps. The outer agent prefixes are still useful.

## Tool presentation

An enabled `toolOutput` policy may set `view`, defaulting to `spans`:

- **`matching-lines`:** the non-detail tool view shows only lines whose prefixes
  match the policy, using the path's title hierarchy and the text after its
  prefix. Other output stays available in the full detail view.
- **`spans`:** split the output at matching prefixes. Each tagged line and all
  following output up to the next match form an outline segment. Untagged
  output before the first match belongs directly to the captured parent.

Matching and presentation are independent: the same whitelist selects
boundaries in either view. A nonmatching tagged-looking line is omitted from
the first view's summary and retained in the current segment in the second.
Both retain the full original output in detail view. Neither interpretation
requires converting tool substeps into separate tool invocations.

## Visualization progression

- **V0, prototype/debugging:** after explicit schema activation, highlight
  matching prefixes or insert visual pseudo-boundaries within a turn or tool
  result. These are not new provider turns, commands, or messages.
- **V1, linear outline:** render titles and nested segments in source order,
  using the selected tool presentation. Repeated paths stay in their original
  positions.
- **Later, regrouped view:** collect all segments with the same full path under
  one outline node. A, B, A can appear as A containing both A segments, then B.
  Ordering groups by first appearance is one possible presentation; retain
  within-group chronology and source links, and keep the linear view available.

Regrouping is a distinct later projection, not a change to emitted paths or
the canonical transcript. It needs segment identities and their original
positions; reordering the underlying messages would lose that distinction.

## Adoption and verification

The procedure owns the work and the meaning of done. Its instructions name the
declaration, emit the opening and stage prefixes, and report intentionally
omitted stages. No stage is mandatory solely because it is declared. A
build-only or no-op path must not claim a push happened just because its command
returned zero.

For an existing opaque tool, declare possible children and leave `containsTags`
false. Enable it when that tool actually emits the convention; choose the
optional whitelist according to the matching table. Do not manufacture a child
timeline from an opaque final success line.

The minimum contract traces are:

| Input or condition | Required interpretation |
| --- | --- |
| Ordinary `[A]` before activation | No visualization is activated. |
| Enabled tool tags, no whitelist, `[new][B] detail` | Match the full path; undeclared keys create child groups, with `B` as title fallback. |
| Whitelist `[A]`, output `[A][B] detail` | No match: whitelisting a parent does not whitelist descendants. |
| Enabled tool tags with an empty whitelist | No tag lines match. |
| `[A]`, `[B]`, `[A]` | Three chronological segments in v1; a later regrouped view may collect both A segments. |
| Tool launched under A, agent advances to B, tool emits `[build]` | Tool content remains beneath A/build. |
| Publisher returns success after preparing only | Report preparation; do not claim publication completed. |

Before adopting a declaration, trace ordinary completion, partial/failure, and
concurrent or noisy output. Check path identity, whitelist presence versus
absence, terminal meaning, and retention of unmatched text. A future renderer
must fold the same source sequence identically live and after reload, including
recovering the declaration, opening, and active paths at a tail boundary.

Rich outcome snapshots, artifact viewers, dependency graphs, and cross-turn
interaction may use separate schema types or later extensions. They are not
prerequisites for these stage spans.
