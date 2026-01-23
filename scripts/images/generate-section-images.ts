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
 *
 * Options:
 *   --retro-futuristic    Generate in retro-futuristic style (default: bw-academic)
 *   --aspect <ratio>      Aspect ratio: 1:1, 3:4, 9:16, 16:9 (default: 1:1)
 *   --dry-run             Show recommendations without generating images
 *   --force               Delete existing section images and regenerate all
 *
 * Examples:
 *   npx tsx scripts/images/generate-section-images.ts knowledge/appendix/invisible-graveyard.qmd
 *   npx tsx scripts/images/generate-section-images.ts knowledge/appendix/invisible-graveyard.qmd --retro-futuristic
 *   npx tsx scripts/images/generate-section-images.ts knowledge/appendix/invisible-graveyard.qmd --aspect 3:4
 *   npx tsx scripts/images/generate-section-images.ts knowledge/appendix/invisible-graveyard.qmd --dry-run
 *   npx tsx scripts/images/generate-section-images.ts knowledge/appendix/invisible-graveyard.qmd --force
 */

import dotenv from 'dotenv';
import path from 'path';
import fs from 'fs/promises';
import { existsSync } from 'fs';
import { generateGeminiProContent } from '../lib/llm.js';
import { generateAndSaveImages } from '../lib/gemini-images.js';
import { getCleanedContentForLLM } from '../lib/file-utils.js';
import { VisualStyles } from '../lib/image-prompts.js';

dotenv.config();

