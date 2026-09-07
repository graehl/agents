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
