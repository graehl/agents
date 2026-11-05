import json
import os
import subprocess
import sys
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

CLI = Path(__file__).resolve().parents[1] / "scripts" / "ya-session"


class SessionLookupTest(unittest.TestCase):
    def test_http_lookup_viewer_alias_formats_errors_and_redirects(self):
        paths = []
        result = {
            "sessionId": "ya-id",
            "provider": "codex",
            "projectId": "project",
            "native": {
                "family": "codex",
                "storageScope": "/rollouts",
                "id": "native-id",
            },
            "transcriptPath": "/rollouts/rollout-native-id.jsonl",
            "status": "available",
        }

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                paths.append(self.path)
                if "redirect" in self.path:
                    self.send_response(302)
                    self.send_header("Location", "/must-not-follow")
                    self.end_headers()
                    return
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps(result).encode())

            def log_message(self, *_args):
                pass

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        base = f"http://127.0.0.1:{server.server_port}"
        env = {**os.environ, "AGENT_SERVER_URL": base}

        def run(*args):
            return subprocess.run(
                [sys.executable, str(CLI), *args],
                env=env,
                text=True,
                capture_output=True,
                timeout=20,
            )

        try:
            url = f"{base}/projects/project/sessions/native-id?yaSessionId=ya-id"
            for flag in ("--json", "--pretty"):
                response = run(url, flag)
                self.assertEqual(response.returncode, 0, response.stderr)
                self.assertEqual(json.loads(response.stdout), result)
                self.assertEqual(paths[-1], "/api/sessions/ya-id/native-source")
            response = run("ya-id", "--text")
            self.assertEqual(response.returncode, 0, response.stderr)
            self.assertIn(
                "Transcript: /rollouts/rollout-native-id.jsonl", response.stdout
            )
            result.update(native=None, transcriptPath=None, status="unbound")
            self.assertEqual(json.loads(run("ya-id").stdout)["status"], "unbound")
            result["status"] = "available"
            response = run("ya-id")
            self.assertEqual(response.returncode, 70)
            self.assertFalse(json.loads(response.stderr.splitlines()[-1])["ok"])
            response = run("redirect")
            self.assertEqual(response.returncode, 3)
            self.assertNotIn("/must-not-follow", paths)
            before = len(paths)
            self.assertEqual(run("--help").returncode, 0)
            self.assertEqual(run("ya-id", "--unknown").returncode, 2)
            self.assertEqual(run("bad/id").returncode, 2)
            self.assertEqual(run("http://[bad/sessions/ya-id").returncode, 2)
            self.assertEqual(
                run("ya-id", "--server", "http://localhost:bad").returncode, 2
            )
            completed = run("--acli-complete", "--ser")
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn("--server", completed.stdout)
            self.assertEqual(len(paths), before)
        finally:
            server.shutdown()
            worker.join()
            server.server_close()


if __name__ == "__main__":
    unittest.main()
