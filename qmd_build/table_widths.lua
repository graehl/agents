-- Apply build-time table column-width decisions through the document AST.
--
-- QMD_TABLE_WIDTHS names a JSON list with one entry per table in document
-- order: null, or { widths = [fraction, ...] }. A decided table gets those
-- widths as its column specifications (the widest band's choice) and a
-- `data-table-widths` attribute holding its index, which the generated band
-- stylesheet uses to vary widths with the content-column width.
local path = assert(os.getenv("QMD_TABLE_WIDTHS"), "Missing QMD_TABLE_WIDTHS")
local file = assert(io.open(path, "r"))
local decisions = pandoc.json.decode(file:read("*a"))
file:close()
local index = 0

function Table(tbl)
  index = index + 1
  local decision = decisions[index]
  if decision == nil or decision == pandoc.json.null then
    return nil
  end
  assert(#decision.widths == #tbl.colspecs, "Table width decision has the wrong column count")
  for i, spec in ipairs(tbl.colspecs) do
    tbl.colspecs[i] = { spec[1], decision.widths[i] }
  end
  tbl.attr.attributes["data-table-widths"] = tostring(index - 1)
  return tbl
end
