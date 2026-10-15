#!/usr/bin/env python3
"""Program dashboards for a repository, served or built by `repo_view.py --pages`.

`pages(root)` returns `index.html`, the project's programs nested by parent,
and `<program>/papers-index.html` for each program with papers. The repository
root is the root program whether or not it has a `PROGRAM.md`; every other
program is declared by one. Each program shows what the `project-directory`
conventions place in its directory: charter, glossary, `ROOT.md` focus,
handoffs, topics, gaps and sketches, and optionally papers, field surveys,
handouts and other documents, with the last commit (its `Contributing-model:`
trailers and the agentctl session note), uncommitted files, and live agent
sessions whose `.agentctl/active` scope lies inside it.

Optional sections appear only when the repository holds their files; an
optional `.project-template/program-view.json` may set `"title"` and turn
sections off, e.g. `{"sections": {"documents": false}}`.

    python3 scripts/repo_view.py serve --pages scripts/program_view.py:pages
    python3 scripts/program_view.py [ROOT]   # print what each program holds
"""

from __future__ import annotations

import html
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

SECTIONS = ("papers", "surveys", "handouts", "documents", "sessions")
ACTIVE_WINDOW_S = 70 * 60
DOCUMENT_LIMIT = 15
SESSION_ID = re.compile(
    r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b"
)
PROGRESS_REPORT = re.compile(r"(^|-)progress-\d{4}-\d{2}-\d{2}\.md$")
TOPIC_COMPANION = re.compile(
    r"\.(evidence|bearings|testing|sketches|mandatory-reread(\.recursive)?)\.md$"
)
# One `git ls-files` over these patterns instead of walking the tree, which
# would enter ignored environments and data. `*` crosses `/` in pathspecs.
PATTERNS = (
    "PROGRAM.md",
    "*/PROGRAM.md",
    "*GLOSSARY.md",
    "*ROOT.md",
    "*.md",
    "*/report.html",
    "*papers/*/index.qmd",
    "*surveys/*/related-work/papers.yaml",
)
# A program's own documents exclude these names, which other blocks show.
NOT_DOCUMENTS = re.compile(
    r"^(PROGRAM|GLOSSARY|GLOSSARY\.agents|ROOT|README|CHANGELOG|handoff|paper-proposals)\.md$"
    r"|^(AGENTS|CLAUDE)(\.[\w-]+)*\.md$|\.log\.md$|\.appendix\.md$|\.repro\.md$|-handout\.md$"
)
DATED_NAME = re.compile(r"(\d{4}-\d{2}-\d{2})")

