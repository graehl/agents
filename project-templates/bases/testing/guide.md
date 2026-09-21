# Testing

Test externally meaningful behavior through public entry points. For a fix,
first reproduce the failure, then show that the changed code resolves it.
Develop one behavior slice at a time; avoid tests that merely mirror private
implementation. Mock external boundaries when necessary, not the internal
collaborators whose integration is the behavior under test.

Run the documented focused checks and a small real-path smoke before reporting
completion. For generated content or UI appearance, state properties to inspect
instead of inventing an exact expected string. Exercise failures as well as
success, including invalid input and unavailable dependencies when relevant.

Keep build/test output in named log files when it would otherwise be truncated.
Own every test server: use a fresh port, wait for readiness, and stop it on both
success and failure. Do not restart someone else's server. Keep interaction
tests deterministic and independent of other projects, external accounts, and
the template's authoring checkout.
