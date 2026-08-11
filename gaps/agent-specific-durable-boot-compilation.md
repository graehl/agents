---
slug: agent-specific-durable-boot-compilation
noticed: 2026-08-11
where: scripts/install-agents / AGENTS.global.md
---

**Gap:** installation currently exposes a static global source to each harness.
It cannot yet prepare and install an agent-profile-specific durable boot,
normally for one flagship model (or one of a small pair) under a given harness,
compiled from the applicable global, project, model, and request-scoped
instruction layers. The compiled result must occupy what that harness treats as
the authoritative `AGENTS.md` world-state. In particular, a next-tier packet
such as `RUNS.md` or `RESEARCH.md` may be summarized away across compaction
unless that protected world-state retains both its action trigger and the
operational meaning of refreshing or locating the packet. Protecting only a
pointer whose dispatch semantics can be lost does not preserve the intended
behavior.

**Noticed while:** splitting the large global, run, and research protocols into
compact binding mains plus optional clarification, to reduce protected-context
cost without weakening post-compaction instruction routing.

**Fix sketch:** add a prepare/compile phase, probably shared by YA and
`scripts/install-agents`, which selects the relevant instruction layers and
materializes the exact global `AGENTS.md` text the selected harness/model
profile will protect as its world-state. Session- or request-specific selection
may refine that stable profile but need not be the only compilation unit. Keep
selection scoped so unrelated packets do not consume durable context.

Treat installation of the flagship profile into each harness's default
new-session load slot as a normal mode. It has generated-copy semantics:
changing the source corpus requires reinstalling, so the manifest records
source hashes and `status` reports a stale compiled boot clearly. Also support a
harness launch argument, environment variable, or direct boot-file path when
available, especially for switching profiles. A just-in-time write to the
canonical slot is valid when the harness is verified to snapshot its bytes into
the durable context cache. Verification must establish whether compaction
reconstructs from captured bytes or rereads the live path before any launcher
restores a temporary target. Preserve prior targets and make every activation
mode reversible.

Test in a synthetic home first, then inspect each harness's effective boot and
run a compaction trace proving that the protected dispatch rule still causes
the required packet refresh. The capability/tendency model in
`topics/agent-instructions.md` should determine whether a route embeds a packet,
embeds only durable dispatch semantics, or relies on verified harness
reconstruction.
