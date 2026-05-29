# Doubt Skill

> The doubt skill re-evaluates a disputed conclusion by solving
> independently first, grounding the answer in external checks where
> possible, and only then comparing against prior reasoning to locate the
> first consequential divergence.

Topic: `doubt-skill`

The desired `/doubt` flow is:

1. Solve independently first.
2. Do not trust any prior reasoning.
3. After reaching an answer, compare against the given reasoning.
4. Identify the first divergence.

In a live session, the target is usually implicit: the reasoning steps and
conclusion the agent just applied. The visible context may contain only the
agent's final answer and a lossy summary of tool actions or reasoning, not
the actual latent chain. A correct doubt pass therefore cannot rely on
introspective blame assignment. It should use fresh evidence and external
checks where possible, then state the first divergence visible from the
available transcript and evidence.

## Motivation

Reasoning LLMs are often capable of sampling a strong problem-solving
trajectory, but are less reliable at assigning causal blame to an earlier
bad latent decision once the transcript has made that decision look like
settled context. A generic "check your work" prompt often starts from the
old answer and edits around it. `/doubt` deliberately breaks that anchoring
by making a clean independent pass before any critique.

This is adjacent to
[Self-Refine](https://arxiv.org/abs/2303.17651) (Madaan et al.,
NeurIPS 2023), which iterates feedback and refinement on an initial output.
`/doubt` differs in the order and objective: it first constructs an
independent answer, then compares against the prior path to find the
earliest answer-changing divergence. The goal is not polish; it is causal
diagnosis under partial observability.

## Contracts

- `/doubt` and natural-language doubt triggers mean: treat the prior
  conclusion as suspect, not as context to defend.
- The independent pass comes before critique. Read the original problem,
  current repo state, logs, source files, docs, tests, or other ground truth
  needed to answer the question directly.
- Use external checks where possible: tests, minimal reproductions, code
  inspection, calculators, authoritative docs, search, or independent
  derivations. If no external check is available, label the result as an
  ungrounded reasoning-only pass.
- Compare only after the independent answer exists. The report should name
  the first consequential divergence: framing, assumption, retrieved fact,
  calculation, semantics, control flow, scope, tool interpretation, or
  stopping criterion.
- Do not invent hidden chain-of-thought. If the actual reasoning trace is
  unavailable, say so and identify the first divergence visible from the
  transcript, summaries, artifacts, or evidence.

## Implementation notes

If a runtime exposes a prior response or conversation handle, use it
carefully. For the OpenAI Responses API, the
[`previous_response_id`](https://platform.openai.com/docs/guides/conversation-state?api-mode=responses)
conversation-state mechanism can chain responses and carry previous
response context into a later call, but it should not be used for the
independent pass because it may re-anchor the model on the suspect answer.
It is useful after the independent pass, when the task is to compare
against the prior response. Even then, it may not provide faithful access to
hidden reasoning; the divergence claim must stay scoped to available
evidence.

When using response chaining, restate the current doubt instructions in the
new request. The
[OpenAI API reference](https://platform.openai.com/docs/api-reference/responses?api-mode=responses)
notes that prior `instructions` are not carried over when
`previous_response_id` is used.

## Non-goals

- `/doubt` is not an adversarial review mode. It may conclude the original
  answer was correct.
- `/doubt` is not a request to expose private chain-of-thought. Provide a
  concise reasoning summary and evidence instead.
- `/doubt` is not a license to cross normal gates. Big-effect commands,
  file writes in discussion-only contexts, credentials, pushes, deploys,
  or destructive actions still follow the governing instructions.
