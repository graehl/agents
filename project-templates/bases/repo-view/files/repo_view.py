#!/usr/bin/env python3
"""Browse a Git repository's documents as web pages, live or as a static site.

`serve` answers HTTP on 127.0.0.1:$PORT. A Markdown or Quarto document is
rendered with pandoc at its own path (`/docs/guide.md`), so links written for
a Git forge keep working unchanged. A directory shows its `index.html`, else
its rendered `README.md`, else a listing of its non-ignored files. Only paths
that links reach from the repository root (and any `--root` or `--pages`
seeds) are served; that set only grows, and it is re-walked on demand when an
existing path is not yet in it. `serve --static` instead serves a site that
`build` wrote, as a whole.

`build` writes that reachable closure as a self-contained static site
(default `_site/`, excluded from Git through `.git/info/exclude`): documents
rendered as `<path>.md.html`, directory pages as `index.html`, every other
linked file beside them, and no access tokens. Publish it anywhere.

`enable` declares `serve` (or, with `--static`, the built site) as this
project's YA app in `.project-template/app.json`.

Pages served by `serve` keep a private link's `ya_access` token visible in the
address bar and on same-origin links, so a copied URL works for its recipient.
Standard library only; pandoc renders documents.
"""

from __future__ import annotations

import argparse
import errno
import hmac
import html
import importlib.util
import json
import mimetypes
import os
import posixpath
import re
import shutil
import subprocess
import sys
import threading
import time
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from http import HTTPStatus
from http.cookies import CookieError, SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, quote, unquote, urlsplit

ACCESS_QUERY = "ya_access"
ACCESS_COOKIE = "ya_app_access"
MANIFEST = ".repo-view.json"
DEFAULT_SITE = "_site"
DOCUMENT_FORMATS = {".md": "gfm", ".markdown": "gfm", ".qmd": "markdown"}
LINKING_SUFFIXES = {".html", ".htm", ".css", *DOCUMENT_FORMATS}
PLAIN_TEXT_SUFFIXES = {
    ".bib", ".cfg", ".csv", ".ini", ".ipynb", ".jsonl", ".log", ".lua", ".py",
    ".rs", ".sh", ".tex", ".toml", ".ts", ".tsv", ".yaml", ".yml",
}  # fmt: skip

STYLE = """
:root { color: #293e35; background: #f7f6f0; font: 15px/1.55 system-ui, sans-serif; }
body { margin: 0 auto; padding: 1rem 1.5rem 3rem; max-width: 1100px; }
a { color: #2f6b52; text-underline-offset: 2px; } a:hover { color: #387c60; }
a:focus-visible { outline: 3px solid #387c60; outline-offset: 3px; }
nav.crumbs { font-size: .9rem; color: #637066; padding: .3rem 0 .6rem; border-bottom: 1px solid #dcded4; }
nav.crumbs a { text-decoration: none; } nav.crumbs a:hover { text-decoration: underline; }
article { max-width: 48rem; }
article h1, article h2, article h3 { line-height: 1.25; margin-top: 1.5em; }
article h1 { font-size: 1.6rem; } article h2 { font-size: 1.25rem; }
table { border-collapse: collapse; margin: 1rem 0; font-size: .93em; }
th, td { text-align: left; vertical-align: top; padding: .35rem .6rem; border: 1px solid #dcded4; }
th { background: #ecebe2; font-weight: 600; }
pre { overflow-x: auto; background: #ecebe2; padding: .75rem 1rem; border-radius: 6px; }
:not(pre) > code { background: #ecebe2; padding: .05em .3em; border-radius: 4px; font-size: .9em; }
blockquote { margin: 1rem 0; padding: .1rem 1rem; border-left: 3px solid #a9b9a3; color: #4c5c52; }
img { max-width: 100%; height: auto; }
div.note, div.tip, div.important, div.warning, div.caution { margin: 1rem 0; padding: .2rem 1rem;
  border-left: 4px solid #4a7fb0; background: #eef2f5; }
div.tip { border-color: #2f8a55; } div.important { border-color: #7a52b3; }
div.warning { border-color: #c27c0e; } div.caution { border-color: #b3261e; }
div.title p { font-weight: 650; margin: .4rem 0; }
table.listing { width: 100%; } table.listing td.num { text-align: right; font-variant-numeric: tabular-nums; }
.layout { display: grid; grid-template-columns: minmax(11rem, 15rem) minmax(0, 1fr); gap: 2.5rem; align-items: start; }
nav.outline { position: sticky; top: 1rem; max-height: calc(100vh - 2rem); overflow: auto; font-size: .88rem;
  padding-top: 1.4rem; }
nav.outline summary { font-weight: 600; cursor: pointer; }
nav.outline ul { list-style: none; margin: .3rem 0 0; padding: 0; }
nav.outline li { margin: .2rem 0; } nav.outline li.h3 { padding-left: .9rem; }
.dim, footer { color: #637066; } footer { margin-top: 3rem; font-size: .85rem; }
.notice { color: #9a5b12; }
code span.kw, code span.cf, code span.im { color: #8f3f71; }
code span.dt, code span.bu, code span.fu { color: #2f5f8f; }
code span.dv, code span.bn, code span.fl, code span.cn { color: #9a5b12; }
code span.st, code span.ch, code span.vs, code span.ss, code span.sc { color: #2f6b52; }
code span.co, code span.do, code span.an, code span.cv, code span.in { color: #7b847d; font-style: italic; }
code span.al, code span.er { color: #b3261e; font-weight: 600; }
@media (prefers-color-scheme: dark) {
  :root { background: #1c1f1d; color: #e6ebe4; } a, a:hover { color: #8fcbab; }
  th, pre, :not(pre) > code { background: #2a2f2b; } th, td, nav.crumbs { border-color: #3a413c; }
  .dim, footer, nav.crumbs { color: #a3ada5; } blockquote { color: #b9c3bb; }
  div.note, div.tip, div.important, div.warning, div.caution { background: #252a27; }
  code span.kw, code span.cf, code span.im { color: #e29ac6; }
  code span.dt, code span.bu, code span.fu { color: #8fb8e2; }
  code span.dv, code span.bn, code span.fl, code span.cn { color: #e2b26a; }
  code span.st, code span.ch, code span.vs, code span.ss, code span.sc { color: #9fdcb5; }
}
@media (max-width: 860px) { .layout { display: block; } nav.outline { position: static; max-height: none;
  margin: .8rem 0 0; padding: .5rem .75rem; background: #ecebe2; border-radius: 6px; } }
@media (max-width: 860px) and (prefers-color-scheme: dark) { nav.outline { background: #2a2f2b; } }
@media (max-width: 700px) { body { padding-inline: 1rem; } }
"""

