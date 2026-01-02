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
 */

import dotenv from 'dotenv';
import path from 'path';
import fs from 'fs/promises';
import { existsSync, unlinkSync } from 'fs';
import matter from 'gray-matter';
import { generateAndSaveImages } from '../lib/gemini-images.js';
import { generateGeminiFlashContent } from '../lib/llm.js';
import {
  getBookFilesForProcessing,
  stringifyWithFrontmatter,
  getCleanedContentForLLM,
  extractReferenceImages
} from '../lib/file-utils.js';
import { ImagePrompts, VisualStyles, VisualStyleName } from '../lib/image-prompts.js';

// Load environment variables
dotenv.config();

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
 * Generate OG image, infographic, and slide for a single file
 * @param filePath Path to the QMD file
 * @param forceRegenerate If true, regenerate images even if they already exist
 * @param includeReferenceImages If true, extract images from QMD and pass as reference images to Gemini
 * @param analyzeFirst If true, use Gemini Flash to analyze if image would be helpful before generating
 * @param useAcademicStyle If true, generate in academic style instead of retro
 */
async function generateImageForFile(
  filePath: string,
  forceRegenerate = false,
  includeReferenceImages = false,
  analyzeFirst = false,
  useAcademicStyle = false
): Promise<void> {
  console.log(`\n[*] Processing: ${filePath}`);

  const fileName = path.basename(filePath, '.qmd');

  // Read file frontmatter for metadata
  const fileContent = await fs.readFile(filePath, 'utf-8');
  const { data: frontmatter, content: body } = matter(fileContent);

  // Get cleaned content for LLM (replaces variables, strips markup)
  const cleanedBody = await getCleanedContentForLLM(filePath);

  // Skip if no title or description
  if (!frontmatter.title && !frontmatter.description) {
    console.log(`[SKIP] No title or description for prompt generation`);
    return;
  }

  // Analyze first if requested
  if (analyzeFirst) {
    const analysis = await analyzeIfImageNeeded(filePath, cleanedBody);
    if (!analysis.recommend) {
      console.log(`[SKIP] ${analysis.reasoning}`);
      return;
    }
    console.log(`[PROCEED] Generating image based on analysis recommendation`);
  }

  // Extract reference images if requested
  let referenceImages: Array<{ data: string; mimeType: string }> = [];
  if (includeReferenceImages) {
    console.log(`  Extracting reference images from QMD file...`);
    referenceImages = await extractReferenceImages(filePath);
  }

  console.log(`  Title: ${frontmatter.title || '(no title)'}`);
  console.log(`  Description: ${frontmatter.description || '(no description)'}`);

  const relativePath = path.relative(process.cwd(), filePath);
  const ogOutputDir = path.join(process.cwd(), 'assets', 'og-images', path.dirname(relativePath));
  const infographicOutputDir = path.join(process.cwd(), 'assets', 'infographics', path.dirname(relativePath));
  const slideOutputDir = path.join(process.cwd(), 'assets', 'slides', path.dirname(relativePath));

  // Check which styles already have images
  const styleExistence: Record<string, { og: boolean; infographic: boolean; slide: boolean }> = {};

  for (const [styleName, styleConfig] of Object.entries(VisualStyles)) {
    const suffix = styleConfig.suffix;
    const ogImageFile = path.join(ogOutputDir, `${fileName}-og${suffix}.png`);
    const infographicImageFile = path.join(infographicOutputDir, `${fileName}-infographic${suffix}.png`);
    const slideImageFile = path.join(slideOutputDir, `${fileName}-slide${suffix}.png`);

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
    console.log(`[SKIP] Already has all images in all ${Object.keys(VisualStyles).length} styles`);
    return;
  }

  let ogImagePath: string | null = null;
  let infographicImagePath: string | null = null;
  let slideImagePath: string | null = null;

  // Determine which style to use (default to academic only)
  const stylesToGenerate = useAcademicStyle
    ? { academic: VisualStyles.academic }
    : { academic: VisualStyles.academic };

  // Generate images in selected styles
  for (const [styleName, styleConfig] of Object.entries(stylesToGenerate)) {
    const suffix = styleConfig.suffix;
    console.log(`\n  --- ${styleConfig.description.toUpperCase()} STYLE ---`);

    // Check if this specific style version exists
    const hasThisStyleOg = styleExistence[styleName].og;
    const hasThisStyleInfographic = styleExistence[styleName].infographic;
    const hasThisStyleSlide = styleExistence[styleName].slide;

    // Generate OG image (optimized for social media thumbnails)
    if (!hasThisStyleOg || forceRegenerate) {
      console.log(`  Generating OG image (${ImagePrompts.og.description})...`);
      const ogPrompt = ImagePrompts.og.buildPrompt(cleanedBody, styleConfig.style);

      const ogFiles = await generateAndSaveImages({
        prompt: ogPrompt,
        aspectRatio: ImagePrompts.og.aspectRatio,
        outputDir: ogOutputDir,
        filePrefix: `${fileName}-og${suffix}`,
        referenceImages,
      });

      if (ogFiles && ogFiles.length > 0) {
        const imagePath = path.relative(process.cwd(), ogFiles[0]).replace(/\\/g, '/');
        console.log(`  [OK] Generated OG image (${styleName}): ${imagePath}`);

        // Default to academic style for frontmatter
        if (styleName === 'academic') {
          ogImagePath = imagePath;
        }
      } else {
        console.log(`  [WARN] No OG image generated (${styleName})`);
      }
    } else {
      console.log(`  [SKIP] OG image (${styleName}) already exists`);
    }

    // Generate infographic (detailed, full-size)
    if (!hasThisStyleInfographic || forceRegenerate) {
      console.log(`  Generating infographic (${ImagePrompts.infographic.description})...`);
      const infographicPrompt = ImagePrompts.infographic.buildPrompt(cleanedBody, styleConfig.style);

      const infographicFiles = await generateAndSaveImages({
        prompt: infographicPrompt,
        aspectRatio: ImagePrompts.infographic.aspectRatio,
        outputDir: infographicOutputDir,
        filePrefix: `${fileName}-infographic${suffix}`,
        referenceImages,
      });

      if (infographicFiles && infographicFiles.length > 0) {
        const imagePath = path.relative(process.cwd(), infographicFiles[0]).replace(/\\/g, '/');
        console.log(`  [OK] Generated infographic (${styleName}): ${imagePath}`);

        // Use academic style (default)
        if (styleName === 'academic') {
          infographicImagePath = imagePath;
        }
      } else {
        console.log(`  [WARN] No infographic generated (${styleName})`);
      }
    } else {
      console.log(`  [SKIP] Infographic (${styleName}) already exists`);
    }

    // Generate slide (PowerPoint-optimized presentation)
    if (!hasThisStyleSlide || forceRegenerate) {
      console.log(`  Generating slide (${ImagePrompts.slide.description})...`);
      const slidePrompt = ImagePrompts.slide.buildPrompt(cleanedBody, styleConfig.style);

      const slideFiles = await generateAndSaveImages({
        prompt: slidePrompt,
        aspectRatio: ImagePrompts.slide.aspectRatio,
        outputDir: slideOutputDir,
        filePrefix: `${fileName}-slide${suffix}`,
        referenceImages,
      });

      if (slideFiles && slideFiles.length > 0) {
        const imagePath = path.relative(process.cwd(), slideFiles[0]).replace(/\\/g, '/');
        console.log(`  [OK] Generated slide (${styleName}): ${imagePath}`);

        // Default to academic style (slides are not typically embedded in QMD)
        if (styleName === 'academic') {
          slideImagePath = imagePath;
        }
      } else {
        console.log(`  [WARN] No slide generated (${styleName})`);
      }
    } else {
      console.log(`  [SKIP] Slide (${styleName}) already exists`);
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

        // Generate meaningful alt text from frontmatter
        const altText = frontmatter.description || frontmatter.title || 'Chapter infographic';
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

    console.log(`  [OK] Updated ${filePath}`);
  } else {
    console.log(`  [SKIP] No new images to add`);
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
  forceRegenerate = false
): Promise<void> {
  console.log('\n' + '='.repeat(60));
  console.log('Generating OG images for book chapters');
  if (analyzeFirst) {
    console.log('Mode: INTELLIGENT ANALYSIS (Gemini Flash decides)');
  }
  if (useAcademicStyle) {
    console.log('Style: ACADEMIC (black and white scientific)');
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

  let filesProcessed = 0;
  const filesSkipped = 0;
  let filesGenerated = 0;
  let filesFailed = 0;

  for (const filePath of bookFiles) {
    try {
      filesProcessed++;
      await generateImageForFile(filePath, forceRegenerate, includeReferenceImages, analyzeFirst, useAcademicStyle);
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
  console.log(`  Files processed: ${filesProcessed}`);
  console.log(`  Images generated: ${filesGenerated}`);
  console.log(`  Files skipped: ${filesSkipped}`);
  console.log(`  Files failed: ${filesFailed}`);
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

  if (analyzeFirst) {
    console.log('[INFO] Using Gemini Flash to analyze if images would be helpful before generating\n');
  }
  if (useAcademicStyle) {
    console.log('[INFO] Generating in academic style (black and white scientific)\n');
  }
  if (forceRegenerate) {
    console.log('[INFO] FORCE MODE - Regenerating all images even if they already exist\n');
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
        console.error('Example: npx tsx scripts/generate-project-images.ts knowledge/economics/economics.qmd');
        await releaseLock();
        process.exit(1);
      }
    }
    console.log(`\nGenerating image for file matching: "${fileFilter}"\n`);
  }

  if (includeReferenceImages) {
    console.log(`[INFO] Reference images from QMD files will be included in generation context\n`);
  }

  await generateBookChapterImages(fileFilter, includeReferenceImages, analyzeFirst, useAcademicStyle, forceRegenerate);
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
