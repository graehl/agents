#!/bin/bash
# usage: run.sh LABEL [VAR=val ...] -- cmd args...
# Runs cmd in a clean environment inside the empty workdir, with stub LABEL set.
set -u
CAP=/home/graehl/agents/surveys/agent-harness-efficiency/.tracks/capture
W=/local/graehl/scratch/harness-hi-empty
label=$1
shift
envs=()
while [ "$#" -gt 0 ] && [ "$1" != "--" ]; do
    envs+=("$1")
    shift
done
shift
echo "$label" >"$CAP/LABEL"
mkdir -p "$CAP/out"
printf '%q ' "${envs[@]}" "$@" >"$CAP/out/$label.cmd"
echo >>"$CAP/out/$label.cmd"
cd "$W" || exit 1
timeout ${RUN_TIMEOUT:-180} env -i HOME="$HOME" USER="$USER" PATH="$PATH" TERM=dumb LANG=C.UTF-8 \
    SHELL=/bin/bash "${envs[@]}" "$@" </dev/null >"$CAP/out/$label.out" 2>"$CAP/out/$label.err"
rc=$?
echo "rc=$rc" >>"$CAP/out/$label.cmd"
echo "[$label] rc=$rc"
tail -c 600 "$CAP/out/$label.out"
echo "--- err"
tail -c 1200 "$CAP/out/$label.err"
ls "$CAP/runs/$label" 2>&1 | head -20
