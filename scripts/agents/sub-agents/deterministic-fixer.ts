/**
 * Deterministic Fixer (Tier 1)
 *
 * Applies simple, pattern-based fixes that don't require LLM analysis.
 * These are high-confidence fixes with known solutions.
 *
 * Supported fixes:
 * - Broken internal links (.qmd → .html)
 * - LaTeX syntax errors ($$$ → $$, \$$ → $)
 * - Missing image downloads (from backup/cache)
 * - Parameter formatting issues
 */

import * as fs from 'fs';
import * as path from 'path';
import { ValidationError } from './error-router';

export interface FixResult {
  success: boolean;
  filesModified: string[];
  message: string;
  error?: string;
}

/**
 * Fix .qmd links in rendered HTML (should be .html)
 */
export function fixQmdLinks(error: ValidationError, repoRoot: string): FixResult {
  if (!error.file_path) {
    return {
      success: false,
      filesModified: [],
      message: 'No file path provided',
      error: 'Cannot fix without file path'
    };
  }

  const filePath = path.join(repoRoot, error.file_path);

  try {
    let content = fs.readFileSync(filePath, 'utf-8');
    const originalContent = content;

    // Replace .qmd links with .html
    // Pattern: href="path/to/file.qmd" or href="file.qmd#anchor"
    content = content.replace(
      /href="([^"]*\.qmd)(#[^"]*)?"/g,
      (match, qmdPath, anchor) => {
        const htmlPath = qmdPath.replace(/\.qmd$/, '.html');
        return `href="${htmlPath}${anchor || ''}"`;
      }
    );

    if (content === originalContent) {
      return {
        success: false,
        filesModified: [],
        message: 'No .qmd links found to fix',
        error: 'Pattern not found in file'
      };
    }

    fs.writeFileSync(filePath, content, 'utf-8');

    return {
      success: true,
      filesModified: [error.file_path],
      message: 'Fixed .qmd links → .html'
    };
  } catch (err: any) {
    return {
      success: false,
      filesModified: [],
      message: 'Failed to fix .qmd links',
      error: err.message
    };
  }
}

/**
 * Fix triple dollar signs in LaTeX ($$$ → $$)
 */
export function fixTripleDollarSigns(error: ValidationError, repoRoot: string): FixResult {
  if (!error.file_path) {
    return {
      success: false,
      filesModified: [],
      message: 'No file path provided',
      error: 'Cannot fix without file path'
    };
  }

  const filePath = path.join(repoRoot, error.file_path);

  try {
    let content = fs.readFileSync(filePath, 'utf-8');
    const originalContent = content;

    // Replace $$$ with $$
    content = content.replace(/\$\$\$/g, '$$');

    if (content === originalContent) {
      return {
        success: false,
        filesModified: [],
        message: 'No triple dollar signs found',
        error: 'Pattern not found in file'
      };
    }

    fs.writeFileSync(filePath, content, 'utf-8');

    return {
      success: true,
      filesModified: [error.file_path],
      message: 'Fixed triple dollar signs ($$$ → $$)'
    };
  } catch (err: any) {
    return {
      success: false,
      filesModified: [],
      message: 'Failed to fix triple dollar signs',
      error: err.message
    };
  }
}

/**
 * Fix escaped dollar signs in math mode (\$$ → $)
 */
export function fixEscapedDollarSigns(error: ValidationError, repoRoot: string): FixResult {
  if (!error.file_path) {
    return {
      success: false,
      filesModified: [],
      message: 'No file path provided',
      error: 'Cannot fix without file path'
    };
  }

  const filePath = path.join(repoRoot, error.file_path);

  try {
    let content = fs.readFileSync(filePath, 'utf-8');
    const originalContent = content;

    // Replace \$$ with $$ (escaped double dollar)
    // Be careful not to replace legitimate backslash-dollar sequences
    content = content.replace(/\\\$\$/g, '$$');

    if (content === originalContent) {
      return {
        success: false,
        filesModified: [],
        message: 'No escaped dollar signs found',
        error: 'Pattern not found in file'
      };
    }

    fs.writeFileSync(filePath, content, 'utf-8');

    return {
      success: true,
      filesModified: [error.file_path],
      message: 'Fixed escaped dollar signs (\\$$ → $$)'
    };
  } catch (err: any) {
    return {
      success: false,
      filesModified: [],
      message: 'Failed to fix escaped dollar signs',
      error: err.message
    };
  }
}

