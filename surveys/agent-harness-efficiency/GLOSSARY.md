# Glossary: agent harness efficiency

Survey-scoped vocabulary for `surveys/agent-harness-efficiency/`.

| term | meaning here |
|---|---|
| harness | Everything around a model in a coding agent: system prompt, tool schemas, injected instruction files and skills catalogs, control loop, context management, and delegation. |
| native harness | The model vendor's own CLI: Claude Code (Anthropic), Codex (OpenAI), Gemini CLI (Google), Grok Build (xAI). |
| neutral harness | A deliberately minimal harness used as a control; mainly Terminus 2 (Terminal-Bench's tmux/bash-only harness) and mini-SWE-agent. pi is minimal but not a benchmark control. |
| foreign harness | A harness running a model it was not built or trained around, e.g. Claude Code driving a GPT or open-weight model. |
| transport | The route between harness and model: vendor API, subscription backend (ChatGPT login, GitHub Copilot), or a translating proxy such as `copilot-api`. |
| fixed first-request context | Tokens a harness sends on the first turn before any work: system prompt, tool schemas, instruction files, skills, environment blocks. Measured here with o200k as a common proxy tokenizer. |
| double injection | Two instruction layers stacked because a proxy or backend adds its own prompt on top of the harness's. Not observed for `copilot-api`. |
| cost per solved task | Billed dollars divided by solved tasks. The comparison metric that matters, because token volume and billed cost diverge under prompt caching. |
| context pressure | The attention and long-context cost of prefix tokens, which caching does not reduce; distinct from their billed cost. |
