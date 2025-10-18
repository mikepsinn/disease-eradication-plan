#!/usr/bin/env tsx

import * as fs from 'fs';
import * as path from 'path';

/**
 * Script to extract references without URLs from references.qmd
 * Outputs to references-to-update.md for manual URL addition
 */

const REFERENCES_FILE = path.join(process.cwd(), 'brain', 'book', 'references.qmd');
const OUTPUT_FILE = path.join(process.cwd(), 'references-to-update.md');

interface Reference {
  id: string;
  title: string;
  quote: string;
  source: string;
  lineStart: number;
  lineEnd: number;
  rawContent: string;
}

function extractReferences(): Reference[] {
  const content = fs.readFileSync(REFERENCES_FILE, 'utf-8');
  const lines = content.split('\n');

  const references: Reference[] = [];
  let i = 0;

  // Skip YAML frontmatter
  if (lines[0].trim() === '---') {
    i = 1;
    while (i < lines.length && lines[i].trim() !== '---') {
      i++;
    }
    i++; // Skip closing ---
  }

  // Skip empty lines after frontmatter
  while (i < lines.length && lines[i].trim() === '') {
    i++;
  }

  while (i < lines.length) {
    const line = lines[i];

    // Look for anchor tags: <a id="..."></a>
    if (line.match(/^<a id="[^"]+"><\/a>$/)) {
      const idMatch = line.match(/^<a id="([^"]+)"><\/a>$/);
      if (!idMatch) {
        i++;
        continue;
      }

      const id = idMatch[1];
      const lineStart = i;
      let currentLine = i + 1;
      let rawContent = line + '\n';

      // Next line should be a bullet point with title
      if (currentLine >= lines.length || !lines[currentLine].match(/^- \*\*/)) {
        i++;
        continue;
      }

      const titleMatch = lines[currentLine].match(/^- \*\*([^*]+)\*\*/);
      if (!titleMatch) {
        i++;
        continue;
      }

      const title = titleMatch[1];
      rawContent += lines[currentLine] + '\n';
      currentLine++;

      // Collect all quote/source lines (lines starting with > or "Alternative title:")
      const allLines: string[] = [];
      while (currentLine < lines.length &&
             (lines[currentLine].trim().startsWith('>') ||
              lines[currentLine].trim().startsWith('Alternative title:'))) {
        rawContent += lines[currentLine] + '\n';
        allLines.push(lines[currentLine]);
        currentLine++;
      }

      if (allLines.length === 0) {
        i++;
        continue;
      }

      // The last line starting with > should be the source (contains —)
      // Everything before that is the quote
      let sourceLineIdx = allLines.length - 1;
      for (let j = allLines.length - 1; j >= 0; j--) {
        if (allLines[j].trim().startsWith('>') && allLines[j].includes('—')) {
          sourceLineIdx = j;
          break;
        }
      }

      const quoteLines = allLines.slice(0, sourceLineIdx).filter(l => l.trim().startsWith('>'));
      const sourceLine = allLines[sourceLineIdx];

      const quote = quoteLines.map(l => l.replace(/^\s*>\s*/, '')).join(' ').trim();
      const source = sourceLine.trim().replace(/^>\s*—\s*/, '');

      // Skip empty line after reference
      if (currentLine < lines.length && lines[currentLine].trim() === '') {
        rawContent += lines[currentLine] + '\n';
        currentLine++;
      }

      const lineEnd = currentLine - 1;

      // Check if this reference has a TODO comment or no URL
      const hasTodo = source.includes('<!-- TODO:');
      const hasNoUrl = !source.match(/\[.*\]\(http/) && !source.match(/https?:\/\//);

      if (hasTodo || hasNoUrl) {
        references.push({
          id,
          title,
          quote,
          source,
          lineStart,
          lineEnd,
          rawContent: rawContent.trimEnd()
        });
      }

      i = currentLine;
    } else {
      i++;
    }
  }

  return references;
}

function generateOutputFile(references: Reference[]): void {
  let output = `# References Without URLs - To Update

This file contains ${references.length} references that need URLs added.

## Instructions:
1. For each reference below, add the URL after "NEW URL:"
2. If you can't find a URL, add a note explaining why
3. Once complete, run the integration script to merge these back into references.qmd

---

`;

  references.forEach((ref, index) => {
    output += `## ${index + 1}. ${ref.title}\n\n`;
    output += `**ID:** \`${ref.id}\`\n\n`;
    output += `**Quote:**\n> ${ref.quote}\n\n`;
    output += `**Current Source:**\n> ${ref.source}\n\n`;
    output += `**NEW URL:** \n\n`;
    output += `---\n\n`;
  });

  fs.writeFileSync(OUTPUT_FILE, output, 'utf-8');
  console.log(`✓ Extracted ${references.length} references without URLs`);
  console.log(`✓ Output written to: ${OUTPUT_FILE}`);

  // Also save as JSON for the integration script
  const jsonFile = OUTPUT_FILE.replace('.md', '.json');
  fs.writeFileSync(jsonFile, JSON.stringify(references, null, 2), 'utf-8');
  console.log(`✓ Reference data saved to: ${jsonFile}`);
}

// Main execution
try {
  console.log('Extracting references without URLs...\n');
  const references = extractReferences();
  generateOutputFile(references);

  console.log('\n📋 Summary:');
  console.log(`   Total references needing URLs: ${references.length}`);
  console.log('\n📝 Next steps:');
  console.log('   1. Open references-to-update.md');
  console.log('   2. Add URLs for each reference');
  console.log('   3. Run: npm run integrate-references');
} catch (error) {
  console.error('Error:', error);
  process.exit(1);
}
