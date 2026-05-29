# Goal distillation

> Training a goal-conditioned agent from goal-annotated interaction
> sessions: the goal's testable done-condition serves as the
> verifier/reward, process labels keep the agent from learning to game
> that reward, and a strong teacher or self-critique installs the
> integrity a prompt can only request.

Topic: goal-distillation

Companion to the [`wish`](../skills/wish/SKILL.md) skill. `wish` is the
*inference-time* shepherd of an autonomous goal loop; this doc is the
*training-time* question — how an agent could be made to run that loop
well in the weights, not just because a prompt asked. The connecting
idea: a prompt safeguard ("don't game the metric") is a weak lever,
because a model trained so the cheat never earned reward simply wants it
less. See [agent-instructions](agent-instructions.md) "Limits of these
methods" for why prompt-only safeguards are unverified.

## Core: the done-condition is the reward

`wish` requires rewriting a goal X as testable predicates. That artifact
is, not by coincidence, the exact ingredient verifiable-reward training
needs: a programmatic check that gates reward. RLVR-style training samples
N rollouts, keeps the ones whose check passes, and updates toward them; the
contract's done-condition doubles as the reward function.

The cheapest instantiation is **rejection-sampling fine-tuning** (STaR /
ReST / RFT): run the loop many times on goals that have tests, fine-tune on
the trajectories that reach DONE-by-test, iterate. For software goals this
is already standard practice — keep only trajectories whose patch passes
the suite, SFT on those, repeat.

## Outcome vs. process supervision — the genie-training trap

<!-- verified: web search 2026-05-29 (Lightman 2023; RLVR noisy-verifier work) -->
Outcome-only reward *trains the loophole*. If reward = "tests green" and the
agent can edit the tests, RLVR actively reinforces deleting or weakening
them, because the cheat earns reward. This is the training-time form of the
`wish` anti-genie problem, and prose cannot fix it — the gradient does what
the reward says, not what the prompt asks. Two correct responses, ideally
combined:

1. **Process supervision** — label the steps, not just the outcome
   (Lightman et al. 2023, "Let's Verify Step by Step"; PRM800K, 800k
   step-level labels). Step-level reward beat outcome reward on MATH, and
   it is the lever for anti-genie: penalize the "weakened the test" step
   even when the final state looks green. The agentic version is
   rubric-style process reward models over trajectories. A per-cycle "was
   this a hack / a correct gate-stop / an appropriate ask?" annotation is
   exactly a process label.
2. **Tamper-proof verifier** — hold the done-condition tests outside the
   agent's write scope so corruption cannot pay. Cheaper than process
   labels; do both when you can.

Caveat: verifiers are noisy. One 2025 analysis found ~38% of
rule-flagged-incorrect answers were actually correct; a noisy verifier
silently caps the achievable ceiling and can teach the wrong lesson.

## Teacher branch: on-policy distillation

For a strong-model teacher, the current best-in-class is **on-policy
distillation**: the *student* rolls out the wish trajectories and the
teacher grades each token of the student's own visited states. It beats
plain SFT (no exposure bias / distribution shift between train and
inference) and beats sparse RLVR (dense per-token signal), and is reported
to reach teacher level far cheaper than RL. The classic framing is
DAgger-style relabeling — student visits the states, teacher says "here you
should have asked / stopped at the gate / not gamed the metric." Known
ceiling: a single teacher's errors transfer to the student, and per-step
errors compound over long agentic trajectories.

## Assembling the pipeline

<!-- assumed: synthesis/design, not drawn from a specific paper -->
A concrete data pipeline (design, not a cited recipe):

- **Goal-conditioned sessions.** Tag each session with the wish contract
  (intent + done-condition) as conditioning, so you train a goal-*conditioned*
  policy rather than a bag of completions — that conditioning is what lets
  the model honor an arbitrary new goal later.
- **Two reward channels.** (a) Outcome: done-condition test pass — free,
  automatic. (b) Process: a lightweight per-cycle annotation of the three
  things `wish` already names — hack-attempt? correct gate-stop? ask vs.
  proceed appropriate? Human early; distilled judge later.
- **Curriculum by uncertainty.** Sample goals where success is roughly a
  coin flip; trivial and impossible instances teach little.
- **Three stages.** Filter+SFT on verified honest trajectories (gets off
  the floor) → **preference-tune on hack-vs-honest pairs for the same goal**
  (DPO/RLAIF; this is where the disposition is installed — generate both a
  loophole and an honest completion, prefer honest) → optional trajectory
  RL (GRPO/PPO) with verifier reward minus a process penalty for gaming.
  The middle stage is the Constitutional-AI / RLAIF shape, where the wish
  anti-genie rules *are* the constitution the model critiques itself
  against — plausibly close to how a vendor instills `/goal` integrity:
  not (only) a prompt, but a trained self-critique.

## The frontier hole: unverifiable goals

The whole stack assumes a verifier. Real software goals — "make the
dashboard feel responsive," "clean up the auth flow" — often have no clean
test, which is exactly the regime `wish` is built for. RLVR does not extend
there; you fall back to LLM-judge reward (gameable) or expensive human
process labels. So the distillation story is weakest precisely where the
skill is most needed (open-ended goals) and strongest where a careful
prompt is arguably unnecessary (math/code with oracle tests). That gap is
the live frontier, and it is why the prose safeguards in `wish` are not
redundant with a trained model: for unverifiable goals, "demonstrate, don't
declare" and "stop at the blast radius" do real work no current reward
signal supplies.

## References

- Lightman et al. 2023, *Let's Verify Step by Step* — arXiv 2305.20050 (PRM800K).
- Zelikman et al. 2022, *STaR: Self-Taught Reasoner* — arXiv 2203.14465;
  ReST (Gulcehre 2023), ReST-EM (Singh 2023) as the rejection-sampling line.
- RLVR / verifiable-reward training — e.g. Tülu-3 (Lambert et al. 2024);
  noisy-verifier limits, arXiv 2510.00915.
- On-policy distillation — Thinking Machines Lab (2025); GKD (Agarwal et
  al. 2023); DAgger (Ross et al. 2011).
- Constitutional AI / RLAIF — Bai et al. 2022, arXiv 2212.08073.
- Long-horizon SWE-agent RL — arXiv 2508.03501; rubric process rewards,
  arXiv 2604.14820.
