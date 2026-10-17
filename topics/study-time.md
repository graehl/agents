# Study time

> An asynchronous learning workflow that turns project work and conversations into opportunities for understanding, exploration, and better supervision of agents.

Topic: `study-time`

The current implementation is an on-demand pre-alpha skill: discover recent
activity, synthesize an invitation, show a demo, and try the exercise. There
is no automatic cross-session collector or semantic index. The
[indexing sketch](study-time.sketches.md) records that proposed system.

## Motivation and pitch

The work can advance faster than the person's understanding. Study time
preserves occasions to return: a method an agent used, a surprising result,
an unexplored alternative, a connection across projects, or a question the
person did not yet know to ask. Deadline work supplies context; a separate
study session supplies room to think creatively and follow an interest.

“Why learn anything?” opens the philosophical question. “What's learning
worth?” invites reflection on its value. “What's worth learning?” is the
product question. Two complementary lines are:

- “Save the question. Come back curious.”
- “You can learn anything. Find what's worth learning next—when you have
  room to explore.”

Saving explicit questions is only one input. The promise is “Turn the work
you got done into understanding you get to keep.” Study time notices what
your projects and conversations bring you near, then prepares a small
demonstration and an invitation to explore. It helps choose a direction
without requiring you to design your own curriculum.

“Taste” names part of the aspiration: recognizing what is interesting, what
deserves attention, and what an explanation leaves unresolved. The outcomes
underneath it are concrete: notice a distinction, ask a better question,
find a relevant result, explain a mechanism, or apply it elsewhere. They
do not require claiming a uniquely human advantage.

If superintelligence takes over discovery, learning and teaching can still
be beautiful activities. Following the state of the art in retrospect,
understanding why a development works, and occasionally anticipating a next
step before its broad announcement are worthwhile pleasures. This purpose
survives even if humans cease to be indispensable to progress.

Broad education also supports supervising semi-autonomous research. A usable
known unknown is a gap you can recognize, name, and investigate. A routine
that asks agents about neglected related problems and results can substitute
for some supervision; study helps the person assess the answers. Orientation,
understanding, retention, and enjoyment are distinct outcomes.

## Proposed capture during ordinary work

After addressing the task, quietly save a short signal when project work or
conversation reveals a promising learning opportunity. Do not wait for an
explicit study directive. Signals include skipped derivations, delegated
methods, consequential assumptions, surprising results, adjacent problems,
recurring interests, and connections across projects or everyday chats.

Record the opportunity, not a diagnosis of ignorance. An agent's explanation
is not evidence the person needed it; a correction by the person can show
existing understanding. Mark an agent-inferred connection as an inference.
The mere occurrence of a technical term does not justify an entry.

Use `~/agents/user/study-time/inbox.md`. Merge duplicates by concept and
purpose. Each entry needs an ID, date, source locator, observed signal, and
possible payoff; add a conceptual bridge when one is apparent. Use an actual
session ID and recognizable turn, or a project path and section. Keep just
enough context to recover the opportunity, never full transcripts or secrets.
All personal study state lives in the locally excluded
`~/agents/user/study-time/` directory.

Capture should cost a few lines, without research, a quiz, or a new conversation
branch. Until a collector is implemented, compilation discovers signals from
available recent work and chats on demand. Do not claim background coverage.

## Study begins with something worth seeing

The [study-time skill](../skills/study-time/SKILL.md) owns compilation and
delivery. Present a term or headline, its relevance, and an optional paper
reference, then a worked toy visualization or demonstration. Make visible
the intermediate steps that a paper may omit. A useful demo can be a small
table or worked example; build an interactive artifact when manipulating
the example helps. Do not substitute a plan to create a demo for the demo.

Paper importance has an explicit basis: relevance to the learner's work,
reach into other topics, and whether the source is a foundational result,
incremental contribution, or contested claim. Prefer these labeled judgments
to an unexplained aggregate score or citation-count proxy. The importance of
the topic and strength of the paper's evidence are separate.

After the demonstration, offer “Already know this?” and “Want to know more?”
with optional free text about the desired direction. Offer “More now” and
“Later,” without asking the person to manage dates or review intervals.
Knowing it, wanting to retain it, and wanting to explore further are separate
choices. A self-report informs selection without becoming a mastery test.
Preserve deferred intent, including the text, with the topic when state is
available. Repeated “Later” with little engagement increases the time before
resurfacing and eventually shelves the candidate. A substantive question,
exploration, or a new consequential project connection can revive it. Page
opening or elapsed dwell time alone does not demonstrate interest or learning.
In pre-alpha, use conversational evidence and existing notes; persistence and
automatic resurfacing remain part of the proposed tracker.

Choose one substantial invitation and at most two alternatives. Weigh
curiosity, explanatory reach, supervision value, prior exposure, and energy.
An optional duration constrains the route, not the learner. Preserve room
for non-work interests and depth on an existing thread. Do not turn unused
invitations into overdue homework or reward constant topic switching.

## Forms and outcomes

| Aim | Study activity |
|---|---|
| Usable known unknown | Map neighboring problems, warning signs, relevant results, and where to investigate. |
| Understand a mechanism | Work an example, predict a change, explain the result. |
| Read a paper | Reconstruct one claim or figure, then read the sections it depends on. |
| Explore visually | Manipulate a meaningful parameter and inspect a boundary case. |
| Follow the frontier | Understand a verified recent advance, its predecessors, and teach it back. |
| Anticipate | Optionally record a prediction before checking the outcome; distinguish retrospective exercises from forecasts. |
| Retain | Select a few useful retrieval prompts for an existing spaced-repetition system. |

The existing `~/agents/user/MASTERY.md` remains the sole mastery registry.
Study history records what actually happened and the learner's expressed
interest; it does not infer learning from attendance or an agent's output.

## Foxes, hedgehogs, and scouts

The fox/hedgehog image comes from Archilochus, was popularized by Isaiah
Berlin, and was used by Philip Tetlock for reasoning styles in *Expert
Political Judgment*, before *Superforecasting*. A hedgehog organizes problems
around one big idea; a fox combines approaches. Deep expertise alone does not
make someone a hedgehog. Tetlock's
[Wharton interview](https://knowledge.wharton.upenn.edu/podcast/knowledge-at-wharton-podcast/expert-political-judgement/)
explains the distinction directly. Peter Salovey's
[“Thinking Like a Fox”](https://salovey.yale.edu/writings-and-speeches/speeches/thinking-fox)
offers a short educational introduction.

Julia Galef's scout/soldier distinction concerns wanting to discover what is
true versus defend a preferred belief; it is compatible with specialization.
Her [short essay](https://ideas.ted.com/why-you-think-youre-right-even-when-youre-wrong/)
and [book introduction](https://juliagalef.com/my-book/) are accessible routes.
“Explore broadly, go deep where it matters” is a plain-language formulation
for this product. The [landscape](study-time-landscape.md) connects it to
existing learning tools and their evidence limits.
