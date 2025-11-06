#!/usr/bin/env npx tsx
/**
 * Parameterize All QMD Files in Project
 *
 * Automatically replaces hardcoded economic values in ALL .qmd files with
 * inline Python expressions from economic_parameters.py
 *
 * Processes all .qmd files in the entire project, including:
 * - Root-level files (index.qmd, etc.)
 * - brain/book/ directory and subdirectories
 * - brain/book/figures/ directory
 *
 * Usage: npx tsx scripts/parameterize-all-files.ts
 *
 * Review changes with: git diff
 * Revert if needed: git checkout .
 */

import * as fs from 'fs';
import * as path from 'path';
import { getProjectRoot } from './lib/file-utils';

// Get project root reliably, regardless of where the script is run from
const ROOT_DIR = getProjectRoot();

// Parameter mapping: pattern -> { param: string, format?: string }
// format can be: 'billions', 'millions', 'roi', 'percentage', 'qalys', 'currency', 'number'
const PARAMETER_MAPPINGS = [
  // Dollar amounts in billions
  { pattern: /\$2,718B|\$2\.7T|\$2,718 billion/gi, param: 'MILITARY_SPENDING', format: 'billions' },
  { pattern: /\$11,355B|\$11\.4T/gi, param: 'TOTAL_WAR_COST', format: 'billions' },
  { pattern: /\$114B|\$114 billion/gi, param: 'SOCIETAL_DIVIDEND', format: 'billions' },
  { pattern: /\$113\.55B/gi, param: 'SOCIETAL_DIVIDEND', format: 'billions' },
  { pattern: /\$27\.18B|\$27B|\$27 billion/gi, param: 'CAPTURED_DIVIDEND', format: 'billions' },
  { pattern: /\$50B|\$50 billion/gi, param: 'DFDA_GROSS_SAVINGS', format: 'billions', context: 'R&D|savings|trial' },
  { pattern: /\$100B|\$100 billion/gi, param: 'GLOBAL_TRIAL_MARKET', format: 'billions', context: 'trial|market|R&D' },
  { pattern: /\$164B|\$164 billion/gi, param: 'TOTAL_ANNUAL_BENEFITS', format: 'billions' },
  { pattern: /\$163\.7B/gi, param: 'NET_ANNUAL_BENEFIT', format: 'billions' },
  { pattern: /\$1\.22T|\$1\.22 trillion|\$1,222B/gi, param: 'TOTAL_COMPLETE_BENEFITS', format: 'billions' },
  { pattern: /\$16\.5T|\$16\.5 trillion/gi, param: 'TOTAL_ENDGAME_BENEFITS', format: 'billions' },

  // Dollar amounts in millions
  { pattern: /\$40M|\$40 million/gi, param: 'DFDA_ANNUAL_OPEX', format: 'millions' },
  { pattern: /\$290M|\$290 million/gi, param: 'TOTAL_ANNUAL_COSTS', format: 'millions' },
  { pattern: /\$1B|\$1 billion/gi, param: 'CAMPAIGN_TOTAL_COST', format: 'billions', context: 'campaign|raise' },
  { pattern: /\$2\.7B|\$2\.718B/gi, param: 'VICTORY_BOND_ANNUAL_PAYOUT', format: 'billions', context: 'bond|payout' },

  // ROI values
  { pattern: /\b463:1\b/g, param: 'ROI_TIER_1_CONSERVATIVE', format: 'roi' },
  { pattern: /\b1,222:1\b/g, param: 'ROI_TIER_2_COMPLETE', format: 'roi' },
  { pattern: /\b25,781:1\b/g, param: 'ROI_TIER_3_ENDGAME', format: 'roi' },
  { pattern: /\b1,250:1\b/g, param: 'DFDA_ROI_SIMPLE', format: 'roi' },

  // Percentages
  { pattern: /\b270%/g, param: 'VICTORY_BOND_ANNUAL_RETURN_PCT', format: 'percentage' },
  { pattern: /\b8%/g, param: 'DISCOUNT_RATE', format: 'percentage', context: 'discount|NPV' },
  { pattern: /\b50%/g, param: 'TRIAL_COST_REDUCTION_PCT', format: 'percentage', context: 'trial|reduction|cost' },

  // Other numbers
  { pattern: /\b82[xX]\b/g, param: 'TRIAL_COST_REDUCTION_FACTOR', format: 'number', suffix: 'x' },
  { pattern: /\b840,000 QALYs?/gi, param: 'DFDA_QALYS_ANNUAL', format: 'qalys' },
  { pattern: /\b925,610 QALYs?/gi, param: 'TOTAL_QALYS_ANNUAL', format: 'qalys' },
  { pattern: /\b-\$176,382/g, param: 'ICER_PER_QALY', format: 'currency' },
  { pattern: /\b-\$6\.56M/g, param: 'COST_PER_LIFE_SAVED', format: 'number', prefix: '-$', suffix: 'M' },
];

const PYTHON_IMPORT_BLOCK = `\`\`\`{python}
#| echo: false
import sys
import os

# Quarto executes from project root (execute-dir: project in _book.yml)
appendix_path = os.path.join(os.getcwd(), 'brain', 'book', 'appendix')
if appendix_path not in sys.path:
    sys.path.insert(0, appendix_path)

from economic_parameters import *
\`\`\``;

function hasJupyterKernel(content: string): boolean {
  return /^jupyter:\s*dih-project-kernel/m.test(content);
}

function hasPythonImport(content: string): boolean {
  return /from economic_parameters import \*/m.test(content);
}

