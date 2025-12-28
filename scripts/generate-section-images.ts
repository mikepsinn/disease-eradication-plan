/**
 * Generate section-specific images using intelligent analysis
 *
 * Gives Gemini the entire file and asks it to identify sections that would
 * benefit from visual aids (diagrams, charts, infographics, flowcharts).
 *
 * Defaults to academic style (black & white scientific) for professional publications.
 * All images use 9:16 portrait aspect ratio for mobile-first design.
 *
 * Usage:
 *   npx tsx scripts/generate-section-images.ts <file.qmd> [options]
 *
 * Options:
 *   --retro-futuristic    Generate in retro-futuristic style (default: academic)
 *   --dry-run             Show recommendations without generating images
 *   --force               Delete existing section images and regenerate all
 *
 * Examples:
 *   npx tsx scripts/generate-section-images.ts knowledge/economics/economics.qmd
 *   npx tsx scripts/generate-section-images.ts knowledge/economics/economics.qmd --retro-futuristic
 *   npx tsx scripts/generate-section-images.ts knowledge/economics/economics.qmd --dry-run
 *   npx tsx scripts/generate-section-images.ts knowledge/economics/economics.qmd --force
 */

import dotenv from 'dotenv';
import path from 'path';
import fs from 'fs/promises';
import { existsSync } from 'fs';
import { generateGeminiFlashContent } from './lib/llm.js';
import { generateAndSaveImages } from './lib/genai-image.js';
import { getCleanedContentForLLM } from './lib/file-utils.js';
import { VisualStyles } from './lib/image-prompts.js';

dotenv.config();

