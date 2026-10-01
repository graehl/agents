-- Make a document's opening level-1 heading its title.
--
-- The build adds this filter only when the root sets no `title`. The heading
-- leaves the body, so Quarto renders it in its title block and the outline
-- starts at the `##` sections nested under it.
function Pandoc(doc)
  local first = doc.blocks[1]
  if doc.meta.title == nil and first and first.t == "Header" and first.level == 1 then
    doc.meta.title = pandoc.MetaInlines(first.content)
    doc.blocks:remove(1)
    return doc
  end
end
