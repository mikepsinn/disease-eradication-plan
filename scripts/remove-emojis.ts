#!/usr/bin/env node
/**
 * Remove or replace emojis in QMD file content for EPUB compatibility.
 *
 * - Replaces semantic emojis with EPUB-safe equivalents (e.g. checkmark, thumbs up/down)
 * - Preserves standard Unicode symbols that render fine in EPUB (checkmark, ballot X, warning)
 * - Removes purely decorative emojis
 * - Skips YAML frontmatter
 *
 * Usage:
 *   npx tsx scripts/remove-emojis.ts [--dry-run] [--file <path>]
 *
 * Options:
 *   --dry-run    Show what would be changed without making changes
 *   --file       Process only a specific file
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

// EPUB-safe Unicode symbols to KEEP (not touch at all)
const KEEP_CHARS = new Set([
  '\u2713', // ✓ checkmark
  '\u2717', // ✗ ballot X
  '\u2716', // ✖ heavy multiplication X
  '\u2714', // ✔ heavy checkmark
  '\u2022', // • bullet
  '\u2026', // … ellipsis
]);

// Emojis to REPLACE with EPUB-safe text
const REPLACEMENTS: Record<string, string> = {
  '\u2705': '\u2713',  // ✅ → ✓
  '\u274C': '\u2717',  // ❌ → ✗
  '\u{1F44D}': '+1',   // 👍 → +1
  '\u{1F44E}': '-1',   // 👎 → -1
  '\u26A0': 'Warning', // ⚠ → Warning
};

// Match emoji characters (broad ranges covering most emoji)
const EMOJI_REGEX = /[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{1F1E0}-\u{1F1FF}\u{1F900}-\u{1F9FF}\u{1FA00}-\u{1FA6F}\u{1FA70}-\u{1FAFF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}\u{2300}-\u{23FF}\u{2B50}\u{2B55}\u{200D}\u{FE0F}\u{20E3}\u{E0020}-\u{E007F}]/gu;

function parseArgs(): Options {
  const args = process.argv.slice(2);

  if (args.includes('--help') || args.includes('-h')) {
    console.log(`
Usage: npx tsx scripts/remove-emojis.ts [options]

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

async function processFile(filePath: string, dryRun: boolean): Promise<{ replaced: number; removed: number }> {
  const content = await fs.readFile(filePath, 'utf-8');
  let replaced = 0;
  let removed = 0;

  // Split frontmatter from content - only process content
  let frontmatter = '';
  let body = content;

  const fmMatch = content.match(/^---\r?\n([\s\S]*?\r?\n)---\r?\n/);
  if (fmMatch) {
    frontmatter = fmMatch[0];
    body = content.slice(frontmatter.length);
  }

  const newBody = body.replace(EMOJI_REGEX, (match) => {
    // Keep EPUB-safe symbols untouched
    if (KEEP_CHARS.has(match)) return match;

    // Replace semantic emojis with text equivalents
    if (REPLACEMENTS[match] !== undefined) {
      replaced++;
      return REPLACEMENTS[match];
    }

    // Remove everything else
    removed++;
    return '';
  });

  const total = replaced + removed;
  if (total === 0) return { replaced: 0, removed: 0 };

  if (!dryRun) {
    await fs.writeFile(filePath, frontmatter + newBody, 'utf-8');
  }

  return { replaced, removed };
}

async function main() {
  const options = parseArgs();
  const modeLabel = options.dryRun ? ' [DRY RUN]' : '';

  console.log('='.repeat(70));
  console.log(`Remove Emojis${modeLabel}`);
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

  let totalReplaced = 0;
  let totalRemoved = 0;
  let filesModified = 0;

  for (const file of files) {
    const relativePath = path.relative(PROJECT_ROOT, file);
    const { replaced, removed } = await processFile(file, options.dryRun);
    const total = replaced + removed;

    if (total > 0) {
      filesModified++;
      totalReplaced += replaced;
      totalRemoved += removed;
      const parts = [];
      if (replaced > 0) parts.push(`${replaced} replaced`);
      if (removed > 0) parts.push(`${removed} removed`);
      console.log(`   ${relativePath}: ${parts.join(', ')}`);
    }
  }

  console.log('\n' + '='.repeat(70));
  console.log(`Files processed:   ${files.length}`);
  console.log(`Files modified:    ${filesModified}`);
  console.log(`Emojis replaced:   ${totalReplaced}`);
  console.log(`Emojis removed:    ${totalRemoved}`);

  if (options.dryRun) {
    console.log('\nDRY RUN - No files were modified');
  }
  console.log('='.repeat(70));
}

main().catch((error) => {
  console.error('Error:', error instanceof Error ? error.message : String(error));
  process.exit(1);
});
