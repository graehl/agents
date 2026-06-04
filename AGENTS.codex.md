# Codex Supplement

Read this after `~/agents/AGENTS.md` and `~/agents/AGENTS.user.md` when
running in Codex / OpenAI Codex. This file contains Codex harness mechanics
only; shared policy stays in `AGENTS.md`.

## Session Identity

When `AGENTS.md` asks for `<session-id>`, use Codex's real resumable session
id: the id a Codex resume/list command would use. Prefer any id exposed by
the runtime. If none is exposed, inspect Codex's local JSONL transcripts under
`~/.codex/sessions/`.

Codex transcripts contain a first-line `session_meta` record with
`payload.id` and `payload.cwd`. A quick lookup is:

```bash
cwd=$(pwd -P)
find "$HOME/.codex/sessions" -type f -name '*.jsonl' -printf '%T@ %p\n' 2>/dev/null |
  sort -nr |
  while IFS= read -r row; do
    file=${row#* }
    id=$(
      head -n 1 "$file" |
        jq -er --arg cwd "$cwd" '
          select(.type == "session_meta" and .payload.cwd == $cwd) |
          .payload.id
        ' 2>/dev/null
    ) && { printf '%s\n' "$id"; break; }
  done
```

If the matching transcript is unavailable, check active Codex process log
outputs before falling back to an ad hoc tag. If an ad hoc tag is unavoidable,
record it once and reuse it after compaction/resume.

## Session Logs

When `AGENTS.md` says to search provider session logs, search
`~/.codex/sessions/**/*.jsonl`, excluding the current session id.

## Skills Path Aliasing

`~/agents/skills` and `~/.codex/skills/user` may alias the same directory;
treat `~/agents/skills` as the canonical edit target. Do not "sync" them into
symlinks — that creates self-referential loops that break skill loading.
Follow symlinks when checking identity:

```bash
stat -Lc '%d:%i %n' ~/agents/skills ~/.codex/skills/user
```
