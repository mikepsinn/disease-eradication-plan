#!/usr/bin/env tsx
/**
 * Generate Image Metadata and Guide
 *
 * This script:
 * 1. Scans all images in assets/ folder
 * 2. Uses Gemini Vision API to generate detailed descriptions and metadata
 * 3. Updates image metadata (using PNG text chunks or EXIF)
 * 4. Generates assets/IMAGE-GUIDE.md with all image information
 *
 * Usage:
 *   pnpm tsx scripts/generate-image-metadata.ts [options]
 *
 * Options:
 *   --all              Process all images (default: only unprocessed)
 *   --skip-metadata    Skip updating image metadata, only generate guide
 *   --guide-only       Only regenerate guide from existing metadata
 *   --limit N          Process only N images (for testing)
 *   --pattern GLOB     Process only images matching pattern (e.g., "*.png")
 */

import { GoogleGenAI } from '@google/genai';
import fs from 'fs';
import path from 'path';
import sharp from 'sharp';
import dotenv from 'dotenv';
import { exiftool } from 'exiftool-vendored';
import { saveFile } from './lib/file-utils';

dotenv.config();

// Configuration
const GEMINI_MODEL_ID = 'gemini-2.5-flash';
const ASSETS_DIR = path.join(process.cwd(), 'assets');
const OUTPUT_GUIDE = path.join(ASSETS_DIR, 'IMAGE-GUIDE.md');
const METADATA_MARKER = 'ai-analyzed';

// Check for API key
const API_KEY = process.env.GOOGLE_GENERATIVE_AI_API_KEY;
if (!API_KEY) {
  throw new Error('GOOGLE_GENERATIVE_AI_API_KEY is not set in .env file');
}

// Initialize Gemini client
const genAI = new GoogleGenAI({ apiKey: API_KEY });

// Parse command line arguments
const args = process.argv.slice(2);
const options = {
  all: args.includes('--all'),
  skipMetadata: args.includes('--skip-metadata'),
  guideOnly: args.includes('--guide-only'),
  limit: args.find(a => a.startsWith('--limit'))?.split('=')[1] || null,
  pattern: args.find(a => a.startsWith('--pattern'))?.split('=')[1] || '**/*.{png,jpg,jpeg,gif,svg,webp}'
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
  // Get all files from assets directory
  const extensions = ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'];
  const allFiles = fs.readdirSync(ASSETS_DIR);

  const imageFiles = allFiles
    .filter(file => {
      const ext = path.extname(file).toLowerCase();
      return extensions.includes(ext);
    })
    .map(file => path.join(ASSETS_DIR, file));

  if (options.limit) {
    return imageFiles.slice(0, parseInt(options.limit));
  }

  return imageFiles;
}

/**
 * Check if image has already been analyzed
 */
async function isAnalyzed(filepath: string): Promise<boolean> {
  try {
    const tags = await exiftool.read(filepath);
    const comment = tags.Comment || tags.UserComment || '';
    return comment.toString().includes(METADATA_MARKER);
  } catch (error) {
    // File doesn't have metadata or exiftool can't read it
    return false;
  }
}

/**
 * Analyze image using Gemini Vision API
 */
async function analyzeImage(filepath: string): Promise<Partial<ImageMetadata>> {
  console.log(`  Analyzing with Gemini Vision API...`);

  try {
    // Read image as base64
    const imageBuffer = fs.readFileSync(filepath);
    const base64Image = imageBuffer.toString('base64');
    const mimeType = getMimeType(filepath);

    const prompt = `Analyze this image for a book about redirecting military spending to medical research (the "1% Treaty").

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

    const result = await genAI.models.generateContent({
      model: GEMINI_MODEL_ID,
      contents: [
        {
          parts: [
            { text: prompt },
            {
              inlineData: {
                mimeType: mimeType,
                data: base64Image
              }
            }
          ]
        }
      ]
    });

    const responseText = result.text || '';

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
 * Get MIME type from file extension
 */
function getMimeType(filepath: string): string {
  const ext = path.extname(filepath).toLowerCase();
  const mimeTypes: Record<string, string> = {
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.webp': 'image/webp',
    '.svg': 'image/svg+xml'
  };
  return mimeTypes[ext] || 'image/png';
}

/**
 * Update image metadata with analysis results
 */
async function updateImageMetadata(filepath: string, metadata: ImageMetadata): Promise<void> {
  if (options.skipMetadata) return;

  try {
    const metadataString = JSON.stringify({
      description: metadata.description,
      keywords: metadata.keywords,
      chapters: metadata.suggestedChapters,
      source: metadata.source || '',
      [METADATA_MARKER]: true
    });

    // Use exiftool-vendored to write metadata
    await exiftool.write(filepath, {
      Comment: metadataString,
      UserComment: metadataString,
      Description: metadata.description,
      Keywords: metadata.keywords
    });

    console.log(`  ✓ Metadata updated`);
  } catch (error) {
    console.log(`  ⚠ Could not update metadata:`, error);
  }
}

/**
 * Read existing metadata from image
 */
async function readImageMetadata(filepath: string): Promise<Partial<ImageMetadata>> {
  try {
    const tags = await exiftool.read(filepath);
    const comment = tags.Comment || tags.UserComment || '';
    const commentStr = comment.toString();

    if (commentStr.includes(METADATA_MARKER)) {
      try {
        const parsed = JSON.parse(commentStr);
        return {
          description: parsed.description,
          keywords: parsed.keywords || [],
          suggestedChapters: parsed.chapters || [],
          source: parsed.source,
          analyzed: true
        };
      } catch {
        // Metadata exists but not in JSON format
      }
    }
  } catch {
    // exiftool can't read this file or other error
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
  } catch {
    // Not a format sharp can read
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
  const existingMetadata = await readImageMetadata(filepath);

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
        const existing = await readImageMetadata(filepath);
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

  console.log(`\n✓ Complete! Processed ${allMetadata.length} images`);
  console.log(`\n📖 View the guide at: ${OUTPUT_GUIDE}`);

  // Clean up exiftool
  await exiftool.end();
}

// Run
main().catch(async error => {
  console.error('Fatal error:', error);
  await exiftool.end();
  process.exit(1);
});
