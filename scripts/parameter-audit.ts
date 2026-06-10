#!/usr/bin/env npx tsx
/**
 * Unified Parameter Audit Tool
 * ============================
 *
 * Consolidated script for all parameter auditing needs:
 * - Find usages of a specific parameter
 * - Find unused parameters
 * - List all parameters
 *
 * Usage:
 *   npx tsx scripts/parameter-audit.ts PARAMETER_NAME         # Find usages of specific param
 *   npx tsx scripts/parameter-audit.ts --all                  # List all parameters
 *   npx tsx scripts/parameter-audit.ts --unused               # Find unused parameters
 *   npx tsx scripts/parameter-audit.ts --unused --json        # Output unused as JSON
 */

import * as fs from 'fs';
import * as path from 'path';
import { fileURLToPath, pathToFileURL } from 'url';
import { glob } from 'glob';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(__dirname, '..');

// File patterns to search
const SEARCH_GLOBS = [
  '**/*.qmd',
  '**/*.py',
  '**/*.ts',
  '**/*.yml',
  '**/*.yaml',
  '**/*.md',
];

// Directories to exclude
const EXCLUDE_DIRS = [
  'node_modules',
  '.git',
  '_book',
  '_freeze',
  '.quarto',
  '_site',
  '.venv',
  'venv',
  '_analysis',
];

// Auto-generated files to exclude (these are regenerated from parameters.py)
const EXCLUDE_FILES = [
  '_variables.yml',
  'parameters-calculations-citations.ts',
  'parameters-and-calculations.qmd',
  'OUTLINE-GENERATED.md',
  'OUTLINE-GENERATED.MD',
];

// Auto-generated review files to exclude
const EXCLUDE_FILE_PREFIXES = [
  'PARAMETER-REVIEW-',
  'REFACTOR-',
];

// Auto-generated file patterns to exclude
const EXCLUDE_FILE_PATTERNS = [
  /^distribution-.*\.qmd$/,
  /^mc-distribution-.*\.qmd$/,
  /^tornado-.*\.qmd$/,
  /^exceedance-.*\.qmd$/,
  /^sensitivity-table-.*\.qmd$/,
];

function isExcludedFile(filePath: string): boolean {
  const fileName = path.basename(filePath);

  if (EXCLUDE_FILES.includes(fileName)) return true;

  for (const prefix of EXCLUDE_FILE_PREFIXES) {
    if (fileName.startsWith(prefix)) return true;
  }

  for (const pattern of EXCLUDE_FILE_PATTERNS) {
    if (pattern.test(fileName)) return true;
  }

  return false;
}

interface Usage {
  file: string;
  lineNumber: number;
  line: string;
  context: string[];
  matchType: 'parameter' | 'variable' | 'both';
}

interface ParameterInfo {
  name: string;
  codeRefs: number;
  qmdFiles: string[];
  scriptFiles: string[];
  dependentParams: string[];
}

interface ClassifiedUsage {
  unused: string[];
  intermediate: { name: string; codeCount: number; deps: string[] }[];
  used: { name: string; totalRefs: number; files: string[] }[];
}

function toQuartoVariable(paramName: string): string {
  return paramName.toLowerCase();
}

