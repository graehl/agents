#!/usr/bin/env python3
"""Capture stub: minimal Anthropic Messages / OpenAI Chat / OpenAI Responses
server that always answers "OK" and records every request (redacted).

Captures go to <root>/runs/<label>/NNN-<method>-<path>.json where <label> is
read from <root>/LABEL at request time.
"""

import json
import sys
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 18765
REDACT = {"authorization", "x-api-key", "api-key", "cookie", "openai-api-key"}
_lock = threading.Lock()
_counter = [0]


def label():
    p = ROOT / "LABEL"
    return p.read_text().strip() if p.exists() else "unlabeled"


def save(handler, body_raw):
    with _lock:
        _counter[0] += 1
        n = _counter[0]
    d = ROOT / "runs" / label()
    d.mkdir(parents=True, exist_ok=True)
    headers = {}
    for k, v in handler.headers.items():
        headers[k] = "<redacted>" if k.lower() in REDACT else v
    try:
        body = json.loads(body_raw) if body_raw else None
    except Exception:
        body = {"_raw": body_raw.decode("utf-8", "replace")}
    safe = handler.path.split("?")[0].strip("/").replace("/", "_") or "root"
    rec = {
        "time": time.time(),
        "method": handler.command,
        "path": handler.path,
        "headers": headers,
        "body_bytes": len(body_raw or b""),
        "body": body,
    }
    (d / f"{n:03d}-{handler.command}-{safe}.json").write_text(
        json.dumps(rec, indent=1, ensure_ascii=False)
    )
    print(f"[stub] {label()} {n} {handler.command} {handler.path}", flush=True)
    return body


MODELS = [
    "claude-opus-5-5",
    "claude-sonnet-4-5",
    "claude-haiku-4-5",
    "gpt-5.5",
    "gpt-5.6-sol",
    "gpt-6-astra",
    "gpt-5.3-codex",
    "gpt-5.4-mini",
]


