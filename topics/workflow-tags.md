# Workflow tags

> Workflow tags are a reusable schema type in which bracketed key paths group
> subsequent agent activity and optionally tagged tool output into nested stages
> of an identified workflow.

Topic: `workflow-tags`

Status: Initial producer convention, 2026-09-07. The single `tagged-stages/1`
prototype is updated in place, including closed matching and collecting
presentation; these additions do not introduce another version. YA implements
the matching rules and validates the presentation fields; its collecting
renderer remains future work.
A skill or project instruction
opts into it; this topic does not require tags for ordinary work. Renderer and
harness support are separate capabilities. Read this topic when adopting or
changing a `tagged-stages/1` workflow. This is one visualization schema type;
activation is separate from its outline/tag interpretation.

## Explicit activation

Activation is one column-one line: the fixed marker, a space, and either a
schema path or an inline JSON whitelist.

```text
@@visualization-schema/1 ~/ya/topics/publish-workflow.local.md#ya-publish/1
@@visualization-schema/1 ["build","test","report"]
```

Trim surrounding whitespace after the marker's separating space. An operand
starting with `[` is the inline list below; otherwise the entire operand is the
schema path. No wrapper or following code fence is needed. This is unambiguous
because an absolute or `~/`-relative path cannot begin with `[`.
If later activation needs structure incompatible with that path, use a new
marker such as `@@viz-2`; keep the current marker's path interpretation intact.

The record must be surfaced in the current turn's agent output or a tool
result. Reading an opted-in skill can also activate through its metadata.
Having a schema file on disk, listing an installed skill, mentioning its name,
or seeing `[A]` in a log is insufficient.

For a file, the declaration's `type` selects the visualization contract and
`id` identifies the declaration. `tagged-stages/1` is the first predefined
type, not the meaning of every activation record. Other types may define different views
and update conventions. Unknown types remain readable data without activating
this tag parser. Conflicting declarations under the same schema ID are invalid.

Quoted or fenced examples are not activation. A producer can emit the line
directly or through skill/tool content. The file form supplies the schema ID
for an explicit workflow opening; the quick form opens its display span itself.
Do not repeat activation at every stage.
Activation lasts for the current turn and does not itself execute anything.

`toolOutput.containsTags`, `closed`, and the additive whitelist govern
stage-prefix recognition after activation. They do not govern the separate
activation record. Merely printing a bracketed lifecycle-looking path in tool
output is not activation.

## Quick inline whitelist

Use the inline list for quickly authored output that needs tag grouping but no
separate schema file. Each string is one literal key atom: `["build","test"]`
recognizes `[build]` and `[test]`. For an exact nested path, use an array entry:

```text
@@visualization-schema/1 ["build",["check","types"],"report"]
```

That recognizes `[build]`, `[check][types]`, and `[report]`. It does not
recognize `[build][other]`. Entries are exact paths, not regexes or implicit
descendant rules. Strings and nested path components obey the key syntax below;
path arrays must be nonempty. An empty outer list matches nothing. A malformed
list is an unresolved activation, never a filename or an unrestricted match.

The quick form selects a generic preset of `tagged-stages/1`:

- The list is the exact whitelist for both assistant prefixes and tool-output
  prefixes; there is no required root key or predeclared stage tree.
- Titles are the key atoms themselves. Paths use the current calling context;
  tool paths remain beneath their invocation's captured parent.
- Tool tags are enabled, with the `spans` view. Unmatched lines remain ordinary
  content under the preceding matched path; source/quote rules still apply.
- The activation source identifies the display span, which runs until the next
  activation or the turn boundary. No separate workflow ID, start marker, or
  terminal result is required, and stopping the span claims no task completion.

A quick activation emitted inside a tool result applies to that invocation's
following output and subsequent activity; earlier output is not reclassified.
Other already-started invocations retain their captured context and policy.
Use a schema file for custom titles, declared stage structure, different
tool policies, or an explicitly identified workflow with reported outcomes.

## Skill metadata and file resolution

