# Research judgment and experimental diagnosis

> Rules and rationale for hypothesis communication, ambitious probes, strong cheap baselines, causal attribution, tie diagnosis, and closure tests.

Read this packet before judging an elaborate arm without a tuned cheap
baseline, attributing a surprising change after multiple differences, reading
a tie on a revision built for stated reasons, or parking a substantial weak
or surprising experiment line. `RESEARCH.md` is the router and wins on
conflict.

## Binding rules

Research communication stance applies throughout this packet's work. Read the
named baseline, attribution, tie, closure, or option-audit section for that
decision; Tie diagnostics supplements Reading a tie on a motivated revision.

### Research communication stance

When the user states an unrun hypothesis baldly, record it as a hypothesis
(“we expect X”); do not waste a reply restating that it needs testing. Push back
promptly when evidence makes it probably wrong.

Truth outranks momentum: null results, falsification, and “does not work” are
successful outcomes. Use positive affect only when evidence supports it.
Prefer ambitious probes that resolve live uncertainty or distinguish competing
hypotheses over redundant confirmation of well-established expectations.


### Build the strongest cheap baseline early

Build and tune the strongest cheap/simple baseline before judging an elaborate
arm. A cheap method that wins is a result; a strong baseline also diagnoses
what the elaborate method must fix. Judge each arm independently rather than
giving a recurring cross-arm story extra triage weight.

### Attributing a surprising change across multiple differences

When several changes precede a surprising result, run one-at-a-time or
baseline-progression ablations when cheap. If controls are expensive, a
single-dominant-cause hypothesis is only a first-probe prior and requires
approximately separable, skewed effects. Distrust it under interaction,
saturation, comparable effects/many changes, sign cancellation, or
slice-dependent regimes.

Aim the first leave-one-out/add-one control at the suspected dominant cause,
then use the residual. A large or sign-flipped residual requires the remaining
factorial cells before attribution. Distinguish the main harmful component from
the net of helpful and harmful effects; an unrun interaction remains
uncertainty, not evidence. For two binary factors, the model is
`delta = delta_A + delta_B + delta_AB`: baseline plus the full departure
cannot identify the separate effects, even when the truth is additive.

### Reading a tie on a motivated revision

A tie does not establish "no change justified" for a revision built for
stated reasons. When proposing the revision, record where those reasons
predict improvement:
a slice plus the variable that identifies it at application time (the
routing key), or an expected aggregate magnitude. Do the power arithmetic
up front: predicted slice mass (its share of evaluation weight) × expected
local effect against the eval's detection floor says in advance whether an
aggregate tie would be uninformative or would already imply harm elsewhere.
On a tie, run one bounded diagnosis pass, cheapest check first: inspect the
intermediate artifact the reasons claim improved (blinded when judging
quality by hand); then test the frozen predicted slice at adequate power,
buying eval N on that slice or pre-registering a metric that keeps the
slice visible (for example, macro-averaged over strata). A null on the
predicted slice closes the line; do not search
further contexts for a win. On a verified slice win, prefer routing the
revision selectively by the pre-named key with the incumbent elsewhere,
measured end-to-end, over wholesale accept or discard. Tie plus significant
added expense — compute, complexity, future attribution burden — is a valid
reason to stop without the pass. The pass delivers a diagnosis; the default
disposition at tie stays don't-land unless the revision also wins on cost.

### Research-line closure

Before parking a substantial weak or surprising line, perform the run/row/log
checks in `_RESEARCH/evidence.md` § Read the failure before reporting it,
tune the strongest cheap baseline, and distinguish a code/configuration failure
from a failed research hypothesis. For combination-only gains, compare
same-budget null controls, such as random same-norm perturbations, across
enough seeds or validation-selected candidates to support the claim. Record
these checks and remaining explanations before moving to another line.

### Post-run option audit

When logs suggest a mishap, inefficiency, anomaly, or suboptimal behavior,
search current `--help` for symptom terms and nearby concepts. Read neighboring
option descriptions; prefer unwrapped help when available. Name any relevant
option and the smallest follow-up that distinguishes a tool limit from an
unexamined configuration. An outright bug is not required to trigger the audit.

### Tie diagnostics

**The tie identity.** With `m` the predicted slice's share of evaluation
weight, an aggregate tie constrains a mass-weighted sum:
`0 ≈ m·Δ_slice + (1−m)·Δ_complement`, so a verified slice win fixes the
implied complement effect at `−(m/(1−m))·Δ_slice`. Small slice mass: the
implied harm sits below the detection floor — the tie is consistent with
"helps there, clean elsewhere" (dilution), but implied-small is not
known-zero, so check the complement rather than assume it. Substantial mass:
the arithmetic forces real harm elsewhere (a focused win offsetting a
common-case loss); locate it before deciding. Selective routing is the
preferred disposition under either anatomy, which is why it beats
accept-or-discard: the routed hybrid — revision on its predicted slice,
incumbent elsewhere — is correct whether the tie was dilution or
cancellation. The up-front power arithmetic tells you before the run which
reading a tie would carry. Significance mechanics for the sliced comparison
follow `_RESEARCH/evidence.md`.

**Freeze the predicted slice.** The recorded prediction is the license for
the sliced test. If the slice is widened after seeing sliced results, the
pre-registration dissolves retroactively; additions discovered during eval
inspection are hypotheses for the next cycle, not members of this
comparison.

**Inspect the artifact claim first.** The revision's case decomposes into
two claims: the artifact it produces is genuinely better where the reasons
say, and that better artifact moves the end metric downstream. The first
costs no compute to check — directly inspect the artifact in the predicted
slice, judging both per-example quality and distributional properties
(coverage, diversity, skew) against a reference independent of the
incumbent. Inspecting examples one at a time cannot reveal what an artifact
is missing: when the producing pipeline anywhere depends on the incumbent —
for example, data selected by a model trained under the incumbent's
defect — the artifact systematically lacks the very cases the revision is
meant to fix, while every retained example still looks good. If the
artifact is not actually better there, discard the revision immediately:
the stated reason was factually wrong. If it holds up while the predicted
slice nulls at adequate power, the downstream claim is falsified — a
transferable negative that settles the value of an entire family of future
investments in that mechanism. That prospective value, not invested cost, is what
justifies the pass; the decision must stay insensitive to sunk compute.

**Symmetry and proposer neutrality.** Any tie contradicting a confident
prediction earns the pass, whichever outcome was hoped — digging only into
ties on favored revisions turns the rule into a prior-amplifier. The bar is the
specificity of the recorded prediction, not who proposed the revision;
user- and agent-originated ideas meet the same test.
