# Research judgment and experimental diagnosis

> Rules and rationale for hypothesis communication, ambitious probes, strong cheap baselines, causal attribution, tie diagnosis, and closure tests.

Read this packet before judging an elaborate arm without a tuned cheap
baseline, attributing a surprising change after multiple differences, reading
a tie on a revision built for stated reasons, or parking a substantial weak
or surprising experiment line. `RESEARCH.md` is the router and wins on
conflict.

## Binding rules

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
uncertainty, not evidence. The formal additive model and worked diagnostics
appear below under the second “Attributing a surprising change across multiple
differences” heading.

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


## Retained detail and examples

### Research communication stance

**Hypothesis-mode communication**: When discussing experiments not yet
run, the user states hypotheses bald, without "probably" / "might" /
"need to test" framing — the unrun status is shared common ground.
Translate, don't restate: when recording such a claim (paper, log,
task file), render it as a hypothesis ("we expect X", "X would imply
Y"); the translation IS the hedge. Skip "needs testing" / "we haven't
measured this yet" replies — they only restate shared ground.

What this rule does NOT suppress: substantive disagreement. If
existing evidence or background knowledge makes the hypothesis
probably wrong (contradicts a known result, fails a quick check
against published findings, conflicts with data already in front of
you), say so promptly — do not meekly record the claim as a
hypothesis to test. The distinction: "needs testing" replies waste
time on shared common ground; "probably wrong because X" is the
pushback the user wants immediately.

**Truth over momentum**: In research, the desired output is what
actually works or is actually true — including null results,
falsified hypotheses, and "doesn't work" findings. Those are
successful experiments, not setbacks to spin. Reserve language like
"promising" / "encouraging" / "on the right track" for cases where
the evidence supports it, not for cases where the user has invested
recent effort and would feel rewarded by it. Report what is, not
what would feel like progress.

**Favor ambition**: Prefer experiments that resolve live uncertainty
over experiments that confirm what we are already nearly sure of. A
run with a known-likely outcome wastes compute and time; design
probes that could plausibly surprise, that distinguish between
competing hypotheses, or that move the frontier of what is known.
"Let's first verify X" is the wrong default when X is already well
established — skip the redundant confirmation and aim higher.


### Build the strongest cheap baseline early

In every experiment arm, build and tune the strongest cheap/simple baseline
*before* judging an elaborate approach — not as a checkbox row but as the
first real effort. The search pays out two ways regardless of how the arm
breaks, so a "we lost to baseline" result is information, not a setback:

- The baseline may simply be the win — a cheap, reliable technique that
  already matches or beats the elaborate method is worth shipping precisely
  because it is cheap and reliable, and it advances the deployable curve now
  while the fancy method is still speculative.
- A strong baseline debugs the elaborate method. If you only compare against
  a *weak* baseline you mis-read a small positive delta as success and never
  diagnose. A strong one forces the diagnosis and names the fix: "losing to
  baseline → need more data," or "→ need at least the smoothing/regular-
  ization that lets us match baseline before any added mechanism can show
  through."

Recurring corollary: across arms, a cheap calibrated/external component
(a selector, a fixed routing recipe, a direct first pass) often beats a
cleverer model-internal mechanism at deployable scale. Expect it; do not
treat each instance as a surprise.

Triage guardrail when this becomes a named theme in a report or paper:
over-claiming a unifying theme is harmless *only as long as it does not
color per-thread triage*. Triage each arm on its own cost and likelihood;
a repeated theme is a story for the reader, not extra evidence, and earns
an arm no triage weight.

### Attributing a surprising change across multiple differences

When a surprising (usually bad) result follows a departure from baseline that
changed several things at once and you have no one-at-a-time ablation: first
resort is to **just run the one-thing-at-a-time ablation, or a progression from
baseline** — if the runs are cheap or the effect is large enough to measure
quickly, do not spend tokens reasoning about attribution you could cheaply
measure. The rest of this applies only when the controls are expensive enough
that careful between-run thought earns its tokens. There, "underperformance
usually has one main cause" is a useful *prior for where to probe first* — not a
conclusion; it is Bayes-valid only under two structural conditions, so step away
from it when either cracks:

- separability — the causes' effects on the metric are ~additive (no
  interaction): `delta = delta_A + delta_B + delta_AB` with `delta_AB ~ 0`.
