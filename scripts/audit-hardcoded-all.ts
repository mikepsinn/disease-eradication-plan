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
  suggestedVar?: string;
  confidence: 'high' | 'medium' | 'low' | 'none';
  hasExistingVar: boolean;
  alternativeVars?: string[];  // Other variables with same value
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

// Score how well context matches variable keywords (0-100)
function scoreContextMatch(varKeywords: string[], lineContext: string): number {
  const contextLower = lineContext.toLowerCase();
  let matchCount = 0;

  for (const keyword of varKeywords) {
    if (contextLower.includes(keyword)) {
      matchCount++;
    }
  }

  if (varKeywords.length === 0) return 0;
  return Math.round((matchCount / varKeywords.length) * 100);
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
          confidence: 'none',
          hasExistingVar: hasVar,
          inCodeBlock,
          inLatexBlock
        });
      }
    }
  });

  return matches;
}

// Check if unit types are compatible
function unitTypesCompatible(hardcodedType: 'currency' | 'percentage' | 'count' | 'other',
                              varType: 'currency' | 'percentage' | 'count' | 'other'): boolean {
  // Exact match always OK
  if (hardcodedType === varType) return true;
  // 'other' is compatible with anything
  if (hardcodedType === 'other' || varType === 'other') return true;
  // Currency and counts should NOT match each other
  if ((hardcodedType === 'currency' && varType === 'count') ||
      (hardcodedType === 'count' && varType === 'currency')) return false;
  // Percentages should only match percentages
  if (hardcodedType === 'percentage' || varType === 'percentage') return hardcodedType === varType;
  return true;
}

// Match hardcoded values to variables with semantic context awareness
function matchToVariables(matches: HardcodedMatch[], variables: Variable[]): HardcodedMatch[] {
  return matches.map(match => {
    const matchNumeric = toNumeric(match.value);
    const matchNormalized = normalize(match.value);
    const matchUnitType = detectHardcodedUnitType(match.value);

    // Find all variables with matching value AND compatible unit type
    const valueMatches = variables.filter(v => {
      // Check unit type compatibility first
      if (!unitTypesCompatible(matchUnitType, v.unitType)) return false;
      // Exact normalized match
      if (v.normalizedValue === matchNormalized) return true;
      // Approximate numeric match (within 5%) - only for same unit types
      if (matchUnitType === v.unitType && approxEqual(v.numericValue, matchNumeric)) return true;
      return false;
    });

    if (valueMatches.length === 0) {
      return { ...match, confidence: 'none' as const };
    }

    if (valueMatches.length === 1) {
      // Single match - check context for confidence
      const contextScore = scoreContextMatch(valueMatches[0].keywords, match.context);
      const confidence = contextScore >= 50 ? 'high' : contextScore >= 20 ? 'medium' : 'low';
      return {
        ...match,
        suggestedVar: valueMatches[0].name,
        confidence: confidence as 'high' | 'medium' | 'low'
      };
    }

    // Multiple matches - use context to disambiguate
    const scored = valueMatches
      .map(v => ({
        var: v,
        score: scoreContextMatch(v.keywords, match.context)
      }))
      .sort((a, b) => b.score - a.score);

    const best = scored[0];
    const alternatives = scored.slice(1).map(s => s.var.name);

    // Determine confidence based on score difference
    let confidence: 'high' | 'medium' | 'low';
    if (best.score >= 50 && (scored.length === 1 || best.score - scored[1].score >= 20)) {
      confidence = 'high';
    } else if (best.score >= 20) {
      confidence = 'medium';
    } else {
      confidence = 'low';
    }

    return {
      ...match,
      suggestedVar: best.var.name,
      confidence,
      alternativeVars: alternatives.length > 0 ? alternatives.slice(0, 3) : undefined
    };
  });
}

