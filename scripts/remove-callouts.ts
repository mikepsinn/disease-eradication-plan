#!/usr/bin/env node
/**
 * Remove Quarto callouts from QMD files and convert to regular sections
 *
 * Converts patterns like:
 *   ::: {.callout-note}
 *   ## Title
 *   Content
 *   :::
 *
 * To:
 *   ## Title
 *   Content
 *
 * And:
 *   ::: {.callout-warning title="My Warning"}
 *   Content
 *   :::
 *
 * To:
 *   ### My Warning
 *   Content
 *
 * Usage:
 *   npx tsx scripts/remove-callouts.ts [--dry-run] [--file <path>]
 *
 * Options:
 *   --dry-run    Show what would be changed without making changes
 *   --file       Process only a specific file
 *   --verbose    Show detailed output for each file
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
  verbose: boolean;
}

interface ConversionStats {
  filesProcessed: number;
  filesModified: number;
  calloutsRemoved: number;
  fileDetails: { file: string; count: number }[];
}

// Files/patterns to exclude (auto-generated)
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
Usage: npx tsx scripts/remove-callouts.ts [options]

Options:
  --dry-run       Show what would be changed without making changes
  --file <path>   Process only a specific file (relative to project root)
  --verbose       Show detailed output for each file
  --help, -h      Show this help message

Examples:
  npx tsx scripts/remove-callouts.ts --dry-run
  npx tsx scripts/remove-callouts.ts --file knowledge/appendix/dfda-impact-paper.qmd --dry-run
  npx tsx scripts/remove-callouts.ts --verbose
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
    verbose: args.includes('--verbose'),
  };
}

/**
 * Convert a callout type to a header prefix (optional - for callouts without titles)
 */
function calloutTypeToPrefix(type: string): string {
  const prefixes: Record<string, string> = {
    'note': 'Note',
    'tip': 'Tip',
    'warning': 'Warning',
    'caution': 'Caution',
    'important': 'Important',
  };
  return prefixes[type] || 'Note';
}

/**
 * Process a single file and remove callouts
 */
