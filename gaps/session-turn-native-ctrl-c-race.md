---
slug: session-turn-native-ctrl-c-race
noticed: 2026-10-18
where: tests/test_session_turn.py test_native_ctrl_c_interrupts_only_the_helper_process_group
---

**Gap:** under a full `tests/test_rendezvous.py tests/test_session_turn.py`
run, this test failed once with outcome `provider-failed` and
`providerExitCode: 1` instead of an interrupted turn; it passed three of three
times run alone. The receipt shows the fake `claude` had already emitted its
`system`/`started` record, which it prints after installing its SIGINT
handler, and the test waits for that event before signalling; so the exit 1
is not the obvious handler-installation race. Cause undiagnosed. The suite
carries an intermittent red that can mask a real regression in native
interrupt handling.

**Noticed while:** validating the switch of rendezvous image preparation from
ImageMagick to Pillow (run under `uv run --with pillow --with pytest`); the
failing path does not prepare images.

**Next step:** capture the fake provider's stderr on failure (the exit-1
traceback) under repeated full-suite runs, then fix the identified ordering.
