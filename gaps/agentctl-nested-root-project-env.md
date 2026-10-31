---
slug: agentctl-nested-root-project-env
noticed: 2026-10-31
where: agentctl.py:ROOT, load_project_env
---

2026-10-31. Contributing-model: opus-5.5.

**Gap:** the invoking project root is the cwd (`AGENTCTL_ROOT` else
`os.getcwd()`), and `start` loads only `<root>/agentctl.env`. In
`~/draft`, the checkout root's `agentctl.env` sets
`AGENTCTL_SOURCE_GUARD=record`, but program subdirectories such as
`research/speech-recognition/` hold their own `.agentctl/` and are common
launch cwds. A start from there gets no project env, so the guard falls back
to `enforce` and refuses on untracked Python anywhere in the checkout, while
the agent believes the project runs in record mode. Reproduced 2026-10-31:
the same `start … -- true` exits 1 from `research/speech-recognition/` and
launches from the checkout root.

Declared source dependencies (`--source-dep`, `--source-deps-scan`) avoid
the refusal, since they ignore unrelated untracked files. The defaults
mismatch remains for undeclared runs and for any other key the checkout
root's file supplies (`PII_EVAL_HOME`).

**Fix options:** load `agentctl.env` files from the Git checkout root down to
the invoking root, nearer winning; or report the selected project env and
guard mode in the start banner so the mismatch is visible. Either changes a
documented contract (§ Contracts, `agentctl.env`) and needs a
backward-compat note.
