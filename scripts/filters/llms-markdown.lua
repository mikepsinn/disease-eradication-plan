-- Markdown twins of rendered pages (scripts/lib/markdown_twins.py).
-- Runs after Quarto's own llms.lua filter.

-- Quarto writes TeX into span.math for MathJax. Pandoc's HTML reader keeps it
-- as text, and the markdown writer then garbles it. Make it real math.
function Span(span)
  if not span.classes:includes("math") then
    return nil
  end
  local tex = pandoc.utils.stringify(span)
  if span.classes:includes("display") then
    return pandoc.Math("DisplayMath", (tex:gsub("^%s*\\%[", ""):gsub("\\%]%s*$", "")))
  end
  return pandoc.Math("InlineMath", (tex:gsub("^%s*\\%(", ""):gsub("\\%)%s*$", "")))
end

-- Inline data: images are icons (ORCID and the like), not content.
function Image(image)
  if image.src:match("^data:") then
    return {}
  end
end

-- A link title is a hover tooltip: each parameter link carries a paragraph.
-- A link with no text and no image (an icon, or a data: image removed above)
-- goes too.
function Link(link)
  local has_image = false
  link.content:walk({ Image = function() has_image = true end })
  if not has_image and pandoc.utils.stringify(link.content):match("^%s*$") then
    return {}
  end
  link.title = ""
  return link
end
