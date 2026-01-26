#!/usr/bin/env npx tsx
/**
 * Unified Review Runner
 * =====================
 *
 * Single entry point for all review checks. Supports running multiple checks
 * on single files or batch processing all files.
 *
 * Usage:
 *   npx tsx scripts/review/run-checks.ts knowledge/file.qmd --checks fact,link
 *   npx tsx scripts/review/run-checks.ts --all --checks fact
 *   npx tsx scripts/review/run-checks.ts --all --checks fact,link,figure,structure
 *   npx tsx scripts/review/run-checks.ts knowledge/file.qmd --checks all
 *
 * Available checks:
 *   fact      - Fact-check claims and statistics
 *   link      - Verify internal and external links
 *   figure    - Check figure references and captions
 *   structure - Verify document structure and formatting
 *   param     - Check for hardcoded values that should be parameters
 *   latex     - Verify LaTeX equations
 *   format    - Format and clean up content
 *   nonprofit - Check for nonprofit compliance issues
 *   all       - Run all checks
 */

import {
  factCheckFileWithLLM,
  linkCheckFile,
  figureCheckFile,
  structureCheckFileWithLLM,
  latexCheckFileWithLLM,
  formatFileWithLLM,
  nonprofitComplianceCheckFileWithLLM,
  parameterizeFileWithLLM,
  getBookFilesForProcessing,
  getStaleFiles,
} from './utils';
import { HASH_FIELDS } from '../lib/constants';
import fs from 'fs';
import path from 'path';
import dotenv from 'dotenv';

dotenv.config();

// Check definitions with their hash fields and functions
interface CheckDefinition {
  name: string;
  hashField: string;
  fn: (filePath: string) => Promise<void>;
  description: string;
}

const CHECKS: Record<string, CheckDefinition> = {
  fact: {
    name: 'Fact Check',
    hashField: HASH_FIELDS.FACT_CHECK,
    fn: factCheckFileWithLLM,
    description: 'Verify claims, statistics, and factual accuracy',
  },
  link: {
    name: 'Link Check',
    hashField: HASH_FIELDS.LINK_CHECK,
    fn: linkCheckFile,
    description: 'Verify internal and external links',
  },
  figure: {
    name: 'Figure Check',
    hashField: HASH_FIELDS.FIGURE_CHECK,
    fn: figureCheckFile,
    description: 'Check figure references and image paths',
  },
  structure: {
    name: 'Structure Check',
    hashField: HASH_FIELDS.STRUCTURE_CHECK,
    fn: structureCheckFileWithLLM,
    description: 'Verify document structure and formatting',
  },
  param: {
    name: 'Parameter Check',
    hashField: HASH_FIELDS.PARAM_CHECK,
    fn: parameterizeFileWithLLM,
    description: 'Find hardcoded values that should be parameters',
  },
  latex: {
    name: 'LaTeX Check',
    hashField: HASH_FIELDS.LATEX_CHECK,
    fn: latexCheckFileWithLLM,
    description: 'Verify LaTeX equations and math formatting',
  },
  format: {
    name: 'Format',
    hashField: HASH_FIELDS.FORMATTED,
    fn: formatFileWithLLM,
    description: 'Format and clean up content',
  },
  nonprofit: {
    name: 'Nonprofit Compliance',
    hashField: HASH_FIELDS.NONPROFIT_COMPLIANCE,
    fn: nonprofitComplianceCheckFileWithLLM,
    description: 'Check for nonprofit compliance issues',
  },
};

interface Options {
  filePath?: string;
  all: boolean;
  checks: string[];
  dryRun: boolean;
  limit?: number;
  force: boolean;
}

function parseArgs(): Options {
  const args = process.argv.slice(2);
  const options: Options = {
    all: false,
    checks: [],
    dryRun: false,
    force: false,
  };

  let i = 0;
  while (i < args.length) {
    const arg = args[i];

    if (arg === '--all' || arg === '-a') {
      options.all = true;
      i++;
      continue;
    }

    if (arg === '--checks' || arg === '-c') {
      const checksArg = args[i + 1];
      if (checksArg === 'all') {
        options.checks = Object.keys(CHECKS);
      } else {
        options.checks = checksArg.split(',').map(c => c.trim().toLowerCase());
      }
      i += 2;
      continue;
    }

    if (arg === '--dry-run') {
      options.dryRun = true;
      i++;
      continue;
    }

    if (arg === '--force' || arg === '-f') {
      options.force = true;
      i++;
      continue;
    }

    if (arg === '--limit' || arg === '-l') {
      options.limit = parseInt(args[i + 1], 10);
      i += 2;
      continue;
    }

    if (arg === '--help' || arg === '-h') {
      printHelp();
      process.exit(0);
    }

    // Non-option argument is the file path
    if (!arg.startsWith('--') && !arg.startsWith('-')) {
      options.filePath = arg;
    }

    i++;
  }

  return options;
}

