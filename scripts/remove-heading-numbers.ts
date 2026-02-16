#!/usr/bin/env node
/**
 * Remove numbering from headings in QMD files.
 *
 * Patterns removed:
 *   ## 5. Title        -> ## Title
 *   ### 1) Title       -> ### Title
 *   ### A. Title       -> ### Title
 *   ### B) Title       -> ### Title
 *
 * Patterns preserved (NOT removed):
 *   ### Step 1: Title  (intentional step labels)
 *   ## 1972: Title     (years, not numbering)
 *
 * Usage:
 *   npx tsx scripts/remove-heading-numbers.ts [--dry-run] [--file <path>]
 */

import fs from 'fs/promises';
import * as fsSync from 'fs';
import path from 'path';
import { glob } from 'glob';
import { getProjectRoot } from './lib/file-utils';

const PROJECT_ROOT = getProjectRoot();

interface Options {
  dryRun: boolean;
  singleFile: string | null;
}

const EXCLUDE_PATTERNS = [
  '**/parameters-and-calculations*.qmd',
  '**/_build_temp/**',
  '**/_site/**',
  '**/_book/**',
  '**/node_modules/**',
  '**/.venv/**',
];


function parseArgs(): Options {
  const args = process.argv.slice(2);

  if (args.includes('--help') || args.includes('-h')) {
    console.log(`
Usage: npx tsx scripts/remove-heading-numbers.ts [options]

Options:
  --dry-run       Show what would be changed without making changes
  --file <path>   Process only a specific file (relative to project root)
  --help, -h      Show this help message
`);
    process.exit(0);
  }

  const fileIndex = args.indexOf('--file');
  let singleFile: string | null = null;
  if (fileIndex !== -1 && args[fileIndex + 1]) {
    singleFile = args[fileIndex + 1].replace(/\\/g, '/');
  }

  return {
    dryRun: args.includes('--dry-run'),
    singleFile,
  };
}

function processContent(content: string): { newContent: string; changes: string[] } {
  const changes: string[] = [];

  // Split frontmatter from content
  let frontmatter = '';
  let body = content;

  const fmMatch = content.match(/^---\r?\n([\s\S]*?\r?\n)---\r?\n/);
  if (fmMatch) {
    frontmatter = fmMatch[0];
    body = content.slice(frontmatter.length);
  }

  // Process line by line so we can show the full heading in logs
  const lines = body.split('\n');
  const newLines: string[] = [];

  // Matches numbered/lettered heading prefixes:
  //   ## 1. Title, ### 12) Title, ### 1: Title
  //   ### A. Title, ### B) Title
  //   ### B.1 Title, ### C.3 Title (compound labels)
  // Does NOT match 4-digit numbers (years like 1972)
  const lineRegex = /^(#{1,6}\s+)([A-Z]\.\d+\s+|\d{1,2}[\.\):\s]\s*|[A-Z][\.\)]\s*)(.*)/;

  for (const line of lines) {
    const match = line.match(lineRegex);
    if (match) {
      const [, hashes, , title] = match;
      const newLine = hashes + title;
      changes.push(`"${line.trim()}" -> "${newLine.trim()}"`);
      newLines.push(newLine);
    } else {
      newLines.push(line);
    }
  }

  return {
    newContent: frontmatter + newLines.join('\n'),
    changes,
  };
}

async function main() {
  const options = parseArgs();
  const modeLabel = options.dryRun ? ' [DRY RUN]' : '';

  console.log('='.repeat(70));
  console.log(`Remove Heading Numbers${modeLabel}`);
  console.log('='.repeat(70));

  let files: string[];

  if (options.singleFile) {
    const absolutePath = path.join(PROJECT_ROOT, options.singleFile);
    if (!fsSync.existsSync(absolutePath)) {
      console.error(`Error: File not found: ${options.singleFile}`);
      process.exit(1);
    }
    files = [absolutePath];
    console.log(`Processing single file: ${options.singleFile}\n`);
  } else {
    files = await glob('**/*.qmd', {
      cwd: PROJECT_ROOT,
      absolute: true,
      ignore: EXCLUDE_PATTERNS,
    });
    console.log(`Found ${files.length} QMD files\n`);
  }

  let totalChanges = 0;
  let filesModified = 0;

  for (const file of files) {
    const relativePath = path.relative(PROJECT_ROOT, file);
    const content = await fs.readFile(file, 'utf-8');
    const { newContent, changes } = processContent(content);

    if (changes.length > 0) {
      filesModified++;
      totalChanges += changes.length;
      console.log(`  ${relativePath}: ${changes.length} heading(s)`);
      for (const change of changes) {
        console.log(`    ${change}`);
      }

      if (!options.dryRun) {
        await fs.writeFile(file, newContent, 'utf-8');
      }
    }
  }

  console.log('\n' + '='.repeat(70));
  console.log(`Files processed:     ${files.length}`);
  console.log(`Files modified:      ${filesModified}`);
  console.log(`Headings renumbered: ${totalChanges}`);

  if (options.dryRun) {
    console.log('\nDRY RUN - No files were modified');
  }
  console.log('='.repeat(70));
}

main().catch((error) => {
  console.error('Error:', error instanceof Error ? error.message : String(error));
  process.exit(1);
});
