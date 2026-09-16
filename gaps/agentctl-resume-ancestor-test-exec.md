---
slug: agentctl-resume-ancestor-test-exec
noticed: 2026-09-16
where: tests/test_agentctl.py test_active_recovers_session_id_from_resume_ancestor
---

**Gap:** the test builds an ancestor whose argv carries `codex resume <uuid>`
by running `bash -c 'true; ./agentctl active "…"' codex resume <uuid>`, relying
on the leading `true;` to stop bash exec-replacing itself with the final
command — the comment in the test says so explicitly. On bash 5.3.9 that no
longer holds: walking `/proc` from the `agentctl.py` process shows its parent is
the *outer* shell, with both the `env` and inner `bash` processes gone. Nothing
in the chain carries `resume <uuid>`, so `session_id_from_proc_tree` correctly
finds nothing and `agentctl active` exits 2 with "no session id". The failure
reproduces outside pytest and at pristine `HEAD`, so it is the test's premise
that is stale, not the recovery code — but it is a second standing red beside
`agentctl-after-marker-test-race`, and together they erode the suite's signal.

**Noticed while:** running the suite to validate the repo-wide `shfmt`/`ruff`
format sweep; it was the only failure, before and after.

**Fix sketch:** stop depending on bash declining to exec. Keep the
`resume <uuid>` process alive for the duration of the call — run the payload in
an explicit subshell and wait on it, or append a second command after it so the
final-command optimization cannot apply, or launch the ancestor with a small
helper that execs nothing. Verify by asserting the ancestor is visible from
`/proc` in the test itself, so a future bash change fails loudly on the premise
rather than on the recovery assertion.
