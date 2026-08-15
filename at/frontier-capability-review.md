---
name: frontier-capability-review
scope:
  - topics/frontier-capability-review.md
  - topics/frontier-capability-review.evidence.md
  - topics/agent-instructions.md
  - _RESEARCH/direction.md
  - AGENTS.frontier.md
  - AGENTS.opus.md
  - AGENTS.copilot.md
---

Review the selective frontier-capability register against evidence accumulated
since its last ledger entry.

- Check whether a major frontier-model generation, fresh user experience, or
  ordinary session traces materially change any registered item's strictness,
  routing, or retirement status. A review that finds no change is complete.
- Verify each owning instruction before changing the register. The owner stays
  authoritative; update it first when a disposition changes.
- Use ordinary traces first. A bounded anecdotal presumption switch is allowed
  when a suitable live task makes it cheap and safe. Do not run a controlled
  guidance-A/guidance-B evaluation unless the item is explicitly high-value and
  the likely decision value justifies the compute and analysis cost.
- Record `retain`, `narrow`, `relax`, `promote`, or `retire` for affected rows,
  and append the evidence or no-change rationale to
  `topics/frontier-capability-review.evidence.md`. Do not edit wording merely to
  demonstrate activity.

Before the final response, acknowledge this run through:

```text
scripts/at-queue done --root /home/graehl/agents \
  --job frontier-capability-review \
  --occurrence <occurrence_id returned by claim> \
  --run-after <exactly 60 days after this run, RFC3339 UTC> \
  --status <concise disposition>
```
