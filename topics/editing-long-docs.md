# Editing long documents

> A long document may be decomposed into a directory of section files as a
> temporary loss-resistant editing representation or as the canonical linked
> form behind a short table-of-contents router.

Topic: `editing-long-docs`

Agents sometimes propose or choose this representation without being told; it
is a normal editing tactic, not a ceremony every long document must follow.
Use it when independent section reads, regrouping, or reliable movement matter
more than preserving one physical file during the edit.

## Two valid lifecycles

**Temporary workspace.** Split the source into section files, regroup and edit
there, then compose the approved final order back into one document. The
directory is scaffolding and may be removed only after the composed document
has been checked for coverage and its references have been updated.

**Canonical catalog.** Keep a short table-of-contents or routing document and
make the linked section files the official sources. This is useful when readers
normally need only one concern, packet sizes should stay bounded, or different
sections have distinct activation conditions. Do not also maintain a stitched
copy as a second source of truth.

The choice is semantic rather than cosmetic: temporary section files optimize
an edit and disappear; a canonical catalog defines how future readers retrieve
the document.

## Scatter, rank, condition-group, place

Use this sequence when a long source needs more than a mechanical split:

1. **Scatter:** inventory the source at section or rule granularity and copy
   each unit without semantic rewriting. Retain its source heading and a
   source-to-destination mapping until coverage is proven.
2. **Rank:** assess each unit's behavioral value, cost if missed, activation
   frequency, and likelihood that an agent will recognize its condition. Mark
   stale, conflicting, duplicated, and merely explanatory units separately.
3. **Condition-group:** cluster retained units by a shared observable
   pre-action cue. Conceptual similarity, equal packet size, and equal group
   importance are secondary; a packet succeeds when a realistic action loads
   the applicable rules without much unrelated text.
4. **Place:** make each cluster a canonical section file, put its cue and link
   in the nearest router that will reliably be in context, and promote narrow
   high-value routes to a compaction-protected main document when warranted.
5. **Validate:** trace representative requests from cue to rule, measure every
   independent read, verify the source inventory, and only then consolidate
   duplicates or remove the old representation.

The scatter may be temporary even when the resulting section directory is
permanent. This ordering lets content move more than once without making each
move a simultaneous rewrite and deletion.

## Preserve before consolidating

Make relocation and cleanup separately reviewable:

1. Inventory every source heading and map it to a destination file and heading.
2. Move content faithfully before deduplicating, reconciling, or shortening it.
3. Preserve heading hierarchy, examples, code fences, links, and precedence
   statements; adjust heading levels only for the new container structure.
4. Check that every source section is represented, intentionally superseded,
   or explicitly proposed for deletion.
5. Update inbound links and routers after the destination layout is stable.
6. Delete the old representation only after the new one is readable and
   recoverable in version control.

This staging lets sections move repeatedly without depending on a sequence of
large single-file rewrites and makes accidental content loss visible.

## Routing and reachability

Physical separation does not make a rule reachable. A canonical catalog maps
an observable condition to the exact file or named section that governs the
next action. Prefer cues an agent encounters before acting—creating a public
research result, launching a long job, entering a foreground wait—over
aspirational directions such as “read this when more detail is needed.”

When no plausible cue reaches an instruction, keep the decision surface in an
already-loaded main document, merge it into a packet with a reachable trigger,
or remove/reclassify it as nonbinding rationale. High-value rules with narrow,
observable conditions may warrant a route in a compaction-protected main file
even when their details remain in a section packet.

## Read-size budget

Keep each independently read section file comfortably below the smallest
measured complete-result budget of its intended harnesses, including command
wrappers and neighboring output. A directory split can lower both the largest
single read and total reading in realistic tasks, but only when its activation
routes avoid loading unrelated packets. Harness-specific ceilings and their
remeasurement cadence belong in the applicable harness supplement and evidence
ledger rather than in this general editing pattern.
