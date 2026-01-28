/**
 * Generate images for specific sections within chapters using intelligent analysis
 *
 * Loops through sections programmatically, checking each one individually.
 * Asks Gemini Flash for each section whether an image would be valuable.
 * If yes, generates it; if no, moves on.
 *
 * Smart skip logic (avoids unnecessary image generation):
 *   - Sections with existing visual content:
 *     - Markdown images: ![alt](path)
 *     - Python/R code blocks generating charts (matplotlib, plotly, ggplot)
 *     - Observable JS blocks, Mermaid diagrams
 *     - HTML <img> tags, Quarto figure shortcodes
 *   - Structural sections: Introduction, Conclusion, Summary, References, etc.
 *   - Very short sections (< 200 chars / ~30 words)
 *
 * Defaults to processing ALL book files if no specific file is provided.
 * Uses bw-academic style (black & white scientific) for professional publications.
 * Default aspect ratio is 1:1 (square) for consistency with manual generations.
 *
 * Usage:
 *   npx tsx scripts/images/generate-section-images.ts              # Process all book files
 *   npx tsx scripts/images/generate-section-images.ts <file.qmd>   # Process specific file
 *
 * Options:
 *   --retro-futuristic    Generate in retro-futuristic style (default: bw-academic)
 *   --aspect <ratio>      Aspect ratio: 1:1, 3:4, 9:16, 16:9 (default: 1:1)
 *   --dry-run             Show recommendations without generating images
 *   --force               Delete existing section images and regenerate all
 *   --limit <n>           Limit to processing n sections (for testing)
 *
 * Examples:
 *   npx tsx scripts/images/generate-section-images.ts                    # All files
 *   npx tsx scripts/images/generate-section-images.ts --dry-run          # Preview all
 *   npx tsx scripts/images/generate-section-images.ts --force            # Regenerate all
 *   npx tsx scripts/images/generate-section-images.ts knowledge/problem.qmd --limit 5
 */

import dotenv from 'dotenv';
import path from 'path';
import fs from 'fs/promises';
import { existsSync, readdirSync, unlinkSync } from 'fs';
import { generateGeminiFlashContent } from '../lib/llm';
import { generateAndSaveImages } from '../lib/gemini-images';
import { getCleanedContentForLLM, getAllQmdFilesWithFrontmatter, prepareContentForLLM, loadQuartoVariables, replaceQuartoVariables, cleanContentForImagePrompt } from '../lib/file-utils';
import { VisualStyles } from '../lib/image-prompts';
import { sortFilesByWorstCoverage, analyzeFileCoverage } from './image-coverage';

dotenv.config();

interface Section {
  heading: string;       // The markdown heading (e.g., "## Problem Statement")
  headingLevel: number;  // 1-6 for h1-h6
  title: string;         // Just the text (e.g., "Problem Statement")
  content: string;       // Full section content including heading
  rawContent: string;    // Raw content before variable replacement
  startLine: number;     // Line number where section starts (0-indexed)
  endLine: number;       // Line number where section ends (0-indexed, exclusive)
  hasVisualContent: boolean;  // Whether section already contains visual content
  visualContentType: string | null;  // Type of visual content found (for logging)
}

interface ImageRecommendation {
  shouldGenerate: boolean;
  imageType: 'diagram' | 'chart' | 'infographic' | 'flowchart' | null;
  caption: string;          // Natural caption for alt text
  reasoning: string;        // Why this image is/isn't needed
  rejectionRule?: string;   // Which automatic rejection applied, if any
}

/**
 * Detect if content contains visual elements (images, charts, diagrams)
 * Returns the type of visual content found, or null if none
 */
