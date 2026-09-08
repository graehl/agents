---
slug: acli-output-view-schema
noticed: 2026-09-08
where: topics/acli-spec.md, tool output producers, consuming renderers
---

**Status:** design gap recorded at the user's request. The vocabulary below
is illustrative, not an advertised capability or an implemented protocol.

**Gap:** consumers can recognize JSON and declared commentary, but lack a
portable description of how a tool's ordinary result fields should become
readable presentation. Inferring semantics from keys such as `stdout` or
writing a YA-specific renderer for each tool couples consumers to producers.

**Noticed while:** improving YA's presentation of agentctl output inside
workflow groups. Basic recognition of ACLI metadata, preservation of command
boundaries, and ordinary JSON/code rendering are separate work. This gap
captures the next layer, rather than making those basics depend on it.

**User-directed design:** each tool producing a kind of JSON or other output
would point to a schema its author co-developed with that output. Prefer a
mostly-declarative language mapping selected parts to Markdown-like content
or a limited HTML vocabulary, so any compatible consumer can render it.
Tool-produced, prerendered views attached as annotations are a possible later
alternative; they are not the initial direction.

**Fix sketch:** define an optional, versioned presentation protocol alongside
the [ACLI contract](../topics/acli-spec.md). Separate the input data schema
from presentation rules; a JSON Schema alone does not specify a view. A tool
announces the applicable schema reference and version with its output, scoped
to the relevant invocation, stream, record kind, or explicitly selected part.
The producer owns matching versions and examples as the output evolves.

An illustrative schema for a command result might look like this:

```json
{
  "language": "tool-output-view/1",
  "id": "example.command-result/1",
  "input": {"encoding": "json", "recordKind": "command_result"},
  "view": [
    {"element": "paragraph", "children": [
      {"literal": "Command: "},
      {"element": "inline-code", "value": {"pointer": "/command"}}
    ]},
    {"element": "code-block", "value": {"pointer": "/stdout"}},
    {"element": "paragraph", "children": [
      {"literal": "Exit code: "},
      {"element": "inline-code", "value": {"pointer": "/exit_code"}}
    ]}
  ]
}
```

The pointer syntax, element names, identifier, and announcement encoding are
unsettled. This example shows field selection and composition, not a proposal
to interpret every `stdout` string as prose or recursively parse it as JSON.
An explicit Markdown element could select an author-designated prose field;
ordinary strings remain escaped text or code. Later examples should cover a
table over an array, links, image captions and dimensions, optional fields,
and a declared non-JSON encoding with unambiguous record boundaries.

Before implementing, settle these externally testable contracts:

- A small, portable set of selectors, literals, composition, bounded
  repetition, and simple conditions; no arbitrary executable templates.
  Define missing fields, type mismatches, ordering, and rendering limits.
- Schema identity, versioning, discovery, availability during replay, and
  invocation/record scope. Unsupported, unavailable, or invalid schemas keep
  the normal JSON/code view and inspectable source; no guessed interpretation.
- Text escaping, the exact Markdown/HTML subset, link/media resolution, and
  host policy. A schema cannot introduce scripts or bypass consumer access
  controls. Equivalent semantics need not imply identical typography.
- Structured data, command boundaries, exit status, and provenance remain
  available. Render selected user-facing content as ordinary assistant-style
  presentation, visible in conversation view, with tool origin retained and
  source/schema details available on expansion. Do not require a second
  assistant message merely to repeat the rendered information.
- Define precedence and deduplication with existing `_acli.commentary` and
  [workflow tags](../topics/workflow-tags.md). Do not silently extend the
  current reserved metadata shape or make workflow grouping reinterpret data.

**Closure evidence:** a producer ships output plus its versioned schema and
fixtures; two independent consumers render the same selected content without
tool-specific code. Tests cover plain fallback, invalid/unknown schemas,
missing fields, hostile text, multiple records and commands, replay, and
commentary/workflow composition. Preserve the original result throughout.

**Related:** the durable baseline is [acli-spec](../topics/acli-spec.md).
This future protocol does not change v1.

2026-09-08 — Contributing-model: 6-Astra.
