#!/usr/bin/env npx tsx
/**
 * Find QMD files with trailing units after variables that now include units.
 *
 * Usage:
 *   npx tsx scripts/find-trailing-units.ts          # Just find and report
 *   npx tsx scripts/find-trailing-units.ts --fix    # Find and fix
 */

import * as fs from 'fs';
import * as path from 'path';
import { glob } from 'glob';

// Common unit patterns that should NOT appear after variables
const TRAILING_UNIT_PATTERNS = [
  // Time units
  { pattern: /(\{\{<\s*var\s+\w*years?\w*\s*>\}\})\s+(years?)/gi, unit: 'years' },
  { pattern: /(\{\{<\s*var\s+\w*days?\w*\s*>\}\})\s+(days?)/gi, unit: 'days' },
  { pattern: /(\{\{<\s*var\s+\w*months?\w*\s*>\}\})\s+(months?)/gi, unit: 'months' },

  // Health units
  { pattern: /(\{\{<\s*var\s+\w*dalys?\w*\s*>\}\})\s+(DALYs?)/gi, unit: 'DALYs' },
  { pattern: /(\{\{<\s*var\s+\w*qalys?\w*\s*>\}\})\s+(QALYs?)/gi, unit: 'QALYs' },
  { pattern: /(\{\{<\s*var\s+\w*deaths?\w*\s*>\}\})\s+(deaths?)/gi, unit: 'deaths' },
  { pattern: /(\{\{<\s*var\s+\w*lives?\w*\s*>\}\})\s+(lives?)/gi, unit: 'lives' },

  // Ratio patterns - variables containing "roi", "ratio", "cost_ratio" followed by :1
  // Exclude _cite, _latex variables (they don't contain numeric values)
  { pattern: /(\{\{<\s*var\s+(?!\w*_cite\b)(?!\w*_latex\b)\w*roi\w*\s*>\}\})\s*:1/gi, unit: ':1' },
  { pattern: /(\{\{<\s*var\s+(?!\w*_cite\b)(?!\w*_latex\b)\w*ratio\w*\s*>\}\})\s*:1/gi, unit: ':1' },

  // Multiplier/factor patterns - variables containing "multiplier", "factor" followed by x or X
  { pattern: /(\{\{<\s*var\s+\w*multiplier\w*\s*>\}\})\s*[xX]\b/gi, unit: 'x' },
  { pattern: /(\{\{<\s*var\s+\w*factor\w*\s*>\}\})\s*[xX]\b/gi, unit: 'x' },

  // Generic patterns - variable ending with unit name followed by that unit
  { pattern: /(\{\{<\s*var\s+\w+_years\s*>\}\})\s+(years?)/gi, unit: 'years' },
  { pattern: /(\{\{<\s*var\s+\w+_days\s*>\}\})\s+(days?)/gi, unit: 'days' },
  { pattern: /(\{\{<\s*var\s+\w+_deaths\s*>\}\})\s+(deaths?)/gi, unit: 'deaths' },
  { pattern: /(\{\{<\s*var\s+\w+_dalys\s*>\}\})\s+(DALYs?)/gi, unit: 'DALYs' },
  { pattern: /(\{\{<\s*var\s+\w+_qalys\s*>\}\})\s+(QALYs?)/gi, unit: 'QALYs' },
  { pattern: /(\{\{<\s*var\s+\w+_patients\s*>\}\})\s+(patients?)/gi, unit: 'patients' },
  { pattern: /(\{\{<\s*var\s+\w+_trials\s*>\}\})\s+(trials?)/gi, unit: 'trials' },
  { pattern: /(\{\{<\s*var\s+\w+_diseases\s*>\}\})\s+(diseases?)/gi, unit: 'diseases' },
];

interface Match {
  file: string;
  line: number;
  original: string;
  fixed: string;
  unit: string;
}

async function findTrailingUnits(fix: boolean = false): Promise<void> {
  const qmdFiles = await glob('**/*.qmd', {
    ignore: ['node_modules/**', '_book/**', '_site/**', '.quarto/**', '_build_temp/**'],
    cwd: process.cwd(),
  });

  const matches: Match[] = [];
  let filesModified = 0;

  for (const file of qmdFiles) {
    const filePath = path.join(process.cwd(), file);
    let content = fs.readFileSync(filePath, 'utf-8');
    const lines = content.split('\n');
    let fileModified = false;

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];

      for (const { pattern, unit } of TRAILING_UNIT_PATTERNS) {
        // Reset regex state
        pattern.lastIndex = 0;

        let match;
        while ((match = pattern.exec(line)) !== null) {
          const original = match[0];
          const varPart = match[1];
          const fixed = varPart; // Remove the trailing unit

          matches.push({
            file,
            line: i + 1,
            original,
            fixed,
            unit,
          });

          if (fix) {
            lines[i] = lines[i].replace(original, fixed);
            fileModified = true;
          }
        }
      }
    }

    if (fix && fileModified) {
      fs.writeFileSync(filePath, lines.join('\n'), 'utf-8');
      filesModified++;
    }
  }

  // Report results
  console.log('\n=== Trailing Unit Analysis ===\n');

  if (matches.length === 0) {
    console.log('No trailing units found!');
    return;
  }

  // Group by file
  const byFile = new Map<string, Match[]>();
  for (const m of matches) {
    if (!byFile.has(m.file)) {
      byFile.set(m.file, []);
    }
    byFile.get(m.file)!.push(m);
  }

  for (const [file, fileMatches] of byFile) {
    console.log(`\n📄 ${file}`);
    for (const m of fileMatches) {
      console.log(`  Line ${m.line}: "${m.original}" -> "${m.fixed}"`);
    }
  }

  console.log(`\n=== Summary ===`);
  console.log(`Found ${matches.length} trailing units in ${byFile.size} files`);

  if (fix) {
    console.log(`Fixed ${filesModified} files`);
  } else {
    console.log(`\nRun with --fix to automatically remove trailing units`);
  }
}

// Main
const args = process.argv.slice(2);
const shouldFix = args.includes('--fix');

findTrailingUnits(shouldFix).catch(console.error);
