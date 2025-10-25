export interface Reference {
  id: string;
  title: string;
  quotes: string[];
  source: string;
}

/**
 * Parses the references.qmd content into structured Reference objects
 */
export function parseReferences(referencesContent: string): Reference[] {
  const references: Reference[] = [];
  const anchorRegex = /<a\s+id="([^"]+)"><\/a>/g;
  const blocks: Array<{ id: string; content: string }> = [];
  let lastIndex = 0;
  let match: RegExpExecArray | null;

  while ((match = anchorRegex.exec(referencesContent)) !== null) {
    if (blocks.length > 0) {
      blocks[blocks.length - 1].content = referencesContent.substring(lastIndex, match.index);
    }
    blocks.push({ id: match[1], content: '' });
    lastIndex = match.index + match[0].length;
  }

  if (blocks.length > 0) {
    blocks[blocks.length - 1].content = referencesContent.substring(lastIndex);
  }

  for (const block of blocks) {
    const lines = block.content.trim().split('\n');
    if (lines.length === 0) continue;

    const titleMatch = lines[0].match(/^-\s+\*\*(.+)\*\*$/);
    if (!titleMatch) {
      console.warn(`⚠ No title found for reference ${block.id}`);
      continue;
    }

    const title = titleMatch[1];
    const quotes: string[] = [];
    let source = '';
    let currentQuote = '';

    for (let i = 1; i < lines.length; i++) {
      const line = lines[i].trim();
      if (!line) {
        if (currentQuote) {
          quotes.push(currentQuote.trim());
          currentQuote = '';
        }
        continue;
      }
      if (line.startsWith('>')) {
        const content = line.substring(1).trim();
        if (content.startsWith('—')) {
          if (currentQuote) {
            quotes.push(currentQuote.trim());
            currentQuote = '';
          }
          const newSource = content.substring(1).trim();
          if (source && source !== newSource) {
            source += ' | ' + newSource;
          } else if (!source) {
            source = newSource;
          }
        } else {
          if (currentQuote) {
            currentQuote += '\n' + content;
          } else {
            currentQuote = content;
          }
        }
      } else if (currentQuote && !line.startsWith('<') && !line.startsWith('-')) {
        currentQuote += '\n' + line;
      }
    }
    if (currentQuote) {
      quotes.push(currentQuote.trim());
    }
    references.push({
      id: block.id,
      title,
      quotes,
      source: source || '<!-- TODO: Add source URL -->'
    });
  }

  const seenIds = new Map<string, number>();
  const uniqueRefs: Reference[] = [];
  for (const ref of references) {
    if (seenIds.has(ref.id)) {
      console.warn(`⚠ Duplicate reference ID "${ref.id}" - merging`);
      const existingIndex = seenIds.get(ref.id)!;
      const existing = uniqueRefs[existingIndex];
      existing.quotes.push(...ref.quotes);
      if (ref.source && ref.source !== existing.source) {
        existing.source += ' | ' + ref.source;
      }
    } else {
      seenIds.set(ref.id, uniqueRefs.length);
      uniqueRefs.push(ref);
    }
  }
  return uniqueRefs;
}

/**
 * Formats references into the standard references.qmd file format
 */
export function formatReferencesFile(references: Reference[], frontmatter: string): string {
  const sorted = references.sort((a, b) => a.id.localeCompare(b.id));
  let output = frontmatter + '\n\n';
  for (const ref of sorted) {
    output += `<a id="${ref.id}"></a>\n`;
    output += `- **${ref.title}**\n`;
    for (const quote of ref.quotes) {
      const quoteLines = quote.split('\n');
      for (const line of quoteLines) {
        output += `  > ${line}\n`;
      }
    }
    output += `  > — ${ref.source}\n\n`;
  }
  return output.trimEnd() + '\n';
}
