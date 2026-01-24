/**
 * Generate images for specific sections within chapters using intelligent analysis
 *
 * Gives Gemini the entire file and asks it to identify sections that would
 * benefit from visual aids (diagrams, charts, infographics, flowcharts).
 *
 * Defaults to bw-academic style (black & white scientific) for professional publications.
 * Default aspect ratio is 1:1 (square) for consistency with manual generations.
 *
 * Usage:
 *   npx tsx scripts/images/generate-section-images.ts <file.qmd> [options]
 *   npx tsx scripts/images/generate-section-images.ts --all [options]
 *
 * Options:
 *   --all                 Process all book QMD files (skips files with existing section images)
 *   --retro-futuristic    Generate in retro-futuristic style (default: bw-academic)
 *   --aspect <ratio>      Aspect ratio: 1:1, 3:4, 9:16, 16:9 (default: 1:1)
 *   --dry-run             Show recommendations without generating images
 *   --force               Delete existing section images and regenerate all
 *
 * Examples:
 *   npx tsx scripts/images/generate-section-images.ts knowledge/appendix/invisible-graveyard.qmd
 *   npx tsx scripts/images/generate-section-images.ts --all
 *   npx tsx scripts/images/generate-section-images.ts --all --dry-run
 *   npx tsx scripts/images/generate-section-images.ts --all --force
 *   npx tsx scripts/images/generate-section-images.ts knowledge/appendix/invisible-graveyard.qmd --retro-futuristic
 *   npx tsx scripts/images/generate-section-images.ts knowledge/appendix/invisible-graveyard.qmd --aspect 3:4
 */

import dotenv from 'dotenv';
import path from 'path';
import fs from 'fs/promises';
import { existsSync, readdirSync, unlinkSync } from 'fs';
import { generateGeminiProContent } from '../lib/llm.js';
import { generateAndSaveImages } from '../lib/gemini-images.js';
import { getCleanedContentForLLM, getBookFilesForProcessing } from '../lib/file-utils.js';
import { VisualStyles } from '../lib/image-prompts.js';

dotenv.config();

interface ImageRecommendation {
  sectionHeading: string;  // The actual markdown heading (e.g., "## Problem Statement")
  anchorText: string;      // Last few words of paragraph before image (for finding position)
  placementHint: string;   // Description like "after the 4-point list"
  sectionTitle: string;
  imageType: 'diagram' | 'chart' | 'infographic' | 'flowchart';
  verbatimContent: string; // Exact text, numbers, and quotes copied directly from the section
  caption: string;         // Natural, human-readable caption for alt text
  reasoning: string;
}

interface AnalysisResponse {
  recommendations: ImageRecommendation[];
  totalRecommendations: number;
  reasoning: string;
}

/**
 * Convert section title to kebab-case for use in filenames
 */
function toKebabCase(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')  // Replace non-alphanumeric with hyphens
    .replace(/^-+|-+$/g, '');      // Remove leading/trailing hyphens
}

/**
 * Find intelligent placement location based on section heading and anchor text
 * Uses cleaned content for anchor matching (LLM analyzed cleaned content with resolved variables)
 * but returns line number for raw content insertion.
 * Avoids placing before lists, after colons, or before headers.
 */
