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

`enable` writes this `service` entry (with extra `serve` arguments appended to
`argv`); write it by hand when the script is run from outside the project:

```json
{
  "version": 1,
  "where": { "kind": "process", "cwd": ".", "entry": "/" },
  "start": { "argv": ["python3", "scripts/repo_view.py", "serve"], "portEnv": "PORT" },
  "status": { "probe": "http", "path": "/healthz", "readyStatus": 200, "startupTimeoutMs": 30000 },
  "stop": { "signal": "SIGTERM", "graceMs": 3000 },
  "serving": { "target": "sandbox-loopback", "protocol": "http" }
}
```

The declaration has no `basePathEnv`, so YA serves the view at the app
address's root and each page's address is its path in the repository
(`/docs/guide.md`). A YA without an app host name for that address needs
`"basePathEnv": "BASE_PATH"` added under `serving`; the view still works, under
an opaque path prefix.

## What it serves

A document is rendered at its own path. A directory shows its `index.html`,
else its rendered `README.md`, else a listing of its non-ignored files and
directories containing Git-tracked files. Directories with no tracked files
are not recursively indexed; an explicit link can still reach an untracked
built page and the assets it links. Staging a file makes its directory eligible
for listing without restarting the server. Only
paths reachable by links from the repository root are served, plus any
`--root` paths and project pages: linking a directory whose page is a listing
exposes the files listed there. Requesting an existing but unlinked path walks
the links to look for it; a request within `--rewalk-after` seconds (default
5) of the last walk's start reuses that walk's answer, so a burst of such
requests costs one walk, and a newly written link works once that window
passes. A path stays servable until the server restarts, even after its last
link is gone.
Paths with a segment beginning with `.` are never served, and the view writes
nothing into the repository.

Startup discovers the entry pages' immediate links instead of crawling the
whole repository. A request for an unknown path triggers link discovery;
concurrent requests share that work, and a discovered file can be served before
the rest of the walk finishes. Dashboard generation still precedes readiness.

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

## Location in YA's App bar

YA shows the app in a frame on another origin, so it cannot read which page
is showing. Every HTML page `serve` sends, including repository `.html` files
such as rendered papers, therefore posts its address (token removed) to a
framing parent as `{type: "yep-anywhere:app-location", href}`, on load and on
history or `#` changes. YA's App bar shows that path as breadcrumbs. Outside a
frame the script does nothing; static builds do not contain it.

Rendered pages open with breadcrumbs, and repository `.html` files served live
get a smaller crumb row at the top of their body that scrolls away with the
page (a file without a `<body>` tag gets none). A framed page hides its own
crumbs, taking the framer to show the location already, until the framer
answers `{type: "yep-anywhere:app-location-shown", shown: false}`; YA's bar
sends that when it is too narrow to show the path, usually on phones.

## Copying paths and commenting

Double-click an inline fixed-font item to select the whole item, including
hyphens, spaces and path separators. Code blocks retain ordinary selection.
Right-click inline code to copy its text, or a repository link/breadcrumb to
copy its project-relative path. Shift-right-click keeps the browser's own menu.
Inline text has no copy icons. The breadcrumb row reveals its current-path
copy button on hover/focus; its overflow menu also works on touch. The current
filename supports these actions without becoming a navigation link.

When embedded in a compatible YA session pane, the menu also offers Comment on
path, and a selected passage offers Comment on selection. These prepare the
containing session's existing draft and focus its composer; they never send a
message. Standalone tabs and older YA clients keep copy actions without an
unroutable comment control. Remembering another destination session or opening
an inline forwarding composer is deferred design work.

