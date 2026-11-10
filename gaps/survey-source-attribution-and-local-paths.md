---
slug: survey-source-attribution-and-local-paths
noticed: 2026-11-10
where: surveys/open-weight-model-censorship, surveys/asr-training-audio-enhancement, surveys/asr-lm-fusion
---

**Gap:** three survey defects found by reading.

- `surveys/open-weight-model-censorship/concepts/refusal-direction-removal.md`
  files two Casademunt results under the Perplexity source.
- `surveys/asr-training-audio-enhancement/survey.md` and `frontier.md` link
  to a path that exists on one machine, and `survey.md` narrates a private
  conversation instead of stating the finding.
- `surveys/asr-lm-fusion/` links an internal code-review host from a
  repository whose origin is public. Whether that link stays is the user's
  decision.

**Noticed while:** the automatic strict review of
`1e439e95a14a..ee441c86d0b2`.

**Fix sketch:** move the two bullets to their source; use
repository-relative paths and drop the aside; replace or remove the
internal link once decided.
