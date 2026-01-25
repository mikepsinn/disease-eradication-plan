/**
 * Generate OG images, infographics, and slides for book chapters
 * Uses a lock file to prevent multiple instances from running simultaneously
 *
 * Usage:
 *   npx tsx scripts/images/generate-chapters.ts [file-filter] [options]
 *
 * Options:
 *   --force                   Regenerate all images even if they already exist
 *   --analyze-first           Use Gemini Flash to analyze if image would be helpful before generating
 *   --academic-style          Generate in academic style (black & white) instead of retro
 *   --with-reference-images   Extract existing images from QMD and use as reference for generation
 *   --outdated                Only regenerate images that are outdated (outputs detailed report of all files)
 *
 * Examples:
 *   # Force regenerate all images in academic style
 *   npx tsx scripts/images/generate-chapters.ts --force
 *
 *   # Generate with intelligent analysis for economics.qmd
 *   npx tsx scripts/images/generate-chapters.ts economics --analyze-first --academic-style
 *
 *   # Generate all missing images with analysis
 *   npx tsx scripts/images/generate-chapters.ts --analyze-first --academic-style
 *
 *   # Regenerate only outdated images (shows detailed report first)
 *   npx tsx scripts/images/generate-chapters.ts --outdated
 */

import dotenv from 'dotenv';
import path from 'path';
import fs from 'fs/promises';
import { existsSync, unlinkSync } from 'fs';
import matter from 'gray-matter';
import { generateAndSaveImages, ImageMetadata } from '../lib/gemini-images';
import { generateGeminiFlashContent, generateGeminiProContent } from '../lib/llm';
import {
  getBookFilesForProcessing,
  stringifyWithFrontmatter,
  getCleanedContentForLLM,
  extractReferenceImages,
  getSiteUrl,
  loadQuartoVariables,
  replaceQuartoVariables
} from '../lib/file-utils';
import { ImagePrompts, VisualStyles, VisualStyleName } from '../lib/image-prompts';

// Load environment variables
dotenv.config();

// Cache for Quarto variables (loaded once at startup)
let cachedVariables: Map<string, string> | null = null;

/**
 * Get cached Quarto variables (loads on first call)
 */
async function getVariables(): Promise<Map<string, string>> {
  if (!cachedVariables) {
    cachedVariables = await loadQuartoVariables();
  }
  return cachedVariables;
}

/**
 * Replace Quarto variables in a string (e.g., title or description)
 * Returns the original string if it's undefined
 */
async function replaceVariablesInString(str: string | undefined): Promise<string | undefined> {
  if (!str) return str;
  const variables = await getVariables();
  return replaceQuartoVariables(str, variables);
}

// Lock file configuration
const LOCK_FILE = path.join(process.cwd(), '.generate-images.lock');

/**
 * Clean content for image generation using LLM
 * Removes meta-content, navigation, chapter references, etc.
 */
async function cleanContentForImageGeneration(
  content: string,
  imageType: 'og' | 'infographic' | 'slide'
): Promise<string> {
  const prompt = `Remove content that would be absolutely useless for generating a ${imageType} image.

Character limit: ${imageType === 'og' ? '1600 max' : imageType === 'infographic' ? '4000 max' : '2400 max'}

Filter out: methodology details, citations, navigation, chapter references, verbose explanations.
Keep exact wording - do not rephrase anything.

${content}

FILTERED:`;

  try {
    const responseText = await generateGeminiFlashContent(prompt);
    return responseText.trim();
  } catch (error) {
    console.error('[WARN] Error cleaning content with LLM, using original:', error);
    // Fallback to original content if LLM cleaning fails
    return content;
  }
}

/**
 * Extract key content for a PowerPoint slide from QMD content
 * Extracts exact sentences - does NOT rephrase or editorialize
 * Prioritizes entertaining, surprising, and informative content
 */
async function extractSlideContent(content: string, title?: string, description?: string): Promise<string> {
  const prompt = `Extract key content for a single slide. Maximum 400 characters. Include the most important statistic and one vivid analogy. Verbatim only.

${title ? `Topic: ${title}\n` : ''}
${content.substring(0, 6000)}

SLIDE TEXT:`;

  try {
    const responseText = await generateGeminiProContent(prompt);
    const extractedContent = responseText.trim();

    // Combine title, description, and extracted content without labels
    const parts: string[] = [];
    if (title) parts.push(title);
    if (description) parts.push(description);
    parts.push(extractedContent);

    return parts.join('\n\n');
  } catch (error) {
    console.error('[WARN] Error extracting slide content, using truncated original:', error);
    const parts: string[] = [];
    if (title) parts.push(title);
    if (description) parts.push(description);
    parts.push(content.substring(0, 300));
    return parts.join('\n\n');
  }
}

/**
 * Check if a process is running (Windows-compatible)
 */
