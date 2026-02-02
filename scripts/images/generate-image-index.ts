/**
 * Generate a JSON index of all images in the project with metadata
 *
 * Supports incremental updates - only reprocesses files that have changed.
 *
 * Usage:
 *   npx tsx scripts/images/generate-image-index.ts           # Incremental update (fast)
 *   npx tsx scripts/images/generate-image-index.ts --force   # Full rebuild (slow)
 *
 * Output: assets/image-index.json
 */

import fs from 'fs/promises';
import path from 'path';
import { glob } from 'glob';
import sharp from 'sharp';

// Shared utilities
import { formatBytes } from '../lib/image-file-utils';
import { isExiftoolAvailable, readImageMetadata } from '../lib/exiftool-utils';
import {
  ImageMetadata,
  ImageIndex,
  cleanStyleFromText,
  getChapterFromPath,
} from '../lib/image-metadata';

export const OUTPUT_FILE = 'assets/image-index.json';

// Formats sharp can process (excludes ico)
const SHARP_SUPPORTED = ['jpg', 'jpeg', 'png', 'webp', 'gif', 'tiff', 'avif', 'svg'];

/**
 * Calculate aspect ratio string
 */
function getAspectRatio(width: number, height: number): string {
  const gcd = (a: number, b: number): number => b === 0 ? a : gcd(b, a % b);
  const divisor = gcd(width, height);
  const w = width / divisor;
  const h = height / divisor;

  // Simplify common ratios
  if (Math.abs(w / h - 16 / 9) < 0.05) return '16:9';
  if (Math.abs(w / h - 4 / 3) < 0.05) return '4:3';
  if (Math.abs(w / h - 1) < 0.05) return '1:1';
  if (Math.abs(w / h - 3 / 4) < 0.05) return '3:4';
  if (Math.abs(w / h - 9 / 16) < 0.05) return '9:16';

  return `${w}:${h}`;
}

/**
 * Determine image type from path/filename
 */
function getImageType(filePath: string): ImageMetadata['imageType'] {
  const lower = filePath.toLowerCase();
  if (lower.includes('-og-') || lower.includes('/og/') || lower.includes('-og.')) return 'og';
  if (lower.includes('-infographic-') || lower.includes('/infographics/')) return 'infographic';
  if (lower.includes('-slide-') || lower.includes('/slides/')) return 'slide';
  if (lower.includes('/icons/') || lower.includes('favicon') || lower.includes('-icon')) return 'icon';
  if (lower.includes('/cover/') || lower.includes('book-cover')) return 'cover';
  if (lower.includes('chart') || lower.includes('graph') || lower.includes('diagram')) return 'chart';
  return 'other';
}

/**
 * Extract style from filename
 */
function getStyle(filename: string): string | undefined {
  if (filename.includes('-academic')) return 'black and white academic';
  if (filename.includes('-retro')) return 'colorful retro-futuristic';
  return undefined;
}

/**
 * Extract metadata using exiftool (if available)
 */
async function getExiftoolMetadata(filePath: string): Promise<Partial<ImageMetadata>> {
  const exifData = await readImageMetadata(filePath);
  if (!exifData) return {};
  return exifData as Partial<ImageMetadata>;
}

/**
 * Process a single image file and return its metadata
 */
export async function processImage(
  filePath: string,
  useExiftool: boolean
): Promise<ImageMetadata> {
  const stats = await fs.stat(filePath);
  const relativePath = path.relative(process.cwd(), filePath).replace(/\\/g, '/');
  const filename = path.basename(filePath);
  const extension = path.extname(filePath).toLowerCase().slice(1);

  // Get image dimensions using sharp (skip unsupported formats)
  let width: number | undefined;
  let height: number | undefined;
  let format: string | undefined;

  if (SHARP_SUPPORTED.includes(extension)) {
    const sharpMeta = await sharp(filePath).metadata();
    width = sharpMeta.width;
    height = sharpMeta.height;
    format = sharpMeta.format;
  }

  const metadata: ImageMetadata = {
    path: relativePath,
    filename,
    extension,
    sizeBytes: stats.size,
    size: formatBytes(stats.size),
    width,
    height,
    format,
    aspectRatio: width && height ? getAspectRatio(width, height) : undefined,
    imageType: getImageType(relativePath),
    style: getStyle(filename),
    chapter: getChapterFromPath(relativePath),
  };

  // Get EXIF/IPTC metadata if exiftool is available
  if (useExiftool) {
    const exifMeta = await getExiftoolMetadata(filePath);
    Object.assign(metadata, exifMeta);
  }

  // Clean style words from title and description
  metadata.title = cleanStyleFromText(metadata.title);
  metadata.description = cleanStyleFromText(metadata.description);

  return metadata;
}

/**
 * Load existing index from disk
 */
export async function loadIndex(): Promise<ImageIndex | null> {
  const outputPath = path.join(process.cwd(), OUTPUT_FILE);
  try {
    const content = await fs.readFile(outputPath, 'utf-8');
    return JSON.parse(content) as ImageIndex;
  } catch {
    return null;
  }
}

