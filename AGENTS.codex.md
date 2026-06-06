# Codex Supplement

Read this after `~/agents/AGENTS.md` and `~/agents/AGENTS.user.md` when
running in Codex / OpenAI Codex. This file contains Codex harness mechanics
only; shared policy stays in `AGENTS.md`.

## Session Identity

If `$AGENTCTL_SESSION_ID` is already set in your Bash env, use it verbatim and
skip the lookup below — that is the done answer, not a hint to verify. A
launcher such as yepanywhere (YA) injects it per command through a `BASH_ENV`
bridge, and `agentctl` adopts the same var first, so its `active/` entry and
yours name the same file with no extra work. The tradeoff is the same as a
personal tag: a launcher-injected id overrides Codex's real resumable id, so
`active/` stays self-consistent but may not match a `~/.codex/sessions/`
transcript. When the launcher derives the value from the resumable
`session_meta.payload.id`, the two agree; if it diverges, note both ids.

### Resumed sessions (terminal resume)

A YA launch injects `$AGENTCTL_SESSION_ID`. A terminal `codex resume <id>`
(positional `resume`, **not** `--resume`) does not — but two mechanisms now
recover it automatically, so this is normally handled for you:

- The `~/bin/codex` wrapper parses `resume <id>` and exports
  `AGENTCTL_SESSION_ID` from it, so your Bash shells and agentctl inherit it.
- `agentctl` independently recovers the id from a `resume <id>` ancestor in
  the process tree (`agent_session_id` → `session_id_from_proc_tree`), gated
  by the same launch-depth guard, so it keys the right
  `.agentctl/active/<id>` even if the wrapper was bypassed.

So read `$AGENTCTL_SESSION_ID` for your own id; if it is set, that is the
answer. It is empty only when both are bypassed — codex launched by an
absolute path that skips the wrapper *and* a PID namespace that hides the
launcher, or `AGENTCTL_NO_PROC_SESSION_ID` is set. Then fall back to the
`$CODEX_THREAD_ID` / transcript lookups below; the resume arg, where visible,
is the resumable `session_meta.payload.id` by construction.

Otherwise, when `AGENTS.md` asks for `<session-id>`, use Codex's real
resumable session id: the id a Codex resume/list command would use. Prefer any
id exposed by the runtime. If none is exposed, inspect Codex's local JSONL
transcripts under `~/.codex/sessions/`.

Codex currently exposes `$CODEX_THREAD_ID` in the runtime. In observed local
JSONL transcripts this matches the resumable `session_meta.payload.id`, so use
it as the first fast lookup hint, then verify the matching transcript before
keying `.agentctl/active/`:

```bash
cwd=$(pwd -P)
if [ -n "${CODEX_THREAD_ID:-}" ]; then
  find "$HOME/.codex/sessions" -type f -name "*${CODEX_THREAD_ID}.jsonl" -print 2>/dev/null |
    while IFS= read -r file; do
      head -n 1 "$file" |
        jq -er --arg cwd "$cwd" --arg id "$CODEX_THREAD_ID" '
          select(.type == "session_meta"
            and .payload.id == $id
            and .payload.cwd == $cwd) |
          .payload.id
        ' 2>/dev/null && break
    done
fi
```

If `$CODEX_THREAD_ID` and `session_meta.payload.id` diverge, prefer the
resumable `session_meta.payload.id` for active-session filenames until the
divergence is understood. Record both ids in notes: a future Codex fork/resume
behavior could justify keying activity on thread id, but do not switch merely
because both names are present.

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
