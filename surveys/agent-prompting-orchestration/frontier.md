# Frontier: agent prompting and orchestration

Mode: **recall**, inherited from `survey.md` (pretrained recall + light web
search 2026-08-15; anchors verified to exist, none read). Per
`frontier-map.md`, a recall-mode frontier pass is brainstorming-grade: every
candidate below is speculative, and the falsification gate has not run in
`grounded` mode. Entry fields say `unknown (unread)` where only a search
snippet has been seen.

## Provisional claim inbox

All revisit dates are unscheduled reminders, not `at/` entries: the grounded
pass is already the program's queued next work item.

### SkillTriage — "Agent Skills Can Be Harmful" (arXiv 2608.11888, unread)

- Claim as surfaced: post-hoc triage of skill-induced agent failures;
  predicts failure categories and returns contrastive evidence over
  target-vs-reference trajectory divergence.
- Incumbent: manual failure triage. Regime/benchmark, train/eval control,
  independent evaluation: unknown (unread).
- Relevance: nearest mechanism neighbor to the diagnosis program's stage-2
  attribution; surfaced as single-scaffold — the differentiation claim
  rests on that unverified characterization.
- Cheapest discriminating check: read the method section — does it
  attribute to instruction text (clauses) or only to skill modules, and
  does it repair anything?
- Revisit: grounded pass (reminder 2026-09-15).

### Harness-induced belief divergence (arXiv 2607.04528, unread)

- Claim as surfaced: measures belief divergence induced by harness/config
  in multi-step agents; much divergence originates in a trajectory's first
  steps.
- Relevance: confound control for stage 1 — if harness differences dominate
  divergence, corpus attribution must hold harness fixed or model the
  residual; the protocol's "same harness conventions where possible" needs
  this quantified.
- Cheapest discriminating check: is the instruction corpus held fixed while
  harness varies, and how large is the harness term?
- Revisit: grounded pass (reminder 2026-09-15).

### Behavioral reproducibility (arXiv 2605.28840, unread)

- Claim as surfaced: measures run-to-run consistency of multi-step
  tool-calling agents.
- Relevance: within-model self-divergence is the noise floor under
  cross-model divergence — a divergence is signal only above it. Motivates
  the same-producer rerun control now named in the proposal's pilot.
- Cheapest discriminating check: reported variance magnitudes per model
  and step depth.
- Revisit: grounded pass (reminder 2026-09-15).

### Black-box system-prompt forensics (arXiv 2606.22698, unread)

- Claim as surfaced: black-box attribution of system prompts works in
  binary settings, degrades when semantic intent is preserved.
- Relevance: bounds what output-only attribution can recover; supports the
  program's white-box choice (transcript read traces + producer forks) over
  judge-from-outputs variants.
- Cheapest discriminating check: their task definition vs clause-cited
  attribution against a known corpus.
- Revisit: grounded pass (reminder 2026-09-15).

### GEPA — reflective prompt evolution (arXiv 2507.19457, ICLR 2026 oral, unread)

- Claim as reported by authors: outperforms GRPO by ~6% average with up to
  35× fewer rollouts, MIPROv2 by >10%. Self-reported; independent
  evaluation unknown.
- Relevance: optimization-side neighbor; also a candidate component —
  GEPA-style reflection could draft stage-4 patch text, with the program
  supplying what GEPA lacks (cause attribution, cross-model evidence, a
  shared maintained corpus as the object).
- Cheapest discriminating check: does its reflection attribute causes, or
  only mutate and score?
- Revisit: grounded pass (reminder 2026-09-15).

### PromptExp — prompt-component attribution (arXiv 2410.13073, unread)

- Claim as surfaced: multi-granularity attribution of a single model's
  output to prompt components.
- Relevance: granularity precedent for chapter-and-verse citation;
  single-model, no repair routing.
- Cheapest discriminating check: component granularity (token/sentence/
  section?) vs clause citation; any corpus-maintenance loop?
- Revisit: grounded pass (reminder 2026-09-15).

## Void map

Axes as in `survey.md` (object × mechanism × signal), abbreviated to the
decision-relevant cells:

- {scaffold × attribute × trajectory} — `filled`/`in-progress`: the
  F cluster above (existence verified, content unread).
- {single prompt × optimize × outcome} — `filled`: B1–B3.
- {any × aggregate × outcome} — `filled`: C (the consensus foil).
- {corpus × measure × outcome} — `filled` at prompt granularity (A1–A3);
  corpus-granularity measurement is the instruction-ablation plan
  (`topics/instruction-ablation.md`), in-repo, not yet run.
- {shared corpus × attribute + repair × trajectory, heterogeneous
  producers} — `untried` as far as recall + light search shows: the
  `research/differential-instruction-diagnosis` cell. Why plausibly
  unexplored: presupposes a maintained multi-file corpus with per-model
  supplements, session-continuation access to producer reasoning, and
  willingness to run a competitor's model on one's own corpus.

## Falsification gate

`prior-art-checked:` recall-mode light search only, 2026-08-15, three
queries recorded in `survey.md` §Disconfirming pass; no hit on the claimed
cell; nearest work is the F cluster. **Gate not passed** — grounded
snowball from anchors {GEPA, SkillTriage, PromptExp, a debate survey} plus
forward citations of the F cluster is required before the void becomes an
established candidate.

## Capstone candidate (speculative)

One candidate: the diagnosis-program cell above.

- Impact: would give corpus maintenance a measured evidence stream —
  exactly the ablation-by-model/harness the repo charter already prefers —
  and populate the model-supplement layer systematically.
- Tractability: high — producers, transcripts, session forks, and the
  supplement routing all exist in this repo's tooling; the missing piece is
  the orchestration script and paging tool.
- Novelty-confidence: `speculative` (gate not passed; recall cap).