# Keeps a private link's token in the address bar and on same-origin links.
# YA validates `ya_access`, then strips it (and its HttpOnly cookie) before
# proxying, so the page remembers the token itself; a server that checks the
# token supplies it in a `ya-access` meta tag instead.
ACCESS_KEEPER = """<script>
(() => {
  const key = "ya_access";
  const url = new URL(location.href);
  let token = url.searchParams.get(key) || document.querySelector('meta[name="ya-access"]')?.content || "";
  try {
    if (token) localStorage.setItem(key, token);
    else token = localStorage.getItem(key) || "";
  } catch {}
  if (!token) return;
  if (url.searchParams.get(key) !== token) {
    url.searchParams.set(key, token);
    history.replaceState(history.state, "", url);
  }
  const keep = () => {
    for (const a of document.querySelectorAll("a[href]")) {
      const href = a.getAttribute("href");
      if (!href || href.startsWith("#") || /^[a-z][a-z0-9+.-]*:|^\\/\\//i.test(href)) continue;
      const target = new URL(href, location.href);
      if (target.origin !== location.origin) continue;
      target.searchParams.set(key, token);
      a.setAttribute("href", target.pathname + target.search + target.hash);
    }
  };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", keep);
  else keep();
})();
</script>"""

MARKDOWN_LINK = re.compile(
    r"\]\(\s*<?([^)\s>]+)>?(?:\s+[\"'][^\"']*[\"'])?\s*\)|^ {0,3}\[[^\]]+\]:\s*<?([^\s>]+)>?",
    re.MULTILINE,
)
HTML_LINK = re.compile(r"""\b(href|src)\s*=\s*(?:"([^"]*)"|'([^']*)')""", re.IGNORECASE)
CSS_URL = re.compile(
    r"""url\(\s*(?:"([^"]*)"|'([^']*)'|([^)'"\s]+))\s*\)""", re.IGNORECASE
)
SCHEME_OR_FRAGMENT = re.compile(r"^(?:[a-z][a-z0-9+.-]*:|//|#)", re.IGNORECASE)
FRONT_MATTER = re.compile(r"\A---[ \t]*\n(.*?)\n(?:---|\.\.\.)[ \t]*\n", re.DOTALL)
SECTION_HEADING = re.compile(
    r"<h([23])\b[^>]*\bid=\"([^\"]+)\"[^>]*>(.*?)</h\1>", re.DOTALL
)
OUTLINE_MIN_SECTIONS = 3


class RepoViewError(Exception):
    """A configuration or input problem reported to the user without a traceback."""


def git(root: Path, *args: str) -> str:
    done = subprocess.run(
        ["git", "-C", str(root), *args], check=False, capture_output=True, text=True
    )
    if done.returncode:
        raise RepoViewError(f"git {args[0]} failed in {root}: {done.stderr.strip()}")
    return done.stdout


def join_rel(directory: str, name: str) -> str:
    return f"{directory}/{name}" if directory else name


def parent_rel(rel: str) -> str:
    return rel.rpartition("/")[0]


def link_target(base_dir: str, url: str) -> str | None:
    """Repository-relative path a relative link names; None for external,
    root-absolute, escaping or dot-segment links."""
    url = html.unescape(url).strip()
    if not url or url.startswith("/") or SCHEME_OR_FRAGMENT.match(url):
        return None
    path = unquote(url.split("#", 1)[0].split("?", 1)[0])
    if not path:
        return None
    joined = posixpath.normpath(posixpath.join(base_dir, path))
    if joined == ".":
        return ""
    if joined == ".." or joined.startswith("../"):
        return None
    if any(part.startswith(".") for part in joined.split("/")):
        return None
    return joined


def link_urls(text: str, suffix: str) -> list[str]:
    """Every link-like URL in a document, page or stylesheet's text."""
    if suffix == ".css":
        return [a or b or c for a, b, c in CSS_URL.findall(text)]
    urls = [b or c for _, b, c in HTML_LINK.findall(text)]
    if suffix in DOCUMENT_FORMATS:
        urls += [a or b for a, b in MARKDOWN_LINK.findall(text)]
    return urls


def is_document(rel: str) -> bool:
    return Path(rel).suffix.lower() in DOCUMENT_FORMATS


@dataclass(frozen=True)
class DirectoryDocument:
    """What a directory URL shows: a project page, an index.html, a README, or a listing."""

    kind: str  # "page" | "index" | "readme" | "listing"
    rel: str | None = None


