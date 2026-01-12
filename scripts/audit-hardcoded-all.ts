#!/usr/bin/env node
/**
 * Audit all QMD files for hardcoded values and generate replacement report
 * Usage: npx tsx scripts/audit-hardcoded-all.ts [--output report.md]
 *
 * Features:
 * - Semantic context matching (uses variable name keywords to disambiguate)
 * - Confidence scoring (high/medium/low based on context match quality)
 * - Better unit normalization ($2.6 billion = $2.6B = $2,600,000,000)
 * - Uses findFiles from file-utils to exclude auto-generated files
 */
import * as fs from 'fs';
import * as path from 'path';
import yaml from 'js-yaml';
import { findFiles } from './lib/file-utils';

interface Variable {
  name: string;
  displayValue: string;
  normalizedValue: string;
  numericValue: number | null;
  keywords: string[];  // Extracted from variable name for semantic matching
  unitType: 'currency' | 'percentage' | 'count' | 'other';
}

interface LatexVariable {
  name: string;  // e.g., "treaty_annual_funding_latex"
  baseName: string;  // e.g., "treaty_annual_funding"
  preview: string;  // First 80 chars of the LaTeX content
}

interface HardcodedLatexBlock {
  file: string;
  startLine: number;
  endLine: number;
  content: string;
  preview: string;
  suggestedVar?: string;
}

interface HardcodedMatch {
  file: string;
  line: number;
  value: string;
  context: string;
  hasExistingVar: boolean;
  inCodeBlock: boolean;  // Whether this is inside a Python/code block
  inLatexBlock: boolean;  // Whether this is inside a $$ LaTeX block
}

// Parse command line args
const args = process.argv.slice(2);
const outputFile = args.includes('--output')
  ? args[args.indexOf('--output') + 1]
  : '_hardcoded-audit-report.md';

// Extract keywords from variable name (e.g., "treaty_annual_funding" -> ["treaty", "annual", "funding"])
function extractKeywords(varName: string): string[] {
  return varName
    .toLowerCase()
    .split('_')
    .filter(w => w.length > 2 && !['the', 'and', 'per', 'pct', 'usd', 'annual'].includes(w));
}

// Normalize value for comparison - handles multiple formats
function normalize(val: string): string {
  let result = val
    .toLowerCase()
    .replace(/[,\s]/g, '')
    .replace(/\$/, '')
    .replace(/trillion/i, 't')
    .replace(/billion/i, 'b')
    .replace(/million/i, 'm')
    .replace(/thousand/i, 'k');

  // Normalize trailing units: "27.2b" -> "27.2b"
  return result;
}

// Convert to numeric value for comparison (e.g., "$2.6B" -> 2600000000)
function toNumeric(val: string): number | null {
  const normalized = normalize(val);

  // Extract number and suffix
  const match = normalized.match(/^([\d.]+)([kmbt])?$/);
  if (!match) return null;

  const num = parseFloat(match[1]);
  const suffix = match[2];

  const multipliers: Record<string, number> = {
    'k': 1e3,
    'm': 1e6,
    'b': 1e9,
    't': 1e12
  };

  return suffix ? num * multipliers[suffix] : num;
}

// Check if two numeric values are approximately equal (within 5%)
function approxEqual(a: number | null, b: number | null): boolean {
  if (a === null || b === null) return false;
  if (a === 0 && b === 0) return true;
  const ratio = a / b;
  return ratio >= 0.95 && ratio <= 1.05;
}

// Extract display value from HTML
function extractDisplayValue(html: string): string {
  return html
    .replace(/<[^>]+>/g, '')
    .replace(/&amp;/g, '&')
    .trim()
    .split(' ')[0]; // Get just the value part, not confidence interval
}

// Detect unit type from value and variable name
function detectUnitType(displayValue: string, varName: string): 'currency' | 'percentage' | 'count' | 'other' {
  if (displayValue.includes('$')) return 'currency';
  if (displayValue.includes('%') || varName.includes('_pct') || varName.includes('_rate')) return 'percentage';
  // Count types based on name patterns
  if (varName.includes('_count') || varName.includes('_patients') || varName.includes('deaths') ||
      varName.includes('_trials') || varName.includes('_drugs') || varName.includes('_diseases') ||
      varName.includes('_people') || varName.includes('_years') || varName.includes('_days')) {
    return 'count';
  }
  return 'other';
}

