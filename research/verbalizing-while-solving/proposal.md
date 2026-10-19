# Verbalizing while solving: why typing beliefs to a partner helps

Status: proposed research, unrun and unscheduled; a survey and paper
candidate parked for graehl to pick up later. Captured 2026-10-17 from his
observation during Order of the Sinking Star puzzle sessions with an agent.
The literature pointers below are recalled from memory and unverified;
graehl expects literature on this kind of question to be of little use, so
the proposal leads with a self-experiment.

Contributing-model: claude-opus-5-5

## Observation

graehl solves puzzles better when he types his beliefs as he goes ("the pad
can't be turned back", "that mirror move can't be undone") to an agent
partner. Sometimes he does not look at what he types, and judges the effect
on what sticks, and on noticing "no, that doesn't make sense", to be about
the same. He has years of fast touch typing and reads code, plans and
document state visually, often while revising sentences.

## Candidate mechanisms

Each predicts a different contrast in the experiment below.

1. **External working memory.** The typed belief is an anchor that frees
   working memory or can be re-read. Predicts: the benefit needs the text to
   stay visible, and private notes help as much as messages to a partner.
2. **Audience effect.** Phrasing a belief so a partner can follow and use
   it (legibility, wanting to seem smart, the excitement of collaborating)
   forces a cleaner internal representation. Predicts: messages to a
   partner beat private notes, even when neither is re-read (A over B with
   the text seen, C over H with it unseen).
3. **Production effect.** Generating the sentence, by hand, keys or voice,
   is what helps, through motor or articulatory encoding. Predicts: the
   benefit survives when the text is never looked at, and speaking aloud
   gives a similar or larger effect.
4. **Error detection at production.** Committing to an explicit sentence
   exposes its flaws while it is formed ("no, that doesn't make sense").
   Predicts: more early corrections of wrong beliefs and fewer wasted moves,
   with or without a reader.

These can co-occur; the experiment aims to show which ones carry most of
the effect for one expert typist.

## Experiment: one solver, matched puzzles

Within one person, rotate conditions across levels of similar difficulty:

| Condition | Produces | Sees own text | Partner reads it |
|---|---|---|---|
| A: typed to agent | typed | yes | yes |
| B: typed private notes | typed | yes | no |
| C: typed, not looked at | typed | no | yes |
| D: spoken, transcript on the game screen | speech | yes | yes |
| E: spoken, transcript hidden | speech | no | yes |
| F: spoken to self, not recorded | speech | no | no |
| G: silent | none | no | no |
| H: typed private notes, not looked at | typed | no | no |

Display placement matters: in D the recognized transcript, and in A the
typed message, should appear on the game monitor, not beside it where it
often goes unread.

**Measures:** time to solve; wasted moves (undos, resets, restarts from a
reset screenshot); requests for hints; self-reported moments where a typed or
spoken belief was caught as wrong. The simulator can count a level's search
states and shortest solution to help match difficulty.

**Confounds:**
- Learning across sessions and familiarity with a world's mechanics: rotate
  condition order within each world.
- Partner replies that carry information: in A, C, D and E the agent
  acknowledges without adding content.
- Level choice: assign matched pairs before seeing the levels.
- Mood and fatigue: record time of day.

Eye tracking (a camera on the game monitor) would show directly whether C,
E and H really go unread, and would turn "sees own text" into a measured
quantity.

## Dependency

Conditions D and E need continuous, low-friction voice input in a quiet
room that attributes speech to graehl and ignores other voices, such as
children. That is
[`~/ya/gaps/sketches/continuous-diarized-voice-input.md`](../../../ya/gaps/sketches/continuous-diarized-voice-input.md).

## Pointers to check later

Recalled, not retrieved; verify before citing:

- self-explanation effect in learning from worked examples (Chi and
  colleagues);
- the production effect: words read aloud are remembered better than words
  read silently (MacLeod and colleagues);
- the generation effect (Slamecka and Graf);
- longhand versus laptop note taking (Mueller and Oppenheimer, 2014) and
  its replication attempts, some of which did not reproduce the effect;
- the drawing effect on memory (Wammes, Meade and Fernandes);
- reactivity of think-aloud protocols (a meta-analysis by Fox, Ericsson
  and Best) and verbal overshadowing in insight problems (Schooler and
  colleagues), which predict that talking can also hurt;
- learning by teaching, and expecting to teach (the protégé effect);
- cognitive offloading (Risko and Gilbert) and external representations in
  problem solving (Zhang and Norman);
- private speech (Vygotsky); rubber-duck debugging as practitioner folklore.

## Future Work

If the audience effect dominates, an agent partner could be designed to
elicit it: ask for the belief behind each move rather than offering
moves. If production dominates, cheap always-on voice capture matters more
than any partner behavior.
