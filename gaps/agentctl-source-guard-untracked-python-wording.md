---
slug: agentctl-source-guard-untracked-python-wording
noticed: 2026-10-19
where: agentctl.py:revalidate_source_snapshot
---

2026-10-19. Contributing-model: opus-5.5.

**Gap:** Two misleading parts of the delayed-launch source guard, seen in
`~/draft` (project `AGENTCTL_SOURCE_GUARD=record`):

1. The untracked-Python check reports "untracked Python appeared after
   submission" whenever any untracked `*.py` exists at launch. It does not
   compare against the submission snapshot, so a file that was already
   untracked at submission (here `research/pii/.../summarize.py`, untracked
   for days) is reported as new.
2. In record mode the message still says "refusing payload launch" and only
   then appends "(recorded, --source-guard record)"; the payload launches.
   An agent read the first clause as a refusal and relaunched, starting a
   duplicate run writing to the same output directory.

**Fix:** record the untracked-Python set at submission and report only
additions; in record mode, word the message as a recorded violation
("would refuse under enforce"), not a refusal.
