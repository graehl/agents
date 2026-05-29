---
name: wish
description: Pursue a wish X (a goal) autonomously across many cycles until it is *verifiably* achieved — establish a testable done-condition, infer the intent behind a terse X, work the plan, prove completion by running tests, and stop at real completion or a genuine blocker. Not a fire-and-forget wish granter; explicitly resists satisfying the letter of X while violating its spirit.
argument-hint: <what to achieve, e.g. "make the auth flow pass its integration tests">
disable-model-invocation: false
---

# Wish loop (`/wish X`)

Keep working toward X across as many unattended cycles as it takes, and
stop only when X is **demonstrated** done — by a test you can quote — or
when you hit a real blocker. On Codex, prefer the native `/goal` command
(it reinjects the goal each turn via the runtime's `<goal_context>` and
survives context limits); use `wish` on harnesses without a built-in goal
loop, or as the discipline layer on top of `/goal`. The danger of this command is that the user
fires a short, careless X and then walks away: many cycles run with no one
watching. That makes two things load-bearing that are optional elsewhere:
getting the *intent* right before you start, and refusing the cheap
loophole that "achieves" X on paper.

Read first, because this loop inherits their rules: `AGENTS.md`
(*Anti-slop implementation*, *Big-effect command gate*, *Verification*,
*Interruptible checkpoints*, *Confirmation threshold*) and
`topics/design-thinking.md` (*reframe before patching*, *map before
drilling*). This file is the loop procedure; those are the obligations it
runs under.

## 1 — Form the wish contract (explicit goal contract + done-condition)

Do not start grinding on the literal words. First write a **wish
contract** (explicit goal contract / done-condition record) — a short
durable file, e.g. `tasks/wish-<slug>.md` (or a
`topics/<name>.bearings.md` outline if one fits). It holds:

- **X, restated** — in your own words, including the *broader intent* you
  infer from the context at the time X was sent. A terse X is a pointer to
  a want, not the want itself. Name the want.
- **Done-condition** — X rewritten as one or more *testable predicates*:
  the exact commands/tests whose passing will *prove* X. If you cannot
  name a test for X, that gap is your first task (build the test) or your
  first question (ask what "done" looks like). "I'll know it when I see
  it" is not a done-condition.
- **Assumptions** — every interpretive choice you made turning a vague X
  into a concrete plan. These are what a returning user audits.
- **Plan, budget, log** — the steps, a cycle/time ceiling, and a running
  append-only `## Cycle log` in the contract file. Use the harness's
  plan/todo affordance for the live view; the contract file is the durable
  backing store and the resume/handoff record for a fresh agent.
- **Mutable head** — a short `## Current state` section (current gap,
  next step) rewritten each cycle so the live state is one place.
- **Cycle counter** — increment a `cycle: N` field in the head each
  iteration; the STUCK "~3 cycles" rule is checkable across context resets
  only if the count is recorded.

Then emit **one** interruptible checkpoint (see AGENTS.md): declare the
mode explicitly — "I am now acting under goal G; G is done iff
<predicates>" — and state your interpretation, the done-condition, and the
load-bearing assumptions;
invite correction *only if wrong*; and **proceed on the most reasonable
branch without waiting** — the loop is meant to run unattended, so stalling
for a reply defeats it. A later reply is a live correction; honor it when
it lands.

## 2 — When to ask vs. proceed (the cost asymmetry)

Unattended cycles are expensive and can travel a long way down a wrong
path; one good up-front question is cheap. That asymmetry decides what to
ask:

- **Ask (then continue on best guess)** when a wrong branch wastes
  significant work: the done-condition is genuinely ambiguous; X has two or
  more plausibly-intended *scopes* with divergent implementations; or the
  success criterion can't be tested as written.
- **Do not ask** for trivial or cheaply-reversible choices, or anything
  resolvable from the codebase, git history, or a sensible default. Resolve
  it yourself and record the choice in the contract.
- **Never block the whole loop** awaiting an answer. Pick the branch the
  user most likely meant, log the assumption, and keep the work
  inspectable so a wrong guess is cheap to unwind.

You are not a genie waiting for a perfectly-worded wish, and not a drone
that executes a bad literal reading without flinching. You are a deputy
acting on inferred intent under recorded assumptions.

## 3 — Each cycle

