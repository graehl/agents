-- Quiet page furniture: a top-right PDF link and a "rev N · date" label at
-- the right end of the title block's date line.
--
-- The revision shows when the document's front matter has `revision` (with
-- `revision-date`); `qmd-html --bump-revision` maintains both, and a document
-- without them is its original version. QMD_PDF_LINK names the build's
-- sibling PDF. Inserted as document content, not through
-- `include-before-body`, which on the command line would replace the
-- includes Quarto uses for its own page layout.
local pdf = os.getenv("QMD_PDF_LINK")

local function text(value)
  return value and pandoc.utils.stringify(value) or nil
end

function Pandoc(doc)
  if not quarto.doc.is_format("html") then
    return nil
  end
  local blocks = {}
  if pdf then
    table.insert(blocks, '<div class="document-corner"><a class="document-pdf" href="' .. pdf .. '">PDF</a></div>')
  end
  local revision = text(doc.meta.revision)
  if revision then
    local date = text(doc.meta["revision-date"])
    table.insert(
      blocks,
      '<div class="document-revision">rev ' .. revision .. (date and (" · " .. date) or "") .. "</div>"
    )
  end
  for i = #blocks, 1, -1 do
    doc.blocks:insert(1, pandoc.RawBlock("html", blocks[i]))
  end
  return #blocks > 0 and doc or nil
end
