---
name: code-map
description: Produce a developer-facing codebase map report by traversing implementation structure. Use when the user asks for a code map, developer map, architecture orientation, module/control-flow map, or a regenerable report explaining what files/modules do and how key flows move through the code.
---

# Code Map

Create a developer-oriented report that answers: what are the important
modules, how do control/data flows move between them, and where would a
maintainer edit or test a behavior?

This is a report/checklist skill, not a `topics/` doc. Topic docs name
cross-cutting contracts; a code map is a derived orientation artifact.

## Output

Default output directory: `code-map/` unless the user names another
directory. The narrative file is always `README.md`.

Use this shape:

1. `# Code Map`
2. `## Orientation` — one paragraph naming the dominant architecture and the
   two or three flows a new developer should understand first.
3. `## Module Index` — compact table of important files/directories.
4. `## Flow Slices` — 2-5 end-to-end traces through user-facing operations
   or core lifecycles.
5. `## Contracts And Seams` — relevant `topics/*.md` contracts, natural edit
   seams, and where tests should attach.
6. `## Blind Spots` — dynamic imports, generated code, framework routing, or
   paths not proved by traversal.
7. `## Reproduce / Refresh` — exact commands/search roots used.

## Evidence Labels

Use lightweight labels in table cells or bullets:

- `verified: <command>` — proved by static traversal, grep, manifest, or
  source read.
- `observed: <command/run>` — proved by a test, smoke, log, or runtime
  observation.
- `assumed` — plausible from naming/structure but not proven.

Do not make derived claims look stronger than they are. Prefer these labels
over broad HTML comments unless a claim would otherwise mislead.

## Workflow

1. **Load repo vocabulary.** Read project instructions and `GLOSSARY.md` if
   present. Prefer glossary terms in headings, prose, and flow names.
2. **Static inventory first.** Use `rg --files`, manifests, package files,
   entrypoints, CLI parsers, route tables, tests, and README references.
   Record the exact commands for `## Reproduce / Refresh`.
3. **Choose flow slices.** Pick 2-5 flows by operation or lifecycle, not by
   directory. Examples: request handling, command execution, model loading,
   build pipeline, persistence/migration, render/update loop.
4. **Traverse only enough.** Follow callers/callees and imports enough to
   validate the module index, flow slices, seams, and blind spots. Do not
   exhaustively summarize every leaf file.
5. **Connect contracts.** Link relevant `topics/*.md` docs where flows touch
   cross-cutting invariants. Do not create a new topic doc unless the map
   exposes a genuine cross-cutting contract that needs one.
6. **Write the report.** Keep orientation high-signal for a new developer.
   Make flow traces concrete: `file -> function/class -> file`, with the
   behavior each hop owns.
7. **Sanity check.** Verify referenced files exist, paths are clickable when
   possible, evidence labels match what was actually checked, and the report
   has a usable refresh command.

## Module Index Table

Use columns like:

| Path | Responsibility | Inputs / Outputs | Key Callers / Callees | Evidence |
|---|---|---|---|---|

Collapse obvious leaf files. The goal is the smallest map that lets a
developer navigate, not an inventory dump.

## Flow Slice Pattern

For each flow:

```markdown
### <Flow Name>

1. `<entry file>` receives/starts <event>.
2. `<module>` normalizes/validates <data>.
3. `<module>` delegates to <owner>.
4. `<test/log/artifact>` covers or demonstrates the path.

Seams: <where to edit/test>.
Evidence: verified: `<command>`.
```

## Avoid

- A hand-written architecture essay detached from commands that can refresh it.
- A generated graph with no explanation of what matters.
- A directory-by-directory tour that never names end-to-end behavior.
- Source edits while producing the map unless the user explicitly asks.
- Adding glossary rows or topic docs before the first report proves the terms
  and contracts are stable.
