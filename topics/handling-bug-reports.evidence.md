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
