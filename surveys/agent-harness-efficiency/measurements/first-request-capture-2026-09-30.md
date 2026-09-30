# First-request fixed context of five coding-agent harnesses (2026-09-30)

What each installed harness sends on the first turn of the one-word prompt
`hi`, measured on graehl's Linux host by pointing the harness at a local
capture stub instead of a model. No model was called for these numbers.
Measured by a delegated worker (Contributing-model: opus-5.5) for
[the survey](../survey.md#a-fixed-first-request-context).

## Method

- [`capture/stub.py`](capture/stub.py) implements just enough of Anthropic
  Messages, OpenAI Chat Completions and OpenAI Responses (streaming) to reply
  `OK` with no tool call, and saves each request body plus redacted headers.
- Each harness ran in an empty non-git directory under `env -i` (HOME, USER,
  PATH, TERM, LANG, SHELL plus the redirect variables), via
  [`capture/run.sh`](capture/run.sh) and the per-harness wrappers. Live
  configuration homes were never edited; "user config" rows use scratch
  copies of `~/.codex`, `~/.copilot` and `~/.pi/agent`.
- Redirects: Claude Code `ANTHROPIC_BASE_URL`; Codex `-c model_providers.stub.*`
  with `wire_api=responses`; pi a stub provider in a scratch
  `PI_CODING_AGENT_DIR`; OpenCode `OPENCODE_CONFIG`; Copilot CLI its
  documented custom-provider variables (`COPILOT_PROVIDER_BASE_URL`, see
  `copilot help providers`).
- [`capture/analyze.py`](capture/analyze.py) splits each request into harness
  system prompt, tool schemas (compact JSON as sent), user instruction files
  (`CLAUDE.md`/`AGENTS.md`/`copilot-instructions.md`), skills catalog, other
  injected context, and the prompt, and counts tiktoken `o200k_base` tokens.
  That is one common proxy tokenizer: exact for GPT-5-era OpenAI models,
  typically an undercount for Claude.
- The scripts carry this host's absolute paths; they are the record of what
  ran, not a reusable tool. The 69 captured request bodies stay on the
  measuring host (`.tracks/capture/runs/`, git-excluded) because they embed
  the user's private compiled boot policy.

Versions: Claude Code 2.1.285, Codex CLI 0.159.2, pi 0.85.1, OpenCode
1.18.31, Copilot CLI 1.0.85.

## Headline (o200k tokens, first request)

| harness | minimal mode | stock (no user config) | user config | what the user config adds |
|---|---|---|---|---|
| Claude Code | 806 (`--bare` = `CLAUDE_CODE_SIMPLE=1`) | 13.9k (Opus 5.5 or a non-Claude id); 24.5k (Haiku 4.5) | 29.3k (Sonnet 5.5); 37.7k (Haiku 4.5) | 15.6k instructions, 1.3k skills |
| Codex | n/a | 7.6k (gpt-5.5), 7.8k (gpt-5.3-codex), 9.2k (gpt-5.6-sol), 10.5k (gpt-6-astra) | 28.0k–30.8k | 15.6k AGENTS.md, 4.7k–5.3k skills |
| pi | 1.2k (empty agent dir and HOME) | 5.3k (real HOME adds a 4.0k skills catalog) | 21.0k | 15.6k AGENTS.md, 4.2k skills |
| OpenCode | n/a | 6.3k–7.1k | 28.9k–29.6k | 15.6k AGENTS.md, 7.1k skills |
| Copilot CLI | n/a | 10.5k–11.4k | 30.4k–31.3k | 15.6k instructions, 3.2k skills, 5 plugin tools |

The user's instruction file is the same compiled boot
(`~/agents/AGENTS.boot.md`, 70.7 kB) in every harness, about 15.6k tokens,
and it is 51–74% of each first request under the user config. Harness-owned
prompt plus tools is 1.2k (pi) to 14k (Claude Code), 24k on Claude Code's
Haiku path.

## Per-model variation

- **Claude Code** sends one prompt family to Sonnet 5.5, Opus 5.5 and a
  non-Claude id (`gpt-5.6-sol` through `ANTHROPIC_MODEL`): about 0.8k tokens
  of system text under the user config and 20–21 tools at 10.7k–11.1k
  tokens. For the foreign id only the identity line, commit-attribution line,
  one auto-mode paragraph and ±70 tokens of Bash description change; it
  also warns and assumes a 200k window. Haiku 4.5 gets an older prompt: 5.7k
  system tokens and 24–25 tools at 16.8k–17.2k, about 10.5k more.
- **Codex** chooses by model slug. gpt-5.5 and gpt-5.3-codex use the classic
  `instructions` field and 10–14 function tools (2.0k–3.7k tokens).
  gpt-5.6-sol and gpt-6-astra move the base prompt into a developer message
  and send tools as an `additional_tools` item: a JavaScript `exec` tool plus
  agent-collaboration tools (4.4k–4.9k), with multi-agent role/mode messages
  (0.7k–0.9k).
- **pi** sends byte-identical text to Claude and GPT (prompt 580 tokens bare,
  four tools about 0.6k). With `pi-lovely-codex` enabled in the scratch copy
  only GPT requests change: `read` becomes `apply_patch` plus `view_image`,
  +38 system and +5 tool tokens.
- **OpenCode** picks one prompt file by model family: Anthropic 1.7k tokens
  with `edit`/`write`; GPT-5.x a Codex-style 1.9k prompt with `apply_patch`
  replacing `edit`/`write`; GPT-4.1 a 2.4k prompt. It also makes a separate
  511-token title-generation call.
- **Copilot CLI** shares one opener with family-specific tail sections: GPT
  gets preamble, tool-use and editing-constraint sections (5.2k–5.5k tokens),
  Claude a progress-update section and an `edit` tool (4.6k–4.9k). Tools are
  17–18 stock (5.7k tokens), 22–23 with the user's plugins (6.9k).

## Server-side probe: blocked

A capped probe ([`capture/probe.py`](capture/probe.py), at most 7 calls, no
Sol or Luna) was meant to compare usage reported through `copilot-api` with
the local count of a minimal request, to bound any prompt GitHub's backend
adds. All 5 calls made returned HTTP 402 `quota_exceeded` ("You have exceeded
your monthly quota"), so it produced no numbers. Rerun it after the quota
resets.

## Defect found

With the real HOME, OpenCode 1.18.31 failed before sending any request: the
stray link `~/.opencode/agents -> ~/agents` made it parse Playwright
`*.agent.md` files under a `node_modules` tree as agent definitions. The
user-config OpenCode rows above used a scratch HOME without that link.
`scripts/build-boot link` now disables such links (commit `5d72237`).
