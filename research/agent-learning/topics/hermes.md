# Hermes

> Nous Research's agent runtime and community, evaluated for experience reuse and subscription-compatible transfer.

Topic: research/agent-learning/hermes

## Contribution to the program

Hermes packages persistent facts, skill files, session search, and background
review into one runtime. Our present interest is the cheap retrieval baseline
and the review machinery as independently testable components, rather than a
wholesale harness change. Source inspection below is pinned to
[`86fa9e6`](https://github.com/NousResearch/hermes-agent/tree/86fa9e6ca1de7ee71132d2be0103f3e37d1fa872);
it supplies candidate mechanisms, not measured improvement on our tasks.

| Mechanism | What it offers | Applicability judgment |
|---|---|---|
| Bounded persistent memory | Session-start snapshots of MEMORY.md and USER.md, maintained by the agent. | Cheap comparison with existing boot/routed facts; test staleness and recurring context cost. |
| Session search | SQLite FTS5/BM25 lexical retrieval, lineage handling, automation demotion, and anchored transcript excerpts. | Strong first baseline for recovering tools/skills and failures from prior work. This built-in search is not an embedding semantic engine. |
| Skills and background review | Separate review can persist reusable procedures and revise skills. | Test against raw retrieval before paying to summarize every task. Generated artifact counts do not establish usefulness. |
| External memory providers | Integration can add semantic retrieval and inferred user models, including [Honcho](honcho.md). | Attribute gains to the provider and its added inference, not automatically to Hermes core. |

The inspected [session-search implementation](https://github.com/NousResearch/hermes-agent/blob/86fa9e6ca1de7ee71132d2be0103f3e37d1fa872/tools/session_search_tool.py)
performs no LLM summarization call, despite the README's summarization claim.
Search semantics live in
[`hermes_state_search.py`](https://github.com/NousResearch/hermes-agent/blob/86fa9e6ca1de7ee71132d2be0103f3e37d1fa872/hermes_state_search.py).

## What triggers review

At the inspected revision, counters mark review due: memory review defaults
to ten turns, skill review to ten loop iterations. Finalization dispatches
eligible review after a final answer, with interruption and automated-run
guards. Optional idle deferral/coalescing concerns when background work runs.
This does not establish that a semantic task has ended or that a separate
agent first judged review worthwhile. Review prompts favor finding something
to save; compare that bias with explicit permission to conclude no update is
useful. Relevant owners are
[`turn_context.py`](https://github.com/NousResearch/hermes-agent/blob/86fa9e6ca1de7ee71132d2be0103f3e37d1fa872/agent/turn_context.py),
[`turn_iteration_prep.py`](https://github.com/NousResearch/hermes-agent/blob/86fa9e6ca1de7ee71132d2be0103f3e37d1fa872/agent/turn_iteration_prep.py),
[`turn_finalizer.py`](https://github.com/NousResearch/hermes-agent/blob/86fa9e6ca1de7ee71132d2be0103f3e37d1fa872/agent/turn_finalizer.py), and
[`background_review.py`](https://github.com/NousResearch/hermes-agent/blob/86fa9e6ca1de7ee71132d2be0103f3e37d1fa872/agent/background_review.py).

## Additional orthogonal capabilities

The [pinned README](https://github.com/NousResearch/hermes-agent/blob/86fa9e6ca1de7ee71132d2be0103f3e37d1fa872/README.md)
advertises the following facilities. Their applicability judgments concern our
workflow, not comparative product quality.

| Capability | Our judgment |
|---|---|
| Messaging gateway and voice transcription | Useful if unattended work must meet the user in messaging apps; not evidence of learning, and not a reason to replace YA. |
| Cron and result delivery | Relevant implementation reference for periodic observers and monitoring; scheduling utility is independent of memory quality. |
| Local, container, SSH, and hosted execution backends | Potentially useful for remote work; adoption needs a concrete execution requirement. |
| Delegation and scripted tool orchestration | Candidate hard-task infrastructure; compare against ordinary diverse attempts at matched cost. |
| Terminal UI and broad provider/tool integration | Convenience and portability; migration burden must earn its cost. |
| Batch trajectories and training-data tooling | Relevant if the program later studies model training; outside the initial context/instruction experiments. |

## Subscription transfer and next evidence

Hermes's [Codex app-server runtime documentation](https://hermes-agent.nousresearch.com/docs/user-guide/features/codex-app-server-runtime)
describes a compatibility path with narrower tool support than its native
loop. Restrictions on foreground memory/session-search/delegation in that
integration should be checked against current code before adoption; they do
not prove those capabilities impossible through a different MCP/host design.

Candidate transfer: expose local session retrieval as a tool, let boot route
its use, and have YA dispatch a separate bounded reviewer at a measured
boundary. Test foreground selection versus pre-injection before assuming that
moving relevance reasoning out of the conversation helps. Watch the
[repository](https://github.com/NousResearch/hermes-agent), its linked Nous
community, and reproducible evaluations for outcome gains after all review
costs, including negative results and stale-memory regressions.
