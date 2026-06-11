# Frontier supplement to AGENTS.md

Latitude for frontier-capability models, loaded via the Claude and
Codex supplements. Everything in `AGENTS.md` still applies; this file
relaxes how, not whether. If this launch also surfaced
`AGENTS.weak.md`, this file does not apply — stop reading it.

## End-state over checklist

Procedural rules — ordered steps, "read X before Y" triggers, format
checklists — spec a default path to an end state, not a ritual. When
a step's purpose is already satisfied, skip the step and state the
one-line deduction in visible output ("only change is a topic-doc
note and the commit message already routes readers there — pushing
without amending"). The deduction must cite evidence from this
session, not general confidence: "I know what that doc says" does
not satisfy a read-before trigger; having read it earlier this
session does. The stated deduction is the price of the skip — it
keeps the latitude auditable and a wrong equivalence cheap to catch.

No equivalence latitude where the observable step is itself the
contract: the big-effect gate record, the shared-workdir discard
ban, edit-mechanism discipline, peer-coordination writes
(`.agentctl/active/`), and any rule phrased "never X" or "stop and
ask". Those exist to resist exactly the in-the-moment "the end state
is fine anyway" reasoning this file licenses elsewhere.
