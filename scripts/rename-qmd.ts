#!/usr/bin/env node
/**
 * Rename a QMD file and update all references across the project
 *
 * This script automates the process of renaming QMD files by:
 * 1. Renaming the file on disk
 * 2. Adding a Quarto alias to the old name (so old links still work)
 * 3. Updating all _quarto*.yml config files
 * 4. Updating all markdown links in QMD files
 * 5. Updating path references in TypeScript/JavaScript files
 * 6. Updating path references in Python files
 * 7. Updating path references in documentation files
 *
 * Usage:
 *   npx tsx scripts/rename-qmd.ts <old_path> <new_path> [--dry-run]
 *
 * Options:
 *   --dry-run    Show what would be changed without making changes
 *
 * Examples:
 *   npx tsx scripts/rename-qmd.ts knowledge/problem/old-name.qmd knowledge/problem/new-name.qmd --dry-run
 *   npx tsx scripts/rename-qmd.ts knowledge/problem/old-name.qmd knowledge/problem/new-name.qmd
 *
 * Note: Paths should be relative to project root, without leading slash
 */

import fs from 'fs/promises';
import * as fsSync from 'fs';
import path from 'path';
import matter from 'gray-matter';
import { glob } from 'glob';
import { getProjectRoot, stringifyWithFrontmatter, getAllSourceFiles } from './lib/file-utils.js';

const PROJECT_ROOT = getProjectRoot();

interface RenameOptions {
  oldPath: string;
  newPath: string;
  dryRun: boolean;
  updateRefsOnly: boolean;  // Skip file rename, only update references
}

interface RenameStats {
  quartoConfigUpdates: number;
  qmdLinkUpdates: number;
  tsJsUpdates: number;
  pythonUpdates: number;
  docUpdates: number;
  yamlUpdates: number;
  jsonUpdates: number;
  filesModified: string[];
  aliasAdded: boolean;
}

/**
 * Parse command line arguments
 */