// Detect unit type from hardcoded value
function detectHardcodedUnitType(value: string): 'currency' | 'percentage' | 'count' | 'other' {
  if (value.includes('$')) return 'currency';
  if (value.includes('%')) return 'percentage';
  // Plain numbers are counts
  if (/^[\d,]+$/.test(value)) return 'count';
  return 'other';
}

// Load variables from _variables.yml
function loadVariables(): Variable[] {
  const content = fs.readFileSync('_variables.yml', 'utf-8');
  const parsed = yaml.load(content) as Record<string, string>;

  const vars: Variable[] = [];
  for (const [name, value] of Object.entries(parsed)) {
    if (typeof value === 'string' && !name.endsWith('_cite') && !name.endsWith('_latex')) {
      const displayValue = extractDisplayValue(value);
      vars.push({
        name,
        displayValue,
        normalizedValue: normalize(displayValue),
        numericValue: toNumeric(displayValue),
        keywords: extractKeywords(name),
        unitType: detectUnitType(displayValue, name)
      });
    }
  }
  return vars;
}

// Load LaTeX variables from _variables.yml
function loadLatexVariables(): LatexVariable[] {
  const content = fs.readFileSync('_variables.yml', 'utf-8');
  const parsed = yaml.load(content) as Record<string, string>;

  const vars: LatexVariable[] = [];
  for (const [name, value] of Object.entries(parsed)) {
    if (typeof value === 'string' && name.endsWith('_latex')) {
      const baseName = name.replace(/_latex$/, '');
      // Extract preview - first meaningful line of the LaTeX
      const preview = value
        .replace(/^\$\$\n?/, '')
        .replace(/\\begin\{aligned\}\n?/, '')
        .split('\n')[0]
        .substring(0, 80);
      vars.push({ name, baseName, preview });
    }
  }
  return vars;
}

// Find hardcoded LaTeX blocks in content
function findHardcodedLatexBlocks(content: string, filePath: string): HardcodedLatexBlock[] {
  const blocks: HardcodedLatexBlock[] = [];
  const lines = content.split('\n');

  let inLatexBlock = false;
  let blockStart = 0;
  let blockContent: string[] = [];

  lines.forEach((line, idx) => {
    if (line.trim() === '$$') {
      if (!inLatexBlock) {
        // Start of block
        inLatexBlock = true;
        blockStart = idx + 1;
        blockContent = [];
      } else {
        // End of block
        inLatexBlock = false;
        const fullContent = blockContent.join('\n');
        // Only include if it doesn't already use a variable
        if (!fullContent.includes('{{< var ')) {
          blocks.push({
            file: filePath,
            startLine: blockStart,
            endLine: idx + 1,
            content: fullContent,
            preview: fullContent.substring(0, 100).replace(/\n/g, ' ')
          });
        }
      }
    } else if (inLatexBlock) {
      blockContent.push(line);
    }
  });

  return blocks;
}


// Find hardcoded values in content
function findHardcodedValues(content: string, filePath: string): HardcodedMatch[] {
  const matches: HardcodedMatch[] = [];
  const lines = content.split('\n');

  // Track block state
  let inCodeBlock = false;
  let inLatexBlock = false;

  // Patterns to find
  const patterns = [
    /\$[\d,]+(?:\.\d+)?[KMB]?(?:\s*(?:billion|million|trillion))?/gi,  // Currency
    /(?<!\d)(?:[2-9]\d|\d{2,})(?:\.\d+)?%/g,  // Percentages (skip single digit, skip 1%)
    /(?<!\d)[\d,]{4,}(?!\d)/g,  // Large numbers with commas (4+ digits)
  ];

  lines.forEach((line, idx) => {
    // Track code block state
    if (line.trim().startsWith('```')) {
      inCodeBlock = !inCodeBlock;
      return;
    }

    // Track LaTeX block state
    if (line.trim() === '$$') {
      inLatexBlock = !inLatexBlock;
      return;
    }

    // Skip lines that are already all variables
    if (!line.includes('$') && !line.includes('%') && !/\d{4,}/.test(line)) return;

    // Check if line has variable references
    const hasVar = line.includes('{{< var ');

    // Remove variable references to find remaining hardcoded values
    const lineWithoutVars = line.replace(/\{\{<\s*var\s+\w+\s*>\}\}/g, '');

    // Skip citation lines entirely
    if (/\[@[\w-]+\]/.test(line)) return;

    // Skip lines that are reference anchors
    if (line.includes('<a id="')) return;

    for (const pattern of patterns) {
      pattern.lastIndex = 0; // Reset regex state
      const patternMatches = lineWithoutVars.matchAll(pattern);
      for (const match of patternMatches) {
        const value = match[0];

        // Skip 1% (treaty concept)
        if (value === '1%') continue;

        // Skip years in isolation (1948, 2024, etc.)
        if (/^(19|20)\d{2}$/.test(value)) continue;

        // Skip years with trailing comma (from lists)
        if (/^(19|20)\d{2},$/.test(value)) continue;

        matches.push({
          file: filePath,
          line: idx + 1,
          value,
          context: line.trim().substring(0, 120),
          hasExistingVar: hasVar,
          inCodeBlock,
          inLatexBlock
        });
      }
    }
  });

  return matches;
}