function findSmartPlacement(
  rawLines: string[],
  cleanedLines: string[],
  sectionHeading: string,
  anchorText: string,
  placementHint: string
): number | null {
  // Find section heading in BOTH files (headings don't contain variables)
  const rawHeadingLine = rawLines.findIndex(line => line.trim() === sectionHeading.trim());
  const cleanedHeadingLine = cleanedLines.findIndex(line => line.trim() === sectionHeading.trim());

  if (rawHeadingLine === -1) {
    console.log(`  [WARN] Could not find section heading in raw file: "${sectionHeading}"`);
    return null;
  }

  if (cleanedHeadingLine === -1) {
    console.log(`  [WARN] Could not find section heading in cleaned content: "${sectionHeading}"`);
    return null;
  }

  // Search for anchor text in CLEANED content (where variables are resolved)
  let cleanedAnchorLine = -1;
  const normalizedAnchor = anchorText.toLowerCase().trim();

  for (let i = cleanedHeadingLine + 1; i < cleanedLines.length; i++) {
    const normalizedLine = cleanedLines[i].toLowerCase().trim();
    if (normalizedLine.includes(normalizedAnchor)) {
      cleanedAnchorLine = i;
      break;
    }
  }

  if (cleanedAnchorLine === -1) {
    console.log(`  [WARN] Could not find anchor text: "${anchorText}" in section "${sectionHeading}"`);
    console.log(`  [INFO] Placement hint: ${placementHint}`);
    return null;
  }

  // Calculate offset from heading to anchor in cleaned content
  const offsetFromHeading = cleanedAnchorLine - cleanedHeadingLine;

  // Apply offset to raw content to get approximate anchor position
  const rawAnchorLine = rawHeadingLine + offsetFromHeading;

  console.log(`  [DEBUG] Heading: raw=${rawHeadingLine}, cleaned=${cleanedHeadingLine}`);
  console.log(`  [DEBUG] Anchor offset: ${offsetFromHeading}, raw anchor line: ${rawAnchorLine}`);

  // Find next safe insertion point after the calculated anchor position in RAW content
  for (let i = rawAnchorLine + 1; i < rawLines.length; i++) {
    const line = rawLines[i].trim();
    const nextLine = i + 1 < rawLines.length ? rawLines[i + 1].trim() : '';

    // Stop at next section heading
    if (line.startsWith('#')) {
      console.log(`  [INFO] Reached next section at line ${i}, placing before it`);
      return i;
    }

    // Skip blank lines
    if (line === '') {
      continue;
    }

    // Check if this is a safe insertion point
    const isList = /^(\d+\.|[-*+])\s/.test(line) || /^(\d+\.|[-*+])\s/.test(nextLine);
    const isHeader = line.startsWith('#') || nextLine.startsWith('#');
    const endsWithColon = line.endsWith(':');
    const isCodeBlock = line.startsWith('```') || line.startsWith('~~~');

    // Skip unsafe locations
    if (isList || isHeader || endsWithColon || isCodeBlock) {
      continue;
    }

    // Found a safe spot after a complete paragraph
    if (line.endsWith('.') || line.endsWith('"') || line.endsWith(')')) {
      // Make sure next line isn't a list or header
      if (!isList && !isHeader) {
        return i + 1; // Insert after this complete paragraph
      }
    }
  }

  // Fallback: place right after calculated anchor line
  console.log(`  [INFO] Using fallback placement after anchor line ${rawAnchorLine}`);
  return rawAnchorLine + 1;
}

/**
 * Analyze entire file and get section-specific image recommendations
 */