async function isProcessRunning(pid: number): Promise<boolean> {
  try {
    // On Windows, process.kill(pid, 0) doesn't work reliably
    // Use tasklist to check if process exists
    if (process.platform === 'win32') {
      const { exec } = await import('child_process');
      return new Promise((resolve) => {
        exec(`tasklist /FI "PID eq ${pid}" /NH`, (error, stdout) => {
          if (error) {
            resolve(false);
            return;
          }
          resolve(stdout.toLowerCase().includes('node.exe'));
        });
      });
    } else {
      // On Unix-like systems, sending signal 0 checks if process exists
      process.kill(pid, 0);
      return true;
    }
  } catch {
    return false;
  }
}

/**
 * Acquire lock file, preventing multiple instances from running
 * Kills existing instance if it's still running
 */
async function acquireLock(): Promise<void> {
  try {
    const lockContent = await fs.readFile(LOCK_FILE, 'utf-8');
    const existingPid = parseInt(lockContent.trim(), 10);

    if (existingPid && await isProcessRunning(existingPid)) {
      console.error(`ERROR: Another instance is already running (PID: ${existingPid})`);
      console.error('Attempting to kill existing process...');

      try {
        process.kill(existingPid, 'SIGTERM');
        // Wait a moment for process to die
        await new Promise(resolve => setTimeout(resolve, 2000));

        // Check if it's still running
        if (await isProcessRunning(existingPid)) {
          console.error('Failed to kill existing process. Please manually stop it and try again.');
          process.exit(1);
        } else {
          console.log('Successfully killed existing process.');
        }
      } catch (killError) {
        console.error('Failed to kill existing process:', killError);
        process.exit(1);
      }
    }
  } catch {
    // Lock file doesn't exist, which is fine
  }

  // Write current PID to lock file
  await fs.writeFile(LOCK_FILE, process.pid.toString(), 'utf-8');
  console.log(`[LOCK] Acquired lock file (PID: ${process.pid})`);
}

/**
 * Release lock file on exit
 */
async function releaseLock(): Promise<void> {
  try {
    await fs.unlink(LOCK_FILE);
    console.log('[LOCK] Released lock file');
  } catch {
    // Lock file already removed, no problem
  }
}

// Ensure lock is released on exit
process.on('exit', () => {
  try {
    // Synchronous version for exit handler
    const lockPath = path.join(process.cwd(), '.generate-images.lock');
    if (existsSync(lockPath)) {
      unlinkSync(lockPath);
    }
  } catch {
    // Ignore errors during cleanup
  }
});

process.on('SIGINT', async () => {
  console.log('\n[SIGINT] Received interrupt signal, cleaning up...');
  await releaseLock();
  process.exit(130);
});

process.on('SIGTERM', async () => {
  console.log('\n[SIGTERM] Received termination signal, cleaning up...');
  await releaseLock();
  process.exit(143);
});

process.on('uncaughtException', async (error) => {
  console.error('[ERROR] Uncaught exception:', error);
  await releaseLock();
  process.exit(1);
});

/**
 * Get the git modified date of a file
 * Returns null if file is not tracked by git or git command fails
 */
async function getGitModifiedDate(filePath: string): Promise<Date | null> {
  try {
    const { exec } = await import('child_process');
    return new Promise((resolve) => {
      // Get the last commit date that modified this file
      exec(
        `git log -1 --format=%cI -- "${filePath}"`,
        { cwd: process.cwd() },
        (error, stdout) => {
          if (error || !stdout.trim()) {
            resolve(null);
            return;
          }
          const date = new Date(stdout.trim());
          resolve(isNaN(date.getTime()) ? null : date);
        }
      );
    });
  } catch {
    return null;
  }
}

/**
 * Check if QMD file is newer than any of its associated images
 * Returns true if QMD should be regenerated (newer or images missing)
 */
async function isQmdNewerThanImages(
  qmdPath: string,
  imagePaths: string[]
): Promise<{ needsRegeneration: boolean; reason: string }> {
  const qmdDate = await getGitModifiedDate(qmdPath);

  if (!qmdDate) {
    return { needsRegeneration: true, reason: 'QMD file not tracked by git or no commit history' };
  }

  // Check each image path
  for (const imagePath of imagePaths) {
    if (!existsSync(imagePath)) {
      return { needsRegeneration: true, reason: `Image missing: ${path.basename(imagePath)}` };
    }

    const imageDate = await getGitModifiedDate(imagePath);

    if (!imageDate) {
      // Image exists but not tracked by git - consider it stale
      return { needsRegeneration: true, reason: `Image not tracked by git: ${path.basename(imagePath)}` };
    }

    if (qmdDate > imageDate) {
      return {
        needsRegeneration: true,
        reason: `QMD updated (${qmdDate.toISOString().split('T')[0]}) after image (${imageDate.toISOString().split('T')[0]})`
      };
    }
  }

  return { needsRegeneration: false, reason: 'All images are up to date' };
}

/**
 * File status information for the detailed report
 */
interface FileImageStatus {
  qmdPath: string;
  qmdDate: Date | null;
  images: {
    type: 'OG' | 'Infographic' | 'Slide';
    path: string;
    exists: boolean;
    date: Date | null;
  }[];
  needsRegeneration: boolean;
  reason: string;
}

