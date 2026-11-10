---
slug: agentctl-source-deps-watch-orphans-children
noticed: 2026-11-10
where: agentctl.py (SourceDepsLoadingWatch, SourceDepScanner)
---

**Gap:** the source-dependency watch on a launched run misses its two
purposes in common cases.

- `SourceDepsLoadingWatch._check` enforces by calling `proc.terminate()` on
  the direct child only. With a payload such as `bash run.sh` that starts
  `python train.py`, an edit during loading kills bash; the trainer is
  orphaned, keeps its GPU, and the run is recorded finished with return
  code 2. Shown in a mirror of the launch, not through agentctl itself.
- `SourceDepScanner._references` parses imports only for `.py` files. A dry
  run with `--source-deps-scan scripts/review-due` lists one file although
  that script imports `acli`, and `unresolved` is empty, so an executable
  without a suffix is silently under-scanned.

Related: `agentctl.py` is over 9,000 lines, and this watch is a
self-contained section of about 610 lines that could split out as
`agentctl_gpu.py` did.

**Noticed while:** the automatic strict review of
`1e439e95a14a..ee441c86d0b2`.

**Fix sketch:** stop the whole descendant set as `stop` does, with a test
whose payload does not exec its child; recognise a `python` shebang and
record files the scanner cannot classify under `unresolved`.
