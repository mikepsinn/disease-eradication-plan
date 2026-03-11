local paper_type = nil
local site_url = nil
local doi = nil

local function stringify(value)
  if not value then
    return nil
  end

  local text = pandoc.utils.stringify(value)
  if text == "" then
    return nil
  end

  return text
end

local function get_nested(value, keys)
  local current = value
  for _, key in ipairs(keys) do
    if type(current) ~= "table" then
      return nil
    end

    current = current[key]
    if current == nil then
      return nil
    end
  end

  return current
end

local function build_html_note()
  local inlines = {
    pandoc.Strong({ pandoc.Str("Version"), pandoc.Space(), pandoc.Str("note.") }),
    pandoc.Space(),
    pandoc.Str("This"),
    pandoc.Space(),
    pandoc.Str("website"),
    pandoc.Space(),
    pandoc.Str("is"),
    pandoc.Space(),
    pandoc.Str("the"),
    pandoc.Space(),
    pandoc.Str("maintained"),
    pandoc.Space(),
    pandoc.Str("interactive"),
    pandoc.Space(),
    pandoc.Str("version"),
    pandoc.Space(),
    pandoc.Str("of"),
    pandoc.Space(),
    pandoc.Str("this"),
    pandoc.Space(),
    pandoc.Str("paper."),
  }

  if doi then
    table.insert(inlines, pandoc.Space())
    table.insert(inlines, pandoc.Str("Citable"))
    table.insert(inlines, pandoc.Space())
    table.insert(inlines, pandoc.Str("archival"))
    table.insert(inlines, pandoc.Space())
    table.insert(inlines, pandoc.Str("snapshot:"))
    table.insert(inlines, pandoc.Space())
    table.insert(inlines, pandoc.Link({ pandoc.Str("https://doi.org/" .. doi) }, "https://doi.org/" .. doi))
    table.insert(inlines, pandoc.Str("."))
  end

  return pandoc.Div({ pandoc.Para(inlines) }, pandoc.Attr("", { "version-note" }))
end

local function build_archive_note()
  local inlines = {
    pandoc.Strong({ pandoc.Str("Version"), pandoc.Space(), pandoc.Str("note.") }),
    pandoc.Space(),
    pandoc.Str("This"),
    pandoc.Space(),
    pandoc.Str("document"),
    pandoc.Space(),
    pandoc.Str("is"),
    pandoc.Space(),
    pandoc.Str("an"),
    pandoc.Space(),
    pandoc.Str("archival"),
    pandoc.Space(),
    pandoc.Str("snapshot."),
    pandoc.Space(),
    pandoc.Str("Latest"),
    pandoc.Space(),
    pandoc.Str("interactive"),
    pandoc.Space(),
    pandoc.Str("version:"),
    pandoc.Space(),
    pandoc.Link({ pandoc.Str(site_url) }, site_url),
    pandoc.Str("."),
  }

  if doi then
    table.insert(inlines, pandoc.Space())
    table.insert(inlines, pandoc.Str("Citable"))
    table.insert(inlines, pandoc.Space())
    table.insert(inlines, pandoc.Str("DOI:"))
    table.insert(inlines, pandoc.Space())
    table.insert(inlines, pandoc.Link({ pandoc.Str("https://doi.org/" .. doi) }, "https://doi.org/" .. doi))
    table.insert(inlines, pandoc.Str("."))
  end

  return pandoc.Div({ pandoc.Para(inlines) }, pandoc.Attr("", { "version-note" }))
end

function Meta(meta)
  paper_type = stringify(meta.type)
    or stringify(get_nested(meta, { "metadata", "type" }))
  site_url = stringify(get_nested(meta, { "publishing", "own-site", "url" }))
    or stringify(get_nested(meta, { "metadata", "publishing", "own-site", "url" }))
    or stringify(get_nested(meta, { "website", "site-url" }))
    or stringify(get_nested(meta, { "book", "site-url" }))
  doi = stringify(meta.doi)
    or stringify(get_nested(meta, { "metadata", "doi" }))
  return meta
end

function Pandoc(doc)
  if paper_type ~= "Academic" or not site_url then
    return doc
  end

  local note = nil
  if FORMAT:match("html") then
    note = build_html_note()
  elseif FORMAT:match("latex") then
    note = build_archive_note()
  else
    return doc
  end

  table.insert(doc.blocks, 1, note)
  return doc
end
