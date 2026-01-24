#!/usr/bin/env tsx
/**
 * AI Image Analysis and Metadata Tagging
 *
 * This script:
 * 1. Scans all images in assets/ folder
 * 2. Uses Gemini Vision API to generate detailed descriptions and metadata
 * 3. Updates image metadata (using PNG text chunks or EXIF)
 * 4. Generates assets/IMAGE-GUIDE.md with all image information
 *
 * Usage:
 *   pnpm tsx scripts/images/analyze-and-tag.ts [options]
 *
 * Options:
 *   --all              Process all images (default: only unprocessed)
 *   --skip-metadata    Skip updating image metadata, only generate guide
 *   --guide-only       Only regenerate guide from existing metadata
 *   --limit N          Process only N images (for testing)
 *   --pattern GLOB     Process only images matching pattern (e.g., "*.png")
 */

import { generateGeminiVisionContent, GEMINI_FLASH_MODEL_ID } from '../lib/llm';
import fs from 'fs';
import path from 'path';
import sharp from 'sharp';
import { saveFile } from '../lib/file-utils';

// Shared utilities
import { findImages, getMimeType, SUPPORTED_IMAGE_EXTENSIONS } from '../lib/image-file-utils';
import { readImageMetadata as readExifMetadata, writeImageMetadata as writeExifMetadata } from '../lib/exiftool-utils';
import { parseCommonArgs, getArgValue, hasFlag, printHeader, printSummary } from '../lib/cli-utils';

// Configuration
const ASSETS_DIR = path.join(process.cwd(), 'assets');
const OUTPUT_GUIDE = path.join(ASSETS_DIR, 'IMAGE-GUIDE.md');
const METADATA_MARKER = 'ai-analyzed';

// Parse command line arguments
const args = process.argv.slice(2);
const commonOptions = parseCommonArgs(args);
const options = {
  all: commonOptions.all,
  skipMetadata: hasFlag(args, 'skip-metadata'),
  guideOnly: hasFlag(args, 'guide-only'),
  limit: commonOptions.limit,
  pattern: getArgValue(args, 'pattern') || '**/*.{png,jpg,jpeg,gif,svg,webp}'
};

interface ImageMetadata {
  filepath: string;
  filename: string;
  description: string;
  keywords: string[];
  suggestedChapters: string[];
  source?: string;
  fileSize: number;
  dimensions?: { width: number; height: number };
  format: string;
  analyzed: boolean;
}

/**
 * Get list of all image files in assets directory
 */
async function getImageFiles(): Promise<string[]> {
  // Use shared findImages utility
  let imageFiles = await findImages(ASSETS_DIR, { recursive: false });

  if (options.limit) {
    imageFiles = imageFiles.slice(0, options.limit);
  }

  return imageFiles;
}

/**
 * Check if image has already been analyzed
 */
async function isAnalyzed(filepath: string): Promise<boolean> {
  try {
    const metadata = await readExifMetadata(filepath);
    // Check if the metadata contains our marker
    return metadata !== null && metadata.description?.includes(METADATA_MARKER) === true;
  } catch (error) {
    // File doesn't have metadata or exiftool can't read it
    return false;
  }
}

/**
 * Analyze image using Gemini Vision API via lib/llm.ts
 */
