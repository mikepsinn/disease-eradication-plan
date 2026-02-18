-- EPUB transforms: author override, parameter link stripping, emoji replacement,
-- and figure caption reordering. Only runs for EPUB builds.
-- PDF doesn't need this (Pandoc drops raw HTML automatically for LaTeX).

-- Override author metadata for EPUB title page and OPF.
-- Book-level YAML keeps Mike P. Sinn for HTML; this filter swaps to WISHONIA for EPUB only.
function Meta(meta)
  meta.author = pandoc.MetaList({
    pandoc.MetaInlines({pandoc.Str("By"), pandoc.Space(), pandoc.Str("WISHONIA")}),
    pandoc.MetaInlines({pandoc.Str("Translated"), pandoc.Space(), pandoc.Str("by"), pandoc.Space(), pandoc.Str("Mike"), pandoc.Space(), pandoc.Str("P."), pandoc.Space(), pandoc.Str("Sinn")})
  })
  return meta
end

-- Emoji replacements for e-reader compatibility.
-- E-readers lack emoji fonts, so these render as empty boxes.
local emoji_map = {
  ["\u{2705}"] = "[YES]",   -- ✅
  ["\u{274C}"] = "[NO]",    -- ❌
  ["\u{274E}"] = "[NO]",    -- ❎
  ["\u{2714}"] = "[OK]",    -- ✔
  ["\u{2716}"] = "[X]",     -- ✖
  ["\u{2611}"] = "[x]",     -- ☑
  ["\u{2610}"] = "[ ]",     -- ☐
  ["\u{26A0}"] = "[!]",     -- ⚠
  ["\u{1F4A1}"] = "[TIP]",  -- 💡
  ["\u{1F4DD}"] = "[NOTE]", -- 📝
  ["\u{1F6A8}"] = "[!]",    -- 🚨
  ["\u{1F4CA}"] = "",        -- 📊 (decorative, in parameter headers)
  ["\u{1F4C8}"] = "",        -- 📈
  ["\u{1F4C9}"] = "",        -- 📉
  ["\u{1F4B0}"] = "",        -- 💰
  ["\u{1F4B5}"] = "",        -- 💵
  ["\u{1F52C}"] = "",        -- 🔬
  ["\u{1F30D}"] = "",        -- 🌍
  ["\u{1F680}"] = "",        -- 🚀
  ["\u{1F3AF}"] = "",        -- 🎯
  ["\u{1F3C6}"] = "",        -- 🏆
  ["\u{2728}"]  = "",        -- ✨
  ["\u{1F525}"] = "",        -- 🔥
  ["\u{1F3E5}"] = "",        -- 🏥
  ["\u{1F3E6}"] = "",        -- 🏦
}

-- Replace emoji in Str elements with text equivalents.
function Str(el)
  local text = el.text
  local changed = false
  for emoji, replacement in pairs(emoji_map) do
    if text:find(emoji, 1, true) then
      text = text:gsub(emoji, replacement)
      changed = true
    end
  end
  if changed then
    return pandoc.Str(text)
  end
end

-- Strip <a class="parameter-link"> and <span class="parameter-*"> HTML wrappers.
-- Keeps display text, removes link/span tags.
function Inlines(inlines)
  local result = pandoc.List()
  local in_param_a = false
  local in_param_span = false

  for _, el in ipairs(inlines) do
    if el.t == "RawInline" and el.format == "html" then
      if el.text:match('<a[^>]*class="parameter%-link"') then
        in_param_a = true
      elseif in_param_a and el.text:match('</a>') then
        in_param_a = false
      elseif el.text:match('<span[^>]*class="parameter%-') then
        in_param_span = true
      elseif in_param_span and el.text:match('</span>') then
        in_param_span = false
      else
        result:insert(el)
      end
    else
      result:insert(el)
    end
  end

  return result
end

-- Strip .qmd internal links that don't resolve in EPUB.
-- Keep the link text, remove the link target.
function Link(el)
  if el.target:match("%.qmd") then
    return el.content
  end
  -- Fix backslash in URLs (Windows path separators)
  if el.target:match("\\") then
    el.target = el.target:gsub("\\", "/")
    return el
  end
end

-- Move figure captions below images.
-- Pandoc's EPUB writer puts <figcaption> before <img> in the XHTML.
-- This reconstructs the figure HTML with caption after content.
-- Note: Quarto may handle this natively (quarto-float-caption-bottom),
-- but this filter ensures correct order regardless.
function Figure(fig)
  local caption = fig.caption
  if not caption or not caption.long or #caption.long == 0 then return end

  local id = fig.attr.identifier or ""
  local id_attr = id ~= "" and (' id="' .. id .. '"') or ""

  local blocks = pandoc.List()
  blocks:insert(pandoc.RawBlock("html", "<figure" .. id_attr .. ">"))

  -- Image content first
  for _, block in ipairs(fig.content) do
    blocks:insert(block)
  end

  -- Caption after
  blocks:insert(pandoc.RawBlock("html", "<figcaption>"))
  for _, block in ipairs(caption.long) do
    blocks:insert(block)
  end
  blocks:insert(pandoc.RawBlock("html", "</figcaption>"))

  blocks:insert(pandoc.RawBlock("html", "</figure>"))

  return blocks
end
