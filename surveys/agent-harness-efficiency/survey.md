# Field map: agent harness efficiency — fixed context, native vs foreign harness, proxies, and success per token

Mode: **grounded** (2026-09-30). Four retrieval tracks ran as delegated leaf
workers on one day: academic snowballing (Semantic Scholar forward citations
of SWE-agent, AI Agents That Matter, OpenHands, RAG-MCP and Lost in the
Middle, plus about 40 arXiv keyword queries); vendor documentation and harness
source; leaderboard data where the model is fixed and the harness varies;
and a local zero-cost capture of what each installed harness sends
([measurement record](measurements/first-request-capture-2026-09-30.md)).
Workers read abstracts plus the results sections cited below; entries read
only at abstract depth are marked in `related-work/papers.yaml`. The
synthesis here has not independently re-read those sources. Counts from
`related-work status`, 2026-09-30:
- 76 sources manifested, 54 verified by a read, 24 with committed full-text
  extracts.
- 14 fetches failed the engine's HTML fidelity checks and await a PDF pass.
- No concept digests yet.

Grades follow `field-map.md`; most rest on one paper or one operator.

Coverage cutoff: literature and leaderboards retrieved 2026-09-30. Saturation
was reached for controlled same-model harness contrasts, not for the wider
2026 "harness" literature, which grows by several papers a day. Not
forward-snowballed yet: Terminal-Bench (arXiv 2601.11868), HAL (2510.11977),
Complexity Trap (2508.21433), AGENTS.md evaluation (2602.11988); the Agentless
citer fetch failed on rate limits.

Placement: sibling of
[`agent-prompting-orchestration`](../agent-prompting-orchestration/survey.md),
which owns harness-induced divergence (§A3), static audits of agent-CLI
system prompts (§I) and harness self-evolution (§J). This map owns the cost
side: how much fixed context a harness adds, whether the native harness
wins with the model held fixed, and what proxies and transports change.

## Map orientation

Four axes:

- **harness** — the vendor's native CLI (Claude Code, Codex, Gemini CLI,
  Grok Build); a neutral minimal harness (Terminus 2, mini-SWE-agent,
  pi); a third-party product harness (Copilot, OpenCode, Droid, Cursor);