class Repository:
    """The served checkout, addressed by repository-relative POSIX paths ("" is the root)."""

    def __init__(self, root: Path):
        self.root = root.resolve()
        self.name = self.root.name
        self._listings: dict[str, tuple[int, list[tuple[str, bool]]]] = {}

    @classmethod
    def containing(cls, directory: Path) -> Repository:
        return cls(Path(git(directory, "rev-parse", "--show-toplevel").strip()))

    def path(self, rel: str) -> Path:
        return self.root / rel if rel else self.root

    def kind(self, rel: str) -> str | None:
        """'dir' or 'file' for an existing path that stays inside the repository."""
        try:
            real = self.path(rel).resolve(strict=True)
        except OSError:
            return None
        if not real.is_relative_to(self.root):
            return None
        return "dir" if real.is_dir() else "file" if real.is_file() else None

    def listing(self, rel: str) -> list[tuple[str, bool]]:
        """Immediate non-ignored children as (name, is_dir), from one `git ls-files`."""
        stamp = self.path(rel).stat().st_mtime_ns
        cached = self._listings.get(rel)
        if cached and cached[0] == stamp:
            return cached[1]
        out = git(
            self.root, "ls-files", "-z", "-co", "--exclude-standard", "--directory",
            "--", f"{rel}/" if rel else ".",
        )  # fmt: skip
        prefix = f"{rel}/" if rel else ""
        children: dict[str, bool] = {}
        for path in out.split("\0"):
            if not path.startswith(prefix):
                continue
            name, slash, _ = path[len(prefix) :].partition("/")
            if name and not name.startswith("."):
                children[name] = children.get(name, False) or bool(slash)
        found = sorted(
            (name, is_dir)
            for name, is_dir in children.items()
            if self.kind(join_rel(rel, name)) is not None
        )
        self._listings[rel] = (stamp, found)
        return found

    def ensure_excluded(self, site: Path) -> None:
        """Exclude the site and its build staging directories via `.git/info/exclude`."""
        try:
            rel = site.resolve().relative_to(self.root).as_posix()
        except ValueError:
            return
        exclude = Path(
            git(self.root, "rev-parse", "--git-path", "info/exclude").strip()
        )
        exclude = exclude if exclude.is_absolute() else self.root / exclude
        present = (
            exclude.read_text(encoding="utf-8").splitlines() if exclude.exists() else []
        )
        wanted = [f"/{rel}{suffix}/" for suffix in ("", ".new", ".old")]
        missing = [line for line in wanted if line not in present]
        if missing:
            exclude.parent.mkdir(parents=True, exist_ok=True)
            with exclude.open("a", encoding="utf-8") as out:
                if present and present[-1]:
                    out.write("\n")
                out.write(
                    "# repo_view.py static site\n" + "".join(f"{m}\n" for m in missing)
                )


@dataclass(frozen=True)
class Rendered:
    title: str
    body: str
    titled: bool  # the body already starts with its own <h1>


class Renderer:
    """Markdown and Quarto documents to HTML fragments with pandoc, cached by file stat."""

    def __init__(self, repo: Repository, require_pandoc: bool):
        self.repo = repo
        self.pandoc = shutil.which("pandoc")
        if require_pandoc and not self.pandoc:
            raise RepoViewError("pandoc not found on PATH; it renders every document")
        self._cache: dict[str, tuple[tuple[int, int], Rendered]] = {}
        self._lock = threading.Lock()

    def render(self, rel: str) -> Rendered:
        path = self.repo.path(rel)
        stat = path.stat()
        stamp = (stat.st_mtime_ns, stat.st_size)
        with self._lock:
            cached = self._cache.get(rel)
        if cached and cached[0] == stamp:
            return cached[1]
        text = path.read_text(encoding="utf-8", errors="replace")
        if self.pandoc:
            body = self._pandoc(text, DOCUMENT_FORMATS[path.suffix.lower()], rel)
        else:
            body = (
                '<p class="notice">pandoc is not installed where this server runs; '
                f"showing the source text.</p><pre>{html.escape(text)}</pre>"
            )
        front = FRONT_MATTER.match(text)
        declared = (
            re.search(r"^title:\s*(.+?)\s*$", front.group(1), re.MULTILINE)
            if front
            else None
        )
        heading = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.DOTALL)
        if declared:
            title = declared.group(1).strip("'\"")
        elif heading:
            title = html.unescape(re.sub(r"<[^>]+>", "", heading.group(1))).strip()
        else:
            title = path.name
        rendered = Rendered(title, body, titled=bool(heading) and not declared)
        with self._lock:
            self._cache[rel] = (stamp, rendered)
        return rendered

    def _pandoc(self, text: str, reader: str, rel: str) -> str:
        command = [
            self.pandoc,
            "--sandbox",
            "-f",
            reader,
            "-t",
            "html5",
            "--mathml",
            "--wrap=none",
        ]
        done = subprocess.run(
            command, check=False, input=text, capture_output=True, text=True
        )
        if done.returncode:
            raise RepoViewError(f"pandoc failed on {rel}: {done.stderr.strip()}")
        return done.stdout


def compose_page(
    repo_name: str,
    page_dir: str,
    current: str | None,
    title: str,
    body: str,
    linkable: Callable[[str], bool],
    footer: str = "",
) -> str:
    """A full page for a URL whose directory is `page_dir`, with breadcrumbs to
    each ancestor directory that is itself servable. All links are relative."""
    parts = page_dir.split("/") if page_dir else []
    crumbs = [(repo_name, "")] + [
        (name, "/".join(parts[: i + 1])) for i, name in enumerate(parts)
    ]
    items = []
    for depth, (label, rel) in enumerate(crumbs):
        up = len(parts) - depth
        if (current is None and depth == len(parts)) or not linkable(rel):
            items.append(html.escape(label))
        else:
            items.append(f'<a href="{"../" * up or "./"}">{html.escape(label)}</a>')
    if current is not None:
        items.append(html.escape(current))
    main = f"<main><article>\n{body}\n</article></main>"
    contents = outline(body)
    return (
        '<!doctype html>\n<html lang="en"><head><meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<meta name="generator" content="repo-view">\n'
        f"<title>{html.escape(title)}</title><style>{STYLE}</style></head><body>\n"
        f'<nav class="crumbs" aria-label="Location">{" / ".join(items)}</nav>\n'
        + (f'<div class="layout">{contents}{main}</div>\n' if contents else main + "\n")
        + (f"<footer>{footer}</footer>\n" if footer else "")
        + "</body></html>\n"
    )


def outline(body: str) -> str:
    """A contents sidebar from a long document's section headings."""
    sections = SECTION_HEADING.findall(body)
    if len(sections) < OUTLINE_MIN_SECTIONS:
        return ""
    items = "".join(
        f'<li class="h{level}"><a href="#{anchor}">{html.escape(html.unescape(re.sub(r"<[^>]+>", "", text)).strip())}</a></li>'
        for level, anchor, text in sections
    )
    return f'<nav class="outline" aria-label="Contents"><details open><summary>Contents</summary><ul>{items}</ul></details></nav>'


