-- Strip <a class="parameter-link"> and <span class="parameter-*"> HTML wrappers
-- for EPUB output. Keeps display text, removes link/span tags.
-- PDF doesn't need this (Pandoc drops raw HTML automatically for LaTeX).

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
