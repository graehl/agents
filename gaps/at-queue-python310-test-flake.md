---
slug: at-queue-python310-test-flake
noticed: 2026-08-15
where: tests/test_at_queue.py
---

**Gap:** Repeated full-suite runs under CPython 3.10 twice produced different
one-off failures in tests expecting `at-queue done` to exit 4. The failing
assertions received empty stdout and do not report the actual return code or
stderr. Immediate full reruns passed, as did 20 targeted repetitions, so the
underlying subprocess failure remains unidentified and unreproduced.

**Noticed while:** Verifying that `scripts/at-queue` honors the documented
Python 3.10 floor after replacing `typing.Self`.

**Fix sketch:** Make the affected assertions retain return code, stdout, and
stderr; loop the complete suite under 3.10 until the unexpected subprocess
outcome is captured, then fix the owning process/lock invariant rather than
loosening the assertions.