interface ImageRecommendation {
  sectionHeading: string;  // The actual markdown heading (e.g., "## Problem Statement")
  anchorText: string;      // Last few words of paragraph before image (for finding position)
  placementHint: string;   // Description like "after the 4-point list"
  sectionTitle: string;
  contentExcerpt: string;
  imageType: 'diagram' | 'chart' | 'infographic' | 'flowchart';
  visualizationGoal: string;  // Detailed prompt for image generation
  caption: string;            // Natural, human-readable caption for alt text
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
 * Avoids placing before lists, after colons, or before headers
 */
function findSmartPlacement(
  lines: string[],
  sectionHeading: string,
  anchorText: string,
  placementHint: string
): number | null {
  // Find section heading
  const headingLine = lines.findIndex(line => line.trim() === sectionHeading.trim());

  if (headingLine === -1) {
    console.log(`  [WARN] Could not find section heading: "${sectionHeading}"`);
    return null;
  }

  // Search for anchor text after the heading
  let anchorLine = -1;
  const normalizedAnchor = anchorText.toLowerCase().trim();

  for (let i = headingLine + 1; i < lines.length; i++) {
    const normalizedLine = lines[i].toLowerCase().trim();
    if (normalizedLine.includes(normalizedAnchor)) {
      anchorLine = i;
      break;
    }
  }

  if (anchorLine === -1) {
    console.log(`  [WARN] Could not find anchor text: "${anchorText}" in section "${sectionHeading}"`);
    console.log(`  [INFO] Placement hint: ${placementHint}`);
    return null;
  }

  // Find next safe insertion point after anchor
  for (let i = anchorLine + 1; i < lines.length; i++) {
    const line = lines[i].trim();
    const nextLine = i + 1 < lines.length ? lines[i + 1].trim() : '';

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

  // Fallback: place right after anchor line
  console.log(`  [INFO] Using fallback placement after anchor line ${anchorLine}`);
  return anchorLine + 1;
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
      "contentExcerpt": "<200-500 word excerpt to visualize>",
      "imageType": "diagram" | "chart" | "infographic" | "flowchart",
      "visualizationGoal": "<detailed technical prompt for image generation>",
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
        console.log(`     Goal: ${rec.visualizationGoal}`);
        console.log(`     Why: ${rec.reasoning}`);
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
  const lines = fileContent.split('\n');

  // Also split cleaned content (for anchor text matching, since LLM analyzed cleaned content)
  const cleanedLines = cleanedContent.split('\n');

  // Generate images for each recommendation
  const generatedImages: Array<{ lineNumber: number; imagePath: string; caption: string }> = [];

  for (let i = 0; i < recommendations.length; i++) {
    const rec = recommendations[i];
    console.log(`\n  [${i + 1}/${recommendations.length}] Generating: ${rec.sectionTitle}`);

    // Find smart placement using section heading and anchor text (search in cleaned content since that's what LLM analyzed)
    const placementLine = findSmartPlacement(cleanedLines, rec.sectionHeading, rec.anchorText, rec.placementHint);

    if (placementLine === null) {
      console.log(`  [SKIP] Could not find safe placement location`);
      continue;
    }

    console.log(`  [INFO] Placement found at line ${placementLine}: ${rec.placementHint}`);

    const style = useAcademicStyle ? VisualStyles['bw-academic'] : VisualStyles['retro-futuristic'];
    const suffix = style.suffix;

    // Use visualizationGoal (detailed composition instructions) + content excerpt for context
    // The visualizationGoal tells Gemini WHAT to draw, the excerpt provides the DATA
    const imagePrompt = `${style.style}

IMAGE TYPE: ${rec.imageType}

COMPOSITION:
${rec.visualizationGoal}

KEY DATA TO INCLUDE:
${rec.contentExcerpt}`;

    try {
      // Use the aspect ratio passed from CLI (default: 1:1 for consistency with manual generations)

      // Generate descriptive filename from section title
      const sectionSlug = toKebabCase(rec.sectionTitle);

      // Log prompts to file for debugging
      const logFile = path.join(process.cwd(), 'image-prompts.log');
      const logEntry = `
${'='.repeat(80)}
[${new Date().toISOString()}] Image ${i + 1}/${recommendations.length}: ${rec.sectionTitle}
${'='.repeat(80)}
Section Heading: ${rec.sectionHeading}
Image Type: ${rec.imageType}
Placement: ${rec.placementHint}
Anchor Text: ${rec.anchorText}

--- VISUALIZATION GOAL (from analysis) ---
${rec.visualizationGoal}

--- CONTENT EXCERPT ---
${rec.contentExcerpt}

--- FINAL PROMPT SENT TO GEMINI ---
${imagePrompt}
${'='.repeat(80)}

`;
      await fs.appendFile(logFile, logEntry, 'utf-8');
      console.log(`  [LOG] Prompt logged to image-prompts.log`);

      const imageFiles = await generateAndSaveImages({
        prompt: imagePrompt,
        aspectRatio,
        outputDir,
        filePrefix: `${fileName}-section-${sectionSlug}${suffix}`,
        referenceImages: [],
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
      lines.splice(lineNumber, 0, imageMarkdown);
      console.log(`  Inserted image at line ${lineNumber}`);
    }

    // Write updated file
    await fs.writeFile(filePath, lines.join('\n'), 'utf-8');
    console.log(`\n[OK] Updated ${filePath} with ${generatedImages.length} images`);
  }
}

async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args[0].startsWith('--')) {
    console.error('Usage: npx tsx scripts/images/generate-section-images.ts <file.qmd> [options]');
    console.error('');
    console.error('Options:');
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

  const filePath = args[0];
  const dryRun = args.includes('--dry-run');
  const force = args.includes('--force');
  // Default to bw-academic style (black & white), use --retro-futuristic for fun retro futuristic style
  const useAcademicStyle = !args.includes('--retro-futuristic');

  // Parse --aspect argument (default: 1:1 for consistency with manual generations)
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

  if (!existsSync(filePath)) {
    console.error(`[ERROR] File not found: ${filePath}`);
    process.exit(1);
  }

  console.log(`[INFO] Style: ${useAcademicStyle ? 'bw-academic (black and white scientific)' : 'retro-futuristic'}`);
  console.log(`[INFO] Aspect ratio: ${aspectRatio}`);
  if (dryRun) {
    console.log('[INFO] DRY RUN - will show recommendations without generating');
  }
  if (force) {
    console.log('[INFO] FORCE MODE - will delete existing images and regenerate all');
  }

  // Force mode: clean up existing section images and references
  if (force && !dryRun) {
    const fileName = path.basename(filePath, '.qmd');
    // Use new output directory: assets/images/<qmd-basename>/
    const outputDir = path.join(process.cwd(), 'assets', 'images', fileName);

    // Delete existing section images
    if (existsSync(outputDir)) {
      const { readdirSync, unlinkSync } = await import('fs');
      const files = readdirSync(outputDir);
      const sectionImages = files.filter(f => f.startsWith(`${fileName}-section-`) && f.endsWith('.png'));

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
    // Match section images with any surrounding newlines (1+ before and after)
    // Replace with exactly 2 newlines to maintain paragraph spacing
    // Match both old (assets/section-images/) and new (assets/images/) paths
    const sectionImagePattern = /\n+!\[.*?\]\(\/assets\/(?:section-images|images)\/.*?\)\n+/g;
    let fileWithoutImages = fileContent.replace(sectionImagePattern, '\n\n');
    // Consolidate any remaining multiple consecutive newlines (3+ → 2)
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
    console.log('\n[DRY RUN COMPLETE] Run without --dry-run to generate images');
    process.exit(0);
  }

  // Generate and insert images
  await generateSectionImages(filePath, analysis.recommendations, useAcademicStyle, cleanedContent, aspectRatio);

  console.log('\n='.repeat(80));
  console.log('✓ Complete');
  console.log('='.repeat(80));
}

main().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
