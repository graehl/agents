# Program dashboards

`scripts/program_view.py` adds program dashboards to the repository web view
(`instructions/repo-view.md`): one page listing the project's programs, nested
by parent, and a papers page for each program that has papers. It reads the
repository as the `project-directory` conventions lay it out
(`~/agents/topics/project-directory.md`): put a document where those
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
- open gaps.

Long lists fold behind "N more". Each program's summary row has "expand all"
and "collapse all" buttons for it and everything nested in it, and the page
has the same pair for all programs. Expanding a program also opens its
ancestors, and an outline link opens the program it points to. The
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
`--pages-max-age`, and at once after `program_view.py` is edited.
