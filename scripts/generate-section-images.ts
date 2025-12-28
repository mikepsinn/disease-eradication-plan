/**
 * Generate section-specific images using intelligent analysis
 *
 * Gives Gemini the entire file and asks it to identify sections that would
 * benefit from visual aids (diagrams, charts, infographics, flowcharts).
 *
 * Usage:
 *   npx tsx scripts/generate-section-images.ts <file.qmd> [options]
 *
 * Options:
 *   --academic-style    Generate in academic style (black & white)
 *   --dry-run           Show recommendations without generating images
 *
 * Example:
 *   npx tsx scripts/generate-section-images.ts knowledge/economics/economics.qmd --academic-style
 */

import dotenv from 'dotenv';
import path from 'path';
import fs from 'fs/promises';
import { existsSync } from 'fs';
import matter from 'gray-matter';
import { generateGeminiFlashContent } from './lib/llm.js';
import { generateAndSaveImages } from './lib/genai-image.js';
import { getCleanedContentForLLM } from './lib/file-utils.js';
import { VisualStyles, ImagePrompts } from './lib/image-prompts.js';

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
 * Analyze entire file and get section-specific image recommendations
 */
async function analyzeFileForSectionImages(
  filePath: string,
  cleanedContent: string
): Promise<AnalysisResponse> {
  console.log(`\n[*] Analyzing file with Gemini Flash...`);
  console.log(`  File: ${filePath}`);

  // Read raw file to get line numbers
  const rawContent = await fs.readFile(filePath, 'utf-8');
  const lines = rawContent.split('\n');

  const prompt = `You are an expert academic editor analyzing a scholarly document. Your task is to identify sections that would benefit from visual aids (diagrams, charts, infographics, or flowcharts).

IMPORTANT GUIDELINES:
1. **Use reasoning**: Only recommend images where visualization would significantly improve comprehension
2. **Quality over quantity**: An image should clarify complex relationships, data, processes, or concepts
3. **No arbitrary limits**: Recommend as many or as few images as genuinely needed
4. **Consider the trade-off**: Each image has a cost (reader attention, page space, generation time)
5. **Ask yourself**: "Would I struggle to understand this section without a visual aid?"

FILE METADATA:
- Path: ${filePath}
- Total lines: ${lines.length}
- Word count: ~${cleanedContent.split(/\s+/).length}

FILE CONTENT WITH LINE NUMBERS:
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
  "reasoning": "<overall assessment: does this document need visual aids? why or why not?>"
}

CRITERIA FOR RECOMMENDATION:
✅ Recommend if:
- Complex quantitative comparisons (e.g., ROI across interventions)
- Multi-step processes or workflows (e.g., clinical trial phases)
- Relationships between entities (e.g., funding flows, causal chains)
- Timeline comparisons (e.g., traditional vs. accelerated pathways)
- Data that's hard to grasp as text (e.g., scale discrepancies)

❌ Skip if:
- Concept is already clear in text
- Section is primarily narrative or argumentative
- Would be decorative rather than educational
- Text already has tables/figures that convey the information

Think step-by-step and be selective. Only recommend where images truly add value.`;

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
 * Extract full section content from line number to next section heading
 */
function extractFullSectionContent(lines: string[], startLine: number): string {
  // Start from the recommended line
  const contentLines: string[] = [];

  // Look backward to find the section heading
  let headingLine = startLine;
  for (let i = startLine; i >= 0; i--) {
    if (lines[i].match(/^#{1,4}\s+/)) {
      headingLine = i;
      break;
    }
  }

  // Collect lines from heading until next heading of same or higher level
  const headingMatch = lines[headingLine].match(/^(#{1,4})\s+/);
  const headingLevel = headingMatch ? headingMatch[1].length : 2;

  for (let i = headingLine; i < lines.length; i++) {
    const line = lines[i];

    // Stop at next heading of same or higher level (fewer #'s)
    if (i > headingLine && line.match(new RegExp(`^#{1,${headingLevel}}\\s+`))) {
      break;
    }

    contentLines.push(line);
  }

  return contentLines.join('\n').trim();
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

  // Get cleaned content with variables replaced (for image generation)
  const cleanedContent = await getCleanedContentForLLM(filePath);
  const cleanedLines = cleanedContent.split('\n');

  // Generate images for each recommendation
  const generatedImages: Array<{ lineNumber: number; imagePath: string }> = [];

  for (let i = 0; i < recommendations.length; i++) {
    const rec = recommendations[i];
    console.log(`\n  [${i + 1}/${recommendations.length}] Generating: ${rec.sectionTitle}`);

    const style = useAcademicStyle ? VisualStyles.academic : VisualStyles.retro;
    const suffix = useAcademicStyle ? '-academic' : '-retro';

    // Extract full section content from cleaned file (variables replaced, includes all context)
    const fullSectionContent = extractFullSectionContent(cleanedLines, rec.lineNumber - 1); // Convert to 0-indexed

    // Build prompt using same style instructions as project image generator
    // Use full section content instead of excerpt for better context
    const contentWithGoal = `VISUALIZATION GOAL: ${rec.visualizationGoal}

${fullSectionContent}`;

    // Use the infographic prompt builder for consistency with project images
    const imagePrompt = ImagePrompts.infographic.buildPrompt(contentWithGoal, style.style);

    try {
      // Determine aspect ratio based on image type
      const aspectRatio = rec.imageType === 'flowchart' || rec.imageType === 'diagram'
        ? '9:16' as const
        : '16:9' as const;

      const imageFiles = await generateAndSaveImages({
        prompt: imagePrompt,
        aspectRatio,
        outputDir,
        filePrefix: `${fileName}-section-${i + 1}${suffix}`,
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
    console.error('Usage: npx tsx scripts/generate-section-images.ts <file.qmd> [--academic-style] [--dry-run]');
    process.exit(1);
  }

  const filePath = args[0];
  const dryRun = args.includes('--dry-run');
  const useAcademicStyle = args.includes('--academic-style');

  console.log('📊 Section-Specific Image Generator');
  console.log('='.repeat(80));

  if (!existsSync(filePath)) {
    console.error(`[ERROR] File not found: ${filePath}`);
    process.exit(1);
  }

  if (useAcademicStyle) {
    console.log('[INFO] Using academic style (black and white scientific)');
  }
  if (dryRun) {
    console.log('[INFO] DRY RUN - will show recommendations without generating');
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