async function analyzeImage(filepath: string): Promise<Partial<ImageMetadata>> {
  console.log(`  Analyzing with Gemini Vision API (${GEMINI_FLASH_MODEL_ID})...`);

  try {
    // Read image as base64
    const imageBuffer = fs.readFileSync(filepath);
    const base64Image = imageBuffer.toString('base64');
    const mimeType = getMimeType(filepath);

    const prompt = `Analyze this image for a book about redirecting military spending to medical research (a "1% treaty").

Provide:
1. DESCRIPTION: Detailed description of what the image shows (2-3 sentences)
2. KEYWORDS: 5-10 relevant keywords/tags (comma-separated)
3. CHAPTERS: Which book chapters would benefit from this image? Consider:
   - Problem chapters: the-daily-massacre, cost-of-war, cost-of-disease, fda-is-unsafe-and-ineffective, nih-spent-1-trillion-eradicating-0-diseases, unrepresentative-democracy, regulatory-capture, the-119-trillion-death-toilet
   - Solution chapters: 1-percent-treaty, wishocracy, dfda, dih, positron, war-on-disease
   - Proof chapters: historical-precedents, economics, futures
   - Strategy chapters: global-referendum, viral-marketing, legislation-package, roadmap
4. PRIMARY_USE: Which 1-2 chapters should use this as a PRIMARY/key visual?

Format your response EXACTLY as:
DESCRIPTION: [your description]
KEYWORDS: [keyword1, keyword2, keyword3, ...]
CHAPTERS: [chapter1.qmd, chapter2.qmd, ...]
PRIMARY_USE: [chapter1.qmd]`;

    const responseText = await generateGeminiVisionContent(prompt, base64Image, mimeType);

    // Parse response
    const descMatch = responseText.match(/DESCRIPTION:\s*(.+?)(?=\n[A-Z]+:|$)/s);
    const keywordsMatch = responseText.match(/KEYWORDS:\s*(.+?)(?=\n[A-Z]+:|$)/s);
    const chaptersMatch = responseText.match(/CHAPTERS:\s*(.+?)(?=\n[A-Z]+:|$)/s);
    const primaryMatch = responseText.match(/PRIMARY_USE:\s*(.+?)(?=\n[A-Z]+:|$)/s);

    // Clean up keywords - remove brackets and split
    let keywords: string[] = [];
    if (keywordsMatch) {
      const keywordText = keywordsMatch[1].replace(/[\[\]]/g, '');
      keywords = keywordText.split(',').map(k => k.trim()).filter(Boolean);
    }

    // Clean up chapters - remove brackets and split
    let chapters: string[] = [];
    if (chaptersMatch) {
      const chapterText = chaptersMatch[1].replace(/[\[\]]/g, '');
      chapters = chapterText.split(',').map(c => c.trim()).filter(Boolean);
    }

    // Clean up primary chapter - remove brackets
    let primaryChapter = '';
    if (primaryMatch) {
      primaryChapter = primaryMatch[1].replace(/[\[\]]/g, '').trim();
    }

    // Add star to primary chapter
    const suggestedChapters = chapters.map(c =>
      c === primaryChapter ? `⭐ ${c}` : c
    );

    return {
      description: descMatch ? descMatch[1].trim() : 'No description generated',
      keywords,
      suggestedChapters,
      analyzed: true
    };

  } catch (error) {
    console.error(`  Error analyzing image:`, error);
    return {
      description: 'Error during analysis',
      keywords: [],
      suggestedChapters: [],
      analyzed: false
    };
  }
}

/**
 * Update image metadata with analysis results
 */
async function updateImageMetadata(filepath: string, metadata: ImageMetadata): Promise<void> {
  if (options.skipMetadata) return;

  try {
    // Use shared writeImageMetadata utility
    await writeExifMetadata(filepath, {
      description: `${metadata.description} [${METADATA_MARKER}]`,
      keywords: metadata.keywords,
      // Store additional data in the JSON blob
      chapters: metadata.suggestedChapters,
      source: metadata.source,
    });

    console.log(`  [OK] Metadata updated`);
  } catch (error) {
    console.log(`  [WARN] Could not update metadata:`, error);
  }
}

/**
 * Read existing metadata from image
 */