function addJupyterKernel(content: string): string {
  const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (frontmatterMatch) {
    const frontmatter = frontmatterMatch[1];
    if (!hasJupyterKernel(frontmatter)) {
      const newFrontmatter = frontmatter + '\njupyter: dih-project-kernel';
      return content.replace(/^---\n[\s\S]*?\n---/, `---\n${newFrontmatter}\n---`);
    }
  }
  return content;
}

function addPythonImport(content: string): string {
  if (hasPythonImport(content)) {
    return content;
  }

  const frontmatterMatch = content.match(/^---\n[\s\S]*?\n---/);
  if (frontmatterMatch) {
    const afterFrontmatter = content.slice(frontmatterMatch[0].length);
    return frontmatterMatch[0] + '\n\n' + PYTHON_IMPORT_BLOCK + '\n' + afterFrontmatter;
  }

  return PYTHON_IMPORT_BLOCK + '\n\n' + content;
}

function formatParameter(param: string, format?: string, prefix?: string, suffix?: string): string {
  switch (format) {
    case 'billions':
      return `\`{python} format_billions(${param})\``;
    case 'millions':
      return `\`{python} format_millions(${param})\``;
    case 'roi':
      return `\`{python} format_roi(${param})\``;
    case 'percentage':
      return `\`{python} format_percentage(${param})\``;
    case 'qalys':
      return `\`{python} format_qalys(${param})\` QALYs`;
    case 'currency':
      return `\`{python} format_currency(${param})\``;
    case 'number':
      const pre = prefix || '';
      const suf = suffix || '';
      return `${pre}\`{python} ${param}\`${suf}`;
    default:
      return `\`{python} ${param}\``;
  }
}

function checkContext(line: string, context?: string): boolean {
  if (!context) return true;
  const contextRegex = new RegExp(context, 'i');
  return contextRegex.test(line);
}

function replaceParameters(content: string): { content: string; changes: number } {
  const lines = content.split('\n');
  let changes = 0;
  let inCodeBlock = false;
  let inFrontmatter = false;
  let frontmatterCount = 0;

  const newLines = lines.map((line) => {
    // Track code blocks
    if (line.trim().startsWith('```')) {
      inCodeBlock = !inCodeBlock;
      return line;
    }

    // Track frontmatter
    if (line.trim() === '---') {
      frontmatterCount++;
      if (frontmatterCount <= 2) {
        inFrontmatter = frontmatterCount === 1;
      }
      return line;
    }

    // Skip processing if in code block or frontmatter
    if (inCodeBlock || inFrontmatter) {
      return line;
    }

    let modifiedLine = line;

    // Try each pattern
    for (const mapping of PARAMETER_MAPPINGS) {
      if (mapping.pattern.test(modifiedLine)) {
        // Check context if specified
        if (!checkContext(modifiedLine, mapping.context)) {
          continue;
        }

        const replacement = formatParameter(
          mapping.param,
          mapping.format,
          (mapping as any).prefix,
          (mapping as any).suffix
        );
        const beforeReplace = modifiedLine;
        modifiedLine = modifiedLine.replace(mapping.pattern, replacement);

        if (beforeReplace !== modifiedLine) {
          changes++;
        }

        // Reset regex lastIndex
        mapping.pattern.lastIndex = 0;
      }
    }

    return modifiedLine;
  });

  return {
    content: newLines.join('\n'),
    changes
  };
}

function processFile(filePath: string): number {
  console.log(`Processing: ${path.relative(process.cwd(), filePath)}`);

  let content = fs.readFileSync(filePath, 'utf-8');
  let totalChanges = 0;

  // Step 1: Add Jupyter kernel if needed
  if (!hasJupyterKernel(content)) {
    console.log('  ✓ Adding jupyter: dih-project-kernel');
    content = addJupyterKernel(content);
    totalChanges++;
  }

  // Step 2: Add Python import if needed
  if (!hasPythonImport(content)) {
    console.log('  ✓ Adding Python import block');
    content = addPythonImport(content);
    totalChanges++;
  }

  // Step 3: Replace parameters
  const result = replaceParameters(content);
  totalChanges += result.changes;

  if (result.changes > 0) {
    console.log(`  ✓ Replaced ${result.changes} hardcoded values`);
  }

  if (totalChanges === 0) {
    console.log('  • No changes needed');
    return 0;
  }

  // Write changes
  fs.writeFileSync(filePath, result.content, 'utf-8');
  console.log(`  ✅ Saved ${totalChanges} changes\n`);
  return totalChanges;
}

function findQmdFiles(dir: string): string[] {
  const files: string[] = [];

  if (!fs.existsSync(dir)) {
    return files;
  }

  const items = fs.readdirSync(dir);

  for (const item of items) {
    const fullPath = path.join(dir, item);
    const stat = fs.statSync(fullPath);

    if (stat.isDirectory()) {
      files.push(...findQmdFiles(fullPath));
    } else if (item.endsWith('.qmd') && !item.includes('_files')) {
      files.push(fullPath);
    }
  }

  return files;
}

async function main() {
  console.log('========================================');
  console.log('Parameterize ALL QMD Files in Project');
  console.log('========================================\n');

  const projectRoot = ROOT_DIR;

  // Process ALL .qmd files in the entire project
  const filesToProcess = findQmdFiles(projectRoot);

  console.log(`Found ${filesToProcess.length} .qmd files in project\n`);

  let totalChanges = 0;
  for (const file of filesToProcess) {
    totalChanges += processFile(file);
  }

  console.log('========================================');
  console.log('Done!');
  console.log(`Modified ${totalChanges} values across ${filesToProcess.length} files`);
  console.log('\n💡 Review changes: git diff');
  console.log('========================================\n');
}

main().catch(error => {
  console.error('Error:', error);
  process.exit(1);
});