/**
 * Get detailed status for a QMD file and its images
 */
async function getFileImageStatus(filePath: string): Promise<FileImageStatus | null> {
  const fileName = path.basename(filePath, '.qmd');

  // Skip index.qmd files
  if (fileName === 'index') {
    return null;
  }

  // Read frontmatter
  const fileContent = await fs.readFile(filePath, 'utf-8');
  const { data: frontmatter } = matter(fileContent);

  if (!frontmatter.title && !frontmatter.description) {
    return null;
  }

  const relativePath = path.relative(process.cwd(), filePath);
  const ogOutputDir = path.join(process.cwd(), 'assets', 'og-images', path.dirname(relativePath));
  const infographicOutputDir = path.join(process.cwd(), 'assets', 'infographics', path.dirname(relativePath));
  const slideOutputDir = path.join(process.cwd(), 'assets', 'slides', path.dirname(relativePath));

  // Only check academic style (that's what we generate)
  const suffix = VisualStyles['bw-academic'].suffix;
  const ogPath = path.join(ogOutputDir, `${fileName}-og${suffix}.jpg`);
  const infographicPath = path.join(infographicOutputDir, `${fileName}-infographic${suffix}.jpg`);
  const slidePath = path.join(slideOutputDir, `${fileName}-slide${suffix}.jpg`);

  const qmdDate = await getGitModifiedDate(filePath);

  const images: FileImageStatus['images'] = [];

  // Get OG image status
  const ogExists = existsSync(ogPath);
  const ogDate = ogExists ? await getGitModifiedDate(ogPath) : null;
  images.push({
    type: 'OG',
    path: path.relative(process.cwd(), ogPath),
    exists: ogExists,
    date: ogDate,
  });

  // Get Infographic image status
  const infographicExists = existsSync(infographicPath);
  const infographicDate = infographicExists ? await getGitModifiedDate(infographicPath) : null;
  images.push({
    type: 'Infographic',
    path: path.relative(process.cwd(), infographicPath),
    exists: infographicExists,
    date: infographicDate,
  });

  // Get Slide image status
  const slideExists = existsSync(slidePath);
  const slideDate = slideExists ? await getGitModifiedDate(slidePath) : null;
  images.push({
    type: 'Slide',
    path: path.relative(process.cwd(), slidePath),
    exists: slideExists,
    date: slideDate,
  });

  // Determine if regeneration is needed
  const allImagePaths = [ogPath, infographicPath, slidePath];
  const { needsRegeneration, reason } = await isQmdNewerThanImages(filePath, allImagePaths);

  return {
    qmdPath: relativePath,
    qmdDate,
    images,
    needsRegeneration,
    reason,
  };
}

/**
 * Format date for display (YYYY-MM-DD or 'N/A')
 */
function formatDate(date: Date | null): string {
  if (!date) return 'N/A';
  return date.toISOString().split('T')[0];
}

/**
 * Print detailed report of all QMD files and their image statuses
 */
async function printDetailedImageReport(bookFiles: string[]): Promise<void> {
  console.log('\n' + '='.repeat(100));
  console.log('DETAILED IMAGE STATUS REPORT');
  console.log('='.repeat(100) + '\n');

  const statuses: FileImageStatus[] = [];

  for (const filePath of bookFiles) {
    const status = await getFileImageStatus(filePath);
    if (status) {
      statuses.push(status);
    }
  }

  // Sort: files needing regeneration first, then alphabetically
  statuses.sort((a, b) => {
    if (a.needsRegeneration !== b.needsRegeneration) {
      return a.needsRegeneration ? -1 : 1;
    }
    return a.qmdPath.localeCompare(b.qmdPath);
  });

  // Count statistics
  const needsRegen = statuses.filter(s => s.needsRegeneration).length;
  const upToDate = statuses.filter(s => !s.needsRegeneration).length;

  console.log(`Total QMD files: ${statuses.length}`);
  console.log(`  Needs regeneration: ${needsRegen}`);
  console.log(`  Up to date: ${upToDate}`);
  console.log('\n' + '-'.repeat(100) + '\n');

  // Print each file status
  for (const status of statuses) {
    const regenFlag = status.needsRegeneration ? '[OUTDATED]' : '[OK]';
    console.log(`${regenFlag} ${status.qmdPath}`);
    console.log(`  QMD Modified: ${formatDate(status.qmdDate)}`);
    console.log(`  Status: ${status.reason}`);
    console.log('  Images:');

    for (const img of status.images) {
      const existsFlag = img.exists ? 'EXISTS' : 'MISSING';
      const dateStr = formatDate(img.date);
      const needsUpdate = status.qmdDate && img.date && status.qmdDate > img.date ? ' <- STALE' : '';
      console.log(`    ${img.type.padEnd(12)} | ${existsFlag.padEnd(7)} | ${dateStr} | ${img.path}${needsUpdate}`);
    }
    console.log('');
  }

  console.log('='.repeat(100));
  console.log('END OF REPORT');
  console.log('='.repeat(100) + '\n');
}

/**
 * Analyze if a file would benefit from an image using Gemini Flash
 */
