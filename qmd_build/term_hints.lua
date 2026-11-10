-- Authored definition spans and TeX term references share one document registry.
local directory = pandoc.path.directory(PANDOC_SCRIPT_FILE)
local html = FORMAT:match("html") ~= nil
local latex = FORMAT:match("latex") ~= nil
local stringify = pandoc.utils.stringify

local function fail(message)
	error("Term hints: " .. message)
end

local function group(text, start)
	local first = text:find("%S", start)
	if not first or text:sub(first, first) ~= "{" then
		fail("expected a braced argument near " .. text:sub(start, start + 40))
	end
	local depth, i = 1, first + 1
	while i <= #text do
		local c = text:sub(i, i)
		if c == "\\" then
			i = i + 2
		else
			if c == "{" then
				depth = depth + 1
			end
			if c == "}" then
				depth = depth - 1
			end
			if depth == 0 then
				return text:sub(first + 1, i - 1), i + 1
			end
			i = i + 1
		end
	end
	fail("unclosed braced argument")
end

local function argument_end(text, start)
	local first = text:find("%S", start)
	if not first then
		return start
	end
	if text:sub(first, first) == "{" then
		local _, last = group(text, first)
		return last
	end
	local command = text:match("^\\[A-Za-z]+", first)
	if command then
		return first + #command
	end
	return first + #utf8.char(utf8.codepoint(text, first))
end

local styled = {
	mathbf = true,
	mathit = true,
	mathrm = true,
	mathbb = true,
	mathcal = true,
	mathsf = true,
	mathtt = true,
	boldsymbol = true,
	operatorname = true,
}
local opaque = {
	text = 1,
	textrm = 1,
	textbf = 1,
	textit = 1,
	label = 1,
	ref = 1,
	tag = 1,
	begin = 1,
	["end"] = 1,
	href = 2,
	hyperlink = 2,
	termignore = 1,
}
local greek = {}
for name in
	("alpha beta gamma delta epsilon varepsilon zeta eta theta vartheta iota kappa lambda mu nu xi pi rho sigma tau upsilon phi varphi chi psi omega Gamma Delta Theta Lambda Xi Pi Sigma Upsilon Phi Psi Omega"):gmatch(
		"%S+"
	)
do
	greek[name] = true
end