- **model family** — Anthropic, OpenAI, Google, xAI, open-weight;
- **transport** — vendor API direct; a subscription backend (Codex's ChatGPT
  login, GitHub Copilot's backend); a translating proxy such as `copilot-api`;
- **metric** — fixed first-request context; task success; tokens and billed
  dollars per solved task; wall time.

Three quantities are routinely conflated and must stay separate: **token
volume** (what a harness sends), **billed cost** (dominated by cache-read
pricing when the prefix is byte-stable), and **context pressure** (what the
model must attend over, which caching does not reduce).

## Readout for the motivating questions

- **Extra context of a Copilot harness versus native.** Measured on this host
  (o200k tokens, stock configuration): Copilot CLI 10.5k–11.4k versus Claude
  Code 13.9k for Claude and Codex 7.6k–10.5k for GPT. So Copilot CLI is
  lighter than Claude Code and 1k–4k heavier than Codex. Under the user's
  configuration all five harnesses land at 21k–31k, and the user's own 15.6k
  instruction file is most of it. VS Code agent mode and Grok's native
  harness were not measured. §A.
- **Performance per token.** No benchmark on current models puts one model
  in Copilot and in its native CLI. The indirect evidence is vendor-specific:
  Codex beats neutral harnesses for GPT models by 5–22 points on
  Terminal-Bench. Claude Code's edge over them is small and has flipped
  sign between benchmark versions. Gemini CLI never beats them. The one old
  Copilot data point (Claude 3.7 Sonnet, March 2025) is within noise of
  Claude Code. Native harnesses spend 2.3–8× the tokens of a minimal harness
  but only 1.0–1.3× the dollars, because they cache well; Codex with
  GPT-5.5 is the exception at 4.2×. §B, §C.
- **Delegation patterns.** Claude Code and both Copilot surfaces may spawn
  subagents on their own. Codex spawns only on request, except at Astra's
  `ultra` effort. pi has no subagents. No study measures subagent token
  overhead for coding against a single-agent control. §F.
- **Proxies.** `copilot-api` adds no system prompt, so there is no double
  instruction injection. Any server-side Copilot prompt is bounded at about
  800 tokens by one local observation. The real losses are at the
  transport. Upstream v0.7.0 drops Claude Code's thinking settings and every
  prompt-cache marker; the local fork passes Anthropic requests through
  intact. A native harness routed through the proxy keeps its native prompt
  and tools, which is the part of the gap that matters. Claude Code driving a
  GPT model instead does not adapt its prompt or tools, which is the
  foreign-harness case. §E, §D4.
- **pi versus Codex for Sol/Astra.** pi sends about 1.2k tokens of harness
  context against Codex's 9.2k (Sol) and 10.5k (Astra). For those models Codex
  also switches to a JavaScript `exec` tool plus collaboration tools, which
  pi does not reproduce; pi-lovely-codex only swaps in `apply_patch` (+43
  tokens). The only same-model pi-versus-Codex result uses GPT-5 on a
  pentest benchmark: Codex 70/104, pi 58/104 (p=0.023), at 2.3× Codex's cost
  per solved challenge. No Sol or Astra comparison exists. §D, frontier.

## A. Fixed first-request context

**A1 Local capture.** One-word prompt, five harnesses, o200k counts
([record](measurements/first-request-capture-2026-09-30.md)).
Harness-owned prompt plus tool schemas, stock:
- pi: 1.2k.
- OpenCode: 6.3k–7.1k.
- Codex: 7.6k (gpt-5.5) to 10.5k (gpt-6-astra).
- Copilot CLI: 10.5k–11.4k.
- Claude Code: 13.9k, or 24.5k on the Haiku 4.5 path.

`claude --bare` is 806. The user's compiled boot adds 15.6k in every harness;
skills catalogs add 1.3k–7.1k. Grade: single-source (one host, one version
each), exact for what was sent.

**A2 Literature and practitioner sizes.** Claude Code tool schemas:
~29K tokens a turn without MCP and 44K–65K with it (`chen2026compressiongateway`,
gateway vendor, version unpinned); XDA measured 51.4k before the first prompt
(system 10.7k, tools 28.5k, skills 6.3k) (`xda2026claudecode51k`). Systima's
open rig: Claude Code 32.8k versus OpenCode 6.9k first turn on Sonnet 4.5
(`systima2026ccopencode`). Production Copilot traffic: system prompt 14% of
input tokens, history 48%, tool calls and results 28%, median prompt 68K of
which 63K cached (`liu2026copilottraces`). Qwen Code's step-1 payload grew 8%
over 35 releases while total tokens nearly doubled with no resolve-rate gain
(`bensghaier2026harnessevolution`). Grades: single-source each, except the
Copilot telemetry (production-scale, one operator).

*Contested:* the local capture puts Claude Code's 20–21 tools at about 11k
o200k tokens, well below the 28K–29K reported elsewhere. Candidate causes are
the Claude tokenizer (larger counts than o200k), deferred tool loading in
2.1.x (`barbaste2026harnessengineering` §8.3), and plugins or MCP servers
present in the other setups. Not resolved.

**A3 Per-model variation.** Each harness except pi changes what it sends
by model id:

- **Codex** keeps a per-slug instruction template in a model catalog bundled
  in the binary, including tool shapes (`apply_patch_tool_type`,
  `tool_mode: code_mode_only`) (`openaicodexrepo`).
- **Copilot CLI** shares one opener and appends family-specific sections.
- **OpenCode** selects one prompt file by model-id substring and swaps
  `apply_patch` in for `edit`/`write` on GPT ids (`opencoderepoprompts`).
- **VS Code's Copilot agent** keeps a per-family prompt registry
  (`vscodecopilotagentprompts`).
- **Claude Code** gates a lean versus full prompt by model. The capture
  shows the same prompt for Opus 5.5, Sonnet 5.5 and a non-Claude id; Haiku
  4.5 gets a legacy prompt about 10.5k tokens larger.
- **pi** has no per-model branch; variation comes only from extensions.

Grade: reproduced from source and binary, plus the local capture.

**A4 User instruction files.** On this host the user's boot file is 51–74%
of every first request. Evidence on whether such files pay:
- LLM-generated AGENTS.md files cost 20–23% more with no significant success
  change, and developer-written ones gave +2.4% (not significant)
  (`gloaguen2026agentsmd`).
- A 124-PR study found −28.6% runtime and −16.6% output tokens
  (`lulla2026agentsmdefficiency`).
- A two-agent ablation found no correctness effect (`khatri2026contextfiles`).

These are repository context files, not a global behavioral policy like this
host's; no study measures the latter. Design consequence: instruction-file
size, not harness choice, is the lever this user controls most directly (see
frontier).

## B. Same model, different harness: success

**B1 Terminal-Bench, runs by the benchmark team** (`tbenchleaderboard`,
`tbench21news`, `merrill2026terminalbench`). Each figure is the native harness
minus Terminus 2, the team's bash-only harness, in percentage points:
- **OpenAI (Codex).** GPT-5 +14.4, GPT-5.2 +8.9, GPT-5-mini +7.8 on 2.0;
  GPT-5.4 +21/+22.5 and GPT-5.4-mini +20/+29 across 2.0 and 2.1; GPT-5.5
  +5.2 on 2.1. GPT-5-Codex is the one tie (+0.9).
- **Anthropic (Claude Code).** −5.6 (Opus 4.5) and −4.9 (Opus 4.6) on 2.0.
  On 2.1 Opus 4.6 is +6.3 and Sonnet 4.6 +7.0.
- **Google (Gemini CLI).** Every pair is a tie or a loss, including −13.1
  (Gemini 2.5 Pro) and −8.1 (Gemini 3 Pro, 2.1).

Combined 95% CI about ±4. Grade: externally-evaluated; the Claude Code
2.0 deficit is contested (B-contested below).

**B2 Other controlled contrasts.**
- **Harbor-Index** (82 hard tasks) (`shi2026harbor`): all three native
  harnesses beat Terminus 2 — GPT-5.5 28.0 vs 19.5, Opus 4.8 20.7 vs 15.9,
  Gemini 3.1 Pro 13.4 vs 11.0. Across 54 benchmarks the model effect was 5.2×
  the harness effect.
- **Contamination-controlled private suite** (80 tasks)
  (`arjmandi2026harnessormodel`): no average native premium — Opus 4.8 −1.25
  pp (CI −10.0 to +7.5) and GPT-5.5 +1.25 pp against a LangGraph harness. There
  is a post-hoc repo-versus-contest interaction for Opus.
- **HAL CORE-Bench Hard** (`halleaderboard`): Claude Code beat the CORE-Agent
  scaffold for Opus 4.5 (77.8 vs 42.2) at half the cost, and lost for Opus
  4.1 (42.2 vs 51.1, n=45, not significant).

Grades: benchmark-reported, single-source, and externally-evaluated
respectively.

**B3 Foreign-harness cases.**
- **Open models in Claude Code:** they cost 4–6× more per run than in
  Terminus 2 at equal or lower pass rate, e.g. GLM 5.2 8.5% at $205 vs 9.8% at
  $52 (`shi2026harbor`).
- **GPT-5 across open harnesses, pentest challenges:** Codex 70, pi 58,
  OpenCode 57 of 104 (`dhakal2026baselines`).
- **Claude 3.7 Sonnet in several products** (n=53) (`liveswebench2025`):
  Copilot agent mode 43.4, Claude Code 37.7, within noise.

Grades: benchmark-reported, externally-evaluated (off-domain), and
externally-evaluated (stale) respectively.

**B4 Self-submitted third-party harnesses** (Droid, Meta-Harness,
TongAgents and others) beat the native harness by 2–3 points for OpenAI and
11–19 for Anthropic and Google on Terminal-Bench 2.0. Grade:
benchmark-reported, unverified.

**B5 How much the harness matters depends on the regime.**
- **Model outweighs harness** across broad pools: Harbor 5.2×; Terminal-Bench
  authors, "model selection is usually more important".
- **Harness outweighs model** when the models are close in capability: 7.8×
  (`zhang2026stopcomparing`).
- **Small models are dominated by the harness:** evaluation harness 4.3× on
  Qwen3-8B (`le2026multiharnessrl`).
- **Stronger models vary less across harnesses** (`yao2026harnessbench`,
  `hu2026beyondmodel`).

A single "harness matters X%" headline is regime-specific.

## C. Tokens and dollars per solved task

Terminal-Bench 2.1 operator-run pairs: native harnesses use 2.3–8.0× more
tokens per trial than Terminus 2, but cost only 1.03–1.26× more. They finish
trials faster. The exception is Codex with GPT-5.5: 4.2× the cost ($5.57 vs
$1.42 per solve). Part of that may be accounting, since the Terminus 2 row
reports zero cached tokens (`tbenchleaderboard`). Grade: benchmark-reported.

Harness choice moves cost more than success:
- Three open harnesses on the same model were 0–8 points apart but 23–41×
  apart in tokens per solved task (`vats2026scaffoldeffect`).
- Two agents on the same model differed more than 20× in cost at list prices,
  mostly through prompt-cache behavior (`arino2026identicalruns`).

Caching dominates the bill:
- Caching cuts agent cost 78–89% for GPT-5.2 and Sonnet 4.5 at 10K–50K
  prefixes (`lumer2026promptcaching`).
- In Claude Code, cache creation plus reads are about 87% of reconstructed
  cost. There, the most aggressive tool-output compression cut tokens 38.4%
  but raised billed cost 6.8% (`weinberger2026tokenreduction`).
- A model switch drops Copilot's prefix-cache hit rate to about 8%, and
  compaction resets it similarly (`liu2026copilottraces`).

Design consequence: a byte-stable fixed prefix is billed near cache-read
rates, so its dollar cost is small. Its context-pressure cost is not (§H).

## D. Model–harness co-adaptation

**D1 Causal evidence, small models only.**
- An agent trained under one harness's tool protocol returned "Invalid tool
  format" on 75–81% of calls after a protocol change, falling below the
  untrained base model (`kim2026harnesspostraining`).
- A search agent parallelizes on 91% of turns in its training harness, 45%
  elsewhere, 2% where not asked (`zhang2026chart`).
- Nemotron-3 30B emits tool calls the harness doesn't offer in 66% of
  bash-only runs (`fan2026harnessdesign`).
- Multi-harness RL learns harness identity rather than portable skill
  (`le2026multiharnessrl`); native-harness RL moves one base model 6.8
  points apart across harnesses before training (`du2026legorl`).

Grade: benchmark-reported. No study tests the mechanism on a vendor
frontier model.

**D2 Vendor and practitioner claims.**
- **OpenAI** on `apply_patch`: "the model has been trained to excel at this
  diff format" (`openaicodexpromptingguide`). Separately, the named tool cut
  apply_patch failures 35%, method unpublished (`openaigpt51promptingguide`).
- **Warp** renamed tools to the names Codex was trained on
  (`warp2025codex`).
- **Anthropic:** no primary statement found that Claude is post-trained on
  Claude Code's tool shapes.
- **Ronacher** hypothesizes that Claude Code's tolerant tool parsing lets
  newer Claude models drift from other harnesses' schemas, with anecdotal
  failure rates in pi (`ronacher2026bettermodels`).

Grades: vendor claim, single-source, and anecdote.

**D3 Edit-format fit is model-specific.**
- Aider's edit format alone moves pass rate 2–11 points (`aiderleaderboard`).
- A hashline edit format raised 15 models by 15 points on average, and
  `apply_patch` failed for non-OpenAI models (Grok 4 50.7% patch failure)
  (`boluk2026harness`).
- Conventional diffs are unnatural for LLMs; block-level diffs match full
  rewrite at lower cost (`cheng2026todiff`).

Grades: benchmark-reported.

**D4 Harness-side accommodation.**
- **Accommodate per model family:** Codex, Copilot, OpenCode and VS Code, as
  in §A3, e.g. OpenCode's `apply_patch` for GPT, SEARCH/REPLACE for others
  (`barbaste2026harnessengineering` Table 7).
- **Do not:** Claude Code (a GPT id gets the Claude prompt and `Edit` tool)
  and pi core.
- **pi extensions:** `pi-lovely-codex` adds `apply_patch` through Codex's own
  binary and removes `read` for GPT ids, with no measurement published
  (`pilovelycodex`). It is disabled on this host. `pi-deepseek-anchor`
  serves DeepSeek a vendor-minimal toolset on request 1 only
  (`pideepseekanchor`).

## E. Transport: proxies and the Copilot backend

**E1 `copilot-api`** (`copilotapi`), upstream v0.7.0:
- Joins Anthropic system blocks into one OpenAI system message and adds
  nothing.
- Drops `thinking`, `top_k` and every `cache_control`, and replays earlier
  thinking blocks as visible assistant text.
- Impersonates VS Code Copilot Chat headers; `X-Initiator` affects billing
  only.
- Pads `count_tokens` for Claude (+346 tokens ×1.15), which shifts Claude
  Code's compaction point, not the request.
- Serves no `/v1/responses`, so Codex cannot use it directly.

The local fork (`~/copilot-api`, `d3aed98`):
- Forwards Anthropic requests unchanged apart from stamping a cache TTL.
- Sends GPT models through Copilot's Responses endpoint with cache markers
  deliberately dropped and reasoning round-tripped.
- Drops old thinking instead of replaying it.

Grade: reproduced from source.

**E2 Double injection.** Not observed. The proxy adds nothing, and any
Copilot server-side prompt is at most about 800 tokens: a `claude --bare`
call to gpt-5.6-luna through the fork reported 829 input tokens in total. A
VS Code issue states Copilot builds prompts client-side
(`vscodeissue254959`). The measurement meant to tighten this bound was
blocked by an exhausted Copilot quota. Grade: single-source bound.

**E3 Lost caching.** Stripped cache markers on OpenAI-compatible
translation paths are a documented cost problem: uncached agent sessions
"can be 10× more expensive" (`vscodeissue312940`). Claude on Copilot's
Anthropic endpoint showed cache reads of 24,003 tokens with markers and 0
without (`openclawissue60174`). Copilot reportedly moved to token-metered
billing on 2026-06-01 (secondary source), which would make lost caching a
cost and not only a latency problem. Grade: single-source each.

**E4 Proxy base URL changes the payload.** Claude Code's tool block measured
~40K tokens a turn against api.anthropic.com versus ~57K against a local base
URL (`chen2026compressiongateway`). The capture confirms Claude Code keeps
Claude-specific prompt and tools for a foreign id, assumes a 200k window,
and sends Haiku a much larger legacy prompt. Grade: single-source.

## F. Delegation and subagents

Vendor defaults:
- **Claude Code** delegates on its own by subagent description. Explore and
  Plan skip CLAUDE.md and git status "to keep research fast and inexpensive";
  forks share the parent's cache and subagents do not. Agent teams use "about
  7x more tokens" (`claudecodesubagentsdocs`, `claudecodecostsdocs`).
- **Anthropic** measured agents at about 4× the tokens of chat and
  multi-agent systems at about 15× (`anthropic2025multiagent`).
- **Codex** spawns only when asked, except that Astra's `ultra` effort
  delegates automatically; subagents inherit model and effort
  (`codexsubagentsdocs`).
- **VS Code Copilot** may call `runSubagent` automatically
  (`vscodesubagentsdocs`).
- **pi** has none by design (`zechner2025pi`).

Grades: vendor claims.

Research evidence:
- Task-specific subagents +4.5 to +5.9 points and general subagents negative
  on ProgramBench (`hu2026beyondmodel`).
- In-context skills at least match subagents without I/O contracts, and
  subagents win with them at higher total tokens
  (`piriyakulkij2026subagentsskills`).
- A single agent matches most multi-agent workflows at lower cost
  (`xu2026singleagent`, `fu2026moreagents`).

Missing: a coding study measuring vendor-harness subagent overhead against a
single-agent control. Local practice already gates optional delegation
harder on the Copilot route (`~/agents/AGENTS.copilot.md`), an observed
over-delegation correction.

## G. Context management and compaction

- Masking old tool outputs matched LLM summarization at about half the
  raw cost (`lindenbauer2025complexitytrap`).
- Drop-only compaction cut cost up to 50% with success maintained
  (`nguyen2026cliffcompaction`).
- Aggressive compression cost 4–5 points of success while cutting 54–77% of
  prompt tokens (`hu2026beyondmodel`).
- Policies using a third of the tokens ran 20–80% longer
  (`satish2026beyondtokensavings`).
- Compaction can silently drop standing instructions, raising constraint
  violations from 0% to 30%; pinning about 47 tokens restores 0%
  (`chen2026governancedecay`). This is directly relevant to instruction-file
  rules surviving compaction.

Grades: benchmark-reported except the last (single-source).

## H. Fixed-prefix cost beyond dollars

**H1 Length hurts.**
- Performance falls 13.9–85% as input grows even with perfect retrieval
  (`du2025contextlength`).
- At 32K, 11 of 13 models drop below half their short-context score
  (`modarressi2025nolima`).
- Chroma reports the same across 18 models (`hong2025contextrot`).
- In coding agents: mini-SWE-agent successes mostly stay under 20–30K tokens
  (`raju2026longcontextbugfix`). A code-audit skill passed 8/10 at 11k
  characters of context and 3/10 at 299k (`xue2026contextrotcoding`).

Grades: benchmark-reported, except Chroma (single-source).

**H2 Tool and skill menus hurt mainly through wrong picks.**
- With a 202-skill library, selection errors explain the drop and pure
  context overhead is indistinguishable from zero (`song2026skillshadowing`).
- Models attend to the right tool yet still pick wrong (`chen2026lookingpicking`).
- Tool-call accuracy drops 7–85% as catalogs grow (`kate2025longfunceval`).
- Short adaptive tool lists beat long ones (`repantis2026howmanytools`,
  `suresh2026toolchoiceconfusion`).

Grades: single-source to benchmark-reported. Unresolved which mechanism
dominates at the 10K–30K-token tool blocks of real coding harnesses.

## I. Measurement confounds that look like harness effects

- Cache-token accounting differs by SDK and board. A published cost result
  reversed after a telemetry normalizer bug (`arjmandi2026harnessormodel` v1).
- Benchmark environment defects hit one harness: Claude Code's KillShell
  depended on `ps` (`zaitb2verified`).
- MCP servers load nondeterministically (40 vs 90 tools across runs).
- Serving-stack tool-call gating (`tang2026servingstack`).
- Leaked git history (`zheng2026clawswebench`).
- Reasoning effort within one harness moves scores more than most harness
  deltas (Claude Code + Opus 5: 34.9 to 53.9 on Terminal-Bench 4.0).
- Run-to-run spread is 2.2–6.0 points on SWE-bench Verified
  (`bjarnason2026randomness`).

## Contested results

- **Does the native harness win?** Yes for Codex on Terminal-Bench and
  Harbor; flips between versions for Claude Code; never for Gemini CLI; no
  average premium on a private suite. Axis: benchmark version, task mix,
  harness version.
- **Claude Code versus Terminus 2 on Terminal-Bench 2.0.** Its deficit was
  partly an environment defect. After the 2.1 fixes Claude Code rose 12.1
  points and Terminus 2 rose 0.9 (`tbench21news`).
- **Claude Code's token overhead against OpenCode.** 3.7–4.7× in Systima's
  proxy-logged rig; the reverse in one LinkedIn run (`napoli2026opencode`).
- **Claude Code tool-schema size.** About 11k o200k locally versus 28K–29K
  reported elsewhere (§A2).
- **AGENTS.md cost direction.** Up 20–23% versus down 16.6% in output tokens;
  the two studies use different metrics.

## Negative and quiet results

- **pi's "8th place" on Terminal-Bench 2.0** had no same-model neighbours.
  Against the current board, pi + Opus 4.5 at 49.8 is below Claude Code 52.1
  and Terminus 2 57.8 (`zechner2025pi`).
- **35 Qwen Code releases** produced no significant gain while doubling
  tokens.
- **Elaborate context managers and multi-agent workflows** mostly fail to
  beat simple baselines at matched cost (§F, §G).
- **The "same model, 32× bill" statement** attributed to Artificial
  Analysis was not found on its methodology page. Grade: folklore.

## Baseline sensitivity

- **Full scaffolds versus bash-only mini-SWE-agent** on SWE-bench Verified:
  a 3–10 point lead, and the self-submitted full-scaffold rows are mostly
  unverified. The ACI advantage in SWE-agent (+7 points on GPT-4 Turbo,
  `yang2024sweagent`) shrinks with model strength (`hu2026beyondmodel`).
- **mini-SWE-agent's own 1.15 → 2.0 update** cost Gemini 3 Pro 4.6 points
  at twice the cost, so a baseline's version matters as much as a harness
  switch.
- **Kapoor et al.'s "control for cost, compare to simple baselines"** remains
  the governing critique (`kapoor2024agentsmatter`, `kapoor2025hal`); grade
  reproduced.

## Disconfirming pass

For "the native harness wins", workers searched for a minimal or foreign
harness beating the vendor's own. They found Terminus 2 over Claude Code
(2.0) and over Gemini CLI, and the Arjmandi null. For "harness bloat hurts",
they found skill-shadowing's null context-overhead component. For "proxies
add instructions", they read the proxy source and found nothing added. For
"pi matches Codex", they found the XBOW loss and the pi board-position
correction.

## Next

- Forward-snowball the four unsnowballed anchors.
- Write concept digests for `shi2026harbor`, `arjmandi2026harnessormodel`,
  `kim2026harnesspostraining`, `liu2026copilottraces` and
  `weinberger2026tokenreduction`.
- Rerun the Copilot quota-blocked probe.

Voids and candidate experiments are in [frontier.md](frontier.md).
