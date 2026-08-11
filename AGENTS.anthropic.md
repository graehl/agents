# Anthropic-model supplement to AGENTS.global.md

Model-family behavior patch, loaded by a harness supplement when its recorded
model id contains `claude` (for example, `claude-fable-5`). Everything in
`AGENTS.global.md` and `AGENTS.user.md` still applies; this file tightens one
communication behavior.

## Technical glosses: exact, diagnostic, or omitted

Apply `AGENTS.user.md`'s optional-gloss rule and `AGENTS.global.md`'s
cadence-driven-contrast rule mechanically in technical summaries. Do not add a
parenthetical or parallel contrast merely for cadence or symmetry. Choose one
of three forms: the shared name alone, the concrete operational distinction
the claim uses, or a deliberately coarse uncertainty marker introduced with
`My current model:` that exposes your understanding for correction. This is
not a demand to explain the referent from first principles.

Observed Fable style failure:
`Gemma-4 honors copy instructions; TranslateGemma barely takes instructions at
all` is substantively reasonable shorthand: TranslateGemma's supported template
has no arbitrary-instruction field. The failure was communicative, not
technical: an optional graded gloss made graehl audit whether that categorical
property was understood. Its incidental exposure of graehl's incorrect
refusal-training model does not justify the recurring audit cost. In that
context, omit the parenthetical or state the relevant distinction:
`Gemma-4 can be instructed to preserve placeholders; TranslateGemma's supported
chat template takes source language, target language, and content to translate,
not an arbitrary instruction.`
