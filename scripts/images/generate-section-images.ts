/**
 * Generate images for specific sections within chapters using intelligent analysis
 *
 * NEW APPROACH: Loops through sections programmatically, checking each one individually.
 * Skips sections that already have images. Asks Gemini Flash for each section whether
 * an image would be valuable - if yes, generates it; if no, moves on.
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
 *   --limit <n>           Limit to processing n sections (for testing)
 *
 * Examples:
 *   npx tsx scripts/images/generate-section-images.ts knowledge/appendix/invisible-graveyard.qmd
 *   npx tsx scripts/images/generate-section-images.ts --all
 *   npx tsx scripts/images/generate-section-images.ts --all --dry-run
 *   npx tsx scripts/images/generate-section-images.ts --all --force
 *   npx tsx scripts/images/generate-section-images.ts knowledge/appendix/invisible-graveyard.qmd --limit 5
 *   npx tsx scripts/images/generate-section-images.ts knowledge/appendix/invisible-graveyard.qmd --retro-futuristic
 */

import dotenv from 'dotenv';
import path from 'path';
import fs from 'fs/promises';
import { existsSync, readdirSync, unlinkSync } from 'fs';
import { generateGeminiFlashContent } from '../lib/llm';
import { generateAndSaveImages } from '../lib/gemini-images';
import { getCleanedContentForLLM, getBookFilesForProcessing, prepareContentForLLM, loadQuartoVariables, replaceQuartoVariables } from '../lib/file-utils';
import { VisualStyles } from '../lib/image-prompts';

dotenv.config();

interface Section {
  heading: string;       // The markdown heading (e.g., "## Problem Statement")
  headingLevel: number;  // 1-6 for h1-h6
  title: string;         // Just the text (e.g., "Problem Statement")
  content: string;       // Full section content including heading
  rawContent: string;    // Raw content before variable replacement
  startLine: number;     // Line number where section starts (0-indexed)
  endLine: number;       // Line number where section ends (0-indexed, exclusive)
  hasImage: boolean;     // Whether section already contains an image
}