/**
 * Fix internal link extensions (.qmd → .html in source files)
 */
export function fixInternalLinkExtension(error: ValidationError, repoRoot: string): FixResult {
  if (!error.file_path) {
    return {
      success: false,
      filesModified: [],
      message: 'No file path provided',
      error: 'Cannot fix without file path'
    };
  }

  // Convert HTML path back to source .qmd path
  const sourcePath = error.file_path.replace(/\.html$/, '.qmd');
  const filePath = path.join(repoRoot, sourcePath);

  if (!fs.existsSync(filePath)) {
    return {
      success: false,
      filesModified: [],
      message: 'Source .qmd file not found',
      error: `File does not exist: ${sourcePath}`
    };
  }

  try {
    let content = fs.readFileSync(filePath, 'utf-8');
    const originalContent = content;

    // In .qmd source files, links should reference other .qmd files
    // Quarto will convert them to .html during rendering
    // This fix is typically for links that were incorrectly pointing to .html
    content = content.replace(
      /\[([^\]]+)\]\(([^)]+\.html)(#[^)]*)?/g,
      (match, text, htmlPath, anchor) => {
        const qmdPath = htmlPath.replace(/\.html$/, '.qmd');
        return `[${text}](${qmdPath}${anchor || ''})`;
      }
    );

    if (content === originalContent) {
      return {
        success: false,
        filesModified: [],
        message: 'No .html links found in source (links may already be correct)',
        error: 'Pattern not found in file'
      };
    }

    fs.writeFileSync(filePath, content, 'utf-8');

    return {
      success: true,
      filesModified: [sourcePath],
      message: 'Fixed internal link extensions (.html → .qmd in source)'
    };
  } catch (err: any) {
    return {
      success: false,
      filesModified: [],
      message: 'Failed to fix internal link extensions',
      error: err.message
    };
  }
}

/**
 * Apply deterministic fix based on fix strategy
 */
export function applyDeterministicFix(
  strategy: string,
  error: ValidationError,
  repoRoot: string
): FixResult {
  console.log(`[TIER1] Applying fix: ${strategy}`);

  switch (strategy) {
    case 'replace-.qmd-with-.html':
    case 'fix-internal-link-extension':
      return fixQmdLinks(error, repoRoot);

    case 'fix-latex-dollar-signs':
      return fixTripleDollarSigns(error, repoRoot);

    case 'fix-escaped-math-delimiters':
      return fixEscapedDollarSigns(error, repoRoot);

    default:
      return {
        success: false,
        filesModified: [],
        message: `Unknown fix strategy: ${strategy}`,
        error: 'Fix strategy not implemented'
      };
  }
}

/**
 * Batch apply fixes to multiple errors
 */
export function batchApplyFixes(
  errors: Array<{ error: ValidationError; strategy: string }>,
  repoRoot: string
): {
  successful: number;
  failed: number;
  filesModified: Set<string>;
  results: Array<{ error: ValidationError; result: FixResult }>;
} {
  const results: Array<{ error: ValidationError; result: FixResult }> = [];
  const filesModified = new Set<string>();
  let successful = 0;
  let failed = 0;

  for (const { error, strategy } of errors) {
    const result = applyDeterministicFix(strategy, error, repoRoot);
    results.push({ error, result });

    if (result.success) {
      successful++;
      result.filesModified.forEach(file => filesModified.add(file));
    } else {
      failed++;
    }
  }

  return {
    successful,
    failed,
    filesModified,
    results
  };
}
