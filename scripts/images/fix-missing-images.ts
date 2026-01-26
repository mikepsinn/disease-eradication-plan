/**
 * Fix Missing Image References
 *
 * Scans all QMD files for image references to non-existent files.
 * - If an alternative extension exists (e.g., .jpg instead of .png), replaces it
 * - If no alternative exists, removes the entire image reference
 *
 * Usage:
 *   npx tsx scripts/images/fix-missing-images.ts          # Dry run (default)
 *   npx tsx scripts/images/fix-missing-images.ts --fix    # Apply fixes
 */

import { existsSync } from 'fs';
import { readFile, writeFile } from 'fs/promises';
import * as path from 'path';
import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';
import { glob } from 'glob';
import { getProjectRoot } from '../lib/file-utils';
import { SUPPORTED_IMAGE_EXTENSIONS } from '../lib/image-file-utils';

const PROJECT_ROOT = getProjectRoot();

/**
 * Find all QMD files in the knowledge directory
 */
async function findQmdFiles(): Promise<string[]> {
  const patterns = [
    'index.qmd',
    'index-manual.qmd',
    'knowledge/**/*.qmd',
  ];

  const allFiles: string[] = [];
  for (const pattern of patterns) {
    const files = await glob(pattern, {
      cwd: PROJECT_ROOT,
      nodir: true,
      ignore: ['_build_temp/**', 'node_modules/**'],
    });
    allFiles.push(...files);
  }

  // Return unique paths
  return [...new Set(allFiles)];
}

// --- Types ---

interface ImageReference {
  file: string;
  line: number;
  column: number;
  imagePath: string;
  resolvedPath: string;
  exists: boolean;
  matchType: 'markdown' | 'html';
  fullMatch: string;
}

interface FixAction {
  ref: ImageReference;
  action: 'replace' | 'remove';
  alternativePath?: string;
}

// --- Image Path Extraction ---

/**
 * Extract all image references from QMD content
 * Handles both markdown ![alt](path) and HTML <img src="path"> syntax
 */
function extractImageReferences(content: string, filePath: string): ImageReference[] {
  const references: ImageReference[] = [];
  const lines = content.split('\n');
  const fileDir = path.dirname(filePath);

  // Markdown image pattern: ![alt text](path)
  const markdownPattern = /!\[([^\]]*)\]\(([^)]+)\)/g;
  // HTML img pattern: <img src="path" /> or <img src='path' />
  const htmlPattern = /<img[^>]+src=["']([^"']+)["'][^>]*\/?>/gi;

  for (let lineIndex = 0; lineIndex < lines.length; lineIndex++) {
    const line = lines[lineIndex];
    const lineNumber = lineIndex + 1;

    // Check markdown images
    let match;
    while ((match = markdownPattern.exec(line)) !== null) {
      const imagePath = match[2];
      if (isLocalPath(imagePath)) {
        const resolvedPath = resolvePath(imagePath, fileDir);
        references.push({
          file: filePath,
          line: lineNumber,
          column: match.index + 1,
          imagePath,
          resolvedPath,
          exists: existsSync(resolvedPath),
          matchType: 'markdown',
          fullMatch: match[0],
        });
      }
    }

    // Reset regex lastIndex for next line
    markdownPattern.lastIndex = 0;

    // Check HTML img tags
    while ((match = htmlPattern.exec(line)) !== null) {
      const imagePath = match[1];
      if (isLocalPath(imagePath)) {
        const resolvedPath = resolvePath(imagePath, fileDir);
        references.push({
          file: filePath,
          line: lineNumber,
          column: match.index + 1,
          imagePath,
          resolvedPath,
          exists: existsSync(resolvedPath),
          matchType: 'html',
          fullMatch: match[0],
        });
      }
    }

    // Reset regex lastIndex for next line
    htmlPattern.lastIndex = 0;
  }

  return references;
}

/**
 * Check if a path is local (not a URL)
 */
function isLocalPath(imagePath: string): boolean {
  return !imagePath.startsWith('http://') && !imagePath.startsWith('https://');
}

/**
 * Resolve image path to absolute path
 */
