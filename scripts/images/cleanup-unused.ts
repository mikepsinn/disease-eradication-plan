#!/usr/bin/env tsx
/**
 * Cleanup Unused Images - Find and delete unreferenced images
 *
 * Scans assets directory for images not referenced in any markdown files.
 *
 * Usage:
 *   npx tsx scripts/images/cleanup-unused.ts           # Dry run (preview)
 *   npx tsx scripts/images/cleanup-unused.ts --delete  # Actually delete files
 */

import fs from 'fs/promises';
import { existsSync, statSync } from 'fs';
import path from 'path';

// Shared utilities
import { findImages } from '../lib/image-file-utils';
import { hasFlag, printHeader, printSummary } from '../lib/cli-utils';

const ROOT_DIR = process.cwd();
const ASSETS_DIR = path.join(ROOT_DIR, 'assets');
const IGNORED_DIRS = ['node_modules', '.git', '.cursor-cache', 'assets', '.quarto', '_book'];

/**
 * Recursively find files with given extensions
 */
async function findFiles(dir: string, extensions: string[]): Promise<string[]> {
  const results: string[] = [];

  try {
    const entries = await fs.readdir(dir, { withFileTypes: true });

    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);

      if (entry.isDirectory()) {
        if (!IGNORED_DIRS.includes(entry.name)) {
          results.push(...await findFiles(fullPath, extensions));
        }
      } else if (extensions.some(ext => entry.name.endsWith(ext))) {
        results.push(fullPath);
      }
    }
  } catch (error) {
    // Directory doesn't exist or not readable
  }

  return results;
}

async function main() {
  const args = process.argv.slice(2);
  const shouldDelete = hasFlag(args, 'delete');
  const isDryRun = !shouldDelete;

  printHeader('Cleanup Unused Images');
  console.log(`Mode: ${isDryRun ? 'DRY RUN (preview only)' : 'DELETE MODE'}`)
  console.log('')

  // 1. Find all image files
  const imageExtensions = ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'];
  const allImageFiles = await findFiles(ASSETS_DIR, imageExtensions);
  console.log(`[1/3] Found ${allImageFiles.length} image files in assets/`);

  // 2. Find all markdown/qmd files and read their content
  const contentFiles = await findFiles(ROOT_DIR, ['.md', '.qmd']);
  let allContent = '';
  for (const file of contentFiles) {
    allContent += await fs.readFile(file, 'utf-8');
  }
  console.log(`[2/3] Scanning ${contentFiles.length} content files for references...`);

  // 3. Check for references
  const unreferencedImages: string[] = [];
  for (const imagePath of allImageFiles) {
    const imageName = path.basename(imagePath);
    // Simple string search for efficiency
    if (!allContent.includes(imageName)) {
      unreferencedImages.push(imagePath);
    }
  }

  console.log(`[3/3] Analysis complete\n`);

  if (unreferencedImages.length === 0) {
    console.log('No unreferenced images found. Everything is clean!');
    return;
  }

  console.log(`Found ${unreferencedImages.length} unreferenced images:`);
  for (const img of unreferencedImages) {
    console.log(`  - ${path.relative(ROOT_DIR, img)}`);
  }

  if (!isDryRun) {
    let deleteCount = 0;
    console.log('\nDeleting...');
    for (const imagePath of unreferencedImages) {
      try {
        await fs.unlink(imagePath);
        deleteCount++;
      } catch (error) {
        console.error(`  [ERROR] ${path.relative(ROOT_DIR, imagePath)}: ${error}`);
      }
    }

    printSummary({
      'Images found': allImageFiles.length,
      'Unreferenced': unreferencedImages.length,
      'Deleted': deleteCount,
    });
  } else {
    printSummary({
      'Images found': allImageFiles.length,
      'Unreferenced': unreferencedImages.length,
      'Would delete': unreferencedImages.length,
    });
    console.log('\n[DRY RUN] No files deleted. Run with --delete to remove.');
  }
}

main().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