async function getAllFiles(): Promise<string[]> {
  const allFiles: string[] = [];

  for (const pattern of SEARCH_GLOBS) {
    const files = await glob(pattern, {
      cwd: PROJECT_ROOT,
      ignore: EXCLUDE_DIRS.map(d => `${d}/**`),
      nodir: true,
      absolute: true,
      dot: false,
    });
    allFiles.push(...files);
  }

  const uniqueFiles = [...new Set(allFiles)];

  // Read .gitignore patterns
  const gitignorePath = path.join(PROJECT_ROOT, '.gitignore');
  let gitignorePatterns: string[] = [];
  try {
    const gitignoreContent = fs.readFileSync(gitignorePath, 'utf-8');
    gitignorePatterns = gitignoreContent
      .split('\n')
      .map(line => line.trim())
      .filter(line => line && !line.startsWith('#'));
  } catch {
    // No .gitignore or can't read it
  }

  return uniqueFiles.filter(filePath => {
    const relPath = path.relative(PROJECT_ROOT, filePath).replace(/\\/g, '/');
    for (const pattern of gitignorePatterns) {
      if (pattern.endsWith('/')) {
        if (relPath.startsWith(pattern) || relPath.startsWith(pattern.slice(0, -1) + '/')) {
          return false;
        }
      } else if (relPath === pattern || relPath.startsWith(pattern + '/') || relPath.includes('/' + pattern)) {
        return false;
      }
      if (pattern.includes('*')) {
        const regexPattern = pattern.replace(/\*/g, '.*').replace(/\?/g, '.');
        if (new RegExp(regexPattern).test(relPath)) {
          return false;
        }
      }
    }
    return true;
  });
}

function searchFileForPattern(filePath: string, patterns: string[]): Usage[] {
  const usages: Usage[] = [];

  try {
    const content = fs.readFileSync(filePath, 'utf-8');
    const lines = content.split('\n');

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      const lineNumber = i + 1;

      let matchType: 'parameter' | 'variable' | 'both' | null = null;
      const hasParam = patterns[0] && line.includes(patterns[0]);
      const hasVar = patterns[1] && line.toLowerCase().includes(patterns[1].toLowerCase());

      if (hasParam && hasVar) {
        matchType = 'both';
      } else if (hasParam) {
        matchType = 'parameter';
      } else if (hasVar) {
        matchType = 'variable';
      }

      if (matchType) {
        const contextLines = 2;
        const start = Math.max(0, i - contextLines);
        const end = Math.min(lines.length, i + contextLines + 1);

        const context: string[] = [];
        for (let j = start; j < end; j++) {
          const prefix = j === i ? '>>> ' : '    ';
          context.push(`${prefix}${j + 1}: ${lines[j]}`);
        }

        const relPath = path.relative(PROJECT_ROOT, filePath);
        usages.push({
          file: relPath,
          lineNumber,
          line: line.trim(),
          context,
          matchType,
        });
      }
    }
  } catch {
    // Skip files that can't be read
  }

  return usages;
}

async function findParameterUsages(paramName: string): Promise<Usage[]> {
  const varName = toQuartoVariable(paramName);
  const patterns = [paramName, varName !== paramName ? varName : ''];

  console.log(`  Searching for: ${paramName}`);
  if (varName !== paramName) {
    console.log(`  Also searching for: ${varName}`);
  }

  const files = await getAllFiles();
  console.log(`  Scanning ${files.length} files...`);

  const allUsages: Usage[] = [];

  for (const file of files) {
    if (isExcludedFile(file)) continue;
    const usages = searchFileForPattern(file, patterns);
    allUsages.push(...usages);
  }

  allUsages.sort((a, b) => {
    const fileCompare = a.file.localeCompare(b.file);
    if (fileCompare !== 0) return fileCompare;
    return a.lineNumber - b.lineNumber;
  });

  return allUsages;
}

