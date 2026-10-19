# Agent learning: working agenda

## Comparisons that could change practice

For hard tasks, compare experience-guided retries against equally expensive
portfolios of independent samples/models, including verification and answer
selection costs. Record independently verified successes, failure modes, and
which prior episode changed the successful attempt. A single breakthrough can
be valuable without establishing general average superiority.

For routine tasks, compare the existing triggered-read/lazy-read hierarchy and
graehl's manual review practice with these separable interventions:

| Candidate | Discriminating comparison |
|---|---|
| Retrieve similar raw sessions | Inspect tools, skills, corrections, failures, and outcomes from similar tasks, without advance summarization or skill creation. |
| Summarize when needed | Synthesize only retrieved episodes at query time versus reading their raw evidence. |
| Consolidate in advance | Task-end or periodic memory/skill extraction versus retrieval alone, accounting for unused artifacts. |
| Human consolidation | Automatic accumulation followed by graehl's criteria review and edits versus fully automatic promotion and manual review alone. |
| Periodic working observer | One continuing session reviewing accumulated work versus isolated structured reviews with the same evidence and budget. |
| Context selection outside the working turn | Mechanical retrieval/injection versus foreground relevance decisions; check whether the selector knows the active task well enough. |
| Review timing | Agent-declared task boundary, user signal, end of turn, inactivity, counters, and a separate review-worthiness decision. |

Hold model, harness, tools, task information, and budgets fixed where the
question is the mechanism. Test recurrence, transfer, changed circumstances,
and irrelevant history. Keep an oracle-selected relevant episode as a
diagnostic of retrieval failure versus inability to use retrieved information.
Use fresh task outcomes to judge utility; a reviewer liking its own rewritten
instructions is insufficient.

An initial small paired pilot can identify promising failures and estimate
costs; it cannot establish reliable general superiority. Freeze task sets,
source history, acceptance checks, and artifact versions before a consequential
comparison. Record prior task exposure to prevent learning from the answer.

Cost includes learning and review calls, retrieval and summarization, injected
tokens, foreground latency, subscription quota, human supervision, adoption
burden, maintenance, and regressions from stale or wrong guidance. Count empty
reviews and unused memories. Compare actual supported subscription routes;
nominally free calls still consume time and quota.

## Translation into our systems

For a useful technique, identify the smallest implementation surface:
instruction or meta-instruction; a change in graehl's review practice; a
periodic observer; boot/routed context; an MCP retrieval or storage tool; or YA
lifecycle orchestration. An MCP tool offers a capability to its caller; the
host determines invocation and lifecycle. Investigate host support before
calling an orchestration limitation inherent to MCP.

Preserve the active task, source provenance, and instruction authority when
injecting retrieved material. Compare additive injection with any technique
that rewrites history: the former may be practical in a subscription harness
without reproducing the latter's token savings. The implementation experiment
must expose that difference.

## Monthly monitoring: report only actionable evidence

Follow the products and communities in [GLOSSARY.md](GLOSSARY.md), including
primary implementation changes, evaluation artifacts, issue reports, and
failed replications. Expand to another product when it introduces a distinct
candidate or relevant evidence. Each product/community topic records:

- what it offers for this program, with mechanism and source;
- additional orthogonal capabilities and our applicability judgments;
- what was implemented, merely advertised, proposed, or independently tested;
- a useful bounded next test, and subscription/harness constraints.

A user-facing report needs new evidence supporting a concrete replication,
adoption, rejection, or changed priority in one of the two use cases. Include
the claim, source/revision, relevant baseline, outcome and total cost, missing
controls, and the smallest proposed action. Feature churn, popularity, token
savings without quality checks, and interesting examples alone do not qualify.
Keep a short internal check record when nothing qualifies; send no routine
digest merely to prove activity.

Monthly source monitoring and periodic review of our own instructions are
different activities. Monthly monitoring is requested; the cadence and budget
for an instruction-review or observer experiment remain to be chosen. A
monitoring result proposes a bounded experiment rather than automatically
editing live instructions, installing software, or spending a large budget.