async function analyzeFileForSectionImages(
  filePath: string,
  cleanedContent: string
): Promise<AnalysisResponse> {
  console.log(`\n[*] Analyzing file with Gemini Flash...`);
  console.log(`  File: ${filePath}`);

  const prompt = `Analyze this document and identify sections needing visual aids (diagrams, charts, infographics, flowcharts). Be selective—only recommend where visualization significantly enhances understanding.

FILE CONTENT:
---
${cleanedContent}
---

Respond with JSON:
{
  "recommendations": [
    {
      "sectionHeading": "<exact markdown heading: '## Problem Statement'>",
      "anchorText": "<last 5-10 words before image placement>",
      "placementHint": "<e.g., 'after the 4-point list'>",
      "sectionTitle": "<section name for filename>",
      "imageType": "diagram" | "chart" | "infographic" | "flowchart",
      "verbatimContent": "<COPY EXACT TEXT from the section - see VERBATIM CONTENT FORMAT below>",
      "caption": "<1-2 sentence description, NO figure numbers like 'Figure 1:'>",
      "reasoning": "<why this image is necessary>"
    }
  ],
  "totalRecommendations": <number>,
  "reasoning": "<overall assessment>"
}

RECOMMEND ONLY IF:
- Complex quantitative comparisons hard to grasp as text
- Multi-step processes (4+ steps) or interconnected relationships (5+ entities)
- Substantial context (200+ words) with data visualization value

PLACEMENT:
- Provide sectionHeading (exact markdown), anchorText (last words before placement), placementHint
- Script finds location by: locating heading → finding anchor → skipping lists/headers/code → placing after complete paragraphs
- Examples: "after the 4-point explanation", "after ROI calculation", "after defining key terms"

VERBATIM CONTENT FORMAT:
Extract and copy the EXACT text from the section that should appear in the figure. Do NOT paraphrase, summarize, or rewrite. Copy-paste directly:
- Key statistics and numbers exactly as written
- Labels, titles, and category names exactly as they appear
- Quoted phrases that should appear in the image
- List items or steps exactly as written

GOOD verbatimContent examples:
- "Global Military Spending: $2.72 Trillion | Disease Cure Funding: $67.5 Billion | Government Clinical Trials: $4.5 Billion | 604:1 ratio"
- "Step 1: Pharma Industry Job | Step 2: FDA Regulator | Step 3: Return to Industry | 400% Salary Raise"
- "NIH RECOVER: $1.665 billion, 4 years, 0 trials completed | UK RECOVERY: $20 million, 6 months, 1 million lives saved"

BAD verbatimContent (paraphrased):
- "A comparison showing military spending vastly exceeds healthcare" (this is a summary, not the actual text)
- "The revolving door between industry and government" (this is a description, not the content)

CAPTION FORMAT:
- Natural descriptions: "Comparison of traditional trial costs ($41K/patient) vs. pragmatic trials ($500/patient)."
- NO figure numbers: ❌ "Figure 1:", "Fig. 1:"

Be selective. Quality over quantity.`;

  try {
    const response = await generateGeminiProContent(prompt);
    const jsonMatch = response.match(/\{[\s\S]*\}/);

    if (!jsonMatch) {
      console.log(`[WARN] Could not parse analysis response`);
      return {
        recommendations: [],
        totalRecommendations: 0,
        reasoning: 'Analysis parsing failed'
      };
    }

    const analysis = JSON.parse(jsonMatch[0]) as AnalysisResponse;

    console.log(`\n[ANALYSIS RESULTS]`);
    console.log(`  Total recommendations: ${analysis.totalRecommendations}`);
    console.log(`  Overall reasoning: ${analysis.reasoning}`);

    if (analysis.recommendations.length > 0) {
      console.log(`\n[RECOMMENDED IMAGES]`);
      analysis.recommendations.forEach((rec, idx) => {
        console.log(`\n  ${idx + 1}. Section "${rec.sectionHeading}": ${rec.sectionTitle}`);
        console.log(`     Type: ${rec.imageType}`);
        console.log(`     Placement: ${rec.placementHint}`);
        console.log(`     Anchor: "${rec.anchorText}"`);
        console.log(`     Caption: ${rec.caption}`);
        console.log(`     Why: ${rec.reasoning}`);
        console.log(`     --- Verbatim Content ---`);
        console.log(`     ${rec.verbatimContent.replace(/\n/g, '\n     ')}`);
        console.log(`     ${'─'.repeat(50)}`);
      });
    } else {
      console.log(`\n  No images recommended - document is clear without visual aids`);
    }

    return analysis;
  } catch (error) {
    console.error(`[ERROR] Analysis failed:`, error);
    return {
      recommendations: [],
      totalRecommendations: 0,
      reasoning: 'Analysis error'
    };
  }
}

/**
 * Generate and insert section images based on recommendations
 */