/**
 * Save index to disk with retry logic for Windows file locking issues
 */
export async function saveIndex(index: ImageIndex, maxRetries = 5): Promise<void> {
  const outputPath = path.join(process.cwd(), OUTPUT_FILE);
  await fs.mkdir(path.dirname(outputPath), { recursive: true });

  let lastError: Error | null = null;
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      await fs.writeFile(outputPath, JSON.stringify(index, null, 2));
      return; // Success
    } catch (error) {
      lastError = error as Error;
      // Check if it's a file locking error (EBUSY, EACCES, UNKNOWN on Windows)
      const code = (error as NodeJS.ErrnoException).code;
      if (code === 'EBUSY' || code === 'EACCES' || code === 'UNKNOWN') {
        const delayMs = Math.min(100 * Math.pow(2, attempt - 1), 2000); // 100ms, 200ms, 400ms, 800ms, 1600ms
        console.warn(`  [RETRY ${attempt}/${maxRetries}] File locked, waiting ${delayMs}ms...`);
        await new Promise(resolve => setTimeout(resolve, delayMs));
      } else {
        throw error; // Non-retryable error
      }
    }
  }
  throw lastError; // All retries exhausted
}

/**
 * Update a single image entry in the index (for incremental updates)
 * This is exported for use by other scripts like enrich-image-metadata.ts
 *
 * Note: For batch updates, use updateImagesInIndexBatch() instead to avoid
 * file locking issues from rapid sequential writes.
 */
export async function updateImageInIndex(
  imagePath: string,
  newMetadata: Partial<ImageMetadata>
): Promise<void> {
  const index = await loadIndex();
  if (!index) {
    console.error('No existing index found. Run generate-image-index.ts first.');
    return;
  }

  const relativePath = path.relative(process.cwd(), imagePath).replace(/\\/g, '/');
  const existingIndex = index.images.findIndex(img => img.path === relativePath);

  if (existingIndex >= 0) {
    // Merge new metadata with existing (new values override old)
    index.images[existingIndex] = {
      ...index.images[existingIndex],
      ...newMetadata,
    };
  } else {
    // Image not in index - need to process it fully
    const useExiftool = await isExiftoolAvailable();
    const fullMetadata = await processImage(imagePath, useExiftool);
    index.images.push({ ...fullMetadata, ...newMetadata });
    index.images.sort((a, b) => a.path.localeCompare(b.path));
    index.totalImages = index.images.length;
    index.totalSizeBytes = index.images.reduce((sum, img) => sum + img.sizeBytes, 0);
    index.totalSize = formatBytes(index.totalSizeBytes);
  }

  await saveIndex(index);
}

/**
 * Batch update multiple images in the index with a single file write
 * This is more efficient and avoids file locking issues on Windows
 */
export async function updateImagesInIndexBatch(
  updates: Array<{ imagePath: string; metadata: Partial<ImageMetadata> }>
): Promise<void> {
  if (updates.length === 0) return;

  const index = await loadIndex();
  if (!index) {
    console.error('No existing index found. Run generate-image-index.ts first.');
    return;
  }

  const useExiftool = await isExiftoolAvailable();

  for (const { imagePath, metadata } of updates) {
    const relativePath = path.relative(process.cwd(), imagePath).replace(/\\/g, '/');
    const existingIndex = index.images.findIndex(img => img.path === relativePath);

    if (existingIndex >= 0) {
      index.images[existingIndex] = {
        ...index.images[existingIndex],
        ...metadata,
      };
    } else {
      const fullMetadata = await processImage(imagePath, useExiftool);
      index.images.push({ ...fullMetadata, ...metadata });
    }
  }

  // Re-sort and update totals
  index.images.sort((a, b) => a.path.localeCompare(b.path));
  index.totalImages = index.images.length;
  index.totalSizeBytes = index.images.reduce((sum, img) => sum + img.sizeBytes, 0);
  index.totalSize = formatBytes(index.totalSizeBytes);

  await saveIndex(index);
}

/**
 * Sync the image index with files on disk (incremental update)
 * Reads EXIF metadata from files and updates the index.
 * Returns stats about what was updated.
 */