# Palette and focus ring follow the page base's style.css.
STYLE = """
:root { color: #293e35; background: #f7f6f0; font: 15px/1.5 system-ui, sans-serif; font-synthesis: none; }
body { margin: 1.5rem auto; padding-inline: 1.5rem; max-width: 1400px; }
a { color: #2f6b52; text-underline-offset: 2px; } a:hover { color: #387c60; }
a:focus-visible { outline: 3px solid #387c60; outline-offset: 3px; }
h1 { font-size: 1.4rem; font-weight: 650; letter-spacing: -0.01em; margin: 0 0 .25rem; }
h2 { font-size: 1.1rem; margin-top: 1.7rem; }
table { border-collapse: collapse; width: 100%; }
th, td { text-align: left; vertical-align: top; padding: .45rem .6rem; border-bottom: 1px solid #dcded4; }
th { font-weight: 600; background: #ecebe2; } td.num { text-align: right; font-variant-numeric: tabular-nums; }
.dim { color: #637066; } .warn { color: #9a5b12; } code { font-size: .88em; }
.layout { display: grid; grid-template-columns: minmax(13rem, 17rem) minmax(0, 1fr); gap: 2rem; align-items: start; }
nav.outline { position: sticky; top: 1rem; max-height: calc(100vh - 2rem); overflow: auto; font-size: .9rem; }
nav.outline summary { font-weight: 600; cursor: pointer; }
nav.outline ul { list-style: none; margin: .2rem 0 0; padding-left: .9rem; border-left: 1px solid #cfd3c7; }
nav.outline ul.tree, nav.outline ul.extra { padding-left: 0; border: 0; }
nav.outline ul.extra { margin-top: .8rem; padding-top: .5rem; border-top: 1px solid #dcded4; }
nav.outline li { margin: .15rem 0; } nav.outline .live { color: #2f8a55; font-size: .8em; }
details.program { margin: .9rem 0 0; padding-left: 1rem; border-left: 3px solid #a9b9a3; }
details.program details.program { border-left-color: #cfd3c7; }
details.program > summary { cursor: pointer; display: flex; flex-wrap: wrap; align-items: baseline; gap: .25rem .6rem;
  padding: .2rem 0; list-style-position: outside; }
details.program > summary .name { font-weight: 650; font-size: 1.02rem; }
.chip { font-size: .8rem; padding: .05rem .5rem; border-radius: 999px; background: #ecebe2; color: #4c5c52; }
.chip.live { background: #dcefe2; color: #1f6b40; } .when { margin-left: auto; font-size: .85rem; }
.desc { max-width: 72ch; margin: .2rem 0 .3rem; color: #3c4f45; } .open { margin: 0 0 .5rem; }
.focus { margin: 0 0 .4rem; }
main { container-type: inline-size; }
.body { display: grid; grid-template-columns: minmax(0, 66ch) minmax(16rem, 1fr); gap: .2rem 2.5rem;
  align-items: start; }
.meta { display: flex; flex-direction: column; gap: .5rem; margin: .2rem 0 .5rem; }
.meta ul { list-style: none; margin: 0; padding: 0; } .meta li { margin: .05rem 0; }
.meta details summary { cursor: pointer; color: #637066; font-size: .85rem; }
@container (max-width: 62rem) { .body { display: block; }
  .meta { flex-direction: row; flex-wrap: wrap; gap: .4rem 2rem; }
  .meta .block { flex: 1 1 18rem; min-width: 0; } }
.meta h4 { margin: 0 0 .1rem; font-size: .72rem; font-weight: 650; letter-spacing: .06em; text-transform: uppercase;
  color: #637066; }
@media (max-width: 860px) { .layout { display: block; } nav.outline { position: static; max-height: none;
  margin-bottom: 1rem; padding: .5rem .75rem; background: #ecebe2; border-radius: 6px; } }
@media (max-width: 700px) { body { margin: 1rem auto; padding-inline: 1rem; }
  details.program { padding-left: .6rem; } .when { margin-left: 0; }
  table.dash, table.dash tr, table.dash td { display: block; }
  table.dash thead { display: none; } table.dash td { border: 0; padding: .2rem 0 !important; }
  td.num { text-align: left; } td[data-label]::before { content: attr(data-label) ": "; color: #637066; }
  table.dash tr { border-bottom: 1px solid #dcded4; padding: .6rem 0; } }
@media (prefers-color-scheme: dark) { :root { background: #1c1f1d; color: #e6ebe4; }
  th { background: #2a2f2b; } th, td, tr { border-color: #3a413c; }
  .dim { color: #a3ada5; } a { color: #8fcbab; }
  .chip { background: #2a2f2b; color: #c8d1c9; } .chip.live { background: #1f3a2a; color: #9fdcb5; }
  .desc { color: #c8d1c9; } details.program details.program { border-left-color: #3a413c; } }
"""


def git(repo: Path, *args: str) -> str:
    done = subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, check=True
    )
    return done.stdout.strip()


def esc(value: object) -> str:
    return html.escape(str(value))


def plural(count: int, noun: str, nouns: str = "") -> str:
    return f"{count} " + (noun if count == 1 else nouns or noun + "s")


def is_handout(rel: str) -> bool:
    """A handout by name: `<slug>-handout.md`, anything under `handouts/`, or a
    dated progress report `[<slug>-]progress-YYYY-MM-DD.md`."""
    path = Path(rel)
    return (
        path.suffix == ".md"
        and (
            path.name.endswith("-handout.md")
            or "handouts" in path.parts[:-1]
            or bool(PROGRESS_REPORT.search(path.name))
        )
        and "related-work" not in path.parts
    )


