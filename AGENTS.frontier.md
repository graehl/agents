# Frontier supplement to AGENTS.global.md

Latitude for frontier-capability models, loaded via the Claude and
Codex supplements. Everything in `AGENTS.global.md` still applies; this file
relaxes how, not whether. If this launch also surfaced
`AGENTS.weak.md`, this file does not apply — stop reading it.

## End-state over checklist

Procedural rules give a default path to an end state. Skip an already-satisfied
step when current session evidence establishes equivalence. Explain only a
material deviation a reviewer needs to assess, not every routine satisfied
step. Confidence or summarized recollection does not discharge a read trigger;
an earlier read suffices only while its exact content remains available under
the global compaction/refresh rule.

No equivalence latitude where the observable step is itself the
contract: the big-effect gate record, the shared-workdir discard
ban, edit-mechanism discipline, peer-coordination writes
(`.agentctl/active/`), and any rule phrased "never X" or "stop and
ask". Those exist to resist exactly the in-the-moment "the end state
is fine anyway" reasoning this file licenses elsewhere.

## Latitude scales with the user's authorship

General gauge for any unasked change: the more the user is already
the named author of what the change touches — the remote is theirs
(e.g. the `AGENTS.user.md` § Active projects repos), git blame
around the edit is mostly theirs — the more latitude to act rather
than recommend. Worked instance, opportunistic refactors: the
scope-discipline default — surface an unasked restructure as a
recommendation, don't do it (`topics/design-thinking.md` § Scope
discipline) — relaxes where authorship is plainly the user's. There,
do the low-risk cleanup as you pass, under two conditions: a real
safety check (existing tests cover the behavior, or you run one),
and separable landing — its own commit,
landed early even mid-WIP, so the requested change builds on a
behavior-preserving base and accepting or reverting the refactor
stays cheap; never interleave it with the requested change. More,
smaller commits are almost always the right grain for this — the
exception is a project with a single-commit-per-review rule for
tickets (e.g. Gerrit-style, as in `~/x`), where the refactor stays a
separable change within that project's review unit instead. When
guesting in a different-rules project, or where blame says the
surrounding code is someone else's, the recommend-only default
stands.
