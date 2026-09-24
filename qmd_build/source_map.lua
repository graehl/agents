-- Carry original section locations through Quarto without changing its reader.
local path = assert(os.getenv("QMD_SOURCE_TARGETS"), "Missing QMD_SOURCE_TARGETS")
local file = assert(io.open(path, "r"))
local targets = pandoc.json.decode(file:read("*a"))
file:close()
local by_header = {}
for _, target in ipairs(targets) do
  if target.headerId then
    assert(not by_header[target.headerId], "Duplicate document heading: " .. target.headerId)
    by_header[target.headerId] = target
  end
end

function Header(header)
  local target = by_header[header.identifier]
  if target then
    header.attributes["data-qmd-source"] = target.id
    return header
  end
end

function Image(image)
  image.attributes["data-qmd-image-source"] = image.src
  return image
end
