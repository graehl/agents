---
name: study-time
description: Compile or conduct a personal study session from recent project work, conversations, interests, and learning history. Use for study time or choosing what to learn next; ordinary task questions do not start a lesson.
---

# Study time

Read `~/agents/topics/study-time.md` for the motivation and demo-first
contract. This is an on-demand pre-alpha, without an automatic tracker or
index. Use recent activity directly; do not require a populated inbox.
Save requested session artifacts privately under `~/agents/user/study-time/`.

## Entry points

- `/study-time`: compile and present an invitation with a worked toy demo.
  Accept optional duration, project, topic, energy, or format. Default to a
  roughly 25-minute expandable route; don't require time-budget setup.
- `/study-time begin`: continue the current invitation interactively.
- `/study-time frontier`: select a verified recent advance to understand,
  optionally teach back or anticipate a next step.
- `/study-time capture ...`: save context without starting study.
- “Already know this,” “more,” “later,” or a particular question steer the
  current invitation; do not restart compilation unnecessarily.

## Compile from activity, not just explicit questions

Read the inbox, current invitation, recent history, and relevant entries in
`~/agents/user/MASTERY.md` when present. Use this conversation and recent
project artifacts. Follow pointers into projects under their instructions.
When more context would change selection, inspect bounded recent work
records and available conversations using supported retrieval. Start with
roughly two weeks, extending for persistent interests. Avoid indiscriminate
transcript sweeps; state material coverage limits once.

Infer candidates beyond requests and recorded weaknesses: prerequisites,
neglected adjacent results, agent-used methods, assumptions, conceptual
bridges, recurring interests, and enjoyable detours. Distinguish the person's
evidence from an agent's explanation or mistake. Existing expertise raises
the level or changes the question; it does not exclude the topic. Distinguish
mere mentions, implementation focus, user discussion, options considered by
the user, and consequential agent-only considerations. Keep speaker and
provenance attached; repetition of an agent's prose is not user interest.

Pick one thread and at most two alternatives. Tie each to a source signal
and a reason to spend attention. Weigh curiosity, transfer, supervision,
prior exposure, and energy without invented numerical relevance scores.
Let continuing interest beat novelty. Merge duplicate signals; honor
dismissals and repeated deferrals unless new context justifies reconsideration.

## Present a complete first encounter

Save `current.md` with date, candidate ID, source coverage, headline, why it
surfaced, and the intended outcome. Include a verified paper/source where
useful and explain its importance separately from the strength of its evidence.
Reuse grounded local retrieval; verify external material before assigning it.

Open by recovering the actual project or conversation: what we were doing,
which question or assumption this addresses, and how the answer could change
the work. Use a descriptive topic title, not an advertisement or curiosity
teaser; the learner has already chosen to study. Then give an actual worked
toy demonstration, showing the mechanism and intermediate steps. Prefer a
manipulable visualization when it makes a causal relationship easier to grasp;
otherwise a table or small worked
example is sufficient. Check the example's answers and boundary cases.
Then name a short reading/tutorial/experiment route, a feasible stopping
point, and a copyable prompt for continuing with another agent.

After the demo, offer familiarity and interest separately:

- Already know this: skip, retain for occasional review, or go deeper.
- Want more: “More now” or “Later.”
- Optional text: what to explain, test, visualize, or connect; keep that text
  attached whether acting now or later.

Use a supported interaction form or concise chat choices. Repeated “Later”
with little substantive engagement pushes the topic further back, eventually
off the shortlist. A question or exploration can renew interest. Use available
conversation or saved evidence; do not invent earlier deferrals, infer them
from silence, or mistake elapsed time for learning. Do not ask for dates or
claim that a future notification is scheduled.

## Continue and remember

Conduct a selected session without another permission round. Ask one
meaningful prediction or question at a time; reveal feedback as the learner
proceeds. Adapt the level. A supervision session can end when the learner
can identify a missing adjacent problem and how to investigate it; it need
not end in detailed mastery. Exploration need not become an exam.

When persistence is requested, maintain `history.md`: candidate ID, date, suggested/started/paused/completed/
dismissed, sources, actual response or artifact, and the next useful step.
Before replacing an unfinished `current.md`, preserve its question, sources,
and stopping position in history. Record expressed interest and self-reported
familiarity as such. Update mastery only under the existing registry's rules.

For prediction practice, preserve a timestamp, specific outcome, horizon,
and later resolution including misses; never score hindsight as foresight.
For durable retention, prepare a few accurate prompts for the learner's
existing system. Do not install integrations or create recurring reminders
implicitly. Stop, defer, or discard freely; this is not a debt queue.
