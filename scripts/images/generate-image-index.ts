/**
 * Generate a JSON index of all images in the project with metadata
 *
 * Also generates missing metadata (transcript, inferredPrompt, etc.) using Gemini
 *
 * Usage:
 *   npx tsx scripts/images/generate-image-index.ts           # Index only, skip missing metadata
 *   npx tsx scripts/images/generate-image-index.ts --fill    # Generate missing metadata with Gemini
 *   npx tsx scripts/images/generate-image-index.ts --force   # Regenerate ALL metadata (overwrite existing)
 *   npx tsx scripts/images/generate-image-index.ts --limit N # Limit to N images for testing
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

const OUTPUT_FILE = 'assets/image-index.json';

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


// isExiftoolAvailable imported from ../lib/exiftool-utils

/**
 * Extract metadata using exiftool (if available)
 * Uses shared readImageMetadata from exiftool-utils
 */
async function getExiftoolMetadata(filePath: string): Promise<Partial<ImageMetadata>> {
  const exifData = await readImageMetadata(filePath);
  if (!exifData) return {};

  const metadata: Partial<ImageMetadata> = {};

  if (exifData.title) metadata.title = exifData.title;
  if (exifData.description) metadata.description = exifData.description;
  if (exifData.keywords) metadata.keywords = exifData.keywords;
  if (exifData.transcript) metadata.transcript = exifData.transcript;
  if (exifData.generationPrompt) metadata.generationPrompt = exifData.generationPrompt;
  if (exifData.inferredPrompt) metadata.inferredPrompt = exifData.inferredPrompt;
  if (exifData.imageIssues) metadata.imageIssues = exifData.imageIssues;
  if (exifData.promptImprovements) metadata.promptImprovements = exifData.promptImprovements;

  return metadata;
}

/**
 * Process a single image file
 */
// Formats sharp can process (excludes ico, svg, etc.)
const SHARP_SUPPORTED = ['jpg', 'jpeg', 'png', 'webp', 'gif', 'tiff', 'avif'];

async function processImage(
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

async function main() {
  console.log('Generating image search index...\n');

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

  const images: ImageMetadata[] = [];
  let totalSize = 0;
  let processed = 0;

  for (const filePath of imageFiles) {
    const metadata = await processImage(filePath, useExiftool);
    images.push(metadata);
    totalSize += metadata.sizeBytes;

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

  // Write output
  const outputPath = path.join(process.cwd(), OUTPUT_FILE);
  await fs.mkdir(path.dirname(outputPath), { recursive: true });
  await fs.writeFile(outputPath, JSON.stringify(index, null, 2));

  console.log('\n' + '='.repeat(60));
  console.log('Summary:');
  console.log(`  Total images: ${images.length}`);
  console.log(`  Total size: ${formatBytes(totalSize)}`);
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

main().catch(console.error);