function resolvePath(imagePath: string, fileDir: string): string {
  if (imagePath.startsWith('/')) {
    // Absolute path from project root
    return path.join(PROJECT_ROOT, imagePath.slice(1));
  } else {
    // Relative path from file location
    return path.resolve(fileDir, imagePath);
  }
}

// --- Alternative Extension Finding ---

/**
 * Find an alternative file with a different extension
 * Priority: .jpg <-> .png, then try other extensions
 */
function findAlternativeExtension(resolvedPath: string): string | null {
  const ext = path.extname(resolvedPath).toLowerCase();
  const basePath = resolvedPath.slice(0, -ext.length);

  // Priority order for alternatives
  const priorityAlternatives: Record<string, string[]> = {
    '.png': ['.jpg', '.jpeg', '.webp', '.gif'],
    '.jpg': ['.png', '.jpeg', '.webp', '.gif'],
    '.jpeg': ['.jpg', '.png', '.webp', '.gif'],
    '.webp': ['.jpg', '.png', '.jpeg', '.gif'],
    '.gif': ['.jpg', '.png', '.jpeg', '.webp'],
  };

  const alternatives = priorityAlternatives[ext] || SUPPORTED_IMAGE_EXTENSIONS.filter(e => e !== ext);

  for (const altExt of alternatives) {
    const altPath = basePath + altExt;
    if (existsSync(altPath)) {
      return altPath;
    }
  }

  return null;
}

/**
 * Convert resolved absolute path back to the original path format
 */
function convertToOriginalFormat(originalPath: string, newResolvedPath: string, fileDir: string): string {
  if (originalPath.startsWith('/')) {
    // Was absolute from project root
    return '/' + path.relative(PROJECT_ROOT, newResolvedPath).replace(/\\/g, '/');
  } else {
    // Was relative
    return path.relative(fileDir, newResolvedPath).replace(/\\/g, '/');
  }
}

// --- Fix Application ---

/**
 * Generate a replacement string for an image reference
 */
function generateReplacement(ref: ImageReference, alternativePath: string, fileDir: string): string {
  const newImagePath = convertToOriginalFormat(ref.imagePath, alternativePath, fileDir);

  if (ref.matchType === 'markdown') {
    // Replace path in markdown: ![alt](oldPath) -> ![alt](newPath)
    const altText = ref.fullMatch.match(/!\[([^\]]*)\]/)?.[1] || '';
    return `![${altText}](${newImagePath})`;
  } else {
    // Replace path in HTML: update src attribute
    return ref.fullMatch.replace(/src=["'][^"']+["']/, `src="${newImagePath}"`);
  }
}

/**
 * Apply fixes to a file
 */
async function applyFixes(filePath: string, fixes: FixAction[]): Promise<void> {
  let content = await readFile(filePath, 'utf-8');
  const fileDir = path.dirname(filePath);

  // Sort fixes by line and column in reverse order to avoid offset issues
  const sortedFixes = [...fixes].sort((a, b) => {
    if (a.ref.line !== b.ref.line) return b.ref.line - a.ref.line;
    return b.ref.column - a.ref.column;
  });

  const lines = content.split('\n');

  for (const fix of sortedFixes) {
    const lineIndex = fix.ref.line - 1;
    const line = lines[lineIndex];

    if (fix.action === 'replace' && fix.alternativePath) {
      const replacement = generateReplacement(fix.ref, fix.alternativePath, fileDir);
      lines[lineIndex] = line.replace(fix.ref.fullMatch, replacement);
    } else if (fix.action === 'remove') {
      // Remove the entire image reference
      let newLine = line.replace(fix.ref.fullMatch, '');
      // Clean up any resulting double spaces or empty lines
      newLine = newLine.replace(/  +/g, ' ').trim();
      if (newLine === '') {
        // Remove empty line entirely
        lines.splice(lineIndex, 1);
      } else {
        lines[lineIndex] = newLine;
      }
    }
  }

  // Collapse consecutive blank lines to single blank line
  const cleanedLines: string[] = [];
  let prevWasBlank = false;
  for (const line of lines) {
    const isBlank = line.trim() === '';
    if (isBlank && prevWasBlank) {
      continue; // Skip consecutive blank lines
    }
    cleanedLines.push(line);
    prevWasBlank = isBlank;
  }

  await writeFile(filePath, cleanedLines.join('\n'), 'utf-8');
}

