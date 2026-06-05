# Claude Supplement

Read this after `~/agents/AGENTS.md` and `~/agents/AGENTS.user.md` when
running in Claude. This file contains Claude harness mechanics only; shared
policy stays in `AGENTS.md`.

## Session Identity And Logs

The harness exports your session id ambiently as
`$CLAUDE_CODE_SESSION_ID` in every Bash shell — use it directly as
the session id for `.agentctl/active/<session-id>` and other
identifiers. It equals the stem of this session's transcript at
`~/.claude/projects/<project-hash>/<session-id>.jsonl`, where
`<project-hash>` is cwd with `/` replaced by `-` (leading `/`
becomes a leading `-`).

You do not need to do anything for active-sessions upkeep:
`agentctl` adopts `$CLAUDE_CODE_SESSION_ID` on its own (no export,
no per-call prefix), so plain `./agentctl start …` maintains this
session's entry (`AGENTS.md` § Active sessions), and a launched job
never inherits your identity (agentctl's internal launch-depth
counter). Because each Bash tool call is a fresh shell, do not rely
on `export`ing the id to carry between calls — the ambient var
already does that.

If `$CLAUDE_CODE_SESSION_ID` is empty (very first turn before the
transcript exists), derive it from the newest transcript stem, and
fall back to a temporary personal tag only until the real id
appears — do not silently keep the tag once the real id is known:

```bash
cwd=$(pwd -P)
project_dir="$HOME/.claude/projects/${cwd//\//-}"
ls -t "$project_dir"/*.jsonl 2>/dev/null |
  head -n1 | xargs -r basename | sed 's/\.jsonl$//'
```

When `AGENTS.md` says to search provider session logs, search
`~/.claude/projects/**/*.jsonl`, excluding the current session
file.
