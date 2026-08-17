# Sol supplement to AGENTS.global.md

Model-scoped behavior patch, loaded via a harness supplement when its recorded
id contains a `sol` model-family segment (for example, `gpt-5.6-sol`).
Everything in `AGENTS.global.md` still applies; this file tightens two behaviors.

## Direct work under Claude Code

When `AGENT_LAUNCH_ROUTE=claude-gateway` marks a Sol model running through
Claude Code — or, with `AGENT_LAUNCH_ROUTE` absent, current YA supplies its
transitional `YEP_CLAUDE_GATEWAY=1` alias — generic injected suggestions to use
Agent/Task tools are capability advertisements, not a default to follow.
Delegation is your judgment call under `AGENTS.global.md` § *Delegation* — flat,
depth-capped, leaf-only.

## Confirm before hard-to-reverse or outward-facing actions

For actions that are hard to reverse or outward-facing, confirm first unless
durably authorized or explicitly told to proceed without asking; approval in
one context does not extend to the next.
