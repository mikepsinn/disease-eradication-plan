#!/usr/bin/env node
/**
 * Refactor parameter names across the entire codebase
 *
 * This script automates the process of renaming parameters by:
 * 1. Finding all usages with context for review
 * 2. Updating Python parameters.py file
 * 3. Replacing references in all QMD files
 * 4. Regenerating variables and figures
 * 5. Validating no broken references remain
 *
 * Usage:
 *   npx tsx scripts/refactor-parameter.ts <old_name> <new_name> [--dry-run] [--review-only]
 *
 * Options:
 *   --dry-run      Show what would be changed without making changes
 *   --review-only  Output all usages with context to a file for review (no changes made)
 *
 * Example:
 *   npx tsx scripts/refactor-parameter.ts DISEASE_ERADICATION_DELAY_ECONOMIC_LOSS EFFICACY_LAG_ECONOMIC_LOSS --review-only
 *   npx tsx scripts/refactor-parameter.ts DISEASE_ERADICATION_DELAY_ECONOMIC_LOSS EFFICACY_LAG_ECONOMIC_LOSS --dry-run
 *   npx tsx scripts/refactor-parameter.ts DISEASE_ERADICATION_DELAY_ECONOMIC_LOSS EFFICACY_LAG_ECONOMIC_LOSS
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
  reviewOnly: boolean;
}

interface UsageContext {
  file: string;
  lineNumber: number;
  line: string;
  contextBefore: string[];
  contextAfter: string[];
  matchType: string;
}

interface RefactorStats {
  pythonUpdates: number;
  qmdUpdates: number;
  pyScriptUpdates: number;
  tsUpdates: number;
  filesModified: string[];
  warnings: string[];
}

/**
 * Parse command line arguments
 */
function parseArgs(): RefactorOptions {
  const args = process.argv.slice(2);

  if (args.length < 2) {
    console.error('Usage: npx tsx scripts/refactor-parameter.ts <old_name> <new_name> [--dry-run] [--review-only]');
    console.error('');
    console.error('Options:');
    console.error('  --dry-run      Show what would be changed without making changes');
    console.error('  --review-only  Output all usages with context to a file for review (no changes made)');
    console.error('');
    console.error('Example:');
    console.error('  npx tsx scripts/refactor-parameter.ts DISEASE_ERADICATION_DELAY_ECONOMIC_LOSS EFFICACY_LAG_ECONOMIC_LOSS --review-only');
    process.exit(1);
  }

  return {
    oldName: args[0],
    newName: args[1],
    dryRun: args.includes('--dry-run'),
    reviewOnly: args.includes('--review-only'),
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
 * Find all Python scripts (excluding parameters.py which is handled separately)
 */
async function findPythonScripts(): Promise<string[]> {
  const pyFiles: string[] = [];
  const excludeDirs = ['node_modules', '.venv', 'venv', '_freeze', '.quarto', '_site', '__pycache__'];

  async function walk(dir: string) {
    const entries = await fs.readdir(dir, { withFileTypes: true });

    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);

      if (entry.isDirectory()) {
        if (!excludeDirs.includes(entry.name)) {
          await walk(fullPath);
        }
      } else if (entry.name.endsWith('.py') && entry.name !== 'parameters.py') {
        pyFiles.push(fullPath);
      }
    }
  }

  await walk(PROJECT_ROOT);
  return pyFiles;
}

/**
 * Find all TypeScript files
 */
async function findTypeScriptFiles(): Promise<string[]> {
  const tsFiles: string[] = [];
  const excludeDirs = ['node_modules', '.venv', 'venv', '_freeze', '.quarto', '_site'];
  const excludeFiles = ['parameters-calculations-citations.ts']; // Auto-generated

  async function walk(dir: string) {
    const entries = await fs.readdir(dir, { withFileTypes: true });

    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);

      if (entry.isDirectory()) {
        if (!excludeDirs.includes(entry.name)) {
          await walk(fullPath);
        }
      } else if (entry.name.endsWith('.ts') && !excludeFiles.includes(entry.name)) {
        tsFiles.push(fullPath);
      }
    }
  }

  await walk(PROJECT_ROOT);
  return tsFiles;
}

/**
 * Find all usages of a parameter with surrounding context
 */