async function processFile(
  filePath: string,
  dryRun: boolean,
  verbose: boolean
): Promise<number> {
  const content = await fs.readFile(filePath, 'utf-8');
  let newContent = content;
  let calloutsRemoved = 0;

  // Regex to match callout blocks
  // Matches: ::: {.callout-TYPE ...attributes...}\n...content...\n:::
  const calloutRegex = /^([ \t]*)::: \{\.callout-([a-z]+)([^}]*)\}\s*\n([\s\S]*?)^\1:::\s*$/gm;

  newContent = content.replace(calloutRegex, (match, indent, type, attributes, innerContent) => {
    calloutsRemoved++;

    // Extract title from attributes if present
    const titleMatch = attributes.match(/title\s*=\s*["']([^"']+)["']/);
    let title = titleMatch ? titleMatch[1] : null;

    // Check if inner content starts with a header
    const headerMatch = innerContent.match(/^(#{1,6})\s+(.+)\n/);

    let result = '';

    if (headerMatch) {
      // Content already has a header - just remove the callout wrapper
      result = innerContent.trim();
    } else if (title) {
      // Use the title attribute as a header
      // Determine header level - use ### for callout titles (one level deeper than typical sections)
      result = `### ${title}\n\n${innerContent.trim()}`;
    } else {
      // No title - check if content starts with **Bold**: pattern
      const boldMatch = innerContent.match(/^\*\*([^*]+)\*\*:\s*/);
      if (boldMatch) {
        // Convert **Bold**: to a header
        const boldTitle = boldMatch[1];
        const restContent = innerContent.replace(/^\*\*[^*]+\*\*:\s*/, '');
        result = `### ${boldTitle}\n\n${restContent.trim()}`;
      } else {
        // No title at all - add a generic one based on callout type
        const prefix = calloutTypeToPrefix(type);
        result = `### ${prefix}\n\n${innerContent.trim()}`;
      }
    }

    // Preserve indentation if any
    if (indent) {
      result = result.split('\n').map(line => indent + line).join('\n');
    }

    if (verbose) {
      console.log(`   Converted ${type} callout${title ? ` "${title}"` : ''}`);
    }

    return '\n' + result + '\n';
  });

  // Also handle nested callouts (:::: with 4 colons)
  const nestedCalloutRegex = /^([ \t]*):::: \{\.callout-([a-z]+)([^}]*)\}\s*\n([\s\S]*?)^\1::::\s*$/gm;

  newContent = newContent.replace(nestedCalloutRegex, (match, indent, type, attributes, innerContent) => {
    calloutsRemoved++;

    const titleMatch = attributes.match(/title\s*=\s*["']([^"']+)["']/);
    let title = titleMatch ? titleMatch[1] : null;

    const headerMatch = innerContent.match(/^(#{1,6})\s+(.+)\n/);

    let result = '';

    if (headerMatch) {
      result = innerContent.trim();
    } else if (title) {
      result = `### ${title}\n\n${innerContent.trim()}`;
    } else {
      const boldMatch = innerContent.match(/^\*\*([^*]+)\*\*:\s*/);
      if (boldMatch) {
        const boldTitle = boldMatch[1];
        const restContent = innerContent.replace(/^\*\*[^*]+\*\*:\s*/, '');
        result = `### ${boldTitle}\n\n${restContent.trim()}`;
      } else {
        const prefix = calloutTypeToPrefix(type);
        result = `### ${prefix}\n\n${innerContent.trim()}`;
      }
    }

    if (indent) {
      result = result.split('\n').map(line => indent + line).join('\n');
    }

    if (verbose) {
      console.log(`   Converted nested ${type} callout${title ? ` "${title}"` : ''}`);
    }

    return '\n' + result + '\n';
  });

  // Clean up excessive blank lines (3+ consecutive blank lines -> 2)
  newContent = newContent.replace(/\n{4,}/g, '\n\n\n');

  if (calloutsRemoved > 0 && !dryRun) {
    await fs.writeFile(filePath, newContent, 'utf-8');
  }

  return calloutsRemoved;
}

async function main() {
  const options = parseArgs();
  const stats: ConversionStats = {
    filesProcessed: 0,
    filesModified: 0,
    calloutsRemoved: 0,
    fileDetails: [],
  };

  const modeLabel = options.dryRun ? ' [DRY RUN]' : '';

  console.log('━'.repeat(80));
  console.log(`📝 Callout Removal Tool${modeLabel}`);
  console.log('━'.repeat(80));

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
    // Find all QMD files excluding auto-generated ones
    files = await glob('**/*.qmd', {
      cwd: PROJECT_ROOT,
      absolute: true,
      ignore: EXCLUDE_PATTERNS,
    });
    console.log(`Found ${files.length} QMD files (excluding auto-generated)\n`);
  }

  for (const file of files) {
    const relativePath = path.relative(PROJECT_ROOT, file);
    stats.filesProcessed++;

    const count = await processFile(file, options.dryRun, options.verbose);

    if (count > 0) {
      stats.filesModified++;
      stats.calloutsRemoved += count;
      stats.fileDetails.push({ file: relativePath, count });

      if (!options.verbose) {
        console.log(`   ${relativePath}: ${count} callout(s) removed`);
      }
    }
  }

  // Summary
  console.log('\n' + '━'.repeat(80));
  console.log('📊 Summary');
  console.log('━'.repeat(80));
  console.log(`Files processed:    ${stats.filesProcessed}`);
  console.log(`Files modified:     ${stats.filesModified}`);
  console.log(`Callouts removed:   ${stats.calloutsRemoved}`);

  if (options.dryRun) {
    console.log('\n⚠️  DRY RUN - No files were actually modified');
    console.log('   Run without --dry-run to apply changes');
  } else if (stats.calloutsRemoved > 0) {
    console.log('\n✅ Callouts removed successfully!');
  } else {
    console.log('\n✅ No callouts found to remove');
  }

  console.log('━'.repeat(80));
}

main().catch((error) => {
  console.error('\n❌ Error:', error instanceof Error ? error.message : String(error));
  process.exit(1);
});
