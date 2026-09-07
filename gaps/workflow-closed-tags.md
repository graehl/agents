---
slug: workflow-closed-tags
noticed: 2026-09-07
where: topics/workflow-tags.md
---

**Gap:** The shared producer specification now defines `closed` and additive
whitelist matching, but YA's parser, examples, and tests still need migration.
The old consumer requires repeating declared child paths in a restrictive
whitelist; it must instead derive them from the captured calling stage.

**Noticed while:** Reviewing YA's workflow rendering and the shared
`tagged-stages/1` producer convention. The user requested this gap and suggested
`closed` as the option name. The user explicitly said backward compatibility
need not constrain this early convention change.

**Fix sketch:** Implement the settled matching and presentation-field contracts
in `topics/workflow-tags.md`. `toolOutput: { containsTags: true, closed: true }`
derives accepted paths from the captured stage's declared descendants and
adds exact whitelist entries. Keep the single existing prototype version.
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
Open/unset matching and whole-policy inheritance are now defined in the
specification. Keep the quick inline list's exact-path interpretation intact.

Update the producer specification, examples, affected skills/schemas, and YA's
parser contract/tests together when implementing. Test named descendants,
unknown prefixes, nested parents, inheritance, and additive whitelist entries
with closed matching enabled.
The shared specification changes the producer contract; YA runtime support is
not established by that documentation change.

## Collecting presentation

The user also requested optional schema presentation rules for a collecting
view, using **collecting** rather than coalescing: collection can bring
nonadjacent occurrences together and is not limited to adjacency.

- A tag can opt into collecting all of its occurrences into one displayed
  group. For example, `A, B, A` can present the two A occurrences together.
- The schema can specify the display order of those groups in a reordered or
  collecting view. `order` defaults to zero, with declaration order breaking
  ties; explicit zero and omission are identical.
- Other tags can require separate occurrences even in a collecting view.
  Repeated occurrences of such a tag remain distinct displayed instances;
  choosing the collecting view does not gather every tag indiscriminately.
- Linear history preserves source order regardless of these presentation
  options. Collection is a reversible view over the same identified source
  activities; it must not rewrite the transcript or lose invocation ancestry.

Follow the specification's grouping identity and parent/child behavior,
including placement of separate occurrences among collected groups. Preserve
occurrence order within a collected group.
Cover nonadjacent repeats, mixed collecting/separate tags, explicit group
order, nested stages, and switching back to linear history. The specification
now defines `presentation.collect` and optional `presentation.order`;
declaration arrays supply default sibling order. No collecting renderer is
implemented by this gap.

## 2026-09-07 status

Contributing-model: 6-Astra.

- Producer matching contract and examples: implemented in the accompanying commit.
  `closed` defaults false; whitelist entries never close matching themselves.
  Closed matching admits the union of declared descendants and exact extras;
  an empty union matches nothing. `containsTags` remains the parsing switch.
- Collecting presentation contract: defined, with `collect: false` and
  `order: 0` as defaults, declaration order breaking ties, parent/invocation
  identity, and reversible history.
- Evidence: contract-table traces cover open/empty and closed/empty matching,
  additive extras, nested inherited context, complete-prefix rejection,
  separate/collected parents, zero-order ties, and restoration of source order.
  These are specification traces, not YA runtime verification.
- Consumer migration: pending. YA session
  `01a07a0f-ac4b-77e0-b7c9-19c30122edea` owns the overlapping parser, tests,
  workflow topic, and publish declarations while publishing. Do not close this
  gap until the consumer update and focused integration checks are complete.
