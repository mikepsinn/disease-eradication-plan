#!/usr/bin/env node
import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'yaml';

const filePath = process.argv[2] || 'knowledge/economics/economics.qmd';
const variablesPath = '_variables.yml';

interface HardcodedNumber {
  line: number;
  context: string;
  number: string;
  type: 'currency' | 'percentage' | 'number' | 'year';
}

interface Variable {
  name: string;
  displayValue: string;
  rawValue: string;
}

function extractDisplayValue(htmlString: string): string {
  // Extract text content from HTML, removing tags
  const withoutTags = htmlString.replace(/<[^>]+>/g, '');
  // Decode HTML entities
  const decoded = withoutTags
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'");
  return decoded.trim();
}

function loadVariables(varsPath: string): Variable[] {
  const fullPath = path.resolve(varsPath);
  if (!fs.existsSync(fullPath)) {
    console.error(`Variables file not found: ${fullPath}`);
    return [];
  }

  const content = fs.readFileSync(fullPath, 'utf-8');
  const parsed = yaml.parse(content);

  const variables: Variable[] = [];
  for (const [key, value] of Object.entries(parsed)) {
    if (typeof value === 'string' && !key.endsWith('_cite') && !key.endsWith('_latex')) {
      variables.push({
        name: key,
        displayValue: extractDisplayValue(value),
        rawValue: value as string
      });
    }
  }

  return variables.sort((a, b) => a.name.localeCompare(b.name));
}

function normalizeNumber(num: string): string {
  // Normalize for comparison: remove spaces, commas, make lowercase
  return num.toLowerCase().replace(/\s+/g, '').replace(/,/g, '');
}

function findMatchingVariables(hardcodedNum: string, variables: Variable[], context?: string): Variable[] {
  const normalized = normalizeNumber(hardcodedNum);

  const matches = variables.filter(v => {
    const varNormalized = normalizeNumber(v.displayValue);
    // Check for exact match or if the variable display contains the hardcoded number
    return varNormalized === normalized ||
           varNormalized.includes(normalized) ||
           normalized.includes(varNormalized);
  });

  // Sort matches: prioritize exact matches, then use context clues
  return matches.sort((a, b) => {
    const aNormalized = normalizeNumber(a.displayValue);
    const bNormalized = normalizeNumber(b.displayValue);

    // Exact match gets highest priority
    const aExact = aNormalized === normalized ? 1 : 0;
    const bExact = bNormalized === normalized ? 1 : 0;
    if (aExact !== bExact) return bExact - aExact;

    // Context-based scoring (if context provided)
    if (context) {
      const contextLower = context.toLowerCase();
      const aScore = getContextScore(a.name, contextLower);
      const bScore = getContextScore(b.name, contextLower);
      if (aScore !== bScore) return bScore - aScore;
    }

    return a.name.localeCompare(b.name);
  });
}

function getContextScore(variableName: string, context: string): number {
  let score = 0;
  const varWords = variableName.toLowerCase().split('_');

  // Extract meaningful words from context (ignore common words)
  const contextWords = context.match(/\b\w{4,}\b/g) || [];

  // Score based on word overlap between variable name and context
  for (const varWord of varWords) {
    if (varWord.length < 3) continue; // Skip short words like "pct", "roi"
    for (const ctxWord of contextWords) {
      if (ctxWord.includes(varWord) || varWord.includes(ctxWord)) {
        score += 2;
      }
    }
  }

  return score;
}

