#!/bin/sh
# Returns the upstream default branch name
git rev-parse --abbrev-ref origin/HEAD 2>/dev/null | sed 's/origin\///' && exit
git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/origin/||' && exit
# Gerrit often uses master; fall back to it
echo master