def document_page(
    repo: Repository,
    rendered: Rendered,
    page_dir: str,
    current: str | None,
    linkable: Callable[[str], bool],
    footer: str = "",
) -> str:
    """A rendered document's page; `current` is its file name, or None for a
    README shown as its directory's page."""
    heading = "" if rendered.titled else f"<h1>{html.escape(rendered.title)}</h1>\n"
    return compose_page(
        repo.name,
        page_dir,
        current,
        rendered.title,
        heading + rendered.body,
        linkable,
        footer,
    )


def listing_page(
    repo: Repository,
    rel: str,
    entries: list[tuple[str, bool]],
    linkable: Callable[[str], bool],
    footer: str = "",
) -> str:
    rows = []
    for name, is_dir in entries:
        stat = repo.path(join_rel(rel, name)).stat()
        size = "" if is_dir else f"{stat.st_size:,}"
        when = time.strftime("%Y-%m-%d %H:%M", time.localtime(stat.st_mtime))
        label = name + ("/" if is_dir else "")
        href = quote(name) + ("/" if is_dir else "")
        rows.append(
            f'<tr><td><a href="{href}">{html.escape(label)}</a></td>'
            f'<td class="num">{size}</td><td class="dim">{when}</td></tr>'
        )
    title = f"{rel or repo.name}/"
    table = (
        f'<h1>{html.escape(title)}</h1>\n<table class="listing"><thead><tr><th>Name</th><th>Bytes</th>'
        f"<th>Modified</th></tr></thead><tbody>{''.join(rows)}</tbody></table>"
        if rows
        else f'<h1>{html.escape(title)}</h1><p class="dim">No files.</p>'
    )
    return compose_page(repo.name, rel, None, title, table, linkable, footer)


def with_access_keeper(page: str, token: str | None) -> str:
    """Insert the address-bar token keeper (and a server-checked token) into a served page."""
    meta = f'<meta name="ya-access" content="{html.escape(token)}">\n' if token else ""
    insert = meta + ACCESS_KEEPER + "\n"
    head = re.search(r"</head\s*>", page, re.IGNORECASE)
    return (
        page[: head.start()] + insert + page[head.start() :] if head else insert + page
    )


class ProjectPages:
    """Pages a project's `--pages FILE:FUNCTION` hook generates, such as dashboards.

    FUNCTION(repo_root: Path) returns {repository-relative path: complete HTML}.
    Pages are seeds of the reachable set and win over repository files at the
    same path. They are regenerated on request once older than `max_age`, and
    at once when FILE changes: an edited generator is reloaded without a
    restart. A reload that fails keeps the previous generator and says why."""

    def __init__(self, spec: str | None, repo: Repository, max_age: float):
        self.repo, self.max_age = repo, max_age
        self.function: Callable[[Path], Mapping[str, str]] | None = None
        self.pages: dict[str, str] = {}
        self.made = float("-inf")
        self._lock = threading.Lock()
        if spec:
            file, sep, self.name = spec.rpartition(":")
            if not sep or not file or not self.name:
                raise RepoViewError(f"--pages wants FILE:FUNCTION, got {spec!r}")
            self.file = (repo.root / file).resolve()
            sys.path.insert(0, str(self.file.parent))
            self.loaded_stamp = self.file.stat().st_mtime_ns
            self.function = self._load()

    def _load(self) -> Callable[[Path], Mapping[str, str]]:
        module_spec = importlib.util.spec_from_file_location(
            f"repo_view_pages_{self.file.stem}", self.file
        )
        if module_spec is None or module_spec.loader is None:
            raise RepoViewError(f"--pages: cannot load {self.file}")
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        function = getattr(module, self.name, None)
        if not callable(function):
            raise RepoViewError(f"--pages: {self.file} has no function {self.name}")
        return function

    def _reload_if_edited(self) -> bool:
        stamp = self.file.stat().st_mtime_ns
        if stamp == self.loaded_stamp:
            return False
        self.loaded_stamp = stamp
        try:
            self.function = self._load()
        except Exception as error:  # noqa: BLE001 -- an edit in progress must not take the view down
            log(
                "pages",
                f"kept the previous generator; reloading {self.file.name} failed: {error!r}",
            )
            return False
        log("pages", f"reloaded {self.file.name}")
        return True

    def current(self) -> dict[str, str]:
        if self.function is None:
            return self.pages
        with self._lock:
            if self._reload_if_edited() or time.monotonic() - self.made > self.max_age:
                started = time.monotonic()
                pages = dict(self.function(self.repo.root))
                for rel in pages:
                    if link_target("", rel) != rel or not rel:
                        raise RepoViewError(
                            f"--pages returned an invalid page path {rel!r}"
                        )
                self.pages, self.made = pages, time.monotonic()
                log(
                    "pages", f"{len(pages)} project pages in {self.made - started:.2f}s"
                )
            return self.pages


