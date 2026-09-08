# Annotation-only teachers for clinical extraction

**Source:** Meoni, de la Clergerie, and Ryffel, BioNLP 2023, *Large Language
Models as Instructors: A Study on Multilingual Clinical Entity Extraction*.
[Full text](https://aclanthology.org/2023.bionlp-1.15.pdf) ·
[local extract](../related-work/extract/meoni2023-clinical-instructors/meoni2023-clinical-instructors.md).
Read: prompting, text alignment, five-language data and training setup,
results, discussion, and limitations.

InstructGPT-3 emits clinical entity strings. A resolver aligns them to source
text, and encoder models train on the resulting BIO labels. The authors have
prediction access only; there is no hidden-state transfer. They also combine
LLM annotations with dictionary-derived supervision. This is a directly
relevant precedent for hard-span distillation.

**Effectiveness: single-source.** Table 3 reports teacher versus aggregated
student F1 of 0.71/0.66 for English, 0.74/0.70 for Spanish, 0.60/0.61 for
Basque, 0.74/0.75 for French, and 0.63/0.75 for Italian. The direction varies
by language. These are narrow clinical-entity extraction results, not a broad
PII ontology. Language-specific model collections also differ.

**Limitations that matter:** Section 4.2 selects among three prompt example
sets using the reported test set. The study acknowledges small test data;
dictionary resources include terms from the gold standard. Its definition of
the mixture ratio is internally inconsistent in one setup paragraph; figures
and Table 4 identify the endpoints. These issues prevent using the numbers as
an independent estimate of teacher/student ceilings.

The source also explains that UMLS linking conventions can split or shorten
gold spans relative to a generic clinical prompt. Apparent extraction errors
can therefore reflect annotation conventions. For Ont3, keep guideline
agreement, input-context equality, and student learning separate. Neither
blind span union nor a teacher's fluent output resolves those distinctions.
