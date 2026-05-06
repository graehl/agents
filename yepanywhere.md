# yepanywhere (YA)

yepanywhere is a web- and mobile-accessible client-server terminal
multiplexer for agent sessions — a tmux-like designed for agent
assistants rather than local terminal use.

- Fork: https://github.com/graehl/yepanywhere (includes heartbeat support)
- Upstream: https://github.com/kzahel/yepanywhere

## Heartbeat turns

Synthetic heartbeat turns delivered through a YA session are not new
semantic user requests. Treat them as liveness nudges for the current
plan. The default text may be `heartbeat`, but session-specific
overrides may use a different configured phrase. On receiving one,
immediately:
- re-check the live wait/watch/job/GPU state, including explicit polling
  of any active unified-exec PTY that backs an `agentctl` watch or other
  foreground wait
- continue the already-approved next step if one exists
- emit a short verified in-session status line even when still waiting,
  so the heartbeat causes visible observable output in the active
  session/CLI rather than only silent internal revalidation
- keep the response terse unless there is a blocker, completion, or new
  result

When a heartbeat turn causes any action that may become visible in the
active CLI session (a status line, a wait/liveness note, or a
command-launch preface), prefix the first such visible output with
`PULSE:` so the user can tell it was heartbeat-related rather than an
unrelated spontaneous turn.
