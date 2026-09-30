#!/bin/bash
# usage: run-codex.sh LABEL HOMEDIR MODEL [extra codex args...]
CAP=/home/graehl/agents/surveys/agent-harness-efficiency/.tracks/capture
label=$1 home=$2 model=$3
shift 3
RUN_TIMEOUT=${RUN_TIMEOUT:-90} "$CAP/run.sh" "$label" CODEX_HOME="$CAP/homes/$home" STUB_KEY=dummy -- \
    codex exec --skip-git-repo-check --ephemeral \
    -c features.hooks=false \
    -c model_providers.stub.name=stub \
    -c model_providers.stub.base_url=http://127.0.0.1:18765/v1 \
    -c model_providers.stub.wire_api=responses \
    -c model_providers.stub.env_key=STUB_KEY \
    -c model_provider=stub \
    -m "$model" "$@" hi
