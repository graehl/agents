# Codex Supplement

Read this after `~/agents/AGENTS.md` and `~/agents/AGENTS.user.md` when
running in Codex / OpenAI Codex. This file contains Codex harness
mechanics; shared policy stays in `AGENTS.md`. Unless this launch also
surfaced `AGENTS.weak.md` (smaller model), read
`~/agents/AGENTS.frontier.md` next — frontier-tier latitude.

## Session Identity

No manual discovery: read `$AGENTCTL_SESSION_ID` for your own id. The
`~/bin/codex` wrapper exports it from a `codex resume <id>` invocation
(positional `resume`, not `--resume`), and `agentctl` recovers it from a
`resume <id>` ancestor in the process tree when the wrapper was bypassed, so
`agentctl` keeps the matching `.agentctl/active/<id>` entry with no per-call
setup. `AGENTCTL_NO_PROC_SESSION_ID` disables the process-tree fallback; full
mechanics in `topics/agentctl.md`. If you ever need the raw resumable id and
the env var is empty, it is the first-line `session_meta.payload.id` of this
cwd's transcript under `~/.codex/sessions/`.

## Session Logs

When `AGENTS.md` says to search provider session logs, search
`~/.codex/sessions/**/*.jsonl`, excluding your own session
(`$AGENTCTL_SESSION_ID`).

## Skills Path Aliasing

`~/agents/skills` and `~/.codex/skills/user` may alias the same directory;
treat `~/agents/skills` as the canonical edit target. Do not "sync" them into
symlinks — that creates self-referential loops that break skill loading.
Follow symlinks when checking identity:

```bash
stat -Lc '%d:%i %n' ~/agents/skills ~/.codex/skills/user
```
