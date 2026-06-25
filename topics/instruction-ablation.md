# Topic: instruction-ablation

> Turning "does this instruction change help?" into a measurement: a
> paired SWE-bench-style ablation that varies only the instruction
> corpus, run inside a network-off, directory-scoped per-instance
> sandbox (no OS-level isolation required for a supervised workflow),
> with contamination and confound controls strong enough that a
> few-point effect is trustworthy.

Topic: `instruction-ablation`

This is the concrete realization of the validation plan that
[`agent-instructions.md`](agent-instructions.md) defers ("Limits of
these methods", and the 2026-05-29 entry in
[`agent-instructions.evidence.md`](agent-instructions.evidence.md)):
every rule in this corpus is currently a hypothesis justified by
introspection, not an outcome comparison. This doc says how to run the
comparison when it is worth the compute — and, just as importantly, how
not to fool ourselves while doing it.

It is a **proposal**: as of writing, no instruction ablation has been
run here. Treat the numbers and power estimates below as design
targets, not results. <!-- assumed -->

## Why this is hard, not just expensive

The effect we are chasing is small. SWE-agent's interface ablation —
swapping a tailored agent-computer interface for a bare shell, same
model — moved SWE-bench resolution by 10.7 pp (Yang, Jimenez et al.,
NeurIPS 2024). A single *wording* change to one rule will move far
less. Mizrahi et al. (TACL 2024) show instruction paraphrases shift
both absolute and relative model rankings across millions of instances.

So the binding constraint is not "can we run SWE-bench" — the harness is
public and Dockerized — it is **noise and confounds large enough to
swamp the signal**. Most of this doc is therefore about measurement
discipline, not plumbing. A sloppy run that reports "+3 pp, instructions
help!" from a single 50-instance pass with the network on is worse than
no run: it manufactures false confidence in exactly the inert-ritual way
the evidence ledger warns against.

## What SWE-bench gives you (and what it does not)

Each SWE-bench instance is a real GitHub issue: a repo pinned at a
`base_commit`, a `problem_statement` (the issue text), a hidden
`test_patch` (the tests the fixing PR added/changed), and a `gold_patch`
(the human fix). The agent sees the repo and the problem statement,
produces a candidate patch; the harness applies it at `base_commit` and
grades:

- **FAIL_TO_PASS** — tests that failed before the fix must now pass.
- **PASS_TO_PASS** — tests that passed before must still pass (no
  regression).

`resolved = all FAIL_TO_PASS pass AND all PASS_TO_PASS stay passing`.
This binary, per-instance, deterministic outcome is what makes a *paired*
comparison possible — the same instance under instruction-set A and B is
a matched pair.

Variants worth knowing: **Lite** (300 instances, cheap pilots),
**Verified** (500 human-validated — the default for any claim, fewer
broken instances), **Multimodal**, and **SWE-bench-Live** (fresh issues,
post-cutoff, for contamination resistance). The harness already ships
per-instance Docker images that pin each repo's exact dependency
snapshot — that is the *environment reproducibility* half of "chroot or
VM" solved for free. The half it does **not** solve is containing a
freely-executing agent, which is where the isolation design actually
matters.

## Isolation: directory-scoped permissions, not OS-level security

For a mostly-supervised in-house workflow the requirement is modest, and
worth stating plainly so nobody over-builds: **a harness that reliably
confines a subagent to a working directory's permissions, plus no
network, is enough.** OS-level security — a kernel boundary, a VM — is
*not* demanded here. The agent is our own trusted frontier model under
human supervision; the threat is the agent accidentally reaching the
answer or scribbling on the host, not a malicious breakout.

So "chroot or VM" overshoots in both directions. A bare `chroot(2)` is
not actually a security boundary (root escapes it, and it isolates
neither network nor mounts), and a VM is more isolation than a supervised
ablation needs. The mechanism that actually fits is **subagent
permissions scoped to a throwaway per-instance work dir**, which most
agent harnesses already provide. Two properties are what matter:

- **Network off at solve time.** The single most important knob: with no
  internet the agent cannot fetch the linked PR, the fixing commit, a
  newer already-fixed package version, or a web answer. Enable the
  network only for image/dependency setup, then drop it before the agent
  starts solving.
- **Writes confined to a fresh per-instance work dir.** Each instance
  starts from a clean checkout at `base_commit`; the agent can only write
  inside its sandbox dir; nothing bleeds between instances or onto the
  host. A read-only repo mount plus a writable overlay is the usual shape,
  but plain dir-scoped permissions on a per-instance copy are equally
  fine.

