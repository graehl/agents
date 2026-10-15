---
slug: repo-view-static-freshness
noticed: 2026-10-15
where: project-templates/bases/repo-view/files/repo_view.py
---

**Desired outcome:** `repo_view.py serve` uses a built `_site/` as an
accelerator page by page: a request is answered from the built file when that
file is still fresh, and rendered live otherwise. Today `serve --static` is
all-or-nothing: it serves the last build as a whole and goes stale until the
next `build`, while plain `serve` renders every document on request (cached in
memory by file stat).

**Proposed approach:** `build` records in `_site/.repo-view.json` each
output's sources with their `(mtime_ns, size)`: the document for a rendered
page, the directory listing for a listing page, the source file for a copied
asset. Freshness is checked on demand when a request arrives, never by
periodic polling (graehl, 2026-10-15); a file watcher (inotify) that
invalidates entries is a possible later refinement. A fresh built page still
passes through the dynamic server, which adds the `ya_access` keeper and any
server-known token, because the published site never contains them.

**Unresolved:**

- Pages depend on more than their source: breadcrumbs and listing pages depend
  on what is reachable, and project (`--pages`) pages have no declared
  sources. Either record those dependencies or always render such pages live.
- Built pages link `x.md.html`; live pages link `x.md`. Serving built pages
  would put the `.md.html` form in the address bar unless the server reverses
  the static link rewrite.
- Whether a per-file check is cheap enough on large closures, compared with
  one whole-tree fingerprint (Git HEAD plus `git status`) at request time.
