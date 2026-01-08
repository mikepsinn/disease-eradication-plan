#!/usr/bin/env node
/**
 * Audit all QMD files for hardcoded values and generate replacement report
 * Usage: npx tsx scripts/audit-hardcoded-all.ts [--output report.md] [--limit 10]
 */
import * as fs from 'fs';
import * as path from 'path';
import { glob } from 'glob';
import yaml from 'js-yaml';

interface Variable {
  name: string;
  displayValue: string;
  normalizedValue: string;
}

interface HardcodedMatch {
  file: string;
  line: number;
  value: string;
  context: string;
  suggestedVar?: string;
  hasExistingVar: boolean;
}

// Parse command line args
const args = process.argv.slice(2);
const outputFile = args.includes('--output')
  ? args[args.indexOf('--output') + 1]
  : '_hardcoded-audit-report.md';
const limit = args.includes('--limit')
  ? parseInt(args[args.indexOf('--limit') + 1], 10)
  : 0;

// Normalize value for comparison
function normalize(val: string): string {
  return val
    .toLowerCase()
    .replace(/[,\s]/g, '')
    .replace(/\$/, '')
    .replace(/billion/i, 'b')
    .replace(/million/i, 'm')
    .replace(/thousand/i, 'k');
}

// Extract display value from HTML
function extractDisplayValue(html: string): string {
  return html
    .replace(/<[^>]+>/g, '')
    .replace(/&amp;/g, '&')
    .trim()
    .split(' ')[0]; // Get just the value part, not confidence interval
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
        normalizedValue: normalize(displayValue)
      });
    }
  }
  return vars;
}

// Find hardcoded values in content
function findHardcodedValues(content: string, filePath: string): HardcodedMatch[] {
  const matches: HardcodedMatch[] = [];
  const lines = content.split('\n');

  // Patterns to find
  const patterns = [
    /\$[\d,]+(?:\.\d+)?[KMB]?(?:\s*(?:billion|million|trillion))?/gi,  // Currency
    /(?<!\d)(?:[2-9]\d|\d{2,})(?:\.\d+)?%/g,  // Percentages (skip single digit, skip 1%)
    /(?<!\d)[\d,]{4,}(?!\d)/g,  // Large numbers with commas (4+ digits)
  ];

  lines.forEach((line, idx) => {
    // Skip lines that are already all variables
    if (!line.includes('$') && !line.includes('%') && !/\d{4,}/.test(line)) return;

    // Check if line has variable references
    const hasVar = line.includes('{{< var ');

    // Remove variable references to find remaining hardcoded values
    const lineWithoutVars = line.replace(/\{\{<\s*var\s+\w+\s*>\}\}/g, '');

    // Skip citation lines
    if (line.includes('@') && /\[@[\w-]+\]/.test(line)) return;

    for (const pattern of patterns) {
      const patternMatches = lineWithoutVars.matchAll(pattern);
      for (const match of patternMatches) {
        const value = match[0];

        // Skip 1% (treaty concept)
        if (value === '1%') continue;

        // Skip years in isolation (but not currency with year-like numbers)
        if (/^(19|20)\d{2}$/.test(value) && !value.includes('$')) continue;

        matches.push({
          file: filePath,
          line: idx + 1,
          value,
          context: line.trim().substring(0, 100),
          hasExistingVar: hasVar
        });
      }
    }
  });

  return matches;
}

// Match hardcoded values to variables
function matchToVariables(matches: HardcodedMatch[], variables: Variable[]): HardcodedMatch[] {
  return matches.map(match => {
    const normalized = normalize(match.value);

    // Find exact match
    const exactMatch = variables.find(v => v.normalizedValue === normalized);
    if (exactMatch) {
      return { ...match, suggestedVar: exactMatch.name };
    }

    // Try fuzzy matching for currency (14m matches $14M)
    const fuzzyMatch = variables.find(v => {
      const vNorm = v.normalizedValue;
      const mNorm = normalized;
      return vNorm === mNorm ||
             vNorm.replace(/^0+/, '') === mNorm.replace(/^0+/, '');
    });

    if (fuzzyMatch) {
      return { ...match, suggestedVar: fuzzyMatch.name };
    }

    return match;
  });
}