async function analyzeIfImageNeeded(
  filePath: string,
  cleanedContent: string
): Promise<{ recommend: boolean; reasoning: string; focusContent?: string }> {
  console.log(`  [*] Analyzing with Gemini Flash...`);

  const wordCount = cleanedContent.split(/\s+/).length;

  // Skip very short content
  if (wordCount < 500) {
    return {
      recommend: false,
      reasoning: `Too short (${wordCount} words) - infographics work best for substantial content`,
    };
  }

  const prompt = `Analyze this academic content and determine if a visual infographic would significantly improve reader comprehension.

Content (${wordCount} words):
---
${cleanedContent.substring(0, 6000)} ${wordCount > 1500 ? '... [truncated for analysis]' : ''}
---

Respond with JSON only:
{
  "recommend": true/false,
  "reasoning": "1-2 sentence explanation of why this would/wouldn't benefit from visualization",
  "focusContent": "If recommending, what specific concept or data should the infographic illustrate?"
}

Only recommend if visualization adds substantial educational value beyond the text.
Consider: Does this content have complex relationships, data, processes, or concepts that would be clearer visually?`;

  try {
    const response = await generateGeminiFlashContent(prompt);
    const jsonMatch = response.match(/\{[\s\S]*\}/);
    if (!jsonMatch) {
      console.log(`  [WARN] Could not parse analysis response, assuming no image needed`);
      return { recommend: false, reasoning: 'Analysis parsing failed' };
    }

    const analysis = JSON.parse(jsonMatch[0]);

    console.log(`  Decision: ${analysis.recommend ? '✅ RECOMMEND' : '❌ SKIP'}`);
    console.log(`  Reason: ${analysis.reasoning}`);
    if (analysis.focusContent) {
      console.log(`  Focus: ${analysis.focusContent}`);
    }

    return {
      recommend: analysis.recommend ?? false,
      reasoning: analysis.reasoning ?? 'No reasoning provided',
      focusContent: analysis.focusContent,
    };
  } catch (error) {
    console.error(`  [ERROR] Analysis failed:`, error);
    return { recommend: false, reasoning: 'Analysis error' };
  }
}

/**
 * Check if a file needs image regeneration (pre-scan without generating)
 * Returns info about whether regeneration is needed and why
 * NOTE: Only checks academic style since that's what we generate
 */
async function checkIfNeedsRegeneration(
  filePath: string,
  forceRegenerate: boolean,
  onlyOutdated: boolean
): Promise<{ needsRegeneration: boolean; reason: string }> {
  const fileName = path.basename(filePath, '.qmd');

  // Skip index.qmd files
  if (fileName === 'index') {
    return { needsRegeneration: false, reason: 'index file' };
  }

  // Read frontmatter
  const fileContent = await fs.readFile(filePath, 'utf-8');
  const { data: frontmatter } = matter(fileContent);

  if (!frontmatter.title && !frontmatter.description) {
    return { needsRegeneration: false, reason: 'no title/description' };
  }

  const relativePath = path.relative(process.cwd(), filePath);
  const ogOutputDir = path.join(process.cwd(), 'assets', 'og-images', path.dirname(relativePath));
  const infographicOutputDir = path.join(process.cwd(), 'assets', 'infographics', path.dirname(relativePath));
  const slideOutputDir = path.join(process.cwd(), 'assets', 'slides', path.dirname(relativePath));

  // Only check academic style (that's what we generate)
  const suffix = VisualStyles['bw-academic'].suffix;
  const ogPath = path.join(ogOutputDir, `${fileName}-og${suffix}.jpg`);
  const infographicPath = path.join(infographicOutputDir, `${fileName}-infographic${suffix}.jpg`);
  const slidePath = path.join(slideOutputDir, `${fileName}-slide${suffix}.jpg`);

  const allImagePaths = [ogPath, infographicPath, slidePath];
  const allImagesExist = existsSync(ogPath) && existsSync(infographicPath) && existsSync(slidePath);

  // Force regenerate always needs regeneration
  if (forceRegenerate) {
    return { needsRegeneration: true, reason: 'force' };
  }

  // If images are missing, needs regeneration
  if (!allImagesExist) {
    const missing: string[] = [];
    if (!existsSync(ogPath)) missing.push('OG');
    if (!existsSync(infographicPath)) missing.push('infographic');
    if (!existsSync(slidePath)) missing.push('slide');
    return { needsRegeneration: true, reason: `missing: ${missing.join(', ')}` };
  }

  // If --outdated flag, check git dates
  if (onlyOutdated) {
    const { needsRegeneration, reason } = await isQmdNewerThanImages(filePath, allImagePaths);
    return { needsRegeneration, reason: needsRegeneration ? reason : 'up to date' };
  }

  // All images exist and not forcing/checking outdated
  return { needsRegeneration: false, reason: 'all images exist' };
}