class LinkGraph:
    """Which repository paths link to which, over pages, documents, HTML, CSS
    and directories; each file's links are cached by its stat."""

    def __init__(self, repo: Repository, pages: ProjectPages):
        self.repo, self.pages = repo, pages
        self._files: dict[str, tuple[tuple[int, int], frozenset[str]]] = {}

    def canonical(self, rel: str) -> str | None:
        """The servable node a path names: a project page, an existing path, or
        a static-site alias (`x.md.html` for `x.md`, `d/index.html` for `d`)."""
        if rel in self.pages.current() or self.repo.kind(rel):
            return rel
        if (
            rel.endswith(".html")
            and is_document(rel[:-5])
            and self.repo.kind(rel[:-5]) == "file"
        ):
            return rel[:-5]
        if (rel == "index.html" or rel.endswith("/index.html")) and self.repo.kind(
            parent_rel(rel)
        ) == "dir":
            return parent_rel(rel)
        return None

    def directory_document(self, rel: str) -> DirectoryDocument:
        index = join_rel(rel, "index.html")
        if index in self.pages.current():
            return DirectoryDocument("page", index)
        if self.repo.kind(index) == "file":
            return DirectoryDocument("index", index)
        readme = join_rel(rel, "README.md")
        if self.repo.kind(readme) == "file":
            return DirectoryDocument("readme", readme)
        return DirectoryDocument("listing")

    def resolve(self, base_dir: str, urls: Iterable[str]) -> frozenset[str]:
        found = set()
        for url in urls:
            target = link_target(base_dir, url)
            node = self.canonical(target) if target is not None else None
            if node is not None:
                found.add(node)
        return frozenset(found)

    def links(self, rel: str) -> frozenset[str]:
        page = self.pages.current().get(rel)
        if page is not None:
            return self.resolve(parent_rel(rel), link_urls(page, ".html"))
        kind = self.repo.kind(rel)
        if kind == "dir":
            document = self.directory_document(rel)
            if document.rel is not None:
                return frozenset({document.rel})
            return frozenset(join_rel(rel, name) for name, _ in self.repo.listing(rel))
        suffix = Path(rel).suffix.lower()
        if kind != "file" or suffix not in LINKING_SUFFIXES:
            return frozenset()
        stat = self.repo.path(rel).stat()
        stamp = (stat.st_mtime_ns, stat.st_size)
        cached = self._files.get(rel)
        if cached and cached[0] == stamp:
            return cached[1]
        text = self.repo.path(rel).read_text(encoding="utf-8", errors="replace")
        found = self.resolve(parent_rel(rel), link_urls(text, suffix))
        self._files[rel] = (stamp, found)
        return found


def seed_nodes(graph: LinkGraph, roots: list[str]) -> list[str]:
    """`--root` paths as servable nodes; a path that names nothing is an error."""
    nodes = []
    for root in roots:
        target = link_target("", root.strip("/"))
        node = graph.canonical(target) if target is not None else None
        if node is None:
            raise RepoViewError(f"--root names no servable path: {root}")
        nodes.append(node)
    return nodes


class Reachability:
    """Paths servable because links reach them from the seeds. The set only
    grows (graehl, 2026-10-15): a path stays servable after its last link goes.
    It is re-walked on demand, when an existing path is asked for but not in it."""

    def __init__(self, graph: LinkGraph, seeds: Callable[[], Iterable[str]]):
        self.graph, self.seeds = graph, seeds
        self.allowed: frozenset[str] = frozenset()
        self._walk = threading.Lock()

    def allows(self, rel: str) -> bool:
        if rel in self.allowed:
            return True
        self.walk()
        return rel in self.allowed

    def walk(self) -> None:
        with self._walk:
            started = time.monotonic()
            reached = set(self.seeds())
            frontier = list(reached | self.allowed)
            reached |= self.allowed
            while frontier:
                for target in self.graph.links(frontier.pop()) - reached:
                    reached.add(target)
                    frontier.append(target)
            self.allowed = frozenset(reached)
            log(
                "reach",
                f"{len(reached)} reachable paths in {time.monotonic() - started:.2f}s",
            )

    def admit_links_of(self, rel: str, links: Iterable[str]) -> None:
        """Allow a served page's current links at once; `rel` must be allowed."""
        if rel in self.allowed:
            self.allowed = self.allowed | frozenset(links)


@dataclass
class Reply:
    status: HTTPStatus
    kind: str = "text/plain; charset=utf-8"
    body: bytes = b""
    file: Path | None = None
    location: str | None = None
    page: bool = False  # generated by this tool: gets the access-link keeper


NOT_FOUND = Reply(HTTPStatus.NOT_FOUND, body=b"not found\n")


def html_reply(page: str) -> Reply:
    return Reply(
        HTTPStatus.OK, "text/html; charset=utf-8", page.encode("utf-8"), page=True
    )


def file_reply(path: Path) -> Reply:
    suffix = path.suffix.lower()
    kind = mimetypes.guess_type(path.name)[0]
    if suffix in PLAIN_TEXT_SUFFIXES or suffix in DOCUMENT_FORMATS or kind is None:
        kind = "text/plain"
    if kind.startswith("text/") or kind in (
        "application/json",
        "image/svg+xml",
        "application/javascript",
    ):
        kind += "; charset=utf-8"
    return Reply(HTTPStatus.OK, kind, file=path)


def slash_redirect(parts: list[str], query: str) -> Reply:
    # Relative, so it is right under any base path a proxy adds.
    return Reply(
        HTTPStatus.FOUND,
        location=quote(parts[-1]) + "/" + (f"?{query}" if query else ""),
    )


class LiveSite:
    """Serves the repository itself, rendering documents on request."""

    def __init__(
        self,
        repo: Repository,
        renderer: Renderer,
        pages: ProjectPages,
        roots: list[str],
    ):
        self.repo, self.renderer, self.pages = repo, renderer, pages
        self.graph = LinkGraph(repo, pages)
        self.roots = seed_nodes(self.graph, roots)
        self.reach = Reachability(
            self.graph, lambda: ["", *self.pages.current(), *self.roots]
        )

    def linkable(self, rel: str) -> bool:
        return rel in self.reach.allowed

    def respond(self, parts: list[str], slash: bool, query: str) -> Reply:
        rel = "/".join(parts)
        page = self.pages.current().get(rel)
        if page is not None:
            self.reach.admit_links_of(rel, self.graph.links(rel))
            return html_reply(page)
        node = self.graph.canonical(rel)
        if node is None:
            return NOT_FOUND
        kind = self.repo.kind(node)
        if kind == "dir" and node == rel and parts and not slash:
            return slash_redirect(parts, query)
        if not self.reach.allows(node):
            return NOT_FOUND
        self.reach.admit_links_of(node, self.graph.links(node))
        if kind == "dir":
            return self.directory(node)
        if is_document(node):
            rendered = self.renderer.render(node)
            self.reach.admit_links_of(
                node,
                self.graph.resolve(parent_rel(node), link_urls(rendered.body, ".html")),
            )
            name = node.rpartition("/")[2]
            return html_reply(
                document_page(
                    self.repo, rendered, parent_rel(node), name, self.linkable
                )
            )
        return file_reply(self.repo.path(node))

    def directory(self, rel: str) -> Reply:
        document = self.graph.directory_document(rel)
        if document.kind == "page":
            return html_reply(self.pages.current()[document.rel])
        if document.kind == "index":
            return file_reply(self.repo.path(document.rel))
        if document.kind == "readme":
            rendered = self.renderer.render(document.rel)
            self.reach.admit_links_of(
                rel, self.graph.resolve(rel, link_urls(rendered.body, ".html"))
            )
            return html_reply(
                document_page(self.repo, rendered, rel, None, self.linkable)
            )
        return html_reply(
            listing_page(self.repo, rel, self.repo.listing(rel), self.linkable)
        )


