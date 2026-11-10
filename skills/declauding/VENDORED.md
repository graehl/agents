# Vendored: declauding

Third-party code copied into this repo, pinned to an exact upstream commit.
Do not edit casually: log every change under "Local changes" so a re-sync
can re-apply it. Convention: `topics/vendoring.md`. Regenerate/verify with
`vendor-skill` (see `topics/helper-scripts.md`).

## Upstream

- **Repo:** https://github.com/oaustegard/claude-skills
- **Subpath:** `declauding`
- **Commit:** `c896746d46951a1fcbb40c398d44d9c7ee8e4ce3`
  (chore: regenerate plugin marketplace [skip ci], 2026-11-10)
- **Vendored:** 2026-11-10

## License

upstream license file(s) detected: LICENSE. vendor-skill does not copy root-level license files automatically; consult upstream before redistributing or relicensing.

The root `LICENSE` at the pinned commit is the MIT License, "Copyright (c)
2025 Oskar Austegard".

## Vendored files

| file | sha256 (at vendor time) |
|------|-------------------------|
| `CHANGELOG.md` | `2728889885fba6dfdadaf3454ebeb39ea8b294fc309530ae94985182fbc3ae3a` |
| `README.md` | `b55a5fa89520c4ee88bb5e4d2a9b2a53377775b7132affd6edd3f54dcc5ac20b` |
| `SKILL.md` | `f9ef43d7c4ccf0743dce6f5c85cc0fbfc262f00630218d7ff96940f87ed4c52a` |
| `assets/annotated.template.html` | `2d5a594d39feec7dcb01c6dd9243d7f224737700d7f7c892dc954ebe9a0748b9` |
| `assets/staging-axis.json` | `ed6a78ddff147695793c99f8a3a624f488fa2076023690fddb8cbf2637fcdea8` |
| `hooks/hooks.json` | `19e45029237b1a2e8dd31f7888eacb3114f6afe504ce9f4f08d27d23ec0631e1` |
| `references/annotating.md` | `beb1e73dca3a3c4999e38a0ed7dd3e38043c58d3f12039437f5343fc8b269a3c` |
| `references/corpus.md` | `e282ca27093a492af0d09acf4c3f57caac910cbef044f2da6d5998c5a34234d9` |
| `references/exceptions.md` | `80a3b66b1bf12aaad9af6cd8fec3d59042f917250dc4f1c381a15434a73c8ed3` |
| `references/fresh-eyes.md` | `1917ebd0ce38c0ebb6b4fcf615474482a9a5bba5ddf5287465ffdf6d491a69d2` |
| `references/models/fable.md` | `04d313cb9a92de5b122140f8f4bd4e2718c38ebb06f974558edbfa93c189a5f5` |
| `references/models/haiku.md` | `8c2cb93c8f2c4c49309ff73311b7c4a36d91e314bc5e8f3636d012d837da7fe9` |
| `references/models/opus-4.md` | `f58c5455e83fc984e88a549c2fff6562de5b3fa50e213bbb4bb9dfb8d6a471fe` |
| `references/models/opus-5.md` | `ecab11ee3a1b8bfd3ba108cd6ded9c8c1a942891c70366edbfa205b4309c8379` |
| `references/models/sonnet.md` | `2b658d1a9c9f26ae4a9d71f420ea53567c756850d4eae2c854750f0071b04398` |
| `references/preservation.md` | `ac065c549bae3ba24a06bfd8eb5c9de1a87e0b2633aead88328abc61d1259e3f` |
| `references/register.md` | `dc1f03674206a56440748b7fcfacf1242300d1d2b80b0fe8428fae5de59ae3c4` |
| `scripts/declaude_diff.py` | `53eb90b7c3909bfa75e98417e3c7644c8e043319f5e13458177f7865686b995c` |
| `scripts/declaude_lint.py` | `6d744f774008b806a4bb7b76610cc4762fa485a750c82adea005aa73718b1ae5` |
| `scripts/declaude_rank.py` | `ba12f444c2bfabae3f394227273fdf6b27dba7735b1a91e6eba0f16423354b6b` |
| `scripts/declaude_review.py` | `4390fe547444ced00cc3a408ecd2862636cfc34de515d4f2dff9ea4154a523ec` |
| `scripts/fresh_eyes.py` | `5e710f7b1d6c8b971845cbe03a13232bee2d0fba4c63a1d20444554ffda9fee5` |
| `tests/sample-clean.md` | `731db4a0b23b55e8986e76a83591501d4bc8a3b6643ab95c0c0656cc114732ab` |
| `tests/sample-structure.html` | `714c832143be452851d2a0f170f099f487e9f2cb8b74b1c885cdb0e2e563db56` |
| `tests/sample-structure.md` | `9e41ca42c85a6bc67947cfa7e4c2a1988ae36da77a0d55fa38b234974eb76b25` |
| `tests/sample-tics.md` | `6441260a3a341cbf7a8624cfa97e2808c258794f856cb4931c357a70e5cd29dd` |
| `tests/test_fresh_eyes.py` | `1b01345d7b055efd0886c89a838a3fe2c7ba0fe7a4e5e49df2a7070f17a1f66a` |

## Local changes

- `SKILL.md` frontmatter gains `disable-model-invocation: true`. Upstream's
  description asks to be loaded for every commit message, PR description,
  and README; here the pass runs on request through `skills/not-ai/SKILL.md`,
  which is the entry point and states the other differences in use (scan
  through `scripts/not-ai-lint`, `declaude_review.py` only with
  `--emit-prompt`, hooks unused). `vendor-skill --check` therefore reports
  `SKILL.md` as drifted by that one line.

Everything else is a verbatim copy of the upstream subpath at the pinned
commit, which carries skill version 0.14.0 (`declauding-v0.13.0` is commit
`89bb12a654b75ce33ad3cb03c67b14e5518063dc`). Record every later local edit
here (what changed and why) so the next re-sync can re-apply it against new
upstream.

## Re-sync from upstream

```bash
vendor-skill --check declauding        # report drift vs current upstream HEAD
vendor-skill https://github.com/oaustegard/claude-skills declauding declauding  # re-pin to a new commit
```

After re-pinning, re-apply anything listed under "Local changes" and update
that section.