interface ImageRecommendation {
  shouldGenerate: boolean;
  imageType: 'diagram' | 'chart' | 'infographic' | 'flowchart' | null;
  caption: string;          // Natural caption for alt text
  reasoning: string;        // Why this image is/isn't needed
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
 * Parse a file into sections based on markdown headings
 */
function parseIntoSections(rawContent: string, cleanedContent: string): Section[] {
  const rawLines = rawContent.split('\n');
  const cleanedLines = cleanedContent.split('\n');
  const sections: Section[] = [];

  // Find all headings in raw content
  const headingPattern = /^(#{1,6})\s+(.+)$/;
  const headingIndices: Array<{ line: number; level: number; title: string; heading: string }> = [];

  for (let i = 0; i < rawLines.length; i++) {
    const match = rawLines[i].match(headingPattern);
    if (match) {
      headingIndices.push({
        line: i,
        level: match[1].length,
        title: match[2].trim(),
        heading: rawLines[i].trim(),
      });
    }
  }

  // Build sections from headings
  for (let i = 0; i < headingIndices.length; i++) {
    const current = headingIndices[i];
    const next = headingIndices[i + 1];

    const startLine = current.line;
    const endLine = next ? next.line : rawLines.length;

    // Extract raw content for this section
    const rawSectionLines = rawLines.slice(startLine, endLine);
    const rawSectionContent = rawSectionLines.join('\n');

    // Find corresponding cleaned content (approximate - headings should match)
    let cleanedSectionContent = '';
    const cleanedHeadingIdx = cleanedLines.findIndex((line, idx) =>
      idx >= (i > 0 ? headingIndices[i - 1].line : 0) &&
      line.trim() === current.heading
    );

    if (cleanedHeadingIdx !== -1) {
      // Find next heading in cleaned content
      let cleanedEndIdx = cleanedLines.length;
      for (let j = cleanedHeadingIdx + 1; j < cleanedLines.length; j++) {
        if (headingPattern.test(cleanedLines[j])) {
          cleanedEndIdx = j;
          break;
        }
      }
      cleanedSectionContent = cleanedLines.slice(cleanedHeadingIdx, cleanedEndIdx).join('\n');
    } else {
      // Fallback: use raw content
      cleanedSectionContent = rawSectionContent;
    }

    // Check if section already has an image
    const hasImage = /!\[.*?\]\(.*?\)/.test(rawSectionContent);

    sections.push({
      heading: current.heading,
      headingLevel: current.level,
      title: current.title,
      content: cleanedSectionContent,
      rawContent: rawSectionContent,
      startLine,
      endLine,
      hasImage,
    });
  }

  return sections;
}

/**
 * Ask Gemini Flash if a section would benefit from an image
 */
async function evaluateSection(section: Section, variables: Map<string, string>): Promise<ImageRecommendation> {
  // Resolve Quarto variables in the section content so LLM sees actual values
  const resolvedContent = replaceQuartoVariables(section.rawContent, variables);

  const prompt = `Analyze this section and determine if it would significantly benefit from a visual aid.

SECTION:
---
${resolvedContent}
---

Respond with JSON only:
{
  "shouldGenerate": true/false,
  "imageType": "diagram" | "chart" | "infographic" | "flowchart" | null,
  "caption": "<1-2 sentence description for alt text, NO 'Figure X:' prefix>",
  "reasoning": "<brief explanation>"
}

ONLY recommend an image if:
- Quantitative comparisons (2+ numbers to compare, especially with ratios like "604:1" or "50x")
- Multi-step processes (3+ steps) needing visualization
- Interconnected relationships (4+ entities) that benefit from a diagram
- Data-dense content with specific statistics, even if brief

Do NOT recommend images for:
- Pure narrative/rhetorical content without specific numbers
- Sections with only 1 number and no comparison
- Already-visual content (lists that are self-explanatory)

If shouldGenerate is false, set imageType to null.`;

  try {
    const response = await generateGeminiFlashContent(prompt);
    const jsonMatch = response.match(/\{[\s\S]*\}/);

    if (!jsonMatch) {
      console.log(`  [WARN] Could not parse response for section "${section.title}"`);
      return {
        shouldGenerate: false,
        imageType: null,
        caption: '',
        reasoning: 'Failed to parse LLM response',
      };
    }

    return JSON.parse(jsonMatch[0]) as ImageRecommendation;
  } catch (error) {
    console.error(`  [ERROR] Evaluation failed for section "${section.title}":`, error);
    return {
      shouldGenerate: false,
      imageType: null,
      caption: '',
      reasoning: 'Evaluation error',
    };
  }
}

/**
 * Generate image for a section and insert it into the file
 */
async function generateAndInsertImage(
  filePath: string,
  section: Section,
  recommendation: ImageRecommendation,
  resolvedContent: string,
  useAcademicStyle: boolean,
  aspectRatio: '1:1' | '3:4' | '9:16' | '16:9'
): Promise<boolean> {
  const fileName = path.basename(filePath, '.qmd');
  const outputDir = path.join(process.cwd(), 'assets', 'images', fileName);

  const style = useAcademicStyle ? VisualStyles['bw-academic'] : VisualStyles['retro-futuristic'];
  const sectionSlug = toKebabCase(section.title);

  // Simple prompt: just style + full section content. Let the image model figure out the visualization.
  const imagePrompt = `${style.style}

${resolvedContent}`;

  console.log(`\n  --- GENERATING IMAGE ---`);
  console.log(`  Section: ${section.title}`);
  console.log(`  Type: ${recommendation.imageType}`);

  try {
    const imageFiles = await generateAndSaveImages({
      prompt: imagePrompt,
      aspectRatio,
      outputDir,
      filePrefix: `${fileName}-section-${sectionSlug}${style.suffix}`,
      referenceImages: [],
      metadata: {
        title: recommendation.caption,
        description: `Visual for section: ${section.title}`,
        keywords: [recommendation.imageType || 'image', section.title, fileName, 'section-image'],
      },
    });

    if (!imageFiles || imageFiles.length === 0) {
      console.log(`  [WARN] No image generated`);
      return false;
    }

    const absolutePath = imageFiles[0];
    const relativePath = path.relative(process.cwd(), absolutePath).replace(/\\/g, '/');

    console.log(`  [OK] Generated: ${relativePath}`);

    // Read current file content
    const fileContent = await fs.readFile(filePath, 'utf-8');
    const lines = fileContent.split('\n');

    // Find where to insert the image (after the section heading, before first paragraph ends)
    // Insert after the first complete paragraph in the section
    let insertLine = section.startLine + 1;

    // Skip to end of first paragraph (find blank line or next content)
    for (let i = section.startLine + 1; i < section.endLine; i++) {
      const line = lines[i].trim();

      // Skip blank lines at start
      if (line === '') continue;

      // Found content - look for end of this paragraph
      for (let j = i + 1; j < section.endLine; j++) {
        const nextLine = lines[j].trim();

        // End of paragraph (blank line) or end of section
        if (nextLine === '' || j === section.endLine - 1) {
          // Check if current line ends properly (sentence end, not colon/list start)
          const prevLine = lines[j - 1].trim();
          if (prevLine.endsWith('.') || prevLine.endsWith('!') || prevLine.endsWith('?') || prevLine.endsWith('"')) {
            insertLine = j;
            break;
          }
        }

        // Don't insert before a list
        if (/^[-*+\d]/.test(nextLine)) {
          continue;
        }
      }
      break;
    }

    // Build image markdown
    const imageMarkdown = `\n![${recommendation.caption}](/${relativePath})\n`;

    // Insert the image
    lines.splice(insertLine, 0, imageMarkdown);

    // Write updated file
    await fs.writeFile(filePath, lines.join('\n'), 'utf-8');
    console.log(`  [OK] Inserted at line ${insertLine + 1}`);

    return true;
  } catch (error) {
    console.error(`  [ERROR] Failed to generate image:`, error);
    return false;
  }
}

/**
 * Count existing section images for a file
 */
function countExistingSectionImages(filePath: string): number {
  const fileName = path.basename(filePath, '.qmd');
  const outputDir = path.join(process.cwd(), 'assets', 'images', fileName);

  if (!existsSync(outputDir)) {
    return 0;
  }

  try {
    const files = readdirSync(outputDir);
    return files.filter((f: string) =>
      f.startsWith(`${fileName}-section-`) && (f.endsWith('.png') || f.endsWith('.jpg'))
    ).length;
  } catch {
    return 0;
  }
}

/**
 * Delete existing section images and references
 */
async function cleanExistingSectionImages(filePath: string): Promise<void> {
  const fileName = path.basename(filePath, '.qmd');
  const outputDir = path.join(process.cwd(), 'assets', 'images', fileName);

  // Delete image files
  if (existsSync(outputDir)) {
    const files = readdirSync(outputDir);
    const sectionImages = files.filter((f: string) =>
      f.startsWith(`${fileName}-section-`) && (f.endsWith('.png') || f.endsWith('.jpg'))
    );

    if (sectionImages.length > 0) {
      console.log(`\n[FORCE] Deleting ${sectionImages.length} existing section images...`);
      for (const img of sectionImages) {
        unlinkSync(path.join(outputDir, img));
        console.log(`  Deleted: ${img}`);
      }
    }
  }

  // Remove image references from file
  const fileContent = await fs.readFile(filePath, 'utf-8');
  const sectionImagePattern = /\n*!\[.*?\]\(\/assets\/(?:section-images|images)\/.*?\)\n*/g;
  let cleanedContent = fileContent.replace(sectionImagePattern, '\n\n');
  cleanedContent = cleanedContent.replace(/\n{3,}/g, '\n\n');

  if (cleanedContent !== fileContent) {
    await fs.writeFile(filePath, cleanedContent, 'utf-8');
    const removedCount = (fileContent.match(sectionImagePattern) || []).length;
    console.log(`[FORCE] Removed ${removedCount} section image references from file\n`);
  }
}

/**
 * Process a single file
 */
async function processFile(
  filePath: string,
  options: {
    dryRun: boolean;
    force: boolean;
    useAcademicStyle: boolean;
    aspectRatio: '1:1' | '3:4' | '9:16' | '16:9';
    limit: number;
  }
): Promise<{ evaluated: number; generated: number; skipped: number }> {
  const { dryRun, force, useAcademicStyle, aspectRatio, limit } = options;

  // Clean existing images if force mode
  if (force && !dryRun) {
    await cleanExistingSectionImages(filePath);
  }

  // Read raw file content
  const rawContent = await fs.readFile(filePath, 'utf-8');

  // Load Quarto variables for resolving in sections
  const variables = await loadQuartoVariables();

  // Parse into sections (we'll resolve variables per-section now)
  const sections = parseIntoSections(rawContent, rawContent);

  console.log(`\n[*] Found ${sections.length} sections in ${path.basename(filePath)}`);

  let evaluated = 0;
  let generated = 0;
  let skipped = 0;
  let limitReached = false;

  for (const section of sections) {
    if (limitReached) break;

    // Skip if section already has an image (unless force mode)
    if (section.hasImage && !force) {
      console.log(`  [SKIP] "${section.title}" - already has image`);
      skipped++;
      continue;
    }

    // Skip very short sections (only skip if truly minimal - under 100 chars)
    if (section.content.length < 100) {
      console.log(`  [SKIP] "${section.title}" - too short (${section.content.length} chars)`);
      skipped++;
      continue;
    }

    // Check limit
    if (limit > 0 && evaluated >= limit) {
      console.log(`\n[LIMIT] Reached limit of ${limit} sections`);
      limitReached = true;
      break;
    }

    console.log(`\n  [${evaluated + 1}] Evaluating: "${section.title}" (${section.rawContent.length} chars)`);

    // Ask Gemini if this section needs an image (pass variables for resolution)
    const recommendation = await evaluateSection(section, variables);
    evaluated++;

    if (!recommendation.shouldGenerate) {
      console.log(`  [NO] ${recommendation.reasoning}`);
      continue;
    }

    console.log(`  [YES] ${recommendation.imageType}: ${recommendation.reasoning}`);

    // Resolve variables for image generation
    const resolvedContent = replaceQuartoVariables(section.rawContent, variables);

    if (dryRun) {
      console.log(`  [DRY RUN] Would generate: ${recommendation.caption}`);
      generated++;
      continue;
    }

    // Generate and insert the image
    const success = await generateAndInsertImage(
      filePath,
      section,
      recommendation,
      resolvedContent,
      useAcademicStyle,
      aspectRatio
    );

    if (success) {
      generated++;

      // Re-read file after insertion (line numbers have changed)
      const updatedContent = await fs.readFile(filePath, 'utf-8');

      // Re-parse sections with updated content for remaining iterations
      const updatedSections = parseIntoSections(updatedContent, updatedContent);

      // Find current section index and update remaining sections
      const currentIdx = sections.findIndex(s => s.title === section.title);
      if (currentIdx !== -1) {
        for (let i = currentIdx + 1; i < sections.length; i++) {
          const updatedSection = updatedSections.find(s => s.title === sections[i].title);
          if (updatedSection) {
            sections[i] = updatedSection;
          }
        }
      }
    }
  }

  return { evaluated, generated, skipped };
}

async function main() {
  const args = process.argv.slice(2);
  const processAll = args.includes('--all');

  // Show help if no arguments
  if (args.length === 0 || (args[0].startsWith('--') && !processAll)) {
    console.error('Usage: npx tsx scripts/images/generate-section-images.ts <file.qmd> [options]');
    console.error('       npx tsx scripts/images/generate-section-images.ts --all [options]');
    console.error('');
    console.error('Options:');
    console.error('  --all                 Process all book QMD files');
    console.error('  --retro-futuristic    Use retro-futuristic style (default: bw-academic)');
    console.error('  --aspect <ratio>      Aspect ratio: 1:1, 3:4, 9:16, 16:9 (default: 1:1)');
    console.error('  --dry-run             Show recommendations without generating images');
    console.error('  --force               Delete existing section images and regenerate all');
    console.error('  --limit <n>           Limit to processing n sections (for testing)');
    console.error('');
    console.error('Examples:');
    console.error('  npx tsx scripts/images/generate-section-images.ts knowledge/problem.qmd --limit 5');
    console.error('  npx tsx scripts/images/generate-section-images.ts --all --dry-run');
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
      process.exit(1);
    }
  }

  // Parse --limit argument
  let limit = 0;
  const limitIndex = args.indexOf('--limit');
  if (limitIndex !== -1 && args[limitIndex + 1]) {
    limit = parseInt(args[limitIndex + 1], 10);
    if (isNaN(limit) || limit < 1) {
      console.error(`[ERROR] Invalid limit: ${args[limitIndex + 1]}`);
      process.exit(1);
    }
  }

  console.log('Section-by-Section Image Generator');
  console.log('='.repeat(80));
  console.log(`[INFO] Style: ${useAcademicStyle ? 'bw-academic' : 'retro-futuristic'}`);
  console.log(`[INFO] Aspect ratio: ${aspectRatio}`);
  if (dryRun) console.log('[INFO] DRY RUN - will show recommendations without generating');
  if (force) console.log('[INFO] FORCE MODE - will regenerate all images');
  if (limit > 0) console.log(`[INFO] LIMIT: Processing max ${limit} sections`);

  const options = { dryRun, force, useAcademicStyle, aspectRatio, limit };

  if (processAll) {
    // Batch mode
    console.log('\n[*] Scanning all book files...');
    const allFiles = await getBookFilesForProcessing();
    const qmdFiles = allFiles.filter(f => !f.endsWith('index.qmd'));
    console.log(`[OK] Found ${qmdFiles.length} QMD files\n`);

    let totalEvaluated = 0;
    let totalGenerated = 0;
    let totalSkipped = 0;

    for (let i = 0; i < qmdFiles.length; i++) {
      const filePath = qmdFiles[i];
      const relativePath = path.relative(process.cwd(), filePath);

      // Check if file already has section images (skip unless force)
      if (!force) {
        const existingCount = countExistingSectionImages(filePath);
        if (existingCount > 0) {
          console.log(`\n[${i + 1}/${qmdFiles.length}] SKIP: ${relativePath} (${existingCount} existing images)`);
          continue;
        }
      }

      console.log(`\n[${i + 1}/${qmdFiles.length}] Processing: ${relativePath}`);
      console.log('-'.repeat(80));

      const result = await processFile(filePath, options);
      totalEvaluated += result.evaluated;
      totalGenerated += result.generated;
      totalSkipped += result.skipped;

      // Check if we've hit the global limit
      if (limit > 0 && totalEvaluated >= limit) {
        console.log(`\n[LIMIT] Global limit of ${limit} reached`);
        break;
      }
    }

    console.log('\n' + '='.repeat(80));
    console.log('BATCH COMPLETE');
    console.log('='.repeat(80));
    console.log(`  Sections evaluated: ${totalEvaluated}`);
    console.log(`  Images ${dryRun ? 'recommended' : 'generated'}: ${totalGenerated}`);
    console.log(`  Sections skipped: ${totalSkipped}`);
  } else {
    // Single file mode
    const filePath = args.find(arg => !arg.startsWith('--') && arg !== aspectRatio && arg !== String(limit));

    if (!filePath) {
      console.error('[ERROR] No file specified');
      process.exit(1);
    }

    if (!existsSync(filePath)) {
      console.error(`[ERROR] File not found: ${filePath}`);
      process.exit(1);
    }

    const result = await processFile(filePath, options);

    console.log('\n' + '='.repeat(80));
    console.log('COMPLETE');
    console.log('='.repeat(80));
    console.log(`  Sections evaluated: ${result.evaluated}`);
    console.log(`  Images ${dryRun ? 'recommended' : 'generated'}: ${result.generated}`);
    console.log(`  Sections skipped: ${result.skipped}`);
  }

  if (dryRun) {
    console.log('\n[DRY RUN COMPLETE] Run without --dry-run to generate images');
  }
}

main().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