async function findUsagesWithContext(
  oldName: string,
  contextLines: number = 3
): Promise<UsageContext[]> {
  const usages: UsageContext[] = [];
  const oldVarName = toQmdVariableName(oldName);

  // Patterns to search for
  const patterns = [
    { pattern: oldName, type: 'Python parameter' },
    { pattern: `{{< var ${oldVarName} >}}`, type: 'QMD variable' },
    { pattern: `{{< var ${oldVarName}_latex >}}`, type: 'QMD LaTeX variable' },
    { pattern: `{{< var ${oldVarName}_cite >}}`, type: 'QMD citation variable' },
    { pattern: `distribution-${oldVarName}`, type: 'Figure include' },
    { pattern: `tornado-${oldVarName}`, type: 'Tornado include' },
    { pattern: `mc-distribution-${oldVarName}`, type: 'MC distribution include' },
  ];

  // Search Python files
  const pythonFile = path.join(PROJECT_ROOT, 'dih_models', 'parameters.py');
  await searchFileForUsages(pythonFile, patterns, usages, contextLines);

  // Search QMD files
  const qmdFiles = await findQmdFiles();
  for (const file of qmdFiles) {
    await searchFileForUsages(file, patterns, usages, contextLines);
  }

  return usages;
}

/**
 * Search a single file for pattern matches with context
 */
async function searchFileForUsages(
  filePath: string,
  patterns: { pattern: string; type: string }[],
  usages: UsageContext[],
  contextLines: number
): Promise<void> {
  const content = await fs.readFile(filePath, 'utf-8');
  const lines = content.split('\n');

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    for (const { pattern, type } of patterns) {
      if (line.includes(pattern)) {
        usages.push({
          file: path.relative(PROJECT_ROOT, filePath),
          lineNumber: i + 1,
          line: line.trim(),
          contextBefore: lines.slice(Math.max(0, i - contextLines), i).map(l => l.trimEnd()),
          contextAfter: lines.slice(i + 1, Math.min(lines.length, i + 1 + contextLines)).map(l => l.trimEnd()),
          matchType: type,
        });
        break; // Only count each line once even if multiple patterns match
      }
    }
  }
}

/**
 * Output usages to a markdown file for review
 */
