---
slug: review-2026-11-25-triage
noticed: 2026-11-25
where: surveys/punctuation-case-restoration, surveys/span-denoising-pretraining, surveys/asr-training-audio-enhancement, scripts/build-boot, vendor/modern-web-guidance/VENDORED.md, topics/ml-model-development.md
---

**Gap:** triage pool of findings from the automatic review of the 17 commits
after `5c0c4d26ad9e`, reported by the reviewer and not yet re-checked here.

- **Punctuation survey fails its own audit.** In
  `surveys/punctuation-case-restoration/related-work/papers.yaml`, entry
  `caseiro2020-capitalization-masks` has an extract and a reading but still
  says `grounded: false`, `fetched: null`, so `related-work audit` exits 3.
  The reading is linked from neither `survey.md` nor a concept page.
- **Span-denoising survey cites unmanifested works.**
  `surveys/span-denoising-pretraining/concepts/multilingual-mt-systems.md`
  and `concepts/prompted-mt.md` give exact figures for about fifteen works
  with no `papers.yaml` entry or extract, which the audit cannot see. Three
  manifested keys (`luo2025-lamate`, `gritta2026-afrislm`,
  `kudugunta2023-madlad`) have table numbers in concept pages but no
  extract. Cheap to make honest with ungrounded manifest rows; grounding
  them is real work.
- **Audio-enhancement survey contradicts itself across passes.**
  `surveys/asr-training-audio-enhancement/survey.md` coverage lists still
  name as unfetched papers that the third pass read, and concept pages
  narrate their own replacement.
- **`scripts/build-boot` omit-marker errors** report a line number in the
  concatenated boot without naming the source file; and
  `topics/agent-instructions.md` says a supplement's lines can be omitted,
  though read-when supplements never pass through that filter.
- **`vendor/modern-web-guidance/VENDORED.md`** says 210 upstream guides in
  one place and 209 in another.
- **Partial-training tags** in `topics/ml-model-development.md`: two tags
  (`r64·top8`, `r64·frz10`) can name the same run on an 18-layer model.

**Noticed while:** the review triggered by the `scripts/jira` verbs commit.
**Fix sketch:** re-check each against the tree, then fix the cheap ones as
their own commits and promote the span-denoising grounding to its own file
under that survey's `gaps/`.
