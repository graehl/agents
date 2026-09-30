"""Server-side injection probe against copilot-api (127.0.0.1:4141).

Real spend: at most 7 tiny calls. No gpt-5.6-sol / gpt-5.6-luna calls.
usage: uvx --with tiktoken python probe.py
Writes probe/*.json (request summary + full response/usage) and probe/summary.json.
"""

import copy
import json
import os
import time
import urllib.error
import urllib.request

import tiktoken

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "probe")
os.makedirs(OUT, exist_ok=True)
BASE = "http://127.0.0.1:4141"
ENC = tiktoken.get_encoding("o200k_base")
TEXT = "Reply with exactly OK"
FORBIDDEN = ("gpt-5.6-sol", "gpt-5.6-luna")
calls = [0]
MAX_CALLS = 7


def tok(s):
    return len(ENC.encode(s, disallowed_special=()))


def post(path, body, headers=None, local=False):
    if not local:
        assert body.get("model") not in FORBIDDEN
        calls[0] += 1
        assert calls[0] <= MAX_CALLS, "call budget exceeded"
    h = {"Content-Type": "application/json", "anthropic-version": "2023-06-01"}
    h.update(headers or {})
    req = urllib.request.Request(BASE + path, data=json.dumps(body).encode(), headers=h, method="POST")
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            raw = r.read().decode()
            code = r.status
    except urllib.error.HTTPError as e:
        raw = e.read().decode()
        code = e.code
    return code, raw, time.time() - t0


def sse_usage(raw):
    """Collect usage objects from an Anthropic SSE stream."""
    usage = {}
    text = ""
    for line in raw.splitlines():
        if not line.startswith("data:"):
            continue
        try:
            d = json.loads(line[5:].strip())
        except Exception:
            continue
        if d.get("type") == "message_start":
            usage.update(d["message"].get("usage") or {})
        elif d.get("type") == "message_delta":
            usage.update(d.get("usage") or {})
        elif d.get("type") == "content_block_delta":
            text += d.get("delta", {}).get("text", "")
    return usage, text


def record(name, path, body, code, raw, dt, extra=None):
    rec = {"name": name, "path": path, "model": body.get("model"), "status": code, "seconds": round(dt, 2),
           "request_bytes": len(json.dumps(body)), "extra": extra or {}}
    try:
        resp = json.loads(raw)
        rec["response"] = resp
        rec["usage"] = resp.get("usage")
    except Exception:
        u, text = sse_usage(raw)
        rec["usage"] = u
        rec["text"] = text
        rec["raw_tail"] = raw[-1500:]
    json.dump(rec, open(os.path.join(OUT, f"{name}.json"), "w"), indent=1)
    print(name, code, json.dumps(rec.get("usage")), flush=True)
    return rec


def main():
    summary = {"text": TEXT, "o200k_text_tokens": tok(TEXT)}
    anth_min = {"model": "claude-haiku-4.5", "max_tokens": 16,
                "messages": [{"role": "user", "content": TEXT}]}
    chat_min = {"model": "claude-haiku-4.5", "max_tokens": 16,
                "messages": [{"role": "user", "content": TEXT}]}
    mini_min = {"model": "gpt-5.4-mini", "max_tokens": 16,
                "messages": [{"role": "user", "content": TEXT}]}

    # free local estimates from copilot-api (/v1/messages/count_tokens is local)
    for nm, b in (("local-count-haiku-min", anth_min), ("local-count-mini-min", mini_min)):
        code, raw, dt = post("/v1/messages/count_tokens", b, local=True)
        summary[nm] = raw

    summary["anth_min"] = record("1-haiku-messages-min", "/v1/messages", anth_min,
                                 *post("/v1/messages", anth_min))["usage"]
    summary["chat_min"] = record("2-haiku-chat-min", "/v1/chat/completions", chat_min,
                                 *post("/v1/chat/completions", chat_min))["usage"]
    summary["mini_min"] = record("3-gpt-5.4-mini-messages-min", "/v1/messages", mini_min,
                                 *post("/v1/messages", mini_min))["usage"]

    # captured Claude Code request (empty config dir, model claude-haiku-4-5), sent verbatim
    cap_dir = os.path.join(ROOT, "runs", "cc-f-vanilla-haiku")
    cap = max((json.load(open(os.path.join(cap_dir, f))) for f in os.listdir(cap_dir) if "messages" in f),
              key=lambda r: r["body_bytes"])
    body = copy.deepcopy(cap["body"])
    body["model"] = "claude-haiku-4.5"  # Copilot's id for the same model; nothing else changed
    hdrs = {k: v for k, v in cap["headers"].items() if k.lower().startswith("anthropic-")}
    code, raw, dt = post("/v1/messages/count_tokens", body, hdrs, local=True)
    summary["local-count-cc"] = raw
    path = "/v1/messages?beta=true"
    r5 = record("5-cc-haiku-verbatim", path, body, *post(path, body, hdrs),
                extra={"anthropic_headers": hdrs})
    time.sleep(2)
    r6 = record("6-cc-haiku-verbatim-repeat", path, body, *post(path, body, hdrs),
                extra={"anthropic_headers": hdrs})
    summary["cc_first"] = r5["usage"]
    summary["cc_repeat"] = r6["usage"]
    summary["calls"] = calls[0]
    json.dump(summary, open(os.path.join(OUT, "summary.json"), "w"), indent=1)
    print(json.dumps(summary, indent=1)[:3000])


if __name__ == "__main__":
    main()