async function generateSectionImages(
  filePath: string,
  recommendations: ImageRecommendation[],
  useAcademicStyle: boolean,
  cleanedContent: string,
  aspectRatio: '1:1' | '3:4' | '9:16' | '16:9' = '1:1'
): Promise<void> {
  if (recommendations.length === 0) {
    console.log(`\n[SKIP] No images to generate`);
    return;
  }

  console.log(`\n[*] Generating ${recommendations.length} section images...`);

  const fileName = path.basename(filePath, '.qmd');
  // Output to assets/images/<qmd-basename>/ for consistency with SKILL.md convention
  const outputDir = path.join(process.cwd(), 'assets', 'images', fileName);

  // Read file content (raw, for insertion)
  const fileContent = await fs.readFile(filePath, 'utf-8');
  const rawLines = fileContent.split('\n');

  // Split cleaned content for anchor text matching (LLM analyzed this version with resolved variables)
  const cleanedLines = cleanedContent.split('\n');

  // Generate images for each recommendation
  const generatedImages: Array<{ lineNumber: number; imagePath: string; caption: string }> = [];

  for (let i = 0; i < recommendations.length; i++) {
    const rec = recommendations[i];
    console.log(`\n  [${i + 1}/${recommendations.length}] Generating: ${rec.sectionTitle}`);

    // Find smart placement: search in cleaned content (for anchor matching), return raw line number
    const placementLine = findSmartPlacement(rawLines, cleanedLines, rec.sectionHeading, rec.anchorText, rec.placementHint);

    if (placementLine === null) {
      console.log(`  [SKIP] Could not find safe placement location`);
      continue;
    }

    console.log(`  [INFO] Placement found at line ${placementLine}: ${rec.placementHint}`);

    const style = useAcademicStyle ? VisualStyles['bw-academic'] : VisualStyles['retro-futuristic'];
    const suffix = style.suffix;

    // Pass the verbatim content directly - let the image model figure out the best visualization
    const imagePrompt = `${style.style}

Create a ${rec.imageType} visualizing this information:

${rec.verbatimContent}`;

    try {
      // Use the aspect ratio passed from CLI (default: 1:1 for consistency with manual generations)

      // Generate descriptive filename from section title
      const sectionSlug = toKebabCase(rec.sectionTitle);

      // Log prompts to console and file for debugging
      console.log(`\n  --- VERBATIM CONTENT (from analysis) ---`);
      console.log(`  ${rec.verbatimContent}`);
      console.log(`\n  --- FINAL PROMPT SENT TO GEMINI ---`);
      console.log(`  ${imagePrompt.replace(/\n/g, '\n  ')}`);
      console.log(`  ${'─'.repeat(60)}`);

      const logsDir = path.join(process.cwd(), 'logs');
      await fs.mkdir(logsDir, { recursive: true });
      const logFile = path.join(logsDir, 'image-prompts.log');
      const logEntry = `
${'='.repeat(80)}
[${new Date().toISOString()}] Image ${i + 1}/${recommendations.length}: ${rec.sectionTitle}
${'='.repeat(80)}
Section Heading: ${rec.sectionHeading}
Image Type: ${rec.imageType}
Placement: ${rec.placementHint}
Anchor Text: ${rec.anchorText}

--- VERBATIM CONTENT (from analysis) ---
${rec.verbatimContent}

--- FINAL PROMPT SENT TO GEMINI ---
${imagePrompt}
${'='.repeat(80)}

`;
      await fs.appendFile(logFile, logEntry, 'utf-8');

      const imageFiles = await generateAndSaveImages({
        prompt: imagePrompt,
        aspectRatio,
        outputDir,
        filePrefix: `${fileName}-section-${sectionSlug}${suffix}`,
        referenceImages: [],
        metadata: {
          title: rec.caption,
          description: rec.verbatimContent,
          keywords: [rec.imageType, rec.sectionTitle, fileName, 'section-image'],
        },
      });

      if (imageFiles && imageFiles.length > 0) {
        const absolutePath = imageFiles[0];
        const relativePath = path.relative(process.cwd(), absolutePath).replace(/\\/g, '/');

        console.log(`  [OK] Generated: ${relativePath}`);
        generatedImages.push({
          lineNumber: placementLine,
          imagePath: `/${relativePath}`,
          caption: rec.caption
        });
      } else {
        console.log(`  [WARN] No image generated for: ${rec.sectionTitle}`);
      }
    } catch (error) {
      console.error(`  [ERROR] Failed to generate image for ${rec.sectionTitle}:`, error);
    }
  }

  // Insert images into file (in reverse order to preserve line numbers)
  if (generatedImages.length > 0) {
    console.log(`\n[*] Inserting ${generatedImages.length} images into file...`);

    // Sort by line number descending (to insert from bottom up)
    generatedImages.sort((a, b) => b.lineNumber - a.lineNumber);

    for (const { lineNumber, imagePath, caption } of generatedImages) {
      const imageMarkdown = `\n![${caption}](${imagePath})\n`;
      rawLines.splice(lineNumber, 0, imageMarkdown);
      console.log(`  Inserted image at line ${lineNumber}`);
    }

    // Write updated file
    await fs.writeFile(filePath, rawLines.join('\n'), 'utf-8');
    console.log(`\n[OK] Updated ${filePath} with ${generatedImages.length} images`);
  }
}

/**
 * Check if a file already has section images
 * Returns the count of existing section images
 */
function countExistingSectionImages(filePath: string): number {
  const fileName = path.basename(filePath, '.qmd');
  const outputDir = path.join(process.cwd(), 'assets', 'images', fileName);

  if (!existsSync(outputDir)) {
    return 0;
  }

  try {
    const { readdirSync } = require('fs');
    const files = readdirSync(outputDir);
    return files.filter((f: string) => f.startsWith(`${fileName}-section-`) && (f.endsWith('.png') || f.endsWith('.jpg'))).length;
  } catch {
    return 0;
  }
}

