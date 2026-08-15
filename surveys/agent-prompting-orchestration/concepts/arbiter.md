# Arbiter — static cross-vendor audit of agent-CLI system prompts

Read method: prompted extraction over the arXiv HTML full text, 2026-08-15.
Full text: [HTML](https://arxiv.org/html/2603.08993v1) ·
[PDF](https://arxiv.org/pdf/2603.08993) ·
[local extract](../related-work/extract/arbiter2026/html/2603.08993.md)
(git-ignored; rebuild with `related-work fetch`). arXiv 2603.08993.

**What it is.** Static analysis of vendor agent-CLI system prompts (Claude
Code, Codex CLI, Gemini CLI) for internal contradictions — e.g. one section
mandating a tool another prohibits. Two phases: directed rule evaluation
over classified blocks (56 blocks for Claude Code) with an AST of typed
nodes (Document → Section → Directive) and semantic roles, and an
undirected multi-model "scourer" pass with convergent termination (three
consecutive models declining to continue). "Cross-vendor" means each
vendor's prompt is analyzed separately; different LLMs serve as diverse
auditors, not as producers being compared.

**Results.** 152 scourer findings across three prompts; 21 hand-labeled
patterns in Claude Code; prompt architecture predicts failure class
(monolithic → boundary contradictions; modular → composition-seam bugs;
flat → capability/consistency trade). One Gemini CLI finding (memory
compression data loss) externally validated by a Google patch. Total cost
$0.27.

**Relation to the diagnosis program.** Complementary, not competing: static
contradiction audit of prompt text with no task trajectories, no
behavioral-divergence signal, no repair. Two direct borrowings: multi-model
auditor diversity is measured precedent for the stage-3 cross-audit's
diverse-lens design, and "modular architectures exhibit composition-seam
bugs" bears on this repo's own routed-packet corpus. Its analyzed objects
literally include the Claude Code system prompt this repo's sessions run
under.