-- TeX control words and styled groups are atomic: s never matches \sin or \text{scores}.
local function tokens(text)
	local result, i = {}, 1
	while i <= #text do
		local start, name = i, nil
		if text:sub(i, i) == "\\" then
			name = text:match("^\\([A-Za-z]+)", i)
			i = i + (name and #name + 1 or 2)
			if name == "termref" then
				local id, following = group(text, i)
				local body, last = group(text, following)
				result[#result + 1] = { text = text:sub(start, last - 1), id = id, body = body }
				i = last
			else
				if styled[name] or opaque[name] then
					if name == "operatorname" and text:sub(i, i) == "*" then
						i = i + 1
					end
					for _ = 1, opaque[name] or 1 do
						i = argument_end(text, i)
					end
				end
				result[#result + 1] = {
					text = text:sub(start, i - 1),
					symbol = styled[name] or greek[name],
					opaque = opaque[name],
					name = name,
				}
			end
		else
			local code = utf8.codepoint(text, i)
			i = i + #utf8.char(code)
			local value = text:sub(start, i - 1)
			result[#result + 1] = { text = value, symbol = value:match("%a") ~= nil or code > 127 }
		end
	end
	return result
end

local function unmarked_math(text)
	local out = {}
	for _, token in ipairs(tokens(text)) do
		if token.id then
			out[#out + 1] = unmarked_math(token.body)
		elseif token.name == "termignore" then
			out[#out + 1] = unmarked_math((group(token.text, #"\\termignore" + 1)))
		else
			out[#out + 1] = token.text
		end
	end
	return table.concat(out)
end

local function aliases(value)
	local out = {}
	for item in (value or ""):gmatch("[^|]+") do
		item = item:match("^%s*(.-)%s*$")
		if item ~= "" then
			out[#out + 1] = item
		end
	end
	return out
end

local defaults = {
	{ "\\sum", "Summation over the indicated indices or set.", "op" },
	{ "\\prod", "Product over the indicated indices or set.", "op" },
	{ "\\in", "Set membership: the left operand is an element of the right-hand set.", "rel" },
	{ "\\notin", "Non-membership: the left operand is not an element of the right-hand set.", "rel" },
	{ "\\subseteq", "Subset inclusion, allowing equality.", "rel" },
	{ "\\cup", "Set union: elements belonging to either set.", "bin" },
	{ "\\cap", "Set intersection: elements belonging to both sets.", "bin" },
	{ "\\forall", "Universal quantifier: for every element in the stated domain.", "ord" },
	{ "\\exists", "Existential quantifier: at least one such element exists.", "ord" },
	{ "\\operatorname{argmax}", "The argument or arguments at which the expression is maximal.", "op" },
	{ "\\operatorname{argmin}", "The argument or arguments at which the expression is minimal.", "op" },
	{ "\\mathbb{R}", "The set of real numbers.", "ord" },
}

-- A metadata switch is a YAML boolean in the rendered document's metadata
-- (front matter or `_quarto.yml`); any other value is an authoring error.
local function metadata_switch(meta, key, default)
	local value = meta[key]
	if value == nil then
		return default
	end
	if type(value) ~= "boolean" then
		fail(key .. " must be true or false")
	end
	return value
end

-- Registry: every definition, built-in notation entry and first-mention
-- paragraph, by ID and by the alias that links to it. A `math` alias matches
-- TeX tokens. A `prose` alias is authored (`terms=`) and matches plain or
-- formatted words.
local function new_registry()
	return { by_id = {}, ordered = {}, math = {}, prose = {}, first_mentions = 0 }
end

local function register(registry, id, content, kind, maths, prose, class)
	if not id:match("^term%-%a[%w%-]*$") then
		fail("definition ID must be term-<name>: " .. id)
	end
	if registry.by_id[id] then
		fail("duplicate definition " .. id)
	end
	local preview = pandoc.Span(content):walk({
		Math = function(el)
			el.text = unmarked_math(el.text)
			return el
		end,
	}).content
	local entry = { id = id, content = preview, kind = kind, class = class }
	registry.by_id[id], registry.ordered[#registry.ordered + 1] = entry, entry
	for _, pair in ipairs({ { registry.math, maths }, { registry.prose, prose } }) do
		for _, alias in ipairs(pair[2]) do
			if pair[1][alias] then
				fail("ambiguous alias " .. alias .. "; use explicit termref markers")
			end
			pair[1][alias] = entry
		end
	end
	return entry
end

local function register_definitions(registry, doc)
	doc:walk({
		Span = function(span)
			if span.classes:includes("term-definition") then
				register(
					registry,
					span.identifier,
					span.content,
					"Definition",
					aliases(span.attributes.math),
					aliases(span.attributes.terms),
					span.attributes["math-class"]
				)
			end
		end,
	})
end

-- An authored definition of the same math alias replaces the built-in entry.
local function register_default_operators(registry)
	for i, item in ipairs(defaults) do
		if not registry.math[item[1]] then
			local entry = register(
				registry,
				"term-operator-" .. i,
				pandoc.Inlines({
					pandoc.Math("InlineMath", item[1]),
					pandoc.Str(":"),
					pandoc.Space(),
					pandoc.Str(item[2]),
				}),
				"Notation",
				{ item[1] },
				{},
				item[3]
			)
			entry.builtin = true
		end
	end
end

local function reference(registry, id)
	local entry = registry.by_id[id]
	if not entry then
		fail("unknown reference " .. id)
	end
	entry.used = true
	return entry
end

-- Implicit discovery: a paragraph is the one entry for every math symbol it
-- introduces, so its preview is embedded once. Discovery leaves an empty span
-- carrying the entry's ID at the start of the paragraph; emission keeps it as
-- the landing site only when a later paragraph links to it. Only math is
-- read. Outside math an arrow or a relation sign is punctuation, and bold or
-- italic text marks stress and labels as often as a new term: a prose term
-- gets links from an authored definition (`terms=`).
local function discover_first_mentions(registry, block)
	local entry
	local function introduce(symbol)
		if not entry then
			registry.first_mentions = registry.first_mentions + 1
			entry = register(
				registry,
				"term-first-" .. registry.first_mentions,
				block.content,
				"First mention",
				{},
				{}
			)
		end
		registry.math[symbol] = entry
	end
	pandoc.Span(block.content):walk({
		traverse = "topdown",
		Link = function(el)
			return el, false
		end,
		Span = function(el)
			if el.classes:includes("no-term-hints") then
				return el, false
			end
		end,
		Math = function(el)
			for _, token in ipairs(tokens(el.text)) do
				if token.symbol and not registry.math[token.text] then
					introduce(token.text)
				end
			end
		end,
	})
	if entry then
		block.content:insert(1, pandoc.Span({}, pandoc.Attr(entry.id)))
		return block
	end
end

-- The entry of the first-mention paragraph `block`, if it is one.
local function own_first_mention(registry, block)
	local first = block.content[1]
	local entry = first and first.t == "Span" and registry.by_id[first.identifier]
	return entry and entry.kind == "First mention" and entry or nil
end

local function register_first_mentions(registry, doc)
	local function discover(block)
		return discover_first_mentions(registry, block)
	end
	return doc:walk({
		traverse = "topdown",
		Para = discover,
		Plain = discover,
		Div = function(el)
			if el.classes:includes("no-term-hints") then
				return el, false
			end
		end,
	})
end

-- Annotation: turn each occurrence of a registered alias into a link.
local math_classes = {
	ord = true,
	op = true,
	bin = true,
	rel = true,
	open = true,
	close = true,
	punct = true,
	inner = true,
}

local function math_link(entry, text, script)
	entry.used = true
	local result = html and ("\\href{#" .. entry.id .. "}{" .. text .. "}")
		or ("\\hyperref[" .. entry.id .. "]{" .. text .. "}")
	if entry.class then
		if not math_classes[entry.class] then
			fail("invalid math-class " .. entry.class)
		end
		result = "\\math" .. entry.class .. "{" .. result .. "}"
		if entry.class == "op" and latex then
			result = result .. "\\displaylimits"
		end
	end
	-- Unclassed links must remain one argument for x^s, tau_b, and hat x.
	-- Keep operator classes outside groups so limits and spacing survive.
	return entry.class and not script and result or ("{" .. result .. "}")
end

local function longest_math_alias(registry)
	local max_tokens = 1
	for alias in pairs(registry.math) do
		max_tokens = math.max(max_tokens, #tokens(alias))
	end
	return max_tokens
end

-- `own` is the first-mention entry of the paragraph holding `el`, or nil.
local function annotate_math(registry, max_tokens, own, el)
	local source, out, i = tokens(el.text), {}, 1
	while i <= #source do
		local token = source[i]
		local previous = i - 1
		while previous > 0 and source[previous].text:match("^%s+$") do
			previous = previous - 1
		end
		local script = previous > 0 and (source[previous].text == "_" or source[previous].text == "^")
		if token.id then
			out[#out + 1] = math_link(reference(registry, "term-" .. token.id), unmarked_math(token.body), script)
			i = i + 1
		elseif token.name == "termignore" then
			out[#out + 1] = group(token.text, #"\\termignore" + 1)
			i = i + 1
		elseif token.opaque then
			out[#out + 1], i = token.text, i + 1
		else
			local candidate, best, last, spelling = "", nil, i, nil
			for j = i, math.min(#source, i + max_tokens - 1) do
				if source[j].opaque or source[j].id then
					break
				end
				candidate = candidate .. source[j].text
				if registry.math[candidate] and registry.math[candidate] ~= own then
					best, last, spelling = registry.math[candidate], j, candidate
				end
			end
			out[#out + 1] = best and math_link(best, spelling, script) or token.text
			i = best and last + 1 or i + 1
		end
	end
	el.text = table.concat(out)
	return el
end

local function link(content, entry)
	entry.used = true
	return pandoc.Link(content, "#" .. entry.id, "", pandoc.Attr("", { "term-ref" }))
end

-- Longest first, so a phrase wins over a shorter alias it contains.
local function prose_phrases(registry)
	local phrases = {}
	for alias, entry in pairs(registry.prose) do
		phrases[#phrases + 1] = { text = alias, entry = entry }
	end
	table.sort(phrases, function(a, b)
		return #a.text > #b.text
	end)
	return phrases
end

-- Match phrases across ordinary prose tokens without changing their formatting.
local function link_phrases(phrases, inlines)
	local out, i = pandoc.Inlines({}), 1
	while i <= #inlines do
		local matched = false
		for _, phrase in ipairs(phrases) do
			local prefix = inlines[i].t == "Str" and (inlines[i].text:match("^([%(\"%[%']*)") or "") or ""
			local value, last = "", i - 1
			for j = i, #inlines do
				local el = inlines[j]
				if el.t ~= "Str" and el.t ~= "Space" and el.t ~= "SoftBreak" then
					break
				end
				local piece = el.t == "Str" and el.text or " "
				if j == i then
					piece = piece:sub(#prefix + 1)
				end
				value = value .. piece
				last = j
				if #value >= #phrase.text then
					break
				end
			end
			local suffix = value:sub(#phrase.text + 1)
			if value:sub(1, #phrase.text) == phrase.text and (suffix == "" or suffix:match("^[%.,;:!?%)]+$")) then
				local content = pandoc.Inlines({})
				for j = i, last do
					content:insert(inlines[j]:clone())
				end
				if prefix ~= "" then
					content[1].text = content[1].text:sub(#prefix + 1)
					out:insert(pandoc.Str(prefix))
				end
				if suffix ~= "" then
					content[#content].text = content[#content].text:sub(1, -#suffix - 1)
				end
				out:insert(link(content, phrase.entry))
				if suffix ~= "" then
					out:insert(pandoc.Str(suffix))
				end
				i, matched = last + 1, true
				break
			end
		end
		if not matched then
			out:insert(inlines[i])
			i = i + 1
		end
	end
	return out
end

-- A `.no-term-hints` passage keeps its text and loses only the authoring markers.
local function without_term_hints(el)
	if el.classes:includes("no-term-hints") then
		return el:walk({
			Math = function(m)
				m.text = unmarked_math(m.text)
				return m
			end,
		}),
			false
	end
end

-- The handlers that annotate the text of one paragraph, or of everything
-- outside first-mention paragraphs when `own` is nil. A link never points at
-- the paragraph it sits in: there the reader is already at the first mention.
local function annotation(registry, max_tokens, phrases, own)
	-- A bold or italic authored alias is linked whole, keeping its formatting.
	local function formatted(el)
		local entry = registry.prose[stringify(el)]
		if entry then
			return link({ el }, entry), false
		end
	end
	return {
		traverse = "topdown",
		Link = function(el)
			return el, false
		end,
		Div = without_term_hints,
		Span = function(el)
			if el.classes:includes("no-term-hints") then
				return without_term_hints(el)
			end
			if el.classes:includes("term-definition") then
				return el, false
			end
			if el.classes:includes("term-ref") then
				return link(el.content, reference(registry, "term-" .. (el.attributes.term or ""))), false
			end
		end,
		Math = function(el)
			return annotate_math(registry, max_tokens, own, el)
		end,
		Strong = formatted,
		Emph = formatted,
		Inlines = function(inlines)
			return link_phrases(phrases, inlines)
		end,
	}
end

local function annotate(registry, doc)
	local max_tokens, phrases = longest_math_alias(registry), prose_phrases(registry)
	local function first_mention_paragraph(block)
		local own = own_first_mention(registry, block)
		if own then
			return block:walk(annotation(registry, max_tokens, phrases, own)), false
		end
	end
	local handlers = annotation(registry, max_tokens, phrases, nil)
	handlers.Para, handlers.Plain = first_mention_paragraph, first_mention_paragraph
	return doc:walk(handlers)
end

-- Emission: landing sites and HTML preview cards for the entries that were used.

-- A first-mention paragraph keeps its anchor only if something links to it.
local function first_mention_anchors(registry, doc)
	return doc:walk({
		Span = function(el)
			local entry = registry.by_id[el.identifier]
			if not entry or entry.kind ~= "First mention" then
				return nil
			end
			if not entry.used then
				return {}
			end
			-- An anchor starting a block is set in vertical mode; in a
			-- table cell that drops the cell's text by a line.
			return latex and { pandoc.RawInline("latex", "\\leavevmode"), el } or nil
		end,
	})
end

-- A built-in notation entry has no authored landing site.
local function notation_reference(registry)
	local blocks = pandoc.Blocks({})
	for _, entry in ipairs(registry.ordered) do
		if entry.used and entry.builtin then
			blocks:insert(pandoc.Div({ pandoc.Para(entry.content) }, pandoc.Attr(entry.id)))
		end
	end
	if #blocks > 0 then
		blocks:insert(1, pandoc.Header(2, "Notation reference", pandoc.Attr("term-notation-reference")))
	end
	return blocks
end

local function packaged_text(name)
	local file = assert(io.open(pandoc.path.join({ directory, name }), "r"))
	local text = file:read("*a")
	file:close()
	return text
end

-- One `<template>` per used entry, with the hover card's style and script.
local function preview_cards(registry)
	local cards = {}
	for _, entry in ipairs(registry.ordered) do
		if entry.used then
			cards[#cards + 1] = '<template data-term-card="'
				.. entry.id
				.. '" data-term-kind="'
				.. entry.kind
				.. '">'
				.. pandoc.write(pandoc.Pandoc({ pandoc.Plain(entry.content) }), "html", { html_math_method = "mathjax" })
				.. "</template>"
		end
	end
	if #cards == 0 then
		return pandoc.Blocks({})
	end
	return pandoc.Blocks({
		pandoc.RawBlock(
			"html",
			table.concat(cards, "\n")
				.. "<style>"
				.. packaged_text("term_hints.css")
				.. "</style>"
				.. "<script>"
				.. packaged_text("term_hints.js")
				.. "</script>"
		),
	})
end

function Pandoc(doc)
	if not html and not latex then
		return doc
	end
	local registry = new_registry()
	register_definitions(registry, doc)
	if metadata_switch(doc.meta, "term-hints-operators", true) then
		register_default_operators(registry)
	end
	if metadata_switch(doc.meta, "term-hints-implicit", false) then
		doc = register_first_mentions(registry, doc)
	end
	doc = first_mention_anchors(registry, annotate(registry, doc))
	doc.blocks:extend(notation_reference(registry))
	if html then
		doc.blocks:extend(preview_cards(registry))
	end
	return doc
end