The SWE-bench harness already runs each instance in a per-instance
container, so in practice you get this by reusing its containers with
`--network none` — but the *requirement* is the two properties above, not
containerization specifically. Any confinement that delivers them
(harness permission scoping, `bubblewrap`/`nsjail`, a container) is
acceptable.

**When a hard boundary would matter (out of scope here).** A real kernel
boundary — gVisor → Firecracker microVM → QEMU/KVM, lightest first —
becomes relevant only if the model or the code it runs is *untrusted*
(adversarial eval, an unknown open-weights model, prompt-injection
research), or you need per-instance snapshot/rollback or kernel-level
reproducibility. None of that applies to validating our own corpus, so
do not pay its cost (slower startup, more ops) — it buys isolation this
workflow does not need and slows the sweep that statistical power demands.

## Contamination invariants

These are the conditions that make a measured delta mean what it says.
Violate one and the run is void, not merely noisy.

- **No network at solve time** (Tier-1 knob above). Non-negotiable.
- **The agent never sees `test_patch` before it patches.** The harness
  applies FAIL_TO_PASS/PASS_TO_PASS tests only at grading time — but a
  free agent with filesystem access will `grep` for them if they are
  mounted. Keep the test patch out of the solve container; inject it only
  in the grading step.
- **Strip post-`base_commit` history.** `git log`/`git show` of future
  commits, tags, or branches can leak the fix. Hand the agent a shallow
  checkout at `base_commit` with no remotes, or a non-git snapshot.
- **Model cutoff vs. issue date.** A model trained after the issue was
  fixed may have memorized the PR. Prefer **Verified** (human-checked)
  and **SWE-bench-Live** (post-cutoff issues) for any headline claim, and
  record `model_version × benchmark_date` so the contamination risk is
  auditable rather than assumed away.

## Experiment design: vary one thing

The whole point is a clean contrast, so hold everything fixed except the
instruction corpus.

The contrast runs two directions, and the inward one is the cheaper win.
*Gating* asks whether a proposed addition earns its tokens (Arm A = with
it, Arm B = without). *Culling* runs leave-one-out over rules already in
the corpus to find the inert ones to delete — the check that pasting a
rule in because it sounded convincing never performs on itself. Culling
needs no new rule to justify it and targets the rules most suspected of
being ritual, so it is usually where the first real sweep belongs.

- **Paired arms.** Arm A = corpus *with* the change (e.g. the new topic
  doc loaded), Arm B = corpus *without*. Same model, same scaffold, same
  instance set, same decoding params. Because the outcome is paired
  binary per instance, test the difference with **McNemar's test** on the
  discordant pairs (instances one arm solves and the other does not) —
  not an unpaired proportion test, which throws away the pairing and
  loses power.
- **Hold the scaffold fixed.** Only instruction *text* varies. Same tool
  set, same agent loop, same `max_steps`. If the changed instructions are
  longer, they consume context/token budget the other arm keeps — a real
  confound; either equalize the budget or report token usage alongside
  resolution so the reader sees the trade.
- **Pin the model version.** Model drift across dates silently invalidates
  cross-time comparisons; run both arms on the same pinned model in the
  same window.
- **Sweep paraphrases, don't conclude from one wording.** Following
  Mizrahi et al.: express the changed rule ≥3 ways and report the spread.
  A change that helps under one phrasing and hurts under another has not
  been validated — it has been gambled on.
- **Power.** With a binary outcome and a true effect of a few points,
  300 paired instances (Lite) gives marginal power; **Verified (500)** or
  bootstrap CIs over instances is the floor for a headline number. Report
  a **confidence interval**, never a bare point delta — a "+3 pp" with a
  [−4, +10] CI is a null result honestly stated.
- **Flakiness.** Some PASS_TO_PASS tests are nondeterministic. Run the
  grading suite twice on a sample; treat instances whose own grade is
  unstable as noise to exclude or flag, not signal.

## Condition on the governed situation

Most single rules fire rarely. force-with-lease only matters on a force
push; the comment rule only when the agent would write a comment;
"verify before voicing" only when it is about to assert a checkable
fact. Average such a rule's effect over a 500-instance suite where its
situation arises in fifteen, and the conditional signal is diluted
against the ~485 irrelevant instances — pushed below the noise floor by
construction, however load-bearing the rule is.

