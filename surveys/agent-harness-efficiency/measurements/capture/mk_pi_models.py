"""Add stub providers to a scratch pi models.json (never the original)."""

import json
import os
import sys

path = sys.argv[1]
assert "/scratch/" in path, path
d = json.load(open(path)) if os.path.exists(path) else {"providers": {}}
STUB = "http://127.0.0.1:18765"


def models(ids):
    return [{"id": i, "name": f"{i} (stub)", "reasoning": True, "contextWindow": 264000} for i in ids]


d["providers"]["stub-oai"] = {"baseUrl": STUB + "/v1", "api": "openai-completions", "apiKey": "dummy",
                              "models": models(["gpt-5.5", "gpt-5.6-sol", "claude-opus-5"])}
d["providers"]["stub-resp"] = {"baseUrl": STUB + "/v1", "api": "openai-responses", "apiKey": "dummy",
                               "models": models(["gpt-5.5", "gpt-5.6-sol"])}
d["providers"]["stub-anth"] = {"baseUrl": STUB, "api": "anthropic-messages", "apiKey": "dummy",
                               "models": models(["claude-opus-5"])}
json.dump(d, open(path, "w"), indent=2)
print("wrote", path, list(d["providers"]))
