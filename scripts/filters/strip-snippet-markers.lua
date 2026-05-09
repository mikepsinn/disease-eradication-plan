-- Remove source-only snippet boundary comments from rendered outputs.
-- The QMD markers are used by the TypeScript/JSON snippet generator.

local function is_snippet_marker(text)
  return text:match("^%s*<!%-%-%s*/?snippet:[%w_%-]+%s*%-%->%s*$") ~= nil
end

function RawBlock(el)
  if el.format == "html" and is_snippet_marker(el.text) then
    return {}
  end
end

function RawInline(el)
  if el.format == "html" and is_snippet_marker(el.text) then
    return {}
  end
end
