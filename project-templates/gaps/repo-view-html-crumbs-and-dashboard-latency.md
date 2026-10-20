---
slug: repo-view-html-crumbs-and-dashboard-latency
noticed: 2026-10-20
where: project-templates/bases/repo-view/files/repo_view.py
---

**Gap:** two repo-view `serve` defects seen browsing the draft research site
inside YA's App pane.

1. **Repository `.html` files have no breadcrumbs.** Rendered documents and
   listings get `nav.crumbs` from `compose_page`, but `.html` files such as
   Quarto papers are sent as stored (`respond` → `file_reply`). Only the
   frame location reporter is now inserted, so YA's App bar can show the path;
   outside YA a paper shows no way back up.

   User-directed shape: the same crumb style as rendered pages, in a lower
   form, scrolling away with the page (no fixed bar or frame). Quarto pages
   carry their own fixed navbar, sidebar and CSS, so the insertion must not
   assume the page's layout. The existing crumb row also has more blank space
   above it than wanted (`body` top padding plus `nav.crumbs` padding); trim
   it for rendered pages too.

2. **The dashboard regenerates inside the request.** `ProjectPages.current()`
   regenerates `--pages` output synchronously once it is older than
   `--pages-max-age` (default 10 s); the draft dashboard takes about 3 s. So
   returning to `/` after reading a page for more than 10 s waits ~3 s
   (measured 3.15 s, then 0.19 s on the next request). Serve the previous
   pages and regenerate in the background (stale-while-revalidate), keeping
   the first generation and generator reloads correct.
