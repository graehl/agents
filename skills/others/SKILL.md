---
name: others
description: Show what other agents are doing in this project — own .agentctl/active status (or that the agent is lurking), peers currently active, recently DONE work, and stale entries that may be orphaned. Use when the user invokes /others, asks "who else is here", "what other agents are running", or similar.
---

# /others — see what other agents are doing here

Reports the multi-agent state of the current project: the agent's
own register entry (or that it is lurking), peers currently
active, work recently DONE, and stale entries that may be
orphaned.

## Scope

The skill consults ONLY the project root — the git toplevel of
cwd. This is not a cross-project view; re-invoke from another
project to check it.

## Workflow

1. **Resolve project root**:
   `root=$(git rev-parse --show-toplevel)`. If non-zero exit,
   output `not inside a git project; /others only operates
   against a project root` and stop.

2. **Resolve own session id**. Use the provider's real session id
   per `AGENTS.<provider>.md` (the discovery snippet there is
   strongly preferred over a personal tag). The agent's entry, if
   it has one, is at `$root/.agentctl/active/<session-id>`.

   If the agent is lurking — no intent to write or change state
   this turn and no prior register — there is no self entry.
   Reporting will say so.

3. **Scan**. Both `$root/.agentctl/active/` and (if present)
   `$root/.agentctl/done/` are inspected. For each file, capture
   relative path, mtime, and first line (`head -n1`). If both
   subdirs are missing, every bucket is `none` and the report
   says `no .agentctl/active/ here yet`.

4. **Categorize**:

   - **self**: file at `$root/.agentctl/active/<session-id>` if
     present; else the agent declares lurking.
   - **active peers**: in `active/`, mtime <70 min, content does
     not start with `DONE:`, not self.
   - **stale**: in `active/`, mtime ≥70 min, content does not
     start with `DONE:`, not self. ("Stale" is the category
     label; the cause may be a crash, a forgotten DONE write, or
     an in-progress session that has just been quiet — do not
     judge.)
   - **done in last 24h**: any file (in `active/` or `done/`)
     whose first line starts with `DONE:` and mtime is within 24
     hours.

5. **Emit the report** (see *Output format*). Buckets with zero
   entries still print a header so the user can see the bucket
   was checked.

## Output format

Number every row so the user can reference by row number.

```
**self**: <state>

**active peers** (n):
  1. <relpath>  (<delta> ago)  → "<first line>"
  2. ...

**stale** (n):
  1. <relpath>  (<delta> ago)  → "<first line>"
  ...

**done in last 24h** (n):
  1. <relpath>  (<delta> ago)  → "<first line, including DONE:>"
  ...
```

Self states:

- Registered:
  `**self**: .agentctl/active/<id>  (<delta> ago)  → "<first line>"`
- Lurking:
  `**self**: lurking (no .agentctl/active/ entry); will register on first planning-to-act step`

Empty buckets:
`**<bucket>**: none`

## Implementation hints

- Project root: `git rev-parse --show-toplevel` (one call).
- mtime delta:
  `now=$(date +%s); delta=$(( now - $(stat -c%Y FILE) ))`,
  then format as `Nm` / `Nh` / `Nd`.
- First line: `head -n1 FILE`.
- The 70-min active threshold matches
  `AGENTS.md § Agent activity register`.
- The `done/` subdir is optional. The base convention writes
  `DONE: <summary>` into the same file at its `active/` path; a
  future maintenance step may move files older than 24h to
  `done/`. The skill handles either location and does not
  itself move files.
- The skill does NOT create `.agentctl/active/`. Creation
  happens via the normal register-on-first-act rule, not as a
  side effect of inspection.