The skill-content field is **`metadata.visualization-schema`**, a string in
`SKILL.md` YAML frontmatter. Its value remains a file pointer; the inline list
is an activation-text shorthand:

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
   invocation. Otherwise use the observed skill-read tool's source path. A skill
   name alone is insufficient; do not invent precedence by searching guessed
   skill directories.
2. Absolute paths refer to that host. Expand `~/` using that session owner's
   home directory, never the browser's home or a different YA host's home.
   Thus `~/agents/...` explicitly names the shared agents checkout; it is not
   an implicit search root.
3. Inside skill metadata, resolve a relative pointer against the directory of
   the resolved skill file, following symlinks to its actual source. An
   installed alias therefore keeps the source skill's adjacent resources.
4. The activation line's schema path must be absolute or `~/`-relative.
   Reject an unbased `path/to/schema` rather than guessing between project cwd,
   home, and `~/agents`. A displayed `[path/to/schema]` is not itself activation.
5. A schema pointer names a JSON declaration or a document containing fenced
   JSON declarations. A `#schema-id` fragment selects the exact
   declaration ID; without it, the document must contain exactly one declaration.
   For example, `~/ya/topics/publish-workflow.local.md#ya-publish/1` is explicit.
   Select declaration data; do not recursively follow activation lines in the file.

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

The schema is structured data. JSON is the initial concrete encoding. Compact,
token-efficient structured encodings may be added with a specified decoder for
the same data model; full YAML is not a schema format. Encoding changes that
still load from a path do not require changing the activation line. The YAML
frontmatter of an existing skill merely carries a string pointer to this data.

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
        "closed": true,
        "view": "spans"
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

In a full declaration, `type`, `id`, `key`, `title`, and `stages` are required.
The quick preset above supplies its own defaults. Each declared stage requires
`key`; `title`, `children`, `toolOutput`, and `presentation` are optional. The
root may also have `presentation`. A component such as
`[B]` uses the title declared at that path, or displays `B` when none is given.
Keys are nonempty, case-sensitive strings without brackets or newlines, unique
among siblings.
The full key path is the stable stage identity. Array order supplies the default
sibling order in a collecting view, not an execution schedule or a reason to
reorder linear history. A schema ID identifies the declaration's
interpretation; update the existing prototype declarations in place during
this initial convention change. The root key `workflow` is reserved for agent
lifecycle lines.

The declaration describes possible stages. A single opaque script can implement
a parent whose children are not individually observable yet. Unobserved children
remain unobserved, rather than becoming fictitious progress.

## Prefixes, lifecycle, and grouping

For a full declaration, open a workflow in agent-authored commentary with a
fresh instance ID and the declared schema ID. Emit stage prefixes, and close
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

With a full declaration, agent commentary recognizes the declared root/stage
paths and lifecycle lines; the quick form instead recognizes its inline list.
Quoted examples and code fences are not emitted markers. Other bracketed gate
checks remain ordinary commentary. The tool-output matching rule below is
deliberately broader when `closed` is false or omitted.

Advancing to another stage is not a claim that the previous stage succeeded.
Report results in ordinary text. Terminal `status` is `completed`, `blocked`,
or `failed`, with a concise outcome; a turn ending without closure leaves an
incomplete or interrupted workflow. Tags do not create approval checkpoints
or change the procedure's authorization or stop rules.

Use prefixes at meaningful boundaries. They accompany normal progress
commentary and require neither extra model turns nor separate process launches
for each stage.

## Tool-output matching

`toolOutput.containsTags` is the Boolean switch for parsing tool-output tags,
defaulting to `false`. `toolOutput.closed` is a Boolean, defaulting to `false`.
A stage may replace the nearest ancestor's complete `toolOutput` policy;
otherwise it inherits that policy from the root. Replacement is not a
field-by-field merge: omitted fields in a replacement take their defaults.
Capture the effective policy and active stage when a tool invocation starts.
Within a declared policy, explicit `false` and omission have the same meaning
for Boolean fields. Omitting the whole policy instead inherits it as above.