The breadcrumb overflow menu also acts on the page itself: copy its link
(keeping a private link's token), open it in a new tab when framed, reload.

## Freshness and rebuilds

A live-served page records what it shows: the file behind it and, for a
build output, its inputs. When the reader returns to the page (it becomes
visible, gains focus, or the pointer enters it), the page asks again with
`?repo-view=fresh` and shows a notice when the file changed on disk (with
Reload) or when the build is older than an input. It never checks on a
timer. A static site carries no freshness.

**Rebuildable outputs: the convention.** Any builder of static output (HTML,
and the PDFs and sidecars it links) makes that output rebuildable by writing
a receipt beside it, `<stem>.receipt.json`, holding:

- `root`: the absolute path of the root source; other paths are relative to
  its directory;
- `inputs`: every file the build read, as `{"path", "sha256"}`;
- `output`, and `pdf` or `source_map` when made: the same `{"path", "sha256"}`
  for what it wrote; and
- `artifact_metadata.regenerate.proposedRegistration`: the command that
  rebuilds every output, `{"cwd", "argv", "outputs", "timeoutSeconds"}`, with
  absolute `outputs` and `argv` an argument vector, never shell code. An HTML
  output also carries this descriptor in its head as the
  `<!-- ya-artifact:v1 {"regenerate": …} -->` comment, which YA's file editor
  reads.

`qmd-html` writes this today (`~/agents` topic
`document-writing-browser-interactive`, § Scripted HTML build).
A receipt describes an output only while the output's hash still matches it,
so a different builder overwriting the same file (plain `quarto render` into
`_build/index.html`) makes it unreceipted again rather than misjudged.

A receipted output is stale exactly when an input's hash differs from its
receipt. `serve --rebuild` makes stale receipted outputs rebuildable by any
visitor: the page's notice offers **Rebuild**, which reruns the receipt's
command (one run per receipt at a time, joined by concurrent requests, within
its timeout; the directory must be inside the repository) while the old page
stays readable. The POST only starts the build; the notice then asks
`GET ?repo-view=rebuild` every second, shows the seconds so far, and reloads
into the new build when it is done, or shows the failure and its log (as the
notice text's tooltip) with **Retry**. No request is held open for the
build, since a proxy in between may drop a long one and leave the page
waiting. A stale receipted PDF or
other non-HTML output may open in a viewer that cannot show a notice, so
requesting it starts the same background build: that request gets the old
file at once, and a later one the new. Such a build starts once per state of
the output and its inputs, so one that fails is not rerun by every request.
Without `--rebuild` the notice names the command instead.

Without a receipt, a Quarto project's render product is judged by mtime
against render inputs chosen by suffix (`.qmd`, `.yml`, `.bib`, `.lua`,
styles, images; `.md` notes and a kept `.tex` are left out so that they do
not mark every build stale; hidden files such as an editor's lock file are
never inputs). A render product is an `.html` or `.pdf` in the project's
`output-dir` at the path of one of its documents (`_build/ch/a.pdf` for
`ch/a.qmd`); other files there, such as a figure PDF or an output renamed
with `output-file`, are not judged. Under `--rebuild` a product is rebuilt
the same ways with Quarto's own command, `quarto render --to html` (or
`--to pdf` for a PDF) in the project directory, when `quarto` is on the
server's `PATH`.

A freshness check that fails (an unreadable project file, say) is logged by
the server and the page is served without its notice.

## Project pages

`--pages FILE:FUNCTION` adds generated pages such as dashboards. The function
receives the repository root and returns `{relative path: complete HTML}`; a
page at `index.html` replaces the root page. Pages link documents by their
source paths (`docs/guide.md`). Under `serve`, a request for pages older than
`--pages-max-age` seconds gets them at once and starts a background
regeneration, so a slow generator never delays a page. After the generator
file is edited, the next request waits for pages from the reloaded generator,
without a restart; a generator edit that fails to load leaves the previous
one serving and logs why. `build` generates them once.

A page element with an `id` and `data-repo-dir="<directory>"` marks where the
page shows that directory. Every page's breadcrumb for a marked directory
links to that element; an unmarked directory links to its own page when it is
servable, else to its nearest marked ancestor's element. The program
dashboard marks each program this way, so `draft / research / speech-recognition`
crumbs open the dashboard at those programs.

After changing the view or its options, open the root, a document, a directory
and a linked built output through the actual app address.
