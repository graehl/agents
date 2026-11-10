---
slug: repo-view-freshness-errors-fail-page
noticed: 2026-11-10
where: project-templates/bases/repo-view/files/repo_view.py
---

**Gap:** the freshness check that decorates a served HTML page can raise,
and the request handler catches only `RepoViewError`, so a decoration
failure makes the page unservable.

- `newest_quarto_input` stats every file with a render-input suffix. It
  skips dot directories but not dot files, so an Emacs lock file
  (`.#index.qmd`, a dangling symlink) raises `FileNotFoundError`. Every page
  in that Quarto output directory fails while a source has unsaved edits.
  Reproduced by calling `freshness()`.
- `Builds.receipt` guards only its first three lookups. A `*.receipt.json`
  that names the page as an output but lacks `root` raises `KeyError`.
  Reproduced the same way.
- Under `--rebuild`, every image request walks the whole Quarto project
  before its suffix is rejected.

**Noticed while:** the automatic strict review of
`1e439e95a14a..ee441c86d0b2`.

**Fix sketch:** skip dot files and treat an entry that cannot be stat'ed as
absent; build the `Receipt` inside one `try` that returns `None`; catch
freshness failures once at the call site so decoration can never fail a
page; reject by suffix before walking.