// --- Main ---

async function main() {
  const argv = await yargs(hideBin(process.argv))
    .option('fix', {
      type: 'boolean',
      description: 'Actually apply the fixes. Defaults to dry run.',
      default: false,
    })
    .option('verbose', {
      alias: 'v',
      type: 'boolean',
      description: 'Show all image references (including valid ones)',
      default: false,
    })
    .help()
    .argv;

  const isDryRun = !argv.fix;

  console.log(isDryRun ? '=== DRY RUN ===' : '=== APPLYING FIXES ===');
  if (isDryRun) {
    console.log('No files will be modified. Use --fix to apply changes.\n');
  }

  // Get all QMD files
  const qmdFiles = await findQmdFiles();
  console.log(`Scanning ${qmdFiles.length} QMD files...\n`);

  // Collect all references
  const allReferences: ImageReference[] = [];
  const missingReferences: ImageReference[] = [];
  const fixActions: Map<string, FixAction[]> = new Map();

  for (const file of qmdFiles) {
    const filePath = path.resolve(PROJECT_ROOT, file);
    if (!existsSync(filePath)) continue;

    const content = await readFile(filePath, 'utf-8');
    const refs = extractImageReferences(content, filePath);

    allReferences.push(...refs);

    for (const ref of refs) {
      if (!ref.exists) {
        missingReferences.push(ref);

        // Find alternative
        const alternative = findAlternativeExtension(ref.resolvedPath);
        const action: FixAction = alternative
          ? { ref, action: 'replace', alternativePath: alternative }
          : { ref, action: 'remove' };

        if (!fixActions.has(ref.file)) {
          fixActions.set(ref.file, []);
        }
        fixActions.get(ref.file)!.push(action);
      }
    }
  }

  // Report
  const validCount = allReferences.length - missingReferences.length;
  const toReplace = missingReferences.filter(r => {
    const actions = fixActions.get(r.file);
    return actions?.find(a => a.ref === r)?.action === 'replace';
  }).length;
  const toRemove = missingReferences.length - toReplace;

  console.log(`VALID IMAGES: ${validCount}`);
  console.log(`MISSING IMAGES: ${missingReferences.length}\n`);

  if (missingReferences.length === 0) {
    console.log('All image references are valid!');
    return;
  }

  // Show details
  let index = 1;
  for (const ref of missingReferences) {
    const relFile = path.relative(PROJECT_ROOT, ref.file).replace(/\\/g, '/');
    const actions = fixActions.get(ref.file);
    const action = actions?.find(a => a.ref === ref);

    console.log(`${index}. ${relFile}:${ref.line}`);
    console.log(`   Missing: ${ref.imagePath}`);

    if (action?.action === 'replace' && action.alternativePath) {
      const altRelPath = path.relative(PROJECT_ROOT, action.alternativePath).replace(/\\/g, '/');
      console.log(`   Action: REPLACE with ${altRelPath}`);
    } else {
      console.log(`   Action: REMOVE (no alternative found)`);
    }
    console.log('');
    index++;
  }

  // Summary
  console.log('=== SUMMARY ===');
  console.log(`Valid images: ${validCount}`);
  console.log(`To replace: ${toReplace}`);
  console.log(`To remove: ${toRemove}`);
  console.log(`Total changes: ${missingReferences.length}`);

  // Apply fixes if not dry run
  if (!isDryRun) {
    console.log('\nApplying fixes...');
    for (const [filePath, actions] of fixActions) {
      await applyFixes(filePath, actions);
      const relPath = path.relative(PROJECT_ROOT, filePath).replace(/\\/g, '/');
      console.log(`  Fixed: ${relPath} (${actions.length} changes)`);
    }
    console.log('\nDone! Run pre-render-validation.py to verify.');
  } else {
    console.log('\nRun with --fix to apply changes.');
  }
}

main().catch(error => {
  console.error('Error:', error);
  process.exit(1);
});