class StaticSite:
    """Serves a site `build` wrote, as a whole: nothing outside it, no rendering."""

    def __init__(self, site: Path):
        self.root = site.resolve()
        manifest = self.root / MANIFEST
        if not manifest.is_file():
            raise RepoViewError(f"{site} has no {MANIFEST}; run `build` first")
        self.pages = frozenset(
            json.loads(manifest.read_text(encoding="utf-8"))["pages"]
        )

    def respond(self, parts: list[str], slash: bool, query: str) -> Reply:
        rel = "/".join(parts)
        path = self.root / rel if rel else self.root
        if path.is_dir():
            if parts and not slash:
                return slash_redirect(parts, query)
            rel, path = join_rel(rel, "index.html"), path / "index.html"
        elif not path.exists() and is_document(rel):
            rel, path = rel + ".html", path.with_name(path.name + ".html")
        try:
            if (
                not path.resolve(strict=True).is_relative_to(self.root)
                or not path.is_file()
            ):
                return NOT_FOUND
        except OSError:
            return NOT_FOUND
        if rel in self.pages:
            return html_reply(path.read_text(encoding="utf-8"))
        return file_reply(path)


class AccessToken:
    """The private-link token pages show, and check under `--require-access`.

    Read on demand from `--access-token-file` (its whole text), else from the
    top-level `yaAccess` string of `.project-template/app.json`, which YA may
    write while the app's link is private and clear otherwise. Re-read when the
    file changes, so a rotated token revokes old links at once."""

    def __init__(self, repo: Repository, token_file: Path | None):
        self.file = token_file or repo.root / ".project-template" / "app.json"
        self.from_app = token_file is None
        self._stamp: int | None = None
        self._token: str | None = None

    def current(self) -> str | None:
        try:
            stamp = self.file.stat().st_mtime_ns
        except FileNotFoundError:
            stamp = None
        if stamp != self._stamp:
            self._stamp, self._token = (
                stamp,
                self._read() if stamp is not None else None,
            )
        return self._token

    def _read(self) -> str | None:
        text = self.file.read_text(encoding="utf-8")
        if not self.from_app:
            return text.strip() or None
        token = json.loads(text).get("yaAccess")
        if token is not None and not isinstance(token, str):
            raise RepoViewError(f"{self.file}: yaAccess must be a string")
        return token or None

    def admits(self, supplied: str | None) -> bool:
        token = self.current()
        return bool(token and supplied) and hmac.compare_digest(
            supplied.encode(), token.encode()
        )


def make_handler(
    site: LiveSite | StaticSite, base: str, access: AccessToken, require_access: bool
):
    class RepoViewRequest(BaseHTTPRequestHandler):
        server_version = "repo-view/1"

        def log_message(self, fmt, *args):
            log("request", fmt % args)

        def do_HEAD(self):
            self.do_GET(head=True)

        def do_GET(self, head: bool = False):
            split = urlsplit(self.path)
            raw = unquote(split.path)
            if base and (raw == base or raw.startswith(base + "/")):
                raw = raw[len(base) :] or "/"
            if raw == "/healthz":
                return self.send(Reply(HTTPStatus.OK, body=b"ok\n"), head)
            cookie = None
            try:
                token = access.current()
            except (OSError, ValueError, RepoViewError) as error:
                log("access", f"token unreadable: {error}")
                return self.send(
                    Reply(
                        HTTPStatus.SERVICE_UNAVAILABLE,
                        body=b"access token unreadable\n",
                    ),
                    head,
                )
            if require_access:
                supplied = parse_qs(split.query).get(ACCESS_QUERY, [None])[0]
                if access.admits(supplied):
                    secure = (
                        "; Secure"
                        if self.headers.get("X-Forwarded-Proto") == "https"
                        else ""
                    )
                    cookie = f"{ACCESS_COOKIE}={supplied}; Path=/; HttpOnly; SameSite=Lax{secure}"
                elif not access.admits(self.cookie(ACCESS_COOKIE)):
                    return self.send(
                        Reply(HTTPStatus.UNAUTHORIZED, body=b"App link required\n"),
                        head,
                    )
            parts = [p for p in raw.split("/") if p]
            if any(p.startswith(".") for p in parts):
                return self.send(NOT_FOUND, head)
            try:
                reply = site.respond(parts, raw.endswith("/"), split.query)
            except RepoViewError as error:
                log("request", str(error))
                reply = Reply(
                    HTTPStatus.INTERNAL_SERVER_ERROR, body=f"{error}\n".encode()
                )
            if reply.page:
                page = with_access_keeper(reply.body.decode("utf-8"), token)
                reply = Reply(reply.status, reply.kind, page.encode("utf-8"))
            return self.send(reply, head, cookie)

        def cookie(self, name: str) -> str | None:
            jar = SimpleCookie()
            try:
                jar.load(self.headers.get("Cookie", ""))
            except CookieError:
                return None
            return jar[name].value if name in jar else None

        def send(self, reply: Reply, head: bool, cookie: str | None = None):
            size = reply.file.stat().st_size if reply.file else len(reply.body)
            self.send_response(reply.status)
            self.send_header("Content-Type", reply.kind)
            self.send_header("Content-Length", str(size))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            if reply.location:
                self.send_header("Location", reply.location)
            if cookie:
                self.send_header("Set-Cookie", cookie)
            self.end_headers()
            if head:
                return
            if reply.file:
                with reply.file.open("rb") as source:
                    shutil.copyfileobj(source, self.wfile)
            else:
                self.wfile.write(reply.body)

    return RepoViewRequest


