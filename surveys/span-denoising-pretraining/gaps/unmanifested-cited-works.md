---
slug: unmanifested-cited-works
noticed: 2026-11-25
where: concepts/multilingual-mt-systems.md, concepts/prompted-mt.md, related-work/papers.yaml
---

**Gap:** the two concept pages give exact figures for about twenty works
that have no `papers.yaml` row and no extract, so `related-work audit`
cannot see them and nothing checked their numbers against a fetched
source. All 15 manifested papers are grounded (2026-11-26). The first
grounding pass found a substantive error (MADLAD-400's layer split,
attributed to a configuration file that says otherwise), so the
ungrounded figures deserve the same check.

Unmanifested, with figures quoted:

- `multilingual-mt-systems.md`: NLLB-200 (Nature 2024) and the NLLB
  expert-pruning study (ACL 2023); TaskMoE (Findings EMNLP 2021);
  Lingual-SMoE (ICLR 2024); THOR-MoE (ACL 2025); SMaLL-100 (2022);
  LiLa and the findings paper (WMT26); Gao et al. (AACL 2022); Qu et al.
  (MRL 2025); the MiLMMT report (arXiv 2608.10812); Sälevä and Lignos
  (LoResLM 2026); the TranslateGemma report (arXiv 2601.09012).
- `prompted-mt.md`: the WMT22 multilingual domain-adaptation study;
  Garcia and Firat (2022); Jauregi Unanue et al. (Findings EACL 2026);
  Hy-MT2 (arXiv 2605.22064). Johnson et al. (2017), Dinu et al. (2019),
  Xu et al. (2020) and the WMT25 retrieval comparison are cited without
  figures.

**Noticed while:** the automatic review of 2026-11-25 (triage gap,
closed).
**Fix sketch:** add a manifest row per work with its venue metadata,
`related-work fetch` them, check each quoted figure against its extract,
and link the extract from the concept page. A row added without a fetch
must say `grounded: false`, not borrow the verified state of its link.