async function outputUsagesToFile(
  usages: UsageContext[],
  oldName: string,
  newName: string
): Promise<string> {
  const outputPath = path.join(PROJECT_ROOT, '_analysis', `refactor-review-${oldName.toLowerCase()}.md`);

  // Group usages by file
  const usagesByFile = new Map<string, UsageContext[]>();
  for (const usage of usages) {
    const existing = usagesByFile.get(usage.file) || [];
    existing.push(usage);
    usagesByFile.set(usage.file, existing);
  }

  let output = `# Parameter Refactoring Review\n\n`;
  output += `**Old name:** \`${oldName}\` (variable: \`${toQmdVariableName(oldName)}\`)\n`;
  output += `**New name:** \`${newName}\` (variable: \`${toQmdVariableName(newName)}\`)\n\n`;
  output += `**Total usages found:** ${usages.length}\n`;
  output += `**Files affected:** ${usagesByFile.size}\n\n`;
  output += `---\n\n`;
  output += `## Review Checklist\n\n`;
  output += `For each usage, check if the surrounding context needs updating:\n`;
  output += `- [ ] Variable reference makes sense with new name\n`;
  output += `- [ ] Surrounding text accurately describes what the parameter measures\n`;
  output += `- [ ] No hardcoded values that should also be updated\n\n`;
  output += `---\n\n`;

  for (const [file, fileUsages] of usagesByFile) {
    output += `## ${file}\n\n`;

    for (const usage of fileUsages) {
      output += `### Line ${usage.lineNumber} (${usage.matchType})\n\n`;
      output += `\`\`\`\n`;

      // Context before
      for (const ctxLine of usage.contextBefore) {
        output += `${ctxLine}\n`;
      }

      // The matching line (highlighted with >>)
      output += `>> ${usage.line}\n`;

      // Context after
      for (const ctxLine of usage.contextAfter) {
        output += `${ctxLine}\n`;
      }

      output += `\`\`\`\n\n`;
      output += `**Review needed?** [ ] Yes / [ ] No\n\n`;
      output += `---\n\n`;
    }
  }

  // Ensure _analysis directory exists
  await fs.mkdir(path.dirname(outputPath), { recursive: true });
  await fs.writeFile(outputPath, output, 'utf-8');

  return outputPath;
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
 * Uses word boundaries to avoid double-prefixing (e.g., DFDA_DFDA_...)
 */
async function updatePythonFile(
  oldName: string,
  newName: string,
  dryRun: boolean
): Promise<number> {
  const pythonFile = path.join(PROJECT_ROOT, 'dih_models', 'parameters.py');

  // Use word boundary regex to replace all instances in a single pass
  // This prevents double-prefixing (e.g., renaming TRIAL_X to DFDA_TRIAL_X
  // won't then rename DFDA_TRIAL_X to DFDA_DFDA_TRIAL_X)
  const content = await fs.readFile(pythonFile, 'utf-8');

  // Word boundary regex: only match oldName when it's not part of a larger identifier
  // (?<![A-Z_]) = negative lookbehind: not preceded by uppercase letter or underscore
  // (?![A-Z_]) = negative lookahead: not followed by uppercase letter or underscore
  const regex = new RegExp(`(?<![A-Z_])${escapeRegExp(oldName)}(?![A-Z_])`, 'g');
  const matches = content.match(regex);
  const count = matches ? matches.length : 0;

  if (count > 0 && !dryRun) {
    const newContent = content.replace(regex, newName);
    await fs.writeFile(pythonFile, newContent, 'utf-8');
  }

  return count;
}

/**
 * Update QMD files (both Quarto variables and embedded Python code)
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

    // Replace Quarto variable patterns
    for (const pattern of patterns) {
      const count = await replaceInFile(file, pattern.old, pattern.new, dryRun);
      if (count > 0) {
        totalCount += count;
        fileModified = true;
      }
    }

    // Also replace UPPERCASE parameter name in embedded Python code
    // Uses word boundary regex to avoid partial matches
    const content = await fs.readFile(file, 'utf-8');
    const regex = new RegExp(`(?<![A-Za-z_])${escapeRegExp(oldName)}(?![A-Za-z_])`, 'g');
    const matches = content.match(regex);
    if (matches && matches.length > 0) {
      if (!dryRun) {
        const newContent = content.replace(regex, newName);
        await fs.writeFile(file, newContent, 'utf-8');
      }
      totalCount += matches.length;
      fileModified = true;
    }

    if (fileModified) {
      modifiedFiles.push(path.relative(PROJECT_ROOT, file));
    }
  }

  return { count: totalCount, files: modifiedFiles };
}

/**
 * Update Python scripts (excluding parameters.py)
 */
async function updatePythonScripts(
  oldName: string,
  newName: string,
  dryRun: boolean
): Promise<{ count: number; files: string[] }> {
  const pyFiles = await findPythonScripts();
  let totalCount = 0;
  const modifiedFiles: string[] = [];

  // Word boundary regex for Python identifiers
  const regex = new RegExp(`(?<![A-Za-z_])${escapeRegExp(oldName)}(?![A-Za-z_])`, 'g');

  for (const file of pyFiles) {
    const content = await fs.readFile(file, 'utf-8');
    const matches = content.match(regex);

    if (matches && matches.length > 0) {
      if (!dryRun) {
        const newContent = content.replace(regex, newName);
        await fs.writeFile(file, newContent, 'utf-8');
      }
      totalCount += matches.length;
      modifiedFiles.push(path.relative(PROJECT_ROOT, file));
    }
  }

  return { count: totalCount, files: modifiedFiles };
}

/**
 * Update TypeScript files
 */
async function updateTypeScriptFiles(
  oldName: string,
  newName: string,
  dryRun: boolean
): Promise<{ count: number; files: string[] }> {
  const tsFiles = await findTypeScriptFiles();
  let totalCount = 0;
  const modifiedFiles: string[] = [];

  // Word boundary regex - matches both UPPERCASE and lowercase versions
  const oldVarName = toQmdVariableName(oldName);
  const newVarName = toQmdVariableName(newName);

  for (const file of tsFiles) {
    let content = await fs.readFile(file, 'utf-8');
    let fileModified = false;

    // Replace UPPERCASE version
    const upperRegex = new RegExp(`(?<![A-Za-z_])${escapeRegExp(oldName)}(?![A-Za-z_])`, 'g');
    const upperMatches = content.match(upperRegex);
    if (upperMatches && upperMatches.length > 0) {
      content = content.replace(upperRegex, newName);
      totalCount += upperMatches.length;
      fileModified = true;
    }

    // Replace lowercase version (in strings, etc.)
    const lowerRegex = new RegExp(`(?<![a-z_])${escapeRegExp(oldVarName)}(?![a-z_])`, 'g');
    const lowerMatches = content.match(lowerRegex);
    if (lowerMatches && lowerMatches.length > 0) {
      content = content.replace(lowerRegex, newVarName);
      totalCount += lowerMatches.length;
      fileModified = true;
    }

    if (fileModified) {
      if (!dryRun) {
        await fs.writeFile(file, content, 'utf-8');
      }
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
  const { oldName, newName, dryRun, reviewOnly } = options;
  const stats: RefactorStats = {
    pythonUpdates: 0,
    qmdUpdates: 0,
    pyScriptUpdates: 0,
    tsUpdates: 0,
    filesModified: [],
    warnings: [],
  };

  const modeLabel = reviewOnly ? ' [REVIEW ONLY]' : dryRun ? ' [DRY RUN]' : '';

  console.log('━'.repeat(80));
  console.log(`🔧 Parameter Rename/Refactoring Tool${modeLabel}`);
  console.log('━'.repeat(80));
  console.log(`Old name: ${oldName}`);
  console.log(`New name: ${newName}`);
  console.log('');

  // Step 1: Find all usages with context and output to file
  console.log('📝 Step 1: Finding all usages with context...');
  const usages = await findUsagesWithContext(oldName);
  console.log(`   Found ${usages.length} usages`);

  const reviewFilePath = await outputUsagesToFile(usages, oldName, newName);
  console.log(`   📄 Review file: ${path.relative(PROJECT_ROOT, reviewFilePath)}`);

  if (reviewOnly) {
    console.log('\n' + '━'.repeat(80));
    console.log('📊 Review Only Mode - No changes made');
    console.log('━'.repeat(80));
    console.log(`\nOpen the review file to check each usage:`);
    console.log(`   ${reviewFilePath}`);
    console.log(`\nAfter review, run without --review-only to apply changes:`);
    console.log(`   npx tsx scripts/refactor-parameter.ts ${oldName} ${newName}`);
    console.log('━'.repeat(80));
    return;
  }

  // Step 2: Update Python file
  console.log('\n📝 Step 2: Updating Python parameters.py...');
  stats.pythonUpdates = await updatePythonFile(oldName, newName, dryRun);
  console.log(`   Found ${stats.pythonUpdates} references in Python file`);

  // Step 3: Update QMD files (including embedded Python code)
  console.log('\n📝 Step 3: Updating QMD files...');
  const qmdResult = await updateQmdFiles(oldName, newName, dryRun);
  stats.qmdUpdates = qmdResult.count;
  stats.filesModified = [...qmdResult.files];
  console.log(`   Found ${stats.qmdUpdates} references across ${qmdResult.files.length} files`);

  // Step 4: Update Python scripts (excluding parameters.py)
  console.log('\n📝 Step 4: Updating Python scripts...');
  const pyResult = await updatePythonScripts(oldName, newName, dryRun);
  stats.pyScriptUpdates = pyResult.count;
  stats.filesModified.push(...pyResult.files);
  console.log(`   Found ${stats.pyScriptUpdates} references across ${pyResult.files.length} files`);

  // Step 5: Update TypeScript files
  console.log('\n📝 Step 5: Updating TypeScript files...');
  const tsResult = await updateTypeScriptFiles(oldName, newName, dryRun);
  stats.tsUpdates = tsResult.count;
  stats.filesModified.push(...tsResult.files);
  console.log(`   Found ${stats.tsUpdates} references across ${tsResult.files.length} files`);

  if (stats.filesModified.length > 0) {
    console.log('\n   Modified files:');
    for (const file of stats.filesModified.slice(0, 15)) {
      console.log(`   - ${file}`);
    }
    if (stats.filesModified.length > 15) {
      console.log(`   ... and ${stats.filesModified.length - 15} more`);
    }
  }

  // Step 6: Regenerate variables
  console.log('\n📝 Step 6: Regenerating variables...');
  await regenerateVariables(dryRun);

  // Step 7: Validate no broken references
  console.log('\n📝 Step 7: Validating references...');
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
  console.log(`Usages found:      ${usages.length}`);
  console.log(`Python params:     ${stats.pythonUpdates}`);
  console.log(`QMD updates:       ${stats.qmdUpdates}`);
  console.log(`Python scripts:    ${stats.pyScriptUpdates}`);
  console.log(`TypeScript:        ${stats.tsUpdates}`);
  console.log(`Files modified:    ${stats.filesModified.length}`);
  console.log(`Warnings:          ${stats.warnings.length}`);
  console.log(`Review file:       ${path.relative(PROJECT_ROOT, reviewFilePath)}`);

  if (dryRun) {
    console.log('\n⚠️  DRY RUN - No files were actually modified');
    console.log('   Run without --dry-run to apply changes');
  } else {
    console.log('\n✅ Refactoring complete!');
    console.log(`   Review usages at: ${reviewFilePath}`);
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
