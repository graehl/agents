# Template authoring guide provenance

This record covers `README.md` and its license only. The template library
itself is authored in this repository; individual vendored resources retain
their own provenance records.

## Upstream

- Repository: https://github.com/graehl/yepanywhere
- Source: `site/src/content/docs/project-templates.md` (moved from
  `topics/project-template-authoring.md` in YA `c3f56f11d`)
- Commit: `5f00b0f2be00b0214c62000c28a039c46d6bae52`
- Commit date: 2026-10-19
- Subject: List the repo-view and program-view template bases

## Vendored

2026-10-19. The pinned commit was available in the local YA checkout;
publication of that commit is separate from this synchronization. The copy
now starts with the site page's title/description front matter instead of an
H1. A repo-view sentence added here directly in `31be972e` was moved into the
canonical guide first, so this copy is again byte-identical.

## License

MIT, copyright 2025–2026 Kyle Graehl, from YA's root `LICENSE` at the
pinned commit. Its complete notice is preserved in `README.LICENSE`.

## Vendored files

| Destination | Upstream path | SHA-256 |
| --- | --- | --- |
| `README.md` | `site/src/content/docs/project-templates.md` | `566ed5970dc5c4a013f16980036ce46dea91c4ceb1a84c495f68e6baa9fe4188` |
| `README.LICENSE` | `LICENSE` | `63d4dea8ee5061785faa9738ca7452dd1f05dfdc94d35ef64188e19dd2ad5a15` |

## Local changes

None. The guide and license are byte-for-byte copies of their upstream files.
Edit the canonical YA guide, then synchronize this copy.

## Re-sync

From the agents repository root, check drift against the recorded pin:

```sh
guide_rev=5f00b0f2be00b0214c62000c28a039c46d6bae52
git -C "$HOME/ya" show "$guide_rev:site/src/content/docs/project-templates.md" |
  cmp - project-templates/README.md
git -C "$HOME/ya" show "$guide_rev:LICENSE" |
  cmp - project-templates/README.LICENSE
sha256sum project-templates/README.md project-templates/README.LICENSE
```

To update, first commit and review the canonical guide in YA. Set `guide_rev`
to that full commit SHA, then copy exactly:

```sh
git -C "$HOME/ya" show "$guide_rev:site/src/content/docs/project-templates.md" > \
  project-templates/README.md
git -C "$HOME/ya" show "$guide_rev:LICENSE" > project-templates/README.LICENSE
```

Update this record's revision, date, subject and checksums, verify with `cmp`,
and commit the synchronized files together. Keep user-facing instructions in
the canonical guide rather than adding local README changes.
