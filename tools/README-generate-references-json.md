# Generate References JSON

This script converts the Quarto references file ([brain/book/references.qmd](../brain/book/references.qmd)) into a structured JSON format.

## Usage

```bash
npm run generate:references-json
```

Or directly with tsx:

```bash
npx tsx scripts/generate-references-json.ts
```

## Input

- **Source**: `brain/book/references.qmd`
- **Format**: Quarto markdown file with YAML frontmatter and reference entries

## Output

- **Destination**: `brain/book/references.json`
- **Format**: Structured JSON with metadata and references array

## JSON Structure

```json
{
  "metadata": {
    "title": "📚 Source Quotes and References",
    "description": "...",
    "published": true,
    "tags": ["references", "sources", ...],
    "lastFormatted": "2025-10-16T00:00:00.000Z",
    ...
  },
  "references": [
    {
      "id": "reference-anchor-id",
      "title": "Reference title",
      "quotes": [
        "Quote text 1",
        "Quote text 2"
      ],
      "sources": [
        {
          "text": "Source name or title",
          "url": "https://example.com/source"
        }
      ],
      "notes": "Optional additional notes"
    }
  ]
}
```

## Features

- Parses YAML frontmatter (title, description, tags, etc.)
- Extracts reference IDs from HTML anchors
- Captures all quotes (lines starting with `>` but not `— `)
- Parses multiple sources separated by pipes (`|`)
- Extracts markdown links with optional prefix text (e.g., "GAO, 2025, [Link](url)")
- Captures notes when present (text after `| Note:`)
- Handles plain text sources without links

## Example Reference Parsing

Input (QMD):
```markdown
<a id="example-ref"></a>

- **Example Reference Title**
  > "This is a quote from the source."
  > — Organization, 2025, [Article Title](https://example.com) | Note: Additional context
```

Output (JSON):
```json
{
  "id": "example-ref",
  "title": "Example Reference Title",
  "quotes": ["\"This is a quote from the source.\""],
  "sources": [
    {
      "text": "Organization, 2025, Article Title",
      "url": "https://example.com"
    }
  ],
  "notes": "Additional context"
}
```

## Statistics

Current parsing results (as of last run):
- **536 references** parsed
- **1,939 total quotes** extracted
- **1,194 total sources** catalogued
