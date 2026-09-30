"""Render the report table (main agent-turn requests only) from analysis.json."""

import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
rows = [r for r in json.load(open(os.path.join(ROOT, "analysis.json"))) if r["main"]]

HARNESS = {"cc": "Claude Code 2.1.285", "cx": "Codex 0.159.2", "pi": "pi 0.85.1",
           "oc": "opencode 1.18.31", "cp": "Copilot CLI 1.0.85"}
COND = {
    "cc-a-default": "user config (~/.claude)", "cc-b-bare": "--bare", "cc-b2-simple": "CLAUDE_CODE_SIMPLE=1",
    "cc-c-sol": "user config, ANTHROPIC_MODEL", "cc-d-haiku": "user config, ANTHROPIC_MODEL",
    "cc-d-opus": "user config, ANTHROPIC_MODEL", "cc-e-bare-sol": "--bare, ANTHROPIC_MODEL",
    "cc-f-vanilla": "empty CLAUDE_CONFIG_DIR", "cc-f-vanilla-sol": "empty CLAUDE_CONFIG_DIR",
    "cc-f-vanilla-haiku": "empty CLAUDE_CONFIG_DIR",
}


def cond(label):
    if label in COND:
        return COND[label]
    p = label.split("-")
    if label.startswith("cx-"):
        return {"real": "user config copy (AGENTS.md)", "noag": "user config copy, no AGENTS.md",
                "vanilla": "empty CODEX_HOME + empty HOME"}[p[1]]
    if label.startswith("pi-"):
        return {"real": "user agent dir copy", "vanilla": "empty agent dir, real HOME",
                "bare": "empty agent dir + empty HOME", "lovely": "user copy + pi-lovely-codex"}[p[1]] + \
            f" [{p[3]}]"
    if label.startswith("oc-"):
        return {"home": "user config (minus broken agents link)", "vanilla": "empty config + HOME"}[p[1]] + \
            f" [{p[2].replace('stub', '')}]"
    if label.startswith("cp-"):
        return {"real": "user COPILOT_HOME copy", "vanilla": "empty COPILOT_HOME + HOME"}[p[1]] + \
            f" [{p[2]}]"
    return label


print("| harness | model | condition (api) | system ch / tok | tools n / tok | instr files tok | "
      "skills tok | other ctx tok | total tok | body KB |")
print("|---|---|---|---|---|---|---|---|---|---|")
for r in rows:
    h = HARNESS[r["label"][:2]]
    api = {"anthropic": "msgs", "chat": "chat", "responses": "resp"}[r["api"]]
    print(f"| {h} | {r['model']} | {cond(r['label'])} ({api}) | {r['system']['chars']} / {r['system']['tokens']} | "
          f"{r['tools']['n']} / {r['tools']['tokens']} | {r['instr']['tokens']} | {r['skills']['tokens']} | "
          f"{r['ctx']['tokens']} | **{r['total_tokens']}** | {r['body_bytes'] / 1000:.0f} |")
