"""Task-owned subscription credentials, configuration and subprocess environment."""

from __future__ import annotations

import json
import os
from pathlib import Path

CONFIG = """approval_policy = "never"
sandbox_mode = "read-only"
model_provider = "openai"
project_doc_max_bytes = 0

[features]
apps = false
memories = false
multi_agent = false
plugins = false
remote_plugin = false
skill_search = false
shell_tool = false
unified_exec = false
computer_use = false
browser_use = false
web_search = false
code_mode = false
code_mode_host = false
code_mode_only = false
code_mode_prewarm = false

[memories]
generate_memories = false
use_memories = false
disable_on_external_context = true

[skills]
include_instructions = false
[skills.bundled]
enabled = false
[agents]
enabled = false
[mcp_servers]
"""


def prepare_profile(auth_home: Path, output: Path, *, resume: bool) -> dict[str, str]:
    auth = (auth_home / "auth.json").read_bytes()
    parsed = json.loads(auth)
    if (
        not isinstance(parsed.get("tokens"), dict)
        or not parsed["tokens"].get("access_token")
        or parsed.get("OPENAI_API_KEY")
    ):
        raise ValueError(
            "auth-home must contain a ChatGPT subscription login; API keys require --backend openai-chat-completions"
        )
    profile, ordinary_home, work = output / ".codex", output / ".home", output / "work"
    if resume:
        if (profile / "config.toml").read_text() != CONFIG:
            raise ValueError(
                "managed Codex configuration changed; do not reuse this campaign"
            )
        # The stored login may have refreshed since campaign creation.
        stored = json.loads((profile / "auth.json").read_bytes())
        if not isinstance(stored.get("tokens"), dict) or stored.get("OPENAI_API_KEY"):
            raise ValueError("campaign no longer has a subscription login")
    else:
        for path in (profile, ordinary_home, work):
            path.mkdir(mode=0o700)
        with (profile / "auth.json").open("xb") as stream:
            os.chmod(stream.name, 0o600)
            stream.write(auth)
        (profile / "config.toml").write_text(CONFIG)
    passthrough = (
        "PATH",
        "LANG",
        "LC_ALL",
        "SSL_CERT_FILE",
        "SSL_CERT_DIR",
        "HTTP_PROXY",
        "HTTPS_PROXY",
        "ALL_PROXY",
        "NO_PROXY",
        "http_proxy",
        "https_proxy",
        "all_proxy",
        "no_proxy",
    )
    env = {key: os.environ[key] for key in passthrough if key in os.environ}
    env.update(
        HOME=str(ordinary_home),
        CODEX_HOME=str(profile),
        XDG_CONFIG_HOME=str(ordinary_home),
        XDG_CACHE_HOME=str(ordinary_home / ".cache"),
    )
    return env
