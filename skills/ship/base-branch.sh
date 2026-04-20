#!/bin/sh
# Print the most likely integration branch name for the current repo.
# Resolution order:
# 1. remote default branch from origin/HEAD
# 2. local main, if present and master is absent
# 3. local master, if present and main is absent
# If none of the above gives a unique answer, exit nonzero so the caller can ask.

remote_default="$(git rev-parse --abbrev-ref origin/HEAD 2>/dev/null | sed 's|^origin/||')"
if [ -n "$remote_default" ] && git rev-parse --verify "$remote_default" >/dev/null 2>&1; then
  printf '%s\n' "$remote_default"
  exit 0
fi

remote_default="$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|^refs/remotes/origin/||')"
if [ -n "$remote_default" ] && git rev-parse --verify "$remote_default" >/dev/null 2>&1; then
  printf '%s\n' "$remote_default"
  exit 0
fi

has_main=0
has_master=0
git rev-parse --verify main >/dev/null 2>&1 && has_main=1
git rev-parse --verify master >/dev/null 2>&1 && has_master=1

if [ "$has_main" -eq 1 ] && [ "$has_master" -eq 0 ]; then
  printf 'main\n'
  exit 0
fi

if [ "$has_master" -eq 1 ] && [ "$has_main" -eq 0 ]; then
  printf 'master\n'
  exit 0
fi

exit 1
