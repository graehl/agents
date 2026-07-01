# Codex Supplement

Read this after `~/agents/AGENTS.md` and `~/agents/AGENTS.user.md` when
running in Codex / OpenAI Codex. This file contains Codex harness
mechanics; broad shared policy stays in `AGENTS.md`. The one carve-out
is the confirm-before-acting rule below, which the Claude harness
injects automatically but Codex does not.

Model tier: do not trust self-knowledge of your model name — models
misreport it. Read the harness-recorded id from your own rollout
file:

```bash
tac "$(find ~/.codex/sessions -name "*$AGENTCTL_SESSION_ID*.jsonl" |
  head -1)" | rg -m1 -o '"model":"[^"]*"'
```

Below GPT-5.5 (e.g. Codex 5.3 Spark), or with `AGENTS.weak.md`
surfaced, you are weak tier: read `~/agents/AGENTS.weak.md` and do
not read `AGENTS.frontier.md`. At GPT-5.5 or above, read
`~/agents/AGENTS.frontier.md` next — frontier-tier latitude.

## Session Identity

**Never fabricate a session id — recover the real one.** Your
active-session entry (`.agentctl/active/<id>`) must be keyed by the
resumable id you would `codex resume`, never a hand-picked personal
tag. This overrides the AGENTS.md "a personal tag is a last resort"
clause: in Codex a real id is *always* recoverable, so the last resort
never applies here. A tasteful invented id (`codex-recap-quote-reply`)
is worse than useless. Agent-set env does not survive a bash call, so
you cannot even keep the invented id stable across your own turns;
meanwhile on resume the wrapper or process tree hands back the *real*
id, orphaning the invented entry so nothing ever DONE-marks it. It then
reads as a live peer for the full 70-minute window and stalls other
agents over work already finished — and a sibling `~/ya` shell, which
exports the real uuid, keys a different entry for the same session. That
is unintentional-fork territory.

**Normal path — let `agentctl` resolve it.** `agentctl active
"<banner>" [scope...]` (and `others` / `alone`) key the entry from
`$AGENTCTL_SESSION_ID`, else a `resume <id>` ancestor in the process
tree — pass no id, and never hand-write `.agentctl/active/<name>`
yourself. The `~/bin/codex` wrapper exports `AGENTCTL_SESSION_ID` from a
positional `codex resume <id>` (not `--resume`); when it was bypassed,
`agentctl` walks the process tree for the id.
`AGENTCTL_NO_PROC_SESSION_ID` disables that fallback; full mechanics in
`topics/agentctl.md`.

**If `agentctl active` refuses with "no session id"** — a fresh session
with empty env and no resume ancestor — that is the cue to do the work,
not to invent a tag. The real id is the first-line
`session_meta.payload.id` of this cwd's transcript under
`~/.codex/sessions/` (also embedded in the filename,
`rollout-<ts>-<id>.jsonl`). One command prints it:

```bash
find ~/.codex/sessions -name '*.jsonl' -printf '%T@ %p\n' | sort -rn |
while read -r _ f; do
  head -1 "$f" | grep -qF "\"cwd\":\"$PWD\"" &&
    { basename "$f" | grep -oE '[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}'; break; }
done
```

Then, in a single bash call (env does not persist between calls),
`export AGENTCTL_SESSION_ID=<id>` before the `agentctl active` you
retry.

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

## Confirm before hard-to-reverse or outward-facing actions

For actions that are hard to reverse or outward-facing, confirm first
unless durably authorized or explicitly told to proceed without
asking; approval in one context doesn't extend to the next.
