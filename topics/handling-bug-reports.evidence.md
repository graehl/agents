# Handling bug reports — evidence

## 2026-07-23 — fixed-code prompting and the false-abstention edge

- The SRI Lab study
  [“Coding Agents Are ‘Fixing’ Correct Code”](https://www.sri.inf.ethz.ch/blog/fixedcode)
  found that explicitly allowing abstention substantially reduced
  redundant patches on already-fixed SWE-bench tasks. A reproduce-only
  prompt did not reliably help.
- The same study's incorrectly pre-patched condition exposed the
  inverse failure: fix-or-abstain strongly favored empty patches even
  though a real defect remained. This rules out “the first reproduction
  attempt passed, therefore stop” as the instruction.
- User refinement: first-party complaints are more credible than remote
  reports, but still need current-target verification. A complaint about
  the result of an active implementation is ordinary evidence and
  refinement, not an automatic fresh-intake ritual; tests,
  investigation, classification, and focused subtasks remain available
  when naturally useful.
- Instruction-design consequence: require an explicit classification
  of exact reproduction, related reproduction, already-fixed behavior,
  or no demonstrated defect. A failed literal reproduction continues
  the investigation instead of choosing either a patch or abstention.

## 2026-07-23 — instruction trace simulation

- **Standalone current defect:** a session-opening complaint triggers
  the topic, the exact current behavior fails, and the agent captures
  the regression signal before fixing it. The topic adds evidence
  without delaying the authorized fix.
- **Inaccurate literal report, real nearby defect:** the first
  reproduction passes, so the agent audits fidelity and probes the
  suspected invariant. It reports that the exact claim did not
  reproduce but the related failure did, then tests and fixes only the
  demonstrated defect. This avoids both redundant patching and false
  abstention.
- **Correction during implementation:** “the button still overlaps”
  does not activate a fresh intake or mandatory subtask. The agent may
  naturally inspect, test, classify, or split out work as the evidence
  warrants, then continues the existing feedback loop.
- **Unrelated defect mentioned mid-effort:** the protocol does not
  derail the active task; it fires when the separate topic is taken up.
- **Remote report without a source revision:** the agent can test
  current HEAD but cannot claim “already fixed” versus “never present,”
  and states that historical limit rather than treating it as proof of
  either conclusion.

## 2026-07-23 — causal adequacy without mandatory exposition

- User accepted a default internal check linking the evidence-backed
  root-cause hypothesis to the implicated family, fix mechanism, and a
  falsifying regression signal. The argument is surfaced only when
  non-obvious or explicitly requested, so obvious fixes do not acquire
  a visible planning ritual.
- **Mechanical fix trace:** a misspelled identifier has an immediate
  cause, affected-use family, and compile/test falsifier; the agent
  checks these without narrating them.
- **Structural fix trace:** a shared-state bug requires the agent to
  connect the proposed change to every caller in the implicated family
  and choose a regression signal that would expose an incomplete
  mechanism. Unsupported links send it back to investigation.
- **Discussion trace:** an explicit request for pre-implementation
  discussion surfaces the same causal chain for user engagement without
  turning the default into an approval checkpoint.
- **Wording correction:** “a regression signal that could falsify the
  root-cause belief” conflated two checks. A regression signal
  demonstrates the behavioral before/after claim; when the cause itself
  remains uncertain, a separate discriminating probe must distinguish
  that hypothesis from alternatives.

## 2026-09-07 — resource pressure omitted from stall diagnosis

- **User-reported incident:** an upload/submission appeared stuck at 0%.
  The agent reported 26 passing focused tests and later confirmed provider
  receipt and a reply, but left the delay unexplained without checking system
  memory or swap pressure. The user said it settled somewhat and suspected
  pressure as the main cause. That causal hypothesis is unverified here; the
  reported omission motivates the instruction change.
- **Decision:** add a global slow/stalled-interaction trigger, with resource
  checks owned by `debugging.md`. The trigger also covers active implementation
  feedback, which deliberately bypasses standalone intake. Require an early
  check and an explicit evidence limit before an unknown-cause conclusion;
  do not demand that unavailable historical evidence exclude pressure.
- **Trace: live stall despite passing tests:** sample memory, paging, CPU,
  and I/O pressure alongside the application path while the symptom persists;
  passing tests and eventual delivery no longer terminate diagnosis alone.
- **Trace: recovered stall, no historical telemetry:** seek incident-time
  evidence, distinguish it from current readings, and report pressure as
  unresolved if necessary. Neither healthy memory now nor occupied swap
  licenses a historical causal claim.
- **Trace: feedback during implementation:** the global symptom trigger
  reaches the same check without restarting bug-report intake. An unrelated
  deterministic typo does not activate the resource-pressure procedure.
- **Validation:** instruction trace simulation only; improvement in live
  diagnosis remains assumed. Contributing-model: 6-Astra.

## 2026-09-07 — numeric preflight precedes live-stall investigation

- **User correction:** a specific cheap query returning one number should run
  before investigating a presently hung or slower-than-previously interaction.
  The earlier "early and before concluding" wording did not make the ordering
  concrete enough and left a broad diagnostic checklist as the first action.
- **Decision:** put the available-RAM-percent query directly in the global
  trigger and debugging packet, before hypothesis lists, searches, and tests.
  It is an initial memory-headroom signal, not proof that all pressure is
  absent. On this host `/proc/pressure/` metrics were unavailable; the verified
  `free` query returned one numeric percentage, so the default does not depend
  on kernel pressure-stall accounting being enabled.
- **Traces:** a live slowdown gets the number before code investigation;
  high available RAM still permits CPU/I/O or container pressure investigation;
  an inaccessible host leaves an explicit evidence limit without blocking
  other diagnosis. A recovered incident retains the historical-evidence rule.
- **Validation:** executed the query and checked these instruction traces;
  live diagnostic benefit remains assumed. Contributing-model: 6-Astra.
