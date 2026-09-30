#!/bin/bash
# usage: run-opencode.sh LABEL real|vanilla provider/model
CAP=/home/graehl/agents/surveys/agent-harness-efficiency/.tracks/capture
label=$1 mode=$2 model=$3
shift 3
common=(OPENCODE_CONFIG="$CAP/homes/opencode-stub.json" XDG_DATA_HOME="$CAP/homes/opencode-data"
    OPENCODE_DISABLE_AUTOUPDATE=1 OPENCODE_DISABLE_MODELS_FETCH=1 OPENCODE_DISABLE_LSP_DOWNLOAD=1
    OPENCODE_DISABLE_SHARE=1)
if [ "$mode" = home ]; then
    # real config/instructions/skills, minus the ~/.opencode/agents -> ~/agents link that breaks startup
    common+=(HOME="$CAP/homes/oc-home" XDG_CONFIG_HOME="$CAP/homes/oc-home/.config"
        XDG_CACHE_HOME="$HOME/.cache")
elif [ "$mode" = vanilla ]; then
    common+=(HOME="$CAP/homes/empty-home" XDG_CONFIG_HOME="$CAP/homes/opencode-xdgconfig-empty"
        XDG_CACHE_HOME="$HOME/.cache")
fi
RUN_TIMEOUT=${RUN_TIMEOUT:-120} "$CAP/run.sh" "$label" "${common[@]}" -- \
    opencode run --model "$model" "$@" hi