function parseArgs(): RenameOptions {
  const args = process.argv.slice(2);

  if (args.length < 2 || args[0] === '--help' || args[0] === '-h') {
    console.log(`
Usage: npx tsx scripts/rename-qmd.ts <old_path> <new_path> [--dry-run] [--update-refs-only]

Arguments:
  old_path     Current path to the QMD file (relative to project root)
  new_path     New path for the QMD file (relative to project root)

Options:
  --dry-run           Show what would be changed without making changes
  --update-refs-only  Skip file rename, only update references (use if file was already renamed)
  --help, -h          Show this help message

Examples:
  npx tsx scripts/rename-qmd.ts knowledge/problem/old-name.qmd knowledge/problem/new-name.qmd --dry-run
  npx tsx scripts/rename-qmd.ts knowledge/problem/cost-of-war.qmd knowledge/problem/price-of-war.qmd
  npx tsx scripts/rename-qmd.ts old.qmd new.qmd --update-refs-only  # If file was already renamed

Notes:
  - Paths should NOT have leading slashes
  - The script will add a Quarto alias to preserve old URLs
  - All _quarto*.yml configs and QMD links will be updated
`);
    process.exit(args[0] === '--help' || args[0] === '-h' ? 0 : 1);
  }

  // Normalize paths (remove leading slashes, normalize to forward slashes)
  const oldPath = args[0].replace(/^\//, '').replace(/\\/g, '/');
  const newPath = args[1].replace(/^\//, '').replace(/\\/g, '/');

  return {
    oldPath,
    newPath,
    dryRun: args.includes('--dry-run'),
    updateRefsOnly: args.includes('--update-refs-only'),
  };
}

/**
 * Validate that paths are valid QMD files
 */
async function validatePaths(oldPath: string, newPath: string): Promise<void> {
  const absoluteOldPath = path.join(PROJECT_ROOT, oldPath);

  // Check old file exists
  if (!fsSync.existsSync(absoluteOldPath)) {
    throw new Error(`Source file does not exist: ${oldPath}`);
  }

  // Check it's a QMD file
  if (!oldPath.endsWith('.qmd')) {
    throw new Error(`Source file must be a .qmd file: ${oldPath}`);
  }

  if (!newPath.endsWith('.qmd')) {
    throw new Error(`Target path must be a .qmd file: ${newPath}`);
  }

  // Check new file doesn't already exist
  const absoluteNewPath = path.join(PROJECT_ROOT, newPath);
  if (fsSync.existsSync(absoluteNewPath) && absoluteOldPath !== absoluteNewPath) {
    throw new Error(`Target file already exists: ${newPath}`);
  }
}

/**
 * Find all Quarto config files in the project root
 */
async function findQuartoConfigs(): Promise<string[]> {
  const configs = await glob('_quarto*.yml', { cwd: PROJECT_ROOT, absolute: true });
  return configs;
}

/**
 * Convert QMD path to HTML path for alias
 * Example: knowledge/problem/old-name.qmd -> /knowledge/problem/old-name.html
 */
function toHtmlPath(qmdPath: string): string {
  return '/' + qmdPath.replace(/\.qmd$/, '.html');
}

/**
 * Add Quarto alias to the renamed file's frontmatter
 */
async function addQuartoAlias(
  newFilePath: string,
  oldQmdPath: string,
  dryRun: boolean
): Promise<boolean> {
  // In dry-run mode, file hasn't been renamed yet, so read from old path
  const readPath = dryRun ? oldQmdPath : newFilePath;
  const absolutePath = path.join(PROJECT_ROOT, readPath);
  const content = await fs.readFile(absolutePath, 'utf-8');
  const { data: frontmatter, content: body } = matter(content);

  const aliasPath = toHtmlPath(oldQmdPath);

  // Initialize aliases array if it doesn't exist
  if (!frontmatter.aliases) {
    frontmatter.aliases = [];
  }

  // Check if alias already exists
  if (frontmatter.aliases.includes(aliasPath)) {
    console.log(`   Alias already exists: ${aliasPath}`);
    return false;
  }

  // Add the new alias
  frontmatter.aliases.push(aliasPath);

  if (!dryRun) {
    const newContent = stringifyWithFrontmatter(body, frontmatter);
    // Always write to the new file path (file has already been renamed at this point)
    const writePath = path.join(PROJECT_ROOT, newFilePath);
    await fs.writeFile(writePath, newContent, 'utf-8');
  }

  console.log(`   Added alias: ${aliasPath}`);
  return true;
}

/**
 * Update references in a Quarto config file
 */
async function updateQuartoConfig(
  configPath: string,
  oldPath: string,
  newPath: string,
  dryRun: boolean
): Promise<number> {
  const content = await fs.readFile(configPath, 'utf-8');

  // Create patterns to match the old path in various contexts:
  // - Direct reference: knowledge/problem/old-name.qmd
  // - With leading slash: /knowledge/problem/old-name.qmd
  // - href format: href: knowledge/problem/old-name.qmd
  const patterns = [
    // Match path without leading slash (most common in _quarto.yml)
    { regex: new RegExp(`(?<![a-zA-Z0-9_/-])${escapeRegExp(oldPath)}(?![a-zA-Z0-9_/-])`, 'g'), replacement: newPath },
    // Match path with leading slash
    { regex: new RegExp(`(?<=[^a-zA-Z0-9_-])/${escapeRegExp(oldPath)}(?![a-zA-Z0-9_/-])`, 'g'), replacement: `/${newPath}` },
  ];

  let newContent = content;
  let totalChanges = 0;

  for (const { regex, replacement } of patterns) {
    const matches = newContent.match(regex);
    if (matches) {
      newContent = newContent.replace(regex, replacement);
      totalChanges += matches.length;
    }
  }

  if (totalChanges > 0 && !dryRun) {
    await fs.writeFile(configPath, newContent, 'utf-8');
  }

  return totalChanges;
}

/**
 * Update markdown links in QMD files
 * Matches: [text](path/to/file.qmd) or [text](../path/to/file.qmd#anchor)
 */
async function updateQmdLinks(
  qmdFile: string,
  oldPath: string,
  newPath: string,
  dryRun: boolean
): Promise<number> {
  const content = await fs.readFile(qmdFile, 'utf-8');
  const fileDir = path.dirname(qmdFile);

  // Calculate what the relative path would be from this file to the old file
  const relativeOldPath = path.relative(fileDir, path.join(PROJECT_ROOT, oldPath)).replace(/\\/g, '/');
  const relativeNewPath = path.relative(fileDir, path.join(PROJECT_ROOT, newPath)).replace(/\\/g, '/');

  // Also calculate absolute paths (with leading /)
  const absoluteOldPath = '/' + oldPath;
  const absoluteNewPath = '/' + newPath;

  let newContent = content;
  let totalChanges = 0;

  // Pattern 1: Relative path links [text](relative/path.qmd) or [text](../relative/path.qmd#anchor)
  const relativeRegex = new RegExp(
    `(\\]\\()${escapeRegExp(relativeOldPath)}((?:#[^)]*)?\\))`,
    'g'
  );
  const relativeMatches = newContent.match(relativeRegex);
  if (relativeMatches) {
    newContent = newContent.replace(relativeRegex, `$1${relativeNewPath}$2`);
    totalChanges += relativeMatches.length;
  }

  // Pattern 2: Absolute path links [text](/knowledge/path.qmd) or [text](/knowledge/path.qmd#anchor)
  const absoluteRegex = new RegExp(
    `(\\]\\()${escapeRegExp(absoluteOldPath)}((?:#[^)]*)?\\))`,
    'g'
  );
  const absoluteMatches = newContent.match(absoluteRegex);
  if (absoluteMatches) {
    newContent = newContent.replace(absoluteRegex, `$1${absoluteNewPath}$2`);
    totalChanges += absoluteMatches.length;
  }

  // Pattern 3: Plain old path (no leading slash, full path from root)
  // This handles cases like `](knowledge/problem/file.qmd)`
  const plainRegex = new RegExp(
    `(\\]\\()${escapeRegExp(oldPath)}((?:#[^)]*)?\\))`,
    'g'
  );
  const plainMatches = newContent.match(plainRegex);
  if (plainMatches) {
    newContent = newContent.replace(plainRegex, `$1${newPath}$2`);
    totalChanges += plainMatches.length;
  }

  // Pattern 4: Match any path ending with the old filename (catches non-canonical paths)
  // This handles cases like `](../appendix/file.qmd)` when file is in same directory
  const oldBasename = path.basename(oldPath);
  const newBasename = path.basename(newPath);
  // Only apply if basename is different from full path (to avoid double-matching)
  if (oldBasename !== oldPath) {
    const basenameRegex = new RegExp(
      `(\\]\\()([^)]*/)${escapeRegExp(oldBasename)}((?:#[^)]*)?\\))`,
      'g'
    );
    const basenameMatches = newContent.match(basenameRegex);
    if (basenameMatches) {
      newContent = newContent.replace(basenameRegex, `$1$2${newBasename}$3`);
      totalChanges += basenameMatches.length;
    }
  }

  if (totalChanges > 0 && !dryRun) {
    await fs.writeFile(qmdFile, newContent, 'utf-8');
  }

  return totalChanges;
}

/**
 * Escape special regex characters
 */
function escapeRegExp(string: string): string {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/**
 * Update path references in a generic file (TS, JS, Python, etc.)
 * Matches string literals containing the path, including paths with anchors
 */
async function updatePathReferencesInFile(
  filePath: string,
  oldPath: string,
  newPath: string,
  dryRun: boolean
): Promise<number> {
  const content = await fs.readFile(filePath, 'utf-8');

  let newContent = content;
  let totalChanges = 0;

  // Pattern 1: Match path with optional anchor inside double quotes
  // e.g., "/knowledge/appendix/file.qmd#section" or "knowledge/appendix/file.qmd"
  const doubleQuoteRegex = new RegExp(
    `"(/?${escapeRegExp(oldPath)})(#[^"]*)?"|"([^"]*/)${escapeRegExp(oldPath)}(#[^"]*)?"`,
    'g'
  );
  const doubleQuoteMatches = newContent.match(doubleQuoteRegex);
  if (doubleQuoteMatches) {
    // Replace while preserving leading slash and anchor
    newContent = newContent.replace(
      new RegExp(`"(/?)(${escapeRegExp(oldPath)})(#[^"]*)?"`, 'g'),
      `"$1${newPath}$3"`
    );
    totalChanges += doubleQuoteMatches.length;
  }

  // Pattern 2: Match path with optional anchor inside single quotes
  const singleQuoteRegex = new RegExp(
    `'(/?${escapeRegExp(oldPath)})(#[^']*)?'`,
    'g'
  );
  const singleQuoteMatches = newContent.match(singleQuoteRegex);
  if (singleQuoteMatches) {
    newContent = newContent.replace(
      new RegExp(`'(/?)(${escapeRegExp(oldPath)})(#[^']*)?'`, 'g'),
      `'$1${newPath}$3'`
    );
    totalChanges += singleQuoteMatches.length;
  }

  // Pattern 3: Match path in backticks (template literals)
  // e.g., `knowledge/economics/1-pct-treaty-impact.qmd`
  const backtickRegex = new RegExp(
    `\`([^\`]*?)${escapeRegExp(oldPath)}([^\`]*?)\``,
    'g'
  );
  const backtickMatches = newContent.match(backtickRegex);
  if (backtickMatches) {
    newContent = newContent.replace(backtickRegex, `\`$1${newPath}$2\``);
    totalChanges += backtickMatches.length;
  }

  if (totalChanges > 0 && !dryRun) {
    await fs.writeFile(filePath, newContent, 'utf-8');
  }

  return totalChanges;
}

/**
 * Find and update references in TypeScript/JavaScript files
 */
async function updateTypeScriptFiles(
  oldPath: string,
  newPath: string,
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
    const changes = await updatePathReferencesInFile(file, oldPath, newPath, dryRun);
    if (changes > 0) {
      totalCount += changes;
      modifiedFiles.push(path.relative(PROJECT_ROOT, file));
    }
  }

  return { count: totalCount, files: modifiedFiles };
}

/**
 * Find and update references in Python files
 */
async function updatePythonFiles(
  oldPath: string,
  newPath: string,
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
    const changes = await updatePathReferencesInFile(file, oldPath, newPath, dryRun);
    if (changes > 0) {
      totalCount += changes;
      modifiedFiles.push(path.relative(PROJECT_ROOT, file));
    }
  }

  return { count: totalCount, files: modifiedFiles };
}

/**
 * Find and update references in documentation files
 */
async function updateDocFiles(
  oldPath: string,
  newPath: string,
  dryRun: boolean
): Promise<{ count: number; files: string[] }> {
  const docFiles = await glob('**/*.{md,txt,rst}', {
    cwd: PROJECT_ROOT,
    absolute: true,
    ignore: ['**/node_modules/**', '**/.venv/**', '**/_site/**', '**/_book/**', '**/*.qmd'],
  });

  let totalCount = 0;
  const modifiedFiles: string[] = [];

  for (const file of docFiles) {
    const content = await fs.readFile(file, 'utf-8');

    let newContent = content;
    let changes = 0;

    // Match the path anywhere in the file (documentation often has paths without quotes)
    const pathRegex = new RegExp(escapeRegExp(oldPath), 'g');
    const pathMatches = newContent.match(pathRegex);
    if (pathMatches) {
      newContent = newContent.replace(pathRegex, newPath);
      changes += pathMatches.length;
    }

    if (changes > 0) {
      if (!dryRun) {
        await fs.writeFile(file, newContent, 'utf-8');
      }
      totalCount += changes;
      modifiedFiles.push(path.relative(PROJECT_ROOT, file));
    }
  }

  return { count: totalCount, files: modifiedFiles };
}

/**
 * Find and update references in YAML files (including _variables*.yml)
 */
async function updateYamlFiles(
  oldPath: string,
  newPath: string,
  dryRun: boolean
): Promise<{ count: number; files: string[] }> {
  // Find all YAML files except _quarto*.yml (handled separately)
  const yamlFiles = await glob('**/*.{yml,yaml}', {
    cwd: PROJECT_ROOT,
    absolute: true,
    ignore: ['**/node_modules/**', '**/.venv/**', '**/_site/**', '**/_book/**', '_quarto*.yml'],
  });

  let totalCount = 0;
  const modifiedFiles: string[] = [];

  for (const file of yamlFiles) {
    const content = await fs.readFile(file, 'utf-8');

    let newContent = content;
    let changes = 0;

    // Match the path anywhere in the file (YAML often has paths in various formats)
    const pathRegex = new RegExp(escapeRegExp(oldPath), 'g');
    const pathMatches = newContent.match(pathRegex);
    if (pathMatches) {
      newContent = newContent.replace(pathRegex, newPath);
      changes += pathMatches.length;
    }

    if (changes > 0) {
      if (!dryRun) {
        await fs.writeFile(file, newContent, 'utf-8');
      }
      totalCount += changes;
      modifiedFiles.push(path.relative(PROJECT_ROOT, file));
    }
  }

  return { count: totalCount, files: modifiedFiles };
}

/**
 * Find and update references in JSON files
 */
async function updateJsonFiles(
  oldPath: string,
  newPath: string,
  dryRun: boolean
): Promise<{ count: number; files: string[] }> {
  const jsonFiles = await glob('**/*.json', {
    cwd: PROJECT_ROOT,
    absolute: true,
    ignore: ['**/node_modules/**', '**/.venv/**', '**/_site/**', '**/_book/**', 'package.json', 'package-lock.json', 'tsconfig.json'],
  });

  let totalCount = 0;
  const modifiedFiles: string[] = [];

  for (const file of jsonFiles) {
    const content = await fs.readFile(file, 'utf-8');

    let newContent = content;
    let changes = 0;

    // Match the path in JSON string values
    const pathRegex = new RegExp(escapeRegExp(oldPath), 'g');
    const pathMatches = newContent.match(pathRegex);
    if (pathMatches) {
      newContent = newContent.replace(pathRegex, newPath);
      changes += pathMatches.length;
    }

    if (changes > 0) {
      if (!dryRun) {
        await fs.writeFile(file, newContent, 'utf-8');
      }
      totalCount += changes;
      modifiedFiles.push(path.relative(PROJECT_ROOT, file));
    }
  }

  return { count: totalCount, files: modifiedFiles };
}

/**
 * Rename the file on disk
 */
async function renameFile(oldPath: string, newPath: string, dryRun: boolean): Promise<void> {
  const absoluteOldPath = path.join(PROJECT_ROOT, oldPath);
  const absoluteNewPath = path.join(PROJECT_ROOT, newPath);

  // Create target directory if it doesn't exist
  const targetDir = path.dirname(absoluteNewPath);
  if (!fsSync.existsSync(targetDir)) {
    if (!dryRun) {
      await fs.mkdir(targetDir, { recursive: true });
    }
    console.log(`   Created directory: ${path.relative(PROJECT_ROOT, targetDir)}`);
  }

  if (!dryRun) {
    await fs.rename(absoluteOldPath, absoluteNewPath);
  }
  console.log(`   Renamed: ${oldPath} -> ${newPath}`);
}

/**
 * Main rename function
 */
async function renameQmdFile(options: RenameOptions): Promise<void> {
  const { oldPath, newPath, dryRun, updateRefsOnly } = options;
  const stats: RenameStats = {
    quartoConfigUpdates: 0,
    qmdLinkUpdates: 0,
    tsJsUpdates: 0,
    pythonUpdates: 0,
    docUpdates: 0,
    yamlUpdates: 0,
    jsonUpdates: 0,
    filesModified: [],
    aliasAdded: false,
  };

  const modeLabel = dryRun ? ' [DRY RUN]' : (updateRefsOnly ? ' [UPDATE REFS ONLY]' : '');

  console.log('━'.repeat(80));
  console.log(`📁 QMD File Rename Tool${modeLabel}`);
  console.log('━'.repeat(80));
  console.log(`Old path: ${oldPath}`);
  console.log(`New path: ${newPath}`);
  console.log('');

  if (!updateRefsOnly) {
    // Validate paths
    console.log('📋 Step 1: Validating paths...');
    await validatePaths(oldPath, newPath);
    console.log('   ✅ Paths validated');

    // Step 2: Rename the file
    console.log('\n📋 Step 2: Renaming file...');
    await renameFile(oldPath, newPath, dryRun);

    // Step 3: Add Quarto alias to the renamed file
    console.log('\n📋 Step 3: Adding Quarto alias...');
    stats.aliasAdded = await addQuartoAlias(newPath, oldPath, dryRun);
  } else {
    console.log('📋 Skipping steps 1-3 (file operations) - update refs only mode');
  }

  // Step 4: Update Quarto config files
  console.log('\n📋 Step 4: Updating Quarto config files...');
  const quartoConfigs = await findQuartoConfigs();
  console.log(`   Found ${quartoConfigs.length} Quarto config files`);

  for (const config of quartoConfigs) {
    const changes = await updateQuartoConfig(config, oldPath, newPath, dryRun);
    if (changes > 0) {
      stats.quartoConfigUpdates += changes;
      stats.filesModified.push(path.relative(PROJECT_ROOT, config));
      console.log(`   Updated ${path.basename(config)}: ${changes} reference(s)`);
    }
  }

  // Step 5: Update links in all QMD files
  console.log('\n📋 Step 5: Updating links in QMD files...');
  const qmdFiles = await getAllSourceFiles(['.qmd']);
  console.log(`   Scanning ${qmdFiles.length} QMD files...`);

  let filesWithChanges = 0;
  for (const qmdFile of qmdFiles) {
    // Skip the renamed file itself
    if (path.resolve(qmdFile) === path.resolve(path.join(PROJECT_ROOT, newPath))) {
      continue;
    }

    const changes = await updateQmdLinks(qmdFile, oldPath, newPath, dryRun);
    if (changes > 0) {
      stats.qmdLinkUpdates += changes;
      stats.filesModified.push(path.relative(PROJECT_ROOT, qmdFile));
      filesWithChanges++;
      if (filesWithChanges <= 10) {
        console.log(`   Updated ${path.relative(PROJECT_ROOT, qmdFile)}: ${changes} link(s)`);
      }
    }
  }

  if (filesWithChanges > 10) {
    console.log(`   ... and ${filesWithChanges - 10} more files`);
  }

  // Step 6: Update TypeScript/JavaScript files
  console.log('\n📋 Step 6: Updating TypeScript/JavaScript files...');
  const tsResult = await updateTypeScriptFiles(oldPath, newPath, dryRun);
  if (tsResult.count > 0) {
    stats.tsJsUpdates = tsResult.count;
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

  // Step 7: Update Python files
  console.log('\n📋 Step 7: Updating Python files...');
  const pyResult = await updatePythonFiles(oldPath, newPath, dryRun);
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

  // Step 8: Update documentation files
  console.log('\n📋 Step 8: Updating documentation files...');
  const docResult = await updateDocFiles(oldPath, newPath, dryRun);
  if (docResult.count > 0) {
    stats.docUpdates = docResult.count;
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

  // Step 9: Update YAML files (including _variables*.yml)
  console.log('\n📋 Step 9: Updating YAML files...');
  const yamlResult = await updateYamlFiles(oldPath, newPath, dryRun);
  if (yamlResult.count > 0) {
    stats.yamlUpdates = yamlResult.count;
    stats.filesModified.push(...yamlResult.files);
    for (const file of yamlResult.files.slice(0, 5)) {
      console.log(`   Updated ${file}`);
    }
    if (yamlResult.files.length > 5) {
      console.log(`   ... and ${yamlResult.files.length - 5} more YAML files`);
    }
  } else {
    console.log('   No references found in YAML files');
  }

  // Step 10: Update JSON files
  console.log('\n📋 Step 10: Updating JSON files...');
  const jsonResult = await updateJsonFiles(oldPath, newPath, dryRun);
  if (jsonResult.count > 0) {
    stats.jsonUpdates = jsonResult.count;
    stats.filesModified.push(...jsonResult.files);
    for (const file of jsonResult.files.slice(0, 5)) {
      console.log(`   Updated ${file}`);
    }
    if (jsonResult.files.length > 5) {
      console.log(`   ... and ${jsonResult.files.length - 5} more JSON files`);
    }
  } else {
    console.log('   No references found in JSON files');
  }

  // Deduplicate files modified list
  stats.filesModified = [...new Set(stats.filesModified)];

  // Summary
  console.log('\n' + '━'.repeat(80));
  console.log('📊 Summary');
  console.log('━'.repeat(80));
  console.log(`File renamed:          ${oldPath} -> ${newPath}`);
  console.log(`Alias added:           ${stats.aliasAdded ? 'Yes' : 'No (already existed)'}`);
  console.log(`Quarto config updates: ${stats.quartoConfigUpdates}`);
  console.log(`QMD link updates:      ${stats.qmdLinkUpdates}`);
  console.log(`TypeScript/JS updates: ${stats.tsJsUpdates}`);
  console.log(`Python updates:        ${stats.pythonUpdates}`);
  console.log(`Documentation updates: ${stats.docUpdates}`);
  console.log(`YAML updates:          ${stats.yamlUpdates}`);
  console.log(`JSON updates:          ${stats.jsonUpdates}`);
  console.log(`Total files modified:  ${stats.filesModified.length}`);

  if (dryRun) {
    console.log('\n⚠️  DRY RUN - No files were actually modified');
    console.log('   Run without --dry-run to apply changes');
  } else {
    console.log('\n✅ Rename complete!');
    console.log('   Old URLs will redirect via Quarto alias');
  }

  console.log('━'.repeat(80));
}

/**
 * Main entry point
 */
async function main() {
  try {
    const options = parseArgs();
    await renameQmdFile(options);
  } catch (error) {
    console.error('\n❌ Error:', error instanceof Error ? error.message : String(error));
    process.exit(1);
  }
}

main();