// Generate markdown report
function generateReport(matches: HardcodedMatch[], variables: Variable[]): string {
  const lines: string[] = [];

  lines.push('# Hardcoded Value Audit Report\n');
  lines.push(`Generated: ${new Date().toISOString()}\n`);

  // Add comprehensive introduction
  lines.push('## 📖 What Is This Report?\n');
  lines.push('This report identifies **hardcoded numbers** in the book\'s QMD files that could be replaced with **Quarto variables**.\n');
  lines.push('### Why Replace Hardcoded Values?');
  lines.push('- **Single source of truth**: Change a value once in `parameters.py`, it updates everywhere');
  lines.push('- **Automatic formatting**: Variables display with proper units ($27B, 10%, etc.)');
  lines.push('- **Built-in tooltips**: Hovering shows source, confidence interval, and formula');
  lines.push('- **Academic rigor**: Auto-generates the parameters appendix with citations\n');

  lines.push('### How Variables Work');
  lines.push('Variables are defined in `dih_models/parameters.py` and generated into `_variables.yml`.\n');
  lines.push('**Syntax:** `{{< var variable_name >}}` renders as formatted value with tooltip.\n');
  lines.push('**Example:**');
  lines.push('```markdown');
  lines.push('Before: The treaty provides $27.2 billion annually.');
  lines.push('After:  The treaty provides {{< var treaty_annual_funding >}} annually.');
  lines.push('```\n');

  lines.push('### How To Make Replacements');
  lines.push('1. **Open the file** listed in the section header (e.g., `knowledge/solution.qmd`)');
  lines.push('2. **Go to the line number** shown (e.g., Line 42)');
  lines.push('3. **Find the hardcoded value** (e.g., `$27.2B`)');
  lines.push('4. **Replace with the suggested variable** (e.g., `{{< var treaty_annual_funding >}}`)');
  lines.push('5. **Check the checkbox** `[ ]` → `[x]` to track progress');
  lines.push('6. **Mark as SKIP** if the value should NOT be replaced: `[ ]` → `[SKIP]`\n');

  lines.push('### After Making Changes');
  lines.push('Run validation to check for errors:');
  lines.push('```bash');
  lines.push('.venv/Scripts/python.exe scripts/pre-render-validation.py');
  lines.push('```\n');

  lines.push('### Report Sections');
  lines.push('| Section | Description |');
  lines.push('|:--------|:------------|');
  lines.push('| **Hardcoded Values by File** | All detected values needing review |');
  lines.push('| **LaTeX Equations** | Standalone `$$...$$` blocks that could use `_latex` variables |');
  lines.push('| **Variable Reference** | All available variables grouped by type (💰📊🔢📝) |');
  lines.push('| **LaTeX Reference** | All available `_latex` equation variables |\n');

  // Summary stats
  const inCodeBlocks = matches.filter(m => m.inCodeBlock);
  const inLatexBlocks = matches.filter(m => m.inLatexBlock);
  const inMarkdown = matches.filter(m => !m.inCodeBlock && !m.inLatexBlock);
  const onMixedLines = matches.filter(m => m.hasExistingVar);

  lines.push('## Summary\n');
  lines.push(`- **Total hardcoded values found**: ${matches.length}`);
  lines.push(`- **In regular markdown** (can use \`{{< var >}}\`): ${inMarkdown.length}`);
  lines.push(`- **In code blocks** (need Python import): ${inCodeBlocks.length}`);
  lines.push(`- **In LaTeX blocks** (need \`_latex\` variable): ${inLatexBlocks.length}`);
  lines.push(`- **On lines with existing variables**: ${onMixedLines.length}\n`);
  lines.push('> **Tip:** Use the Variable Reference at the end to find the right variable for each value.\n');

  // Add critical guidelines
  lines.push('## ⚠️ Critical Replacement Guidelines\n');
  lines.push('**Before replacing ANY value, follow these rules:**\n');
  lines.push('### ❌ DO NOT:');
  lines.push('1. **Put variables inside markdown links** - Variables are already hyperlinks with tooltips. Remove link wrapper: `[{{< var x >}}](url)` → `{{< var x >}}`');
  lines.push('2. **Keep partial ranges** - If text says "$1B to $2.6B", replace the ENTIRE range with one variable. Variables already include confidence intervals in their display.');
  lines.push('3. **Replace illustrative/fictional numbers** - Jokes, hypothetical examples, and made-up scenarios should stay hardcoded (e.g., "30% success: Hopping lessons + Prayer")');
  lines.push('4. **Replace values in Python/code blocks** - Quarto variables don\'t work inside ```` ```python ```` blocks. These need Python imports from parameters.py.');
  lines.push('5. **Replace values in LaTeX blocks with regular vars** - Quarto `{{< var >}}` syntax does NOT work inside `$$...$$`. Use `_latex` variables instead.');
  lines.push('6. **Replace historical one-off values** - Things like "WWII cost $4T" are historical facts, not parameters.\n');
  lines.push('### ✅ DO:');
  lines.push('1. **Replace entire ranges** - `$1.0 billion to $2.6 billion` → `{{< var pharma_drug_development_cost_current >}}` (CI shown automatically)');
  lines.push('2. **Remove link wrappers** - Variables have built-in source links via tooltips');
  lines.push('3. **Mark as [SKIP]** - Change `[ ]` to `[SKIP]` for items that should NOT be replaced');
  lines.push('4. **Verify semantic match** - "10%" could be success rate, discount rate, or allocation - check context!');
  lines.push('5. **Replace entire LaTeX blocks** - If a `_latex` variable exists, replace the whole `$$...$$` with `{{< var param_name_latex >}}`\n');

  // Group by file
  const byFile = new Map<string, HardcodedMatch[]>();
  for (const match of matches) {
    const existing = byFile.get(match.file) || [];
    existing.push(match);
    byFile.set(match.file, existing);
  }

  // List all hardcoded values by file
  lines.push('## Hardcoded Values by File\n');
  lines.push('*Review each value and find the appropriate variable in the reference section below.*\n');

  for (const [file, fileMatches] of byFile) {
    // Make file path relative and shorter
    const shortFile = file.replace(/.*\\knowledge\\/, 'knowledge/').replace(/\\/g, '/');
    lines.push(`### ${shortFile}\n`);
    
    for (const match of fileMatches) {
      const mixed = match.hasExistingVar ? ' [MIXED]' : '';
      let checkbox = '[ ]';
      let note = '';
      if (match.inCodeBlock) {
        checkbox = '[CODE]';
        note = ' *(in code block)*';
      } else if (match.inLatexBlock) {
        checkbox = '[LATEX]';
        note = ' *(in LaTeX block)*';
      }
      lines.push(`- ${checkbox} **Line ${match.line}**: \`${match.value}\`${mixed}${note}`);
      lines.push(`  > ${match.context}...`);
    }
    lines.push('');
  }

  // Variable Reference section - grouped by unit type for easy lookup
  lines.push('## Variable Reference\n');
  lines.push('*All available variables grouped by type. Use `{{< var variable_name >}}` syntax.*\n');

  // Group variables by unit type
  const byType = new Map<string, Variable[]>();
  for (const v of variables) {
    const existing = byType.get(v.unitType) || [];
    existing.push(v);
    byType.set(v.unitType, existing);
  }

  // Sort each group by display value (numeric) for easier scanning
  const typeOrder = ['currency', 'percentage', 'count', 'other'];
  const typeLabels: Record<string, string> = {
    currency: '💰 Currency Values',
    percentage: '📊 Percentages',
    count: '🔢 Counts/Numbers',
    other: '📝 Other'
  };

  for (const type of typeOrder) {
    const vars = byType.get(type);
    if (!vars || vars.length === 0) continue;

    // Sort by numeric value (descending) for easier scanning
    vars.sort((a, b) => (b.numericValue || 0) - (a.numericValue || 0));

    lines.push(`### ${typeLabels[type]}\n`);
    lines.push('| Variable | Value |');
    lines.push('|:---------|:------|');

    for (const v of vars) {
      // Escape pipe characters in display value
      const safeValue = v.displayValue.replace(/\|/g, '\\|');
      lines.push(`| \`${v.name}\` | ${safeValue} |`);
    }
    lines.push('');
  }

  return lines.join('\n');
}

