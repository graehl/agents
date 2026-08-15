# Frontier: agent prompting and orchestration

Mode: recall base + **grounded falsification slice 2026-08-15** — ten
anchor/neighbor papers read via prompted arXiv-HTML extraction and backed by
ten local searchable Markdown extracts (10 manifested / 10 verified / 10
grounded / 10 extracted; 5 concept digests), citers snowballed via Semantic
Scholar, and reframing queries run (survey §Disconfirming pass). Entries
below are read-backed unless marked existence-only; independent replication
is unchecked for all (grade cap `single-source`).

## Provisional claim inbox

Revisit dates are unscheduled reminders, not `at/` entries. Discriminating
checks recorded before the reads are answered inline; what remains open is
named per entry.

### SkillTriage — "Agent Skills Can Be Harmful" (arXiv 2608.11888)

- Read: single system (OpenCode + Claude Opus 4.6); contrastive
  target-vs-reference trajectories; attribution at skill-module
  granularity (88.8% subcategory accuracy); classification only, no
  repair; no shared-corpus or cross-model diagnosis.
- Check answered: attributes to skill modules, not instruction clauses;
  repairs nothing. Differentiation holds.
- Open: replication; whether follow-ups add repair. Revisit 2026-11.

### Harness-induced belief divergence (arXiv 2607.04528)

- Read: six harness configs, task/model/instructions fixed; divergence
  from evidence-stream filtering, not instruction text; failure-mode
  divergence up to 0.80; no repair.
- Protocol consequence (adopted): holding the harness fixed is
  load-bearing for corpus attribution — unequal harnesses swamp the
  signal.
- Open: replication. Revisit 2026-11.

### Behavioral reproducibility (arXiv 2605.28840)

- Read: same-model rerun noise floor — TSS 0.87, argument consistency
  0.69 (6 models × 19 tasks × 10 runs); ~60% of divergence arises in
  steps 1–2; ambiguity the dominant driver; no repair loop.
- Protocol consequence (adopted): the pilot's same-producer rerun control
  now has published reference numbers; early-trajectory divergence
  concentration suggests attribution effort focuses there.
- Open: replication; floor values for frontier-tier models. Revisit
  2026-11.

### Black-box system-prompt forensics (arXiv 2606.22698)

- Read: attribution/fingerprinting of prompt + base model from
  conversations; prompts opaque units (no clause-level attribution); no
  repair; ~97% pairwise on structurally different prompts, <80% under
  paraphrase; sensitivity model-dependent.
- Check answered: supports the program's white-box choice — output-only
  attribution degrades exactly where clause diagnosis needs resolution.
- Open: replication. Revisit 2026-11.

### GEPA — reflective prompt evolution (arXiv 2507.19457, ICLR 2026 oral)

- Read: reflection attributes successes/failures to prompt elements, then
  rewrites; instance-level Pareto selection; single system,
  outcome-scored; cross-model transfer post hoc (Qwen3-8B →
  GPT-4.1-Mini +9%). Numbers self-reported.
- Check answered: it DOES attribute (corrects this survey's earlier
  claim); differentiation now rests on signal/object/checkability/
  validation, and GEPA-style reflection is a candidate stage-4 component.
- Open: independent evaluation of reported gains. Revisit 2026-11.

### PromptExp (arXiv 2410.13073)

- Read: token→component attribution (IG + perturbation); two models
  evaluated separately; human-in-loop refinement (compression study, 10
  developers, 84% found explanations reasonable).
- Check answered: has a weak repair loop (human-guided), single-model, no
  corpus routing or ablation gate.
- Open: nothing decision-relevant. Park.

### HarnessFix (arXiv 2606.06324) — nearest attribute+repair neighbor

- Read: HTIR aligns failed-trajectory steps with harness artifacts
  including prompt templates; scoped repair operators across seven
  layers; regression-aware validation (target-flaw reduction within
  regression limits on held-out tasks); +6.3–18.4% on GAIA/SWE-bench
  Verified/AppWorld/Terminal-Bench; GPT-5 mini primary, five LLMs tested.
- Differentiation: failure signal on one system vs divergence between
  heterogeneous producers (needs no failure/ground truth — organic tasks
  qualify); no shared corpus, no model-scoped routing, no producer-side
  introspective evidence.