def static_links(
    page: str, page_dir: str, documents: set[str], directories: set[str]
) -> str:
    """Point a page's links at static-site names: `x.md` → `x.md.html`, `d/` → `d/index.html`."""

    def relink(match: re.Match) -> str:
        attr = match.group(1)
        url = html.unescape(
            match.group(2) if match.group(2) is not None else match.group(3)
        )
        target = link_target(page_dir, url)
        cut = min(
            (i for i in (url.find("?"), url.find("#")) if i >= 0), default=len(url)
        )
        path, rest = url[:cut], url[cut:]
        if target in documents:
            path += ".html"
        elif target in directories:
            path = (path if path.endswith("/") else path + "/") + "index.html"
        else:
            return match.group(0)
        return f'{attr}="{html.escape(path + rest)}"'

    return HTML_LINK.sub(relink, page)


def build_site(
    repo: Repository, pages: ProjectPages, roots: list[str], site: Path, max_bytes: int
) -> dict:
    """Write the reachable closure as a static site into `site`, replacing it atomically."""
    renderer = Renderer(repo, require_pandoc=True)
    graph = LinkGraph(repo, pages)
    project_pages = pages.current()
    seeds = ["", *project_pages, *seed_nodes(graph, roots)]
    reached: set[str] = set()
    frontier = list(dict.fromkeys(seeds))
    reached.update(frontier)
    documents: dict[str, Rendered] = {}
    directories: dict[str, DirectoryDocument] = {}
    assets: set[str] = set()
    while frontier:
        rel = frontier.pop()
        if rel in project_pages:
            links = graph.links(rel)
        elif repo.kind(rel) == "dir":
            directories[rel] = document = graph.directory_document(rel)
            if document.kind == "readme":
                rendered = documents.setdefault(
                    document.rel, renderer.render(document.rel)
                )
                links = graph.resolve(rel, link_urls(rendered.body, ".html"))
            else:
                links = graph.links(rel)
        elif is_document(rel):
            documents[rel] = rendered = renderer.render(rel)
            links = graph.resolve(parent_rel(rel), link_urls(rendered.body, ".html"))
        else:
            assets.add(rel)
            links = graph.links(rel)
        for target in links - reached:
            reached.add(target)
            frontier.append(target)

    generated = time.strftime("%Y-%m-%d %H:%M %Z")
    footer = f"Generated {html.escape(generated)} by repo_view.py"
    linked_dirs = set(directories)
    linked_docs = {rel for rel in documents if rel in reached}
    linkable = linked_dirs.__contains__
    outputs: dict[str, str] = {}
    for rel, page in project_pages.items():
        outputs[rel] = static_links(page, parent_rel(rel), linked_docs, linked_dirs)
    for rel in linked_docs:
        page = document_page(
            repo,
            documents[rel],
            parent_rel(rel),
            rel.rpartition("/")[2],
            linkable,
            footer,
        )
        outputs[rel + ".html"] = static_links(
            page, parent_rel(rel), linked_docs, linked_dirs
        )
    for rel, document in directories.items():
        index = join_rel(rel, "index.html")
        if document.kind == "readme":
            page = document_page(
                repo, documents[document.rel], rel, None, linkable, footer
            )
        elif document.kind == "listing":
            page = listing_page(repo, rel, repo.listing(rel), linkable, footer)
        else:
            continue  # a project page or the directory's own index.html is already written
        outputs[index] = static_links(page, rel, linked_docs, linked_dirs)
    clashes = sorted(set(outputs) & assets)
    if clashes:
        raise RepoViewError(
            f"generated pages would replace linked files: {', '.join(clashes[:5])}"
        )

    staging = site.with_name(site.name + ".new")
    if staging.exists():
        shutil.rmtree(staging)
    total = 0
    try:
        for rel, page in outputs.items():
            data = page.encode("utf-8")
            total += len(data)
            out = staging / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(data)
        for rel in sorted(assets):
            source = repo.path(rel)
            total += source.stat().st_size
            if total > max_bytes:
                raise RepoViewError(
                    f"site exceeds --max-bytes {max_bytes} at {rel}; nothing replaced"
                )
            out = staging / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            try:
                os.link(source.resolve(), out)
            except OSError as error:
                if error.errno not in (errno.EXDEV, errno.EPERM, errno.EMLINK):
                    raise
                shutil.copy2(source.resolve(), out)
        if total > max_bytes:
            raise RepoViewError(
                f"site exceeds --max-bytes {max_bytes}; nothing replaced"
            )
        manifest = {"version": 1, "generated": generated, "pages": sorted(outputs)}
        (staging / MANIFEST).write_text(
            json.dumps(manifest, indent=1) + "\n", encoding="utf-8"
        )
        repo.ensure_excluded(site)
        retired = site.with_name(site.name + ".old")
        if retired.exists():
            shutil.rmtree(retired)
        if site.exists():
            site.rename(retired)
        staging.rename(site)
        if retired.exists():
            shutil.rmtree(retired)
    except BaseException:
        if staging.exists():
            shutil.rmtree(staging)
        raise
    return {
        "site": str(site),
        "pages": len(outputs),
        "files": len(assets),
        "bytes": total,
    }