// Generate LaTeX blocks report section
function generateLatexReport(latexBlocks: HardcodedLatexBlock[], latexVars: LatexVariable[]): string {
  const lines: string[] = [];

  lines.push('\n## 📐 Hardcoded LaTeX Equations\n');
  lines.push('*These `$$...$$` blocks could potentially be replaced with pre-built `_latex` variables.*\n');
  lines.push('**Instructions:** Check if a `_latex` variable exists that matches the equation. If so, replace the entire `$$...$$` block with `{{< var variable_name_latex >}}`.\n');

  if (latexBlocks.length === 0) {
    lines.push('No hardcoded LaTeX blocks found (all use variables or are in code blocks).\n');
  } else {
    // Group by file
    const byFile = new Map<string, HardcodedLatexBlock[]>();
    for (const block of latexBlocks) {
      const existing = byFile.get(block.file) || [];
      existing.push(block);
      byFile.set(block.file, existing);
    }

    lines.push(`Found **${latexBlocks.length}** hardcoded LaTeX blocks:\n`);

    for (const [file, blocks] of byFile) {
      lines.push(`### ${file}\n`);
      for (const block of blocks) {
        lines.push(`- [ ] **Lines ${block.startLine}-${block.endLine}**`);
        lines.push(`  > \`${block.preview}...\``);
      }
      lines.push('');
    }
  }

  // LaTeX variable reference
  lines.push('## 📐 LaTeX Variable Reference\n');
  lines.push('*Available `_latex` variables. Use `{{< var variable_name_latex >}}` to insert entire equation blocks.*\n');
  lines.push('| Variable | Preview |');
  lines.push('|:---------|:--------|');

  // Sort alphabetically by base name
  latexVars.sort((a, b) => a.baseName.localeCompare(b.baseName));

  for (const v of latexVars) {
    const safePreview = v.preview.replace(/\|/g, '\\|').replace(/\n/g, ' ');
    lines.push(`| \`${v.name}\` | \`${safePreview}...\` |`);
  }
  lines.push('');

  return lines.join('\n');
}

