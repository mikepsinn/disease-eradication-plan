#!/usr/bin/env node
import * as fs from 'fs';
import * as path from 'path';
import yaml from 'js-yaml';

// Get file path from command line argument
const targetFile = process.argv[2];
if (!targetFile) {
  console.error('Usage: npm run review-hardcoded <file.qmd>');
  process.exit(1);
}

const variablesPath = '_variables.yml';

interface Variable {
  name: string;
  value: string;
  unitType: 'currency' | 'percentage' | 'year' | 'number' | 'other';
}

interface Match {
  lineNum: number;
  lineText: string;
  hardcodedValue: string;
  matchingVars: Variable[];
}

// Extract display value from HTML
function extractDisplayValue(html: string): string {
  return html
    .replace(/<[^>]+>/g, '')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .trim();
}

// Detect unit type
function detectUnitType(value: string, varName: string): Variable['unitType'] {
  const lower = value.toLowerCase();
  if (value.includes('$') || lower.includes('billion') || lower.includes('million')) return 'currency';
  if (value.includes('%') || varName.endsWith('_pct') || varName.endsWith('_rate')) return 'percentage';
  if (/\b(19|20)\d{2}\b/.test(value) || varName.includes('_year')) return 'year';
  if (/^[\d,\.]+[KMB]?$/.test(value.replace(/\s/g, ''))) return 'number';
  return 'other';
}

// Normalize for comparison
function normalize(val: string): string {
  return val.toLowerCase().replace(/[,\s]/g, '');
}

// Load variables from _variables.yml
function loadVariables(): Variable[] {
  const content = fs.readFileSync(variablesPath, 'utf-8');
  const parsed = yaml.load(content) as Record<string, unknown>;

  const vars: Variable[] = [];
  for (const [key, value] of Object.entries(parsed)) {
    if (typeof value === 'string' && !key.endsWith('_cite') && !key.endsWith('_latex')) {
      const displayValue = extractDisplayValue(value);
      vars.push({
        name: key,
        value: displayValue,
        unitType: detectUnitType(displayValue, key)
      });
    }
  }
  return vars;
}

// Find hardcoded numbers in a line
function findHardcodedNumbers(line: string): Array<{ value: string; type: Variable['unitType'] }> {
  const found: Array<{ value: string; type: Variable['unitType'] }> = [];

  // Skip if already a variable reference
  if (line.includes('{{< var ')) return found;

  // Currency: $X, $XB, $XM, $XK
  const currencyMatches = line.matchAll(/\$\d+(?:\.\d+)?(?:[KMB]|(?:\s*(?:billion|million|trillion)))?/gi);
  for (const match of currencyMatches) {
    found.push({ value: match[0], type: 'currency' });
  }

  // Percentages: X% (but skip "1%" which refers to the treaty concept)
  const percentMatches = line.matchAll(/\d+(?:\.\d+)?%/g);
  for (const match of percentMatches) {
    if (match[0] !== '1%') {
      found.push({ value: match[0], type: 'percentage' });
    }
  }

  // Years: 19XX, 20XX (not in citations)
  if (!line.includes('@')) {
    const yearMatches = line.matchAll(/\b(19|20)\d{2}\b/g);
    for (const match of yearMatches) {
      found.push({ value: match[0], type: 'year' });
    }
  }

  return found;
}

// Main analysis
function main() {
  const fullPath = path.resolve(targetFile);
  if (!fs.existsSync(fullPath)) {
    console.error(`File not found: ${fullPath}`);
    process.exit(1);
  }

  const variables = loadVariables();
  const lines = fs.readFileSync(fullPath, 'utf-8').split('\n');

  const matches: Match[] = [];
  const seen = new Set<string>(); // Deduplicate: line+value

  lines.forEach((lineText, idx) => {
    const lineNum = idx + 1;
    const hardcodedNums = findHardcodedNumbers(lineText);

    for (const { value: hardcoded, type } of hardcodedNums) {
      const dedupeKey = `${lineNum}:${hardcoded}`;
      if (seen.has(dedupeKey)) continue;
      seen.add(dedupeKey);

      // Find exact matches
      const matchingVars = variables.filter(v =>
        v.unitType === type && normalize(v.value) === normalize(hardcoded)
      );

      if (matchingVars.length > 0) {
        matches.push({ lineNum, lineText, hardcodedValue: hardcoded, matchingVars });
      }
    }
  });

  // Write output
  const output: string[] = [];
  output.push('# Hardcoded Values Review\n\n');
  output.push(`File: ${targetFile}\n`);
  output.push(`Found ${matches.length} hardcoded values with exact variable matches\n\n`);
  output.push('---\n\n');

  matches.forEach((match, idx) => {
    output.push(`## ${idx + 1}. Line ${match.lineNum}: \`${match.hardcodedValue}\`\n\n`);
    output.push(`\`\`\`\n${match.lineText}\n\`\`\`\n\n`);

    if (match.matchingVars.length === 1) {
      const v = match.matchingVars[0];
      output.push(`**Suggestion:**\n- [ ] Replace with \`{{< var ${v.name} >}}\`\n`);
    } else {
      output.push(`**Choose one:**\n`);
      match.matchingVars.forEach(v => {
        output.push(`- [ ] \`{{< var ${v.name} >}}\`\n`);
      });
    }

    output.push(`- [ ] Skip\n\n`);
    output.push('---\n\n');
  });

  const outputFile = `hardcoded-review-${path.basename(targetFile, '.qmd')}.md`;
  fs.writeFileSync(outputFile, output.join(''));
  console.log(`✓ Review file: ${outputFile}`);
  console.log(`  Found ${matches.length} values with exact matches`);
}

main();
