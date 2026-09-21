# Template authoring guide provenance

This record covers `README.md` and its license only. The template library
itself is authored in this repository; individual vendored resources retain
their own provenance records.

## Upstream

- Repository: https://github.com/graehl/yepanywhere
- Source: `topics/project-template-authoring.md`
- Commit: `799bcd2b3a40175a77f9635e768f42b7319d0ce1`
- Commit date: 2026-09-21
- Subject: Document GitHub directory URLs and local template overlays

## Vendored

2026-09-21. The pinned commit was available in the local YA checkout;
publication of that commit is separate from this synchronization.

## License

MIT, copyright 2025–2026 Kyle Graehl, from YA's root `LICENSE` at the
pinned commit. Its complete notice is preserved in `README.LICENSE`.

## Vendored files

| Destination | Upstream path | SHA-256 |
| --- | --- | --- |
| `README.md` | `topics/project-template-authoring.md` | `44f68700d290f2ca4749918931b86f996d093a0b2c955c8a8d0ec280c4e58d3d` |
| `README.LICENSE` | `LICENSE` | `63d4dea8ee5061785faa9738ca7452dd1f05dfdc94d35ef64188e19dd2ad5a15` |

## Local changes

None. The guide and license are byte-for-byte copies of their upstream files.
Edit the canonical YA guide, then synchronize this copy.

## Re-sync

From the agents repository root, check drift against the recorded pin:

```sh
guide_rev=799bcd2b3a40175a77f9635e768f42b7319d0ce1
git -C "$HOME/ya" show "$guide_rev:topics/project-template-authoring.md" |
  cmp - project-templates/README.md
git -C "$HOME/ya" show "$guide_rev:LICENSE" |
  cmp - project-templates/README.LICENSE
sha256sum project-templates/README.md project-templates/README.LICENSE
```

To update, first commit and review the canonical guide in YA. Set `guide_rev`
to that full commit SHA, then copy exactly:

```sh
git -C "$HOME/ya" show "$guide_rev:topics/project-template-authoring.md" > \
  project-templates/README.md
git -C "$HOME/ya" show "$guide_rev:LICENSE" > project-templates/README.LICENSE
```

Update this record's revision, date, subject and checksums, verify with `cmp`,
and commit the synchronized files together. Keep user-facing instructions in
the canonical guide rather than adding local README changes.