/**
 * Process a single file for section image generation
 */
async function processFile(
  filePath: string,
  options: {
    dryRun: boolean;
    force: boolean;
    useAcademicStyle: boolean;
    aspectRatio: '1:1' | '3:4' | '9:16' | '16:9';
  }
): Promise<{ generated: number; skipped: boolean; error?: string }> {
  const { dryRun, force, useAcademicStyle, aspectRatio } = options;
  const fileName = path.basename(filePath, '.qmd');

  // Force mode: clean up existing section images and references
  if (force && !dryRun) {
    const outputDir = path.join(process.cwd(), 'assets', 'images', fileName);

    // Delete existing section images
    if (existsSync(outputDir)) {
      const files = readdirSync(outputDir);
      const sectionImages = files.filter((f: string) => f.startsWith(`${fileName}-section-`) && (f.endsWith('.png') || f.endsWith('.jpg')));

      if (sectionImages.length > 0) {
        console.log(`\n[FORCE] Deleting ${sectionImages.length} existing section images...`);
        for (const img of sectionImages) {
          unlinkSync(path.join(outputDir, img));
          console.log(`  Deleted: ${img}`);
        }
      }
    }

    // Remove existing section image references from file
    const fileContent = await fs.readFile(filePath, 'utf-8');
    const sectionImagePattern = /\n+!\[.*?\]\(\/assets\/(?:section-images|images)\/.*?\)\n+/g;
    let fileWithoutImages = fileContent.replace(sectionImagePattern, '\n\n');
    fileWithoutImages = fileWithoutImages.replace(/\n{3,}/g, '\n\n');

    if (fileWithoutImages !== fileContent) {
      await fs.writeFile(filePath, fileWithoutImages, 'utf-8');
      const removedCount = (fileContent.match(sectionImagePattern) || []).length;
      console.log(`[FORCE] Removed ${removedCount} section image references from file\n`);
    }
  }

  // Get cleaned content for analysis
  const cleanedContent = await getCleanedContentForLLM(filePath);

  // Analyze file
  const analysis = await analyzeFileForSectionImages(filePath, cleanedContent);

  if (dryRun) {
    return { generated: analysis.recommendations.length, skipped: false };
  }

  // Generate and insert images
  await generateSectionImages(filePath, analysis.recommendations, useAcademicStyle, cleanedContent, aspectRatio);

  return { generated: analysis.recommendations.length, skipped: false };
}

