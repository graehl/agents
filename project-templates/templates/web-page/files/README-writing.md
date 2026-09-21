
## Writing and riff

This project carries writing guidance under `instructions/`: prose craft,
story and world-building craft, and a story project layout with fill-in
sheets. Your agent reads them when the task is writing; a factual page needs
none of it. Three small files at the project root, once you have answered
the agent's questions, keep the reader, the voice and the look consistent:
`audience.md` (who this is for), `prose-style.md` (how the writing should
sound) and `illustration-style.md` (whether you want pictures, and what
kind). Change them and the agent follows.

Want the same story for a younger reader, in first person, or with pictures?
Ask for a **remix** (Codex: `$remix`). The agent asks the core questions
again and writes the new version under `remixes/`, leaving the original as
it is. Its instructions are in `.agents/skills/remix/SKILL.md`.

When you face a creative choice (a title, an opening, a character, a page
look), ask for a **riff**: four independent alternatives, a recommendation,
and your pick. In a harness with skill invocation, select riff from its skill
picker (Codex: `$riff`); asking in ordinary language works too. Its
instructions are in `.agents/skills/riff/SKILL.md`.