async function readLocalImageMetadata(filepath: string): Promise<Partial<ImageMetadata>> {
  try {
    const exifData = await readExifMetadata(filepath);

    if (exifData && exifData.description?.includes(METADATA_MARKER)) {
      return {
        description: exifData.description?.replace(` [${METADATA_MARKER}]`, ''),
        keywords: exifData.keywords || [],
        suggestedChapters: (exifData as any).chapters || [],
        source: (exifData as any).source,
        analyzed: true
      };
    }
  } catch (error) {
    console.warn(`Could not read metadata from ${filepath}:`, error);
  }

  return { analyzed: false };
}

/**
 * Get image file information
 */
async function getImageInfo(filepath: string): Promise<Partial<ImageMetadata>> {
  const stats = fs.statSync(filepath);
  const filename = path.basename(filepath);
  const format = path.extname(filepath).slice(1).toUpperCase();

  let dimensions;
  try {
    const metadata = await sharp(filepath).metadata();
    dimensions = { width: metadata.width || 0, height: metadata.height || 0 };
  } catch (error) {
    console.warn(`Could not read image dimensions for ${filepath}:`, error);
  }

  return {
    filepath,
    filename,
    fileSize: stats.size,
    format,
    dimensions
  };
}

/**
 * Process a single image
 */
async function processImage(filepath: string): Promise<ImageMetadata> {
  console.log(`\nProcessing: ${path.relative(ASSETS_DIR, filepath)}`);

  // Get basic file info
  const fileInfo = await getImageInfo(filepath);

  // Check if already analyzed
  const existingMetadata = await readLocalImageMetadata(filepath);

  if (!options.all && existingMetadata.analyzed) {
    console.log(`  ✓ Already analyzed, skipping`);
    return { ...fileInfo, ...existingMetadata } as ImageMetadata;
  }

  // Analyze with Gemini
  const analysisResult = await analyzeImage(filepath);

  // Combine all metadata
  const metadata: ImageMetadata = {
    ...fileInfo,
    ...analysisResult
  } as ImageMetadata;

  // Update image metadata
  await updateImageMetadata(filepath, metadata);

  return metadata;
}

/**
 * Generate markdown guide from all image metadata
 */