def enable(
    repo: Repository, static: bool, replace: bool, site: Path, serve_args: list[str]
) -> Path:
    """Declare the repository view as the project's YA app, keeping other app.json fields."""
    app_path = repo.root / ".project-template" / "app.json"
    app = json.loads(app_path.read_text(encoding="utf-8")) if app_path.exists() else {}
    current = "service" if "service" in app else "kind" if "kind" in app else None
    if current and not replace:
        raise RepoViewError(
            f"{app_path.relative_to(repo.root)} already declares an app ({current!r}); "
            "pass --replace to make the repository view this project's app instead"
        )
    if static:
        root = site.resolve().relative_to(repo.root).as_posix()
        service = {
            "version": 1,
            "where": {"kind": "static", "root": root, "entry": "index.html"},
            "serving": {"target": "static-root"},
        }
    else:
        if not Path(__file__).resolve().is_relative_to(repo.root):
            raise RepoViewError(
                f"run enable with the copy of {Path(__file__).name} vendored in this repository"
            )
        script = Path(__file__).resolve().relative_to(repo.root).as_posix()
        service = {
            "version": 1,
            "where": {"kind": "process", "cwd": ".", "entry": "/"},
            "start": {
                "argv": ["python3", script, "serve", *serve_args],
                "portEnv": "PORT",
            },
            "status": {
                "probe": "http",
                "path": "/healthz",
                "readyStatus": 200,
                "startupTimeoutMs": 30000,
            },
            "stop": {"signal": "SIGTERM", "graceMs": 3000},
            "serving": {"target": "sandbox-loopback", "protocol": "http"},
        }
    app["service"] = service
    app_path.parent.mkdir(parents=True, exist_ok=True)
    app_path.write_text(json.dumps(app, indent=2) + "\n", encoding="utf-8")
    repo.ensure_excluded(site)
    return app_path


def log(phase: str, message: str) -> None:
    sys.stderr.write(f"[{phase}] {message}\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    verbs = parser.add_subparsers(dest="verb", required=True)

    def add_seed_options(command: argparse.ArgumentParser) -> None:
        command.add_argument(
            "--root", action="append", default=None, metavar="PATH",
            help="another repository path to serve and follow links from (repeatable)",
        )  # fmt: skip
        command.add_argument(
            "--pages", metavar="FILE:FUNCTION",
            help="project page generator: FUNCTION(repo_root) returns {relative path: HTML}",
        )  # fmt: skip

    serve = verbs.add_parser(
        "serve", help="serve documents live (or a built site with --static)"
    )
    add_seed_options(serve)
    serve.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("PORT") or 0),
        help="default: $PORT",
    )
    serve.add_argument(
        "--base-path",
        default=os.environ.get("BASE_PATH", ""),
        help="URL prefix a proxy adds",
    )
    serve.add_argument(
        "--pages-max-age",
        type=float,
        default=10.0,
        help="seconds before --pages regenerates",
    )
    serve.add_argument(
        "--static",
        action="store_true",
        help="serve the built --site as a whole instead",
    )
    serve.add_argument(
        "--site",
        type=Path,
        default=Path(DEFAULT_SITE),
        help="built site directory for --static",
    )
    serve.add_argument(
        "--access-token-file", type=Path,
        help="read the private-link token from this file instead of app.json's yaAccess",
    )  # fmt: skip
    serve.add_argument(
        "--require-access", action="store_true",
        help="check the token (?ya_access= or cookie) here; only where no YA proxy checks and strips it",
    )  # fmt: skip

    build = verbs.add_parser(
        "build", help="write the reachable closure as a static site"
    )
    add_seed_options(build)
    build.add_argument(
        "--site",
        type=Path,
        default=Path(DEFAULT_SITE),
        help=f"output directory (default {DEFAULT_SITE})",
    )
    build.add_argument(
        "--max-bytes",
        type=int,
        default=1 << 30,
        help="refuse a larger site (default 1 GiB)",
    )

    enable_verb = verbs.add_parser(
        "enable", help="declare the view as this project's YA app"
    )
    enable_verb.add_argument(
        "--static",
        action="store_true",
        help="declare the built --site, not the live server",
    )
    enable_verb.add_argument(
        "--replace", action="store_true", help="replace an existing app declaration"
    )
    enable_verb.add_argument("--site", type=Path, default=Path(DEFAULT_SITE))
    enable_verb.add_argument(
        "serve_args", nargs=argparse.REMAINDER, help="after --: extra `serve` arguments"
    )

    args = parser.parse_args(argv)
    try:
        repo = Repository.containing(Path.cwd())
        site = args.site if args.site.is_absolute() else repo.root / args.site
        if args.verb == "enable":
            extra = (
                args.serve_args[1:]
                if args.serve_args[:1] == ["--"]
                else args.serve_args
            )
            path = enable(repo, args.static, args.replace, site, extra)
            print(
                f"[enable] declared the repository view in {path.relative_to(repo.root)}"
            )
            return 0
        # A build is one snapshot: its project pages are generated once.
        pages = ProjectPages(
            args.pages, repo, getattr(args, "pages_max_age", float("inf"))
        )
        if args.verb == "build":
            summary = build_site(repo, pages, args.root or [], site, args.max_bytes)
            print(
                f"[build] {summary['pages']} pages and {summary['files']} files, {summary['bytes']:,} bytes, in {site}"
            )
            return 0
        if not args.port:
            raise RepoViewError("no port: pass --port or set PORT")
        access = AccessToken(repo, args.access_token_file)
        if args.require_access and not access.current():
            raise RepoViewError(
                "--require-access needs a token: none in --access-token-file or app.json yaAccess"
            )
        if args.static:
            served: LiveSite | StaticSite = StaticSite(site)
        else:
            renderer = Renderer(repo, require_pandoc=False)
            if not renderer.pandoc:
                log("serve", "pandoc not found; documents will show as source text")
            served = LiveSite(repo, renderer, pages, args.root or [])
        handler = make_handler(
            served, args.base_path.rstrip("/"), access, args.require_access
        )
        server = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
        mode = f"static site {site}" if args.static else "live"
        log("serve", f"{repo.root} ({mode}) on 127.0.0.1:{server.server_port}")
        server.serve_forever()
    except RepoViewError as error:
        log(args.verb, str(error))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
