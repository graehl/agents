# Glossary — differential instruction diagnosis

Program-scoped vocabulary; governs every document under this directory.
Parent chain: `~/agents/GLOSSARY.md`.

| term | definition | topic / refs |
|---|---|---|
| differential instruction diagnosis | The program's protocol: two different-lab frontier models run the same task under the identical boot corpus; their output divergences are attributed to cited corpus text and converted into instruction patches. "Differential" is deliberately overloaded: the two-substantially-different-models contrast pair, the difference-derived evidence (performance and how the instructions bore on each), and the medical-sense per-divergence diagnosis; software differential testing is stage 1's structural ancestor | [proposal](proposal.md) |
| boot corpus | The instruction set under test: `AGENTS.global.md`, its routed packets (`_RESEARCH/`, `_RUNS/`, `AGENTS/`), and the harness/model supplements loaded for a session | [proposal](proposal.md) |
| producer session | One of the two sessions that performs the task under the corpus; its transcript is the raw evidence | [proposal](proposal.md) |
| attribution fork | A continuation of a producer session branched from its post-answer state, used for divergence attribution; retains whatever access the provider grants to the session's own reasoning trace | [proposal](proposal.md) |
| pre-registered self-account | The attribution fork's first-turn private account of its key decisions and their drivers, recorded before any peer material enters its context; anchors the attribution pass and gives the cross-audit a consistency check | [proposal](proposal.md) |
| read-trace diff | Mechanical comparison of which corpus files/sections each producer actually opened (logged tool calls), run before any introspective attribution; the transcript-objective trust floor | [proposal](proposal.md) |
| chapter-and-verse attribution | An attribution that cites the specific corpus clause it blames, checkable against the corpus text and the read traces | [proposal](proposal.md) |
| divergence verdict | Per-divergence classification: shared-clause ambiguity (both read the same clause differently), differential salience (one followed a clause the other never surfaced), or model prior (no clause applies — a first-class verdict, not a failure to cite) | [proposal](proposal.md) |
| session-class patch | A proposed amendment to a model-scoped supplement (`AGENTS.anthropic.md`-style) correcting one model family's reading of the corpus | [proposal](proposal.md) |
| benefiting-both patch | A proposed amendment to the shared corpus that both producers' evidence supports | [proposal](proposal.md) |
| answer-revision stage | Organic-task option: the attribution fork is offered a revision of its original answer informed only by the attribution exchange, never by the proposed instruction patches; convergence behavior doubles as validation of the attribution | [proposal](proposal.md) |
| incentive-neutrality norm | The scripted orchestration statement that the protocol diagnoses the corpus, that supplement patches are corrections rather than demerits, and that self- or lab-flattering attribution is a protocol violation | [proposal](proposal.md) |
