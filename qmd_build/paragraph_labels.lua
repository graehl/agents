-- Give paragraph lead labels ("**NC boundary.** Text…") outline entries.
--
-- A paragraph opening with bold text that ends in "." or ":" becomes a
-- run-in heading one level below the enclosing section, followed by the
-- rest of the paragraph. The heading keeps its punctuation out of the
-- outline (`data-label-punct`, restored by the style's CSS), so Quarto's
-- table of contents lists the label under its section and expands it when
-- the reader is in that section. Bold terms without trailing punctuation
-- ("**Annotations** here means…") stay ordinary bold text.
local function split_label(para)
  local first, second = para.content[1], para.content[2]
  if not (first and first.t == "Strong" and second and second.t == "Space") then
    return nil
  end
  local label = pandoc.utils.stringify(first)
  local text, punct = label:match("^(.-)%s*([.:])$")
  if not text or text == "" then
    return nil
  end
  local inlines = first.content:clone()
  local last = inlines[#inlines]
  if last and last.t == "Str" then
    last.text = last.text:gsub("[.:]$", "")
    if last.text == "" then
      inlines:remove(#inlines)
    end
  end
  local rest = para.content:clone()
  rest:remove(1)
  rest:remove(1)
  return inlines, punct, rest
end

-- Filter-made headings miss Pandoc's reader-time automatic identifiers.
local used = {}

local function identifier(inlines)
  local base = pandoc.utils.stringify(inlines):lower():gsub("[^%w]+", "-"):gsub("^-+", ""):gsub("-+$", "")
  base = base ~= "" and base or "label"
  local id, n = base, 1
  while used[id] do
    id, n = base .. "-" .. n, n + 1
  end
  used[id] = true
  return id
end

local function relabel(blocks, level)
  local out = pandoc.Blocks({})
  for _, block in ipairs(blocks) do
    if block.t == "Header" then
      level = block.level
      out:insert(block)
    elseif block.t == "Div" then
      block.content, level = relabel(block.content, level)
      out:insert(block)
    elseif block.t == "Para" then
      local inlines, punct, rest = split_label(block)
      if inlines then
        local attr = pandoc.Attr(identifier(inlines), { "paragraph-label" }, { ["data-label-punct"] = punct })
        out:insert(pandoc.Header(math.min(level + 1, 6), inlines, attr))
        out:insert(pandoc.Para(rest))
      else
        out:insert(block)
      end
    else
      out:insert(block)
    end
  end
  return out, level
end

function Pandoc(doc)
  doc:walk({
    Header = function(h)
      used[h.identifier] = true
    end,
    Div = function(d)
      used[d.identifier] = true
    end,
  })
  doc.blocks = relabel(doc.blocks, 1)
  return doc
end