function findHardcodedNumbers(content: string): HardcodedNumber[] {
  const lines = content.split('\n');
  const hardcoded: HardcodedNumber[] = [];

  lines.forEach((line, index) => {
    // Skip lines that are comments
    if (line.trim().startsWith('#')) {
      return;
    }

    // Skip YAML frontmatter
    if (index < 10 && (line.trim() === '---' || line.includes(':'))) {
      return;
    }

    // Currency patterns: $X, $XB, $XM, $XK, $X billion, $X million, etc.
    const currencyMatches = [
      ...line.matchAll(/\$(\d+(?:,\d{3})*(?:\.\d+)?)\s*(billion|million|trillion|B|M|T|K)?/gi),
      ...line.matchAll(/~?\$(\d+(?:\.\d+)?)\s*(billion|million|trillion|B|M|T|K)?/gi),
    ];

    currencyMatches.forEach(match => {
      // Skip if this exact match is inside a variable reference
      const matchStart = line.indexOf(match[0]);
      const beforeMatch = line.substring(0, matchStart);
      const afterMatch = line.substring(matchStart);

      // Check if we're inside {{< var ... >}}
      const lastVarOpen = beforeMatch.lastIndexOf('{{< var ');
      const lastVarClose = beforeMatch.lastIndexOf('>}}');
      const nextVarClose = afterMatch.indexOf('>}}');

      const insideVar = lastVarOpen > lastVarClose && nextVarClose !== -1;

      if (!insideVar) {
        hardcoded.push({
          line: index + 1,
          context: line.trim(),
          number: match[0],
          type: 'currency'
        });
      }
    });

    // Percentage patterns: X%, X percent
    const percentMatches = Array.from(line.matchAll(/(\d+(?:\.\d+)?)\s*(%|percent)/gi));
    percentMatches.forEach(match => {
      const matchStart = line.indexOf(match[0]);
      const beforeMatch = line.substring(0, matchStart);
      const afterMatch = line.substring(matchStart);

      const lastVarOpen = beforeMatch.lastIndexOf('{{< var ');
      const lastVarClose = beforeMatch.lastIndexOf('>}}');
      const nextVarClose = afterMatch.indexOf('>}}');

      const insideVar = lastVarOpen > lastVarClose && nextVarClose !== -1;

      if (!insideVar) {
        hardcoded.push({
          line: index + 1,
          context: line.trim(),
          number: match[0],
          type: 'percentage'
        });
      }
    });

    // Year patterns: 19XX, 20XX
    const yearMatches = Array.from(line.matchAll(/\b(19\d{2}|20\d{2})\b/g));
    yearMatches.forEach(match => {
      if (!line.includes('@')) {
        const matchStart = line.indexOf(match[0]);
        const beforeMatch = line.substring(0, matchStart);
        const afterMatch = line.substring(matchStart);

        const lastVarOpen = beforeMatch.lastIndexOf('{{< var ');
        const lastVarClose = beforeMatch.lastIndexOf('>}}');
        const nextVarClose = afterMatch.indexOf('>}}');

        const insideVar = lastVarOpen > lastVarClose && nextVarClose !== -1;

        if (!insideVar) {
          hardcoded.push({
            line: index + 1,
            context: line.trim(),
            number: match[0],
            type: 'year'
          });
        }
      }
    });

    // Large numbers: XXX,XXX or X million/billion
    const largeNumberMatches = Array.from(line.matchAll(/\b(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?\s+(?:million|billion|trillion))\b/gi));
    largeNumberMatches.forEach(match => {
      if (!line.includes('$')) {
        const matchStart = line.indexOf(match[0]);
        const beforeMatch = line.substring(0, matchStart);
        const afterMatch = line.substring(matchStart);

        const lastVarOpen = beforeMatch.lastIndexOf('{{< var ');
        const lastVarClose = beforeMatch.lastIndexOf('>}}');
        const nextVarClose = afterMatch.indexOf('>}}');

        const insideVar = lastVarOpen > lastVarClose && nextVarClose !== -1;

        if (!insideVar) {
          hardcoded.push({
            line: index + 1,
            context: line.trim(),
            number: match[0],
            type: 'number'
          });
        }
      }
    });

    // Ratio patterns: X:1, X×
    const ratioMatches = Array.from(line.matchAll(/(\d+(?:\.\d+)?):1|(\d+(?:\.\d+)?)×/g));
    ratioMatches.forEach(match => {
      const matchStart = line.indexOf(match[0]);
      const beforeMatch = line.substring(0, matchStart);
      const afterMatch = line.substring(matchStart);

      const lastVarOpen = beforeMatch.lastIndexOf('{{< var ');
      const lastVarClose = beforeMatch.lastIndexOf('>}}');
      const nextVarClose = afterMatch.indexOf('>}}');

      const insideVar = lastVarOpen > lastVarClose && nextVarClose !== -1;

      if (!insideVar) {
        hardcoded.push({
          line: index + 1,
          context: line.trim(),
          number: match[0],
          type: 'number'
        });
      }
    });
  });

  return hardcoded;
}