/**
 * Generate OG image, infographic, and slide for a single file
 * @param filePath Path to the QMD file
 * @param forceRegenerate If true, regenerate images even if they already exist
 * @param includeReferenceImages If true, extract images from QMD and pass as reference images to Gemini
 * @param analyzeFirst If true, use Gemini Flash to analyze if image would be helpful before generating
 * @param useAcademicStyle If true, generate in academic style instead of retro
 * @param onlyOutdated If true, only regenerate if QMD is newer than existing images (git dates)
 * @param quietSkips If true, don't log skip messages (used when pre-scan already showed what will be processed)
 */
async function generateImageForFile(
  filePath: string,
  forceRegenerate = false,
  includeReferenceImages = false,
  analyzeFirst = false,
  useAcademicStyle = false,
  onlyOutdated = false,
  quietSkips = false
): Promise<void> {
  const fileName = path.basename(filePath, '.qmd');

  // Skip index.qmd files - they're landing pages, not content chapters
  if (fileName === 'index') {
    if (!quietSkips) console.log(`\n[SKIP] ${filePath} (index files don't need chapter images)`);
    return;
  }

  const relativePath = path.relative(process.cwd(), filePath);
  console.log(`\n[*] ${relativePath}`);

  // Read file frontmatter for metadata
  const fileContent = await fs.readFile(filePath, 'utf-8');
  const { data: frontmatter, content: body } = matter(fileContent);

  // Get cleaned content for LLM (replaces variables, strips markup)
  const cleanedBody = await getCleanedContentForLLM(filePath);

  // Skip if no title or description
  if (!frontmatter.title && !frontmatter.description) {
    if (!quietSkips) console.log(`  [SKIP] No title/description`);
    return;
  }

  // Analyze first if requested
  if (analyzeFirst) {
    const analysis = await analyzeIfImageNeeded(filePath, cleanedBody);
    if (!analysis.recommend) {
      if (!quietSkips) console.log(`  [SKIP] ${analysis.reasoning}`);
      return;
    }
    if (!quietSkips) console.log(`  [PROCEED] Analysis recommends image`);
  }

  // Extract reference images if requested
  let referenceImages: Array<{ data: string; mimeType: string }> = [];
  if (includeReferenceImages) {
    console.log(`  Extracting reference images...`);
    referenceImages = await extractReferenceImages(filePath);
  }

  // Build base image metadata from QMD frontmatter
  // Replace Quarto variables in title and description (e.g., {{< var some_variable >}} -> actual value)
  const siteUrl = await getSiteUrl();
  const resolvedTitle = await replaceVariablesInString(frontmatter.title) || fileName;
  const resolvedDescription = await replaceVariablesInString(frontmatter.description) || resolvedTitle;
  const resolvedKeywords = Array.isArray(frontmatter.tags) ? frontmatter.tags :
                           Array.isArray(frontmatter.keywords) ? frontmatter.keywords :
                           Array.isArray(frontmatter.categories) ? frontmatter.categories : [fileName];
  const baseMetadata: Omit<ImageMetadata, 'category'> = {
    title: resolvedTitle,
    description: resolvedDescription,
    keywords: resolvedKeywords,
    sourceUrl: `${siteUrl}/${relativePath.replace(/\\/g, '/').replace('.qmd', '.html')}`,
  };

  // Helper to create metadata with image type category
  const getMetadataForType = (imageType: 'og-image' | 'infographic' | 'slide'): ImageMetadata => ({
    ...baseMetadata,
    category: imageType,
  });

  const ogOutputDir = path.join(process.cwd(), 'assets', 'og-images', path.dirname(relativePath));
  const infographicOutputDir = path.join(process.cwd(), 'assets', 'infographics', path.dirname(relativePath));
  const slideOutputDir = path.join(process.cwd(), 'assets', 'slides', path.dirname(relativePath));

  // Check which styles already have images
  const styleExistence: Record<string, { og: boolean; infographic: boolean; slide: boolean }> = {};

  for (const [styleName, styleConfig] of Object.entries(VisualStyles)) {
    const suffix = styleConfig.suffix;
    const ogImageFile = path.join(ogOutputDir, `${fileName}-og${suffix}.jpg`);
    const infographicImageFile = path.join(infographicOutputDir, `${fileName}-infographic${suffix}.jpg`);
    const slideImageFile = path.join(slideOutputDir, `${fileName}-slide${suffix}.jpg`);

    styleExistence[styleName] = {
      og: await fs.access(ogImageFile).then(() => true).catch(() => false),
      infographic: await fs.access(infographicImageFile).then(() => true).catch(() => false),
      slide: await fs.access(slideImageFile).then(() => true).catch(() => false),
    };
  }

  // Skip if ALL styles have ALL images (unless forceRegenerate is true)
  const allStylesComplete = Object.values(styleExistence).every(
    style => style.og && style.infographic && style.slide
  );

  if (!forceRegenerate && allStylesComplete) {
    // If --outdated flag is set, check git dates before skipping
    if (onlyOutdated) {
      // Build list of all existing image paths to check
      const existingImagePaths: string[] = [];
      for (const [styleName, styleConfig] of Object.entries(VisualStyles)) {
        const suffix = styleConfig.suffix;
        existingImagePaths.push(
          path.join(ogOutputDir, `${fileName}-og${suffix}.jpg`),
          path.join(infographicOutputDir, `${fileName}-infographic${suffix}.jpg`),
          path.join(slideOutputDir, `${fileName}-slide${suffix}.jpg`)
        );
      }

      const { needsRegeneration, reason } = await isQmdNewerThanImages(filePath, existingImagePaths);

      if (!needsRegeneration) {
        if (!quietSkips) console.log(`[SKIP] ${reason}`);
        return;
      }

      if (!quietSkips) console.log(`[OUTDATED] ${reason} - regenerating images`);
      // Continue to regeneration (don't return)
    } else {
      if (!quietSkips) console.log(`[SKIP] Already has all images in all ${Object.keys(VisualStyles).length} styles`);
      return;
    }
  }

  // Note: Pre-scan already determined this file needs processing, so no need for verbose logging here

  let ogImagePath: string | null = null;
  let infographicImagePath: string | null = null;
  let slideImagePath: string | null = null;

  // Determine which style to use (default to bw-academic only)
  const stylesToGenerate = useAcademicStyle
    ? { 'bw-academic': VisualStyles['bw-academic'] }
    : { 'retro-futuristic': VisualStyles['retro-futuristic'] };

  // Generate images in selected styles
  for (const [styleName, styleConfig] of Object.entries(stylesToGenerate)) {
    const suffix = styleConfig.suffix;

    // Check if this specific style version exists
    const hasThisStyleOg = styleExistence[styleName].og;
    const hasThisStyleInfographic = styleExistence[styleName].infographic;
    const hasThisStyleSlide = styleExistence[styleName].slide;

    // Generate OG image (optimized for social media thumbnails)
    if (!hasThisStyleOg || forceRegenerate || onlyOutdated) {
      console.log(`  Generating OG image...`);
      const ogPrompt = ImagePrompts.og.buildPrompt(cleanedBody, styleConfig.style);

      const ogFiles = await generateAndSaveImages({
        prompt: ogPrompt,
        aspectRatio: ImagePrompts.og.aspectRatio,
        outputDir: ogOutputDir,
        filePrefix: `${fileName}-og${suffix}`,
        format: 'jpg',
        referenceImages,
        metadata: getMetadataForType('og-image'),
      });

      if (ogFiles && ogFiles.length > 0) {
        const imagePath = path.relative(process.cwd(), ogFiles[0]).replace(/\\/g, '/');
        console.log(`  [OK] OG: ${path.basename(imagePath)}`);

        // Default to academic style for frontmatter
        if (styleName === 'academic') {
          ogImagePath = imagePath;
        }
      } else {
        console.log(`  [WARN] OG image generation failed`);
      }
    }

    // Generate infographic (detailed, full-size)
    if (!hasThisStyleInfographic || forceRegenerate || onlyOutdated) {
      console.log(`  Generating infographic...`);
      const infographicPrompt = ImagePrompts.infographic.buildPrompt(cleanedBody, styleConfig.style);

      const infographicFiles = await generateAndSaveImages({
        prompt: infographicPrompt,
        aspectRatio: ImagePrompts.infographic.aspectRatio,
        outputDir: infographicOutputDir,
        filePrefix: `${fileName}-infographic${suffix}`,
        format: 'jpg',
        referenceImages,
        metadata: getMetadataForType('infographic'),
      });

      if (infographicFiles && infographicFiles.length > 0) {
        const imagePath = path.relative(process.cwd(), infographicFiles[0]).replace(/\\/g, '/');
        console.log(`  [OK] Infographic: ${path.basename(imagePath)}`);

        // Use academic style (default)
        if (styleName === 'academic') {
          infographicImagePath = imagePath;
        }
      } else {
        console.log(`  [WARN] Infographic generation failed`);
      }
    }

    // Generate slide (PowerPoint-optimized presentation)
    if (!hasThisStyleSlide || forceRegenerate || onlyOutdated) {
      console.log(`  Generating slide...`);
      console.log(`    Extracting key content for slide...`);
      // Use baseMetadata which has variables already replaced
      const slideContent = await extractSlideContent(cleanedBody, baseMetadata.title, baseMetadata.description);
      const slidePrompt = ImagePrompts.slide.buildPrompt(slideContent, styleConfig.style);

      const slideFiles = await generateAndSaveImages({
        prompt: slidePrompt,
        aspectRatio: ImagePrompts.slide.aspectRatio,
        outputDir: slideOutputDir,
        filePrefix: `${fileName}-slide${suffix}`,
        format: 'jpg',
        referenceImages,
        metadata: getMetadataForType('slide'),
      });

      if (slideFiles && slideFiles.length > 0) {
        const imagePath = path.relative(process.cwd(), slideFiles[0]).replace(/\\/g, '/');
        console.log(`  [OK] Slide: ${path.basename(imagePath)}`);

        // Default to academic style (slides are not typically embedded in QMD)
        if (styleName === 'academic') {
          slideImagePath = imagePath;
        }
      } else {
        console.log(`  [WARN] Slide generation failed`);
      }
    }
  }

  // Update file if we generated any new images
  if (ogImagePath || infographicImagePath || slideImagePath) {
    let updatedBody = body;
    const updatedFrontmatter = { ...frontmatter };

    // Add OG image to frontmatter (defaults to academic style)
    if (ogImagePath) {
      // Only update if not already set or if we should update
      if (!frontmatter.image || forceRegenerate) {
        updatedFrontmatter.image = `/${ogImagePath}`;
      }
    }

    // Insert infographic at top of content (after setup-parameters include)
    if (infographicImagePath) {
      // Check if any infographic reference already exists in the body
      const hasExistingInfographic = body.includes(`${fileName}-infographic-`);

      if (!hasExistingInfographic) {
        const includeDirective = '{{< include /knowledge/includes/setup-parameters.qmd >}}';

        // Generate meaningful alt text from frontmatter (use baseMetadata with variables replaced)
        const altText = baseMetadata.description || baseMetadata.title || 'Chapter infographic';
        const infographicMarkdown = `![${altText}](/${infographicImagePath})`;

        // Find the include directive and insert infographic after it
        if (updatedBody.includes(includeDirective)) {
          updatedBody = updatedBody.replace(
            includeDirective,
            `${includeDirective}\n\n${infographicMarkdown}\n`
          );
        } else {
          // If no include directive, insert at the very beginning
          updatedBody = `${infographicMarkdown}\n\n${updatedBody}`;
        }
      }
    }

    // Write updated file
    const updatedContent = stringifyWithFrontmatter(updatedBody, updatedFrontmatter);
    await fs.writeFile(filePath, updatedContent, 'utf-8');

    console.log(`  [OK] Updated QMD`);
  }
}

