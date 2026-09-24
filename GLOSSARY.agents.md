# Agent glossary

Read this file in full at project entry, and a scope's own copy on entering
that scope. When it exists, agents read it instead of `GLOSSARY.md`, which is
the human-facing glossary (a tooltip inventory plus definitions the user wants
help recalling) and may carry material inert for agents.

Two kinds of row. A **Governs:** row names an activity and the topic that
governs it: read the topic before starting that activity. The trigger is the
activity, never an occurrence of the word. A sense row gives the meaning a
term carries here when it differs from standard usage; standard vocabulary is
omitted because it already works. Governs rows are regenerated from each
topic doc's `Governs:` line; sense rows are curated. Procedure:
`topics/glossary.md` § Agent glossary.

| term | sense or governs | read |
|---|---|---|
| `acli` | Governs: calling a tool that identifies itself as acli or declares acli capabilities | [acli](topics/acli.md) |
| `acli-implementer` | Governs: implementing an acli tool or library in any language | [acli-implementer](topics/acli-implementer.md) |
| `acli-spec` | Governs: specifying or verifying an acli tool's exact protocol | [acli-spec](topics/acli-spec.md) |
| active sessions | `.agentctl/active/<session-id>` status files, one per working agent: line 1 present-tense gist, optional `scope:` line, `DONE` prefix when complete; read by `agentctl others`. | [agentctl](topics/agentctl.md) |
| ADR | A bullet in a topic doc's `## Design decisions` section: `**<decision>** (vs. <rejected alternative>): <rationale>`, naming the trade-off accepted. | |
| `agent-guard` | Governs: launching agents in a shared worktree or diagnosing a guard block | [agent-guard](topics/agent-guard.md) |
| `agent-instructions` | Governs: writing or editing agent instructions, supplements, skills, or instruction topics | [agent-instructions](topics/agent-instructions.md) |
| `AGENT_ENV_VARS` | Governs: reading or setting launcher, harness, session, or guard environment variables | [AGENT_ENV_VARS](topics/AGENT_ENV_VARS.md) |
| `agentctl` | Governs: changing or diagnosing active-session or run semantics, staleness, launch-depth guards, or plugins | [agentctl](topics/agentctl.md) |
| `almanac` | Governs: building, repairing, or querying an almanac dataset from a web page | [almanac](topics/almanac.md) |
| ambition framing | Instructing for a high bar while conveying trust in the agent's capability; the intended register for harsh review, as opposed to pressure framing. | [harsh-review](skills/harsh-review/SKILL.md) |
| `at-scheduling` | Governs: creating or changing an /at future-run entry | [at-scheduling](topics/at-scheduling.md) |
| autoresearch | Asking an agent to occupy the GPU to refine or choose research directions, not merely execute a plan; presupposes a non-cheatable success criterion. | [research workflow](_RESEARCH/workflow.md) |
| `backward-compat` | Governs: breaking or shimming a public API, CLI flag, wire format, or persisted schema | [backward-compat](topics/backward-compat.md) |
| `blog-post-writing` | Governs: writing a technical or research blog post for a static site | [blog-post-writing](topics/blog-post-writing.md) |
| `claim-provenance` | Governs: citing evidence in a manuscript, verifying its claims, or moving its run records | [claim-provenance](topics/claim-provenance.md) |
| code map | A regenerable developer-facing orientation report over a codebase's structure, flows, seams, and refresh commands; not a topic doc. | [code-map](code-map/README.md) |
| `codex-session` | Governs: recovering Codex session identity or waiting on owned jobs under Codex | [codex-session](topics/codex-session.md) |
| `commits` | Governs: writing a non-trivial commit message, amending, rewriting history, or choosing trailers | [commits](topics/commits.md) |
| concepts/ | A survey's per-paper concept digests under `surveys/<field>/concepts/`, the primary artifact reasoned on. | [research-survey](topics/research-survey.md) |
| contributing-model trailer | `Contributing-model: <short name>` commit trailer, one per model, from harness-recorded identity; replaces the forbidden `Co-Authored-By` and is never stripped. | [commits](topics/commits.md) |
| `cpp` | Governs: first editing C or C++ in a repo | [cpp](topics/cpp.md) |
| `debugging` | Governs: diagnosing a defect or slow or stalled behavior | [debugging](topics/debugging.md) |
| `degradation-injection` | Governs: stress-testing worker queues or async boundaries with injected slowdowns or faults | [degradation-injection](topics/degradation-injection.md) |
| deleting reframe | A behavior-preserving restructure that deletes whole branches, layers, or concepts by reframing the problem. | [harsh-review](skills/harsh-review/SKILL.md) |
| `design-thinking` | Governs: approaching a non-trivial change before and during implementation | [design-thinking](topics/design-thinking.md) |
| director, steward (on-deck) | Director owns priority, guards, and launch commands for ratified on-deck entries; steward services eligible work and may launch preemptible speculative runs. | [on-deck](topics/on-deck.md) |
| divergence point | An intentional duplication whose copies are expected to evolve independently; not a consolidation target. | [harsh-review](skills/harsh-review/SKILL.md) |
| `document-annotation` | Governs: building or running fixed-prompt segmented-document annotation | [document-annotation](topics/document-annotation.md) |
| `document-writing` | Governs: choosing the source of truth and renderer for a research document | [document-writing](topics/document-writing.md) |
| `document-writing-browser-interactive` | Governs: rendering a research document as interactive static HTML | [document-writing-browser-interactive](topics/document-writing-browser-interactive.md) |
| `document-writing-figures` | Governs: a paper, handout, report, or blog asks for a graph, diagram, or rich table | [document-writing-figures](topics/document-writing-figures.md) |
| `document-writing-printable` | Governs: producing a PDF or LaTeX submission package from a research document | [document-writing-printable](topics/document-writing-printable.md) |
| `doubt-skill` | Governs: /doubt, or explicit distrust of a just-applied conclusion | [doubt-skill](topics/doubt-skill.md) |
| duplicate fix | A second independent remediation of a defect the tree already handles; consolidate to one fix at the owning invariant. | [harsh-review](skills/harsh-review/SKILL.md) |
| `editing-long-docs` | Governs: editing a long document where section-wise reads, regrouping, or moving matter | [editing-long-docs](topics/editing-long-docs.md) |
| `evidence-ledger` | Governs: appending to or creating a topic's .evidence.md | [evidence-ledger](topics/evidence-ledger.md) |
| `explanation-style` | Governs: the user says "remind me" or "refresher" before a named concept | [explanation-style](topics/explanation-style.md) |
| `frontier-capability-review` | Governs: reevaluating a capability-sensitive instruction as models improve | [frontier-capability-review](topics/frontier-capability-review.md) |
| full gate record, light check | Big-effect-gate tiers: the numbered record block for irreversible or shared-state actions; a one-line staged-scope confirmation for local commits and amends. | |
| `functional-layout` | Governs: deciding how a screen should look: layout, alignment, spacing, focal point | [functional-layout](topics/functional-layout.md) |
| `glossary` | Governs: adding, sorting, promoting, or regenerating glossary rows, or creating a scoped glossary | [glossary](topics/glossary.md) |
| `handling-bug-reports` | Governs: a new or unrelated defect report arrives | [handling-bug-reports](topics/handling-bug-reports.md) |
| `handoffs` | Governs: creating or updating a handoff | [handoffs](topics/handoffs.md) |
| `handout-writing` | Governs: writing or revising a research handout | [handout-writing](topics/handout-writing.md) |
| `helper-scripts` | Governs: adding a helper to ~/bin or scripts/, or using queued-anchor or session-turn | [helper-scripts](topics/helper-scripts.md) |
| `instruction-ablation` | Governs: measuring whether an instruction change helps | [instruction-ablation](topics/instruction-ablation.md) |
| interruptible checkpoint | A brief visible statement of the current interpretation or branch choice that invites correction only if wrong and continues without waiting. | |
| leaf (subagent) | A depth-1 delegated agent that reports to its creator and cannot spawn; may be re-engaged across turns. | |
| lede (topic-doc) | The `> ` blockquote lines after a topic doc's H1; the definition consumed by glossary regeneration. | [topic-doc-format](topics/topic-doc-format.md) |
| load-bearing instruction | An instruction whose presence demonstrably steers behavior beyond a capable agent's default; others are cut candidates. | |
| `on-deck` | Governs: servicing, authoring, or ratifying on-deck queue entries; tending | [on-deck](topics/on-deck.md) |
| paper form | The governing expository lens and reader promise that controls a paper's abstract, section order, and cadence; independent of discovery value. | [successful-paper-forms](topics/successful-paper-forms.md) |
| `paper-attractiveness` | Governs: deciding what makes a paper attractive beyond its form | [paper-attractiveness](topics/paper-attractiveness.md) |
| `paper-drafting` | Governs: turning program evidence into paper proposals or promoting one to a draft | [paper-drafting](topics/paper-drafting.md) |
| `paper-reviewer` | Governs: reviewing a proposed or drafted paper against program evidence | [paper-reviewer](topics/paper-reviewer.md) |
| `paper-writing` | Governs: writing a selected research paper | [paper-writing](topics/paper-writing.md) |
| `pareto-figures` | Governs: making a quality-versus-cost Pareto figure | [pareto-figures](topics/pareto-figures.md) |
| path-trace | Attach provenance from this session's tool output to a claim about project code, or mark the claim unverified; no third register. | |
| `pdf` | Governs: reading or extracting a PDF | [pdf](topics/pdf.md) |
| `perf` | Governs: benchmarking, profiling, or load simulation on a shared host | [perf](topics/perf.md) |
| `plan-grilling` | Governs: the user says "grill" about a plan or design | [plan-grilling](topics/plan-grilling.md) |
| program instructions, program scope, self-rooted program | Binding rules under a `PROGRAM.md` heading `Program instructions`, the subproject it declares, and the `Program root: self` marker that stops parent inheritance there. | [TOPICS](TOPICS.md) |
| `progress-report` | Governs: writing a dated research progress report | [progress-report](topics/progress-report.md) |
| prompt debt | Instruction text that replaces ordinary judgment rather than preventing a specific known failure. | |
| `prototyping` | Governs: writing throwaway code to answer one question | [prototyping](topics/prototyping.md) |
| `provenance-tracking` | Governs: recording what run produced an output and how to regenerate it | [provenance-tracking](topics/provenance-tracking.md) |
| `python` | Governs: first editing Python in a repo | [python](topics/python.md) |
| related-work | A survey's `related-work/` directory and the shared `scripts/related-work` engine that owns it; a survey-local fetch script is a defect. | [research-survey](topics/research-survey.md) |
| research advisor | The long-lived program-scoped advisor under `research/<program>/advisor/`; "tell advisor" delivers a packet, "ask advisor" obtains a response before the named decision. | [advisor serve](advisor/serve.md) |
| research program | A durable line of inquiry declared by `research/<program>/PROGRAM.md`, whose sibling `GLOSSARY.md` governs that subtree. | [research artifacts](_RESEARCH/artifacts.md) |
| `research-blog-writing` | Governs: writing a research blog post that showcases one result | [research-blog-writing](topics/research-blog-writing.md) |
| `research-survey` | Governs: surveying a research field, mapping its frontier, or fetching related work | [research-survey](topics/research-survey.md) |
| `research-writing` | Governs: writing anything that makes research claims: prior art, attribution, citations | [research-writing](topics/research-writing.md) |
| `result-visualization-templates` | Governs: choosing a results layout before picking a plotting package | [result-visualization-templates](topics/result-visualization-templates.md) |
| rider | A topic doc's unloaded companion (`.evidence.md`, `.runs/`, `.bearings.md`, `.testing.md`, `.sketches.md`), read on demand. | [topic-doc-format](topics/topic-doc-format.md) |
| `runs-ledger` | Governs: curating run records under a topic's .runs/ | [runs-ledger](topics/runs-ledger.md) |
| `shell` | Governs: first editing shell scripts in a repo | [shell](topics/shell.md) |
| sketch | A captured prototype-stage alternative that is not the current path, in `.sketches.md` or a `## Sketches` section; uncommitted, unlike an ADR. | |
| `soft-checks` | Governs: verifying generated output that has no exact expected value | [soft-checks](topics/soft-checks.md) |
| `software-aesthetic` | Governs: writing or reviewing code structure, naming, and boundaries | [software-aesthetic](topics/software-aesthetic.md) |
| `story-project-layout` | Governs: creating or reorganizing a story project's files | [story-project-layout](topics/story-project-layout.md) |
| `story-writing` | Governs: planning, drafting, or revising a story, screenplay, or character or world document | [story-writing](topics/story-writing.md) |
| `successful-paper-forms` | Governs: choosing a paper's governing expository form | [successful-paper-forms](topics/successful-paper-forms.md) |
| `technical-writing` | Governs: revising a handout, progress report, blog post, or paper for outside readers | [technical-writing](topics/technical-writing.md) |
| tend | Filling idle GPU with the next highest-research-value run; what the steward does. `/steward` and "tend on-deck jobs" are the same request. | [on-deck](topics/on-deck.md) |
| `testing` | Governs: writing or changing tests, or validating a behavior change | [testing](topics/testing.md) |
| `testing-rider` | Governs: creating or using a topic's .testing.md | [testing-rider](topics/testing-rider.md) |
| `theming` | Governs: adding or changing themes, dark mode, skins, or design tokens | [theming](topics/theming.md) |
| `tool-surprises` | Governs: /tool-surprises, or recurring tool or command failure patterns | [tool-surprises](topics/tool-surprises.md) |
| TOON | Token-Oriented Object Notation: declares a uniform array's length and fields once, then streams rows; read-side only, for large uniform tables. | |
| topic doc, topic-like, topic trailer | A formal `topics/` file owned by a glossary; any glossary term addressable as "the topic for X"; the `Topic: <name>` commit trailer marking series membership. | [topic-doc-format](topics/topic-doc-format.md) |
| `topic-doc-format` | Governs: creating or normalizing topic docs, companions, bearings, or epistemic labels | [topic-doc-format](topics/topic-doc-format.md) |
| `typescript` | Governs: first editing TypeScript or JavaScript in a repo | [typescript](topics/typescript.md) |
| `ui-design` | Governs: asked what a feature's UI should look like | [ui-design](topics/ui-design.md) |
| `ui-quality` | Governs: starting UI work in a project | [ui-quality](topics/ui-quality.md) |
| `ui-report` | Governs: producing a screenshot-backed UI report | [ui-report](topics/ui-report.md) |
| `ui-testing` | Governs: testing a web UI with rendered captures across viewports | [ui-testing](topics/ui-testing.md) |
| `ui-verification` | Governs: approving or verifying a UI change | [ui-verification](topics/ui-verification.md) |
| ungrounded survey | A survey requested as `light`, `recall`, or `ungrounded`: model-memory answer, no corpus, no artifact. Anything else is grounded and persists under `surveys/`. | [research-survey](topics/research-survey.md) |
| `vendoring` | Governs: copying third-party code or a skill to keep | [vendoring](topics/vendoring.md) |
| `verified-provenance` | Governs: row-wise translating, paraphrasing, or rewriting a dataset | [verified-provenance](topics/verified-provenance.md) |
| `web-digest` | Governs: updating the claude.ai preferences paste or web digest | [web-digest](topics/web-digest.md) |
| `workflow-tags` | Governs: adopting or emitting schema-announced workflow tags | [workflow-tags](topics/workflow-tags.md) |
| `writing` | Governs: drafting or revising prose for a reader | [writing](topics/writing.md) |
