# HarnessFix — trace-guided diagnosis and repair of agent harnesses

Read method: prompted extraction over the arXiv HTML full text, 2026-08-15.
Full text: [HTML](https://arxiv.org/html/2606.06324v2) ·
[PDF](https://arxiv.org/pdf/2606.06324) ·
[code](https://github.com/HarnessFix/HarnessFix) ·
[local extract](../related-work/extract/harnessfix2026/html/2606.06324.html)
(git-ignored; rebuild with `related-work fetch`). arXiv 2606.06324.

**What it is.** A framework that compiles raw execution traces plus harness
artifacts into a Harness-aware Trace Intermediate Representation (HTIR) —
step-level data-flow/control-flow aligned with the artifacts that shaped each
step — then attributes failures to a harness layer and applies scoped repair
operators. Seven-layer harness model (execution env, tools, context,
lifecycle, observability, verification, governance); artifacts include
prompt templates, tool specs, orchestration code, configs.

**Signal and validation.** Diagnostic signal is failed trajectories of one
agent system (primary model GPT-5 mini; five LLMs tested overall).
Validation is regression-aware: a patch must reduce its target flaw while
staying within regression limits on held-out validation tasks. Gains
6.3–18.4% over initial harnesses on GAIA, SWE-bench Verified, AppWorld,
Terminal-Bench 2.0; beats human-designed and self-evolution baselines.

**Relation to the diagnosis program.** Nearest attribute+repair neighbor:
it closes a diagnose→patch loop whose blamable artifacts include
instruction text, with validation stronger than end-to-end scoring. It does
not use divergence between heterogeneous models as signal (failures only —
requires a failure, where divergence also works on organic tasks with no
ground truth), has no shared cross-model corpus or model-scoped routing,
and no producer-side introspective evidence — the diagnosis is fully
external/mechanical over the trace.
