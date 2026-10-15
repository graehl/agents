# Project directory conventions

> Where a project's programs and their documents live, so that an agent
> browsing the repository and the program dashboard find each kind of
> document by its path and name, without a registry to keep current.

Topic: `project-directory`
Governs: choosing a path or name for a program's handout, report, paper or focus document, or changing what the program dashboard discovers

A document is registered by where it is and what it is called. Nothing lists
a program's handouts, papers or gaps except the directory itself, so a file
in the conventional place is found and a file elsewhere is not. The
`program-view` template base (`project-templates/bases/program-view/`)
implements this topic: change both together.

## Programs

The repository root is the root program, whether or not it has a
`PROGRAM.md`. Every other program is declared by a `PROGRAM.md` in its
directory; [TOPICS.md § Program scope charters](../TOPICS.md#program-scope-charters)
owns what a charter says and how programs inherit. A file belongs to the
nearest enclosing program, so a child program's files are not its parent's.
Discovery reads only files Git does not ignore, except private handoffs.

## Where each kind of document lives

Paths are relative to the owning program's directory.

| Kind | Path or name | Owner of the rules |
|---|---|---|
| Charter | `PROGRAM.md` | [TOPICS.md](../TOPICS.md#program-scope-charters) |
| Vocabulary | `GLOSSARY.md`, `GLOSSARY.agents.md` | [glossary](glossary.md) |
| Topic docs | `topics/<name>.md`; companions `topics/<name>.<suffix>.md` | [topic-doc-format](topic-doc-format.md) |
| Gaps and sketches | `gaps/<slug>.md`, `gaps/sketches/<slug>.md` | [gaps/README.md](../gaps/README.md) |
| Handoffs (private) | `handoffs/<scope>.md` | [handoffs](handoffs.md) |
| Handoff pointer | `ROOT`, one relative path to a handoff | [handoffs](handoffs.md) |
| Current focus | `ROOT.md`; its first `## ` heading is the focus | below |
| Paper proposals | `paper-proposals.md`, `paper-proposals/<form>-<focus>.md` | [paper-drafting](paper-drafting.md) |
| Papers | `papers/<slug>/index.qmd` (built project), `papers/<slug>.md` (skeleton) | [paper-projects](paper-projects.md) |
| Field surveys | `surveys/<field>/survey.md`, `surveys/<field>/related-work/papers.yaml` | [research-survey](research-survey.md) |
| Handouts | `<slug>-handout.md`, `handouts/<slug>.md`, `[<slug>-]progress-YYYY-MM-DD.md` | [handout-writing](handout-writing.md), [progress-report](progress-report.md) |
| Built report | `report.html` | [document-writing](document-writing.md) |

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
The research workflow's `research/ROOT.md` (cross-program triage for
autonomous research, [_RESEARCH/workflow.md](../_RESEARCH/workflow.md)) is
this file for a project's research program. The shallowest `ROOT.md` below
the root is the project's current focus. Keep a program's durable aims in its
charter and its live state in handoffs; `ROOT.md` is the short, revisable
pointer between them.

## Dated names

A `YYYY-MM-DD` in a file name is the document's own date, and views sort and
label by it: a move or a later typo fix does not make an old progress report
new. Undated documents sort by their last commit.

## Browsing

Served through the repository web view (`project-templates/bases/repo-view/`),
every Markdown document renders at its own path and a directory without an
`index.html` or `README.md` shows its file listing, so `topics/`, `gaps/` and
`gaps/sketches/` are browsable as soon as a dashboard or document links them.
The program dashboard joins each program to its last commit (with
`Contributing-model:` trailers and the agentctl session note), uncommitted
files, and live sessions whose `.agentctl/active` scope lies inside it.
