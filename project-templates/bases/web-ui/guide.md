# Web UI

Keep the interface legible and usable at desktop and phone widths. Use native
buttons and labeled inputs, visible keyboard focus, accessible names, practical
touch targets, and sufficient contrast. Align visible text and icons optically,
not just their boxes. Preserve the user's focal point during resize and updates.
Respect reduced motion and avoid unnecessary continuous work on hidden pages.

Keep input acknowledgement immediate and independent of expensive rendering.
For changed inputs, test real sequential typing under expected content volume:
each character must appear within 100 ms, without dropped keys. Whole-field
replacement does not establish that. Test touch and keyboard equivalents for
pointer interactions.

Capture and inspect 1200×600 desktop and 375×812 phone renders sequentially.
Check overflow, clipping, spacing, focus, and the requested behavior. Save
captures and present them through the available viewer. `npm run test:browser`
exercises the built app; `npx playwright install chromium` provisions its test
browser when needed. Do not claim untested Safari/device support.

The app can run inside an iframe on its own origin. Use relative asset URLs;
do not call YA APIs or rely on its cookies. Add microphone/camera access only
for a requested feature, with a user gesture and matching iframe permissions.
Do not depend on WebSockets, workers, or cross-origin isolation without checking
the chosen host's support. HTTP static hosting works without a backend API.
