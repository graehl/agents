---
slug: python-cli-format-debt
noticed: 2026-09-07
where: agentctl.py, tests/test_agentctl.py, scripts/pdf-figures-svg
---

**Gap:** `uvx ruff format --check` reports existing formatting drift in
these three files. `uvx ruff check scripts/pdf-figures-svg` also reports
I001 on the import block and two RUF100 unused `noqa: E402` directives.

**Noticed while:** adding shared acli `--text` support. The feature's
changed Python blocks are formatted; the remaining findings occur outside
them. The affected acli library files pass Ruff lint and formatting checks.

**Fix sketch:** isolate a mechanical cleanup of these files in its own
commit, preserving any concurrent changes. This is adjacent formatting
work, deferred from the requested text-output feature and color sketch.
