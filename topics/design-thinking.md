# Design thinking

> How to approach a change before and during implementation — independent of language or domain.

Topic: design-thinking

For how these show up in the code itself, see [software-aesthetic.md](software-aesthetic.md) and [software-aesthetic.coordinated.md](software-aesthetic.coordinated.md).

## Reframe before patching

Repair the model of the problem rather than force the output. Before you add a special case, name the invariant it protects and ask whether a different representation removes the need for it entirely. A run of "if this input, force that output" clauses is a design smell unless each branch follows from a stated domain rule. The same test gates every new concept or abstraction: name the problem it solves and the invariant it holds, then check whether a simpler representation makes it unnecessary.

This is a *deleting reframe* — a reframing that preserves behavior while deleting whole branches, layers, or concepts. The aim is to make the change look inevitable in hindsight, not to polish the structure already there.

## Map before drilling

Entering an unfamiliar area, build the high-level map first — the modules, callers, and invariants that matter, named in the project's vocabulary — before opening any single function. Skipping the map is how you patch a function while missing the three callers that depended on the old behavior, or reimplement something that already exists one module over. On re-entry, refresh the map before drilling again.

## Sweep callers when a contract moves

When a change moves a shared facility's contract — signature, semantics,
errors, performance — every call site is in scope, not only those in the
diff. Sweep the callers and confirm each one's assumptions still hold, or
update it; the duty is heaviest where the facility sits at a boundary many
callers cross and no test battery catches the ripples. The same holds for
prose: a doc section that other docs cite or a read-trigger points at is a
shared facility, and compressing or moving it obliges checking, block by
block, that every pointer still lands on the content it promises.

## Weigh alternatives where effects are distant

Lay out 2–3 real alternatives — and record the choice — when a decision's
effects reach beyond the local edit: a contract callers cross, a persisted or
wire format, a choice that constrains work not yet written, or one that is hard
to undo. A surface reviewer reads the local diff and so inherently misses
effects at distance; the recorded decision is the only channel that carries
them to a reader the diff cannot reach, which is why the record matters as much
as the choice itself.

For such a fork, name what each alternative trades off *before* picking. If the
work is significant and the fork is live, surface them as an interruptible
checkpoint — the recommended pick in **bold**, its reason inline, no tacked-on
invitation to override (the checkpoint is interruptible by nature); otherwise
decide internally. Either way, record the outcome as a `## Design decisions`
bullet in the relevant topic doc (or the commit body when no topic doc fits):
`**<decision>** (vs. <rejected alternative>): <rationale>`, naming the trade-off
accepted and the priorities the chosen path serves.

Lean toward firing this, not against it. When unsure whether an effect is
local, treat it as distant: a three-line record that turns out unnecessary
costs little, whereas a missed distant effect is exactly what surface review
cannot recover. Only a purely local, cheaply reversible decision needs none of
it — there Scope discipline governs: pick and move.

## Hypotheses over traces

Treat every assumption as a hypothesis until you check it. Form one that fits the known invariants, then test it against the trace — not the reverse. Replaying the trace with no hypothesis in hand produces patches, not understanding.

## Scope discipline

Build for the problem in front of you, not a hypothetical future. A bug fix needs no surrounding cleanup; a one-shot needs no helper. Add no feature, refactor, or abstraction the task did not ask for.

One reconciliation with the strict-review bar (harsh-review demands restructuring that scope discipline forbids volunteering): when your change already opens the relevant *seam*, the restructure is cheap and in scope — do it now. Otherwise stay minimal and surface the restructure as a recommendation rather than doing it unasked.

One regime inverts the "no unasked-for flourish" default: a **brand surface** (landing/marketing/launch content) where being memorable *is* the requirement, so committing to a distinctive aesthetic direction is in scope rather than scope creep. See the functional ↔ distinctive split in [ui-quality.md](ui-quality.md) §1; it does not license skipping the verification thresholds.
