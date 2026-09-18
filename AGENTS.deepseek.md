# DeepSeek Supplement

Read this after `~/agents/AGENTS.global.md` and `~/agents/AGENTS.user.md` when
running as a DeepSeek model. This file holds DeepSeek-specific limits; shared
policy stays in `AGENTS.global.md`.

## Tier

DeepSeek models are weak tier here: read `~/agents/AGENTS.weak.md` and do not
read `AGENTS.frontier.md`.

## No image viewing on DeepSeek v4

DeepSeek v4 models are not multimodal. Never attempt to view an image; the
call fails and causes a service error. DeepSeek v4.1 and later are not
affected by this limitation.
