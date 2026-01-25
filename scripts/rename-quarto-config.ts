#!/usr/bin/env node
/**
 * Rename a Quarto config file (_quarto*.yml) and update all references
 *
 * This script automates the process of renaming Quarto config files by:
 * 1. Renaming the file on disk
 * 2. Updating all references in package.json
 * 3. Updating all references in Python scripts
 * 4. Updating all references in TypeScript/JavaScript files
 * 5. Updating all references in documentation files
 * 6. Updating netlify.toml and other config files
 *
 * Usage:
 *   npx tsx scripts/rename-quarto-config.ts <old_name> <new_name> [--dry-run]
 *
 * Options:
 *   --dry-run    Show what would be changed without making changes
 *
 * Examples:
 *   npx tsx scripts/rename-quarto-config.ts _quarto-1-pct-treaty-impact.yml _quarto-1-pct-treaty-impact.yml --dry-run
 *   npx tsx scripts/rename-quarto-config.ts _quarto-1-pct-treaty-impact.yml _quarto-1-pct-treaty-impact.yml
 */

import fs from 'fs/promises';
import * as fsSync from 'fs';
import path from 'path';
import { glob } from 'glob';
import { getProjectRoot } from './lib/file-utils';

const PROJECT_ROOT = getProjectRoot();

interface RenameOptions {
  oldName: string;
  newName: string;
  dryRun: boolean;
}

interface RenameStats {
  packageJsonUpdates: number;
  pythonUpdates: number;
  typescriptUpdates: number;
  markdownUpdates: number;
  configUpdates: number;
  filesModified: string[];
}

/**
 * Parse command line arguments
 */
function parseArgs(): RenameOptions {
  const args = process.argv.slice(2);

  if (args.length < 2 || args[0] === '--help' || args[0] === '-h') {
    console.log(`
Usage: npx tsx scripts/rename-quarto-config.ts <old_name> <new_name> [--dry-run]

Arguments:
  old_name     Current name of the Quarto config file (e.g., _quarto-1-pct-treaty-impact.yml)
  new_name     New name for the Quarto config file (e.g., _quarto-1-pct-treaty-impact.yml)

Options:
  --dry-run    Show what would be changed without making changes
  --help, -h   Show this help message

Examples:
  npx tsx scripts/rename-quarto-config.ts _quarto-1-pct-treaty-impact.yml _quarto-1-pct-treaty-impact.yml --dry-run
  npx tsx scripts/rename-quarto-config.ts _quarto-1-pct-treaty-impact.yml _quarto-1-pct-treaty-impact.yml

Notes:
  - Config names should start with _quarto- and end with .yml
  - The script will update references in package.json, Python, TypeScript, and docs
`);
    process.exit(args[0] === '--help' || args[0] === '-h' ? 0 : 1);
  }

  return {
    oldName: args[0],
    newName: args[1],
    dryRun: args.includes('--dry-run'),
  };
}

/**
 * Validate that names are valid Quarto config files
 */
async function validateNames(oldName: string, newName: string): Promise<void> {
  const absoluteOldPath = path.join(PROJECT_ROOT, oldName);

  // Check old file exists
  if (!fsSync.existsSync(absoluteOldPath)) {
    throw new Error(`Source config does not exist: ${oldName}`);
  }

  // Check it's a yml file
  if (!oldName.endsWith('.yml')) {
    throw new Error(`Source must be a .yml file: ${oldName}`);
  }

  if (!newName.endsWith('.yml')) {
    throw new Error(`Target must be a .yml file: ${newName}`);
  }

  // Check new file doesn't already exist
  const absoluteNewPath = path.join(PROJECT_ROOT, newName);
  if (fsSync.existsSync(absoluteNewPath) && absoluteOldPath !== absoluteNewPath) {
    throw new Error(`Target config already exists: ${newName}`);
  }
}

/**
 * Escape special regex characters
 */
