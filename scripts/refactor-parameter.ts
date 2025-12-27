#!/usr/bin/env node
/**
 * Refactor parameter names across the entire codebase
 *
 * This script automates the process of renaming parameters by:
 * 1. Updating Python parameters.py file
 * 2. Replacing references in all QMD files
 * 3. Regenerating variables and figures
 * 4. Validating no broken references remain
 *
 * Usage:
 *   npx tsx scripts/refactor-parameter.ts <old_name> <new_name> [--dry-run]
 *
 * Example:
 *   npx tsx scripts/refactor-parameter.ts PRE_1962_DRUG_DEVELOPMENT_COST PRE_1962_DRUG_DEVELOPMENT_COST_2024
 */

import fs from 'fs/promises';
import path from 'path';
import { execSync } from 'child_process';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(__dirname, '..');

interface RefactorOptions {
  oldName: string;
  newName: string;
  dryRun: boolean;
}

interface RefactorStats {
  pythonUpdates: number;
  qmdUpdates: number;
  filesModified: string[];
  warnings: string[];
}

/**
 * Parse command line arguments
 */
function parseArgs(): RefactorOptions {
  const args = process.argv.slice(2);

  if (args.length < 2) {
    console.error('Usage: npx tsx scripts/refactor-parameter.ts <old_name> <new_name> [--dry-run]');
    console.error('');
    console.error('Example:');
    console.error('  npx tsx scripts/refactor-parameter.ts PRE_1962_DRUG_DEVELOPMENT_COST PRE_1962_DRUG_DEVELOPMENT_COST_2024');
    process.exit(1);
  }

  return {
    oldName: args[0],
    newName: args[1],
    dryRun: args.includes('--dry-run'),
  };
}

/**
 * Convert Python parameter name to QMD variable name
 * Example: PRE_1962_DRUG_DEVELOPMENT_COST -> pre_1962_drug_development_cost
 */
function toQmdVariableName(pythonName: string): string {
  return pythonName.toLowerCase();
}

/**
 * Find all QMD files in knowledge directory
 */
async function findQmdFiles(): Promise<string[]> {
  const qmdFiles: string[] = [];

  async function walk(dir: string) {
    const entries = await fs.readdir(dir, { withFileTypes: true });

    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);

      if (entry.isDirectory()) {
        await walk(fullPath);
      } else if (entry.name.endsWith('.qmd')) {
        qmdFiles.push(fullPath);
      }
    }
  }

  await walk(path.join(PROJECT_ROOT, 'knowledge'));
  return qmdFiles;
}

/**
 * Replace text in file
 */
async function replaceInFile(
  filePath: string,
  oldText: string,
  newText: string,
  dryRun: boolean
): Promise<number> {
  const content = await fs.readFile(filePath, 'utf-8');
  const regex = new RegExp(escapeRegExp(oldText), 'g');
  const matches = content.match(regex);
  const count = matches ? matches.length : 0;

  if (count > 0 && !dryRun) {
    const newContent = content.replace(regex, newText);
    await fs.writeFile(filePath, newContent, 'utf-8');
  }

  return count;
}

/**
 * Escape special regex characters
 */