| Effective policy | What matches in that invocation's output |
| --- | --- |
| `containsTags: false` | Nothing; all output is ordinary content, even if it resembles a prefix. |
| `containsTags: true`, `closed: false` or omitted | Every syntactically valid start-of-line bracketed path, including undeclared keys, whether or not a whitelist is present. |
| `containsTags: true`, `closed: true` | Declared descendant paths of the captured calling stage, plus exact whitelist entries. With neither descendants nor whitelist entries, nothing matches. |

The whitelist is always additive; it never restricts declared descendants or
implicitly enables closed matching. An absent or empty whitelist adds nothing.
With open matching the accepted set is already unrestricted. Thus an enabled
policy with no children or whitelist is useful for arbitrary tagged output;
`closed: true` with no children gives whitelist-only matching.

Derive declared paths relative to the captured calling stage, including every
intermediate descendant. Children `build/types`, `build/bundle`, and `copy`
admit `[build]`, `[build][types]`, `[build][bundle]`, and `[copy]`. They do not
admit `[INFO]` or `[build][other]`. Adding `whitelist: ["[INFO]"]` admits
`[INFO]` without removing any of those declared paths.

Inheritance copies the policy, not a precomputed descendant set. A tool called
under `publish/client/build` with an inherited closed policy recognizes
`[types]` and `[bundle]`, not `[build][types]` or the sibling `[copy]`.
Whitelist entries are likewise interpreted relative to that invocation's
captured stage. Matching uses the complete prefix, never a shorter admitted
ancestor of an otherwise unrecognized path.

Whitelist entries are literal paths such as `[build][types]`; they are not
regular expressions or implicit subtree prefixes. Listing `[build]` does not
match `[build][types]`. Entries need not be declared stages. A nonmatching
prefix remains content in the current span. Closed matching controls tag
recognition; it does not delete unmatched source output. Validate the
declaration's field types and path syntax; do not silently ignore an invalid
whitelist.

Matching examines tool-output lines directly. With open matching, a line
beginning `[INFO]` or `[link](url)` also starts a span; surrounding log content
or a code fence does not suppress it. Choose `closed: true` when those should
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

Matching and presentation are independent: the same accepted path set selects
boundaries in either view. A nonmatching tagged-looking line is omitted from
the first view's summary and retained in the current segment in the second.
Both retain the full original output in detail view. Neither interpretation
requires converting tool substeps into separate tool invocations.

## Collecting presentation

These fields specify a collecting view when a renderer supports one; they do
not require that view to exist. Linear history always preserves source order.
A stage can request:

```json
{ "presentation": { "collect": true, "order": 10 } }
```

`collect` is a Boolean, defaulting to `false` (separate occurrences).
`order` is an optional finite number, defaulting to `0`. Validate both fields
when present. These settings apply to the declared stage itself and are not
inherited by children.
Undeclared paths and quick inline paths use the defaults.

In a collecting view, construct displayed parent groups from the root inward:

- `collect: true` gathers nonadjacent occurrences with the same full stage path
  under the same displayed parent, within one workflow instance and producer
  context. Assistant and tool streams do not merge. Each tool invocation and
  each independently delivered output stream retains its own context.
- `collect: false` keeps each occurrence as a distinct displayed instance.
  Children of separate parent instances cannot collect across those instances.
  If a parent collects, its children follow their own occurrence settings within
  the collected parent; tool invocation boundaries still apply.
- Order sibling groups and separate instances by ascending `order`, using `0`
  when omitted. Ties use declaration-array order. Explicit `0` and omission
  are identical; `-1` precedes default-order siblings and `1` follows them.
  Undeclared paths use `0`, after declared siblings with that same value and
  in first-appearance order among themselves. Repeated separate instances of
  one stage retain their relative source order.

The existing `stages` and `children` arrays are sufficient to specify default
display order. The optional numeric override lets an author change one stage's
position without moving its declaration or repeating sibling keys in another
list. Ordering is local to siblings; it never lifts a child out of its parent.
The root's `order` has no effect because a workflow has only one root.