function printVariablesReference(variables: Variable[]) {
  console.log('\n========================================');
  console.log('AVAILABLE VARIABLES FROM _variables.yml');
  console.log('========================================\n');

  // Group by category based on variable name prefix
  const categories = new Map<string, Variable[]>();

  variables.forEach(v => {
    const prefix = v.name.split('_')[0];
    if (!categories.has(prefix)) {
      categories.set(prefix, []);
    }
    categories.get(prefix)!.push(v);
  });

  // Print in columns for information density
  const sortedCategories = Array.from(categories.entries()).sort((a, b) => a[0].localeCompare(b[0]));

  for (const [prefix, vars] of sortedCategories) {
    console.log(`\n--- ${prefix.toUpperCase()} (${vars.length}) ---`);
    vars.forEach(v => {
      const name = v.name.padEnd(60);
      const display = v.displayValue.substring(0, 40);
      console.log(`${name} = ${display}`);
    });
  }

  console.log(`\n\nTOTAL VARIABLES: ${variables.length}\n`);
}

function main() {
  const fullPath = path.resolve(filePath);

  if (!fs.existsSync(fullPath)) {
    console.error(`File not found: ${fullPath}`);
    process.exit(1);
  }

  // Load variables first
  const variables = loadVariables(variablesPath);

  // Print variables reference
  printVariablesReference(variables);

  // Find hardcoded numbers
  const content = fs.readFileSync(fullPath, 'utf-8');
  const hardcodedNumbers = findHardcodedNumbers(content);

  // Group by type
  const byType = {
    currency: hardcodedNumbers.filter(h => h.type === 'currency'),
    percentage: hardcodedNumbers.filter(h => h.type === 'percentage'),
    year: hardcodedNumbers.filter(h => h.type === 'year'),
    number: hardcodedNumbers.filter(h => h.type === 'number'),
  };

  console.log('\n========================================');
  console.log(`HARDCODED NUMBERS IN ${path.basename(filePath)}`);
  console.log('========================================\n');

  console.log(`\n--- CURRENCY (${byType.currency.length}) ---`);
  byType.currency.forEach(h => {
    console.log(`Line ${h.line}: ${h.number}`);
    console.log(`  ${h.context.substring(0, 120)}...`);

    // Find matching variables with context
    const matches = findMatchingVariables(h.number, variables, h.context);
    if (matches.length > 0) {
      console.log(`  → Potential variables:`);
      matches.slice(0, 5).forEach(m => { // Limit to top 5 matches
        console.log(`     {{< var ${m.name} >}} = ${m.displayValue}`);
      });
    }
    console.log('');
  });

  console.log(`\n--- PERCENTAGES (${byType.percentage.length}) ---`);
  byType.percentage.forEach(h => {
    console.log(`Line ${h.line}: ${h.number}`);
    console.log(`  ${h.context.substring(0, 120)}...`);

    const matches = findMatchingVariables(h.number, variables, h.context);
    if (matches.length > 0) {
      console.log(`  → Potential variables:`);
      matches.slice(0, 5).forEach(m => {
        console.log(`     {{< var ${m.name} >}} = ${m.displayValue}`);
      });
    }
    console.log('');
  });

  console.log(`\n--- YEARS (${byType.year.length}) ---`);
  byType.year.forEach(h => {
    console.log(`Line ${h.line}: ${h.number}`);
    console.log(`  ${h.context.substring(0, 120)}...`);

    const matches = findMatchingVariables(h.number, variables, h.context);
    if (matches.length > 0) {
      console.log(`  → Potential variables:`);
      matches.slice(0, 5).forEach(m => {
        console.log(`     {{< var ${m.name} >}} = ${m.displayValue}`);
      });
    }
    console.log('');
  });

  console.log(`\n--- OTHER NUMBERS (${byType.number.length}) ---`);
  byType.number.forEach(h => {
    console.log(`Line ${h.line}: ${h.number}`);
    console.log(`  ${h.context.substring(0, 120)}...`);

    const matches = findMatchingVariables(h.number, variables, h.context);
    if (matches.length > 0) {
      console.log(`  → Potential variables:`);
      matches.slice(0, 5).forEach(m => {
        console.log(`     {{< var ${m.name} >}} = ${m.displayValue}`);
      });
    }
    console.log('');
  });

  console.log(`\n\nTOTAL HARDCODED NUMBERS: ${hardcodedNumbers.length}`);
  console.log(`TOTAL AVAILABLE VARIABLES: ${variables.length}\n`);
}

main();