async function main() {
  console.log('Loading variables from _variables.yml...');
  const variables = loadVariables();
  const latexVars = loadLatexVariables();
  console.log(`Loaded ${variables.length} variables, ${latexVars.length} LaTeX variables`);

  console.log('Finding QMD files (excluding auto-generated)...');
  // Use findFiles from file-utils which respects .gitignore and excludes auto-generated files
  let files = await findFiles('knowledge/**/*.qmd', { excludeAutoGenerated: true });
  
  // Additional exclusions specific to this audit
  files = files.filter(f => {
    const normalized = f.replace(/\\/g, '/');
    // Exclude fictional scenarios with intentional values
    if (normalized.includes('/futures/')) return false;
    // Exclude references.qmd (bibliography data)
    if (normalized.endsWith('/references.qmd')) return false;
    return true;
  });

  console.log(`Scanning ${files.length} files...`);

  let allMatches: HardcodedMatch[] = [];
  let allLatexBlocks: HardcodedLatexBlock[] = [];

  for (const file of files) {
    const content = fs.readFileSync(file, 'utf-8');
    const matches = findHardcodedValues(content, file);
    allMatches = allMatches.concat(matches);
    
    // Also find hardcoded LaTeX blocks
    const latexBlocks = findHardcodedLatexBlocks(content, file);
    allLatexBlocks = allLatexBlocks.concat(latexBlocks);
  }

  const inMarkdown = allMatches.filter(m => !m.inCodeBlock && !m.inLatexBlock).length;
  const inCode = allMatches.filter(m => m.inCodeBlock).length;
  const inLatex = allMatches.filter(m => m.inLatexBlock).length;

  console.log(`Found ${allMatches.length} hardcoded values (${inMarkdown} in markdown, ${inCode} in code, ${inLatex} in LaTeX)`);
  console.log(`Found ${allLatexBlocks.length} standalone LaTeX blocks`);

  // Generate report
  const report = generateReport(allMatches, variables);
  const latexReport = generateLatexReport(allLatexBlocks, latexVars);
  fs.writeFileSync(outputFile, report + latexReport);
  console.log(`Report written to ${outputFile}`);

  console.log(`\n✓ Review the report and use the Variable Reference to find appropriate replacements.`);
}

main().catch(err => {
  console.error('Error:', err);
  process.exit(1);
});
