#!/usr/bin/env npx tsx
/**
 * Move images from assets/ root to assets/images/ and update all references
 *
 * Usage:
 *   npx tsx scripts/move-assets-to-images.ts [--dry-run]
 *
 * Options:
 *   --dry-run    Show what would be changed without making changes
 */

import fs from 'fs/promises';
import path from 'path';
import { glob } from 'glob';
import ignore from 'ignore';

const PROJECT_ROOT = path.resolve(import.meta.dirname, '..');
const ASSETS_DIR = path.join(PROJECT_ROOT, 'assets');
const TARGET_DIR = path.join(PROJECT_ROOT, 'assets', 'images');

// Image extensions to move
const IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.ico', '.mp4', '.webm', '.mov', '.avi'];

// File extensions to search for references
const SEARCHABLE_EXTENSIONS = [
  '.qmd', '.md', '.ts', '.tsx', '.js', '.jsx', '.py', '.yml', '.yaml',
  '.html', '.css', '.scss', '.json', '.toml', '.ini', '.sh', '.bat'
];

interface MoveOperation {
  oldPath: string;
  newPath: string;
  filename: string;
}

interface FileUpdate {
  filePath: string;
  count: number;
}

async function loadGitignore(): Promise<ReturnType<typeof ignore>> {
  const ig = ignore();

  // Always ignore these directories
  ig.add([
    'node_modules',
    '.git',
    '_book',
    '_freeze',
    '_build_temp',
    '.quarto',
    '.venv',
    'venv',
    '__pycache__',
    '.claude',
    'dist',
    'build',
  ]);

  // Load .gitignore if it exists
  const gitignorePath = path.join(PROJECT_ROOT, '.gitignore');
  try {
    const content = await fs.readFile(gitignorePath, 'utf-8');
    ig.add(content);
  } catch {
    // .gitignore doesn't exist, continue with defaults
  }

  return ig;
}

async function getImagesToMove(): Promise<MoveOperation[]> {
  const operations: MoveOperation[] = [];

  // Get all files in assets root (not subdirectories)
  const entries = await fs.readdir(ASSETS_DIR, { withFileTypes: true });

  for (const entry of entries) {
    if (!entry.isFile()) continue;

    const ext = path.extname(entry.name).toLowerCase();
    if (!IMAGE_EXTENSIONS.includes(ext)) continue;

    const oldPath = path.join(ASSETS_DIR, entry.name);
    const newPath = path.join(TARGET_DIR, entry.name);

    operations.push({
      oldPath,
      newPath,
      filename: entry.name,
    });
  }

  return operations;
}

async function getSearchableFiles(ig: ReturnType<typeof ignore>): Promise<string[]> {
  const patterns = SEARCHABLE_EXTENSIONS.map(ext => `**/*${ext}`);

  const files = await glob(patterns, {
    cwd: PROJECT_ROOT,
    absolute: true,
    nodir: true,
    ignore: ['**/node_modules/**', '**/.git/**'],
  });

  // Filter out gitignored files
  return files.filter(file => {
    const relativePath = path.relative(PROJECT_ROOT, file);
    return !ig.ignores(relativePath);
  });
}