// Generate markdown report
function generateReport(matches: HardcodedMatch[]): string {
  const lines: string[] = [];

  lines.push('# Hardcoded Value Audit Report\n');
  lines.push(`Generated: ${new Date().toISOString()}\n`);

  // Summary stats
  const withSuggestion = matches.filter(m => m.suggestedVar);
  const withoutSuggestion = matches.filter(m => !m.suggestedVar);
  const onMixedLines = matches.filter(m => m.hasExistingVar);

  lines.push('## Summary\n');
  lines.push(`- **Total hardcoded values found**: ${matches.length}`);
  lines.push(`- **With variable match**: ${withSuggestion.length}`);
  lines.push(`- **Without match (may need new param)**: ${withoutSuggestion.length}`);
  lines.push(`- **On lines with existing variables**: ${onMixedLines.length}\n`);

  // Group by file
  const byFile = new Map<string, HardcodedMatch[]>();
  for (const match of matches) {
    const existing = byFile.get(match.file) || [];
    existing.push(match);
    byFile.set(match.file, existing);
  }

  lines.push('## Files with Hardcoded Values\n');

  for (const [file, fileMatches] of byFile) {
    const withMatch = fileMatches.filter(m => m.suggestedVar).length;
    lines.push(`### ${file} (${fileMatches.length} values, ${withMatch} have matches)\n`);

    for (const match of fileMatches) {
      const mixed = match.hasExistingVar ? ' [MIXED LINE]' : '';
      if (match.suggestedVar) {
        lines.push(`- [ ] **Line ${match.line}**: \`${match.value}\` → \`{{< var ${match.suggestedVar} >}}\`${mixed}`);
      } else {
        lines.push(`- [ ] **Line ${match.line}**: \`${match.value}\` - *No variable match*${mixed}`);
      }
      lines.push(`  > ${match.context}...`);
    }
    lines.push('');
  }

  // Values needing new parameters
  if (withoutSuggestion.length > 0) {
    lines.push('## Values That May Need New Parameters\n');
    const uniqueValues = [...new Set(withoutSuggestion.map(m => m.value))];
    for (const value of uniqueValues.slice(0, 20)) {
      const occurrences = withoutSuggestion.filter(m => m.value === value);
      lines.push(`- \`${value}\` (${occurrences.length} occurrences)`);
    }
  }

  return lines.join('\n');
}

async function main() {
  console.log('Loading variables from _variables.yml...');
  const variables = loadVariables();
  console.log(`Loaded ${variables.length} variables`);

  console.log('Finding QMD files...');
  let files = await glob('knowledge/**/*.qmd', {
    ignore: ['**/knowledge/_build_temp/**', '**/references.qmd']
  });

  if (limit > 0) {
    files = files.slice(0, limit);
    console.log(`Limited to ${limit} files`);
  }

  console.log(`Scanning ${files.length} files...`);

  let allMatches: HardcodedMatch[] = [];

  for (const file of files) {
    const content = fs.readFileSync(file, 'utf-8');
    const matches = findHardcodedValues(content, file);
    allMatches = allMatches.concat(matches);
  }

  console.log(`Found ${allMatches.length} hardcoded values`);

  // Match to variables
  allMatches = matchToVariables(allMatches, variables);

  const withMatch = allMatches.filter(m => m.suggestedVar).length;
  console.log(`${withMatch} have variable matches`);

  // Generate report
  const report = generateReport(allMatches);
  fs.writeFileSync(outputFile, report);
  console.log(`Report written to ${outputFile}`);

  // Exit with error if replaceable values found (useful for CI)
  if (withMatch > 0) {
    console.log(`\n⚠️  ${withMatch} values can be replaced with variables`);
    process.exit(1);
  }
}

main().catch(err => {
  console.error('Error:', err);
  process.exit(1);
});
