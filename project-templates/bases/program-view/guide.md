# Program dashboards

`scripts/program_view.py` adds program dashboards to the repository web view
(`instructions/repo-view.md`): one page listing the project's programs, nested
by parent, and a papers page for each program that has papers. It reads the
repository as the project directory conventions lay it out
(`instructions/project-directory.md`): put a document where those
conventions say and the dashboard finds it; there is no registry to update.

## Turn it on

Pass the generator to the view:

```sh
python3 scripts/repo_view.py serve --pages scripts/program_view.py:pages
python3 scripts/repo_view.py enable -- --pages scripts/program_view.py:pages
```

The first serves it once; the second makes it the project's YA app. The
dashboard replaces the root page, and every document it links is served
rendered. `python3 scripts/program_view.py` prints what each program holds,
which checks discovery without a browser.

## What it shows

Per program: the charter's title and first paragraph, the focus heading of
its `ROOT.md`, and links to its charter, glossary, papers page, paper
proposals, newest handout, report, topics, gaps and sketches. Beside the
description sit its last commit (with `Contributing-model:` trailers and the
agentctl session that made it), uncommitted files, newest handoff, and live
agent sessions whose `.agentctl/active` scope lies inside it. Below, a
full-width row of expandable lists shows:
- papers, linked to their built HTML when available, otherwise their source;
- field surveys, including those without a program charter;
- sketches (`gaps/sketches/`), with each sketch's title as its tooltip;
- handouts;
- paper skeletons;
- other documents in the program's directory;
- open gaps and private handoffs.

Newest activity comes first, including each program's descendants. Choose
**A–Z** for alphabetical order, and **Flat** for one list of programs without
nesting. Flat programs retain clickable parent breadcrumbs. The TOC follows
the same ordering. Document date labels remain their publication dates when
the filename supplies one; activity uses the last commit, or file modification
time for uncommitted and private files.

The initial age cutoff is seven days. Enter a duration (`7`, `7d`, `12h`,
`2w`) or a UTC date (`MM-DD` in the current year, or `YYYY-MM-DD`), or use the
days slider. Older items and programs stay available behind counted folds.
The kind buttons toggle previews everywhere in the dashboard. **Expand all
items** opens older content and every "N more" list; **Reapply age cutoff**
restores the selected age and kind settings. All documents remain searchable
and expandable, including those beyond the initial preview limit.

Search filters program names, paths, document titles and kinds as you type,
including collapsed content. Matching files expand temporarily; clearing
search restores the age and kind settings. `/` focuses search and `Esc`
clears it. A breadcrumb to a parent excluded by search clears the query and
reveals that parent. Hovering or focusing a document link shows a bounded
plain-text source excerpt when available; `Esc` dismisses it.

On wide screens controls follow the TOC in the left rail. On narrow screens
they precede it, and an opening without a fragment scrolls to the TOC;
scroll up or select **Controls** to reach them. Each program's summary retains
expand/collapse buttons for its currently displayed branch. An outline link
opens the program it points to and its ancestors. The
repository root is the root program even without a `PROGRAM.md`. The
shallowest `ROOT.md` focus heads the page as the project's current focus.

The papers page lists each `papers/<slug>/index.qmd` project below the
program: built outputs, latest `CHANGELOG.md` entry, last commit, open
`` `TBD` `` count in its section fragments, and live sessions; then the field
surveys below the program with their manifest sizes.

## Optional sections

Papers, surveys, handouts, documents and live sessions appear only when the
repository holds them. `.project-template/program-view.json` may give the page
a title and turn sections off:

```json
{ "title": "Research programs", "sections": { "documents": false, "sessions": false } }
```

Under `serve` the pages are regenerated on request once older than the view's
`--pages-max-age`, and at once after `program_view.py` is edited. Keep the
adjacent `program_view.js` and `program_view.css` with the Python generator;
it embeds them into each page so static builds need no additional requests.