function escapeRegex(str: string): string {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

async function updateFileReferences(
  filePath: string,
  operations: MoveOperation[],
  dryRun: boolean
): Promise<number> {
  let content: string;
  try {
    content = await fs.readFile(filePath, 'utf-8');
  } catch {
    return 0;
  }

  let updatedContent = content;
  let totalReplacements = 0;

  for (const op of operations) {
    // Build patterns for different reference styles
    const filename = op.filename;

    // Patterns to match:
    // - assets/filename.png
    // - /assets/filename.png
    // - ../assets/filename.png
    // - ../../assets/filename.png (etc)
    // - ./assets/filename.png

    const patterns = [
      // Absolute paths: /assets/file.png or assets/file.png
      new RegExp(`(["\`'(\\[])(/?)assets/${escapeRegex(filename)}(["\`')\\]])`, 'g'),
      // Relative paths: ../assets/file.png, ../../assets/file.png, ./assets/file.png
      new RegExp(`(["\`'(\\[])((?:\\.\\./)*|\\./?)assets/${escapeRegex(filename)}(["\`')\\]])`, 'g'),
      // Markdown image syntax: ![alt](assets/file.png)
      new RegExp(`(\\]\\()(/?)assets/${escapeRegex(filename)}(\\))`, 'g'),
      // Markdown image with relative: ![alt](../assets/file.png)
      new RegExp(`(\\]\\()((?:\\.\\./)*|\\./?)assets/${escapeRegex(filename)}(\\))`, 'g'),
      // HTML src/href: src="assets/file.png" or href="assets/file.png"
      new RegExp(`((?:src|href)=["'])(/?)assets/${escapeRegex(filename)}(["'])`, 'gi'),
      // HTML with relative paths
      new RegExp(`((?:src|href)=["'])((?:\\.\\./)*|\\./?)assets/${escapeRegex(filename)}(["'])`, 'gi'),
      // CSS url(): url(assets/file.png) or url("assets/file.png")
      new RegExp(`(url\\(["']?)(/?)assets/${escapeRegex(filename)}(["']?\\))`, 'gi'),
      // Quarto/YAML image fields
      new RegExp(`(image:\\s*["']?)(/?)assets/${escapeRegex(filename)}(["']?)`, 'gi'),
      // Cover image fields
      new RegExp(`(cover-image:\\s*["']?)(/?)assets/${escapeRegex(filename)}(["']?)`, 'gi'),
      new RegExp(`(epub-cover-image:\\s*["']?)(/?)assets/${escapeRegex(filename)}(["']?)`, 'gi'),
    ];

    for (const pattern of patterns) {
      const matches = updatedContent.match(pattern);
      if (matches) {
        totalReplacements += matches.length;
        updatedContent = updatedContent.replace(pattern, (match, prefix, slashOrRelative, suffix) => {
          // Preserve the slash or relative path prefix, just insert 'images/' after 'assets/'
          return `${prefix}${slashOrRelative || ''}assets/images/${filename}${suffix}`;
        });
      }
    }
  }

  if (totalReplacements > 0 && !dryRun) {
    await fs.writeFile(filePath, updatedContent, 'utf-8');
  }

  return totalReplacements;
}

async function main() {
  const args = process.argv.slice(2);
  const dryRun = args.includes('--dry-run');

  console.log('━'.repeat(80));
  console.log(`📁 Move Assets to Images Tool${dryRun ? ' [DRY RUN]' : ''}`);
  console.log('━'.repeat(80));
  console.log(`Source: assets/`);
  console.log(`Target: assets/images/`);
  console.log();

  // Step 1: Get images to move
  console.log('📋 Step 1: Finding images to move...');
  const operations = await getImagesToMove();
  console.log(`   Found ${operations.length} images in assets/ root`);

  if (operations.length === 0) {
    console.log('\n✅ No images to move!');
    return;
  }

  // Step 2: Ensure target directory exists
  console.log('\n📋 Step 2: Ensuring target directory exists...');
  if (!dryRun) {
    await fs.mkdir(TARGET_DIR, { recursive: true });
  }
  console.log(`   Target: assets/images/`);

  // Step 3: Load gitignore
  console.log('\n📋 Step 3: Loading .gitignore patterns...');
  const ig = await loadGitignore();

  // Step 4: Get searchable files
  console.log('\n📋 Step 4: Finding files to update...');
  const searchableFiles = await getSearchableFiles(ig);
  console.log(`   Found ${searchableFiles.length} searchable files`);

  // Step 5: Update references in all files
  console.log('\n📋 Step 5: Updating references...');
  const fileUpdates: FileUpdate[] = [];
  let totalUpdates = 0;

  for (const filePath of searchableFiles) {
    const count = await updateFileReferences(filePath, operations, dryRun);
    if (count > 0) {
      const relativePath = path.relative(PROJECT_ROOT, filePath);
      fileUpdates.push({ filePath: relativePath, count });
      totalUpdates += count;
    }
  }

  // Show updated files
  if (fileUpdates.length > 0) {
    const showCount = Math.min(10, fileUpdates.length);
    for (let i = 0; i < showCount; i++) {
      console.log(`   Updated ${fileUpdates[i].filePath}: ${fileUpdates[i].count} reference(s)`);
    }
    if (fileUpdates.length > showCount) {
      console.log(`   ... and ${fileUpdates.length - showCount} more files`);
    }
  } else {
    console.log('   No references found to update');
  }

  // Step 6: Move the files
  console.log('\n📋 Step 6: Moving image files...');
  let movedCount = 0;
  let skippedCount = 0;

  for (const op of operations) {
    try {
      // Check if target already exists
      try {
        await fs.access(op.newPath);
        console.log(`   ⚠️  Skipped ${op.filename} (already exists in target)`);
        skippedCount++;
        continue;
      } catch {
        // Target doesn't exist, good to move
      }

      if (!dryRun) {
        await fs.rename(op.oldPath, op.newPath);
      }
      movedCount++;
    } catch (error) {
      console.error(`   ❌ Failed to move ${op.filename}: ${error}`);
    }
  }

  if (movedCount > 0) {
    console.log(`   Moved ${movedCount} image(s)`);
  }
  if (skippedCount > 0) {
    console.log(`   Skipped ${skippedCount} image(s) (already exist)`);
  }

  // Summary
  console.log('\n' + '━'.repeat(80));
  console.log('📊 Summary');
  console.log('━'.repeat(80));
  console.log(`Images moved:          ${movedCount}`);
  console.log(`Images skipped:        ${skippedCount}`);
  console.log(`Files updated:         ${fileUpdates.length}`);
  console.log(`Total references:      ${totalUpdates}`);

  if (dryRun) {
    console.log('\n⚠️  DRY RUN - No files were actually modified');
    console.log('   Run without --dry-run to apply changes');
  } else {
    console.log('\n✅ Move complete!');
  }
  console.log('━'.repeat(80));
}

main().catch(err => {
  console.error('Error:', err);
  process.exit(1);
});
