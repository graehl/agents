# Untranscribed speech vocabulary

| Term | Sense in this survey | Reference |
|---|---|---|
| acoustic domain | Recording conditions and speech style; speaker/language are targets or nuisances depending on the task | [map](survey.md#what-no-transcript-and-domain-mean-here) |
| alternating-speaker spans | Ordered speech intervals with multiple speakers across time, mostly one active at a time; distinct from overlapping voices | [conditions](concepts/condition-views.md) |
| audio-only SSL | Self-supervised learning from audio without transcript-derived target geometry; refers to the base checkpoint, not every fine-tuned derivative | [representations](concepts/audio-domain-representations.md) |
| dataset streaming | Incremental reading of an existing archive; does not imply live acquisition | [capture](concepts/sources-and-capture.md) |
| live edge | Latest published media available to a collector, already subject to upstream delay | [capture](concepts/sources-and-capture.md) |
| no-transcript | Three separate constraints: no source transcript requirement, no ASR during embedding, or no transcript-derived training geometry | [map](survey.md#what-no-transcript-and-domain-mean-here) |
| semantic domain | Spoken subject matter and intent, distinct from recording conditions | [representations](concepts/audio-domain-representations.md) |
| source archive | Immutable recording bytes with provenance; segments and model inputs are versioned derived views | [storage](concepts/storage-and-compression.md) |
| span view | A versioned selection from immutable recordings, such as clean single-speaker, clean alternating-speaker or mixed-condition speech | [conditions](concepts/condition-views.md) |
