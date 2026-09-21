export interface Point {
  x: number;
  y: number;
}

export interface Stroke {
  color: string;
  points: Point[];
}

/** Converts a pointer position to normalized canvas coordinates. */
export function canvasPoint(x: number, y: number, width: number, height: number): Point {
  if (width <= 0 || height <= 0) throw new Error("Canvas must have positive dimensions");
  return {
    x: Math.max(0, Math.min(1, x / width)),
    y: Math.max(0, Math.min(1, y / height)),
  };
}
