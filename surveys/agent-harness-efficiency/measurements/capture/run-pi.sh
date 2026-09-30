#!/bin/bash
# usage: run-pi.sh LABEL AGENTDIR-NAME provider/model [extra pi args...]
CAP=/home/graehl/agents/surveys/agent-harness-efficiency/.tracks/capture
label=$1 dir=$2 model=$3
shift 3
RUN_TIMEOUT=${RUN_TIMEOUT:-90} "$CAP/run.sh" "$label" \
    PI_CODING_AGENT_DIR=/local/graehl/scratch/harness-capture-homes/$dir PI_OFFLINE=1 -- \
    pi -p --no-session --offline --model "$model" "$@" hi
