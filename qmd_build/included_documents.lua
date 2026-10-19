-- Make documents included into one root read as one document.
--
-- Links to an included fragment become in-document links: `x.md#part` ->
-- `#part`, bare `x.md` -> the fragment's first heading. QMD_FRAGMENT_ANCHORS
-- names a JSON file mapping each fragment's path relative to the root's
-- directory -> that heading id. Included text no longer says which file it
-- came from, so a link matches the fragment whose path equals its own, else
-- the one fragment whose path ends with it once leading `./` and `../` are
-- dropped; two fragments with that ending leave the link alone. A `::: {.appendix-doc}` div holds a whole included document:
-- its headings drop one level, and topic-doc metadata lines (`Topic:`,
-- `Glossary:`, `Governs:`) are removed as working metadata.
local anchors = {}
local path = os.getenv("QMD_FRAGMENT_ANCHORS")
if path then
  local file = assert(io.open(path, "r"))
  anchors = pandoc.json.decode(file:read("*a"))
  file:close()
end

local function fragment_link(link)
  if link.target:match("^%a[%w+.-]*:") then
    return nil
  end
  local file, fragment = link.target:match("^([^#]*)#?(.*)$")
  if file == "" then
    return nil
  end
  local anchor = anchors[file]
  if not anchor then
    local tail = file
    repeat
      local before = tail
      tail = tail:gsub("^%./", ""):gsub("^%.%./", "")
    until tail == before
    local matches = 0
    for key, id in pairs(anchors) do
      if key == tail or key:sub(-(#tail + 1)) == "/" .. tail then
        matches = matches + 1
        anchor = id
      end
    end
    if matches ~= 1 then
      return nil
    end
  end
  link.target = "#" .. (fragment ~= "" and fragment or anchor)
  return link
end

local METADATA = { Topic = true, Glossary = true, Governs = true }

local function is_metadata(para)
  local first = para.content[1]
  return first and first.t == "Str" and METADATA[first.text:match("^(%a+):$") or ""]
end

local function appendix(div)
  if not div.classes:includes("appendix-doc") then
    return nil
  end
  div.content = div.content:walk({
    Header = function(header)
      header.level = math.min(header.level + 1, 6)
      return header
    end,
  })
  local kept = pandoc.Blocks({})
  for _, block in ipairs(div.content) do
    if not (block.t == "Para" and is_metadata(block)) then
      kept:insert(block)
    end
  end
  div.content = kept
  return div
end

return {
  { Link = fragment_link },
  { Div = appendix },
}
