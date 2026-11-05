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

function Pandoc(doc)
	if not html and not latex then
		return doc
	end
	if doc.meta["term-hints-processed"] then
		return doc
	end
	doc.meta["term-hints-processed"] = true
	local implicit = doc.meta["term-hints-implicit"] == true
		or stringify(doc.meta["term-hints-implicit"] or "") == "true"
	local registry, math_aliases, prose_aliases, ordered = {}, {}, {}, {}

	local function register(id, content, kind, maths, prose, class)
		if not id:match("^term%-%a[%w%-]*$") then
			fail("definition ID must be term-<name>: " .. id)
		end
		if registry[id] then
			fail("duplicate definition " .. id)
		end
		local preview = pandoc.Span(content):walk({
			Math = function(el)
				el.text = unmarked_math(el.text)
				return el
			end,
		}).content
		local entry = { id = id, content = preview, kind = kind, class = class }
		registry[id], ordered[#ordered + 1] = entry, entry
		for _, pair in ipairs({ { math_aliases, maths }, { prose_aliases, prose } }) do
			for _, alias in ipairs(pair[2]) do
				if pair[1][alias] then
					fail("ambiguous alias " .. alias .. "; use explicit termref markers")
				end
				pair[1][alias] = entry
			end
		end
		return entry
	end

	doc:walk({
		Span = function(span)
			if span.classes:includes("term-definition") then
				register(
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
	if doc.meta["term-hints-operators"] ~= false and stringify(doc.meta["term-hints-operators"] or "") ~= "false" then
		for i, item in ipairs(defaults) do
			if not math_aliases[item[1]] then
				local entry = register(
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

	local count = 0
	local function discover(block)
		if not implicit then
			return
		end
		local found = {}
		local function add(alias, mapping)
			if not mapping[alias] then
				count = count + 1
				local entry = register(
					"term-first-" .. count,
					block.content,
					"First mention",
					mapping == math_aliases and { alias } or {},
					mapping == prose_aliases and { alias } or {}
				)
				found[#found + 1] = entry.id
			end
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
					if token.symbol then
						add(token.text, math_aliases)
					end
				end
			end,
			Str = function(el)
				for _, code in utf8.codes(el.text) do
					if (code >= 0x2100 and code <= 0x22ff) or (code >= 0x1d400 and code <= 0x1d7ff) then
						add(utf8.char(code), prose_aliases)
					end
				end
			end,
			Strong = function(el)
				add(stringify(el), prose_aliases)
			end,
			Emph = function(el)
				add(stringify(el), prose_aliases)
			end,
		})
		if #found > 0 then
			local anchors = pandoc.Inlines({})
			for _, id in ipairs(found) do
				anchors:insert(pandoc.Span({}, pandoc.Attr(id)))
			end
			anchors:extend(block.content)
			block.content = anchors
			return block
		end
	end
	doc = doc:walk({
		traverse = "topdown",
		Para = discover,
		Plain = discover,
		Div = function(el)
			if el.classes:includes("no-term-hints") then
				return el, false
			end
		end,
	})

	local function reference(id)
		local entry = registry[id]
		if not entry then
			fail("unknown reference " .. id)
		end
		entry.used = true
		return entry
	end

	local function math_link(entry, text, script)
		entry.used = true
		local result = html and ("\\href{#" .. entry.id .. "}{" .. text .. "}")
			or ("\\hyperref[" .. entry.id .. "]{" .. text .. "}")
		if entry.class then
			if
				not ({
					ord = true,
					op = true,
					bin = true,
					rel = true,
					open = true,
					close = true,
					punct = true,
					inner = true,
				})[entry.class]
			then
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

	local max_tokens = 1
	for alias in pairs(math_aliases) do
		max_tokens = math.max(max_tokens, #tokens(alias))
	end
	local function annotate_math(el)
		local source, out, i = tokens(el.text), {}, 1
		while i <= #source do
			local token = source[i]
			local previous = i - 1
			while previous > 0 and source[previous].text:match("^%s+$") do
				previous = previous - 1
			end
			local script = previous > 0 and (source[previous].text == "_" or source[previous].text == "^")
			if token.id then
				out[#out + 1] = math_link(reference("term-" .. token.id), unmarked_math(token.body), script)
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
					if math_aliases[candidate] then
						best, last, spelling = math_aliases[candidate], j, candidate
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
	local function formatted(el)
		local entry = prose_aliases[stringify(el)]
		if entry then
			return link({ el }, entry), false
		end
	end
	-- Match phrases across ordinary prose tokens without changing their formatting.
	local phrases = {}
	for alias, entry in pairs(prose_aliases) do
		phrases[#phrases + 1] = { text = alias, entry = entry }
	end
	table.sort(phrases, function(a, b)
		return #a.text > #b.text
	end)
	local function prose(inlines)
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
	local function ignore(el)
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
	doc = doc:walk({
		traverse = "topdown",
		Link = function(el)
			return el, false
		end,
		Div = ignore,
		Span = function(el)
			if el.classes:includes("no-term-hints") then
				return ignore(el)
			end
			if el.classes:includes("term-definition") then
				return el, false
			end
			if el.classes:includes("term-ref") then
				return link(el.content, reference("term-" .. (el.attributes.term or ""))), false
			end
		end,
		Math = annotate_math,
		Strong = formatted,
		Emph = formatted,
		Inlines = prose,
	})

	-- A built-in notation entry has no authored landing site. Emit only used entries.
	local builtin_blocks = pandoc.Blocks({})
	for _, entry in ipairs(ordered) do
		if entry.used and entry.builtin then
			builtin_blocks:insert(pandoc.Div({ pandoc.Para(entry.content) }, pandoc.Attr(entry.id)))
		end
	end
	if #builtin_blocks > 0 then
		builtin_blocks:insert(1, pandoc.Header(2, "Notation reference", pandoc.Attr("term-notation-reference")))
		doc.blocks:extend(builtin_blocks)
	end
	if html then
		local cards = {}
		for _, entry in ipairs(ordered) do
			if entry.used then
				cards[#cards + 1] = '<template data-term-card="'
					.. entry.id
					.. '" data-term-kind="'
					.. entry.kind
					.. '">'
					.. pandoc.write(
						pandoc.Pandoc({ pandoc.Plain(entry.content) }),
						"html",
						{ html_math_method = "mathjax" }
					)
					.. "</template>"
			end
		end
		if #cards > 0 then
			local function read(name)
				local file = assert(io.open(pandoc.path.join({ directory, name }), "r"))
				local text = file:read("*a")
				file:close()
				return text
			end
			doc.blocks:insert(
				pandoc.RawBlock(
					"html",
					table.concat(cards, "\n")
						.. "<style>"
						.. read("term_hints.css")
						.. "</style>"
						.. "<script>"
						.. read("term_hints.js")
						.. "</script>"
				)
			)
		end
	end
	return doc
end
