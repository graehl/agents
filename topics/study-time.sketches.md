# Study time: activity indexing and deferred interest

Candidate implementation for the [study-time workflow](study-time.md).
The pre-alpha skill retrieves activity on demand; this index is not built.

## Context that survives the work

Ingest authorized project artifacts, commits, plans, and chat turns with
source IDs, timestamps, project identity, and speaker. Preserve meaningful
context windows rather than isolated sentences. Tag the relation to a topic:

| Evidence type | Meaning |
|---|---|
| Mention | Appears in passing; weak signal by itself. |
| Implementation focus | Material to code, an experiment, or a result. |
| User discussion | The person substantively asks, explains, critiques, or connects it. |
| User-considered option | The person weighs it in planning, even if rejected. |
| Agent-considered option | An agent raises it; potentially important without user endorsement. |

Keep considered, selected, rejected, and implemented distinct. An important
rejected alternative may teach more than the selected routine method. Preserve
the reason for rejection. Tags can overlap and should carry their supporting
span and uncertain attribution; do not force each item into one category.

Use lexical retrieval plus semantic embeddings, with source, time, actor,
and project filters. Retrieve diversity across conceptual neighbors before
reranking. Deduplicate copied summaries so agent verbosity does not dominate.
Candidate generation should include useful absences and connections inferred
from the retrieved context, with an explanation of the inference. Embeddings
do not directly establish either importance or a learner's knowledge.

Keep private text and indexes local by default; remote embedding services
need an explicit data boundary. Incremental refresh uses content hashes and
source versions, supports deletion, and invalidates derived entries when a
source disappears. The source remains authoritative over generated tags.

## Later means less often

Separate familiarity, interest, recall, and deferral. “Already know this” can
skip an introduction without preventing deeper exploration. “Later” signals
low current priority, not a failed recall attempt.

A candidate policy is to skip roughly 1, then 3, then 7 eligible study
sessions after repeated low-engagement deferrals, then shelve it. These are
tunable defaults, not validated memory intervals. A substantive question or
demo exploration can reset the interest backoff. Passive page views cannot.
Retain the optional free-text request with the candidate for its return.
New high-value context may justify resurfacing a shelved topic with a reason;
the user can dismiss it outright. No streaks or overdue counters are needed.

If retention is requested after learning, use an established scheduler such
as FSRS with actual recall observations. Do not feed interest postponements
into a forgetting model as failed recalls.

## Test whether the experience pays

First test whether a single invitation makes the person want to explore,
whether the toy demo clarifies something, and whether the follow-up fits.
Record optional feedback about enjoyment, useful recognition, better
supervision, explanation, or transfer. Time spent and cards completed are
interaction measures, not proof of understanding or general cognitive gain.
Only build the index after enough practice identifies what context selection
gets wrong and what persistent information would fix it.