class H(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *a):
        pass

    def _read(self):
        n = int(self.headers.get("Content-Length") or 0)
        if n:
            return self.rfile.read(n)
        if self.headers.get("Transfer-Encoding", "").lower() == "chunked":
            buf = b""
            while True:
                size = int(self.rfile.readline().strip() or b"0", 16)
                if size == 0:
                    self.rfile.readline()
                    break
                buf += self.rfile.read(size)
                self.rfile.readline()
            return buf
        return b""

    def _json(self, obj, code=200):
        data = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _sse_start(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "close")
        self.end_headers()
        self.close_connection = True

    def _ev(self, event, data):
        s = ""
        if event:
            s += f"event: {event}\n"
        s += f"data: {json.dumps(data) if not isinstance(data, str) else data}\n\n"
        self.wfile.write(s.encode())
        self.wfile.flush()

    def do_GET(self):
        save(self, b"")
        p = self.path.split("?")[0]
        if p.endswith("/models"):
            return self._json(
                {
                    "object": "list",
                    "data": [
                        {"id": m, "object": "model", "type": "model",
                         "display_name": m, "created": 0, "owned_by": "stub"}
                        for m in MODELS
                    ],
                    "models": [{"slug": m} for m in MODELS],
                    "has_more": False,
                }
            )
        return self._json({})

    def do_HEAD(self):
        save(self, b"")
        self.send_response(200)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_POST(self):
        raw = self._read()
        body = save(self, raw) or {}
        p = self.path.split("?")[0]
        model = body.get("model", "stub") if isinstance(body, dict) else "stub"
        stream = bool(body.get("stream")) if isinstance(body, dict) else False
        if p.endswith("/messages/count_tokens"):
            return self._json({"input_tokens": 1})
        if p.endswith("/messages"):
            return self.anthropic(model, stream)
        if p.endswith("/chat/completions"):
            return self.chat(model, stream)
        if p.endswith("/responses"):
            return self.responses_api(model, stream)
        return self._json({})

    def anthropic(self, model, stream):
        mid = "msg_" + uuid.uuid4().hex[:20]
        usage = {"input_tokens": 1, "output_tokens": 1,
                 "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0}
        if not stream:
            return self._json({
                "id": mid, "type": "message", "role": "assistant", "model": model,
                "content": [{"type": "text", "text": "OK"}],
                "stop_reason": "end_turn", "stop_sequence": None, "usage": usage})
        self._sse_start()
        self._ev("message_start", {"type": "message_start", "message": {
            "id": mid, "type": "message", "role": "assistant", "model": model,
            "content": [], "stop_reason": None, "stop_sequence": None,
            "usage": usage}})
        self._ev("content_block_start", {"type": "content_block_start", "index": 0,
                                         "content_block": {"type": "text", "text": ""}})
        self._ev("content_block_delta", {"type": "content_block_delta", "index": 0,
                                         "delta": {"type": "text_delta", "text": "OK"}})
        self._ev("content_block_stop", {"type": "content_block_stop", "index": 0})
        self._ev("message_delta", {"type": "message_delta",
                                   "delta": {"stop_reason": "end_turn", "stop_sequence": None},
                                   "usage": {"output_tokens": 1}})
        self._ev("message_stop", {"type": "message_stop"})

    def chat(self, model, stream):
        cid = "chatcmpl-" + uuid.uuid4().hex[:20]
        usage = {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2}
        if not stream:
            return self._json({
                "id": cid, "object": "chat.completion", "created": int(time.time()),
                "model": model, "choices": [{"index": 0, "finish_reason": "stop",
                "message": {"role": "assistant", "content": "OK"}}], "usage": usage})
        self._sse_start()
        base = {"id": cid, "object": "chat.completion.chunk",
                "created": int(time.time()), "model": model}
        self._ev(None, {**base, "choices": [{"index": 0, "delta": {"role": "assistant", "content": ""}, "finish_reason": None}]})
        self._ev(None, {**base, "choices": [{"index": 0, "delta": {"content": "OK"}, "finish_reason": None}]})
        self._ev(None, {**base, "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}]})
        self._ev(None, {**base, "choices": [], "usage": usage})
        self._ev(None, "[DONE]")

    def responses_api(self, model, stream):
        rid = "resp_" + uuid.uuid4().hex[:20]
        iid = "msg_" + uuid.uuid4().hex[:20]
        part = {"type": "output_text", "text": "OK", "annotations": []}
        item = {"id": iid, "type": "message", "status": "completed",
                "role": "assistant", "content": [part]}
        usage = {"input_tokens": 1, "input_tokens_details": {"cached_tokens": 0},
                 "output_tokens": 1, "output_tokens_details": {"reasoning_tokens": 0},
                 "total_tokens": 2}
        resp = {"id": rid, "object": "response", "created_at": int(time.time()),
                "status": "completed", "model": model, "output": [item], "usage": usage}
        if not stream:
            return self._json(resp)
        self._sse_start()
        seq = [0]

        def ev(t, d):
            d = {"type": t, "sequence_number": seq[0], **d}
            seq[0] += 1
            self._ev(t, d)

        ev("response.created", {"response": {**resp, "status": "in_progress", "output": [], "usage": None}})
        ev("response.in_progress", {"response": {**resp, "status": "in_progress", "output": [], "usage": None}})
        ev("response.output_item.added", {"output_index": 0, "item": {**item, "status": "in_progress", "content": []}})
        ev("response.content_part.added", {"item_id": iid, "output_index": 0, "content_index": 0,
                                           "part": {"type": "output_text", "text": "", "annotations": []}})
        ev("response.output_text.delta", {"item_id": iid, "output_index": 0, "content_index": 0, "delta": "OK"})
        ev("response.output_text.done", {"item_id": iid, "output_index": 0, "content_index": 0, "text": "OK"})
        ev("response.content_part.done", {"item_id": iid, "output_index": 0, "content_index": 0, "part": part})
        ev("response.output_item.done", {"output_index": 0, "item": item})
        ev("response.completed", {"response": resp})


if __name__ == "__main__":
    print(f"[stub] listening 127.0.0.1:{PORT}", flush=True)
    ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
