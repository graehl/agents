# TRACE

> A community memory-tree approach associated with Odysseus, evaluated for selective context and changing instructions.

Topic: research/agent-learning/trace

## Contribution to the program

The [author's community account](https://www.reddit.com/r/learnmachinelearning/comments/1tygbhe/i_built_a_selfreorganizing_memory_tree_for/)
describes hierarchical topic paths, freezing/summarizing inactive branches, and
selecting active context before inference. It claims about 30% fewer tokens
per turn and negligible context bloat. Those claims motivate a replication
with quality and total maintenance cost; they do not yet establish a saving
for our workload or elimination of stale instructions.

The account links [standalone TRACE](https://github.com/husain34/TRACE) and
[an Odysseus fork](https://github.com/husain34/odysseus-trace). A related
[hierarchical-memory PR](https://github.com/odysseus-dev/odysseus/pull/3730)
is a separate implementation lead, not proof that the proposal ships in core.

Our judgment: selective context under rapidly changing rules is a worthwhile
small stress test. Compare with explicit current-rule replacement, ordinary
compaction, and retrieval from raw history. Measure forgotten obligations,
wrong-rule use, task success, and the tokens spent constructing the tree.

## Additional orthogonal capabilities

The cited account establishes no separate workspace, scheduler, or execution
advantage for TRACE. An Odysseus fork may inherit those capabilities; their
applicability belongs in the [Odysseus topic](odysseus.md). Native/local
operation in the related PR is a deployment property to verify, not a memory
quality result.

## Subscription transfer and next evidence

Whole-history reconstruction can require control that an additive boot message
or MCP tool does not provide. A selected-context file plus injected pointer is
a plausible partial implementation; it cannot promise to remove history
already retained by the harness. Test actual context size and correctness in
the supported host before claiming equivalent token savings.

Prioritize public traces, reproducible tasks, and current implementation
status. Independent replication with an equal-budget simple baseline would
make this actionable; a tree visualization or smaller prompt alone would not.