- Open: whether its citers extend to cross-model signals — the active
  harness self-evolution cluster (Harness-R1, HarnessBank, Capability
  Sheaves, Harness Handbook) is unswept. Revisit 2026-10 (fastest-moving
  neighbor).

### One Recipe, Many Harnesses (arXiv 2608.10178) — closest goal overlap

- Read: one evolution recipe across 8 languages × 3 models; separate
  harness per cell; model-specificity by post-hoc Jaccard comparison;
  per-edit typed-failure manifests with predicted-impact contracts
  validated next round; language binds more than model; two null regions.
- Differentiation: pursues the shared-vs-model-specific partition by
  evolve-then-compare; no shared maintained corpus, no
  divergence-as-live-signal, no shared/model-scoped routing mechanism.
- Adopted precedent: predicted-impact contracts = published cousin of the
  pre-registered patch discipline.
- Open: its citers; whether any successor maintains a shared corpus.
  Revisit 2026-10.

### Arbiter (arXiv 2603.08993) and Instruction Bleed (arXiv 2606.26356)

- Read: Arbiter — static contradiction audit of vendor agent-CLI prompts
  (incl. Claude Code) at block/AST/directive granularity; multi-model
  auditor diversity yields categorically different findings; detects,
  does not patch; one finding externally validated (Google patch).
  Instruction Bleed — module-interference measurement by perturbation
  (d=0.63, sub-threshold), single model, proposes regression tests, no
  repair.
- Adopted precedents: auditor diversity backs the stage-3 cross-audit;
  module-interaction regression tests are natural post-patch checks;
  "modular corpora exhibit composition-seam bugs" applies to this repo's
  routed-packet architecture.
- Open: both papers' citers (very fresh). Revisit 2026-10.

## Void map

Axes as in `survey.md` (object × mechanism × signal), decision-relevant
cells after the grounded slice:

- {scaffold × attribute × failure trajectories} — `filled`: SkillTriage,
  HarnessFix diagnosis stage.
- {scaffold incl. prompts × attribute + repair × failure trajectories} —
  `filled`: HarnessFix; active cluster `in-progress` (Harness-R1 etc.).
- {per-system prompt × attribute + rewrite × outcome metric} — `filled`:
  GEPA (B3).
- {prompt components × attribute + human repair × perturbation} —
  `filled`: PromptExp.
- {corpus text × static audit × none} — `filled`: Arbiter.
- {corpus modules × interference measurement × perturbation} — `filled`:
  Instruction Bleed.
- {per-model harnesses × shared-vs-specific partition × post-hoc artifact
  comparison} — `filled`: One Recipe.
- {shared versioned corpus × clause-cited attribution + routed repair ×
  cross-model divergence} — **`untried` after the grounded pass**: the
  `research/differential-instruction-diagnosis` cell. Why plausibly
  unexplored: presupposes a maintained multi-file corpus with per-model
  supplements, session-continuation access to producer reasoning, and
  willingness to run a competitor's model on one's own corpus.

## Falsification gate

`prior-art-checked:` grounded slice 2026-08-15 — ten papers read
(prompted arXiv-HTML extraction); S2 forward-citation snowballs of GEPA,
PromptExp, HarnessFix; four reframing/title queries (survey
§Disconfirming pass items 4–7). **Result: no occupant of the narrowed
cell; gate passed at moderate confidence.** Corrections the pass forced:
GEPA does attribute (earlier claim withdrawn); bare attribute+repair is
occupied at adjacent objects; goal overlap exists via One Recipe's
evolve-then-compare route. Residuals: citers of Arbiter / Instruction
Bleed / One Recipe unswept, debate-survey reference lists unmined,
industrial write-ups spot-checked only.

## Capstone candidate

The diagnosis-program cell above.

- Impact: a measured evidence stream for corpus maintenance — the
  ablation-by-model/harness the repo charter already prefers — and
  systematic population of the model-supplement layer; divergence-as-
  signal works on organic tasks with no ground truth, which the
  failure-signal neighbors cannot.
- Tractability: high — producers, transcripts, session forks, and
  supplement routing exist in this repo's tooling; missing pieces are the
  orchestration script and transcript-paging tool. Published cousins now
  exist for two protocol parts (predicted-impact contracts; multi-model
  audit diversity).
- Novelty-confidence: `moderate` (gate passed 2026-08-15 with named
  residuals; fastest-moving neighbor is the harness self-evolution
  cluster — revisit 2026-10).
