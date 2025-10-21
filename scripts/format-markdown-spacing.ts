import { readFileSync, writeFileSync } from 'fs';
import { globSync } from 'glob';

/**
 * Ensures proper spacing after bold text and other markdown elements
 * to prevent unintended inline rendering in Quarto.
 */
function fixMarkdownSpacing(content: string): string {
  let result = content;

  // Normalize line endings to \n for processing
  const hasWindowsLineEndings = content.includes('\r\n');
  if (hasWindowsLineEndings) {
    result = result.replace(/\r\n/g, '\n');
  }

  // Rule 1: Ensure blank line after bold text at end of line
  // Matches: **Bold text**\n (not followed by blank line)
  // Skip if followed by list, heading, code block
  result = result.replace(
    /^(\*\*[^*]+\*\*)\n(?!\n)(?![-*+]\s)(?!#{1,6}\s)(?!```)/gm,
    '$1\n\n'
  );

  // Rule 2: Ensure blank line after lines ending with colon
  // Skip frontmatter and other special cases
  result = result.replace(
    /^([^-\n][^:\n]*:)\n(?!\n)(?![-*+]\s)(?!#{1,6}\s)(?!```|  )(?!---)/gm,
    '$1\n\n'
  );

  // Restore Windows line endings if original had them
  if (hasWindowsLineEndings) {
    result = result.replace(/\n/g, '\r\n');
  }

  return result;
}

function formatFile(filePath: string): boolean {
  try {
    const content = readFileSync(filePath, 'utf-8');
    const formatted = fixMarkdownSpacing(content);

    if (content !== formatted) {
      writeFileSync(filePath, formatted, 'utf-8');
      console.log(`✓ Fixed spacing in ${filePath}`);
      return true;
    }
    return false;
  } catch (error) {
    console.error(`✗ Error formatting ${filePath}:`, error);
    return false;
  }
}

function main() {
  const pattern = process.argv[2] || '**/*.{md,qmd}';
  console.log(`Formatting markdown files matching: ${pattern}`);

  const files = globSync(pattern, {
    ignore: ['node_modules/**', '_book/**', 'dist/**', '.git/**']
  });

  if (files.length === 0) {
    console.log('No files found matching pattern.');
    return;
  }

  console.log(`Found ${files.length} files to check...\n`);

  let fixedCount = 0;
  files.forEach(file => {
    if (formatFile(file)) {
      fixedCount++;
    }
  });

  console.log(`\nDone! Fixed spacing in ${fixedCount} file(s).`);
}

main();
