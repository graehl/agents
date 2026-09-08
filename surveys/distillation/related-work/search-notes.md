# Distillation search record

**Cutoff: 2026-09-08. Grounded first edition; bounded coverage.** The search
started from the existing tokenizer-free span-tagging survey, then followed
active selection, structured distillation, and explanations of teacher/student
gaps. It did not attempt saturation across all knowledge-distillation papers.

## Retrieval and source coverage

Primary-source searches covered ACL Anthology, arXiv, CVPR, AAAI, and author
publication pages. Queries included dynamic knowledge distillation, active
data curation, structured sequence-labeling distillation, clinical LLM
instructors, teacher assistants, patient consistent distillation, and dataset
cartography. Seven locally fetched sources earned concept pages after reading
their relevant full-text methods and results. Four background citations use
the sibling survey's existing digest and extracts, without new extraction or
independent replication.

HTML fidelity checks passed for Dynamic KD, cartography, teacher assistants,
and error-decay prediction. Active curation and patient-consistent teaching
failed HTML block-fidelity checks and were fetched through PDF/marker instead;
the checks were not relaxed. Clinical instructors used PDF/marker. Extraction
hashes, source URLs, dates, and referenced assets are in each `.fetched` record.

## Citation snowballing

OpenAlex was queried by exact DOI, then forward citations sorted both by
`cited_by_count:desc` and `publication_date:desc`.

- Dynamic KD: `W3200808010`, DOI `10.18653/v1/2021.emnlp-main.31`, 36 citing
  works at lookup; first 12 under each ordering inspected. This found clinical
  instructors and active curation, both fetched. Other candidates included
  *Tailoring Instructions to Student's Learning Levels* (ACL 2023),
  *Improved Knowledge Distillation via Knowledge Selection* (Findings EMNLP
  2022), and *Rethinking Task-Specific Knowledge Distillation: A Contextualized
  Corpus as Better Textbook* (EMNLP 2022).
- Structure-Level KD: `W3034949522`, DOI `10.18653/v1/2020.acl-main.304`, 34
  citing works; first eight under each ordering inspected. High-impact
  candidates included *Improving Named Entity Recognition by External Context
  Retrieving and Cooperative Learning* (ACL 2021), *Automated Concatenation of
  Embeddings for Structured Prediction* (ACL 2021), and *Multi-Grained Knowledge
  Distillation for Named Entity Recognition* (NAACL 2021). Recent matches
  covered more specialized domains; none was accepted as a general result
  merely because it was recent.

These are discovery records. Counts are database observations, not evidence
grades; conference/arXiv duplicates were not counted as independent studies.
Backward references from the selected full texts identified reducible-loss
selection, active NER, and model-change forecasting as adjoining work.

## Disconfirming search and its consequences

Queries explicitly sought limits: `active learning named entity recognition
uncertainty sampling random baseline failure label noise distillation` and
`knowledge distillation data selection irreducible loss student feedback
contextualized corpus`.

The most consequential result was Chang et al.'s [error-decay
prediction](https://arxiv.org/abs/1911.07335). It was fetched and read because
it substantially overlaps the motivating proposal. The map and frontier were
revised to describe it as a predecessor, not to claim a novel empty area.
Its clean-data efficiency limits and contextual independence assumption bound
the proposed experiment.

Full-text checks also bounded the headline claims: Dynamic KD's random
baseline is competitive on original data; cartography has an optimization
failure on small difficult-only subsets; active curation loses some evaluation
slices; patient teaching's fixed-target arm overfits; clinical instructors use
test-set prompt selection and have language-dependent outcomes. No independent
replication dispute was established. These are named negative arms and
methodological limitations, not failed-replication claims.

## Priority follow-up: discovered, not yet read in full

- [A More Robust Baseline for Active Learning by Injecting Randomness to
  Uncertainty Sampling](https://icml.cc/virtual/2023/27400): directly relevant
  to the random-mixture control; only primary abstract inspected.
- [Does Knowledge Distillation Really Work?](https://research.google/pubs/does-knowledge-distillation-really-work/):
  NeurIPS 2021 study of fidelity and optimization; only author-page abstract
  inspected. Read before claiming an irreducible capacity gap.
- [Discrepancy and Uncertainty Aware Denoising KD for Cross-Lingual
  NER](https://ojs.aaai.org/index.php/AAAI/article/view/29762): primary abstract
  inspected; its representation requirements need checking before adoption.
- [Contextualized Corpus as Better Textbook](https://aclanthology.org/2022.emnlp-main.729/):
  contextual retrieval versus simply increasing annotation volume.
- [External Context Retrieving and Cooperative Learning](https://aclanthology.org/2021.acl-long.142/):
  directly bounds the missing-context hypothesis.
- [Automated Concatenation of Embeddings](https://aclanthology.org/2021.acl-long.206/):
  directly relevant to combining encoders before compression.
- [Deep Bayesian Active Learning for NLP](https://aclanthology.org/D18-1318/)
  and [cost-aware clinical NER acquisition](https://pmc.ncbi.nlm.nih.gov/articles/PMC6798575/):
  uncertainty and annotation-cost controls.
- [In Good GRACES: Principled Teacher Selection](https://proceedings.iclr.cc/paper_files/paper/2026/hash/59fa5d049b777d880fdcddba2b24738f-Abstract-Conference.html):
  recent candidate for forecasting a teacher/student pairing; search result
  only, no effectiveness claim adopted.

A September 2026 on-policy distillation preprint surfaced through a secondary
index. It was not accepted as primary-verified evidence and is outside this
first edition's span-labeling focus. Generative reasoning, rationale training,
and large-scale influence estimation remain incompletely covered. Before a
publication novelty claim, expand the follow-up set and citation snowballing.
