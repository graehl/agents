import assert from "node:assert/strict";
import test from "node:test";
import { canvasPoint } from "../drawing.ts";

test("a stroke retains its relative position when the canvas resizes", () => {
  assert.deepEqual(canvasPoint(50, 25, 200, 100), canvasPoint(100, 50, 400, 200));
});
test("captured pointer outside the canvas stays on its boundary", () => {
  assert.deepEqual(canvasPoint(-10, 110, 100, 100), { x: 0, y: 1 });
  assert.throws(() => canvasPoint(0, 0, 0, 100), /positive dimensions/);
});
