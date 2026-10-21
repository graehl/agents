# Training and evaluation data boundaries

> Preserve source identity and meaningful split independence when acquiring, segmenting or partitioning model data.

Topic: `training-data`

Read when acquiring or partitioning training/evaluation data, including
corpus-quality smoke evaluations. This conditional route is reached from
[ML model development](ml-model-development.md); it is not a routine read
for inference on an already frozen, unchanged evaluation set.

## Split the source before its segments

Choose the independence unit for the claim before sampling or segmenting.
Keep a source document, recording, conversation or episode wholly within one
train/dev/test role where that boundary is available. Related sentences or
audio crops share content, voices and recording conditions; random row splits
can overstate generalization. Retain parent identifiers through segmentation,
transcription, translation, augmentation and repackaging, and check that
parent sets do not intersect across roles.

Document/recording separation does not establish speaker, author, site or
domain separation. Add those grouping constraints when the intended claim
requires them, and report unknown identities or unavoidable overlap. Do not
claim unseen-speaker performance from recording-disjoint data alone.

Preserve established benchmark split roles. If a source spans upstream
splits, prevent its training portions from leaking into a custom held-out
comparison; record the exclusion or whole-source reservation. A new internal
split may be useful, but name it as such rather than silently relabeling the
publisher's benchmark. Freeze group assignments, selection rule and seed
before viewing model results, and retain reservations independently of which
files were successfully retrieved. New segments inherit their parent's role.

When boundaries are unavailable, record that limitation and use the strongest
available grouping or overlap check. A tiny smoke may still diagnose decoding
or transcript alignment without supporting a generalization claim; do not
discard useful diagnostics merely because stronger independence is impossible.

## Acquire to the decision's scale

For a bounded quality evaluation, retrieve the needed source material and
metadata rather than automatically ingesting the whole corpus. A web article
and its radio recording may be separate aligned-data candidates: retain both
identities and verify transcript correspondence instead of assuming that
co-location implies a verbatim transcript. Keep original references and
provenance when preparing an evaluation view. Corpus acquisition permissions
and project license/quarantine rules still apply.

Scoring and selection roles remain governed by
[research evidence](../_RESEARCH/evidence.md); important outputs and row-wise
transform provenance by [RUNS](../RUNS.md). Project-specific split contracts
take precedence over these defaults.
