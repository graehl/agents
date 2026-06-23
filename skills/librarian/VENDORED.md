# Vendored: librarian

Third-party code copied into this repo, pinned to an exact upstream commit.
Do not edit casually: log every change under "Local changes" so a re-sync
can re-apply it. Convention: `topics/vendoring.md`. Regenerate/verify with
`vendor-skill` (see `topics/helper-scripts.md`).

## Upstream

- **Repo:** https://github.com/xl0/agent-files
- **Subpath:** `skills/librarian`
- **Commit:** `8c72904b189830eb0138978dd3fd583f56c99c78`
  (Clean up librarian skill, rewrite fetcher in python, 2026-06-20)
- **Vendored:** 2026-06-22

## License

NO LICENSE/COPYING file upstream at the pinned commit. Treat as all-rights-reserved-by-default; re-check the repo's terms before redistributing or relicensing.

## Vendored files

| file | sha256 (at vendor time) |
|------|-------------------------|
| `SKILL.md` | `9ec1ba8f81846c6ddf33c0387bb16391130301e342d58b5be858b7ee47e2cd85` |
| `checkout.py` | `d44ae18e3c597f01408ec57f3fa678c526a52db9033337f946ff4e16ef10f2cc` |

## Local changes

- `checkout.py`: strip GitLab (`/-/tree`, `/-/blob`, etc.) and Bitbucket
  deep-link suffixes to the repository path; warn when a fetched checkout
  cannot fast-forward.

## Re-sync from upstream

```bash
vendor-skill --check skills/librarian        # report drift vs current upstream HEAD
vendor-skill https://github.com/xl0/agent-files skills/librarian skills/librarian  # re-pin to a new commit
```

After re-pinning, re-apply anything listed under "Local changes" and update
that section.
