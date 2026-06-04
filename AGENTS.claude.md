# Claude Supplement

Read this after `~/agents/AGENTS.md` and `~/agents/AGENTS.user.md` when
running in Claude. This file contains Claude harness mechanics only; shared
policy stays in `AGENTS.md`.

## Session Identity And Logs

Claude sessions are local JSONL transcripts at
`~/.claude/projects/<project-hash>/<session-id>.jsonl`, where
`<project-hash>` is cwd with `/` replaced by `-` (leading `/` becomes
a leading `-`). The filename stem is the real provider session id;
always use it for `.agentctl/active/<session-id>` and other
identifiers.

Discovery — works once the current session has written anything
to its transcript (i.e. after the first turn or two):

```bash
cwd=$(pwd -P)
project_dir="$HOME/.claude/projects/${cwd//\//-}"
ls -t "$project_dir"/*.jsonl 2>/dev/null |
  head -n1 | xargs -r basename | sed 's/\.jsonl$//'
```

If the project's transcript directory does not yet exist (very
first turn in a brand-new project), record a temporary personal
tag and replace it with the real id once a transcript exists.
Do not silently keep the personal tag when the real id becomes
discoverable.

When `AGENTS.md` says to search provider session logs, search
`~/.claude/projects/**/*.jsonl`, excluding the current session
file.
