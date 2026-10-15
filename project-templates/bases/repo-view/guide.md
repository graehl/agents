# Repository web view

`scripts/repo_view.py` shows this repository's Markdown and Quarto documents
as web pages, with every relative link between them working, beside the
images, PDFs and built HTML they link. It needs Python 3.9+ and `pandoc`
(without pandoc, the live view shows documents as source text; `build`
refuses). `python3 scripts/repo_view.py --help` lists the options.

## Make it the project's app

`python3 scripts/repo_view.py enable` declares the live view as this project's
YA app in `.project-template/app.json`, keeping that file's other fields. It
refuses when the project already declares an app, since YA opens one app per
project; `--replace` makes the view the app instead. Arguments after `--` are
passed to `serve`, for example `enable -- --root docs/handbook.md`. Then start
the app from YA's App button. To try it without YA:

```sh
python3 scripts/repo_view.py serve --port 8000   # http://127.0.0.1:8000/
```

The declaration has no `basePathEnv`, so YA serves the view at the app
address's root and each page's address is its path in the repository
(`/docs/guide.md`). A YA without an app host name for that address needs
`"basePathEnv": "BASE_PATH"` added under `serving`; the view still works, under
an opaque path prefix.

## What it serves

A document is rendered at its own path. A directory shows its `index.html`,
else its rendered `README.md`, else a listing of its non-ignored files. Only
paths reachable by links from the repository root are served, plus any
`--root` paths and project pages: linking a directory whose page is a listing
exposes the files listed there. A newly written link works at once; a path
stays servable until the server restarts, even after its last link is gone.
Paths with a segment beginning with `.` are never served, and the view writes
nothing into the repository.

To limit what a shared address shows, link less from the root documents or
publish a static build of a narrower `--root`.

## Publish a static site

`python3 scripts/repo_view.py build` writes the same reachable set to `_site/`:
documents as `<path>.md.html`, directory pages as `index.html`, and every
linked file beside them, with links rewritten to match. It replaces the old
site only after the new one is complete, refuses a site larger than
`--max-bytes`, and adds `_site/` to `.git/info/exclude`. The output contains no
access tokens: copy `_site/` to any static host to publish it.

`enable --static` declares the built site as the YA app instead of the live
server. `serve --static` serves the built site as a whole, without pandoc. Both
show the site as of its last build; rebuild after changing documents.

## Private links

YA's private app links carry a `ya_access` token. Pages from `serve` keep the
token in the address bar and on same-origin links, so a copied address opens
the same page for its recipient. The page takes the token from its own
address, else from the server, else from one it saw earlier on this site.
The server knows the token when `.project-template/app.json` has a top-level
`"yaAccess": "<token>"`, or from `--access-token-file`; it re-reads either on
change. Static builds never contain the token.

Behind YA, YA checks the token and strips it before the request reaches the
view, so the view only displays it. Where no YA proxy stands in front, add
`--require-access`: requests then need the token as `?ya_access=` or the
`ya_app_access` cookie set by a valid link, and a rotated token revokes old
links at once.

## Project pages

`--pages FILE:FUNCTION` adds generated pages such as dashboards. The function
receives the repository root and returns `{relative path: complete HTML}`; a
page at `index.html` replaces the root page. Pages link documents by their
source paths (`docs/guide.md`). Under `serve` they are regenerated on request
once older than `--pages-max-age` seconds; `build` generates them once.

After changing the view or its options, open the root, a document, a directory
and a linked built output through the actual app address.