function generateMarkdown(paramName: string, usages: Usage[]): string {
  const varName = toQuartoVariable(paramName);
  const now = new Date().toISOString().split('T')[0];

  let md = `# Parameter Usage Review: ${paramName}

Generated: ${now}

---

## Review Instructions

**Purpose**: Review each usage of \`${paramName}\` / \`${varName}\` to determine if it should:
- **KEEP**: Usage refers to historical evidence
- **REPLACE**: Usage describes future/projected costs that should use a different parameter
- **UPDATE**: Usage needs modification for clarity or accuracy

---

## Summary

- **Parameter Name**: \`${paramName}\`
- **Quarto Variable**: \`${varName}\`
- **Total Usages Found**: ${usages.length}

## Usage Types

| Type | Count |
|------|-------|
| Parameter (UPPERCASE) | ${usages.filter(u => u.matchType === 'parameter').length} |
| Variable (lowercase) | ${usages.filter(u => u.matchType === 'variable').length} |
| Both in same line | ${usages.filter(u => u.matchType === 'both').length} |

---

## Review Checklist

`;

  const byFile = new Map<string, Usage[]>();
  for (const usage of usages) {
    const existing = byFile.get(usage.file) || [];
    existing.push(usage);
    byFile.set(usage.file, existing);
  }

  let usageIndex = 1;
  for (const [file, fileUsages] of byFile) {
    md += `### ${file}\n\n`;

    for (const usage of fileUsages) {
      const typeEmoji = usage.matchType === 'parameter' ? '>' :
                        usage.matchType === 'variable' ? '<' : '<>';

      md += `#### ${usageIndex}. Line ${usage.lineNumber} ${typeEmoji}

- [ ] Reviewed

**Match**: \`${usage.line.substring(0, 100)}${usage.line.length > 100 ? '...' : ''}\`

<details>
<summary>Context</summary>

\`\`\`
${usage.context.join('\n')}
\`\`\`

</details>

`;
      usageIndex++;
    }
  }

  return md;
}

// ==================== UNUSED PARAMETERS MODE ====================

