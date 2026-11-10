-- Size LaTeX table columns from their content, as a browser does in HTML.
--
-- Pandoc gives a pipe table relative column widths from its separator dashes
-- once a source row is longer than `columns` (72 by default). The usual
-- `|---|---|` separator makes those widths nearly equal, so in a PDF a
-- two-letter code column takes as much room as a column of prose, and the
-- prose wraps one word per line. HTML builds avoid this with a large
-- `columns` value, which lets the browser size columns and leaves the dash
-- counts with no visible effect, but LaTeX needs widths for wrapping.
--
-- A paper that lists this filter opts out of dash-count widths. It replaces
-- every table's relative widths with widths from the content: each column
-- gets its longest unbreakable piece, and the room left over is shared in
-- proportion to how much more each column's longest cell needs, like HTML's
-- automatic table layout. Set explicit widths with `tbl-colwidths`, which is
-- left unchanged, as are tables without relative widths (no source row
-- longer than `columns`). Other formats are left unchanged.
--
-- Limits. A cell is measured by counting the characters of its text, so a
-- cell of math counts its TeX source (`\frac{a}{b}` is eleven characters
-- wide) and an image counts its alt text; give such a table `tbl-colwidths`.
-- The character budget is for 10pt type in one column. The text-block width
-- comes from the document's `geometry` and `papersize` metadata when they
-- state it as a `textwidth` or as a known paper size with horizontal margins;
-- otherwise it is assumed to be 6.5in (US Letter with 1in margins, the page
-- the paper template sets).
if not FORMAT:match("latex") then
  return {}
end

local stringify = pandoc.utils.stringify

-- Average 10pt characters across a 6.5in text block. Pandoc's widths are
-- fractions of the block less 2\tabcolsep (12pt, about 2.4 characters) per
-- column, so that padding comes off the budget. A word gets one character
-- of slack because proportional glyphs vary in width.
local ASSUMED_TEXT_INCHES = 6.5
local ASSUMED_LINE_CHARS = 94
local line_chars = ASSUMED_LINE_CHARS
local COLUMN_PADDING_CHARS = 2.4
local WORD_SLACK_CHARS = 1
-- Type sizes to try, with how many more characters each fits than 10pt.
-- The padding is a fixed length, so the whole 10pt budget scales.
local SIZE_STEPS = {
  { command = nil, chars = 1.0 },
  { command = "\\small", chars = 10 / 9 },
  { command = "\\footnotesize", chars = 10 / 8 },
  { command = "\\scriptsize", chars = 10 / 7 },
}

-- Capitals are wider than the average character; MAPSSWE overflowed a
-- column sized by its letter count.
local CAPITAL_CHARS = 1.4

