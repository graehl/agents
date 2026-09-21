# Canvas2D

The initial canvas is a small drawing surface, not the user's finished app.
Keep drawing coordinates normalized to the canvas so strokes survive resize.
Match the backing bitmap to device pixel ratio while preserving CSS dimensions.
Use pointer capture for drawing; keep touch scrolling disabled only on the
canvas, not the entire document. Keep keyboard controls useful outside it.

Render on changes rather than running an idle animation loop. If the requested
app needs animation, use elapsed time and pause nonessential work when hidden.
Keep the state model separate from DOM/canvas calls so behavior can be tested.
Handle resize by redrawing state instead of losing it.

`src/main.ts` owns browser wiring; `src/drawing.ts` owns drawing coordinates.
The app has no backend or persistence initially. A page reload clears strokes.
The optional server add-on serves the same bundle and adds an API entry point.
Do not imply that adding it alone stores user data or makes the app public.