export function extractParameterNames(content: string): Set<string> {
  const params = new Set<string>();
  const paramRegex = /^([A-Z][A-Z0-9_]+)\s*=\s*Parameter\(/gm;
  let match;

  while ((match = paramRegex.exec(content)) !== null) {
    params.add(match[1]);
  }

  const aliasRegex = /^([A-Z][A-Z0-9_]+)\s*=\s*([A-Z][A-Z0-9_]+)\b/gm;
  let changed = true;
  while (changed) {
    changed = false;
    aliasRegex.lastIndex = 0;
    while ((match = aliasRegex.exec(content)) !== null) {
      const aliasName = match[1];
      const targetName = match[2];
      if (!params.has(aliasName) && params.has(targetName)) {
        params.add(aliasName);
        changed = true;
      }
    }
  }

  return params;
}

function getAllParameters(): Set<string> {
  const paramsFile = path.join(PROJECT_ROOT, 'dih_models', 'parameters.py');
  const content = fs.readFileSync(paramsFile, 'utf-8');
  return extractParameterNames(content);
}

function addDependent(dependents: Map<string, string[]>, inputParam: string, dependentParam: string): void {
  const existing = dependents.get(inputParam) || [];
  if (!existing.includes(dependentParam)) {
    existing.push(dependentParam);
  }
  dependents.set(inputParam, existing);
}

export function findDependentsInSource(content: string, allParams: Set<string>): Map<string, string[]> {
  const lines = content.split('\n');

  const dependents = new Map<string, string[]>();

  // Find parameter definition blocks
  let i = 0;
  while (i < lines.length) {
    const line = lines[i];
    const match = line.match(/^([A-Z][A-Z0-9_]+)\s*=\s*Parameter\s*\(/);

    if (match) {
      const paramName = match[1];
      let depth = 0;
      const blockLines: string[] = [];
      let inParam = false;

      // Collect the full Parameter(...) block
      for (let j = i; j < lines.length; j++) {
        const currentLine = lines[j];
        blockLines.push(currentLine);

        for (const char of currentLine) {
          if (char === '(') {
            depth++;
            inParam = true;
          } else if (char === ')') {
            depth--;
          }
        }

        if (inParam && depth === 0) {
          i = j + 1;
          break;
        }
      }

      const blockText = blockLines.join('\n');

      // Find references to other parameters in this block
      for (const otherParam of allParams) {
        if (otherParam === paramName) continue;
        if (new RegExp(`\\b${otherParam}\\b`).test(blockText)) {
          addDependent(dependents, otherParam, paramName);
        }
      }
    } else {
      i++;
    }
  }

  const aliasRegex = /^([A-Z][A-Z0-9_]+)\s*=\s*([A-Z][A-Z0-9_]+)\b/gm;
  let match;
  while ((match = aliasRegex.exec(content)) !== null) {
    const aliasName = match[1];
    const targetName = match[2];
    if (allParams.has(aliasName) && allParams.has(targetName) && aliasName !== targetName) {
      addDependent(dependents, targetName, aliasName);
    }
  }

  return dependents;
}

function findDependents(allParams: Set<string>): Map<string, string[]> {
  const paramsFile = path.join(PROJECT_ROOT, 'dih_models', 'parameters.py');
  const content = fs.readFileSync(paramsFile, 'utf-8');
  return findDependentsInSource(content, allParams);
}

export function classifyParameterUsage({
  allParams,
  dependents,
  qmdRefs,
  scriptRefs,
  codeRefs,
}: {
  allParams: Set<string>;
  dependents: Map<string, string[]>;
  qmdRefs: Map<string, string[]>;
  scriptRefs: Map<string, string[]>;
  codeRefs: Map<string, number>;
}): ClassifiedUsage {
  const unused: string[] = [];
  const intermediate: { name: string; codeCount: number; deps: string[] }[] = [];
  const used: { name: string; totalRefs: number; files: string[] }[] = [];

  for (const param of allParams) {
    const codeCount = codeRefs.get(param) || 0;
    const qmdFiles = qmdRefs.get(param) || [];
    const pyFiles = scriptRefs.get(param) || [];
    const deps = dependents.get(param) || [];

    const allExternal = [...new Set([...qmdFiles, ...pyFiles])];
    const totalExternal = allExternal.length;
    const dependencyCount = deps.length > 0 ? deps.length : codeCount;

    if (dependencyCount === 0 && totalExternal === 0) {
      unused.push(param);
    } else if (totalExternal === 0) {
      intermediate.push({ name: param, codeCount: dependencyCount, deps });
    } else {
      used.push({ name: param, totalRefs: totalExternal, files: allExternal.slice(0, 5) });
    }
  }

  unused.sort();
  intermediate.sort((a, b) => a.codeCount - b.codeCount);
  used.sort((a, b) => b.totalRefs - a.totalRefs);

  return { unused, intermediate, used };
}

async function findUnusedParameters(jsonOutput: boolean = false): Promise<void> {
  const log = (...args: unknown[]) => {
    const message = args.map(String).join(' ');
    if (jsonOutput) {
      console.error(message);
    } else {
      console.log(message);
    }
  };
  const progressOutput = jsonOutput ? process.stderr : process.stdout;

  log('=' .repeat(80));
  log('PARAMETER USAGE ANALYSIS');
  log('='.repeat(80));
  log();

  log('[1/4] Extracting all parameters from parameters.py...');
  const allParams = getAllParameters();
  log(`      Found ${allParams.size} parameters`);
  log();

  log('[2/4] Analyzing parameter dependencies...');
  const dependents = findDependents(allParams);
  log('      Dependency analysis complete!');
  log();

  log('[3/4] Scanning for parameter usages...');
  const files = await getAllFiles();

  // Track usages
  const codeRefs = new Map<string, number>();
  const qmdRefs = new Map<string, string[]>();
  const scriptRefs = new Map<string, string[]>();

  // Initialize
  for (const param of allParams) {
    codeRefs.set(param, 0);
    qmdRefs.set(param, []);
    scriptRefs.set(param, []);
  }

  // Scan parameters.py for internal references
  const paramsFile = path.join(PROJECT_ROOT, 'dih_models', 'parameters.py');
  const paramsContent = fs.readFileSync(paramsFile, 'utf-8');

  for (const param of allParams) {
    // Count refs excluding definition line
    const pattern = new RegExp(`\\b${param}\\b(?!\\s*=\\s*Parameter)`, 'g');
    const matches = paramsContent.match(pattern) || [];
    codeRefs.set(param, matches.length);
  }

  // Scan other files
  let scannedCount = 0;
  for (const file of files) {
    if (isExcludedFile(file)) continue;
    if (file.endsWith('parameters.py')) continue;

    scannedCount++;
    if (scannedCount % 100 === 0) {
      progressOutput.write(`      Scanned ${scannedCount} files...\r`);
    }

    try {
      const content = fs.readFileSync(file, 'utf-8');
      const relPath = path.relative(PROJECT_ROOT, file).replace(/\\/g, '/');
      const isQmd = file.endsWith('.qmd');
      const isPy = file.endsWith('.py');
      const isTs = file.endsWith('.ts');

      // Check for variable references in QMD: {{< var param_name >}}
      if (isQmd) {
        const varPattern = /\{\{<\s*var\s+([a-z][a-z0-9_]+)\s*>\}\}/gi;
        let match;
        while ((match = varPattern.exec(content)) !== null) {
          const varName = match[1].toLowerCase();
          // Map back to parameter name
          let paramName = varName.toUpperCase();
          if (varName.endsWith('_latex')) {
            paramName = varName.slice(0, -6).toUpperCase();
          } else if (varName.endsWith('_cite')) {
            paramName = varName.slice(0, -5).toUpperCase();
          }

          if (allParams.has(paramName)) {
            const existing = qmdRefs.get(paramName) || [];
            if (!existing.includes(relPath)) {
              existing.push(relPath);
              qmdRefs.set(paramName, existing);
            }
          }
        }
      }

      // Check for direct parameter usage in Python/TS that imports from parameters
      if ((isPy || isTs || isQmd) && content.includes('from dih_models.parameters import')) {
        for (const param of allParams) {
          if (new RegExp(`\\b${param}\\b`).test(content)) {
            const existing = scriptRefs.get(param) || [];
            if (!existing.includes(relPath)) {
              existing.push(relPath);
              scriptRefs.set(param, existing);
            }
          }
        }
      }
    } catch {
      // Skip unreadable files
    }
  }
  log(`      Scanned ${scannedCount} files                `);
  log();

  // Categorize parameters
  log('[4/4] Categorizing parameters...');

  const { unused, intermediate, used } = classifyParameterUsage({
    allParams,
    dependents,
    qmdRefs,
    scriptRefs,
    codeRefs,
  });

  // Output results
  log();
  log('RESULTS:');
  log();

  if (jsonOutput) {
    const result = {
      unused: unused,
      intermediate: intermediate.map(i => i.name),
      used: used.map(u => u.name),
      summary: {
        total: allParams.size,
        unused: unused.length,
        intermediate: intermediate.length,
        used: used.length,
      }
    };
    process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
    return;
  }

  if (unused.length > 0) {
    console.log(`COMPLETELY UNUSED (${unused.length} parameters):`);
    console.log('   These are not referenced anywhere - safe to delete!');
    console.log('-'.repeat(80));
    for (const param of unused) {
      console.log(`   - ${param}`);
    }
    console.log();
  } else {
    console.log('No completely unused parameters found!');
    console.log();
  }

  if (intermediate.length > 0) {
    console.log(`INTERMEDIATE CALCULATION VALUES (${intermediate.length} parameters):`);
    console.log('   Used in other parameter formulas, not displayed in documents.');
    console.log('-'.repeat(80));

    const singleUse = intermediate.filter(i => i.codeCount === 1);
    const multiUse = intermediate.filter(i => i.codeCount > 1);

    if (singleUse.length > 0) {
      console.log();
      console.log(`   SINGLE-USE (${singleUse.length} params) - could potentially inline:`);
      for (const item of singleUse.slice(0, 15)) {
        const depStr = item.deps[0] || 'unknown';
        console.log(`      - ${item.name}`);
        console.log(`        used by: ${depStr}`);
      }
      if (singleUse.length > 15) {
        console.log(`      ... and ${singleUse.length - 15} more`);
      }
    }

    if (multiUse.length > 0) {
      console.log();
      console.log(`   MULTI-USE (${multiUse.length} params) - keep these (reused across formulas):`);
      for (const item of multiUse.slice(0, 10)) {
        const depList = item.deps.slice(0, 3).join(', ') + (item.deps.length > 3 ? ` (+${item.deps.length - 3} more)` : '');
        console.log(`      - ${item.name} (${item.codeCount}x)`);
        console.log(`        used by: ${depList}`);
      }
      if (multiUse.length > 10) {
        console.log(`      ... and ${multiUse.length - 10} more`);
      }
    }
    console.log();
  }

  console.log(`ACTIVELY DISPLAYED (${used.length} parameters):`);
  console.log('   Used in QMD files or scripts - these appear in output documents.');
  console.log('-'.repeat(80));
  console.log('   Top 10 most referenced:');
  for (const item of used.slice(0, 10)) {
    const fileList = item.files.map(f => path.basename(f)).slice(0, 3).join(', ') +
                     (item.files.length > 3 ? ', ...' : '');
    console.log(`      - ${item.name}: ${item.totalRefs} files`);
    console.log(`        ${fileList}`);
  }
  if (used.length > 10) {
    console.log(`      ... and ${used.length - 10} more`);
  }
  console.log();

  // Summary
  console.log('='.repeat(80));
  console.log('SUMMARY');
  console.log('='.repeat(80));
  console.log();
  console.log(`  Total parameters:              ${allParams.size}`);
  console.log(`  Completely unused:             ${unused.length} (can delete)`);
  console.log(`  Intermediate (calc only):      ${intermediate.length} (required for formulas)`);
  console.log(`  Actively displayed:            ${used.length} (appear in documents)`);
  console.log();

  if (unused.length > 0) {
    console.log(`Action: ${unused.length} unused parameters can be deleted`);
  } else {
    console.log('No unused parameters - codebase is clean!');
  }
}

function listAllParameters(): void {
  const params = getAllParameters();
  const sorted = Array.from(params).sort();

  console.log(`Found ${params.size} parameters:\n`);
  sorted.slice(0, 50).forEach(p => console.log(`  ${p}`));
  if (params.size > 50) {
    console.log(`  ... and ${params.size - 50} more`);
  }
  console.log(`\nUsage: npx tsx scripts/parameter-audit.ts PARAMETER_NAME`);
}

async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.log('Parameter Audit Tool');
    console.log('====================\n');
    console.log('Usage:');
    console.log('  npx tsx scripts/parameter-audit.ts PARAMETER_NAME   # Find usages of specific param');
    console.log('  npx tsx scripts/parameter-audit.ts --all            # List all parameters');
    console.log('  npx tsx scripts/parameter-audit.ts --unused         # Find unused parameters');
    console.log('  npx tsx scripts/parameter-audit.ts --unused --json  # Output unused as JSON');
    console.log('\nExample:');
    console.log('  npx tsx scripts/parameter-audit.ts DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT');
    process.exit(1);
  }

  if (args[0] === '--all') {
    listAllParameters();
    process.exit(0);
  }

  if (args[0] === '--unused') {
    const jsonOutput = args.includes('--json');
    await findUnusedParameters(jsonOutput);
    process.exit(0);
  }

  // Find usages of specific parameter
  const paramName = args[0].toUpperCase();
  console.log(`\nSearching for usages of ${paramName}...\n`);

  const usages = await findParameterUsages(paramName);

  if (usages.length === 0) {
    console.log(`\nNo usages found for ${paramName}`);
    process.exit(0);
  }

  console.log(`\nFound ${usages.length} usages`);

  const markdown = generateMarkdown(paramName, usages);
  const outputFile = path.join(PROJECT_ROOT, `PARAMETER-REVIEW-${paramName}.md`);

  fs.writeFileSync(outputFile, markdown);
  console.log(`\nOutput written to: ${outputFile}`);

  console.log(`\nSummary:`);
  console.log(`  Parameter usages: ${usages.filter(u => u.matchType === 'parameter').length}`);
  console.log(`  Variable usages: ${usages.filter(u => u.matchType === 'variable').length}`);
  console.log(`  Both: ${usages.filter(u => u.matchType === 'both').length}`);
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  main().catch(console.error);
}
