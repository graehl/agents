---
slug: repository-web-view
noticed: 2026-10-15
where: project-templates/bases (new capability base); .project-template/app.json
---

**Gap:** no template or capability base gives a project an easy-to-enable,
YA-like web view of its own repository: Markdown rendered as pages, relative
links that keep working between documents, and built HTML/PDF outputs
reachable, opened from YA's App button. YA's static app and artifact serving
hand raw `.md` to the browser as a download, and nothing rewrites a page's
links to YA's own Markdown viewer.

**User-directed scope (graehl, 2026-10-15):** an easy-to-enable web-service
view as a project template capability, addable to an existing project as
well as chosen at creation. "Every traversable link works" is the bar.

**Prototype:** `~/draft` `scripts/research_index.py` writes a static site:
a programs/papers dashboard at the repository root, and the transitive
closure of reachable Markdown rendered by pandoc into a git-excluded `_views/`
with every relative `href`/`src` re-pointed. `.project-template/app.json`
declares `{"where": {"kind": "static", "root": ".", "entry": "index.html"}}`,
so YA serves the whole repository (YA already refuses dot-prefixed path
segments, so `.git/` is not served). It works, but every regenerate re-renders
the closure, and the dashboard part is research-program specific.

**Fix sketch:** a capability base (working name `repo-view`) that vendors:

- **Static mode:** a generator rendering reachable Markdown to HTML with link
  rewriting, a size cap, atomic swap of the output directory, and Git
  exclusion of the output; plus the static `app.json` declaration.
- **Live mode (preferred end state):** a small read-only process app
  (`where.kind: "process"`) rendering a requested path on demand, which needs
  no mirror and is never stale. YA runs process apps in its project sandbox
  with the network firewall, which suits a filesystem reader.
- Rendering parity with YA's viewer where cheap: GFM, math, code
  highlighting, Quarto/Markdown front matter, relative image links.
- An optional dashboard plug-in (programs, papers, sessions) built on the
  shared records described in `~/agents` `gaps/sketches/program-session-view.md`.

Lessons from the live prototype (2026-10-15, `~/draft`
`scripts/research_site_server.py`):

- **Serve only what is reachable.** Precompute reachability from the
  dashboards over Markdown and HTML links, caching each file's links by
  mtime; also admit a served page's current links and links from an allowed
  referring page, so new links work at once. graehl: the set may only grow.
- **Keep the private-link token visible.** YA validates `ya_access`, sets a
  cookie and strips the token before proxying, so only the page can copy it
  onto same-origin links; dropping it from PDF or built-HTML links is fine.
- **Token checks for servers YA does not proxy.** A reserved project-app
  address needs nothing: YA checks the token before forwarding to the
  sandboxed process. A manual host-port vhost or an independent user service
  could verify the token itself if YA published it to a git-excluded or
  YA-data-dir dotfile (graehl's proposal); that needs a YA contract.
- **Cheap metadata.** One `git status --untracked-files=normal` and one
  `git ls-files` per rebuild; per-path status walks and recursive globs over
  ignored trees stalled for minutes inside the sandbox.

Open decisions: whether the live renderer is Node (matching the `server`
base) or Python with pandoc; how much of YA's viewer to mirror versus linking
into YA itself (`~/ya` `gaps/sketches/session-links-in-viewer.md` covers link
interpretation inside YA); and how a project limits what the view exposes
when its app address is shared.
