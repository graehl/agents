# Claude Supplement

Read this after `~/agents/AGENTS.md` and `~/agents/AGENTS.user.md` when
running in Claude. This file contains Claude harness mechanics only; shared
policy stays in `AGENTS.md`.

## Session Identity And Logs

Claude sessions are local JSONL transcripts stored at
`~/.claude/projects/<project-hash>/<session-id>.jsonl`. The filename stem is
the real provider session id.

When `AGENTS.md` says to search provider session logs, search
`~/.claude/projects/**/*.jsonl`, excluding the current session file.
