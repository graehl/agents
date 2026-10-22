-- Link table-note markers to their notes in HTML output.
-- Source convention: a table cell carries a short superscript marker
-- (`^a^`), and the paragraphs directly after the table start each note
-- with the same marker at a line start (`^a^ Protocol C ...`). Pandoc
-- reads both as plain superscripts, so the reader gets no link and the
-- notes run together as one paragraph. This filter sets each note in its
-- own anchored block with a hanging indent, and links every marker in the
-- table and notes that names one of them. Other formats are left unchanged.
if not FORMAT:match("html") then
  return {}
end

-- Inline so a plain `quarto render` without a stylesheet still indents.
local NOTE_STYLE = "padding-left:1.1em;text-indent:-1.1em;margin:0.2em 0"

local tables_seen = 0

local function marker(inline)
  if inline and inline.t == "Superscript" and #inline.content == 1 then
    local str = inline.content[1]
    -- Letters only, so a power such as m^2^ is never taken for a note.
    if str.t == "Str" and str.text:match("^%a%a?$") then
      return str.text
    end
  end
end

local function is_note_block(block)
  return (block.t == "Para" or block.t == "Plain") and marker(block.content[1]) ~= nil
end

local function contains_table(block)
  local found = false
  pandoc.walk_block(pandoc.Div({ block }), {
    Table = function()
      found = true
    end,
  })
  return found
end

-- Raw blocks, such as qmd-html's source-map comments, may sit between a
-- table and its notes.
local function skip_raw(blocks, j)
  while blocks[j] and blocks[j].t == "RawBlock" do
    j = j + 1
  end
  return j
end

-- Split note paragraphs at each line-initial marker into one block per
-- note. A repeated label stays inside the note text.
local function note_blocks(paragraphs, prefix, ids)
  local notes = {}
  for _, paragraph in ipairs(paragraphs) do
    local content = paragraph.content
    for i, inline in ipairs(content) do
      local label = marker(inline)
      local previous = content[i - 1]
      local line_start = i == 1 or previous.t == "SoftBreak" or previous.t == "LineBreak"
      local current = notes[#notes]
      if label and line_start and not ids[label] then
        if i > 1 then
          current.inlines:remove() -- the break before this note
        end
        ids[label] = prefix .. label
        notes[#notes + 1] = {
          id = ids[label],
          inlines = pandoc.List({ pandoc.Span({ inline }, pandoc.Attr("", { "table-note-label" })) }),
        }
      else
        current.inlines:insert(inline)
      end
    end
  end
  local blocks = pandoc.List()
  for _, note in ipairs(notes) do
    blocks:insert(
      pandoc.Div({ pandoc.Plain(note.inlines) }, pandoc.Attr(note.id, { "table-note" }, { style = NOTE_STYLE }))
    )
  end
  return pandoc.Div(blocks, pandoc.Attr("", { "table-notes" }))
end

-- Link bare markers named in `ids`, leaving the notes' own labels.
local function link_markers(block, ids)
  return block:walk({
    traverse = "topdown",
    Span = function(span)
      if span.classes:includes("table-note-label") then
        return span, false
      end
    end,
    Superscript = function(sup)
      local label = marker(sup)
      if label and ids[label] then
        return pandoc.Superscript({
          pandoc.Link({ pandoc.Str(label) }, "#" .. ids[label], "", pandoc.Attr("", { "table-note-ref" })),
        }), false
      end
    end,
  })
end

-- Label -> note id over the whole document, false once a label repeats.
local unique_notes = {}

function Blocks(blocks)
  local out = pandoc.Blocks({})
  local i = 1
  while i <= #blocks do
    local j = skip_raw(blocks, i + 1)
    if contains_table(blocks[i]) and blocks[j] and is_note_block(blocks[j]) then
      tables_seen = tables_seen + 1
      local ids = {}
      local paragraphs = pandoc.List()
      while blocks[j] and is_note_block(blocks[j]) do
        paragraphs:insert(blocks[j])
        j = skip_raw(blocks, j + 1)
      end
      local notes = note_blocks(paragraphs, "tblnote-" .. tables_seen .. "-", ids)
      out:insert(link_markers(blocks[i], ids))
      -- Raw blocks keep their order; the notes take the first paragraph's
      -- place, so source-map comments still enclose them.
      for k = i + 1, j - 1 do
        if blocks[k] == paragraphs[1] then
          out:insert(link_markers(notes, ids))
        elseif not is_note_block(blocks[k]) then
          out:insert(blocks[k])
        end
      end
      for label, id in pairs(ids) do
        unique_notes[label] = unique_notes[label] == nil and id or false
      end
    else
      for k = i, j - 1 do
        out:insert(blocks[k])
      end
    end
    i = j
  end
  return out
end

-- A marker in prose names a note only when no other table reuses its label.
function Pandoc(doc)
  local ids = {}
  for label, id in pairs(unique_notes) do
    if id then
      ids[label] = id
    end
  end
  doc.blocks = pandoc.Blocks(doc.blocks):map(function(block)
    return link_markers(block, ids)
  end)
  return doc
end