async function main() {
  const args = process.argv.slice(2);
  const processAll = args.includes('--all');

  // Show help if no arguments and not --all mode
  if (args.length === 0 || (args[0].startsWith('--') && !processAll)) {
    console.error('Usage: npx tsx scripts/images/generate-section-images.ts <file.qmd> [options]');
    console.error('       npx tsx scripts/images/generate-section-images.ts --all [options]');
    console.error('');
    console.error('Options:');
    console.error('  --all                 Process all book QMD files (skips files with existing section images)');
    console.error('  --retro-futuristic    Use retro-futuristic style (default: bw-academic)');
    console.error('  --aspect <ratio>      Aspect ratio: 1:1, 3:4, 9:16, 16:9 (default: 1:1)');
    console.error('  --dry-run             Show recommendations without generating images');
    console.error('  --force               Delete existing section images and regenerate all');
    console.error('');
    console.error('Available styles:');
    console.error('  bw-academic (default)  Black and white scientific illustration');
    console.error('  retro-futuristic       Fun retro futuristic style with large text');
    process.exit(1);
  }

  const dryRun = args.includes('--dry-run');
  const force = args.includes('--force');
  const useAcademicStyle = !args.includes('--retro-futuristic');

  // Parse --aspect argument
  let aspectRatio: '1:1' | '3:4' | '9:16' | '16:9' = '1:1';
  const aspectIndex = args.indexOf('--aspect');
  if (aspectIndex !== -1 && args[aspectIndex + 1]) {
    const ratioArg = args[aspectIndex + 1];
    if (['1:1', '3:4', '9:16', '16:9'].includes(ratioArg)) {
      aspectRatio = ratioArg as typeof aspectRatio;
    } else {
      console.error(`[ERROR] Invalid aspect ratio: ${ratioArg}`);
      console.error('Valid options: 1:1, 3:4, 9:16, 16:9');
      process.exit(1);
    }
  }

  console.log('📊 Section-Specific Image Generator');
  console.log('='.repeat(80));
  console.log(`[INFO] Style: ${useAcademicStyle ? 'bw-academic (black and white scientific)' : 'retro-futuristic'}`);
  console.log(`[INFO] Aspect ratio: ${aspectRatio}`);
  if (dryRun) console.log('[INFO] DRY RUN - will show recommendations without generating');
  if (force) console.log('[INFO] FORCE MODE - will delete existing images and regenerate all');

  const options = { dryRun, force, useAcademicStyle, aspectRatio };

  // Batch mode: process all book files
  if (processAll) {
    console.log('\n[*] Scanning all book files...');
    const allFiles = await getBookFilesForProcessing();

    // Filter out index files and files without meaningful content
    const qmdFiles = allFiles.filter(f => !f.endsWith('index.qmd'));
    console.log(`[OK] Found ${qmdFiles.length} QMD files\n`);

    // Pre-scan to determine which files need processing
    const filesToProcess: Array<{ path: string; existingCount: number }> = [];
    const skippedFiles: Array<{ path: string; existingCount: number }> = [];

    for (const filePath of qmdFiles) {
      const existingCount = countExistingSectionImages(filePath);

      if (force || existingCount === 0) {
        filesToProcess.push({ path: filePath, existingCount });
      } else {
        skippedFiles.push({ path: filePath, existingCount });
      }
    }

    // Show summary
    console.log(`[*] Files to process: ${filesToProcess.length}`);
    console.log(`[*] Files skipped (have section images): ${skippedFiles.length}\n`);

    if (skippedFiles.length > 0 && skippedFiles.length <= 20) {
      console.log('Skipped files:');
      for (const { path: fp, existingCount } of skippedFiles) {
        const relativePath = path.relative(process.cwd(), fp);
        console.log(`  - ${relativePath} (${existingCount} section images)`);
      }
      console.log('');
    }

    if (filesToProcess.length === 0) {
      console.log('[OK] All files already have section images. Use --force to regenerate.\n');
      process.exit(0);
    }

    console.log('Files to process:');
    for (const { path: fp, existingCount } of filesToProcess) {
      const relativePath = path.relative(process.cwd(), fp);
      const status = existingCount > 0 ? `(${existingCount} existing, will regenerate)` : '(no section images)';
      console.log(`  - ${relativePath} ${status}`);
    }
    console.log('\n' + '='.repeat(80));

    // Process each file
    let totalGenerated = 0;
    let filesProcessed = 0;
    let filesFailed = 0;

    for (let i = 0; i < filesToProcess.length; i++) {
      const { path: filePath } = filesToProcess[i];
      const relativePath = path.relative(process.cwd(), filePath);

      console.log(`\n[${ i + 1}/${filesToProcess.length}] Processing: ${relativePath}`);
      console.log('-'.repeat(80));

      try {
        const result = await processFile(filePath, options);
        totalGenerated += result.generated;
        filesProcessed++;

        if (dryRun) {
          console.log(`[DRY RUN] Would generate ${result.generated} images`);
        }
      } catch (error) {
        console.error(`[ERROR] Failed to process ${relativePath}:`, error);
        filesFailed++;
      }
    }

    // Final summary
    console.log('\n' + '='.repeat(80));
    console.log('BATCH PROCESSING COMPLETE');
    console.log('='.repeat(80));
    console.log(`  Files processed: ${filesProcessed}`);
    console.log(`  Files failed: ${filesFailed}`);
    console.log(`  Files skipped: ${skippedFiles.length}`);
    console.log(`  Total images ${dryRun ? 'recommended' : 'generated'}: ${totalGenerated}`);
    console.log('='.repeat(80));

    if (dryRun) {
      console.log('\n[DRY RUN COMPLETE] Run without --dry-run to generate images');
    }
  } else {
    // Single file mode
    const filePath = args.find(arg => !arg.startsWith('--') && arg !== aspectRatio);

    if (!filePath) {
      console.error('[ERROR] No file specified');
      process.exit(1);
    }

    if (!existsSync(filePath)) {
      console.error(`[ERROR] File not found: ${filePath}`);
      process.exit(1);
    }

    await processFile(filePath, options);

    if (dryRun) {
      console.log('\n[DRY RUN COMPLETE] Run without --dry-run to generate images');
    } else {
      console.log('\n' + '='.repeat(80));
      console.log('✓ Complete');
      console.log('='.repeat(80));
    }
  }
}

main().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