function printHelp(): void {
  console.log(`
Unified Review Runner
=====================

Single entry point for all review checks.

Usage:
  npx tsx scripts/review/run-checks.ts <file> --checks <checks>
  npx tsx scripts/review/run-checks.ts --all --checks <checks>

Arguments:
  <file>              Single file to check (e.g., knowledge/chapter.qmd)

Options:
  --all, -a           Process all book files (uses hash tracking for staleness)
  --checks, -c        Comma-separated list of checks to run (or 'all')
  --force, -f         Skip staleness check, process all files
  --limit, -l <n>     Limit number of files to process (with --all)
  --dry-run           Show what would be processed without running checks
  --help, -h          Show this help message

Available Checks:
${Object.entries(CHECKS).map(([key, def]) =>
  `  ${key.padEnd(12)} - ${def.description}`
).join('\n')}
  all              - Run all checks

Examples:
  # Run fact and link checks on a single file
  npx tsx scripts/review/run-checks.ts knowledge/problem/regulatory-delay.qmd --checks fact,link

  # Run all checks on all stale files
  npx tsx scripts/review/run-checks.ts --all --checks all

  # Run structure check on first 5 stale files
  npx tsx scripts/review/run-checks.ts --all --checks structure --limit 5

  # See what would be processed without running
  npx tsx scripts/review/run-checks.ts --all --checks fact --dry-run

  # Force recheck all files (ignore hash tracking)
  npx tsx scripts/review/run-checks.ts --all --checks link --force
`);
}

async function runCheckOnFile(filePath: string, checkKey: string): Promise<void> {
  const check = CHECKS[checkKey];
  if (!check) {
    console.error(`Unknown check: ${checkKey}`);
    return;
  }

  console.log(`\n  Running ${check.name}...`);
  await check.fn(filePath);
}

async function processFile(filePath: string, checks: string[]): Promise<void> {
  console.log(`\nProcessing: ${filePath}`);

  for (const checkKey of checks) {
    try {
      await runCheckOnFile(filePath, checkKey);
    } catch (error) {
      console.error(`  Error running ${checkKey}: ${error}`);
      throw error;
    }
  }
}

async function getFilesToProcess(options: Options, checks: string[]): Promise<string[]> {
  if (options.filePath) {
    // Single file mode
    if (!fs.existsSync(options.filePath)) {
      console.error(`Error: File not found: ${options.filePath}`);
      process.exit(1);
    }
    return [options.filePath];
  }

  if (!options.all) {
    console.error('Error: Must specify a file or use --all');
    printHelp();
    process.exit(1);
  }

  // All files mode - get stale files for each check
  const allBookFiles = await getBookFilesForProcessing();

  if (options.force) {
    // Force mode - return all files
    let files = allBookFiles;
    if (options.limit) {
      files = files.slice(0, options.limit);
    }
    return files;
  }

  // Get union of stale files across all requested checks
  const staleFileSets: Set<string>[] = [];

  for (const checkKey of checks) {
    const check = CHECKS[checkKey];
    if (!check) continue;

    const staleFiles = await getStaleFiles(check.hashField, 'knowledge');
    staleFileSets.push(new Set(staleFiles.map(f => f.replace(/\\/g, '/'))));
  }

  // Union of all stale file sets (a file is included if it's stale for ANY check)
  const unionStale = new Set<string>();
  for (const staleSet of staleFileSets) {
    for (const file of staleSet) {
      unionStale.add(file);
    }
  }

  // Filter to only book files
  let filesToProcess = allBookFiles.filter(f =>
    unionStale.has(f.replace(/\\/g, '/'))
  );

  if (options.limit) {
    filesToProcess = filesToProcess.slice(0, options.limit);
  }

  return filesToProcess;
}

async function main(): Promise<void> {
  const options = parseArgs();

  // Validate checks
  if (options.checks.length === 0) {
    console.error('Error: Must specify at least one check with --checks');
    printHelp();
    process.exit(1);
  }

  const invalidChecks = options.checks.filter(c => !CHECKS[c]);
  if (invalidChecks.length > 0) {
    console.error(`Error: Unknown checks: ${invalidChecks.join(', ')}`);
    console.error(`Available checks: ${Object.keys(CHECKS).join(', ')}, all`);
    process.exit(1);
  }

  console.log('='.repeat(80));
  console.log('UNIFIED REVIEW RUNNER');
  console.log('='.repeat(80));
  console.log();
  console.log(`Checks to run: ${options.checks.join(', ')}`);
  console.log(`Mode: ${options.all ? 'All files' : 'Single file'}`);
  if (options.force) console.log('Force: Skipping staleness check');
  if (options.limit) console.log(`Limit: ${options.limit} files`);
  console.log();

  const filesToProcess = await getFilesToProcess(options, options.checks);

  console.log(`Files to process: ${filesToProcess.length}`);
  if (filesToProcess.length === 0) {
    console.log('\nNo files need processing. All files are up-to-date!');
    return;
  }

  if (options.dryRun) {
    console.log('\n[DRY RUN] Would process:');
    for (const file of filesToProcess) {
      console.log(`  - ${file}`);
    }
    console.log('\nChecks that would run:');
    for (const checkKey of options.checks) {
      const check = CHECKS[checkKey];
      console.log(`  - ${check.name}: ${check.description}`);
    }
    return;
  }

  // Process files
  let processedCount = 0;
  let errorCount = 0;

  for (const file of filesToProcess) {
    processedCount++;
    console.log(`\n[${processedCount}/${filesToProcess.length}] ${path.basename(file)}`);

    try {
      await processFile(file, options.checks);
    } catch (error) {
      errorCount++;
      console.error(`\nError processing ${file}:`, error);
      // Continue with next file instead of stopping
      console.log('Continuing with next file...');
    }
  }

  // Summary
  console.log('\n' + '='.repeat(80));
  console.log('SUMMARY');
  console.log('='.repeat(80));
  console.log(`Total files: ${filesToProcess.length}`);
  console.log(`Processed: ${processedCount}`);
  console.log(`Errors: ${errorCount}`);
  console.log(`Checks run: ${options.checks.join(', ')}`);

  if (errorCount > 0) {
    process.exit(1);
  }
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
