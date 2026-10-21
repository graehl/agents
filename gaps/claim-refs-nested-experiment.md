---
slug: claim-refs-nested-experiment
noticed: 2026-10-21
where: claim-refs pack --run
---

Contributing-model: gpt-6-astra

**Gap:** `claim-refs pack --run` rejects a nested experiment/run locator
with `--run expects <experiment>/<run-id>`, although agentctl accepts
slash-separated experiment names and writes their run records normally.

**Noticed while:** preserving the Lao corpus-quality smoke from a clean
ancillary checkout. Experiment `speech-recognition/lo/purchase-smoke-20261021`,
run `20261021T201807Z`, had a valid completed JSON record. The workaround
copied the exact experiment directory after verifying the destination was
absent; no existing experiment records were overwritten.

**Fix sketch:** resolve the final path component as the run ID and preserve
the preceding experiment path, with ordinary traversal validation. Inspect
the actual parser before implementation; retain a nested-name integration
case against a real run-record layout.