function escapeRegExp(string: string): string {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/**
 * Rename the file on disk
 */
async function renameFile(oldName: string, newName: string, dryRun: boolean): Promise<void> {
  const absoluteOldPath = path.join(PROJECT_ROOT, oldName);
  const absoluteNewPath = path.join(PROJECT_ROOT, newName);

  if (!dryRun) {
    await fs.rename(absoluteOldPath, absoluteNewPath);
  }
  console.log(`   Renamed: ${oldName} -> ${newName}`);
}

/**
 * Update references in a file
 */
async function updateReferencesInFile(
  filePath: string,
  oldName: string,
  newName: string,
  dryRun: boolean
): Promise<number> {
  const content = await fs.readFile(filePath, 'utf-8');

  // Extract just the base name without path for matching
  const oldBaseName = path.basename(oldName);
  const newBaseName = path.basename(newName);

  // Also handle the name without extension for some contexts
  const oldNameNoExt = oldBaseName.replace(/\.yml$/, '');
  const newNameNoExt = newBaseName.replace(/\.yml$/, '');

  let newContent = content;
  let totalChanges = 0;

  // Pattern 1: Direct file reference (with or without quotes)
  const directRegex = new RegExp(escapeRegExp(oldBaseName), 'g');
  const directMatches = newContent.match(directRegex);
  if (directMatches) {
    newContent = newContent.replace(directRegex, newBaseName);
    totalChanges += directMatches.length;
  }

  // Pattern 2: Reference without .yml extension (for npm script names, etc.)
  // Only match if it's a word boundary (not part of another word)
  const noExtRegex = new RegExp(`(?<![a-zA-Z0-9_-])${escapeRegExp(oldNameNoExt)}(?![a-zA-Z0-9_])`, 'g');
  const noExtMatches = newContent.match(noExtRegex);
  if (noExtMatches) {
    // Be careful not to double-replace if already replaced with .yml
    const tempContent = newContent.replace(noExtRegex, newNameNoExt);
    if (tempContent !== newContent) {
      newContent = tempContent;
      totalChanges += noExtMatches.length;
    }
  }

  if (totalChanges > 0 && !dryRun) {
    await fs.writeFile(filePath, newContent, 'utf-8');
  }

  return totalChanges;
}

/**
 * Find and update references in package.json
 */
async function updatePackageJson(
  oldName: string,
  newName: string,
  dryRun: boolean
): Promise<{ count: number; file: string | null }> {
  const packageJsonPath = path.join(PROJECT_ROOT, 'package.json');

  if (!fsSync.existsSync(packageJsonPath)) {
    return { count: 0, file: null };
  }

  const changes = await updateReferencesInFile(packageJsonPath, oldName, newName, dryRun);

  return {
    count: changes,
    file: changes > 0 ? 'package.json' : null,
  };
}

/**
 * Find and update references in Python files
 */
async function updatePythonFiles(
  oldName: string,
  newName: string,
  dryRun: boolean
): Promise<{ count: number; files: string[] }> {
  const pyFiles = await glob('**/*.py', {
    cwd: PROJECT_ROOT,
    absolute: true,
    ignore: ['**/node_modules/**', '**/.venv/**', '**/venv/**', '**/__pycache__/**'],
  });

  let totalCount = 0;
  const modifiedFiles: string[] = [];

  for (const file of pyFiles) {
    const changes = await updateReferencesInFile(file, oldName, newName, dryRun);
    if (changes > 0) {
      totalCount += changes;
      modifiedFiles.push(path.relative(PROJECT_ROOT, file));
    }
  }

  return { count: totalCount, files: modifiedFiles };
}

/**
 * Find and update references in TypeScript/JavaScript files
 */
async function updateTypeScriptFiles(
  oldName: string,
  newName: string,
  dryRun: boolean
): Promise<{ count: number; files: string[] }> {
  const tsFiles = await glob('**/*.{ts,js,mjs,cjs}', {
    cwd: PROJECT_ROOT,
    absolute: true,
    ignore: ['**/node_modules/**', '**/.venv/**', '**/dist/**', '**/_site/**', '**/_book/**'],
  });

  let totalCount = 0;
  const modifiedFiles: string[] = [];

  for (const file of tsFiles) {
    const changes = await updateReferencesInFile(file, oldName, newName, dryRun);
    if (changes > 0) {
      totalCount += changes;
      modifiedFiles.push(path.relative(PROJECT_ROOT, file));
    }
  }

  return { count: totalCount, files: modifiedFiles };
}

/**
 * Find and update references in Markdown/documentation files
 */
async function updateDocFiles(
  oldName: string,
  newName: string,
  dryRun: boolean
): Promise<{ count: number; files: string[] }> {
  const docFiles = await glob('**/*.{md,txt,rst}', {
    cwd: PROJECT_ROOT,
    absolute: true,
    ignore: ['**/node_modules/**', '**/.venv/**', '**/_site/**', '**/_book/**'],
  });

  let totalCount = 0;
  const modifiedFiles: string[] = [];

  for (const file of docFiles) {
    const changes = await updateReferencesInFile(file, oldName, newName, dryRun);
    if (changes > 0) {
      totalCount += changes;
      modifiedFiles.push(path.relative(PROJECT_ROOT, file));
    }
  }

  return { count: totalCount, files: modifiedFiles };
}

/**
 * Find and update references in config files (netlify.toml, .gitignore, etc.)
 */
async function updateConfigFiles(
  oldName: string,
  newName: string,
  dryRun: boolean
): Promise<{ count: number; files: string[] }> {
  const configPatterns = [
    'netlify.toml',
    'vercel.json',
    '.gitignore',
    '.dockerignore',
    'Makefile',
    '*.toml',
    '.claude/**/*.md',
    'docs/**/*.yml',
    'docs/**/*.yaml',
  ];

  let totalCount = 0;
  const modifiedFiles: string[] = [];

  for (const pattern of configPatterns) {
    const files = await glob(pattern, {
      cwd: PROJECT_ROOT,
      absolute: true,
      ignore: ['**/node_modules/**', '**/.venv/**'],
    });

    for (const file of files) {
      const changes = await updateReferencesInFile(file, oldName, newName, dryRun);
      if (changes > 0) {
        totalCount += changes;
        const relPath = path.relative(PROJECT_ROOT, file);
        if (!modifiedFiles.includes(relPath)) {
          modifiedFiles.push(relPath);
        }
      }
    }
  }

  return { count: totalCount, files: modifiedFiles };
}

/**
 * Main rename function
 */
async function renameQuartoConfig(options: RenameOptions): Promise<void> {
  const { oldName, newName, dryRun } = options;
  const stats: RenameStats = {
    packageJsonUpdates: 0,
    pythonUpdates: 0,
    typescriptUpdates: 0,
    markdownUpdates: 0,
    configUpdates: 0,
    filesModified: [],
  };

  const modeLabel = dryRun ? ' [DRY RUN]' : '';

  console.log('━'.repeat(80));
  console.log(`⚙️  Quarto Config Rename Tool${modeLabel}`);
  console.log('━'.repeat(80));
  console.log(`Old name: ${oldName}`);
  console.log(`New name: ${newName}`);
  console.log('');

  // Validate names
  console.log('📋 Step 1: Validating config names...');
  await validateNames(oldName, newName);
  console.log('   ✅ Names validated');

  // Step 2: Rename the file
  console.log('\n📋 Step 2: Renaming config file...');
  await renameFile(oldName, newName, dryRun);

  // Step 3: Update package.json
  console.log('\n📋 Step 3: Updating package.json...');
  const packageResult = await updatePackageJson(oldName, newName, dryRun);
  if (packageResult.count > 0) {
    stats.packageJsonUpdates = packageResult.count;
    stats.filesModified.push(packageResult.file!);
    console.log(`   Updated package.json: ${packageResult.count} reference(s)`);
  } else {
    console.log('   No references found in package.json');
  }

  // Step 4: Update Python files
  console.log('\n📋 Step 4: Updating Python files...');
  const pyResult = await updatePythonFiles(oldName, newName, dryRun);
  if (pyResult.count > 0) {
    stats.pythonUpdates = pyResult.count;
    stats.filesModified.push(...pyResult.files);
    for (const file of pyResult.files.slice(0, 5)) {
      console.log(`   Updated ${file}`);
    }
    if (pyResult.files.length > 5) {
      console.log(`   ... and ${pyResult.files.length - 5} more Python files`);
    }
  } else {
    console.log('   No references found in Python files');
  }

  // Step 5: Update TypeScript/JavaScript files
  console.log('\n📋 Step 5: Updating TypeScript/JavaScript files...');
  const tsResult = await updateTypeScriptFiles(oldName, newName, dryRun);
  if (tsResult.count > 0) {
    stats.typescriptUpdates = tsResult.count;
    stats.filesModified.push(...tsResult.files);
    for (const file of tsResult.files.slice(0, 5)) {
      console.log(`   Updated ${file}`);
    }
    if (tsResult.files.length > 5) {
      console.log(`   ... and ${tsResult.files.length - 5} more TS/JS files`);
    }
  } else {
    console.log('   No references found in TypeScript/JavaScript files');
  }

  // Step 6: Update documentation files
  console.log('\n📋 Step 6: Updating documentation files...');
  const docResult = await updateDocFiles(oldName, newName, dryRun);
  if (docResult.count > 0) {
    stats.markdownUpdates = docResult.count;
    stats.filesModified.push(...docResult.files);
    for (const file of docResult.files.slice(0, 5)) {
      console.log(`   Updated ${file}`);
    }
    if (docResult.files.length > 5) {
      console.log(`   ... and ${docResult.files.length - 5} more doc files`);
    }
  } else {
    console.log('   No references found in documentation files');
  }

  // Step 7: Update config files
  console.log('\n📋 Step 7: Updating config files (netlify.toml, .gitignore, etc.)...');
  const configResult = await updateConfigFiles(oldName, newName, dryRun);
  if (configResult.count > 0) {
    stats.configUpdates = configResult.count;
    stats.filesModified.push(...configResult.files);
    for (const file of configResult.files) {
      console.log(`   Updated ${file}`);
    }
  } else {
    console.log('   No references found in config files');
  }

  // Deduplicate files modified list
  stats.filesModified = [...new Set(stats.filesModified)];

  // Summary
  console.log('\n' + '━'.repeat(80));
  console.log('📊 Summary');
  console.log('━'.repeat(80));
  console.log(`Config renamed:        ${oldName} -> ${newName}`);
  console.log(`package.json updates:  ${stats.packageJsonUpdates}`);
  console.log(`Python updates:        ${stats.pythonUpdates}`);
  console.log(`TypeScript/JS updates: ${stats.typescriptUpdates}`);
  console.log(`Documentation updates: ${stats.markdownUpdates}`);
  console.log(`Config file updates:   ${stats.configUpdates}`);
  console.log(`Total files modified:  ${stats.filesModified.length}`);

  if (dryRun) {
    console.log('\n⚠️  DRY RUN - No files were actually modified');
    console.log('   Run without --dry-run to apply changes');
  } else {
    console.log('\n✅ Rename complete!');
  }

  console.log('━'.repeat(80));
}

/**
 * Main entry point
 */
async function main() {
  try {
    const options = parseArgs();
    await renameQuartoConfig(options);
  } catch (error) {
    console.error('\n❌ Error:', error instanceof Error ? error.message : String(error));
    process.exit(1);
  }
}

main();