function detectVisualContent(content: string): string | null {
  // Markdown images: ![alt](path)
  if (/!\[.*?\]\(.*?\)/.test(content)) {
    return 'markdown-image';
  }

  // Python code blocks that likely generate charts
  // Look for matplotlib, plotly, seaborn, altair patterns
  if (/```\{python\}[\s\S]*?(plt\.|fig\.|px\.|sns\.|alt\.)[\s\S]*?```/i.test(content)) {
    return 'python-chart';
  }

  // R code blocks that likely generate plots
  if (/```\{r\}[\s\S]*?(ggplot|plot\(|geom_)[\s\S]*?```/i.test(content)) {
    return 'r-plot';
  }

  // Observable JS blocks (often used for interactive visualizations)
  if (/```\{ojs\}/.test(content)) {
    return 'observable-js';
  }

  // Mermaid diagrams
  if (/```\{?mermaid\}?/.test(content)) {
    return 'mermaid-diagram';
  }

  // HTML img tags
  if (/<img\s+[^>]*src=/i.test(content)) {
    return 'html-image';
  }

  // Quarto figure shortcodes
  if (/\{\{<\s*figure\s+/.test(content)) {
    return 'quarto-figure';
  }

  // Quarto include of image files
  if (/\{\{<\s*include\s+.*\.(png|jpg|jpeg|gif|svg|webp)/i.test(content)) {
    return 'quarto-include-image';
  }

  // Quarto include of QMD files (included content likely has its own images)
  if (/\{\{<\s*include\s+.*\.qmd/i.test(content)) {
    return 'quarto-include-qmd';
  }

  return null;
}

/**
 * Detect if section contains markdown tables (tables ARE visualizations)
 */
function hasTable(content: string): boolean {
  // Markdown tables: |---|---| pattern with at least 2 columns
  return /\|[^|]+\|[^|]+\|/.test(content) && /\|-+\|/.test(content);
}

/**
 * Detect if section is primarily mathematical (LaTeX equations)
 * Formulas are self-explanatory and don't need generated images
 */
function hasMathEquations(content: string): boolean {
  // Display math: $$ ... $$ or \[ ... \]
  const displayMath = /\$\$[\s\S]+?\$\$|\\\[[\s\S]+?\\\]/.test(content);
  // Count inline math occurrences
  const inlineMathCount = (content.match(/\$[^$]+\$/g) || []).length;
  return displayMath || inlineMathCount >= 3;
}

/**
 * Detect if section has ASCII diagrams/flowcharts (already visual)
 */
function hasAsciiDiagram(content: string): boolean {
  // Box-drawing characters or arrow patterns
  return /[┌┐└┘│─├┤┬┴┼]/.test(content) ||
         /(\+[-=]+\+|[|│]\s+[|│])/.test(content) ||
         /^.*[→←↑↓▲▼►◄].*$/m.test(content);
}

/**
 * Check if section title suggests it's structural (intro/conclusion/references)
 * These sections typically don't benefit from generated images
 */
function isStructuralSection(title: string): boolean {
  const structuralPatterns = [
    /^introduction$/i,
    /^conclusion$/i,
    /^summary$/i,
    /^references$/i,
    /^bibliography$/i,
    /^acknowledgements?$/i,
    /^appendix$/i,
    /^table of contents$/i,
    /^overview$/i,
    /^preface$/i,
    /^foreword$/i,
  ];

  return structuralPatterns.some(pattern => pattern.test(title.trim()));
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
  // Normalize line endings (handle Windows \r\n)
  const normalizedRaw = rawContent.replace(/\r\n/g, '\n').replace(/\r/g, '\n');
  const normalizedCleaned = cleanedContent.replace(/\r\n/g, '\n').replace(/\r/g, '\n');

  const rawLines = normalizedRaw.split('\n');
  const cleanedLines = normalizedCleaned.split('\n');
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

    // Check if section already has visual content
    const visualContentType = detectVisualContent(rawSectionContent);

    sections.push({
      heading: current.heading,
      headingLevel: current.level,
      title: current.title,
      content: cleanedSectionContent,
      rawContent: rawSectionContent,
      startLine,
      endLine,
      hasVisualContent: visualContentType !== null,
      visualContentType,
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

  const prompt = `Analyze if this section would SIGNIFICANTLY benefit from a generated image.

SECTION:
---
${resolvedContent}
---

AUTOMATIC REJECTIONS (answer NO if ANY apply):
1. Section contains a TABLE - tables ARE the visualization
2. Section contains MATH EQUATIONS ($$...$$) - formulas are self-explanatory
3. Section shows a SIMPLE CURVE described by a formula (e.g., "Score = 1 - e^{-x}")
4. Section has ASCII DIAGRAMS or box-drawing characters
5. Information is ALREADY CLEAR from text/lists - image would just restate it
6. Section describes ONE metric threshold or scale (e.g., "I² > 75% means high heterogeneity")
7. This appears to be ONE STEP of a worked example (limit images per example)
8. A bar chart would just restate what a table already shows

ONLY recommend YES if:
- Complex MULTI-ENTITY relationships (5+ interconnected components)
- COMPARATIVE data across 4+ categories that would benefit from side-by-side visual
- PROCESS FLOW with conditional branching (not simple linear steps)
- ARCHITECTURE diagrams showing system components and data flow
- The image would provide understanding NOT achievable from the text

KEY QUESTION: Would a reader skip the text and understand from JUST the image?
If the text/table/formula is clearer than any possible image, answer NO.

DEFAULT TO NO unless there is compelling reason for an image.

Respond with JSON only:
{
  "shouldGenerate": true/false,
  "imageType": "diagram" | "chart" | "infographic" | "flowchart" | null,
  "caption": "<1-2 sentence description for alt text, NO 'Figure X:' prefix>",
  "reasoning": "<brief explanation>",
  "rejectionRule": "<which automatic rejection rule applied, or 'none' if recommending>"
}

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

  // Clean content for image generation (strips markdown links, footnotes, code blocks, etc.)
  const contentForImage = cleanContentForImagePrompt(resolvedContent);

  // Simple prompt: just style + full section content. Let the image model figure out the visualization.
  const imagePrompt = `${style.style}

${contentForImage}`;

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

    // Skip if section already has visual content (unless force mode)
    if (section.hasVisualContent && !force) {
      console.log(`  [SKIP] "${section.title}" - already has ${section.visualContentType}`);
      skipped++;
      continue;
    }

    // Skip structural sections (intro, conclusion, references, etc.)
    if (isStructuralSection(section.title)) {
      console.log(`  [SKIP] "${section.title}" - structural section`);
      skipped++;
      continue;
    }

    // Skip very short sections (under 200 chars / ~30 words)
    if (section.content.length < 200) {
      console.log(`  [SKIP] "${section.title}" - too short (${section.content.length} chars)`);
      skipped++;
      continue;
    }

    // Skip sections with tables (tables ARE visualizations)
    if (hasTable(section.rawContent)) {
      console.log(`  [SKIP] "${section.title}" - contains table (tables are visualizations)`);
      skipped++;
      continue;
    }

    // Skip sections with significant math equations (formulas are self-explanatory)
    if (hasMathEquations(section.rawContent)) {
      console.log(`  [SKIP] "${section.title}" - contains math equations`);
      skipped++;
      continue;
    }

    // Skip sections with ASCII diagrams (already visual)
    if (hasAsciiDiagram(section.rawContent)) {
      console.log(`  [SKIP] "${section.title}" - contains ASCII diagram`);
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
  // Default to --all if no file specified
  const hasFileArg = args.some(arg => !arg.startsWith('--') && arg.endsWith('.qmd'));
  const processAll = args.includes('--all') || !hasFileArg;

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
    // Batch mode - process all QMD files with frontmatter (excludes figures/, includes/, templates/)
    console.log('\n[*] Scanning all QMD files with frontmatter...');
    const allFiles = await getAllQmdFilesWithFrontmatter();
    const unsortedFiles = allFiles.filter(f => !f.endsWith('index.qmd'));
    console.log(`[OK] Found ${unsortedFiles.length} QMD files`);

    // Sort files by worst image coverage first (highest chars/image ratio)
    console.log('[*] Analyzing image coverage to prioritize files...');
    const qmdFiles = await sortFilesByWorstCoverage(unsortedFiles, { quiet: true });
    console.log('[OK] Files sorted by image coverage (worst first)\n');

    let totalEvaluated = 0;
    let totalGenerated = 0;
    let totalSkipped = 0;

    for (let i = 0; i < qmdFiles.length; i++) {
      const filePath = qmdFiles[i];
      const relativePath = path.relative(process.cwd(), filePath);

      // Get coverage info for display
      const coverage = await analyzeFileCoverage(filePath);
      const coverageNote = ` [${coverage.status}: ${coverage.ratio.toLocaleString()} chars/img]`;

      // Log existing section images count (but still process - per-section logic handles skipping)
      const existingCount = countExistingSectionImages(filePath);
      const existingNote = existingCount > 0 ? ` (${existingCount} existing)` : '';

      console.log(`\n[${i + 1}/${qmdFiles.length}] Processing: ${relativePath}${coverageNote}${existingNote}`);
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
    const filePath = args.find(arg => arg.endsWith('.qmd'));

    if (!filePath) {
      console.error('[ERROR] No .qmd file specified');
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
