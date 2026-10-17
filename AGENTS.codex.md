## Model and session identity

If `$AGENT_LAUNCH_MODEL` is absent, read the model from your rollout:

```bash
tac "$(find ~/.codex/sessions -name "*$AGENTCTL_SESSION_ID*.jsonl" |
  head -1)" | rg -m1 -o '"model":"[^"]*"'
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

Global provider-log searches use `~/.codex/sessions/**/*.jsonl`, excluding
your session. Use top-level ISO-8601 `timestamp` for elapsed time;
`queued-anchor` v1 parses only Claude logs.

## Tool results and waits

`functions.exec` and nested `exec_command` have independent output budgets.
The outer default is 10,000 tokens; increasing nested `max_output_tokens`
does not raise it. A first-line `// @exec` pragma may request more, subject
to harness caps. Split required reads to fit the smaller active budget.
Any truncation/elision means the read is incomplete.

A terminal `wait` consumes its `cell_id`; reuse only an explicitly running id.

Do not finalize with owned running/queued work or its successor decision
unconsumed unless the user deferred it. A promise is no wakeup; questions and
compaction do not discharge ownership. Before launching/resuming/waiting, read
`topics/codex-session.md` § Job ownership and waits plus triggered RUNS packets.

## Skill aliases

`~/agents/skills` is the canonical edit target; `~/.agents/skills` may already
alias it. Never "sync" aliases into self-referential symlinks. Check identity
with `stat -Lc '%d:%i %n' ~/agents/skills ~/.agents/skills`.
