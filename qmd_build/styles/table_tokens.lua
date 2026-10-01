-- Keep short hyphenated tokens whole inside table cells ("CC-BY-NC-SA").
-- Browsers may break a line after any hyphen; U+2011 NON-BREAKING HYPHEN
-- makes such a token one unbreakable unit, so automatic table layout sizes
-- its column to fit it instead of wrapping mid-name. Longer hyphenated
-- runs keep ordinary hyphens and may still wrap.
local MAX_TOKEN = 16
local NB_HYPHEN = "\u{2011}"

local function keep_whole(str)
  local text = str.text
  if text:find("-", 1, true) and utf8.len(text) <= MAX_TOKEN and not text:match("^%-") then
    str.text = text:gsub("%-", NB_HYPHEN)
    return str
  end
end

local function cell_blocks(cell)
  cell.contents = cell.contents:walk({ Str = keep_whole })
  return cell
end

function Table(tbl)
  local function rows(list)
    for _, row in ipairs(list) do
      for i, cell in ipairs(row.cells) do
        row.cells[i] = cell_blocks(cell)
      end
    end
  end
  rows(tbl.head.rows)
  for _, body in ipairs(tbl.bodies) do
    rows(body.head)
    rows(body.body)
  end
  rows(tbl.foot.rows)
  return tbl
end
