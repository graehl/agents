---
slug: workflow-closed-tags
noticed: 2026-09-07
where: topics/workflow-tags.md
---

**Gap:** A declared workflow must repeat its child paths in
`toolOutput.whitelist` to recognize only those paths. Omitting the whitelist
currently recognizes every bracketed tool prefix, so declaring children does
not provide a concise way to close the accepted vocabulary. The publish
example exposes the duplication between `children` and its explicit list.

**Noticed while:** Reviewing YA's workflow rendering and the shared
`tagged-stages/1` producer convention. The user requested this gap and suggested
`closed` as the option name. The user explicitly said backward compatibility
need not constrain this early convention change.

**Fix sketch:** Define a concise option, with `closed` the preferred candidate,
that derives accepted tool-output paths from the current stage's declared
descendants. A possible spelling is `toolOutput: { containsTags: true,
closed: true }`; settle its inheritance/default behavior in the specification.
Avoid maintaining a generated duplicate whitelist.

For a calling stage with declared `build/types`, `build/bundle`, and `copy`,
closed matching should recognize the named relative paths, including the
intermediate `[build]`, and leave `[INFO]` and undeclared `[build][other]`
ordinary. Nested invocation context must still supply the parent path.

The user's settled direction is to keep `whitelist` and make it additive to
the declared descendants, including when `closed` is true. For example,
`closed: true, whitelist: ["[INFO]"]` admits every declared descendant plus
`[INFO]`. An empty whitelist adds nothing and does not remove declared paths.
Do not reinterpret the list as a subset restriction over declared children.
Define open/unset behavior and inherited policy explicitly. Keep the quick
inline list's exact-path interpretation clear.

Update the producer specification, examples, affected skills/schemas, and YA's
parser contract/tests together when implementing. Test named descendants,
unknown prefixes, nested parents, inheritance, and additive whitelist entries
with closed matching enabled.
This entry records the design work; it does not change today's matching rules.

## Collecting presentation

The user also requested optional schema presentation rules for a collecting
view, using **collecting** rather than coalescing: collection can bring
nonadjacent occurrences together and is not limited to adjacency.

- A tag can opt into collecting all of its occurrences into one displayed
  group. For example, `A, B, A` can present the two A occurrences together.
- The schema can specify the display order of those groups in a reordered or
  collecting view. Settle whether declaration order supplies the default and
  how explicit order interacts with hierarchy and unspecified tags.
- Other tags can require separate occurrences even in a collecting view.
  Repeated occurrences of such a tag remain distinct displayed instances;
  choosing the collecting view does not gather every tag indiscriminately.
- Linear history preserves source order regardless of these presentation
  options. Collection is a reversible view over the same identified source
  activities; it must not rewrite the transcript or lose invocation ancestry.

Define grouping identity and parent/child behavior, including how separate
occurrences are placed among collected groups. Preserve occurrence order
within a collected group unless the schema explicitly defines otherwise.
Cover nonadjacent repeats, mixed collecting/separate tags, explicit group
order, nested stages, and switching back to linear history. The field names
remain to be designed; no collecting renderer is implemented by this gap.