/**
 * Generate OG images for book chapters
 */
async function generateBookChapterImages(
  fileFilter?: string,
  includeReferenceImages = false,
  analyzeFirst = false,
  useAcademicStyle = false,
  forceRegenerate = false,
  onlyOutdated = false
): Promise<void> {
  console.log('\n' + '='.repeat(60));
  console.log('Generating OG images for book chapters');
  if (analyzeFirst) {
    console.log('Mode: INTELLIGENT ANALYSIS (Gemini Flash decides)');
  }
  if (useAcademicStyle) {
    console.log('Style: ACADEMIC (black and white scientific)');
  }
  if (onlyOutdated) {
    console.log('Mode: OUTDATED ONLY (regenerate only if QMD is newer than images)');
  }
  console.log('='.repeat(60) + '\n');

  // Get all book files
  console.log('[*] Loading book files...');
  const allBookFiles = await getBookFilesForProcessing();

  // Filter to specific file if provided
  let bookFiles: string[];
  if (fileFilter) {
    const matchingFiles = allBookFiles.filter(f => f.includes(fileFilter));
    if (matchingFiles.length === 0) {
      console.error(`ERROR: No files found matching "${fileFilter}"`);
      console.error('\nAvailable files:');
      allBookFiles.slice(0, 10).forEach(f => console.error(`  - ${f}`));
      if (allBookFiles.length > 10) {
        console.error(`  ... and ${allBookFiles.length - 10} more`);
      }
      process.exit(1);
    }

    // Only process the first matching file when filter is provided
    bookFiles = [matchingFiles[0]];

    if (matchingFiles.length > 1) {
      console.log(`[INFO] Found ${matchingFiles.length} matching files, processing only the first one:`);
      console.log(`  Selected: ${matchingFiles[0]}`);
      console.log(`  Skipped: ${matchingFiles.slice(1).join(', ')}\n`);
    } else {
      console.log(`[OK] Found 1 file matching "${fileFilter}"\n`);
    }
  } else {
    bookFiles = allBookFiles;
    console.log(`[OK] Found ${bookFiles.length} book files\n`);
  }

  // If --outdated flag, always show detailed report first
  if (onlyOutdated) {
    await printDetailedImageReport(bookFiles);
  }

  // Pre-scan to determine which files need regeneration
  console.log('[*] Scanning files to determine which need regeneration...\n');

  const filesToProcess: Array<{ path: string; reason: string }> = [];
  const skippedFiles: Array<{ path: string; reason: string }> = [];

  for (const filePath of bookFiles) {
    const { needsRegeneration, reason } = await checkIfNeedsRegeneration(
      filePath,
      forceRegenerate,
      onlyOutdated
    );

    if (needsRegeneration) {
      filesToProcess.push({ path: filePath, reason });
    } else {
      skippedFiles.push({ path: filePath, reason });
    }
  }

  // Show summary of what will be processed
  if (filesToProcess.length === 0) {
    console.log('[OK] All images are up to date. Nothing to regenerate.\n');
    if (skippedFiles.length > 0 && skippedFiles.length <= 10) {
      console.log('Skipped files:');
      for (const { path: fp, reason } of skippedFiles) {
        console.log(`  - ${path.basename(fp, '.qmd')}: ${reason}`);
      }
    } else if (skippedFiles.length > 10) {
      console.log(`Skipped ${skippedFiles.length} files (all up to date)`);
    }
    return;
  }

  console.log(`[*] Files to regenerate (${filesToProcess.length}):\n`);
  for (const { path: fp, reason } of filesToProcess) {
    const relativePath = path.relative(process.cwd(), fp);
    console.log(`  - ${relativePath} (${reason})`);
  }
  console.log('');

  if (skippedFiles.length > 0) {
    console.log(`[*] Skipping ${skippedFiles.length} files (up to date)\n`);
  }

  console.log('='.repeat(60));
  console.log(`Starting generation of ${filesToProcess.length} files...`);
  console.log('='.repeat(60) + '\n');

  let filesGenerated = 0;
  let filesFailed = 0;

  for (const { path: filePath } of filesToProcess) {
    try {
      // Use quietSkips=true since we already showed the pre-scan summary
      await generateImageForFile(filePath, forceRegenerate, includeReferenceImages, analyzeFirst, useAcademicStyle, onlyOutdated, true);
      filesGenerated++;
    } catch (error) {
      if (error instanceof Error && error.message === 'Image generation failed') {
        filesFailed++;
      } else {
        console.error(`[ERROR] Failed to process ${filePath}:`, error);
        filesFailed++;
      }
      // Continue with next file
    }
  }

  console.log('\n' + '='.repeat(60));
  console.log('Summary:');
  console.log(`  Files to process: ${filesToProcess.length}`);
  console.log(`  Successfully generated: ${filesGenerated}`);
  console.log(`  Failed: ${filesFailed}`);
  console.log(`  Skipped (up to date): ${skippedFiles.length}`);
  console.log('='.repeat(60) + '\n');
}

