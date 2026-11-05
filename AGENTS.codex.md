## Model and session identity

If `$AGENT_LAUNCH_MODEL` is absent, locate your rollout using § Logs below,
then read its model:

```bash
tac /absolute/path/to/rollout.jsonl | rg -m1 -o '"model":"[^"]*"'
```

Register through `agentctl active "<banner>" [scope...]`; it resolves the
published id or a `resume <id>` ancestor. If unresolved, read
`topics/codex-session.md` § Identity recovery before retrying.

## Writing discipline

- State shared evidence limits once near the opening; repeat only differing
  status or a qualification needed to prevent a misleading local claim.
- Avoid scattered bold and routine bold bullet lead-ins. Reserve it for
  occasional useful paragraph openers that state a claim consistent with the
  document's decisions.
- Cut first-person editorial asides ("my proposed default"); state the
  recommendation and reason. Retain materially personal experience/authorship.
- Replace "Evidence grade:" and opaque shorthand with concrete evidence,
  actions or quantities. Keep precise technical terms, not invented jargon.
- Attach necessary uncertainty to its claim; omit generic closing hedges.

## Logs

Codex homes used with agent-auth-router are `~/.codex` (`codex-primary`)
and `~/.agent-auth-router/profiles/codex-second` (`codex-second`). Check
`${AAR_STATE_DIR:-$HOME/.agent-auth-router}/accounts.json` for current
enrolled home paths. Router account homes supply upstream credentials;
routing through `codex-second` does not move the client's rollouts there.
Rollouts use the client process's `${CODEX_HOME:-$HOME/.codex}`, under
`sessions/YYYY/MM/DD/` or `archived_sessions/` after archival.

YA URL/session ids can differ from native Codex thread ids. On this host,
resolve a YA id through its read-only identity registry:

```bash
sqlite3 -readonly "$HOME/.yep-anywhere/discovery.sqlite" \
  "SELECT native_scope, native_id FROM session_identities WHERE session_id = '<YA-session-id>';"
```

`native_scope` is the transcript directory; search it for the returned native
id (filenames start with `rollout-<timestamp>-`, not the session id):

```bash
find /absolute/native_scope -type f -name '*<native-id>*.jsonl'
```

A profile used only for login/quota reads may have no rollouts. Keep the
launcher-published `AGENTCTL_SESSION_ID` for coordination; do not replace it
with the native id. Global provider-log searches use the client rollout
directories, excluding your native session. Use top-level ISO-8601 `timestamp` for elapsed time;
`queued-anchor` v1 parses only Claude logs.

## Tool results and waits

`functions.exec` and nested `exec_command` have independent output budgets.
The outer default is 10,000 tokens; increasing nested `max_output_tokens`
does not raise it. A first-line `// @exec` pragma may request more, subject
to harness caps. Split required reads to fit the smaller active budget.
Any truncation/elision means the read is incomplete.

A terminal `wait` consumes its `cell_id`; reuse only an explicitly running id.

## File content writes

Write or rewrite authored file content through `apply_patch` (in code mode,
`tools.apply_patch` inside `exec`), never a shell heredoc or redirect through
`exec_command`; content a program computes is unaffected. `apply_patch`
produces a file-change item clients render as an edit. Either form is silent
while its input is generated: the app-server reports nothing for a call until
the whole input exists, so the global section-size rule is what bounds that
silence.

Do not finalize with owned running/queued work or its successor decision
unconsumed unless the user deferred it. A promise is no wakeup; questions and
compaction do not discharge ownership. Before launching/resuming/waiting, read
`topics/codex-session.md` § Job ownership and waits plus triggered RUNS packets.

## Skill aliases

`~/agents/skills` is the canonical edit target; `~/.agents/skills` may already
alias it. Never "sync" aliases into self-referential symlinks. Check identity
with `stat -Lc '%d:%i %n' ~/agents/skills ~/.agents/skills`.
