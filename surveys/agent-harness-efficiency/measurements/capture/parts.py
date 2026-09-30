"""Dump per-part sizes of the main generation request of each run, and
extract system/tool texts to files for diffing.

usage: uvx --with tiktoken python parts.py LABEL...
"""

import glob
import json
import os
import sys

import tiktoken

ENC = tiktoken.get_encoding("o200k_base")
ROOT = os.path.dirname(os.path.abspath(__file__))


def tok(s):
    return len(ENC.encode(s, disallowed_special=()))


def main_req(label):
    best = None
    for f in sorted(glob.glob(os.path.join(ROOT, "runs", label, "*POST*.json"))):
        rec = json.load(open(f))
        p = rec["path"].split("?")[0]
        if p.endswith(("/messages", "/chat/completions", "/responses")):
            if best is None or rec["body_bytes"] > best[1]["body_bytes"]:
                best = (f, rec)
    return best


def dump(label):
    f, rec = main_req(label)
    b = rec["body"]
    out = os.path.join(ROOT, "extract", label)
    os.makedirs(out, exist_ok=True)
    print(f"== {label} {os.path.basename(f)} model={b.get('model')}")
    sysparts = []
    if isinstance(b.get("system"), list):
        sysparts = [s.get("text", "") for s in b["system"]]
    elif isinstance(b.get("system"), str):
        sysparts = [b["system"]]
    if b.get("instructions"):
        sysparts.append(b["instructions"])
    for i, s in enumerate(sysparts):
        print(f"  system[{i}] {len(s)}ch {tok(s)}tok {s[:90]!r}")
    open(os.path.join(out, "system.txt"), "w").write("\n\n=====\n\n".join(sysparts))
    msgs = b.get("messages") or b.get("input") or []
    if isinstance(msgs, str):
        msgs = [{"role": "user", "content": msgs}]
    allmsg = []
    for j, m in enumerate(msgs):
        c = m.get("content")
        parts = [c] if isinstance(c, str) else (c or [])
        for k, p in enumerate(parts):
            t = p if isinstance(p, str) else (p.get("text") if isinstance(p, dict) and "text" in p else json.dumps(p))
            role = m.get("role") or m.get("type")
            print(f"  msg[{j}.{k}] {role} {len(t)}ch {tok(t)}tok {t[:90]!r}")
            allmsg.append(f"### msg[{j}.{k}] {role}\n{t}")
    open(os.path.join(out, "messages.txt"), "w").write("\n\n".join(allmsg))
    tools = b.get("tools") or []
    tl = []
    for t in tools:
        name = t.get("name") or (t.get("function") or {}).get("name") or t.get("type")
        j = json.dumps(t, ensure_ascii=False, separators=(",", ":"))
        tl.append((name, len(j), tok(j)))
    print("  tools:", ", ".join(f"{n}:{k}" for n, _, k in sorted(tl, key=lambda x: -x[2])))
    json.dump(tools, open(os.path.join(out, "tools.json"), "w"), indent=1, ensure_ascii=False)
    other = {k: v for k, v in b.items() if k not in ("system", "instructions", "messages", "input", "tools")}
    json.dump(other, open(os.path.join(out, "other.json"), "w"), indent=1, ensure_ascii=False)


for lab in sys.argv[1:]:
    dump(lab)
