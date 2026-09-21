---
name: start-task
disable-model-invocation: true
description: Start a named work scope using a gap and, when useful, a program-scoped handoff. Use when explicitly asked to scaffold work or on /start-task.
argument-hint: "<short-description, e.g. auth-refactor>"
---

# Instructions

1. Resolve the requested scope and its most specific owning program. Search
   existing gaps, handoffs, and maintainer records before creating a duplicate.
2. Read the governing `gaps/README.md` and `topics/handoffs.md` (project-local,
   else global). Extend or create a gap for unresolved work; use the last named
   handoff, or create a program-scoped handoff when continuity needs one.
3. Record the aim, acceptance condition, current mismatch, chosen approach,
   and next action at useful granularity. Ask only for missing information
   that changes the work. A fixed section template is not required.
4. A requested latest-handoff pointer is `ROOT` at the selected program scope,
   with a target relative to that directory. Preserve another session's live
   entry point and report a conflicting unfinished scope before redirecting it.

Scaffolding records intent; it does not start implementation or create/switch
branches. Keep private handoffs excluded and follow the project's gap visibility
rules. The skill name is retained for explicit invocations; it no longer creates
the retired numbered-task directory convention.
