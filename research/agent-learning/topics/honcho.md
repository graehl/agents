# Honcho

> Persistent peer modeling and reasoning over interaction history, evaluated as a memory component.

Topic: research/agent-learning/honcho

## Contribution to the program

[Honcho's overview](https://honcho.dev/docs/v3/documentation/introduction/overview)
describes background reasoning over stored messages to maintain representations
of persistent entities, queried for later context. That offers a candidate
beyond retrieving what a user explicitly said: inferring useful relationships
and reconciling evolving information. Its advantage over query-time reasoning
on retrieved raw episodes remains to be measured for our tasks.

Applicability is strongest for recurring preferences and cross-session facts.
For procedural task learning, compare inferred conclusions against original
episodes and check whether they actually improve tool/skill choice. A plausible
user model can be wrong; preserve provenance and test changed preferences.

## Additional orthogonal capabilities

The same overview describes a managed service, an open-source implementation,
and workspaces/peers/sessions/messages as storage primitives. Managed operation
may reduce maintenance, while self-hosting changes operational cost. Entity
modeling beyond the user may support applications outside this program; it
does not establish better coding or research outcomes. No application-specific
benefit is assumed from the storage abstraction alone.

## Subscription transfer and next evidence

External memory can be queried by a subscription-driven agent while its
background reasoning still incurs separate inference/service costs. An MCP
wrapper alone does not remove those costs. A candidate local alternative is
periodic review through a supported harness, storing conclusions and source
references in inspectable files; compare capability, delay, and quota use.

Follow the overview's evaluation links for reproducible tasks, costs, and
baselines. The next useful test compares inferred profiles with explicit facts
plus raw-session retrieval on recurring and changed-preference tasks. Retention
or recall claims need a separate check for task-level benefit.
