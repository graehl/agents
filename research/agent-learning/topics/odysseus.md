# Odysseus

> The PewDiePie-associated self-hosted workspace and community, evaluated for memory, skills, and review practice.

Topic: research/agent-learning/odysseus

## Contribution to the program

Odysseus supplies a useful comparison for explicit memory/skill management and
review. The [memory and skills specification at `88772b3`](https://github.com/odysseus-dev/odysseus/blob/88772b3278183949413e9da7d57e741057302e5e/specs/memory-skills.md)
describes JSON-backed facts with pinned state and keyword matching, optional
Chroma/embedding retrieval, LLM extraction/consolidation, and skill audit and
publication machinery. These documented mechanisms merit isolated tests; we
have not reproduced a task-performance benefit.

| Program capability | Our judgment |
|---|---|
| Pinned plus retrieved memories | Useful contrast with always-loaded boot and explicit lazy-read routes; measure irrelevant injection and outdated facts. |
| Skill extraction from conversations | Candidate automatic accumulation for later human review, with provenance back to the original episode. |
| With/without-skill audits and worker/teacher revision | More relevant than judging a skill's prose alone; inspect task independence, judge bias, cost, and fresh-task transfer before trusting promotion. |
| User controls and publication gates | Useful design reference for graehl's manual criteria review of accumulated material. |
| Community memory variants | Source of independent experiments; treat proposed forks separately from shipped core. [TRACE](trace.md) has its own topic. |

## Additional orthogonal capabilities

The [pinned README](https://github.com/odysseus-dev/odysseus/blob/88772b3278183949413e9da7d57e741057302e5e/README.md)
describes a broader workspace:

| Capability | Our judgment |
|---|---|
| Hardware-aware local-model cookbook, downloads, and serving | Useful for cheap local observer experiments if quality and hardware costs work; not itself evidence for memory. |
| Blind model comparison and synthesis | Potential source of task-evaluation UX and diverse hard-task attempts. Check independence and selection costs. |
| Multi-step web research | Could assist monthly evidence discovery; source-reading quality matters more than report fluency. |
| Document editor, email, notes, tasks, calendar/CalDAV | Orthogonal personal-workspace integration; no current reason to migrate graehl's workflow for this program. |
| Image/gallery features, themes, uploads, and account controls | Product completeness rather than a learning mechanism; low priority here. |
| Local/API chat, shell, files, and MCP | Execution substrate; inspect the specific Codex/MCP route before assuming subscription parity with native local/API behavior. |

## Next evidence and implementation transfer

Start with a reproducible skill-audit example using held-out tasks and a
no-skill control. Include automatic extraction and audit cost, then compare
human-approved publication with automatic promotion. The same experiment can
operate over `~/agents` candidates without adopting Odysseus's full workspace.

Watch [the canonical repository](https://github.com/odysseus-dev/odysseus) and
its linked community for traces and replications. The earlier
`pewdiepie-archdaemon/odysseus` address redirects there. Community enthusiasm,
model releases, and software feature breadth do not substitute for the
program's two outcome/cost criteria.
