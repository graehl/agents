# Theorem development

> Develop and check the program's mathematical claims while recording which
> reasoning procedures improve them.

Topic: research/efficiency-and-alignment/theorem-development
Glossary: omit

This is the local pilot required by [the program](../PROGRAM.md), not a general
theorem-proving policy. Its first application is the
[optimizer-audit analysis](../papers/conditional-reuse/sections/_37-optimizer-memory.qmd).
Use the procedures that address the current uncertainty; the aim is a correct,
useful result with explicit hypotheses, not completion of a checklist.

## Fix the mathematical question

Before deriving a new claim, write its quantified statement and the model it
actually concerns. For training audits this includes the optimizer recurrence,
initial state and counter, horizon, learning-rate convention, attacker budget,
allowed interventions, all-step checks, sampled checks, and target quantity.
Keep the auditor's random choices private after commitment even when the
attacker knows the audit family. Distinguish training draws from audit draws.

Keep direct weight edits, optimizer-state replacements, and forged gradients
as distinct feasible sets. State whether the cheap audit rejects an oversized
raw step or the optimizer clips it. State whether future gradients are fixed
inputs or recomputed at the changed weights. Mark a relaxed model explicitly;
a construction in it does not establish realizability through plausible data.
Changing one of these assumptions creates a different claim, not a silent
repair to an existing proof.

## Find connections and try to refute the claim

Start with the smallest case that could kill the proposed conclusion: scalar,
one intervention, a short horizon, and a fixed recurrence. Ask for a proof or
counterexample. Then add the feature the real question depends on, such as
gradient feedback or coupled moments. A counterexample that identifies a
necessary audit condition is a useful result.

Search by mathematical structure as well as application vocabulary. Candidate
connections here include impulse responses and induced gains for momentum,
reachable sets for constrained state edits, and optimization stability for
gradient feedback. Before importing a theorem, retrieve its actual statement
and map its objects and hypotheses to this model. Reject a connection whose
regularity, norm, independence, or asymptotic assumptions do not hold. Record
useful failed connections so later work does not repeatedly rediscover them.

Separate the logical dependencies: local state corruption, propagated parameter
change, behavioral change, required number of invalid transitions, and audit
detection probability. Each arrow needs its own argument. In particular, small
parameter movement alone does not bound a discrete behavioral change without
an appropriate regularity or margin assumption.

## Check the load-bearing step

For a closed form or finite optimization, compare an implementation of the
original recurrence with the independently derived expression. Use exact
arithmetic where practical; include endpoints and the conditions most likely
to change the answer, such as bias correction, clipping location, denominator
floors, and delayed interventions. Exhaustive small instances can check a
dynamic program. Preserve a minimal failing case when a conjecture breaks.
Passing simulations are finite checks, not a proof of the general claim.

Re-derive the decisive lemma from the model before comparing with the candidate
proof. Concentrate review on the strongest quantifier and weakest reduction.
Independent review can be useful when authorized; this procedure does not
itself authorize spawning agents. Keep a readable proof with its assumptions
even when an external checker succeeds.

Use Lean or another proof assistant when a stable, consequential lemma has
enough algebraic or logical complexity to justify formalization. Start with
the smallest result that removes a real uncertainty, for example the finite
residual-propagation inequality. Do not formalize a moving model merely to
produce a verified artifact. Record “not formalized” when that is the state.

When formalizing, review the correspondence between the prose and formal
statement separately from the proof. Check definitions, quantifiers, excluded
cases, non-vacuous assumptions, admitted axioms, and any use of placeholders.
Pin the toolchain and libraries and retain the exact verification command and
result. Kernel acceptance proves the submitted statement; it does not prove
the statement models the optimizer, data commitments, or behavioral objective.
When using Lean Comparator or an equivalent challenge checker, keep the trusted
statement separate from the proposed solution and verify its supported local
interface before invoking it.

## Record performance before promotion

Append consequential methodology observations to
[the evidence record](theorem-development.evidence.md). Link the exact claim
and reproduction artifact; record the initial conjecture, intervention, defect
caught or new result obtained, unsuccessful attempts, remaining uncertainty,
and incremental effort when measured. Do not invent timing or imply that a
retrospective success isolates the instruction's causal effect.

Several substantively different claims should demonstrate repeatable benefit
at acceptable cost before proposing promotion. Compare against ordinary work
where feasible and retain failures. Promote the particular useful procedure,
not the entire workflow because one theorem was proved. Global instructions
remain outside this pilot's edit scope.

## Disclosed precedents and their limits

The following primary sources were read on 2026-10-17 for their process
disclosures. They motivate this pilot; none establishes that this instruction
sequence improves our program's results.

- Woodruff et al., [*Accelerating Scientific Research with Gemini*,
  sections 2 and 9](https://arxiv.org/html/2602.03837v3), describe cross-field
  connections, executable counterexamples, and checking theorem hypotheses;
  they report confirmation bias and dropped constraints. These are selected
  case studies, not an ablation of the proposed workflow.
- Feng et al., [*Towards Autonomous Mathematics Research*, sections 1–2](https://arxiv.org/html/2602.10177v3),
  separate generation, verification, and revision in Aletheia. Their
  natural-language verification is distinct from proof-assistant acceptance;
  autonomy is also distinct from mathematical novelty.
- Hubert et al., [*Olympiad-level formal mathematical reasoning with
  reinforcement learning*](https://www.nature.com/articles/s41586-025-09833-y),
  describe AlphaProof's Lean search, related problem variants, and cheap
  refutation. Its learned search machinery is more than a prompting recipe.
- Anthropic's [August 2026 zeta-result process account](https://www.anthropic.com/news/riemann-zeta)
  describes failed ideas, numerical falsification, literature checks,
  independent reconstruction, human review, and Lean formalization. The
  announcement was read; its headline theorem and complete proof artifacts
  were not independently verified here. Its search budget is not a default.
- OpenAI's [October 2026 mathematics release](https://openai.com/index/sharing-ai-progress-in-mathematics/)
  links manuscripts, formal artifacts, and reasoning summaries with differing
  verification status. The linked reasoning PDFs were not read for this pilot;
  no detailed discovery method is attributed to them.
- [Lean Comparator's documentation](https://github.com/leanprover/comparator)
  distinguishes a trusted challenge from a proposed proof and warns that
  definition holes can make a checked claim vacuous. This motivates the
  separate statement review; local tool availability must still be checked.
