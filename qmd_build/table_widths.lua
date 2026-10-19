-- Identify document tables, and apply build-time column-width decisions.
--
-- Every Pandoc table gets `data-qmd-table` holding its 0-based index in
-- document order, so the first-render measurement (table_widths.js) and the
-- decisions below name the same tables even when raw HTML tables are present.
-- On the second render, QMD_TABLE_WIDTHS names a JSON list with one entry per
-- table: null, or { widths = [fraction, ...] }. A decided table gets those
-- widths as its column specifications (the widest band's choice) and a
-- `data-table-widths` attribute holding its index, which the generated band
-- stylesheet uses to vary widths with the content-column width.
local decisions = {}
local path = os.getenv("QMD_TABLE_WIDTHS")
if path then
  local file = assert(io.open(path, "r"))
  decisions = pandoc.json.decode(file:read("*a"))
  file:close()
end
local index = 0

-- Top-down, so a nested table is numbered after its parent, as in the page.
traverse = "topdown"

function Table(tbl)
  index = index + 1
  tbl.attr.attributes["data-qmd-table"] = tostring(index - 1)
  local decision = decisions[index]
  if decision == nil or decision == pandoc.json.null then
    return tbl
  end
  assert(#decision.widths == #tbl.colspecs, "Table width decision has the wrong column count")
  for i, spec in ipairs(tbl.colspecs) do
    tbl.colspecs[i] = { spec[1], decision.widths[i] }
  end
  tbl.attr.attributes["data-table-widths"] = tostring(index - 1)
  return tbl
end