export async function syncIndex(options?: {
  forceRebuild?: boolean;
  quiet?: boolean;
}): Promise<{ total: number; skipped: number; updated: number; removed: number }> {
  const forceRebuild = options?.forceRebuild ?? false;
  const quiet = options?.quiet ?? false;

  if (!quiet) {
    console.log(`[*] Syncing image index (${forceRebuild ? 'full rebuild' : 'incremental'})...`);
  }

  const useExiftool = await isExiftoolAvailable();

  // Find all image files
  const imageFiles = await glob('assets/**/*.{jpg,jpeg,png,gif,webp,svg,ico}', {
    cwd: process.cwd(),
    absolute: true,
    ignore: ['node_modules/**', '_book/**', '.quarto/**'],
  });

  // Load existing index for incremental mode
  const existingIndex = forceRebuild ? null : await loadIndex();
  const existingByPath = new Map<string, ImageMetadata>();
  const previousCount = existingIndex?.images.length ?? 0;
  if (existingIndex) {
    for (const img of existingIndex.images) {
      existingByPath.set(img.path, img);
    }
  }

  const images: ImageMetadata[] = [];
  let totalSize = 0;
  let processed = 0;
  let skipped = 0;
  let updated = 0;
  let added = 0;

  for (const filePath of imageFiles) {
    const relativePath = path.relative(process.cwd(), filePath).replace(/\\/g, '/');
    const stats = await fs.stat(filePath);

    // Check if we can skip this file (incremental mode) - use file size for change detection
    const existing = existingByPath.get(relativePath);
    if (existing && existing.sizeBytes === stats.size) {
      // File hasn't changed - reuse existing metadata
      images.push(existing);
      totalSize += existing.sizeBytes;
      skipped++;
    } else {
      // File is new or changed - process it to get fresh file metadata
      const freshMetadata = await processImage(filePath, useExiftool);

      if (existing) {
        // IMPORTANT: Preserve enriched metadata fields when merging
        // Fresh file metadata (size, dimensions, EXIF) takes priority
        // But enriched fields (socialCaption, qualityScore, etc.) are preserved
        const merged: ImageMetadata = {
          ...existing,       // Preserve all existing enriched fields
          ...freshMetadata,  // Overwrite with fresh file metadata
        };
        images.push(merged);
        updated++;
      } else {
        // New file - no existing metadata to preserve
        images.push(freshMetadata);
        added++;
      }
      totalSize += freshMetadata.sizeBytes;
    }

    processed++;
    if (!quiet && processed % 100 === 0) {
      console.log(`  Processed ${processed}/${imageFiles.length}...`);
    }
  }

  // Sort by path
  images.sort((a, b) => a.path.localeCompare(b.path));

  const index: ImageIndex = {
    totalImages: images.length,
    totalSizeBytes: totalSize,
    totalSize: formatBytes(totalSize),
    images,
  };

  await saveIndex(index);

  // Calculate removed: files that were in previous index but not found on disk
  const removed = previousCount - skipped - updated;

  if (!quiet) {
    const parts = [`${skipped} unchanged`];
    if (added > 0) parts.push(`${added} added`);
    if (updated > 0) parts.push(`${updated} updated`);
    if (removed > 0) parts.push(`${removed} removed`);
    console.log(`  [OK] Synced ${images.length} images (${parts.join(', ')})`);
  }

  return { total: images.length, skipped, updated, removed };
}

async function main() {
  const args = process.argv.slice(2);
  const forceRebuild = args.includes('--force');

  console.log('Generating image index...\n');
  console.log(`Mode: ${forceRebuild ? 'FULL REBUILD' : 'INCREMENTAL UPDATE'}\n`);

  const useExiftool = await isExiftoolAvailable();
  if (useExiftool) {
    console.log('[OK] exiftool available - will extract full metadata\n');
  } else {
    console.log('[WARN] exiftool not available - using basic metadata only\n');
  }

  const { total, skipped, updated, removed } = await syncIndex({ forceRebuild, quiet: false });

  // Reload index for stats
  const index = await loadIndex();
  if (!index) {
    console.error('Failed to load index after sync');
    process.exit(1);
  }

  const images = index.images;

  console.log('\n' + '='.repeat(60));
  console.log('Summary:');
  console.log(`  Total images: ${total}`);
  console.log(`  Total size: ${index.totalSize}`);
  console.log(`  Skipped (unchanged): ${skipped}`);
  console.log(`  Updated: ${updated}`);
  if (removed > 0) {
    console.log(`  Removed (deleted from disk): ${removed}`);
  }
  console.log(`  Output: ${OUTPUT_FILE}`);
  console.log('='.repeat(60));

  // Print breakdown by type
  const byType: Record<string, number> = {};
  for (const img of images) {
    const type = img.imageType || 'other';
    byType[type] = (byType[type] || 0) + 1;
  }
  console.log('\nBy type:');
  for (const [type, count] of Object.entries(byType).sort((a, b) => b[1] - a[1])) {
    console.log(`  ${type}: ${count}`);
  }

  // Print metadata coverage stats
  const withTranscript = images.filter(img => img.transcript).length;
  const withTitle = images.filter(img => img.title).length;
  const withDescription = images.filter(img => img.description).length;
  const withKeywords = images.filter(img => img.keywords && img.keywords.length > 0).length;

  console.log('\nMetadata coverage:');
  console.log(`  With transcript (OCR): ${withTranscript} (${((withTranscript / total) * 100).toFixed(0)}%)`);
  console.log(`  With title: ${withTitle} (${((withTitle / total) * 100).toFixed(0)}%)`);
  console.log(`  With description: ${withDescription} (${((withDescription / total) * 100).toFixed(0)}%)`);
  console.log(`  With keywords: ${withKeywords} (${((withKeywords / total) * 100).toFixed(0)}%)`);
}

// Only run main if this module is executed directly (not imported)
import { fileURLToPath } from 'url';
if (process.argv[1] === fileURLToPath(import.meta.url)) {
  main().catch(console.error);
}
