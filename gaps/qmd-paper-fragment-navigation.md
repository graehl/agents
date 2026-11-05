---
slug: qmd-paper-fragment-navigation
noticed: 2026-11-05
where: qmd_build/source_map.py and qmd_build/common.py fragment_anchors
---

**Gap:** Three ASR manuscripts do not build through the shared HTML builder's
default source-navigation path. Observed while adding term-definition previews:

- `~/draft/research/speech-recognition/papers/shared-trunk-price/` fails with
  “Rendered sections do not match the original source targets”. The supported
  `--no-source-map` option successfully builds its HTML and browser PDF.
- `~/draft/research/speech-recognition/papers/weakn-compact-asr/` and
  `~/draft/research/speech-recognition/papers/tts-and-lexicons-for-asr/` include
  headingless `sections/_00-abstract.qmd` fragments. Source-target discovery
  rejects them. With `--no-source-map`, fragment-anchor discovery still rejects
  them. Direct `quarto render index.qmd --to html` succeeds for both.

**Fix sketch:** Reconcile included abstract fragments with source-navigation
contracts; determine the precise unmatched section in shared-trunk-price before
changing its source or the mapper. Do not weaken target validation merely to
accept these builds. Cause and baseline status of the section mismatch have
not yet been isolated. The term filter and implicit-preview switches are wired
in all three manuscripts; these navigation failures remain separately visible.

Contributing-model: 6-astra
