# Instruction Bleed — cross-module interference in prompt-composed systems

Read method: prompted extraction over the arXiv HTML full text, 2026-08-15;
local extract pending (`related-work fetch`). Full text:
[HTML](https://arxiv.org/html/2606.26356) · [PDF](https://arxiv.org/pdf/2606.26356).
arXiv 2606.26356.

**What it is.** Names and measures compositional behavioral leakage (CBL):
behavioral interference between co-resident prompt modules sharing one
attention context, in systems that compose instruction modules via markdown
conventions/templating/inheritance (OpenClaw, career-ops, OpenHands,
aider). A reusable three-channel protocol perturbs non-focal modules along
volume, content, and form and measures the effect on focal-module behavior
with paired comparisons (bootstrap CIs, Cohen's d).

**Results.** Existence proof on Claude Sonnet 4.6 (144 trials, 12 job
descriptions): adding an irrelevant archetype to shared rules shifted
focal-module scores d=0.63 (CI excluding zero), sub-threshold (no
recommendation flips). Proposes a regression-testing framework —
compositional consistency, module-interaction regression,
format-perturbation robustness — rather than repair.

**Relation to the diagnosis program.** The object is corpus-like (a
multi-module instruction set) and the method is perturbation-based
measurement — effectively the program's confirmation layer (ablation) used
as the finder, on one model. No cross-model divergence signal, no
attribution from natural task trajectories, no repair loop. Its
module-interaction regression tests are a natural post-patch check for
corpus patches this program lands.
