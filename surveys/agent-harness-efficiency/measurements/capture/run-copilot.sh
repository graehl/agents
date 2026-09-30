#!/bin/bash
# usage: run-copilot.sh LABEL real|vanilla openai|anthropic completions|responses MODEL [extra args]
CAP=/home/graehl/agents/surveys/agent-harness-efficiency/.tracks/capture
label=$1 mode=$2 ptype=$3 wire=$4 model=$5
shift 5
base=http://127.0.0.1:18765/v1
[ "$ptype" = anthropic ] && base=http://127.0.0.1:18765
envs=(COPILOT_HOME="$CAP/homes/copilot-$mode" COPILOT_PROVIDER_BASE_URL="$base"
    COPILOT_PROVIDER_TYPE="$ptype" COPILOT_PROVIDER_API_KEY=dummy COPILOT_PROVIDER_WIRE_API="$wire"
    COPILOT_MODEL="$model")
[ "$mode" = vanilla ] && envs+=(HOME="$CAP/homes/empty-home")
RUN_TIMEOUT=${RUN_TIMEOUT:-120} "$CAP/run.sh" "$label" "${envs[@]}" -- \
    copilot -p hi --allow-all-tools --log-dir "$CAP/out/copilot-logs-$label" "$@"