class Project:
    """One `git ls-files` listing of the repository, and Git facts about its paths."""

    def __init__(self, root: Path):
        self.root = root
        listed = git(root, "ls-files", "-co", "--exclude-standard", "--", *PATTERNS)
        self.files = sorted(set(listed.splitlines()))
        self.changed = [
            line[3:].split(" -> ")[-1].strip('"')
            for line in git(
                root, "status", "--porcelain", "--untracked-files=normal"
            ).splitlines()
            if "/_build/" not in line
        ]
        self._commits: dict[str, dict[str, str]] = {}
        config = root / ".project-template" / "program-view.json"
        self.config = (
            json.loads(config.read_text(encoding="utf-8")) if config.is_file() else {}
        )
        unknown = set(self.config.get("sections", {})) - set(SECTIONS)
        if unknown:
            raise ValueError(
                f"{config}: unknown sections {sorted(unknown)}; known: {', '.join(SECTIONS)}"
            )

    def enabled(self, section: str) -> bool:
        return bool(self.config.get("sections", {}).get(section, True))

    def last_commit(self, rel: str) -> dict[str, str]:
        if rel in self._commits:
            return self._commits[rel]
        line = git(self.root, "log", "-1", "--format=%h%x09%cI%x09%s", "--", rel or ".")
        commit: dict[str, str] = {}
        if line:
            sha, date, subject = line.split("\t", 2)
            body = git(self.root, "log", "-1", "--format=%B", sha)
            # agentctl's post-commit hook records the authoring session in a
            # local note; a commit without one exits nonzero.
            note = subprocess.run(
                [
                    "git",
                    "-C",
                    str(self.root),
                    "notes",
                    "--ref=agent-session",
                    "show",
                    sha,
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            found = SESSION_ID.search(note.stdout) if note.returncode == 0 else None
            commit = {
                "sha": sha,
                "date": date,
                "subject": subject,
                "models": ", ".join(
                    re.findall(r"^Contributing-model:\s*(\S+)", body, re.MULTILINE)
                ),
                "session": found.group(0) if found else "",
            }
        self._commits[rel] = commit
        return commit

    def commit_dates(self, rels: list[str]) -> dict[str, str]:
        """Last commit date of each path, from one `git log` walk."""
        if not rels:
            return {}
        out = git(self.root, "log", "--format=%x00%cI", "--name-only", "--", *rels)
        dates: dict[str, str] = {}
        date = ""
        for line in out.splitlines():
            if line.startswith("\x00"):
                date = line[1:]
            elif line and line not in dates:
                dates[line] = date
        return dates

    def dirty(self, rel: str) -> int:
        prefix = rel.rstrip("/") + "/" if rel else ""
        return sum(1 for path in self.changed if path.startswith(prefix))


def live_sessions(root: Path) -> list[dict[str, object]]:
    sessions = []
    now = time.time()
    for entry in sorted((root / ".agentctl" / "active").glob("*")):
        if not entry.is_file():
            continue
        age = now - entry.stat().st_mtime
        lines = entry.read_text(encoding="utf-8").splitlines()
        if not lines or age > ACTIVE_WINDOW_S or lines[0].startswith("DONE"):
            continue
        scope = (
            lines[1].removeprefix("scope:").split()
            if len(lines) > 1 and lines[1].startswith("scope:")
            else []
        )
        sessions.append(
            {
                "id": entry.name,
                "banner": lines[0],
                "scope": scope,
                "age_min": round(age / 60),
            }
        )
    return sessions


def touches(session: dict[str, object], rel: str) -> bool:
    """True when any scope pattern lies inside repo-relative `rel` or covers it."""
    for pattern in session["scope"]:
        base = str(pattern).split("*", 1)[0].rstrip("/")
        if base and (
            not rel
            or base == rel
            or base.startswith(rel + "/")
            or rel.startswith(base + "/")
        ):
            return True
    return False


def charter(path: Path) -> tuple[str, str]:
    """H1 title (without a `Program ` prefix) and the first prose paragraph as plain text."""
    text = path.read_text(encoding="utf-8")
    title = re.search(r"^# (.+)$", text, re.MULTILINE)
    paragraphs = [
        p.strip()
        for p in re.split(r"\n\s*\n", text)
        if p.strip() and not p.lstrip().startswith(("#", "Program root:"))
    ]
    name = title.group(1).removeprefix("Program ") if title else path.parent.name
    prose = " ".join(paragraphs[0].split()) if paragraphs else ""
    prose = (
        re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", prose)
        .replace("`", "")
        .replace("**", "")
    )
    return name[:1].upper() + name[1:], prose


def focus_heading(root_md: Path) -> str:
    """The first `## ` heading of a `ROOT.md`, its current focus, without a
    leading "Current main focus" / "Program focus" label."""
    found = re.search(r"^## (.+)$", root_md.read_text(encoding="utf-8"), re.MULTILINE)
    heading = found.group(1) if found else ""
    return (
        re.sub(r"(?i)^(current\s+|program\s+)?(main\s+)?focus\s*", "", heading).lstrip(
            ": "
        )
        or heading
    )


def front_matter(index: Path) -> dict[str, object]:
    text = index.read_text(encoding="utf-8")
    match = re.match(r"---\n(.*?)\n---\n", text, re.DOTALL)
    head = match.group(1) if match else ""
    fields: dict[str, object] = {}
    for key in ("title", "subtitle"):
        found = re.search(rf"^{key}:\s*\"?(.*?)\"?\s*$", head, re.MULTILINE)
        fields[key] = found.group(1) if found else ""
    fields["output_files"] = re.findall(
        r"^\s+output-file:\s*\"?([^\"\s]+)", head, re.MULTILINE
    )
    return fields


class Program:
    """A program directory and the files the conventions place in it."""

    def __init__(self, project: Project, rel: str):
        self.project, self.rel = project, rel
        self.dir = project.root / rel if rel else project.root
        charter_path = self.dir / "PROGRAM.md"
        self.declared = charter_path.is_file()
        if self.declared:
            self.name, self.description = charter(charter_path)
        else:
            self.name, self.description = (
                project.root.name,
                "Repository root (implicit root program).",
            )
        self.files: list[
            str
        ] = []  # repository-relative, owned by this program and no nearer one

    def owned(self, predicate) -> list[str]:
        return [f for f in self.files if predicate(f)]

    def local(self, rel: str) -> str:
        """Path relative to this program's directory."""
        return rel[len(self.rel) + 1 :] if self.rel else rel


def build_programs(project: Project) -> list[Program]:
    rels = {
        f.rpartition("/")[0]
        for f in project.files
        if f.rpartition("/")[2] == "PROGRAM.md"
    }
    programs = {rel: Program(project, rel) for rel in sorted({"", *rels})}
    for f in project.files:
        owner = f.rpartition("/")[0]
        while owner not in programs:
            owner = owner.rpartition("/")[0]
        programs[owner].files.append(f)
    return [programs[rel] for rel in sorted(programs, key=lambda r: Path(r).parts)]


def link(page: Path, target: Path, label: str) -> str:
    href = os.path.relpath(target, page.parent).replace(os.sep, "/")
    return f'<a href="{esc(href)}">{esc(label)}</a>'


def session_id(full: str) -> str:
    return f'<code title="{esc(full)}">{esc(full[:8])}</code>'


def commit_cell(commit: dict[str, str], uncommitted: int) -> str:
    if commit:
        cell = f"<code>{esc(commit['sha'][:9])}</code> {esc(commit['subject'])}"
        extra = [esc(commit["models"])] if commit.get("models") else []
        extra += (
            [f"session {session_id(commit['session'])}"]
            if commit.get("session")
            else []
        )
        if extra:
            cell += f'<br><span class="dim">{" · ".join(extra)}</span>'
    else:
        cell = '<span class="dim">never committed</span>'
    if uncommitted:
        cell += f' <span class="warn">· {uncommitted} uncommitted</span>'
    return cell


def sessions_cell(sessions: list) -> str:
    return (
        "<br>".join(
            f'{session_id(s["id"])} {esc(s["banner"])} <span class="dim">({s["age_min"]} min ago)</span>'
            for s in sessions
        )
        or '<span class="dim">none</span>'
    )


def render_page(title: str, subtitle: str, body: str) -> str:
    # The repo view adds the script that keeps a private link's token visible.
    return (
        '<!doctype html>\n<html lang="en"><head><meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{esc(title)}</title><style>{STYLE}</style></head><body>\n"
        f'<h1>{esc(title)}</h1>\n<p class="dim">{subtitle}</p>\n{body}\n</body></html>\n'
    )


def link_list(
    page: Path, root: Path, rels: list[str], dates: dict[str, str], shown: int
) -> str:
    """Newest first; the first `shown` listed, the rest folded."""
    items = [
        f"<li>{link(page, root / r, Path(r).name)}"
        + (f' <span class="dim">{esc(dates[r][:10])}</span>' if dates.get(r) else "")
        + "</li>"
        for r in rels
    ]
    head, rest = items[:shown], items[shown:]
    folded = (
        f"<details><summary>{len(rest)} more</summary><ul>{''.join(rest)}</ul></details>"
        if rest
        else ""
    )
    return f"<ul>{''.join(head)}</ul>{folded}"


class Dashboard:
    def __init__(self, project: Project):
        self.project = project
        self.root = project.root
        self.generated = time.strftime("%Y-%m-%d %H:%M %Z")
        self.sessions = (
            live_sessions(project.root) if project.enabled("sessions") else []
        )
        self.programs = build_programs(project)
        self.pages: dict[Path, str] = {}

    # -- per-program collections ---------------------------------------------

    def papers(self, program: Program) -> list[dict[str, object]]:
        """Papers in this program's subtree: `papers/<slug>/index.qmd` projects."""
        prefix = program.rel + "/" if program.rel else ""
        found = []
        for f in self.project.files:
            path = Path(f)
            if not (
                f.startswith(prefix)
                and path.name == "index.qmd"
                and path.parent.parent.name == "papers"
            ):
                continue
            paper = self.root / path.parent
            meta = front_matter(self.root / f)
            log = paper / "CHANGELOG.md"
            latest = (
                re.search(r"^## (.+)$", log.read_text(encoding="utf-8"), re.MULTILINE)
                if log.exists()
                else None
            )
            build = paper / "_build"
            outputs = [
                build / name
                for name in meta["output_files"]
                if (build / name).is_file()
            ]
            outputs += sorted(p for p in build.glob("acl*/paper*.pdf") if p.is_file())
            rel = str(path.parent)
            found.append(
                {
                    "path": paper,
                    "title": meta["title"] or path.parent.name,
                    "subtitle": meta["subtitle"],
                    "changelog": latest.group(1) if latest else "",
                    "outputs": outputs,
                    "commit": self.project.last_commit(rel),
                    "uncommitted": self.project.dirty(rel),
                    "tbd": sum(
                        s.read_text(encoding="utf-8").count("`TBD`")
                        for s in (paper / "sections").glob("_*.qmd")
                    ),
                    "sessions": [s for s in self.sessions if touches(s, rel)],
                }
            )
        return found

    def skeletons(self, program: Program) -> list[str]:
        """Lightweight paper skeletons `papers/<slug>.md` owned by this program."""
        return program.owned(
            lambda f: Path(f).parent.name == "papers" and f.endswith(".md")
        )

    def surveys(self, program: Program) -> list[dict[str, object]]:
        prefix = program.rel + "/" if program.rel else ""
        dirs = sorted(
            {
                str(
                    Path(f).parent
                    if f.endswith("/survey.md")
                    else Path(f).parent.parent
                )
                for f in self.project.files
                if f.startswith(prefix)
                and (
                    (
                        f.endswith("/survey.md")
                        and Path(f).parent.parent.name == "surveys"
                    )
                    or f.endswith("/related-work/papers.yaml")
                    and Path(f).parent.parent.parent.name == "surveys"
                )
            }
        )
        found = []
        for d in dirs:
            manifest = self.root / d / "related-work" / "papers.yaml"
            entries = (
                len(
                    re.findall(
                        r"^- key:", manifest.read_text(encoding="utf-8"), re.MULTILINE
                    )
                )
                if manifest.exists()
                else 0
            )
            found.append(
                {
                    "path": self.root / d,
                    "entries": entries,
                    "commit": self.project.last_commit(d),
                }
            )
        return found

    def handouts(self, program: Program) -> list[str]:
        return program.owned(is_handout)

    def documents(self, program: Program) -> list[str]:
        """Markdown directly in the program directory that no other block shows."""
        return program.owned(
            lambda f: (
                str(Path(f).parent) == (program.rel or ".")
                and f.endswith(".md")
                and not NOT_DOCUMENTS.search(Path(f).name)
                and not is_handout(f)
            )
        )

    def topic_counts(self, program: Program) -> tuple[int, int, int]:
        """Topic docs, open gaps, and sketches directly in the program's collections."""

        def under(name: str, f: str) -> bool:
            return str(Path(f).parent) == (
                f"{program.rel}/{name}" if program.rel else name
            )

        topics = program.owned(
            lambda f: under("topics", f) and not TOPIC_COMPANION.search(f)
        )
        gaps = program.owned(lambda f: under("gaps", f) and Path(f).name != "README.md")
        sketches = program.owned(lambda f: under("gaps/sketches", f))
        return len(topics), len(gaps), len(sketches)

    def handoffs(self, program: Program) -> list[Path]:
        # Handoffs are usually private and Git-excluded, so they are globbed, not listed.
        found = sorted((program.dir / "handoffs").glob("*.md"))
        single = program.dir / "handoff.md"
        found += [single] if single.is_file() else []
        return sorted(found, key=lambda p: p.stat().st_mtime, reverse=True)

    def handoff_pointer(self, program: Program) -> Path | None:
        """The handoff an extensionless `ROOT` names, relative to its directory."""
        pointer = program.dir / "ROOT"
        if not pointer.is_file():
            return None
        lines = pointer.read_text(encoding="utf-8").split()
        target = (program.dir / lines[0]).resolve() if lines else None
        return (
            target
            if target and target.is_file() and target.is_relative_to(self.root)
            else None
        )

    # -- pages -----------------------------------------------------------------

    def papers_page(self, program: Program, papers: list, surveys: list) -> Path:
        page = program.dir / "papers-index.html"
        rows = []
        for p in papers:
            outputs = (
                " · ".join(link(page, o, o.name) for o in p["outputs"]) or "not built"
            )
            rows.append(
                f'<tr><td><b>{esc(p["title"])}</b><br><span class="dim">{esc(p["subtitle"])}</span>'
                f"<br>{link(page, p['path'] / 'index.qmd', str(p['path'].relative_to(program.dir)))}</td>"
                f'<td data-label="Built">{outputs}</td><td data-label="Changelog">{esc(p["changelog"])}</td>'
                f'<td data-label="Last change">{commit_cell(p["commit"], p["uncommitted"])}</td>'
                f'<td class="num" data-label="Open TBDs">{p["tbd"]}</td>'
                f'<td data-label="Live sessions">{sessions_cell(p["sessions"])}</td></tr>'
            )
        survey_items = "".join(
            "<li>"
            + (
                link(
                    page,
                    s["path"] / "survey.md",
                    str(s["path"].relative_to(program.dir)),
                )
                if (s["path"] / "survey.md").exists()
                else f"<code>{esc(s['path'].relative_to(program.dir))}</code> (no survey.md yet)"
            )
            + f": {s['entries']} manifest entries"
            + (
                f", last commit {esc(s['commit']['date'][:10])}"
                if s["commit"]
                else ", never committed"
            )
            + "</li>"
            for s in surveys
        )
        body = (
            '<table class="dash"><thead><tr><th>Paper</th><th>Built outputs</th><th>Latest changelog entry</th>'
            f"<th>Last change</th><th>Open TBDs</th><th>Live sessions on it</th></tr></thead><tbody>{''.join(rows)}"
            "</tbody></table>"
            + (f"<h2>Field surveys</h2><ul>{survey_items}</ul>" if surveys else "")
        )
        charter_link = (
            link(page, program.dir / "PROGRAM.md", "charter") + " · "
            if program.declared
            else ""
        )
        subtitle = (
            f"Program <code>{esc(program.rel or '.')}</code> · {charter_link}"
            f"{link(page, self.root / 'index.html', 'all programs')} · generated {esc(self.generated)} by "
            "<code>program_view.py</code>."
        )
        self.pages[page] = render_page(
            f"{program.name}: papers in progress", subtitle, body
        )
        return page

    def program_record(self, program: Program) -> dict[str, object]:
        enabled = self.project.enabled
        papers = self.papers(program) if enabled("papers") else []
        surveys = self.surveys(program) if enabled("surveys") else []
        page = (
            self.papers_page(program, papers, surveys)
            if papers and (program.dir / "papers").is_dir()
            else None
        )
        handouts = self.handouts(program) if enabled("handouts") else []
        documents = self.documents(program) if enabled("documents") else []
        dates = self.project.commit_dates(handouts + documents)
        # A dated name (`progress-2026-07-20.md`) carries the document's own
        # date; its last commit may only be a move.
        dates.update(
            {
                r: m.group(1)
                for r in handouts + documents
                if (m := DATED_NAME.search(Path(r).name))
            }
        )
        handouts.sort(key=lambda r: (dates.get(r, ""), r), reverse=True)
        documents.sort(key=lambda r: (dates.get(r, ""), r), reverse=True)
        root_md = program.dir / "ROOT.md"
        return {
            "program": program,
            "depth": len(Path(program.rel).parts),
            "papers": papers,
            "skeletons": self.skeletons(program) if enabled("papers") else [],
            "proposals": program.dir / "paper-proposals.md"
            if (program.dir / "paper-proposals.md").is_file()
            else None,
            "page": page,
            "surveys": surveys,
            "handouts": handouts,
            "documents": documents[:DOCUMENT_LIMIT],
            "more_documents": max(0, len(documents) - DOCUMENT_LIMIT),
            "dates": dates,
            "root_md": root_md if root_md.is_file() else None,
            "focus": focus_heading(root_md) if root_md.is_file() else "",
            "glossary": program.dir / "GLOSSARY.md"
            if (program.dir / "GLOSSARY.md").is_file()
            else None,
            "counts": self.topic_counts(program),
            "report": program.dir / "report.html"
            if (program.dir / "report.html").is_file()
            else None,
            "handoffs": self.handoffs(program),
            "pointer": self.handoff_pointer(program),
            "commit": self.project.last_commit(program.rel),
            "uncommitted": self.project.dirty(program.rel),
            "sessions": [s for s in self.sessions if touches(s, program.rel)],
        }

    def section(self, page: Path, r: dict, children: dict[str, list]) -> str:
        program: Program = r["program"]
        topics, gaps, sketches = r["counts"]
        links = (
            [link(page, program.dir / "PROGRAM.md", "charter")]
            if program.declared
            else []
        )
        links += [link(page, r["glossary"], "glossary")] if r["glossary"] else []
        links += [link(page, r["root_md"], "ROOT")] if r["root_md"] else []
        links += (
            [link(page, r["page"], plural(len(r["papers"]), "paper"))]
            if r["page"]
            else []
        )
        links += [link(page, r["proposals"], "proposals")] if r["proposals"] else []
        links += (
            [link(page, self.root / r["handouts"][0], "latest handout")]
            if r["handouts"]
            else []
        )
        links += [link(page, r["report"], "report")] if r["report"] else []
        links += (
            [link(page, program.dir / "topics", plural(topics, "topic"))]
            if topics
            else []
        )
        links += [link(page, program.dir / "gaps", plural(gaps, "gap"))] if gaps else []
        links += (
            [
                link(
                    page,
                    program.dir / "gaps" / "sketches",
                    plural(sketches, "sketch", "sketches"),
                )
            ]
            if sketches
            else []
        )
        chips = [plural(len(r["papers"]), "paper")] if r["papers"] else []
        chips += [plural(len(r["surveys"]), "survey")] if r["surveys"] else []
        chips += [plural(len(r["handouts"]), "handout")] if r["handouts"] else []
        chips += [plural(len(r["handoffs"]), "handoff")] if r["handoffs"] else []
        live = (
            f'<span class="chip live">● {plural(len(r["sessions"]), "live session")}</span>'
            if r["sessions"]
            else ""
        )
        date = (
            f'<span class="dim when">{esc(r["commit"]["date"][:10])}</span>'
            if r["commit"]
            else ""
        )
        blocks = [("Last change", commit_cell(r["commit"], r["uncommitted"]))]
        if r["handouts"]:
            blocks.append(
                ("Handouts", link_list(page, self.root, r["handouts"], r["dates"], 4))
            )
        if r["skeletons"]:
            blocks.append(
                ("Paper skeletons", link_list(page, self.root, r["skeletons"], {}, 4))
            )
        if r["pointer"]:
            blocks.append(("ROOT handoff", link(page, r["pointer"], r["pointer"].name)))
        if r["handoffs"]:
            blocks.append(
                ("Newest handoff", link(page, r["handoffs"][0], r["handoffs"][0].name))
            )
        if r["documents"]:
            more = (
                f'<span class="dim">and {r["more_documents"]} older</span>'
                if r["more_documents"]
                else ""
            )
            blocks.append(
                (
                    "Documents",
                    link_list(page, self.root, r["documents"], r["dates"], 4) + more,
                )
            )
        blocks += (
            [("Live sessions", sessions_cell(r["sessions"]))] if r["sessions"] else []
        )
        meta = "".join(
            f'<div class="block {re.sub(r"[^a-z]+", "-", t.lower())}"><h4>{esc(t)}</h4>{body}</div>'
            for t, body in blocks
        )
        focus = f'<p class="focus">Focus {esc(r["focus"])}</p>' if r["focus"] else ""
        kids = "".join(
            self.section(page, c, children) for c in children.get(program.rel, [])
        )
        return (
            f'<details class="program" id="{anchor_id(program)}" open><summary>'
            f'<span class="name">{esc(program.name)}</span> <code class="dim">{esc(program.rel or ".")}</code> '
            + "".join(f'<span class="chip">{esc(c)}</span>' for c in chips)
            + live
            + date
            + f'</summary><div class="body"><div><p class="desc">{esc(program.description)}</p>{focus}'
            + f'<p class="open">{" · ".join(links)}</p></div>'
            + f'<div class="meta">{meta}</div></div>{kids}</details>'
        )

    def index_page(self) -> None:
        page = self.root / "index.html"
        records = [self.program_record(p) for p in self.programs]
        children: dict[str, list] = {}
        for r in records:
            rel = r["program"].rel
            if rel:
                parent = str(Path(rel).parent)
                while parent not in ("", ".") and not any(
                    x["program"].rel == parent for x in records
                ):
                    parent = str(Path(parent).parent)
                children.setdefault("" if parent == "." else parent, []).append(r)
        root = next(r for r in records if not r["program"].rel)

        def outline(r: dict) -> str:
            kids = "".join(outline(c) for c in children.get(r["program"].rel, []))
            live = (
                ' <span class="live" title="live sessions">●</span>'
                if r["sessions"]
                else ""
            )
            return (
                f'<li><a href="#{anchor_id(r["program"])}">{esc(r["program"].name)}</a>{live}'
                + (f"<ul>{kids}</ul>" if kids else "")
                + "</li>"
            )

        # The shallowest focus below the root is the project's current focus
        # (for research projects, `research/ROOT.md`).
        focused = sorted((r for r in records if r["focus"]), key=lambda r: r["depth"])
        lead = (
            f"<p>Current focus {esc(focused[0]['focus'])} · {link(page, focused[0]['root_md'], 'open')}</p>"
            if focused
            else ""
        )
        session_items = "".join(
            f'<li>{session_id(str(s["id"]))} {esc(s["banner"])} <span class="dim">({s["age_min"]} min ago;'
            f" scope: {esc(' '.join(s['scope']) or 'none')})</span></li>"
            for s in self.sessions
        )
        extra_nav = (
            '<li><a href="#sessions">Live sessions</a></li>'
            if self.project.enabled("sessions")
            else ""
        )
        main = lead + self.section(page, root, children)
        if self.project.enabled("sessions"):
            main += f'<h2 id="sessions">All live sessions in this checkout</h2><ul>{session_items or "<li>none</li>"}</ul>'
        sidebar = (
            '<nav class="outline" aria-label="Programs"><details open><summary>Programs</summary>'
            f'<ul class="tree">{outline(root)}</ul><ul class="extra">{extra_nav}</ul></details></nav>'
        )
        title = self.project.config.get("title") or "Programs"
        subtitle = (
            f"Programs declared by <code>PROGRAM.md</code> in <code>{esc(self.root.name)}</code> · generated "
            f"{esc(self.generated)} by <code>program_view.py</code>."
        )
        self.pages[page] = render_page(
            title, subtitle, f'<div class="layout">{sidebar}<main>{main}</main></div>'
        )


def anchor_id(program: Program) -> str:
    return "program-" + (
        re.sub(r"[^a-z0-9]+", "-", program.rel.lower()).strip("-") or "root"
    )


def pages(root: Path) -> dict[str, str]:
    """The repo-view `--pages` hook: dashboards keyed by repository-relative path."""
    root = root.resolve()
    dashboard = Dashboard(Project(root))
    dashboard.index_page()
    return {
        path.relative_to(root).as_posix(): text
        for path, text in dashboard.pages.items()
    }


def describe(root: Path) -> str:
    """Plain-text inventory of each program, for checking discovery without a browser."""
    dashboard = Dashboard(Project(root.resolve()))
    lines = []
    for program in dashboard.programs:
        r = dashboard.program_record(program)
        topics, gaps, sketches = r["counts"]
        lines.append(f"{program.rel or '.'}: {program.name}")
        lines.append(
            f"  papers {len(r['papers'])}, skeletons {len(r['skeletons'])}, surveys {len(r['surveys'])},"
            f" handouts {len(r['handouts'])}, handoffs {len(r['handoffs'])}, documents"
            f" {len(r['documents']) + r['more_documents']}, topics {topics}, gaps {gaps}, sketches {sketches}"
            + (f", focus: {r['focus']}" if r["focus"] else "")
        )
    return "\n".join(lines)


if __name__ == "__main__":
    print(describe(Path(sys.argv[1] if len(sys.argv) > 1 else ".")))