local function text_length(s)
  local _, capitals = s:gsub("%u", "")
  return (utf8.len(s) or #s) + (CAPITAL_CHARS - 1) * capitals
end

local INCHES_PER_UNIT = { ["in"] = 1, cm = 1 / 2.54, mm = 1 / 25.4, pt = 1 / 72.27, bp = 1 / 72 }
local PAPER_WIDTH_INCHES = {
  letter = 8.5,
  legal = 8.5,
  executive = 7.25,
  a4 = 210 / 25.4,
  a5 = 148 / 25.4,
  b5 = 176 / 25.4,
}

local function inches(length)
  local number, unit = (length or ""):match("^([%d%.]+)%s*(%a+)$")
  return number and INCHES_PER_UNIT[unit] and tonumber(number) * INCHES_PER_UNIT[unit]
end

-- The geometry package's `key=value` options, whether the metadata holds a
-- list of them or one comma-separated string.
local function geometry_options(meta)
  local options = {}
  if meta.geometry == nil then
    return options
  end
  local items = pandoc.utils.type(meta.geometry) == "List" and meta.geometry or { meta.geometry }
  for _, item in ipairs(items) do
    for option in stringify(item):gmatch("[^,]+") do
      local key, value = option:match("^%s*(%a+)%s*=%s*(.-)%s*$")
      if key then
        options[key] = value
      end
    end
  end
  return options
end

-- Text-block width when the metadata states it, else nil: geometry accepts
-- layouts (`scale`, a two-valued margin, a class default) not resolved here.
local function text_block_inches(meta)
  local options = geometry_options(meta)
  if options.textwidth then
    return inches(options.textwidth)
  end
  local paper = inches(options.paperwidth) or PAPER_WIDTH_INCHES[stringify(meta.papersize or "")]
  local left = inches(options.left or options.lmargin or options.inner or options.hmargin or options.margin)
  local right = inches(options.right or options.rmargin or options.outer or options.hmargin or options.margin)
  return paper and left and right and paper - left - right
end

local function read_text_block(meta)
  local width = text_block_inches(meta)
  if width then
    line_chars = ASSUMED_LINE_CHARS * width / ASSUMED_TEXT_INCHES
  end
end

local function measure(tbl)
  local ncols = #tbl.colspecs
  local longest, word = {}, {}
  for i = 1, ncols do
    longest[i], word[i] = 1, 1
  end
  local function visit(rows)
    for _, row in ipairs(rows) do
      local col = 1
      for _, cell in ipairs(row.cells) do
        if cell.col_span == 1 and col <= ncols then
          local s = pandoc.utils.stringify(cell.contents)
          longest[col] = math.max(longest[col], text_length(s))
          -- LaTeX may break a line after an explicit hyphen or slash, so a
          -- name such as parakeet-ctc-vi needs only its longest piece.
          for w in s:gmatch("[^%s%-/]+[%-/]?") do
            word[col] = math.max(word[col], text_length(w) + WORD_SLACK_CHARS)
          end
        end
        col = col + cell.col_span
      end
    end
  end
  visit(tbl.head.rows)
  for _, body in ipairs(tbl.bodies) do
    visit(body.head)
    visit(body.body)
  end
  visit(tbl.foot.rows)
  return longest, word
end

local function has_relative_widths(tbl)
  if #tbl.colspecs < 2 then
    return false
  end
  for _, spec in ipairs(tbl.colspecs) do
    if type(spec[2]) ~= "number" or spec[2] <= 0 then
      return false
    end
  end
  return true
end

-- Quarto applies `tbl-colwidths` after user filters, so here it may still be
-- a table attribute or text in the caption's trailing `{...}`.
local function has_author_widths(tbl)
  if tbl.attr.attributes["tbl-colwidths"] then
    return true
  end
  local caption = stringify(tbl.caption.long or {})
  return caption:find("tbl-colwidths=", 1, true) ~= nil
end

local function size_columns(tbl)
  if has_author_widths(tbl) or not has_relative_widths(tbl) then
    return nil
  end
  local longest, word = measure(tbl)
  local ncols = #tbl.colspecs
  local need, minimum, slack = 0, 0, 0
  for i = 1, ncols do
    longest[i] = math.max(longest[i], word[i])
    need = need + longest[i]
    minimum = minimum + word[i]
    slack = slack + (longest[i] - word[i])
  end
  -- A table whose longest words cannot all fit (in HTML it would usually be
  -- set wider than the text) is set in the first smaller size that fits
  -- them, rather than splitting words mid-letter.
  local size, available
  for _, step in ipairs(SIZE_STEPS) do
    size = step
    available = (line_chars - COLUMN_PADDING_CHARS * ncols) * step.chars
    if minimum <= available then
      break
    end
  end
  local widths = {}
  for i = 1, ncols do
    if need <= available then
      widths[i] = longest[i] / available
    elseif minimum >= available or slack == 0 then
      widths[i] = word[i] / minimum
    else
      local extra = (available - minimum) * (longest[i] - word[i]) / slack
      widths[i] = (word[i] + extra) / available
    end
    tbl.colspecs[i] = { tbl.colspecs[i][1], widths[i] }
  end
  if size.command == nil then
    return tbl
  end
  return {
    pandoc.RawBlock("latex", "\\begingroup" .. size.command),
    tbl,
    pandoc.RawBlock("latex", "\\endgroup"),
  }
end

-- Two passes: within one pass Pandoc visits tables before metadata.
return { { Meta = read_text_block }, { Table = size_columns } }