For source `A1, B1, A2, B2`, with A collecting, B separate, and declaration
order A then B, display the A group containing A1 then A2, followed by separate
B1 and B2 instances. Giving B `order: -1` displays B1 and B2 before the A group.
This is a reversible view: retain source activity/segment identities, original
positions, and invocation ancestry. Preserve occurrence chronology inside a
collected stage; its child-group layout may use the sibling-order rules above.
Switching back to linear history restores `A1, B1, A2, B2` exactly, and neither
collection nor ordering changes tag matching or reports a new outcome.

## Visualization progression

- **V0, prototype/debugging:** after explicit schema activation, highlight
  matching prefixes or insert visual pseudo-boundaries within a turn or tool
  result. These are not new provider turns, commands, or messages.
- **V1, linear outline:** render titles and nested segments in source order,
  using the selected tool presentation. Repeated paths stay in their original
  positions.
- **Later, collecting view:** apply the occurrence and sibling-order settings
  above, retaining source links and keeping the linear view available. Only
  stages that opt into collection gather their repeated occurrences.

Regrouping is a distinct later projection, not a change to emitted paths or
the canonical transcript. It needs segment identities and their original
positions; reordering the underlying messages would lose that distinction.

## Authoring scripts and skills

When asked to give a script, skill, or informal procedure schema-governed
output, use this topic as the authoring contract:

Request wording such as **"Create/update X with schema-announced workflow
output"** routes here through `AGENTS.global.md` for skills, acli tools, and
agent-managed procedures. Add **"inline"** to select the quick whitelist form
without a schema file; the author chooses meaningful stage keys when none are
specified. Ordinary skill/tool creation does not automatically opt into this
protocol. The acli authoring topic also routes matching requests here.

For an inline skill or informal procedure, put an instruction like this in its
body, adapting the keys to the work:

```text
At workflow start, emit this line verbatim, outside a code fence:
@@visualization-schema/1 ["build","test","report"]
Prefix progress at each stage with [build], [test], or [report] at column one.
Following activity belongs to that stage until the next recognized prefix.
Report the actual result, including failures and intentionally skipped stages.
```

