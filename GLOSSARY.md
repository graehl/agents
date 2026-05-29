# Glossary

Project-specific terminology — terms whose meaning here is distinct
from default agent usage. Topic-linked rows point to a
`topics/<name>.md` cross-cutting-concern doc.

See [`topics/glossary.md`](topics/glossary.md) for contribution and
regeneration rules.

| term | definition | topic / refs |
|---|---|---|
| ADR | (Architectural Decision Record) A bullet in a topic doc's `## Design decisions` section, format `**<decision>** (vs. <rejected alternative>): <rationale>`. The rationale must name both the trade-off accepted and the priorities the chosen path serves. Written when a decision is hard to reverse, would surprise a surface reviewer, or is genuinely trade-off-laden (any one; all judgment calls) | |
| `agent-instructions` | The repo's core correctness claim: committed global instructions give future agents stable, searchable policy across projects without relying on stale chat state | [agent-instructions](topics/agent-instructions.md) |
| `agentctl` | Dependency-free local job manager: process-group lifecycle, GPU/CPU resource gating, and on-disk run state under `.agentctl/`, with project-specific concerns delegated to plugins under `agentctl_plugins/` | [agentctl](topics/agentctl.md) |
| ambition framing | Instructing for a high bar while conveying trust in the agent's capability, which empirically unlocks above-default effort; distinct from pressure/fear framing, which underperforms it. The intended register for harsh-review's demanding stance — demanding content, trusting stance, not adversarial | [harsh-review](skills/harsh-review/SKILL.md) |
| `code judo` | A restructuring that preserves behavior while making the implementation materially simpler by reframing the problem — deleting whole branches, layers, or concepts rather than rearranging them | [harsh-review](skills/harsh-review/SKILL.md) |
| `design-thinking` | Principles for approaching a change or problem before and during implementation — reframe before patching, map before drilling, hypotheses over traces | [design-thinking](topics/design-thinking.md) |
| `debugging` | Disciplined diagnosis: build a fast deterministic feedback loop before hypothesising, generate ranked falsifiable hypotheses, tag debug instrumentation `[DEBUG-xxxx]` for one-grep cleanup, and write the regression test at a correct seam — or record the seam's absence as the finding | [debugging](topics/debugging.md) |
| divergence point | An intentional duplication where the copies are expected to evolve independently; justifies keeping separate code rather than consolidating it behind a shared function with mode/flag arguments | [harsh-review](skills/harsh-review/SKILL.md) |
| `evidence-ledger` | An optional, append-only `<topic>.evidence.md` companion to a topic doc — agent-owned space for notes that help maintain accurate knowledge and good behavior on the topic | [evidence-ledger](topics/evidence-ledger.md) |
| full gate record | Big-effect-gate tier for irreversible or shared-state actions; requires the numbered record block (action, checks, command) before running | |
| `glossary` | Project-specific terminology lives in `GLOSSARY.md` at repo root: one sorted table whose topic-linked rows are autopopulated from `topics/<name>.md` ledes and whose vernacular rows are curated | [glossary](topics/glossary.md) |
| `goal-distillation` | Training a goal-conditioned agent from goal-annotated sessions: the goal's testable done-condition serves as the verifier/reward, process labels keep the agent from gaming that reward, and a strong teacher or self-critique installs integrity a prompt can only request | [goal-distillation](topics/goal-distillation.md) |
| handoff message | First-turn context-dump from another agent or compaction event; signals that `/bye` did not run and `last-session.md` is probably stale | |
| interruptible checkpoint | Brief visible statement of the agent's current interpretation, branch choice, or assumption; invites correction only if wrong, continues at normal pace as if no correction will arrive | |
| `lede` (topic-doc) | The `> ` blockquote line(s) immediately after a topic doc's H1; canonical one-sentence definition consumed by glossary regeneration | |
| `light check` | Big-effect-gate tier for cheaply reversible local actions (commits, amends): one-line confirmation of staged scope, no full gate record | |
| leaky abstraction | An abstraction whose callers must understand the underlying implementation to use it correctly; the encapsulation boundary fails in practice even if it exists syntactically (Spolsky) | [harsh-review](skills/harsh-review/SKILL.md) |
| load-bearing instruction | An entry in the global instructions whose presence demonstrably steers agent behavior beyond what a capable agent does by default; non-load-bearing entries are candidates for cutting | |
| prompt debt | Accumulated instruction text that replaces ordinary engineering judgment rather than preventing a specific known failure; a smell when proposing new entries | |
| `prototyping` | Throwaway code that answers one specific question. One command to run, no persistence, no polish, state surfaced after every action, deleted or absorbed when done — with the answer captured durably | [prototyping](topics/prototyping.md) |
| `provenance-tracking` | What run produced an output, what its inputs were, what to rerun to regenerate it, and what's changed since the last good run | [provenance-tracking](topics/provenance-tracking.md) |
| `research-survey` | How the project surveys an active research field and maps its frontier; governs `survey-field.md`, `research-frontier.md`, and the `surveys/` artifact tree | [research-survey](topics/research-survey.md) |
| `runs-ledger` | An optional `<topic>.runs/` subdir holding curated run records — typically agentctl artifacts — and a developer-facing README that indexes them and explains which still inform `<topic>.md` | [runs-ledger](topics/runs-ledger.md) |
| seam | A natural boundary in code where behavior can be altered or structure split without editing the surrounding code; low-cost decomposition and substitution points. When a diff touches a seam, the threshold for demanding restructuring now drops | [harsh-review](skills/harsh-review/SKILL.md) |
| `software-aesthetic` | Shared criteria for how code should look, feel, and be structured — applied both when writing code and when reviewing it. Universal rules in the main doc; coordinated (project-wide) rules in the companion | [software-aesthetic](topics/software-aesthetic.md) · [coordinated](topics/software-aesthetic.coordinated.md) |
| sketch | A prototype-stage exploration captured for later: what was considered, why it is not the current path, and what would change the answer. Lives in a topic doc's `## Sketches` section. Distinguished from an ADR by lack of commitment — touchpoints are still easy to modify, and we expect more knowledge later to inform the final pick | |
| spaghetti | Ad-hoc conditionals, mode flags, or special-case branches scattered across unrelated flows rather than contained in a dedicated abstraction | [harsh-review](skills/harsh-review/SKILL.md) |
| task file | Git-ignored `tasks/NNN-<name>.md` tracking per-feature progress, decisions, and dated status notes; the source of truth on resume after recovery from live worktree state | |
| `testing` | Vertical-slice TDD: one test → minimal code to pass → next test. Tests verify behavior through public interfaces and survive internal refactor; mocking is for system boundaries, not internal collaborators | [testing](topics/testing.md) |
| topic doc | A committed `topics/<name>.md` file naming a cross-cutting concern's contracts, invariants, assumptions, and edge cases | |
| topic trailer | A `Topic: <name>` git-commit trailer marking thread membership in a related commit series; `<name>` is the basename of `topics/<name>.md` | |
