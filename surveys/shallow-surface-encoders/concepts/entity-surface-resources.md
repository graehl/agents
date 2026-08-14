# entity-surface-resources — authentic multilingual carriers and validators

> Read-backed digest (cluster I, trust `single-source` for each corpus). Named-
> entity corpora, gazetteers, locale standards, and high-precision mining play
> different roles. No located source supplies representative contextual spans
> for every PII family across the target languages.

**Papers.** Steinberger et al., “JRC-NAMES: A Freely Available, Highly
Multilingual Named Entity Resource,” RANLP 2011; Tedeschi and Navigli,
“MultiNERD,” Findings of NAACL 2022; Fetahu et al., “MultiCoNER v2,”
Findings of EMNLP 2023; Mayhew et al., “Universal NER,” NAACL 2024.
**Full text:** [JRC-NAMES](https://aclanthology.org/R11-1015/) ·
[MultiNERD](https://aclanthology.org/2022.findings-naacl.60/) ·
[MultiCoNER v2](https://aclanthology.org/2023.findings-emnlp.134/) ·
[UNER](https://aclanthology.org/2024.naacl-long.243/).

## Source roles

| resource | useful evidence | boundary that must survive intake |
|---|---|---|
| [JRC-NAMES](https://joint-research-centre.ec.europa.eu/language-technology-resources/jrc-names_en) | person and organization spelling variants observed in multilingual news, including cross-script aliases | mostly automatic and biased toward public/high-frequency entities; a name list is neither carrier text nor negative supervision; capture edition-specific terms because the historical download page points to an EULA while the current RDF catalogue states an EC reuse notice |
| MultiNERD | Wikipedia/Wikinews carriers in ten languages with fifteen silver entity types | automatic annotations and entity-linking construction; its manually checked fine-grained test is English; the released data is CC BY-NC-SA 4.0 and therefore a research/audit source, not an assumed commercial training source |
| MultiCoNER v2 | low-context Wikipedia/Wikidata carriers in twelve languages, with 33 fine types under six coarse groups and a large entity gazetteer | Bengali, Chinese, German, and Hindi carriers were translated from English; synthetic corruption belongs to robustness evaluation, not the clean natural pool; the paper says CC BY-SA 4.0 while the AWS registry says CC BY 4.0, so resolve the terms attached to the exact downloaded files before admission |
| UNER v1 | native-speaker gold spans on 19 Universal Dependencies datasets across 13 language varieties, with a shared person/organization/location schema | only some datasets have train/dev/test; domains and original treebank terms vary; CC BY-SA 4.0; useful for audit/calibration but too coarse and narrow to stand in for PII coverage |
| [Wikidata dumps](https://www.wikidata.org/wiki/Wikidata:Database_download/en) | CC0 multilingual labels, aliases, type links, and structured seeds | public-entity and label-availability bias; not contextual supervision |
| [GeoNames](https://download.geonames.org/export/dump/readme.txt) | CC BY 4.0 place names, alternate names with language codes, country/admin metadata, and population | geographic names only; language tags and feature records need filtering and deduplication |
| [CLDR person names](https://www.unicode.org/reports/tr35/tr35-personNames.html) | locale-specific name order, spacing, punctuation, and formatting rules | a format oracle, not an inventory or frequency model |
| [libphonenumber](https://github.com/google/libphonenumber) | region-aware parsing, formatting, validation, and number-type metadata | a validator/generator; it does not estimate how people write numbers in the target domain |
| [SWIFT IBAN registry](https://www.swift.com/resource/iban-registry-pdf) | official ISO 13616 national IBAN structures | an account-format oracle, not authentic frequency or carrier text |

The role distinction is load-bearing. A registry can validate or seed a
surface; it cannot establish contextual prevalence, span boundaries, negative
examples, or natural language. Conversely, a high-precision tagger can recover
authentic carriers but cannot make its own omissions representative.

## Named-entity corpus coverage

For the current twenty-language commissioning set
`ar cs de en es fr hi id it ja ko nl pl pt ru sv tr uk vi zh`, the three
contextual corpora have the following explicit overlap:

| corpus | current-set overlap | Final35 additions represented |
|---|---|---|
| MultiNERD | `de en es fr it nl pl pt ru zh` | none |
| MultiCoNER v2 | `de en es fr hi it pt sv uk zh` | `bn fa` |
| UNER v1 | `de en pt ru sv zh` | `da hr fil` (released as Tagalog `tl`) |

JRC-NAMES covers many languages and scripts but does not expose a clean,
exhaustive language-support promise suitable for this matrix. Wikidata and
GeoNames can provide seeds much more broadly, with uneven label availability.
Neither fact closes a contextual-data cell.

The proposed Final35 extension retains all twenty current languages and adds
`bn te hr da fi el ro no th ms fil fa ta ur he`. Every one of those fifteen
inherits the complete acquisition and fluent-review debt below. Incidental
coverage in MultiCoNER or UNER is useful intake, not a waiver. In particular,
no translation, synthetic realization, training, or commissioning is implied
merely by naming the extension.

## Acquisition and admission protocol

Build the natural pool in source-role layers rather than flattening all rows
into one claimed distribution:

1. Admit human gold contextual spans first, retaining original document,
   character offsets, annotation policy, split, and license.
2. Admit authentic-context corpora after mapping only reachable labels and
   preserving whether the row was native, translated, silver, or manually
   annotated.
3. Use structured resources for native surfaces, aliases, formatting, and
   validation. Preserve the full name, components, order, script, locale,
   source identifier, and aliases; do not force Western first/last-name fields.
4. Mine large authentic text with a high-precision teacher, the best incumbent,
   or their agreement. Keep the original carrier and score/provenance. Treat
   positive-only mining as positive supervision, not evidence about negatives
   or recall.
5. Use a locale-audited Faker-style generator only for families and languages
   whose rules and output have passed fluent review. Synthetic rows remain a
   separately measurable source.

Every admitted row records at least language decision and confidence, script,
locale/region when known, PII family and mapped label, source role, source
dataset/document/row, native-versus-translated construction, generator or
teacher version, acquisition date, license/terms reference, and a content hash.
Deduplicate both exact carrier occurrences and normalized surfaces, while
retaining their exposure counts. Sample language weights only at an explicit
large-pool gate; do not let a later normalization silently turn a requested
small dose into zero.

## Source-blind subjective evaluation

Quality review needs two complementary views for each language and family:

- **exposure-weighted:** estimates what the training stream actually repeats;
- **distinct-surface:** exposes memorized templates and a poor long tail.

Hide dataset, path, generator, teacher, row ID, and sampling-view identity from
the reviewer. Show enough carrier context to judge the span. Collect
naturalness, locale fit, type correctness, boundary correctness, formatting,
name order, likely origin, and free-form defect notes. Use a stable second-
review subset and preserve disagreements rather than manufacturing agreement.
Surface-only lists are a separate audit mode and cannot substitute for
contextual judgment.

Admission is reported as a source-by-language-by-family ledger. Union coverage
can hide that a family is supplied only by translated or synthetic data, so it
is never the sole readiness claim. The current twenty languages receive the
first complete audit and repair pass. The fifteen proposed additions owe the
same pass before commissioning, including native-speaker or comparably fluent
review; their existing-corpus overlap only determines which acquisition layer
can be attempted first.

## Decision

The immediate data program should combine, rather than choose among, structured
seeds and authentic carriers. JRC-NAMES, Wikidata, GeoNames, CLDR,
libphonenumber, and SWIFT provide inventories or validity constraints.
MultiNERD, MultiCoNER, UNER, and high-precision mining provide contextual
evidence with different language, domain, quality, and licensing limits. This
is enough to build and audit a materially better surface pool, but not enough
to declare any language/family complete before the blinded human review.
