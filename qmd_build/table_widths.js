// Choose table column widths that minimize rendered table height, per band
// of content-column width.
//
// Runs in the headless build browser on a first render, never in the
// published page. For each target width, the main content column is set to
// that width; phase 1 estimates each column's wrapped line count from canvas
// font metrics and searches widths on that model; phase 2 applies the
// estimate with fixed table layout and takes a few real-layout steps from it.
// A band keeps the browser's automatic layout unless the chosen widths render
// shorter. Returns decisions[table][band]: null or
// { widths: [fraction, ...], autoHeight, height, estimatedHeight }.
(({ bandWidths, step = 0.02, refineSteps = 6 }) => {
  const canvas = document.createElement("canvas").getContext("2d");
  const main = document.querySelector("main") ?? document.body;
  const tables = [...document.querySelectorAll("table")];
  const originals = tables.map((table) => table.cloneNode(true));

  function px(value) {
    return Number.parseFloat(value) || 0;
  }

  // Line-break pieces: whitespace-separated words, split after ordinary
  // hyphens (U+2011 non-breaking hyphens keep a token whole).
  function pieces(text) {
    return text
      .split(/\s+/)
      .filter(Boolean)
      .flatMap((word) => word.split(/(?<=-)(?=.)/));
  }

  function cellModel(cell) {
    const style = getComputedStyle(cell);
    canvas.font = `${style.fontStyle} ${style.fontWeight} ${style.fontSize} ${style.fontFamily}`;
    const widths = pieces(cell.innerText).map((piece) => canvas.measureText(piece).width);
    return {
      widths,
      space: canvas.measureText(" ").width,
      lineHeight: px(style.lineHeight) || 1.4 * px(style.fontSize),
      padX:
        px(style.paddingLeft) +
        px(style.paddingRight) +
        px(style.borderLeftWidth) +
        px(style.borderRightWidth),
      padY: px(style.paddingTop) + px(style.paddingBottom),
      minWidth: Math.max(0, ...widths),
      natural: widths.reduce((sum, w) => sum + w, 0) + Math.max(0, widths.length - 1) * canvas.measureText(" ").width,
    };
  }

  function lineCount(model, width) {
    const available = width - model.padX;
    let lines = 1;
    let used = 0;
    for (const w of model.widths) {
      const extended = used === 0 ? w : used + model.space + w;
      if (extended > available && used > 0) {
        lines += 1;
        used = w;
      } else {
        used = extended;
      }
    }
    return lines;
  }

  function estimatedHeight(models, widthsPx) {
    return models.reduce(
      (total, row) =>
        total +
        Math.max(
          ...row.map(
            (model, column) => lineCount(model, widthsPx[column]) * model.lineHeight + model.padY,
          ),
        ),
      0,
    );
  }

  // Pairwise transfer search: move `step` of the width from one column to
  // another while that lowers `cost` and keeps each column above its minimum.
  function descend(fractions, minimums, cost, maxMoves) {
    let best = cost(fractions);
    for (let move = 0; move < maxMoves; move += 1) {
      let improved = null;
      for (let from = 0; from < fractions.length; from += 1) {
        for (let to = 0; to < fractions.length; to += 1) {
          if (from === to || fractions[from] - step < minimums[from]) continue;
          const trial = fractions.slice();
          trial[from] -= step;
          trial[to] += step;
          const value = cost(trial);
          if (value < best - 0.5 && (!improved || value < improved.value)) {
            improved = { trial, value };
          }
        }
      }
      if (!improved) break;
      fractions = improved.trial;
      best = improved.value;
    }
    return { fractions, value: best };
  }

  function applyWidths(table, fractions) {
    let group = table.querySelector(":scope > colgroup");
    if (!group) {
      group = document.createElement("colgroup");
      table.insertBefore(group, table.querySelector(":scope > thead, :scope > tbody"));
    }
    group.replaceChildren(
      ...fractions.map((f) => {
        const col = document.createElement("col");
        col.style.setProperty("width", `${(100 * f).toFixed(2)}%`, "important");
        return col;
      }),
    );
    table.style.tableLayout = "fixed";
    table.style.width = "100%";
  }

  function decide(table) {
    const rows = [...table.rows].map((row) => [...row.cells]);
    const columns = rows[0]?.length ?? 0;
    if (columns < 2 || rows.some((cells) => cells.length !== columns || cells.some((c) => c.colSpan !== 1))) {
      return null;
    }
    const autoHeight = table.getBoundingClientRect().height;
    const available = table.parentElement.getBoundingClientRect().width;
    const models = rows.map((cells) => cells.map(cellModel));
    const column = (c, f) => Math.max(...models.map((row) => f(row[c])));
    const minimums = [...Array(columns).keys()].map((c) => column(c, (m) => m.minWidth + m.padX) / available);
    if (minimums.reduce((a, b) => a + b, 0) > 1) return null;
    const natural = [...Array(columns).keys()].map((c) => column(c, (m) => m.natural + m.padX));
    const total = natural.reduce((a, b) => a + b, 0);
    const start = natural.map((n, c) => Math.max(minimums[c], n / total));
    const scale = start.reduce((a, b) => a + b, 0);
    const estimate = descend(
      start.map((f) => f / scale),
      minimums,
      (f) => estimatedHeight(models, f.map((x) => x * available)),
      400,
    );
    const real = descend(
      estimate.fractions,
      minimums,
      (f) => {
        applyWidths(table, f);
        return table.getBoundingClientRect().height;
      },
      refineSteps,
    );
    if (real.value >= autoHeight - 1) return null;
    return { widths: real.fractions, autoHeight, height: real.value, estimatedHeight: estimate.value };
  }

  const decisions = tables.map(() => []);
  for (const width of bandWidths) {
    main.style.width = `${width}px`;
    main.style.maxWidth = "none";
    tables.forEach((table, index) => {
      const fresh = originals[index].cloneNode(true);
      table.replaceWith(fresh);
      tables[index] = fresh;
      decisions[index].push(decide(fresh));
    });
  }
  return decisions;
})
