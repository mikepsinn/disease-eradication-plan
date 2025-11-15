#!/usr/bin/env node
/**
 * Generate JSON references file from references.qmd
 *
 * Parses brain/book/references.qmd and converts it to a structured JSON format
 * Usage: npx tsx scripts/generate-references-json.ts
 */

import * as fs from 'fs';
import * as path from 'path';

interface Reference {
  id: string;
  title: string;
  quotes: string[];
  sources: Array<{
    text: string;
    url?: string;
  }>;
  notes?: string;
}

interface ReferencesData {
  metadata: {
    title: string;
    description: string;
    published: boolean;
    tags: string[];
    lastFormatted?: string;
    lastStyleCheck?: string;
    lastFormattedHash?: string;
    lastFactCheckHash?: string;
    lastStructureCheckHash?: string;
  };
  references: Reference[];
}

function parseYamlFrontmatter(content: string): { metadata: any; bodyStart: number } {
  const yamlMatch = content.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n/);
  if (!yamlMatch) {
    return { metadata: {}, bodyStart: 0 };
  }

  const yamlContent = yamlMatch[1];
  const metadata: any = {};

  let currentKey: string | null = null;
  let currentArray: string[] = [];

  yamlContent.split(/\r?\n/).forEach(line => {
    if (line.match(/^(\w+):/)) {
      // Save previous array if exists
      if (currentKey && currentArray.length > 0) {
        metadata[currentKey] = currentArray;
        currentArray = [];
        currentKey = null;
      }

      const colonIndex = line.indexOf(':');
      currentKey = line.substring(0, colonIndex).trim();
      const value = line.substring(colonIndex + 1).trim();

      if (value) {
        // Handle boolean
        if (value === 'true') {
          metadata[currentKey] = true;
          currentKey = null;
        } else if (value === 'false') {
          metadata[currentKey] = false;
          currentKey = null;
        } else {
          metadata[currentKey] = value;
          currentKey = null;
        }
      }
      // If value is empty, currentKey stays set for array collection
    } else if (line.trim().startsWith('- ') && currentKey) {
      // Array item
      currentArray.push(line.trim().substring(2));
    }
  });

  // Save last array if exists
  if (currentKey && currentArray.length > 0) {
    metadata[currentKey] = currentArray;
  }

  return { metadata, bodyStart: yamlMatch[0].length };
}

function parseReferences(content: string): Reference[] {
  const references: Reference[] = [];

  // Split by anchor tags
  const anchorRegex = /<a id="([^"]+)"><\/a>/g;
  const parts = content.split(anchorRegex);

  // Skip first part (before first anchor)
  for (let i = 1; i < parts.length; i += 2) {
    const id = parts[i];
    const refContent = parts[i + 1];

    if (!refContent || !refContent.trim()) continue;

    // Extract the bullet point content
    const bulletMatch = refContent.match(/^\s*-\s+\*\*(.*?)\*\*/m);
    if (!bulletMatch) continue;

    const title = bulletMatch[1].trim();

    // Extract quotes (lines starting with >)
    const quotes: string[] = [];
    const quoteRegex = /^\s*>\s*(.+)$/gm;
    let quoteMatch;

    while ((quoteMatch = quoteRegex.exec(refContent)) !== null) {
      const quoteLine = quoteMatch[1].trim();
      // Skip source lines (starting with —)
      if (!quoteLine.startsWith('—')) {
        quotes.push(quoteLine);
      }
    }

    // Extract sources (lines with —) and notes
    const sources: Array<{ text: string; url?: string }> = [];
    let notes: string | undefined;
    const sourceRegex = /^\s*>\s*—\s*(.+)$/gm;
    let sourceMatch;

    while ((sourceMatch = sourceRegex.exec(refContent)) !== null) {
      const fullSourceLine = sourceMatch[1].trim();

      // Split by pipe to get individual parts
      const parts = fullSourceLine.split('|').map(p => p.trim());

      // Process each part
      parts.forEach(part => {
        // Check if this part is a note
        if (part.toLowerCase().startsWith('note:')) {
          notes = part.substring(5).trim(); // Remove "Note:" prefix
          return;
        }

        // Parse markdown links in this part: [text](url)
        const linkRegex = /\[([^\]]+)\]\(([^\)]+)\)/g;
        const matches: Array<{ text: string; url: string; index: number }> = [];
        let linkMatch;

        while ((linkMatch = linkRegex.exec(part)) !== null) {
          matches.push({
            text: linkMatch[1],
            url: linkMatch[2],
            index: linkMatch.index
          });
        }

        if (matches.length > 0) {
          // For each link, check if there's prefix text before it
          matches.forEach((match, i) => {
            const startIndex = i === 0 ? 0 : matches[i - 1].index + part.substring(matches[i - 1].index).indexOf(')') + 1;
            const prefix = part.substring(startIndex, match.index).trim();

            // Combine prefix with link text if prefix exists
            const fullText = prefix ? `${prefix} ${match.text}` : match.text;

            sources.push({
              text: fullText.replace(/,\s*$/, '').trim(), // Remove trailing comma
              url: match.url
            });
          });
        } else if (part) {
          // Plain text source
          sources.push({ text: part });
        }
      });
    }

    references.push({
      id,
      title,
      quotes,
      sources,
      ...(notes && { notes })
    });
  }

  return references;
}

function main() {
  const referencesPath = path.join(process.cwd(), 'brain', 'book', 'references.qmd');
  const outputPath = path.join(process.cwd(), 'brain', 'book', 'references.json');

  console.log('Reading references.qmd...');
  const content = fs.readFileSync(referencesPath, 'utf-8');

  console.log('Parsing YAML frontmatter...');
  const { metadata, bodyStart } = parseYamlFrontmatter(content);

  console.log('Parsing references...');
  const body = content.substring(bodyStart);
  const references = parseReferences(body);

  const data: ReferencesData = {
    metadata,
    references
  };

  console.log(`Found ${references.length} references`);

  console.log('Writing JSON file...');
  fs.writeFileSync(outputPath, JSON.stringify(data, null, 2), 'utf-8');

  console.log(`✓ Successfully generated ${outputPath}`);
  console.log(`  - ${references.length} references`);
  console.log(`  - ${references.reduce((sum, ref) => sum + ref.quotes.length, 0)} total quotes`);
  console.log(`  - ${references.reduce((sum, ref) => sum + ref.sources.length, 0)} total sources`);
}

main();