Do not put the inline list in `metadata.visualization-schema`; that field is
for file pointers. A fenced example in skill content is not activation: the
instruction above makes the agent emit the live line when executing the work.
An acli tool may instead emit activation and tags on its documented progress
stream; preserve [acli's structured result and error contracts](acli.md#schema-announced-workflow-output).
Wrapping an existing tool with caller-emitted markers needs no tool changes.

For either form:

1. For a quick case, emit the inline whitelist with meaningful key atoms. Use
   a separate declaration when titles, stage structure, or tool policy need
   more control. Keep encoding separate from the stage model; use JSON until
   another compact encoding has an explicit decoder contract.
2. Place prefixes at actual work boundaries. Full-schema agent paths include
   its root key; tool paths are relative to the calling stage. One script can emit
   all its substeps without becoming several invocations.
3. In a file declaration, set `containsTags` from actual tool output. Leave
   `closed` false or omitted to permit arbitrary bracketed paths. For mixed
   logs, use `closed: true` to admit declared descendants, leaving `[INFO]`
   ordinary unless explicitly added. Use `whitelist` only for extra exact
   paths; do not repeat declared children there. Whitelist entries are not
   patterns or implicit descendant rules.
4. In a file declaration, choose `matching-lines` to show only the
   selected progress lines, or `spans` when their intervening output belongs
   beneath each stage. Titles describe the work; they are not matching rules.
5. Wire activation through `metadata.visualization-schema` for a skill, or a
   one-line activation emitted by the caller or surfaced procedure content.
   With files, prefer a skill-relative pointer; otherwise emit the actual
   absolute or home-relative schema path. Include the full workflow's opening,
   stage reporting, and honest terminal result in the calling instructions.
   The quick form only needs activation and tagged output.
6. Check the emitted paths against the declaration and effective policy using
   the completion, failure/no-op, and noisy/concurrent traces below. Do not
   require YA rendering to be implemented before authoring usable output.

## Adoption and verification

The procedure owns the work and the meaning of done. Its instructions name the
declaration, emit the opening and stage prefixes, and report intentionally
omitted stages. No stage is mandatory solely because it is declared. A
build-only or no-op path must not claim a push happened just because its command
returned zero.

For an existing opaque tool, declare possible children and leave `containsTags`
false. Enable it when that tool actually emits the convention; choose `closed`
and any additive whitelist according to the matching table. Do not manufacture
a child timeline from an opaque final success line.

The minimum contract traces are:

| Input or condition | Required interpretation |
| --- | --- |
| Ordinary `[A]` before activation | No visualization is activated. |
| Inline `["A",["B","C"]]` | Match `[A]` and `[B][C]` in assistant/tool output; no schema file is read. |
| Inline `["A"]`, output `[A][B]` | No match: the inline atom permits only the exact one-component path. |
| A schema path whose filename contains brackets | Read the path normally; its absolute or home-relative prefix distinguishes it from a list. |
| Enabled open tool tags, no children, absent or empty whitelist, `[new][B] detail` | Match the full path; undeclared keys create child groups, with `B` as title fallback. |
| Enabled open tool tags, whitelist `[A]`, output `[B]` | Match: a whitelist never makes open matching restrictive. |
| Closed tool tags, child `build/types`, output `[build]` then `[build][types]` | Both match, including the intermediate declared path. |
| Same closed policy, output `[build][other]` or `[INFO]` | Neither matches; do not shorten the first prefix to `[build]`. |
| Same closed policy, whitelist `[INFO]` | Declared paths and `[INFO]` match; an empty whitelist still admits declared paths. |
| Closed tool tags, no children, whitelist `[A]`, output `[A][B] detail` | No match: an exact whitelist entry does not admit descendants. |
| Closed tool tags, no children, absent or empty whitelist | No tag lines match; original output remains available. |
| Closed policy inherited by a call under `build`, whose child is `types` | Match `[types]` relative to `build`; reject `[build][types]`. |
| Child replaces a closed enabled policy with `{ "containsTags": true }` | Open matching: replacement defaults `closed` to false and does not retain the ancestor's whitelist. |
| `containsTags: false` with children, `closed: true`, and a whitelist | No tool tags match; the explicit parsing switch is off. |
| `[A]`, `[B]`, `[A]` | Three chronological segments in linear history; collect both A segments only if A opts in and their parent/producer contexts agree. |
| `A1, B1, A2, B2`; A collects, B stays separate | Collect A1 then A2; keep B1 and B2 as distinct instances in sibling display order. |
| Same stages; B has `order: -1`, A has no explicit order | B1 and B2 precede the collected A group; source order inside each stage is preserved. |
| Equal order, including explicit `0` versus omission | Declared sibling order resolves ties; omission has the numeric value `0`. |
| Declared A at `order: 1`, undeclared X, declared B with omitted order | Display B, X, A: undeclared X uses `0` after declared zero-order siblings. |
| Repeated separate parent P, collecting child A | Each P occurrence retains its own A group; collection does not cross separate parents or tool invocations. |
| Collecting parent P, separate child A | P may gather its occurrences, but A occurrences remain distinct. |
| Switch from collecting view to linear history | Restore the exact original activity order and invocation ancestry. |
| Tool launched under A, agent advances to B, tool emits `[build]` | Tool content remains beneath A/build. |
| Publisher returns success after preparing only | Report preparation; do not claim publication completed. |

Before adopting a declaration, trace ordinary completion, partial/failure, and
concurrent or noisy output. Check path identity, open versus closed matching,
additive entries, terminal meaning, and retention of unmatched text. A future renderer
must fold the same source sequence identically live and after reload, including
recovering the declaration, opening, and active paths at a tail boundary.

Rich outcome snapshots, artifact viewers, dependency graphs, and cross-turn
interaction may use separate schema types or later extensions. They are not
prerequisites for these stage spans.
