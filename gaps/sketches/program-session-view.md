---
slug: program-session-view
noticed: 2026-10-15
where: agentctl active; agentctl commit-note; PROGRAM.md / GLOSSARY.md scopes
---

**Outcome:** one browsable view of a project's program structure joined to its
agent sessions: each program (by `PROGRAM.md`, nested by parent), its papers,
surveys, topics, handoffs and gaps, with what changed last, which session
changed it, and which sessions are working in it now. Opened from a button
(a YA project app) and current without a manual regenerate step.

**Landed (2026-10-15):** the `program-view` template base
(`project-templates/bases/program-view/`) generates the program tree and
per-program papers pages as a `repo_view.py --pages` hook, live under the
repo-view service: programs nested with the repository root as the root
program; charter summary and `ROOT.md` focus; glossary, topics, gaps,
sketches, handoffs and the `ROOT` handoff pointer; papers, surveys, handouts
and other documents; last commit with `Contributing-model:` and the
`refs/notes/agent-session` session; uncommitted count; live
`.agentctl/active` sessions whose `scope:` lies in the program. Discovery
follows `topics/project-directory.md`. `~/draft` serves it as its YA app
through `scripts/research_site.py`. Still open below: a monitor (runs,
session history), the JSON record emitter, and the session-centred view.

**Superseded prototype:** `~/draft` `scripts/research_index.py` wrote the
same pages for that repository alone. It was project-local, research-shaped and stale
the moment a session moves.

**Proposed approach:**
- Promote the collection logic into a shared acli helper here (or an
  `agentctl` read verb) that emits the joined records as JSON: program tree
  from `PROGRAM.md` discovery, topic and gap inventory per glossary scope,
  handoffs, sessions from `agentctl active` (fresh, stale and `DONE`, with
  scope), commit→session joins from `commit-note`, and runs from
  `agentctl list`. The static HTML becomes one renderer of that JSON.
- A live variant as a YA *process* app (`service.where.kind: "process"`),
  read-only, polling or watching `.agentctl/active/` and `refs/notes/` mtimes,
  so a session claim or commit appears without regeneration. Process apps run
  in YA's project sandbox with the network firewall, which suits a
  read-only filesystem/Git reader. The same service can render any authorized
  repository path on demand (Markdown to HTML with relative links kept
  working), replacing the prototype's pre-rendered `_views/` mirror; the
  reusable template capability is the `repo-view` base
  (`project-templates/bases/repo-view/`), whose `--pages` hook can host this
  dashboard.
- A session-centred view as the inverse join: for a session id, its banner
  history, scope, commits (via notes), runs started, handoffs and gaps
  touched. Session ids in either view become YA session links inside YA's
  viewer (`~/ya` `gaps/sketches/session-links-in-viewer.md`).

**Unresolved decisions:**
- **History of activity.** `active/` keeps only current entries (plus
  `stale/`); "last session active on X" for uncommitted work needs either
  retained banner history or transcript scanning. Commit notes cover only
  committed work.
- **Scope matching.** `scope:` globs are advisory and often broad; deciding
  which program a session "is in" from them is heuristic.
- **Exposure.** The views name session ids and transcript paths; keep them
  out of Git (the prototype uses `.git/info/exclude`) and out of public app
  addresses.
- **Owner.** A shared helper here versus a YA feature that reads the same
  records; YA already observes sessions directly and need not trust
  `active/` files.
