# Project directory conventions

Where this project's programs and their documents live, so that an agent
browsing the repository and the program dashboard (`scripts/program_view.py`)
find each kind of document by its path and name. Nothing lists a program's
handouts, papers or gaps except the directory itself: a file in the
conventional place is found, and a file elsewhere is not.

## Programs

The repository root is the root program, whether or not it has a
`PROGRAM.md`. Every other program is declared by a `PROGRAM.md` in its
directory, whose title and first paragraph describe it. A file belongs to the
nearest enclosing program, so a child program's files are not its parent's.
Discovery reads only files Git does not ignore, except private handoffs.

## Where each kind of document lives

Paths are relative to the owning program's directory.

| Kind | Path or name |
|---|---|
| Charter | `PROGRAM.md` |
| Vocabulary | `GLOSSARY.md`, `GLOSSARY.agents.md` |
| Topic docs | `topics/<name>.md`; companions `topics/<name>.<suffix>.md` |
| Gaps and sketches | `gaps/<slug>.md`, `gaps/sketches/<slug>.md` |
| Handoffs (private) | `handoffs/<scope>.md` |
| Handoff pointer | `ROOT`, one relative path to a handoff |
| Current focus | `ROOT.md`; its first `## ` heading is the focus |
| Paper proposals | `paper-proposals.md`, `paper-proposals/<form>-<focus>.md` |
| Papers | `papers/<slug>/index.qmd` (built project), `papers/<slug>.md` (skeleton) |
| Field surveys | `surveys/<field>/survey.md`, `surveys/<field>/related-work/papers.yaml` |
| Handouts | `<slug>-handout.md`, `handouts/<slug>.md`, `[<slug>-]progress-YYYY-MM-DD.md` |
| Built report | `report.html` |

Any other Markdown directly in a program directory is one of its documents —
a design document, a standalone paper effort, a note — except its running log
(`<name>.log.md`), appendix (`<name>.appendix.md`), reproduction rider
(`<name>.repro.md`), `README.md`, `CHANGELOG.md` and agent instruction files.
A document that names another kind takes a different name: a review of a
handout is `<slug>-handout-review.md`, which is not a handout.

## Current focus: `ROOT.md`

A program's `ROOT.md` states the current focus across that program and its
children; its first `## ` heading names the focus and its date, and the body
says which child programs and threads are active and points to their records.
The shallowest `ROOT.md` below the root is the project's current focus. Keep a
program's durable aims in its charter and its live state in handoffs;
`ROOT.md` is the short, revisable pointer between them.

## Dated names

A `YYYY-MM-DD` in a file name is the document's own date, and views sort and
label by it: a move or a later typo fix does not make an old progress report
new. Undated documents sort by their last commit.