// Generate markdown report
function generateReport(matches: HardcodedMatch[], variables: Variable[]): string {
  const lines: string[] = [];

  lines.push('# Hardcoded Value Audit Report\n');
  lines.push(`Generated: ${new Date().toISOString()}\n`);

  // Summary stats
  const highConf = matches.filter(m => m.confidence === 'high');
  const medConf = matches.filter(m => m.confidence === 'medium');
  const lowConf = matches.filter(m => m.confidence === 'low');
  const noMatch = matches.filter(m => m.confidence === 'none');
  const onMixedLines = matches.filter(m => m.hasExistingVar);

  lines.push('## Summary\n');
  lines.push(`- **Total hardcoded values found**: ${matches.length}`);
  lines.push(`- **High confidence matches**: ${highConf.length} (safe to replace)`);
  lines.push(`- **Medium confidence matches**: ${medConf.length} (review context)`);
  lines.push(`- **Low confidence matches**: ${lowConf.length} (likely wrong match)`);
  lines.push(`- **No match found**: ${noMatch.length} (may need new param)`);
  lines.push(`- **On lines with existing variables**: ${onMixedLines.length}\n`);

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

  // High confidence section first
  if (highConf.length > 0) {
    lines.push('## High Confidence Replacements\n');
    lines.push('*These matches have strong context alignment and are safe to replace.*\n');

    for (const [file, fileMatches] of byFile) {
      const highInFile = fileMatches.filter(m => m.confidence === 'high');
      if (highInFile.length === 0) continue;

      lines.push(`### ${file}\n`);
      for (const match of highInFile) {
        const mixed = match.hasExistingVar ? ' [MIXED]' : '';
        // Pre-mark items that can't use Quarto variables
        let checkbox = '[ ]';
        let skipReason = '';
        if (match.inCodeBlock) {
          checkbox = '[SKIP:CODE]';
          skipReason = ' ⚠️ In code block - use Python import';
        } else if (match.inLatexBlock) {
          checkbox = '[SKIP:LATEX]';
          skipReason = ' ⚠️ In LaTeX - use _latex variable';
        }
        lines.push(`- ${checkbox} **Line ${match.line}**: \`${match.value}\` → \`{{< var ${match.suggestedVar} >}}\`${mixed}${skipReason}`);
        lines.push(`  > ${match.context}...`);
      }
      lines.push('');
    }
  }

  // Medium confidence section
  if (medConf.length > 0) {
    lines.push('## Medium Confidence (Review Context)\n');
    lines.push('*These have partial context match. Verify the semantic meaning before replacing.*\n');

    for (const [file, fileMatches] of byFile) {
      const medInFile = fileMatches.filter(m => m.confidence === 'medium');
      if (medInFile.length === 0) continue;

      lines.push(`### ${file}\n`);
      for (const match of medInFile) {
        const mixed = match.hasExistingVar ? ' [MIXED]' : '';
        const alts = match.alternativeVars ? ` | Also: ${match.alternativeVars.join(', ')}` : '';
        // Pre-mark items that can't use Quarto variables
        let checkbox = '[ ]';
        let skipReason = '';
        if (match.inCodeBlock) {
          checkbox = '[SKIP:CODE]';
          skipReason = ' ⚠️ In code block';
        } else if (match.inLatexBlock) {
          checkbox = '[SKIP:LATEX]';
          skipReason = ' ⚠️ In LaTeX block';
        }
        lines.push(`- ${checkbox} **Line ${match.line}**: \`${match.value}\` → \`{{< var ${match.suggestedVar} >}}\`${mixed}${alts}${skipReason}`);
        lines.push(`  > ${match.context}...`);
      }
      lines.push('');
    }
  }

  // Low confidence section
  if (lowConf.length > 0) {
    lines.push('## Low Confidence (Likely Wrong Match)\n');
    lines.push('*Value matches but context does not. These are probably false positives.*\n');

    for (const [file, fileMatches] of byFile) {
      const lowInFile = fileMatches.filter(m => m.confidence === 'low');
      if (lowInFile.length === 0) continue;

      lines.push(`### ${file}\n`);
      for (const match of lowInFile) {
        const alts = match.alternativeVars ? ` | Also: ${match.alternativeVars.join(', ')}` : '';
        // Pre-mark items that can't use Quarto variables
        let checkbox = '[ ]';
        let skipReason = '';
        if (match.inCodeBlock) {
          checkbox = '[SKIP:CODE]';
          skipReason = ' ⚠️ In code block';
        } else if (match.inLatexBlock) {
          checkbox = '[SKIP:LATEX]';
          skipReason = ' ⚠️ In LaTeX block';
        }
        lines.push(`- ${checkbox} **Line ${match.line}**: \`${match.value}\` ≈ \`${match.suggestedVar}\`${alts}${skipReason} ⚠️`);
        lines.push(`  > ${match.context}...`);
      }
      lines.push('');
    }
  }

  // No match section
  if (noMatch.length > 0) {
    lines.push('## No Variable Match\n');
    lines.push('*These values have no matching variable. Consider creating new parameters.*\n');

    // Group by unique value
    const byValue = new Map<string, HardcodedMatch[]>();
    for (const match of noMatch) {
      const existing = byValue.get(match.value) || [];
      existing.push(match);
      byValue.set(match.value, existing);
    }

    // Sort by occurrence count
    const sorted = [...byValue.entries()].sort((a, b) => b[1].length - a[1].length);

    for (const [value, occurrences] of sorted.slice(0, 30)) {
      lines.push(`### \`${value}\` (${occurrences.length} occurrences)\n`);
      for (const match of occurrences.slice(0, 5)) {
        lines.push(`- ${match.file}:${match.line}`);
        lines.push(`  > ${match.context.substring(0, 80)}...`);
      }
      if (occurrences.length > 5) {
        lines.push(`- ... and ${occurrences.length - 5} more`);
      }
      lines.push('');
    }
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

  console.log(`Found ${allMatches.length} hardcoded values, ${allLatexBlocks.length} LaTeX blocks`);

  // Match to variables
  allMatches = matchToVariables(allMatches, variables);

  const highConf = allMatches.filter(m => m.confidence === 'high').length;
  const medConf = allMatches.filter(m => m.confidence === 'medium').length;
  const lowConf = allMatches.filter(m => m.confidence === 'low').length;

  console.log(`Matches: ${highConf} high, ${medConf} medium, ${lowConf} low confidence`);

  // Generate report
  const report = generateReport(allMatches, variables);
  const latexReport = generateLatexReport(allLatexBlocks, latexVars);
  fs.writeFileSync(outputFile, report + latexReport);
  console.log(`Report written to ${outputFile}`);

  // Exit with code based on findings
  if (highConf > 0) {
    console.log(`\n✓ ${highConf} high-confidence values can be replaced with variables`);
    process.exit(1);
  } else if (medConf > 0) {
    console.log(`\n~ ${medConf} medium-confidence matches need review`);
    process.exit(0);
  }
}

main().catch(err => {
  console.error('Error:', err);
  process.exit(1);
});