- skew — effect sizes are unequal, so one term usually dominates.

Distrust the single-cause story when any of these hold (signature in parens):

- Interaction / synergy — metric moves only with both present, AND-gate; neither
  alone is "the" cause (joint != sum of singles).
- Saturation — a cause near a floor/ceiling caps and hides another's real
  marginal effect until it is relieved (metric pinned at an extreme).
- Comparable magnitudes or many simultaneous changes — no reason one dwarfs the
  rest; with many similar-scope changes a lone dominator is unlikely (order
  statistics).
- Sign cancellation — one change helps while another hurts, so the net
  understates two large opposing effects; "one main cause of the net" is then a
  category error (net smaller than the changes' scope implies).
- Regime dependence — a cause helps in one slice and hurts in another; the
  aggregate is a blend with no context-free main cause (subgroup numbers
  disagree).

Scope note: a *limiting factor / binding constraint* (one stage binds, so
changing others does nothing) is deliberately absent — it explains a *missing*
expected difference (the dual problem), and when it does yield an observed one
the per-cause harms are usually additive, so it is not a separability failure
here.

Operational rule: use the prior to aim the *first* control (one leave-one-out,
or add-one-to-baseline, for the suspected dominant cause), then let the residual
adjudicate. If that cause explains most of the gap, the prior earned it; if a
large residual remains — or the residual flips sign — finish the factorial
before attributing. Two binary factors are four cells; additivity lets three
determine the fourth, but a confounded pair (baseline + full departure only)
never identifies the parts, however separable the truth is. One clean
leave-one-out earns its keep even when the observed gap looks modest: checking A
alone can reveal B is opposite-signed — a help masking a larger hurt — which the
net hid.

Two discipline riders. Keep straight *what* you are attributing: one cause can be
the main driver of the harmful component while the net is a two-effect story (a
help plus a larger hurt) — "usually one cause" can be true for one and false for
the other. And until the deciding cell is run, treat any interaction as an open
question, not a risk: an imagined failure mode is not evidence, and uncertainty
about an untested interaction is symmetric.


**Research-line closure before moving on**:
- After a substantial experiment line produces a surprising or weakly-positive signal, do
  not immediately jump to the next high-level research-plan item. First exhaust the
  reasonable closure tests that explain whether the previous investment paid off, failed
  for a code/configuration reason, or only beat an insufficient baseline.
- For combination-only gains, compare against embarrassing null baselines with the same
  decode/selection budget, such as random same-norm adapter perturbations or random
  one-step experts. A learned adapter that cannot improve on its own only earns credit in
  a blend or system-combination result if it beats those random-direction controls across
  enough seeds or validation-selected candidates.
- Treat this closure work as part of the result, not a detour: record the null baselines,
  bug checks, and plausible failure explanations before declaring the line exhausted or
  moving to the next paper-level project.

**Post-run option audit**:
- When post-run analysis of logs raises a possible mishap, inefficiency, anomaly, or
  suboptimal behavior, grep the relevant tool's `--help` output for the symptom terms
  and nearby concepts before assuming the behavior is fixed. The log does not need to
  show an outright bug; terms such as "reload", "sync", "batch", "patience",
  "checkpoint", "cache", "offload", "wrap", "timeout", or "floor" may indicate an
  existing controllable knob.
- Use context-aware searches over help text so the matched option and its neighboring
  descriptions are visible. Prefer an agent-friendly non-wrapped help mode when
  available because it saves tokens and avoids follow-up wider-context reads to
  reconstruct wrapped option descriptions.
- Summaries should name any relevant existing options and recommend the smallest
  follow-up run or setting change that would distinguish "tool limitation" from
  "unexamined option/configuration".

### Reading a tie on a motivated revision

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

**Worked instance.** Entity surface-form substitution for tagger training:
synthetic entity strings from the Faker library, the incumbent, were
known-defective for specific (language, tag) types; a character-level name
generator trained on scarce gold/gazetteer data was proposed as the
substitution source. Brief training runs scored +0.0001 F1, not
significant. The predicted slice — the known-defective (language, tag)
pairs — was a small share of evaluation weight, so the aggregate tie was
expected even under success; the informative tests are the sliced
comparison with eval N bought there, and on a win, the substitution source
routed by (language, tag) with the incumbent elsewhere, measured by
training.
