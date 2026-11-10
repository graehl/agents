---
slug: repo-view-receipt-names-rebuild-command
noticed: 2026-11-10
where: project-templates/bases/repo-view/files/repo_view_builds.py
---

**Gap:** under `serve --rebuild`, any `*.receipt.json` in a served directory
that names a served output supplies the command line a visitor can run
(`Builds.receipt` reads `argv` from
`artifact_metadata.regenerate.proposedRegistration`). Only the working
directory is confined to the repository. A cloned or generated file can
therefore choose the executable. The `--rebuild` help text says any visitor
may rerun a receipt-declared command; it does not say a receipt may declare
any command.

**Why it is not narrowed yet:** the one builder in this repository that
writes such receipts, `qmd_build/html.py`, records
`[sys.executable, <checkout>/scripts/qmd-html, ...]`: the builder's own
interpreter and an absolute path into a checkout of this repository. The
view is vendored into other projects as `scripts/repo_view.py` and cannot
know either path, and its guide invites any builder to write a receipt
(§ Freshness and rebuilds, "Rebuildable outputs: the convention"). An
allowlist derived inside `repo_view.py` would be a guess. The receipt's
`hook` name is written by the receipt itself, so it proves nothing.

**Noticed while:** the strict review of `1e439e95a14a..ee441c86d0b2`
(advisory A9), which deferred it to a security review.

**Fix sketch:** let the operator name the trusted builders when enabling
rebuilds (for example the command prefixes a receipt's `argv` must start
with), and refuse a receipt whose command is not among them. That changes
the `--rebuild` command line, so it needs a decision on the option's shape
and on what `enable` writes into `app.json`.