async function main() {
  console.log('🎨 Book Chapter OG Image Generator');
  console.log('='.repeat(60));

  // Acquire lock file to prevent multiple instances
  await acquireLock();

  // Check for API key
  if (!process.env.GOOGLE_GENERATIVE_AI_API_KEY) {
    console.error('ERROR: GOOGLE_GENERATIVE_AI_API_KEY environment variable is not set');
    console.error('Please set your Google Gemini API key in .env file:');
    console.error('GOOGLE_GENERATIVE_AI_API_KEY=your_api_key_here');
    console.error('Get your API key from: https://aistudio.google.com/app/apikey');
    await releaseLock();
    process.exit(1);
  }

  // Parse command line arguments
  const args = process.argv.slice(2);

  // Support both --file <name> and just <name> as positional argument
  let fileFilter: string | undefined;
  const fileIndex = args.indexOf('--file');
  if (fileIndex !== -1 && args[fileIndex + 1]) {
    // --file <name> syntax
    fileFilter = args[fileIndex + 1];
  } else if (args.length > 0 && !args[0].startsWith('--')) {
    // Positional argument syntax
    fileFilter = args[0];
  }

  // Check for flags
  const includeReferenceImages = args.includes('--with-reference-images');
  const analyzeFirst = args.includes('--analyze-first');
  const useAcademicStyle = args.includes('--academic-style');
  const forceRegenerate = args.includes('--force');
  const onlyOutdated = args.includes('--outdated');

  if (analyzeFirst) {
    console.log('[INFO] Using Gemini Flash to analyze if images would be helpful before generating\n');
  }
  if (useAcademicStyle) {
    console.log('[INFO] Generating in academic style (black and white scientific)\n');
  }
  if (forceRegenerate) {
    console.log('[INFO] FORCE MODE - Regenerating all images even if they already exist\n');
  }
  if (onlyOutdated) {
    console.log('[INFO] OUTDATED MODE - Only regenerating images where QMD is newer (git dates)\n');
  }

  if (fileFilter) {
    // If fileFilter looks like a file path (contains / or ends with .qmd), verify it exists
    if (fileFilter.includes('/') || fileFilter.endsWith('.qmd')) {
      const fullPath = path.join(process.cwd(), fileFilter);
      if (!existsSync(fullPath)) {
        console.error(`\nERROR: File not found: ${fileFilter}`);
        console.error(`Full path checked: ${fullPath}`);
        console.error('\nIf you want to search by keyword, use a simple keyword without path separators.');
        console.error('Example: npx tsx scripts/generate-project-images.ts economics');
        console.error('\nIf you want to specify a file, use the full path:');
        console.error('Example: npx tsx scripts/generate-project-images.ts knowledge/economics/1-pct-treaty-impact.qmd');
        await releaseLock();
        process.exit(1);
      }
    }
    console.log(`\nGenerating image for file matching: "${fileFilter}"\n`);
  }

  if (includeReferenceImages) {
    console.log(`[INFO] Reference images from QMD files will be included in generation context\n`);
  }

  await generateBookChapterImages(fileFilter, includeReferenceImages, analyzeFirst, useAcademicStyle, forceRegenerate, onlyOutdated);
}

// Run the script
main()
  .then(async () => {
    await releaseLock();
    process.exit(0);
  })
  .catch(async (error) => {
    console.error('Fatal error:', error);
    await releaseLock();
    process.exit(1);
  });
