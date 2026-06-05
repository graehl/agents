# Grok Supplement

Read this after `~/agents/AGENTS.md` and `~/agents/AGENTS.user.md` when
running in Grok / xAI. This file contains harness mechanics only; shared
policy stays in `AGENTS.md`.

This is a stub: Grok is not yet a harness used in earnest here, so the
specifics below are deliberately thin. Fill them in from observed runtime
behavior rather than assumed vendor defaults; flag anything still unknown
rather than guessing a path or flag.

## Session Identity

Primary mechanism: the launcher-injected `$AGENTCTL_SESSION_ID`. It is
harness-agnostic — a launcher such as yepanywhere (YA) exports it per
command through a `BASH_ENV` bridge that the `agentctl` bash wrapper
sources regardless of provider — so it works for Grok with no
Grok-specific discovery snippet. If it is set in your Bash env, use it
verbatim as the session id for `.agentctl/active/<session-id>` and skip
any further lookup; `agentctl` adopts the same var first, so its `active/`
entry and yours name the same file.

If Grok exposes a native resumable session id (a var, or an id a
resume/list command would use), prefer it, and have the launcher mint
`AGENTCTL_SESSION_ID` to equal it so the entry and any transcript agree —
the same pattern as Claude's `claude --session-id <uuid>`. Until such a
mechanism is confirmed for Grok, the YA-injected id is effectively a
personal tag: `active/` stays self-consistent across peers but may not map
to a provider transcript. Record the tag once and reuse it across
compaction/resume.

If no `AGENTCTL_SESSION_ID` is present and no native id is exposed, fall
back to a personal tag per `AGENTS.md` § Active sessions and note that the
launcher bridge was absent.

## Session Logs

The on-disk location of Grok transcripts (if any) is not documented here
yet. When `AGENTS.md` says to search provider session logs, discover the
transcript directory from the running harness and record it in this file
once known; do not assume a path from training data.
