---
name: doubt
description: Re-evaluate a conclusion the user doubts by solving independently first, using external checks where possible, then comparing against prior reasoning to identify the first consequential divergence. Use when the user invokes /doubt or says they doubt, distrust, are unconvinced by, or want a clean re-check of an agent conclusion, answer, plan, proof, diagnosis, or review.
---

# Doubt

Run a clean doubt pass. The job is not to defend, patch, or lightly revise
the prior answer; it is to answer the underlying question again and then
diagnose where the earlier path first diverged.

If the user gives no explicit target, the target is the conclusion and
reasoning just applied by the agent in the current session.

## Workflow

1. **Frame the target.**
   - State the problem, goal, or question being re-answered.
   - State the prior conclusion only as the suspect result, not as the
     default.
   - If the target is materially ambiguous, emit a brief interruptible
     checkpoint and continue on the most likely branch when reversible.

2. **Solve independently first.**
   - Re-read the original problem and ground-truth sources before comparing
     against the old answer.
   - Actively avoid using the prior reasoning as a scaffold. Treat every
     prior premise, interpretation, and tool reading as untrusted until
     checked.
   - Use external checks where possible: source inspection, tests, minimal
     reproductions, calculators, authoritative docs, web/search, logs, or
     independent derivations.
   - If no external check is available, say the pass is reasoning-only and
     keep confidence modest.

3. **Compare after the fresh answer exists.**
   - Now inspect the prior answer, transcript, summaries, artifacts, or
     available reasoning trace.
   - Identify the first consequential divergence: problem framing,
     assumption, retrieved fact, calculation, semantics, control flow,
     scope, tool interpretation, or stopping criterion.
   - If actual reasoning is hidden or only summarized, do not invent it.
     Say "first visible divergence" and scope the claim to what you can see.

4. **Report compactly.**
   - Independent answer.
   - Checks performed, with file/source/command references when available.
   - First divergence.
   - Resulting correction or next action.

## Runtime continuity

If the runtime exposes a response or conversation handle, use it only after
the independent pass. For example, with the OpenAI Responses API,
`previous_response_id` can help compare against the prior response state,
but using it during the independent pass risks re-anchoring on the suspect
answer.

When chaining to the prior response, restate the doubt instructions in the
new request; prior response `instructions` may not carry over. Chaining also
does not guarantee faithful access to hidden reasoning, so divergence
claims still need to be limited to visible or otherwise available evidence.

## Anti-patterns

- Starting by critiquing the old answer.
- Treating the old answer as a default that needs only a patch.
- Assigning causal blame to a hidden chain-of-thought you cannot inspect.
- Letting a plausible narrative override a failed external check.
- Reporting "no issue found" without saying what was actually checked.