interface ImageRecommendation {
  lineNumber: number;
  sectionTitle: string;
  contentExcerpt: string;
  imageType: 'diagram' | 'chart' | 'infographic' | 'flowchart';
  visualizationGoal: string;
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
 * Analyze entire file and get section-specific image recommendations
 */
async function analyzeFileForSectionImages(
  filePath: string,
  cleanedContent: string
): Promise<AnalysisResponse> {
  console.log(`\n[*] Analyzing file with Gemini Flash...`);
  console.log(`  File: ${filePath}`);

  // Use cleaned content (with variables replaced) for analysis
  // Line numbers from cleaned content should match raw file since variable replacement is inline
  const lines = cleanedContent.split('\n');

  const prompt = `You are an expert academic editor analyzing a scholarly document. Your task is to identify sections that would benefit from visual aids (diagrams, charts, infographics, or flowcharts).

IMPORTANT GUIDELINES:
1. **Default to YES**: Recommend images for ALL major sections (## headings) unless the image would be actively unhelpful
2. **Bias towards visuals**: When in doubt, include the image - visual aids enhance engagement and comprehension
3. **Only skip if harmful**: Skip images only if they would distract, confuse, or provide zero value
4. **Err on the side of more**: Better to have too many visuals than too few in an academic book

FILE METADATA:
- Path: ${filePath}
- Total lines: ${lines.length}
- Word count: ~${cleanedContent.split(/\s+/).length}

FILE CONTENT WITH LINE NUMBERS (Quarto variables replaced with actual values):
---
${lines.map((line, idx) => `${idx + 1}: ${line}`).join('\n')}
---

Respond with JSON:
{
  "recommendations": [
    {
      "lineNumber": <exact line number where image should be inserted>,
      "sectionTitle": "<section heading text>",
      "contentExcerpt": "<relevant 200-500 word excerpt to visualize>",
      "imageType": "diagram" | "chart" | "infographic" | "flowchart",
      "visualizationGoal": "<specific description: what should the image show?>",
      "reasoning": "<1-2 sentences: why is this image necessary?>"
    }
  ],
  "totalRecommendations": <number>,
  "reasoning": "<overall assessment: how many visuals does this document need?>"
}

CRITERIA FOR RECOMMENDATION:
✅ ALWAYS recommend for:
- Any section with quantitative comparisons or data
- Any section describing processes, workflows, or systems
- Any section with multiple stakeholders or entities
- Any section with timelines, pathways, or alternatives
- Any section where spatial/visual relationships matter

✅ STRONGLY CONSIDER for:
- Abstract concepts that could be made concrete
- Lists of 3+ items that could be shown visually
- Cause-and-effect relationships
- Before/after scenarios

❌ ONLY skip if:
- Section is purely introductory/transitional (<100 words)
- Section is entirely citations/references
- Would be genuinely confusing or distracting
- Already has comprehensive tables/figures

When in doubt, INCLUDE the image. Visuals are valuable.`;

  try {
    const response = await generateGeminiFlashContent(prompt);
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
        console.log(`\n  ${idx + 1}. Line ${rec.lineNumber}: ${rec.sectionTitle}`);
        console.log(`     Type: ${rec.imageType}`);
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
  useAcademicStyle: boolean
): Promise<void> {
  if (recommendations.length === 0) {
    console.log(`\n[SKIP] No images to generate`);
    return;
  }

  console.log(`\n[*] Generating ${recommendations.length} section images...`);

  const fileName = path.basename(filePath, '.qmd');
  const relativePath = path.relative(process.cwd(), filePath);
  const outputDir = path.join(process.cwd(), 'assets', 'section-images', path.dirname(relativePath));

  // Read file content (raw, for line number mapping and insertion)
  const fileContent = await fs.readFile(filePath, 'utf-8');
  const lines = fileContent.split('\n');

  // Generate images for each recommendation
  const generatedImages: Array<{ lineNumber: number; imagePath: string }> = [];

  for (let i = 0; i < recommendations.length; i++) {
    const rec = recommendations[i];
    console.log(`\n  [${i + 1}/${recommendations.length}] Generating: ${rec.sectionTitle}`);

    const style = useAcademicStyle ? VisualStyles.academic : VisualStyles['retro-futuristic'];
    const suffix = useAcademicStyle ? '-academic' : '-retro-futuristic';

    // Use Gemini's curated excerpt (200-500 words specifically chosen for visualization)
    // Since we analyze cleaned content, the excerpt already has variables replaced
    // Simple prompt: just style + content, no meta-instructions that might leak into images
    const imagePrompt = `${style.style}

${rec.contentExcerpt}`;

    try {
      // Book-friendly: use portrait 3:4 (closest to standard book format)
      // Balances mobile readability with print compatibility (1:1.33 aspect ratio)
      // Fits printed pages better than 9:16 (1:1.78) without excessive scaling
      const aspectRatio = '3:4' as const;

      // Generate descriptive filename from section title
      const sectionSlug = toKebabCase(rec.sectionTitle);

      const imageFiles = await generateAndSaveImages({
        prompt: imagePrompt,
        aspectRatio,
        outputDir,
        filePrefix: `${fileName}-section-${sectionSlug}${suffix}`,
        referenceImages: [],
      });

      if (imageFiles && imageFiles.length > 0) {
        const imagePath = path.relative(process.cwd(), imageFiles[0]).replace(/\\/g, '/');
        console.log(`  [OK] Generated: ${imagePath}`);
        generatedImages.push({ lineNumber: rec.lineNumber, imagePath: `/${imagePath}` });
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

    for (const { lineNumber, imagePath } of generatedImages) {
      const imageMarkdown = `\n![Section Image](${imagePath})\n`;
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
    console.error('Usage: npx tsx scripts/generate-section-images.ts <file.qmd> [--retro-futuristic] [--dry-run] [--force]');
    console.error('');
    console.error('Options:');
    console.error('  --retro-futuristic    Use retro-futuristic style (default: academic black & white)');
    console.error('  --dry-run             Show recommendations without generating images');
    console.error('  --force               Delete existing section images and regenerate all');
    process.exit(1);
  }

  const filePath = args[0];
  const dryRun = args.includes('--dry-run');
  const force = args.includes('--force');
  // Default to academic style (black & white), use --retro-futuristic for fun retro futuristic style
  const useAcademicStyle = !args.includes('--retro-futuristic');

  console.log('📊 Section-Specific Image Generator');
  console.log('='.repeat(80));

  if (!existsSync(filePath)) {
    console.error(`[ERROR] File not found: ${filePath}`);
    process.exit(1);
  }

  console.log(`[INFO] Style: ${useAcademicStyle ? 'Academic (black and white scientific)' : 'Retro-futuristic'}`);
  if (dryRun) {
    console.log('[INFO] DRY RUN - will show recommendations without generating');
  }
  if (force) {
    console.log('[INFO] FORCE MODE - will delete existing images and regenerate all');
  }

  // Force mode: clean up existing section images and references
  if (force && !dryRun) {
    const fileName = path.basename(filePath, '.qmd');
    const relativePath = path.relative(process.cwd(), filePath);
    const outputDir = path.join(process.cwd(), 'assets', 'section-images', path.dirname(relativePath));

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
    // Match section images with surrounding blank lines
    const sectionImagePattern = /\n*!\[Section Image\]\(\/assets\/section-images\/.*?\)\n*/g;
    const cleanedContent = fileContent.replace(sectionImagePattern, '\n');

    if (cleanedContent !== fileContent) {
      await fs.writeFile(filePath, cleanedContent, 'utf-8');
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
  await generateSectionImages(filePath, analysis.recommendations, useAcademicStyle);

  console.log('\n='.repeat(80));
  console.log('✓ Complete');
  console.log('='.repeat(80));
}

main().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
