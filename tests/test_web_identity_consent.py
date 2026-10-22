#!/usr/bin/env python3
"""Behavior tests for scripts/web-identity-consent."""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "web-identity-consent"


def run_check(config: Path, url: str, disclosure: str, action: str, *extra: str):
    proc = subprocess.run(
        [
            str(SCRIPT),
            url,
            "--disclosure",
            disclosure,
            "--action",
            action,
            "--config",
            str(config),
            "--json",
            *extra,
        ],
        capture_output=True,
        text=True,
        env={**os.environ, "ACLI_QUIET": "1"},
        check=False,
    )
    records = [json.loads(line) for line in proc.stdout.splitlines() if line]
    return proc.returncode, records, proc.stderr


def write_policy(root: Path, body: str) -> Path:
    config = root / "policy.toml"
    config.write_text(body, encoding="utf-8")
    return config


def test_missing_policy_asks_for_account_but_allows_anonymous():
    with tempfile.TemporaryDirectory() as raw_root:
        config = Path(raw_root) / "missing.toml"
        code, records, err = run_check(
            config, "https://example.com/data", "account", "read"
        )
        assert code == 3, err
        assert records[0]["decision"] == "ask"
        assert records[0]["config_present"] is False
        code, records, err = run_check(
            config, "https://example.com/data", "anonymous", "read"
        )
        assert code == 0, err
        assert records[0]["decision"] == "allow"


def test_anonymous_does_not_read_identity_policy():
    with tempfile.TemporaryDirectory() as raw_root:
        config = Path(raw_root) / "malformed.toml"
        config.write_text("not valid toml = [", encoding="utf-8")
        code, records, err = run_check(
            config, "https://example.com/data", "anonymous", "read"
        )
        assert code == 0, err
        assert records[0]["decision"] == "allow"


def test_exact_origin_account_allow_does_not_allow_contact_or_lookalike():
    with tempfile.TemporaryDirectory() as raw_root:
        config = write_policy(
            Path(raw_root),
            """version = 1
[[rule]]
origin = "https://github.com"
disclosures = ["account"]
actions = ["read", "write"]
decision = "allow"
reason = "Existing account."
""",
        )
        code, records, err = run_check(
            config, "https://github.com/settings", "account", "read"
        )
        assert code == 0, err
        assert records[0]["matched"]["reason"] == "Existing account."
        code, records, _ = run_check(
            config, "https://github.com/settings", "contact", "read"
        )
        assert code == 3
        assert records[0]["decision"] == "ask"
        code, records, _ = run_check(
            config, "https://github.com.evil.example/", "account", "read"
        )
        assert code == 3
        assert records[0]["decision"] == "ask"


def test_more_specific_path_decides_and_segment_matching_is_exact():
    with tempfile.TemporaryDirectory() as raw_root:
        config = write_policy(
            Path(raw_root),
            """version = 1
[[rule]]
origin = "https://example.com"
disclosures = ["account"]
actions = ["read"]
decision = "allow"
[[rule]]
origin = "https://example.com"
path_prefix = "/private/"
disclosures = ["account"]
actions = ["read"]
decision = "deny"
""",
        )
        code, records, _ = run_check(
            config, "https://example.com/private/report", "account", "read"
        )
        assert code == 4
        assert records[0]["decision"] == "deny"
        code, records, err = run_check(
            config, "https://example.com/privateer", "account", "read"
        )
        assert code == 0, err
        assert records[0]["decision"] == "allow"


def test_conflicting_equal_specificity_is_invalid_policy():
    with tempfile.TemporaryDirectory() as raw_root:
        config = write_policy(
            Path(raw_root),
            """version = 1
[[rule]]
origin = "https://example.com"
disclosures = ["account"]
actions = ["read"]
decision = "allow"
[[rule]]
origin = "https://example.com"
disclosures = ["account"]
actions = ["read"]
decision = "deny"
""",
        )
        code, records, err = run_check(
            config, "https://example.com/", "account", "read"
        )
        assert code == 2
        assert records == []
        assert (
            "conflicting decisions"
            in json.loads(err.splitlines()[-1])["error"]["message"]
        )


def test_url_userinfo_is_rejected():
    with tempfile.TemporaryDirectory() as raw_root:
        code, records, err = run_check(
            Path(raw_root) / "missing.toml",
            "https://person@example.com/",
            "anonymous",
            "read",
        )
        assert code == 2
        assert records == []
        assert "userinfo" in json.loads(err.splitlines()[-1])["error"]["message"]


if __name__ == "__main__":
    for name, function in list(globals().items()):
        if name.startswith("test_"):
            function()
            print(f"ok {name}")
