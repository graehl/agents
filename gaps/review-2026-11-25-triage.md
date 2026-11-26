---
slug: review-2026-11-25-triage
noticed: 2026-11-25
where: topics/ml-model-development.md § Partial training is named and chosen explicitly
---

**Gap:** the partial-training tags let one run carry two names. On an
18-layer model, `r64·top8` (adapter on the last 8 layers) and
`r64·frz10` (no adapter on the first 10) describe the same run, so a
search or a cross-session table comparison by tag can miss half of
them. Re-checked 2026-11-26 against the topic: both forms are listed,
and nothing says which one to prefer.

The rule is recorded as graehl's (2026-11-24), so the choice of a
canonical form waits on him. Candidate: write the trained span
(`·topN`), with `frzN` only for full fine-tuning with frozen layers,
since `top` reads the same for any depth.

The rest of this triage pool was fixed or moved on 2026-11-26: the
punctuation and audio-enhancement surveys, the build-boot errors, and
the vendored count. The span-denoising works without a manifest row are
in `surveys/span-denoising-pretraining/gaps/unmanifested-cited-works.md`.

**Noticed while:** the review triggered by the `scripts/jira` verbs commit.
**Fix sketch:** pick the canonical form and add one sentence to the tag
rule.
