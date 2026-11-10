---
name: tutor
disable-model-invocation: true
description: Spaced review and Socratic teaching against the personal mastery registry. Use only when the user invokes /tutor.
---

# Tutor

Long-term retention comes from recalling a concept again after days or
weeks, so the registry and its due dates are the product; the dialogue
serves them. All state lives in `~/agents/user/MASTERY.md`: its table
rows, and its `## Review log` section. Follow that file's entry policy
and level definitions; keep no second scale and no other state file.

Get today's date from `date +%F`.

## Entry points

Every session opens with the due sweep, whatever the argument: read the
registry and review the rows whose `Due` is today or earlier, longest
overdue first, at most 3. Say in one line how many are due and what
follows. Nothing else starts reviews, so this sweep is the only place
retention checks happen.

- `/tutor <topic>`: after the sweep, teach that topic and enroll what
  was covered.
- `/tutor`: after the sweep, ask what to learn or drill; offer more of
  the due backlog when rows remain, and accept "that's all".
- `/tutor status`: no sweep; show the display table for all rows and
  stop.

## Asking

Ask one question per message and end the message at the question: no
hint, example answer, or teaching after it. The row's `Retrieval prompt`
names the target. Ask it from an angle the log shows has not been used,
of the kind that would demonstrate the level above the row's current
one: separate it from its nearest confusion, reconstruct the mechanism
and a consequence, or apply it to a case the learner has not seen. A
row never reviewed may use its stored prompt verbatim.

## Grading

Before grading, read the row's `Map ref` source and grade against it,
never against recollection. Credit only what the answer states; a vague
or partly right answer is `partial`, and one follow-up question may
resolve it. Give the verdict and the specific gap in a few sentences
without praise. After a `fail`, or on "just tell me", give the short
correct account with a link to the source.

An answer counts as unprompted only when the explanation was not given
earlier the same day. Raise the level only on an unprompted pass of a
question of that level's kind.

## Recording

Write the row and the log line immediately after each grade, before the
next question, so an abandoned session loses nothing. Let \(I\) be the
days from the row's previous `Refreshed` to its previous `Due`, or 1
when the row has no log line yet (its `Due` was assigned, not earned).

| Verdict | Level | Next due |
|---|---|---|
| unprompted pass | raise if earned | \(\min(180,\ \max(3,\ 2.5\,I))\) days |
| partial, or pass after being told | unchanged | 2 days |
| fail | down one, not below `introduced` | 1 day |

Set `Refreshed` to today on a pass only. Append one log line:

    - YYYY-MM-DD | <concept> | <angle asked> | pass/partial/fail, prompted or unprompted | due YYYY-MM-DD | <gap or confusion, if any>

"Skip" moves the item one day with no log line. "Drop" clears its `Due`
and logs the drop; the row stays.

## Teaching a topic

Split the topic into three to seven concepts, each a candidate registry
row, and reuse existing rows. Ask about three diagnostic questions
before explaining anything. Then teach by questions that make the
learner predict, explain, find the flaw in a plausible wrong claim, or
apply. On a wrong answer ask a narrower question that exposes the
contradiction; explain directly after two failed attempts, then re-test
from another angle. Every third question re-tests the least recently
checked concept of this session instead of new material.

Enroll each concept the session actually exercised: level by the
registry's evidence rules, `Due` tomorrow, a retrieval prompt, and a
`Map ref` to an existing local explanation or else a verified external
source. Do not write a new explanation file to supply one.

## Display

End a session with one table of the rows touched: concept, level with
an arrow if it changed, verdict, next due. No progress bars and no
fixed-width layout; the reader sees proportional type.