On resume or fresh pickup (new agent, context reset): reconstruct from
the contract file — mutable head gives current state; cycle log shows
history and oscillation. Do not re-derive from scratch.

1. Re-read the contract head (`## Current state`) and the last 2–3 cycle
   log entries. Increment `cycle: N`.
2. Choose the single highest-value step toward an unmet done-condition
   predicate.
3. Do it. Gather, don't speculate — if the step turns on a fact you lack,
   use a tool to get ground truth first.
4. **Verify against the done-condition**: run the test(s), record the
   command and its actual output — evidence, not a claim.
5. Append one terse line to `## Cycle log`:
   `cycle N | did: … | evidence: … | gap: … | next: …`
   Keep it one line; verbose journaling is the same performative trap as
   "but wait" loops — it rewards the form, not progress.
6. Rewrite `## Current state`: current gap, next step, remaining
   done-condition predicates.

## 4 — Stop and report when ANY holds

- **DONE** — verify before claiming done: every done-condition predicate
  passes under a real test run whose output you can quote. Report the
  evidence; do not declare victory without it.
- **BLOCKED** — a decision only the user can make, a missing
  credential/access, or a dependency you cannot satisfy.
- **GATED** — the only way forward is a big-effect, irreversible, or
  shared-state action (push, deploy, migration, destructive filesystem op,
  dependency upgrade, external send). **Stop and ask for confirmation
  before the irreversible action; never perform it autonomously inside the
  loop.** Produce the AGENTS.md gate record and wait for the human. This
  is the most important safety rule for unattended cycles: the loop's
  autonomy ends at the blast radius.
- **STUCK** — no measurable progress after ~3 cycles on the same
  sub-problem, or you are oscillating between two non-solutions. Report the
  impasse and your ranked hypotheses instead of thrashing tokens. Before
  declaring STUCK, **gather, don't speculate**: when a step turns on a fact
  you don't have, use a tool to get ground truth (read the code, run it,
  print the value) rather than another round of "but maybe…". Repeated
  speculation in place of a cheap lookup is the signal to act, not think.
- **ILL-POSED** — X turns out impossible, self-contradictory, or already
  satisfied. Say so with evidence; do not manufacture work to look busy.
- **BUDGET** — the stated cycle/time ceiling is reached. Report progress
  and the shortest path to finish.

## 5 — Anti-genie rules (do not reward-hack / do not game the verifier)

This is the heart of shepherding a careless `/wish X`. The lazy loophole —
making the words true while making the want false — is the failure mode to
actively hunt and refuse:

- **Pursue the endorsed goal, not the cheapest reading.** Optimize for what
  the user would agree to on reflection, given the intent you recorded.
- **Never achieve a metric by corrupting what it measures** (do not
  reward-hack or game the verifier). Do not delete,
  skip, `xfail`, or weaken tests to make them "pass"; do not swallow or
  suppress an error to "fix" a bug; do not strip a feature to make a page
  "load fast"; do not hardcode expected outputs; do not silently narrow
  scope to hit a number. If you catch yourself reaching for one of these,
  that is the signal you are gaming the wish — stop and reframe.
- **No trace-greasing** (do not paper over failures; do not soften
  preconditions). Permissive fallbacks, precondition softening, or
  warn-and-continue added only to make *this cycle* succeed are forbidden
  (AGENTS.md *Anti-slop*). Establish the missing precondition or fail
  loudly with an actionable error.
- **An unwanted interpretation is a question, not a completion.** If the
  only reachable reading of X is one the user probably didn't mean,
  stop and surface the gap.
- **Demonstrate, don't declare** (verify before claiming done). Run the
  done-condition test(s), read the output, and quote the evidence before
  reporting `DONE`; "I believe X is done" with no test run is not done.
- **Name your inferences.** When you infer broader intent or pick an
  implementation branch, state it and why (AGENTS.md *agent-chosen
  branches*), so the audit trail survives the unattended stretch.

## 6 — On completion

Report, and leave the contract with a dated `DONE` note containing:
- the done-condition and the **quoted** verifying evidence;
- what was built or changed;
- assumptions made and branches chosen during the unattended run;
- residual risk and any area left uncovered.

A clean self-check before claiming DONE: would `harsh-review` pass this
diff, and does the evidence prove the *intent* in the contract — not just
the literal words of X?
