# Topic: agents-bench

> A proposed benchmark that reproduces the AGENTS.md-helpfulness question
> (see [`agent-instructions.evidence.md`](agent-instructions.evidence.md),
> Gloaguen et al. 2026-06-25) on *sequences* of historical tickets from
> real, CI-backed OSS repos stratified by size — scoring whole instruction
> corpora (ours vs. others') by judge-free cost-to-converge and by whether
> the repo's *own future tests* still pass on the agent's branch, so the
> longitudinal hygiene/accessibility value a single ticket cannot show
> becomes measurable.

Topic: `agents-bench`

This is a **proposal**: nothing has been built or run. Treat every design
choice below as a target to be falsified by a pilot, not a result.
<!-- assumed -->

`agents-bench` is a working coinage for "a benchmark of agent-instruction
*corpora*" — the treatment under test is a whole `~/agents`-style
instruction repo, not a model or a scaffold. Confirm or rename before it
spreads.

## Why a new benchmark, not just instruction-ablation

[`instruction-ablation`](instruction-ablation.md) already supplies the
measurement *machinery* — paired arms, McNemar on discordant pairs,
network-off directory-scoped isolation, contamination invariants, the
paraphrase sweep, and the calibrated-judge carve-out for the "would a
maintainer merge this" half. `agents-bench` reuses all of it unchanged and
adds the two things that machinery assumes someone else provides:

1. **A dataset with properties SWE-bench lacks** — chronological *sequences*
   of tickets per repo, a README-bearing fair baseline, and explicit
   size strata. SWE-bench is single-shot, library-flavored, and its
   no-context arm is "no context at all."
2. **A cross-*corpus* contrast, not a cross-*rule* one.** The arm varies a
   whole published instruction repo (ours, someone else's, none,
   auto-generated). instruction-ablation gates and culls rules *within* our
   corpus; agents-bench ranks corpora *against* each other on real repos.

If a pilot shows the sequence twist is unworkable (divergence, below), this
collapses back to instruction-ablation's single-shot A/B on a better repo
set, which is still worth having.

## The reproduction, and the twists

Kept from the paper: instruction corpus as the treatment; a real ticket
with a hidden test patch as the judge-free, deterministic ground truth
(`FAIL_TO_PASS` must go green, `PASS_TO_PASS` must stay green).

**Twist 1 — sequences, not single tickets (the headline).** The value of
instructions aimed at *sane long-term evolution* — code quality, keeping the
repo agent-navigable — is invisible in one ticket by construction: there is
no "later" for the hygiene to pay off in. So replay a repo's real ticket
history in chronological order on one *persistent* working branch per arm.
The agent's own accumulated decisions become the substrate the next ticket
lands on. Good instructions should show up as a *flatter cost slope* and
*longer survival* across the run, not a higher single-ticket pass rate.

**Twist 2 — the repo's own future tests are the quality judge.** This is the
answer to "we cannot easily LLM-judge quality." A patch that is locally
green but globally degrading gets caught for free when a *later* real
ticket's added tests fail on the agent's branch. The project's future
history is an objective, judge-free grader of whether an earlier solution
was sane — no model scoring "code quality." The sequence is the single
mechanism that solves *both* open problems the prompt named: it gives the
compounding benefit room to appear (Twist 1) and it supplies the quality
signal (Twist 2).

> Hard part, named not hidden — **counterfactual divergence.** Once the
> agent's patch differs from the merged one, real future commits/tests may
> not apply cleanly to its branch, and merge conflict confounds the cost
> signal. Candidate resolutions to pilot: (a) keep sequences short (5–20
> tickets) so divergence stays bounded and measure the cost *slope* over
> that window; (b) apply future tests only where they touch modules the
> agent left functionally equivalent; (c) periodically rebase the agent's
> structural artifacts onto the real merged base while preserving what the
> instructions changed (risky — may launder the effect). Which of these is
> viable is the central thing a pilot must settle.

**Twist 3 — cross-corpus leaderboard.** Hold model and scaffold fixed; vary
the instruction repo: ours, others' published `AGENTS.md`/global-instruction
repos, none, vendor-auto-generated. "Evaluate others' agents repos against
our own." Informative, not definitive: a foreign corpus may assume a
different harness or workflow, so a loss for it can be a harness mismatch,
not worse instructions — report the mismatch rather than scoring through it.

**Twist 4 — README-only is the fair baseline.** The no-instructions arm
still gets the repo's own README onboarding, and gets requirements via the
simulated-maintainer review rounds of instruction-ablation's carve-out — not
zero context. This is the harder, fairer baseline the paper skipped, and it
reframes the question as *front-load the rules vs. learn them from the
reviewer*, whose only clean scoreboard is cost-to-converge.

**Twist 5 — stratify by size, expect size to modify the effect.** Small
repos may not need much beyond their README; large/complex ones should
reward navigation and convention instructions most. Size is an
effect-modifier, so report per-stratum and predict the instruction benefit
*grows* with repo size, ticket-graph depth, and test-suite breadth. A
corpus that helps large repos and hurts small ones is scoped, not global —
the same lesson instruction-ablation draws about scoped rules.

## Dataset selection criteria

Per the prompt, a repo qualifies only if all hold:

- **Substantial/significant OSS** — real contributors, real review culture,
  enough surface that navigation and convention actually matter.
- **Reasonable per-repo README onboarding** — required, because it defines
  the fair baseline (Twist 4); a repo with no onboarding can't separate
  "instructions help" from "any context at all helps."
- **Working CI test suite of believable size** — the source of both the
  `PASS_TO_PASS` regression signal and the future-tests-as-judge quality
  signal. Too small and neither bites.
- **Tickets with a decent merged solution and tests** — `FAIL_TO_PASS`
  must exist; a ticket whose fix shipped no test is ungradeable here.
- **Stratified by size** — bucket by LOC, contributor count, test-suite
  breadth, and ticket-sequence depth; sample across buckets, not just the
  cheap small ones.
- **Sequence-formable** — enough chronologically adjacent qualifying tickets
  per repo to form a run, not a single isolated fix.

Selection criteria must be **pre-registered** before looking at results, or
the leaderboard is just a search for repos where our corpus wins.

## Metrics

Judge-free wherever possible; the only model-judged component is the
optional mergeability verdict, admissible only under instruction-ablation's
calibrated-judge carve-out.

- **Cost-to-converge** (primary) — agent rounds / wall-clock / tokens to
  reach green on a ticket, and crucially its **slope across the sequence**.
  Flat or sublinear slope is the instruction-value signal.
- **Survival depth** — how far into the sequence the agent's branch keeps
  passing accumulated + future tests before it rots.
- **Future-test pass rate** — objective quality proxy from Twist 2.
- **Per-ticket `resolved`** — kept for comparability with the paper, but
  de-emphasized: it is the weak single-shot metric this design exists to
  go beyond.

## Contamination is the acute threat here

"Significant OSS" means "heavily memorized." instruction-ablation's
contamination invariants all apply; agents-bench makes contamination
load-bearing and adds an active detector rather than trusting dates.

- **Stay ahead by harvesting — this is a *living* benchmark.** The primary
  defense is freshness: VERY recent tickets, harvested continuously
  (SWE-bench-Live style) so even the frontier eval model is past its cutoff.
  A frozen set is contaminated within one model generation, so the
  operational commitment is a rolling harvest, not a one-time dataset.
  Record `model_cutoff × ticket_date` per instance; treat recency as a
  first-class stratification axis.
- **Sequence wrinkle, in our favor:** later tickets in a chronological run
  are newer, so weighting survival/cost toward the tail partly launders
  memorization of the early, famous fixes.
- **An active memorization probe, calibrated against known-clean.** Do not
  assume freshness; measure it. For a model exposing token logprobs (the
  eval model where possible, else a same-era open-weights proxy), score how
  predictable the held-out *fix* — gold patch, test patch — is given only
  the issue and the base-commit repo (Min-K%/perplexity-style membership
  inference). Flag and exclude instances whose predictability exceeds a
  baseline **calibrated on known-clean post-cutoff tickets** — some fixes
  are predictable from the code alone (easy ticket) rather than from
  memorization, and only the null separates the two. Probe the *solution*,
  never the issue text (the agent gets that anyway). Two honest limits: it
  catches verbatim memorization, not conceptual leakage from
  changelogs/blogs/discussion (necessary, not sufficient); and on a closed
  frontier model with no logprobs the signal is only a proxy's, which
  under-detects the frontier model's larger, fresher training set.
- **A guaranteed-clean old model is a sanity arm, not the eval.** An
  open-weights release predating the tickets *cannot* be contaminated — but
  it is weaker, and a weak model's best corpus differs from a strong one's
  (this corpus already splits `AGENTS.weak.md` from `AGENTS.frontier.md`).
  So it answers a different question: a contamination-free lower bound that
  the corpus helps *at all*, whose corpus *ranking* does not transfer to
  frontier models. Run it as a check, not as the headline.

## Open design questions a pilot must answer

1. **Divergence** (Twist 2's hard part) — which counterfactual-history
   resolution survives contact with a real repo. Central; everything else
   is secondary if this fails.
2. **Cost-unit comparability** across heterogeneous agents/harnesses.
3. **Corpus normalization** — corpora differ in length/token budget;
   equalize the budget or report tokens alongside, per instruction-ablation.
4. **Cross-harness fairness** for foreign corpora (Twist 3).
5. **Sequence length vs. divergence** tradeoff — long enough for compounding
   to show, short enough to stay applicable.
6. **Probe transfer** — whether a logprob memorization probe calibrated on
   known-clean tickets reliably separates "memorized" from "merely easy,"
   and whether a same-era proxy model's signal stands in for a no-logprob
   frontier eval model.

## Relation to other topics

- [`instruction-ablation`](instruction-ablation.md) — the measurement
  machinery, statistics, isolation, contamination invariants, and
  calibrated-judge carve-out this proposal reuses wholesale; read it first.
- [`agent-instructions`](agent-instructions.md) and its
  [`evidence`](agent-instructions.evidence.md) ledger — the corpus under
  test and the origin (Gloaguen et al.) this reproduces; headline results
  land in that ledger.
- [`provenance-tracking`](provenance-tracking.md) — every run records model
  version, corpus revision, repo+ticket-date, seed, isolation tier, or the
  number cannot be trusted or reproduced.
