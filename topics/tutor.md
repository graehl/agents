# Tutor

> An explicitly invoked skill that reviews concepts from the personal mastery registry at spaced intervals and teaches requested topics by questioning.

Topic: `tutor`
Glossary: omit

The [tutor skill](../skills/tutor/SKILL.md) owns the procedure. This doc
records the decisions behind it and its trial status.

## Contracts

- **One store.** Review state lives only in the private mastery registry,
  `~/agents/user/MASTERY.md`: level, last refresh, due date and retrieval
  prompt per concept, plus a review log. The skill uses that file's levels
  and entry policy and keeps no second scale or state file.
- **Explicit invocation only.** Work sessions are many and short; none
  should open with an off-task quiz. Nothing runs on a clock, so a review
  happens only when the user starts a `/tutor` session.
- **Every session sweeps what is due.** Because no other trigger exists,
  each session first asks the concepts whose due date has arrived, then
  teaches a requested topic or asks what to learn.
- **State is written per answer.** The row and a log line are written
  after each grade, so a session abandoned midway loses nothing.
- **Grading reads the source.** An answer is graded against the concept's
  linked explanation, since the learner cannot be expected to catch a
  grading error made from the grader's recollection.

## Why review across sessions

Re-asking a concept later in the same conversation spaces recall by
minutes. That is useful as a check before a concept enters the schedule,
but retention over months needs recall after days and weeks, which only
stored due dates can arrange. The tracked items are mechanisms and
distinctions, so each review asks for a free-text reconstruction from an
angle not used before. A flashcard tool would suit paired facts recalled
verbatim; it was not adopted because the user does not use one and these
items need a grader.

The interval rule is deliberately simple: lengthen by a fixed factor on
an unaided pass, shorten to a day or two otherwise. Whether reviews
happen at all matters far more than the formula.

## Status

Trial from 2026-11-10: the user intends to invoke `/tutor` a few times in
the first week. Open after the trial:

- whether a scheduled prompt that only reports "n due" is worth building;
  scheduled-session support in the session UI is still planned, not built
  ([at-scheduling](at-scheduling.md));
- a variant for a child of about ten, which would reuse the registry and
  schedule but replace the dialogue policy: worked examples before
  questions, short fixed-length sessions, no visible demotion, and only
  material whose answers can be checked mechanically.

The skill's teaching loop adapts the question-led approach of Jane
Street's `socratic-tutor` skill (`github.com/janestreet/agent_skills`),
which tracks state only within a conversation.