async function generateGuide(allMetadata: ImageMetadata[]): Promise<void> {
  console.log(`\nGenerating IMAGE-GUIDE.md...`);

  // Group images by category (based on keywords)
  const categories: Record<string, ImageMetadata[]> = {
    'ThinkByNumbers.org Sources': [],
    'FDA & Medical Research': [],
    'Military & War Costs': [],
    'Democracy & Governance': [],
    'Health Data & Charts': [],
    'Platform & Architecture': [],
    'Logos & Branding': [],
    'Other': []
  };

  for (const img of allMetadata) {
    const keywords = img.keywords.join(' ').toLowerCase();

    if (img.source?.includes('thinkbynumbers.org') || img.filename.includes('death-and-dollars')) {
      categories['ThinkByNumbers.org Sources'].push(img);
    } else if (keywords.includes('fda') || keywords.includes('drug') || keywords.includes('treatment')) {
      categories['FDA & Medical Research'].push(img);
    } else if (keywords.includes('military') || keywords.includes('war') || keywords.includes('nuclear')) {
      categories['Military & War Costs'].push(img);
    } else if (keywords.includes('democracy') || keywords.includes('voter') || keywords.includes('governance')) {
      categories['Democracy & Governance'].push(img);
    } else if (keywords.includes('chart') || keywords.includes('graph') || keywords.includes('data')) {
      categories['Health Data & Charts'].push(img);
    } else if (keywords.includes('platform') || keywords.includes('architecture') || keywords.includes('diagram')) {
      categories['Platform & Architecture'].push(img);
    } else if (keywords.includes('logo') || keywords.includes('brand') || keywords.includes('icon')) {
      categories['Logos & Branding'].push(img);
    } else {
      categories['Other'].push(img);
    }
  }

  let guide = `# Image Asset Guide

This guide catalogs all images in the \`assets/\` folder with AI-generated descriptions and usage recommendations.

**Last Updated:** ${new Date().toISOString().split('T')[0]}
**Total Images:** ${allMetadata.length}

---

`;

  // Write each category
  for (const [category, images] of Object.entries(categories)) {
    if (images.length === 0) continue;

    guide += `## ${category}\n\n`;

    for (const img of images.sort((a, b) => a.filename.localeCompare(b.filename))) {
      const sizeKB = (img.fileSize / 1024).toFixed(1);
      const dims = img.dimensions ?
        `${img.dimensions.width}x${img.dimensions.height}` : 'N/A';

      guide += `### ${img.filename}\n\n`;
      guide += `**File:** \`${img.filename}\`  \n`;
      guide += `**Size:** ${sizeKB} KB | **Format:** ${img.format} | **Dimensions:** ${dims}\n\n`;

      if (img.source) {
        guide += `**Source:** ${img.source}\n\n`;
      }

      guide += `**Description:** ${img.description}\n\n`;

      if (img.keywords.length > 0) {
        guide += `**Keywords:** ${img.keywords.join(', ')}\n\n`;
      }

      if (img.suggestedChapters.length > 0) {
        guide += `**Suggested Chapters:**\n`;
        for (const chapter of img.suggestedChapters) {
          guide += `- ${chapter}\n`;
        }
        guide += `\n`;
      }

      guide += `---\n\n`;
    }
  }

  // Add quick reference index
  guide += `## Quick Reference: All Images\n\n`;
  guide += `| Filename | Size | Format | Primary Chapter |\n`;
  guide += `|----------|------|--------|----------------|\n`;

  for (const img of allMetadata.sort((a, b) => a.filename.localeCompare(b.filename))) {
    const sizeKB = (img.fileSize / 1024).toFixed(0);
    const primary = img.suggestedChapters.find(c => c.includes('⭐'))?.replace('⭐ ', '') || '-';
    guide += `| ${img.filename} | ${sizeKB} KB | ${img.format} | ${primary} |\n`;
  }

  guide += `\n---\n\n`;
  guide += `*This guide was automatically generated by \`scripts/generate-image-metadata.ts\`*\n`;
  guide += `*To update: \`pnpm tsx scripts/generate-image-metadata.ts\`*\n`;

  await saveFile(OUTPUT_GUIDE, guide);
  console.log(`✓ Guide written to ${OUTPUT_GUIDE}`);
}

/**
 * Main execution
 */
async function main() {
  console.log('🖼️  Image Metadata Generator\n');
  console.log(`Options:`, options);

  if (options.guideOnly) {
    console.log('\n📖 Guide-only mode: Reading existing metadata...\n');
  }

  // Get all image files
  const imageFiles = await getImageFiles();
  console.log(`\nFound ${imageFiles.length} images to process\n`);

  if (imageFiles.length === 0) {
    console.log('No images found matching pattern');
    return;
  }

  // Process each image
  const allMetadata: ImageMetadata[] = [];

  for (let i = 0; i < imageFiles.length; i++) {
    const filepath = imageFiles[i];
    console.log(`[${i + 1}/${imageFiles.length}]`);

    try {
      if (options.guideOnly) {
        // Just read existing metadata
        const fileInfo = await getImageInfo(filepath);
        const existing = await readLocalImageMetadata(filepath);
        allMetadata.push({ ...fileInfo, ...existing } as ImageMetadata);
      } else {
        // Full processing
        const metadata = await processImage(filepath);
        allMetadata.push(metadata);
      }
    } catch (error) {
      console.error(`  ✗ Error processing ${filepath}:`, error);
    }

    // Rate limiting: wait 1 second between API calls
    if (!options.guideOnly && i < imageFiles.length - 1) {
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }

  // Generate markdown guide
  await generateGuide(allMetadata);

  console.log(`\n[OK] Complete! Processed ${allMetadata.length} images`);
  console.log(`\nView the guide at: ${OUTPUT_GUIDE}`);
}

// Run
main().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
