#!/usr/bin/env npx tsx
/**
 * Find all usages of a parameter name and its Quarto variable in the project.
 * Outputs a Markdown file with context and review checklist.
 *
 * Usage:
 *   npx tsx scripts/find-parameter-usages.ts PARAMETER_NAME
 *   npx tsx scripts/find-parameter-usages.ts DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT
 *   npx tsx scripts/find-parameter-usages.ts --all  # List all parameters
 */

import * as fs from 'fs';
import * as path from 'path';
import { fileURLToPath } from 'url';
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
  /^distribution-.*\.qmd$/,        // Distribution figures
  /^mc-distribution-.*\.qmd$/,     // MC distribution figures
  /^tornado-.*\.qmd$/,             // Tornado figures
  /^exceedance-.*\.qmd$/,          // Exceedance figures
  /^sensitivity-table-.*\.qmd$/,   // Sensitivity tables
];

function isExcludedFile(filePath: string): boolean {
  const fileName = path.basename(filePath);

  // Check exact matches
  if (EXCLUDE_FILES.includes(fileName)) {
    return true;
  }

  // Check prefixes
  for (const prefix of EXCLUDE_FILE_PREFIXES) {
    if (fileName.startsWith(prefix)) {
      return true;
    }
  }

  // Check patterns
  for (const pattern of EXCLUDE_FILE_PATTERNS) {
    if (pattern.test(fileName)) {
      return true;
    }
  }

  return false;
}

interface Usage {
  file: string;
  lineNumber: number;
  line: string;
  context: string[]; // Lines before and after
  matchType: 'parameter' | 'variable' | 'both';
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
      dot: false,          // Exclude hidden files
      followSymbolicLinks: false,
    });
    allFiles.push(...files);
  }

  // Deduplicate and filter out gitignored patterns
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
  } catch (e) {
    // No .gitignore or can't read it
  }

  // Filter files based on gitignore patterns
  return uniqueFiles.filter(filePath => {
    const relPath = path.relative(PROJECT_ROOT, filePath).replace(/\\/g, '/');
    for (const pattern of gitignorePatterns) {
      // Simple pattern matching - exact match or directory prefix
      if (pattern.endsWith('/')) {
        if (relPath.startsWith(pattern) || relPath.startsWith(pattern.slice(0, -1) + '/')) {
          return false;
        }
      } else if (relPath === pattern || relPath.startsWith(pattern + '/') || relPath.includes('/' + pattern)) {
        return false;
      }
      // Check if pattern matches any part of the path
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
        // Get context (2 lines before and after)
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
  } catch (e) {
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
    // Skip auto-generated files
    if (isExcludedFile(file)) {
      continue;
    }
    const usages = searchFileForPattern(file, patterns);
    allUsages.push(...usages);
  }

  // Sort by file, then line number
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
- **KEEP**: Usage refers to historical evidence (e.g., "The RECOVERY trial demonstrated...")
- **REPLACE**: Usage describes future/projected costs that should use a different parameter
- **UPDATE**: Usage needs modification for clarity or accuracy

**Process**:
1. Read each usage in context
2. Determine the appropriate action (KEEP/REPLACE/UPDATE)
3. Check the box when reviewed/addressed
4. Make necessary edits to the source files
5. After all usages are addressed, regenerate variables and re-render

**Note**: Auto-generated files are excluded from this report (they regenerate from parameters.py).

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

  // Group by file
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
      const typeEmoji = usage.matchType === 'parameter' ? '🔷' :
                        usage.matchType === 'variable' ? '🔶' : '🔷🔶';

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

  md += `---

## Legend

- 🔷 Parameter name (UPPERCASE) - typically in Python/TypeScript code
- 🔶 Variable name (lowercase) - typically in QMD files as \`{{< var ${varName} >}}\`
- 🔷🔶 Both forms appear in the same line

## Actions After Review

- [ ] All usages verified correct
- [ ] No stale references found
- [ ] Regenerated variables if needed
- [ ] Rendered and checked output
`;

  return md;
}

function listAllParameters(): void {
  const paramsFile = path.join(PROJECT_ROOT, 'dih_models', 'parameters.py');
  const content = fs.readFileSync(paramsFile, 'utf-8');

  // Match parameter definitions
  const paramRegex = /^([A-Z][A-Z0-9_]+)\s*=\s*Parameter\(/gm;
  const params: string[] = [];
  let match;

  while ((match = paramRegex.exec(content)) !== null) {
    params.push(match[1]);
  }

  console.log(`Found ${params.length} parameters:\n`);
  params.slice(0, 50).forEach(p => console.log(`  ${p}`));
  if (params.length > 50) {
    console.log(`  ... and ${params.length - 50} more`);
  }
  console.log(`\nUsage: npx tsx scripts/find-parameter-usages.ts PARAMETER_NAME`);
}

async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.log('Usage: npx tsx scripts/find-parameter-usages.ts PARAMETER_NAME');
    console.log('       npx tsx scripts/find-parameter-usages.ts --all');
    console.log('\nExample:');
    console.log('  npx tsx scripts/find-parameter-usages.ts DFDA_PRAGMATIC_TRIAL_COST_PER_PATIENT');
    process.exit(1);
  }

  if (args[0] === '--all') {
    listAllParameters();
    process.exit(0);
  }

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

  // Print summary
  console.log(`\nSummary:`);
  console.log(`  Parameter usages: ${usages.filter(u => u.matchType === 'parameter').length}`);
  console.log(`  Variable usages: ${usages.filter(u => u.matchType === 'variable').length}`);
  console.log(`  Both: ${usages.filter(u => u.matchType === 'both').length}`);
}

main().catch(console.error);
