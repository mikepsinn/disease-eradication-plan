#!/usr/bin/env node
/**
 * Pre-render validation script
 * Validates .qmd files before Quarto rendering to catch errors early:
 * - LaTeX syntax errors (escaped dollar signs, malformed equations, etc.)
 * - Missing image files
 * - Invalid image paths
 *
 * Runs automatically via _quarto.yml pre-render hook
 */

import { readFileSync, existsSync } from 'fs';
import { globSync } from 'glob';
import { join, dirname, resolve } from 'path';

interface ValidationError {
  file: string;
  line: number;
  column?: number;
  message: string;
  context: string;
}

const errors: ValidationError[] = [];

/**
 * Common LaTeX error patterns to check for
 */
const latexPatterns = [
  {
    pattern: /\$\$\$/g,
    message: 'Triple dollar sign (\\$\\$\\$) - should be \\$\\$ for display math or single \\$ for inline',
  },
  {
    pattern: /\\\$\$/g,
    message: 'Escaped double dollar sign (\\\\\\$\\$) - likely intended as single \\$ inside math mode',
  },
  {
    pattern: /\$\$[^\n]*\\underbrace\{[^}]*\}[^\n]*\$\$/g,
    message: 'Check \\underbrace syntax - ensure all braces are properly closed',
    validator: (match: string) => {
      // Check for matching braces
      let braceCount = 0;
      for (const char of match) {
        if (char === '{') braceCount++;
        if (char === '}') braceCount--;
        if (braceCount < 0) return false;
      }
      return braceCount === 0;
    },
  },
  {
    pattern: /\$\$[^\n]*\\\\]/g,
    message: 'Malformed equation end (\\\\\\]) - should be \\] without extra backslash',
  },
  {
    pattern: /\\\}\\_\\\{/g,
    message: 'Malformed subscript (\\\\}\\\\_\\\\{) - should be }_{',
  },
];

/**
 * Check for unmatched dollar signs in math mode
 */
function checkMathDelimiters(content: string, filename: string) {
  const lines = content.split('\n');
  let inMathBlock = false;

  lines.forEach((line, lineIndex) => {
    // Skip code blocks
    if (line.trim().startsWith('```')) return;

    // Track display math mode ($$)
    const displayMathMatches = line.match(/\$\$/g);
    if (displayMathMatches) {
      displayMathMatches.forEach(() => {
        inMathBlock = !inMathBlock;
      });
    }

    // Check for single $ in display math mode (potential error)
    // BUT ignore \$ (escaped dollar signs, which are valid in \text{} blocks)
    if (inMathBlock && line.includes('$') && !line.includes('$$')) {
      // Remove all \$ (escaped dollar signs) and \text{...} blocks
      const cleanedLine = line
        .replace(/\\text\{[^}]*\}/g, '') // Remove \text{...} blocks
        .replace(/\\\$/g, ''); // Remove escaped dollar signs

      // Now check if there are any remaining unescaped $ signs
      if (cleanedLine.includes('$')) {
        const context = line.trim();
        errors.push({
          file: filename,
          line: lineIndex + 1,
          message: 'Unescaped $ inside display math mode ($$...$$)',
          context: context.substring(0, 80),
        });
      }
    }
  });
}

/**
 * Check for missing image files
 */
function checkImagePaths(content: string, filepath: string) {
  const lines = content.split('\n');
  const fileDir = dirname(filepath);

  // Match markdown image syntax: ![alt text](path)
  const imagePattern = /!\[([^\]]*)\]\(([^)]+)\)/g;

  lines.forEach((line, lineIndex) => {
    const matches = line.matchAll(imagePattern);
    for (const match of matches) {
      const imagePath = match[2];

      // Skip URLs (http://, https://, etc.)
      if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) {
        continue;
      }

      // Resolve the image path relative to the .qmd file
      const resolvedPath = resolve(fileDir, imagePath);

      if (!existsSync(resolvedPath)) {
        errors.push({
          file: filepath,
          line: lineIndex + 1,
          message: `Image file not found: ${imagePath}`,
          context: line.trim().substring(0, 80),
        });
      }
    }
  });
}

/**
 * Validate a single file
 */
function validateFile(filepath: string) {
  if (!existsSync(filepath)) {
    console.error(`File not found: ${filepath}`);
    return;
  }

  const content = readFileSync(filepath, 'utf-8');
  const lines = content.split('\n');

  // Check for common LaTeX patterns
  latexPatterns.forEach(({ pattern, message, validator }) => {
    const matches = content.matchAll(pattern);
    for (const match of matches) {
      // If there's a custom validator, use it
      if (validator && validator(match[0])) {
        continue; // Pattern is valid
      }

      // Find line number
      const beforeMatch = content.substring(0, match.index);
      const lineNumber = beforeMatch.split('\n').length;
      const line = lines[lineNumber - 1];

      errors.push({
        file: filepath,
        line: lineNumber,
        message,
        context: line.trim().substring(0, 80),
      });
    }
  });

  // Check math delimiters
  checkMathDelimiters(content, filepath);

  // Check image paths
  checkImagePaths(content, filepath);
}

/**
 * Main validation function
 */
function main() {
  console.log('🔍 Validating LaTeX in .qmd files...\n');

  // Find all .qmd files
  const qmdFiles = globSync('**/*.qmd', {
    ignore: ['node_modules/**', '_book/**', '.quarto/**'],
  });

  console.log(`Found ${qmdFiles.length} .qmd files to validate\n`);

  // Validate each file
  qmdFiles.forEach(validateFile);

  // Report results
  if (errors.length === 0) {
    console.log('✅ No LaTeX errors found!\n');
    process.exit(0);
  } else {
    console.error(`❌ Found ${errors.length} LaTeX validation error(s):\n`);

    // Group errors by file
    const errorsByFile = errors.reduce((acc, error) => {
      if (!acc[error.file]) acc[error.file] = [];
      acc[error.file].push(error);
      return acc;
    }, {} as Record<string, ValidationError[]>);

    // Print errors grouped by file
    Object.entries(errorsByFile).forEach(([file, fileErrors]) => {
      console.error(`\n📄 ${file}:`);
      fileErrors.forEach(error => {
        console.error(`   Line ${error.line}: ${error.message}`);
        console.error(`   Context: ${error.context}`);
      });
    });

    console.error('\n❌ Please fix the above errors before building the PDF.\n');
    process.exit(1);
  }
}

main();
