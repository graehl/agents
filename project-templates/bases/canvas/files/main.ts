import { canvasPoint, type Stroke } from "./drawing.ts";
import "./style.css";

const canvas = document.querySelector<HTMLCanvasElement>("canvas")!;
const context = canvas.getContext("2d");
if (!context) throw new Error("Canvas2D is unavailable");
const ctx = context;
const status = document.querySelector<HTMLOutputElement>("#status")!;
const title = document.querySelector<HTMLInputElement>("#title")!;
const strokes: Stroke[] = [];
let current: Stroke | undefined;
let pointerId: number | undefined;
let color = "#7357c8";

function redraw() {
  const { width, height } = canvas.getBoundingClientRect();
  const ratio = window.devicePixelRatio || 1;
  canvas.width = Math.round(width * ratio);
  canvas.height = Math.round(height * ratio);
  ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
  ctx.lineWidth = 4;
  ctx.lineCap = "round";
  ctx.lineJoin = "round";
  for (const stroke of strokes) {
    ctx.strokeStyle = stroke.color;
    ctx.fillStyle = stroke.color;
    const first = stroke.points[0];
    if (!first) continue;
    ctx.beginPath();
    ctx.arc(first.x * width, first.y * height, 2, 0, 2 * Math.PI);
    ctx.fill();
    ctx.beginPath();
    ctx.moveTo(first.x * width, first.y * height);
    for (const point of stroke.points.slice(1))
      ctx.lineTo(point.x * width, point.y * height);
    ctx.stroke();
  }
  status.value = `${strokes.length} ${strokes.length === 1 ? "stroke" : "strokes"}`;
}

canvas.addEventListener("pointerdown", (event) => {
  if (pointerId !== undefined || event.button !== 0) return;
  pointerId = event.pointerId;
  const rect = canvas.getBoundingClientRect();
  current = {
    color,
    points: [
      canvasPoint(
        event.clientX - rect.left,
        event.clientY - rect.top,
        rect.width,
        rect.height,
      ),
    ],
  };
  strokes.push(current);
  canvas.setPointerCapture(event.pointerId);
  redraw();
});
canvas.addEventListener("pointermove", (event) => {
  if (!current || event.pointerId !== pointerId) return;
  const rect = canvas.getBoundingClientRect();
  current.points.push(
    canvasPoint(
      event.clientX - rect.left,
      event.clientY - rect.top,
      rect.width,
      rect.height,
    ),
  );
  redraw();
});
canvas.addEventListener("lostpointercapture", () => {
  current = undefined;
  pointerId = undefined;
});
for (const button of document.querySelectorAll<HTMLButtonElement>("[data-color]")) {
  button.addEventListener("click", () => {
    color = button.dataset.color!;
    for (const other of document.querySelectorAll("[data-color]"))
      other.setAttribute("aria-pressed", String(other === button));
  });
}
document.querySelector("#undo")!.addEventListener("click", () => {
  strokes.pop();
  redraw();
});
document.querySelector("#clear")!.addEventListener("click", () => {
  strokes.length = 0;
  redraw();
});
title.addEventListener("input", () => {
  document.title = title.value || "App canvas";
});
new ResizeObserver(redraw).observe(canvas);
redraw();
