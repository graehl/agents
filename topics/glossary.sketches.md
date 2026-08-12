# Glossary sketches

> Dormant candidate extensions to project glossary loading; none changes the
> current glossary discovery or regeneration contract.

Topic: `glossary`

## Domain-segregated or conditional loading

The current model loads one `GLOSSARY.md` per project. As the number of projects
grows and spans multiple domains (coding, research, ops, writing, ...), a
project's glossary accumulates terms only relevant to some work done in it. A
richer model: each project declares the domains it belongs to; each domain
maintains its own glossary layer; an agent loads only the intersection of active
domains rather than the full root table. Open questions: how domains are
declared and discovered; whether domain glossaries live globally (under
`~/agents/`) or per-project; how to handle terms that span domains; whether
per-conversation context budget is the binding constraint that motivates this
at all. No action needed until project count or glossary size makes loading cost
visible.
