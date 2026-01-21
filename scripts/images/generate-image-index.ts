/**
 * Generate a JSON index of all images in the project with metadata
 *
 * Usage:
 *   npx tsx scripts/images/generate-image-index.ts
 *
 * Output: assets/image-search-index.json
 */

import fs from 'fs/promises';
import path from 'path';
import { glob } from 'glob';
import sharp from 'sharp';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

const OUTPUT_FILE = 'assets/image-search-index.json';

interface ImageMetadata {
  /** Relative path from project root */
  path: string;
  /** File name */
  filename: string;
  /** File extension */
  extension: string;
  /** File size in bytes */
  sizeBytes: number;
  /** Human-readable file size */
  size: string;
  /** Image width */
  width?: number;
  /** Image height */
  height?: number;
  /** Image format (jpeg, png, etc.) */
  format?: string;
  /** Aspect ratio as string (e.g., "16:9") */
  aspectRatio?: string;
  /** Last modified date */
  modified: string;
  /** Image type based on path/naming */
  imageType?: 'og' | 'infographic' | 'slide' | 'icon' | 'cover' | 'chart' | 'other';
  /** Style (academic, retro, etc.) */
  style?: string;
  /** Related chapter/section if applicable */
  chapter?: string;

  // EXIF/IPTC metadata (if available)
  /** Title/headline */
  title?: string;
  /** Description/caption */
  description?: string;
  /** Keywords/tags */
  keywords?: string[];
  /** Author/creator */
  author?: string;
  /** Copyright notice */
  copyright?: string;
  /** Creation date from EXIF */
  dateCreated?: string;
}

interface ImageIndex {
  generated: string;
  totalImages: number;
  totalSizeBytes: number;
  totalSize: string;
  images: ImageMetadata[];
}

/**
 * Format bytes to human-readable string
 */
function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / 1024 / 1024).toFixed(1)} MB`;
}

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
 * Clean title/description by removing style words
 */
function cleanStyleFromText(text: string | undefined): string | undefined {
  if (!text) return text;
  return text
    .replace(/\s*[-–]\s*(Retro|Academic)\s*/gi, ' ')
    .replace(/\b(Retro|Academic)\b\s*/gi, '')
    .replace(/\s+/g, ' ')
    .trim();
}

/**
 * Extract chapter/section from path
 */
function getChapter(filePath: string): string | undefined {
  // Look for knowledge/{section}/{chapter} pattern
  const match = filePath.match(/knowledge\/([^/]+)(?:\/([^/]+))?/);
  if (match) {
    if (match[2]) {
      // Remove file extension and suffixes
      const chapter = match[2].replace(/-(?:og|infographic|slide)-.*$/, '');
      return `${match[1]}/${chapter}`;
    }
    return match[1];
  }
  return undefined;
}

/**
 * Check if exiftool is available
 */
async function isExiftoolAvailable(): Promise<boolean> {
  try {
    await execAsync('exiftool -ver');
    return true;
  } catch {
    return false;
  }
}

/**
 * Extract metadata using exiftool (if available)
 */
async function getExiftoolMetadata(filePath: string): Promise<Partial<ImageMetadata>> {
  try {
    const { stdout } = await execAsync(
      `exiftool -json -Title -Description -Keywords -Author -Artist -Creator -Copyright -DateTimeOriginal -CreateDate "${filePath}"`,
      { maxBuffer: 1024 * 1024 }
    );

    const data = JSON.parse(stdout)[0];
    if (!data) return {};

    const metadata: Partial<ImageMetadata> = {};

    if (data.Title) metadata.title = data.Title;
    if (data.Description) metadata.description = data.Description;
    if (data.Keywords) {
      metadata.keywords = Array.isArray(data.Keywords) ? data.Keywords : [data.Keywords];
    }
    if (data.Author || data.Artist || data.Creator) {
      metadata.author = data.Author || data.Artist || data.Creator;
    }
    if (data.Copyright) metadata.copyright = data.Copyright;
    if (data.DateTimeOriginal || data.CreateDate) {
      metadata.dateCreated = data.DateTimeOriginal || data.CreateDate;
    }

    return metadata;
  } catch {
    return {};
  }
}

/**
 * Process a single image file
 */
async function processImage(
  filePath: string,
  useExiftool: boolean
): Promise<ImageMetadata | null> {
  try {
    const stats = await fs.stat(filePath);
    const relativePath = path.relative(process.cwd(), filePath).replace(/\\/g, '/');
    const filename = path.basename(filePath);
    const extension = path.extname(filePath).toLowerCase().slice(1);

    // Get image dimensions using sharp
    let width: number | undefined;
    let height: number | undefined;
    let format: string | undefined;

    try {
      const sharpMeta = await sharp(filePath).metadata();
      width = sharpMeta.width;
      height = sharpMeta.height;
      format = sharpMeta.format;
    } catch {
      // Not a valid image or unsupported format
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
      chapter: getChapter(relativePath),
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
  } catch (error) {
    console.error(`[ERROR] Failed to process ${filePath}:`, error);
    return null;
  }
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
    if (metadata) {
      images.push(metadata);
      totalSize += metadata.sizeBytes;
    }

    processed++;
    if (processed % 100 === 0) {
      console.log(`  Processed ${processed}/${imageFiles.length}...`);
    }
  }

  // Sort by path
  images.sort((a, b) => a.path.localeCompare(b.path));

  const index: ImageIndex = {
    generated: new Date().toISOString(),
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
}

main().catch(console.error);