So a flat aggregate-resolution delta is the wrong estimator for a narrow
rule, and a null from it is ambiguous between two opposite findings: the
rule had no effect, or the benchmark never triggered it. Resolve the
ambiguity by conditioning on the governed situation — detect the
instances where the rule's trigger arose and measure the paired outcome
on that subset, where the per-instance effect is undiluted. The suite
size that gives only marginal aggregate power often gives ample power on
the triggering subset.

One statistical caution: condition on the *opportunity* — the situation
occurred, detected independently of the rule's own behavior — not on the
rule *firing*, its response. A rule that changes how often its own
trigger arises makes firing a post-treatment collider, and conditioning
on it induces selection bias. Detect the situation from the task or
transcript (a force-push step was reached, a comment site was edited)
under both arms, then compare outcomes within that matched set.

## Smallest first experiment

Do not open with the full sweep. The first run's job is to prove the
plumbing and *estimate the noise floor* — how much resolution varies
between two identical-corpus runs (same instructions, different seed).
That variance is the bar any real effect must clear.

1. SWE-bench **Lite**, n≈50, single frontier model, Tier-1 isolation.
2. Run the *same* corpus twice (A vs. A') to measure run-to-run variance.
3. Only if the A-vs-A' gap is small relative to the effect you hope to
   see is it worth scaling to Verified with the real A-vs-B contrast and
   paraphrase sweep.

If step 2 shows the noise floor already swamps plausible instruction
effects on this benchmark, that is itself the finding — but read it
correctly: for a narrow rule it usually means the suite rarely triggers
the rule, not that the rule is inert. Before concluding "unvalidatable,"
condition on the governed situation (above) or pick a more sensitive
task distribution; only a null on the *triggering* subset is evidence
the rule does nothing.

## "And similar": don't overfit to one benchmark

The instruction corpus is general, so a single-benchmark verdict
overfits. SWE-bench measures Python-library bug-fixing; this corpus also
governs research workflow, debugging discipline, run operations, and
multi-step planning that SWE-bench barely exercises. Span ≥2 task
distributions before generalizing: **SWE-bench Verified** plus one of
**Aider polyglot** (multi-language edit accuracy), **Terminal-Bench**
(shell/ops tasks closer to this repo's `agentctl`/runs work), or a replay
of this repo's own `tasks/*.md` as held-out scenarios. A rule that helps
on SWE-bench and hurts on terminal/ops tasks is a scoped rule, not a
global one — and the ablation is how you would find that out.

## What `resolved` stands in for

The developer-facing question is the valid one: how much *human* effort —
wall-clock, correction and review rounds — does it take to land a change
that both passes the tests *and* meets project requirements (a maintainer
would merge it), with the corpus versus without? SWE-bench `resolved` is
the automatable proxy for that gold standard, and it differs on two axes
that govern how to read any benchmark verdict (Gloaguen et al. included):

- **Cost unit is flipped.** The benchmark prices *agent tokens* — cheap and
  abundant; the objective prices *developer time* — scarce and expensive.
  Instructions trade the former to cut the latter (front-loaded convention
  knowledge buys fewer review-rework loops), so a token-cost metric books
  that trade as pure loss. A "+20% token cost" can be a net win in hours.
- **Outcome gate is lowered.** `resolved` = hidden tests green; "meets
  project requirements" = a human merges. The binary metric never checks
  the second half — the half most of this corpus is *for*.

Why not just run the gold standard: it is a within-subject HCI study, not a
benchmark — confounded by developer skill and agent-fluency, needing
counterbalancing and matched task pairs (you cannot reuse one issue
with-and-without), human-judged per instance, hence small-N and costly.
That cost is exactly why the proxy exists: the proxy's job is to be cheap
enough to sweep, the gold standard's is to be valid. The merge decision is
a *human* judge, not the LLM judge rejected below — unbiased-but-expensive,
where the LLM judge is cheap-but-biased.

Even the gold standard under-prices the tail-risk rules (the discard ban,
"don't invert a rule under compression"): their payoff is a rare
catastrophe *avoided* — a destroyed afternoon that never enters median
time-to-land. For those the estimator is the *tail* of human cost (rate of
unrecoverable rework or work-destroying events), not the median; a
median-time metric is blind to a variance-reducer.

## Simulating the merge bar: the calibrated-judge carve-out

The gold standard above needs a developer and a maintainer; both can be
*personas* of a SOTA agent — a developer-persona does the work, a
maintainer-persona gates on "tests pass **and** I would merge this" —
turning an expensive within-subject HCI study into something sweepable.
This deliberately admits the LLM judge the next section otherwise bans, so
it is valid only under conditions that convert "trust the judge" into "the
judge is checked":

- **The reviewer is a hybrid; only one half is a judge.** Running the test
  suite and checking for regressions is judge-free — keep it. Only the
  "meets requirements / mergeable" verdict is the LLM judge, and it is
  admissible *because it has ground truth*: SWE-bench ships `gold_patch`
  and the real PR was actually merged, so the persona's merge decision can
  be **calibrated against the human's**. Abstract "communication quality"
  has no such anchor and stays banned — the carve-out is for mergeability,
  not for prose scoring.
- **Calibrate on the adversarial slice.** The calibration set must include
  good-looking-but-wrong changes humans *rejected*; agreement on easy
  accepts flatters the judge, only the rejects test whether it is fooled.
- **Decontaminate the rubric — this is the dangerous bias.** "Meets project
  requirements" presupposes a rubric, and the obvious source is the project
  context file, which *is the treatment*. A reviewer reading the AGENTS.md
  under test grades the treated arm against its own rules → a manufactured
  false positive. Source the review standard from outside the treatment
  (the real PR's review-comment history, or a held-out human rubric), never
  the file being ablated. This is the multi-agent analog of the
  contamination invariants.
- **Two judge-biases, opposite signs.** Rubric-circularity inflates the
  *treatment* (false positive — kill it, per the bullet above).
  Gameability-by-emulation — the persona accepting persuasive compliance
  over real adherence — inflates the *baseline*: the no-instructions arm
  can reach "merged" by gaming the same as the treatment, erasing the
  treatment's adherence edge. Once circularity is removed, the only
  residual judge-bias is the benign one — it costs power, never a false
  positive — so an instructions-**win survives it (trustworthy)** while a
  **loss or tie stays ambiguous** (the judge may simply not see real
  adherence).
- **Cost-to-converge is judge-gaming-robust.** Gameability attacks the
  binary merged-or-not and the final-quality verdict, but not *rounds to
  converge*: a no-instructions agent ships a first draft violating
  conventions it was never told, eats more review feedback, and iterates
  more before it lands — more developer-time, the metric "What `resolved`
  stands in for" already elevated. Measure on cost-to-merge and the
  instructions advantage relocates to the axis the gameable judge cannot
  reach.
- **Judge-independence.** A maintainer-persona from the developer's own
  model family shares its exploits, so it is more gameable in the
  correlated direction; use a cross-family reviewer, ideally an ensemble.

This reframes the baseline itself. The honest "no-instructions" arm is not
the paper's *no context file at all* — it is *requirements delivered via
review rounds instead of front-loaded*. That is a fairer and harder
baseline, and it turns the question into "front-load the rules vs. learn
them from the reviewer," whose only clean scoreboard is cost-to-converge.

## Limits and cost

- The full SWE-bench image set is hundreds of GB; cache base images and
  reuse them across arms.
- A paired Verified run with a paraphrase sweep is thousands of agent
  rollouts per arm — real money. The pilot exists to avoid spending it on
  a rule whose effect is below the noise floor.
- This validates *outcomes on benchmark tasks*, not the corpus's effect
  on the qualities it mostly targets — clearer user communication, fewer
  silent wrong turns, durable cross-session policy. Those resist a binary
  pass/fail and stay, for now, intuition-grade. Honesty about that gap is
  the point: the ablation raises a few rules from `assumed` to measured;
  it does not retire the disclaimer in `agent-instructions.md`.
- Do not close that gap with an *uncalibrated* LLM judge. The binary
  `resolved` metric is trustworthy precisely because it is judge-free;
  scoring "comment quality" or "clearer communication" with a model
  reintroduces a grader selected by the same human-approval pressure the
  corpus's weakest rules are optimized for, so it would reward persuasive
  wording over effect — the exact bias this harness exists to escape.
  Those qualities have no ground truth to calibrate against, so they stay
  intuition-grade. The one admissible exception is the *mergeability* judge
  of the carve-out above, which earns its place only by calibration against
  real merge decisions; a quality-scoring judge has no such anchor.

## Relation to other topics

- [`agent-instructions`](agent-instructions.md) — the corpus this
  measures, and the source of the deferred-validation plan this doc
  realizes. Headline ablation results belong in its evidence ledger.
- [`provenance-tracking`](provenance-tracking.md) — every run must record
  model version, corpus revision, benchmark/version, seed, and isolation
  tier, or the number cannot be reproduced or trusted.
- [`testing`](testing.md), [`debugging`](debugging.md) — discipline docs
  whose own claims are candidate ablation targets.
