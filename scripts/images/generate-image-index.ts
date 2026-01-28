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
    modified: stats.mtime.toISOString(),
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
 * Save index to disk
 */
export async function saveIndex(index: ImageIndex): Promise<void> {
  const outputPath = path.join(process.cwd(), OUTPUT_FILE);
  await fs.mkdir(path.dirname(outputPath), { recursive: true });
  await fs.writeFile(outputPath, JSON.stringify(index, null, 2));
}

/**
 * Update a single image entry in the index (for incremental updates)
 * This is exported for use by other scripts like enrich-image-metadata.ts
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
    // Merge new metadata with existing
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

  // Find all image files
  const imageFiles = await glob('assets/**/*.{jpg,jpeg,png,gif,webp,svg,ico}', {
    cwd: process.cwd(),
    absolute: true,
    ignore: ['node_modules/**', '_book/**', '.quarto/**'],
  });

  console.log(`Found ${imageFiles.length} image files\n`);

  // Load existing index for incremental mode
  const existingIndex = forceRebuild ? null : await loadIndex();
  const existingByPath = new Map<string, ImageMetadata>();
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

  for (const filePath of imageFiles) {
    const relativePath = path.relative(process.cwd(), filePath).replace(/\\/g, '/');
    const stats = await fs.stat(filePath);
    const fileModified = stats.mtime.toISOString();

    // Check if we can skip this file (incremental mode)
    const existing = existingByPath.get(relativePath);
    if (existing && existing.modified === fileModified) {
      // File hasn't changed - reuse existing metadata
      images.push(existing);
      totalSize += existing.sizeBytes;
      skipped++;
    } else {
      // File is new or changed - process it
      const metadata = await processImage(filePath, useExiftool);
      images.push(metadata);
      totalSize += metadata.sizeBytes;
      updated++;
    }

    processed++;
    if (processed % 100 === 0) {
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

  console.log('\n' + '='.repeat(60));
  console.log('Summary:');
  console.log(`  Total images: ${images.length}`);
  console.log(`  Total size: ${formatBytes(totalSize)}`);
  console.log(`  Skipped (unchanged): ${skipped}`);
  console.log(`  Updated/added: ${updated}`);
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
  console.log(`  With transcript (OCR): ${withTranscript} (${((withTranscript / images.length) * 100).toFixed(0)}%)`);
  console.log(`  With title: ${withTitle} (${((withTitle / images.length) * 100).toFixed(0)}%)`);
  console.log(`  With description: ${withDescription} (${((withDescription / images.length) * 100).toFixed(0)}%)`);
  console.log(`  With keywords: ${withKeywords} (${((withKeywords / images.length) * 100).toFixed(0)}%)`);
}

// Only run main if this module is executed directly (not imported)
import { fileURLToPath } from 'url';
if (process.argv[1] === fileURLToPath(import.meta.url)) {
  main().catch(console.error);
}