function escapeRegExp(string: string): string {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/**
 * Update Python parameters.py file
 */
async function updatePythonFile(
  oldName: string,
  newName: string,
  dryRun: boolean
): Promise<number> {
  const pythonFile = path.join(PROJECT_ROOT, 'dih_models', 'parameters.py');
  let totalReplacements = 0;

  // Pattern 1: Parameter definition (handle both with and without spaces)
  const defPattern = `${oldName} = Parameter(`;
  totalReplacements += await replaceInFile(pythonFile, defPattern, `${newName} = Parameter(`, dryRun);

  // Pattern 2: Parameter references in formulas
  totalReplacements += await replaceInFile(pythonFile, oldName, newName, dryRun);

  return totalReplacements;
}

/**
 * Update QMD files
 */
async function updateQmdFiles(
  oldName: string,
  newName: string,
  dryRun: boolean
): Promise<{ count: number; files: string[] }> {
  const qmdFiles = await findQmdFiles();
  const oldVarName = toQmdVariableName(oldName);
  const newVarName = toQmdVariableName(newName);

  let totalCount = 0;
  const modifiedFiles: string[] = [];

  // Patterns to replace in QMD files
  const patterns = [
    // Variable references: {{< var pre_1962_drug_development_cost >}}
    { old: `{{< var ${oldVarName} >}}`, new: `{{< var ${newVarName} >}}` },

    // LaTeX variables: {{< var pre_1962_drug_development_cost_latex >}}
    { old: `{{< var ${oldVarName}_latex >}}`, new: `{{< var ${newVarName}_latex >}}` },

    // Citation references: {{< var pre_1962_drug_development_cost_cite >}}
    { old: `{{< var ${oldVarName}_cite >}}`, new: `{{< var ${newVarName}_cite >}}` },

    // Figure includes with prefixes (check existing prefix first to avoid mc-mc-, tornado-tornado-, etc.)
    { old: `mc-distribution-${oldVarName}.qmd`, new: `mc-distribution-${newVarName}.qmd` },
    { old: `tornado-${oldVarName}.qmd`, new: `tornado-${newVarName}.qmd` },
    { old: `sensitivity-table-${oldVarName}.qmd`, new: `sensitivity-table-${newVarName}.qmd` },
    { old: `exceedance-${oldVarName}.qmd`, new: `exceedance-${newVarName}.qmd` },

    // Figure includes without prefixes (legacy format, add mc- prefix)
    { old: `distribution-${oldVarName}.qmd`, new: `mc-distribution-${newVarName}.qmd` },
  ];

  for (const file of qmdFiles) {
    let fileModified = false;

    for (const pattern of patterns) {
      const count = await replaceInFile(file, pattern.old, pattern.new, dryRun);
      if (count > 0) {
        totalCount += count;
        fileModified = true;
      }
    }

    if (fileModified) {
      modifiedFiles.push(path.relative(PROJECT_ROOT, file));
    }
  }

  return { count: totalCount, files: modifiedFiles };
}

/**
 * Regenerate variables and figures
 */
async function regenerateVariables(dryRun: boolean): Promise<void> {
  if (dryRun) {
    console.log('\n[DRY RUN] Would regenerate variables with:');
    console.log('  .venv/Scripts/python.exe scripts/generate-everything-parameters-variables-calculations-references.py');
    return;
  }

  console.log('\n🔄 Regenerating variables and figures...');

  try {
    const pythonPath = path.join(PROJECT_ROOT, '.venv', 'Scripts', 'python.exe');
    const scriptPath = path.join(PROJECT_ROOT, 'scripts', 'generate-everything-parameters-variables-calculations-references.py');

    execSync(`"${pythonPath}" "${scriptPath}"`, {
      cwd: PROJECT_ROOT,
      stdio: 'inherit',
    });

    console.log('✅ Variables regenerated successfully');
  } catch (error) {
    throw new Error(`Failed to regenerate variables: ${error}`);
  }
}

/**
 * Validate no broken references remain
 */
async function validateReferences(oldName: string): Promise<string[]> {
  const warnings: string[] = [];
  const qmdFiles = await findQmdFiles();
  const oldVarName = toQmdVariableName(oldName);

  // Check for any remaining references to old name
  const patterns = [
    `{{< var ${oldVarName} >}}`,
    `{{< var ${oldVarName}_latex >}}`,
    `{{< var ${oldVarName}_cite >}}`,
  ];

  for (const file of qmdFiles) {
    const content = await fs.readFile(file, 'utf-8');

    for (const pattern of patterns) {
      if (content.includes(pattern)) {
        warnings.push(`Found legacy reference in ${path.relative(PROJECT_ROOT, file)}: ${pattern}`);
      }
    }
  }

  return warnings;
}

/**
 * Main refactoring function
 */
async function refactorParameter(options: RefactorOptions): Promise<void> {
  const { oldName, newName, dryRun } = options;
  const stats: RefactorStats = {
    pythonUpdates: 0,
    qmdUpdates: 0,
    filesModified: [],
    warnings: [],
  };

  console.log('━'.repeat(80));
  console.log(`🔧 Parameter Refactoring Tool${dryRun ? ' [DRY RUN]' : ''}`);
  console.log('━'.repeat(80));
  console.log(`Old name: ${oldName}`);
  console.log(`New name: ${newName}`);
  console.log('');

  // Step 1: Update Python file
  console.log('📝 Step 1: Updating Python parameters.py...');
  stats.pythonUpdates = await updatePythonFile(oldName, newName, dryRun);
  console.log(`   Found ${stats.pythonUpdates} references in Python file`);

  // Step 2: Update QMD files
  console.log('\n📝 Step 2: Updating QMD files...');
  const qmdResult = await updateQmdFiles(oldName, newName, dryRun);
  stats.qmdUpdates = qmdResult.count;
  stats.filesModified = qmdResult.files;
  console.log(`   Found ${stats.qmdUpdates} references across ${stats.filesModified.length} files`);

  if (stats.filesModified.length > 0) {
    console.log('\n   Modified files:');
    for (const file of stats.filesModified.slice(0, 10)) {
      console.log(`   - ${file}`);
    }
    if (stats.filesModified.length > 10) {
      console.log(`   ... and ${stats.filesModified.length - 10} more`);
    }
  }

  // Step 3: Regenerate variables
  console.log('\n📝 Step 3: Regenerating variables...');
  await regenerateVariables(dryRun);

  // Step 4: Validate no broken references
  console.log('\n📝 Step 4: Validating references...');
  stats.warnings = await validateReferences(oldName);

  if (stats.warnings.length > 0) {
    console.log('\n⚠️  Warnings:');
    for (const warning of stats.warnings) {
      console.log(`   ${warning}`);
    }
  } else {
    console.log('   ✅ No broken references found');
  }

  // Summary
  console.log('\n' + '━'.repeat(80));
  console.log('📊 Summary');
  console.log('━'.repeat(80));
  console.log(`Python updates:    ${stats.pythonUpdates}`);
  console.log(`QMD updates:       ${stats.qmdUpdates}`);
  console.log(`Files modified:    ${stats.filesModified.length}`);
  console.log(`Warnings:          ${stats.warnings.length}`);

  if (dryRun) {
    console.log('\n⚠️  DRY RUN - No files were actually modified');
    console.log('   Run without --dry-run to apply changes');
  } else {
    console.log('\n✅ Refactoring complete!');
  }

  console.log('━'.repeat(80));
}

/**
 * Main entry point
 */
async function main() {
  try {
    const options = parseArgs();
    await refactorParameter(options);
  } catch (error) {
    console.error('\n❌ Error:', error instanceof Error ? error.message : String(error));
    process.exit(1);
  }
}

main();
