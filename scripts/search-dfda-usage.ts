#!/usr/bin/env node
/**
 * Search for exact case "dFDA" occurrences within string literals in parameters.py
 */

import * as fs from 'fs';
import * as path from 'path';

const CONTEXT_LINES = 3; // Number of lines to show before/after each match

interface Match {
  lineNumber: number;
  line: string;
  contextBefore: string[];
  contextAfter: string[];
  matchPositions: number[]; // Column positions where matches were found
}

/**
 * Check if a position in a line is within a string literal.
 * Handles Python string literals: '', "", ''''''', """"""", f'', f"", r'', r""
 */
function isInString(line: string, position: number): boolean {
  let inString = false;
  let stringChar: string | null = null;
  let isTripleQuote = false;
  let i = 0;

  while (i < position) {
    const char = line[i];
    const nextTwo = line.slice(i, i + 3);

    // Check for triple quotes
    if (!inString && (nextTwo === '"""' || nextTwo === "'''")) {
      inString = true;
      stringChar = char;
      isTripleQuote = true;
      i += 3;
      continue;
    }

    // Check for closing triple quote
    if (inString && isTripleQuote && nextTwo === stringChar!.repeat(3)) {
      inString = false;
      stringChar = null;
      isTripleQuote = false;
      i += 3;
      continue;
    }

    // Check for single/double quote (with optional f/r prefix)
    if (!inString && (char === '"' || char === "'")) {
      // Check if previous char is f or r (for f-strings, r-strings)
      inString = true;
      stringChar = char;
      isTripleQuote = false;
      i++;
      continue;
    }

    // Check for closing single/double quote (not triple)
    if (inString && !isTripleQuote && char === stringChar) {
      // Check if it's escaped
      let escapeCount = 0;
      let j = i - 1;
      while (j >= 0 && line[j] === '\\') {
        escapeCount++;
        j--;
      }
      // If odd number of backslashes, the quote is escaped
      if (escapeCount % 2 === 0) {
        inString = false;
        stringChar = null;
      }
      i++;
      continue;
    }

    i++;
  }

  return inString;
}

function searchFile(filePath: string, searchTerm: string): Match[] {
  const content = fs.readFileSync(filePath, 'utf-8');
  const lines = content.split('\n');
  const matches: Match[] = [];
  
  // Determine if we should filter by string literals (only for .py files)
  const isPythonFile = filePath.endsWith('.py');

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const matchPositions: number[] = [];

    // Find all occurrences of the exact search term (case-sensitive)
    let searchIndex = 0;
    while (true) {
      const foundIndex = line.indexOf(searchTerm, searchIndex);
      if (foundIndex === -1) break;

      // For Python files, check if within a string; for other files, accept all matches
      if (!isPythonFile || isInString(line, foundIndex)) {
        matchPositions.push(foundIndex);
      }

      searchIndex = foundIndex + 1;
    }

    // If we found matches, add this line
    if (matchPositions.length > 0) {
      const contextBefore: string[] = [];
      const contextAfter: string[] = [];

      // Get context before
      for (let j = Math.max(0, i - CONTEXT_LINES); j < i; j++) {
        contextBefore.push(lines[j]);
      }

      // Get context after
      for (let j = i + 1; j <= Math.min(lines.length - 1, i + CONTEXT_LINES); j++) {
        contextAfter.push(lines[j]);
      }

      matches.push({
        lineNumber: i + 1, // Line numbers are 1-indexed
        line: lines[i],
        contextBefore,
        contextAfter,
        matchPositions,
      });
    }
  }

  return matches;
}

function formatMatch(match: Match, index: number, total: number, searchTerm: string): string {
  const separator = '='.repeat(80);
  let output = `\n${separator}\n`;
  output += `Match ${index + 1} of ${total} (Line ${match.lineNumber}`;
  if (match.matchPositions.length > 1) {
    output += `, ${match.matchPositions.length} occurrences`;
  }
  output += `)\n`;
  output += `${separator}\n`;

  // Show context before
  if (match.contextBefore.length > 0) {
    match.contextBefore.forEach((line, idx) => {
      const lineNum = match.lineNumber - match.contextBefore.length + idx;
      output += `  ${String(lineNum).padStart(5, ' ')} | ${line}\n`;
    });
  }

  // Show the matching line with position markers
  output += `> ${String(match.lineNumber).padStart(5, ' ')} | ${match.line}\n`;
  
  // Add position indicators showing where matches are
  const positionLine = ' '.repeat(9) + '| ';
  const indicators = new Array(match.line.length).fill(' ');
  match.matchPositions.forEach(pos => {
    for (let i = 0; i < searchTerm.length && pos + i < indicators.length; i++) {
      indicators[pos + i] = '^';
    }
  });
  output += positionLine + indicators.join('') + '\n';

  // Show context after
  if (match.contextAfter.length > 0) {
    match.contextAfter.forEach((line, idx) => {
      const lineNum = match.lineNumber + idx + 1;
      output += `  ${String(lineNum).padStart(5, ' ')} | ${line}\n`;
    });
  }

  return output;
}

function main() {
  // Get target file from command line argument or use default
  const targetFile = process.argv[2] 
    ? path.join(process.cwd(), process.argv[2])
    : path.join(process.cwd(), 'dih_models', 'parameters.py');
  const searchTerm = 'dFDA';

  console.log(`\nSearching for "${searchTerm}" (exact case) in: ${targetFile}\n`);

  if (!fs.existsSync(targetFile)) {
    console.error(`ERROR: File not found: ${targetFile}`);
    process.exit(1);
  }

  const matches = searchFile(targetFile, searchTerm);

  if (matches.length === 0) {
    console.log(`No matches found for "${searchTerm}"`);
    return;
  }

  // Count total occurrences across all matches
  const totalOccurrences = matches.reduce((sum, match) => sum + match.matchPositions.length, 0);
  
  const isPythonFile = targetFile.endsWith('.py');
  const filterNote = isPythonFile ? ' (within string literals only)' : '';

  console.log(`Found ${totalOccurrences} occurrence(s) of "${searchTerm}" in ${matches.length} line(s)${filterNote}\n`);

  matches.forEach((match, index) => {
    console.log(formatMatch(match, index, matches.length, searchTerm));
  });

  // Summary
  console.log('\n' + '='.repeat(80));
  console.log(`SUMMARY: ${totalOccurrences} total occurrences of "${searchTerm}" in ${matches.length} lines`);
  if (isPythonFile) {
    console.log(`(Only showing exact case matches within string literals)`);
  }
  console.log('='.repeat(80) + '\n');
}

main();

