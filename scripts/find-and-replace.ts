#!/usr/bin/env tsx
/**
 * Find and Replace Across QMD Files
 * ==================================
 *
 * Performs bulk find-and-replace operations across all .qmd files in the project.
 * Uses the centralized file-utils library for consistent file handling.
 *
 * Usage:
 *   # Basic find and replace (dry run by default)
 *   npx tsx scripts/find-and-replace.ts "old text" "new text"
 *
 *   # Multiple replacements
 *   npx tsx scripts/find-and-replace.ts "text1" "replacement1" "text2" "replacement2"
 *
 *   # Using regex (wrap in slashes)
 *   npx tsx scripts/find-and-replace.ts "/word—word/g" "word, word"
 *
 *   # Actually apply changes (not dry run)
 *   npx tsx scripts/find-and-replace.ts --apply "old text" "new text"
 *
 *   # Search in specific directory
 *   npx tsx scripts/find-and-replace.ts --path knowledge/proof "old" "new"
 *
 * Options:
 *   --apply         Actually apply changes (default: dry run)
 *   --path <dir>    Limit search to specific directory (default: all .qmd files)
 *   --help          Show this help message
 *
 * Examples:
 *   # Replace em-dashes with comma-space (dry run)
 *   npx tsx scripts/find-and-replace.ts "/([a-zA-Z])—([a-zA-Z])/g" "$1, $2"
 *
 *   # Replace outdated term across all files
 *   npx tsx scripts/find-and-replace.ts --apply "dFDA" "Decentralized FDA"
 *
 *   # Multiple replacements in one pass
 *   npx tsx scripts/find-and-replace.ts --apply \
 *     "utilise" "use" \
 *     "optimise" "optimize" \
 *     "grey" "gray"
 */

import { bulkReplaceInQmdFiles, type BulkReplaceResult } from './lib/file-utils';

function parseArgs(args: string[]): {
  replacements: Map<string | RegExp, string>;
  options: { basePath?: string; dryRun: boolean };
  showHelp: boolean;
} {
  const replacements = new Map<string | RegExp, string>();
  const options: { basePath?: string; dryRun: boolean } = { dryRun: true };
  let showHelp = false;

  let i = 0;
  while (i < args.length) {
    const arg = args[i];

    if (arg === '--help' || arg === '-h') {
      showHelp = true;
      break;
    }

    if (arg === '--apply') {
      options.dryRun = false;
      i++;
      continue;
    }

    if (arg === '--path') {
      options.basePath = args[i + 1];
      i += 2;
      continue;
    }

    // Remaining args should be find/replace pairs
    const searchArg = args[i];
    const replaceArg = args[i + 1];

    if (!searchArg || !replaceArg) {
      throw new Error(`Invalid argument pair at position ${i}. Expected: "search" "replace"`);
    }

    // Check if search arg is a regex (wrapped in slashes)
    const regexMatch = searchArg.match(/^\/(.+)\/([gimuy]*)$/);
    if (regexMatch) {
      const pattern = regexMatch[1];
      const flags = regexMatch[2];
      replacements.set(new RegExp(pattern, flags), replaceArg);
    } else {
      replacements.set(searchArg, replaceArg);
    }

    i += 2;
  }

  return { replacements, options, showHelp };
}

function printHelp(): void {
  const helpText = `
Find and Replace Across QMD Files
==================================

Performs bulk find-and-replace operations across all .qmd files in the project.

USAGE:
  npx tsx scripts/find-and-replace.ts [OPTIONS] <search> <replace> [<search2> <replace2> ...]

OPTIONS:
  --apply         Actually apply changes (default: dry run)
  --path <dir>    Limit search to specific directory (default: all .qmd files)
  --help, -h      Show this help message

ARGUMENTS:
  <search>        Text or regex pattern to find (regex: /pattern/flags)
  <replace>       Replacement text (can use $1, $2 for regex groups)

EXAMPLES:
  # Dry run - preview changes without applying
  npx tsx scripts/find-and-replace.ts "old text" "new text"

  # Apply changes
  npx tsx scripts/find-and-replace.ts --apply "old text" "new text"

  # Replace with regex (em-dashes to comma-space)
  npx tsx scripts/find-and-replace.ts --apply "/([a-zA-Z])—([a-zA-Z])/g" "$1, $2"

  # Multiple replacements in one pass
  npx tsx scripts/find-and-replace.ts --apply \\
    "utilise" "use" \\
    "optimise" "optimize" \\
    "grey" "gray"

  # Limit to specific directory
  npx tsx scripts/find-and-replace.ts --apply --path knowledge/proof "old" "new"

NOTES:
  - Dry run is the default - use --apply to actually modify files
  - Respects .gitignore patterns
  - Regex flags: g (global), i (case-insensitive), m (multiline)
  - Use double quotes around patterns with special characters
`;
  console.log(helpText);
}

function printResults(result: BulkReplaceResult, dryRun: boolean): void {
  console.log('\n' + '='.repeat(80));
  console.log(dryRun ? 'DRY RUN RESULTS (no files modified)' : 'REPLACEMENT RESULTS');
  console.log('='.repeat(80));
  console.log(`Total files scanned: ${result.totalFiles}`);
  console.log(`Files with changes: ${result.filesChanged}`);
  console.log(`Total replacements: ${result.totalChanges}`);

  if (result.filesChanged > 0) {
    console.log('\n' + '-'.repeat(80));
    console.log('FILES MODIFIED:');
    console.log('-'.repeat(80));

    for (const { file, changes } of result.details) {
      console.log(`  ${file} (${changes} replacement${changes !== 1 ? 's' : ''})`);
    }
  } else {
    console.log('\nNo files matched the search pattern(s).');
  }

  if (dryRun && result.filesChanged > 0) {
    console.log('\n' + '='.repeat(80));
    console.log('⚠️  DRY RUN MODE - No files were actually modified');
    console.log('Run with --apply to apply these changes');
    console.log('='.repeat(80));
  }

  console.log();
}

async function main() {
  try {
    const { replacements, options, showHelp } = parseArgs(process.argv.slice(2));

    if (showHelp) {
      printHelp();
      process.exit(0);
    }

    if (replacements.size === 0) {
      console.error('Error: No search/replace pairs provided\n');
      printHelp();
      process.exit(1);
    }

    // Show what we're searching for
    console.log('\n' + '='.repeat(80));
    console.log('FIND AND REPLACE CONFIGURATION');
    console.log('='.repeat(80));
    console.log(`Mode: ${options.dryRun ? 'DRY RUN (preview only)' : 'APPLY CHANGES'}`);
    console.log(`Path: ${options.basePath || 'all .qmd files'}`);
    console.log('\nReplacements:');

    let index = 1;
    for (const [search, replace] of replacements.entries()) {
      const searchStr = search instanceof RegExp ? `/${search.source}/${search.flags}` : `"${search}"`;
      const replaceStr = `"${replace}"`;
      console.log(`  ${index}. ${searchStr} → ${replaceStr}`);
      index++;
    }

    console.log('='.repeat(80));
    console.log('\nProcessing files...\n');

    // Perform the replacement
    const result = await bulkReplaceInQmdFiles(replacements, options);

    // Print results
    printResults(result, options.dryRun);

    // Exit with error code if dry run and changes were found (to indicate action needed)
    if (options.dryRun && result.filesChanged > 0) {
      process.exit(1);
    }

    process.exit(0);
  } catch (error) {
    if (error instanceof Error) {
      console.error(`\nError: ${error.message}\n`);
    } else {
      console.error('\nUnknown error occurred\n');
    }
    printHelp();
    process.exit(1);
  }
}

main();
