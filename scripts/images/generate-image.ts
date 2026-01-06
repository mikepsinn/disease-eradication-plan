/**
 * Generate a single image from a prompt for insertion into chapters
 * Designed to be called by Claude Code during editing sessions
 *
 * Usage:
 *   npx tsx scripts/images/generate-image.ts "your prompt here" [options]
 *
 * Options:
 *   --file <path>         Auto-insert image into specified QMD file
 *   --type <type>         Image type: figure (default), diagram, chart, illustration
 *   --aspect <ratio>      Aspect ratio: 16:9 (default), 1:1, 4:3, 9:16
 *   --style <style>       Visual style: academic (default), retro, modern
 *   --output <dir>        Output directory (default: assets/images/generated)
 *   --alt <text>          Alt text for accessibility
 *
 * Examples:
 *   # Generate figure and get path
 *   npx tsx scripts/images/generate-image.ts "Flow chart showing treaty adoption process"
 *
 *   # Generate and auto-insert into file
 *   npx tsx scripts/images/generate-image.ts "Cost comparison bar chart" \
 *     --file knowledge/economics/economics.qmd \
 *     --alt "Bar chart comparing intervention costs"
 *
 *   # Generate diagram in specific style
 *   npx tsx scripts/images/generate-image.ts "Venn diagram of stakeholder interests" \
 *     --type diagram --style academic --aspect 1:1
 */

import dotenv from 'dotenv';
import path from 'path';
import fs from 'fs/promises';
import { existsSync } from 'fs';
import matter from 'gray-matter';
import { generateAndSaveImages } from '../lib/gemini-images.js';
import { VisualStyles } from '../lib/image-prompts.js';

// Load environment variables
dotenv.config();

// Image type configurations
const ImageTypes = {
  figure: {
    description: 'General figure illustration',
    promptPrefix: 'Create a clear, informative figure illustrating:',
  },
  diagram: {
    description: 'Diagram with labeled components',
    promptPrefix: 'Create a detailed diagram showing:',
  },
  chart: {
    description: 'Data visualization or chart',
    promptPrefix: 'Create a data visualization chart showing:',
  },
  illustration: {
    description: 'Conceptual illustration',
    promptPrefix: 'Create a conceptual illustration depicting:',
  },
} as const;

type ImageType = keyof typeof ImageTypes;

// Aspect ratio mappings
const AspectRatios: Record<string, string> = {
  '16:9': '16:9',
  '1:1': '1:1',
  '4:3': '4:3',
  '9:16': '9:16',
  'wide': '16:9',
  'square': '1:1',
  'portrait': '9:16',
};

interface GenerateImageOptions {
  prompt: string;
  file?: string;
  type: ImageType;
  aspect: string;
  style: string;
  output: string;
  alt?: string;
}

/**
 * Parse command line arguments
 */
function parseArgs(): GenerateImageOptions {
  const args = process.argv.slice(2);

  if (args.length === 0 || args[0].startsWith('--')) {
    console.error('ERROR: Prompt is required as first argument');
    console.error('Usage: npx tsx scripts/images/generate-image.ts "your prompt" [options]');
    process.exit(1);
  }

  const prompt = args[0];

  const getArg = (flag: string, defaultValue: string = ''): string => {
    const index = args.indexOf(flag);
    return index !== -1 && args[index + 1] ? args[index + 1] : defaultValue;
  };

  return {
    prompt,
    file: getArg('--file') || undefined,
    type: (getArg('--type', 'figure') as ImageType),
    aspect: AspectRatios[getArg('--aspect', '16:9')] || '16:9',
    style: getArg('--style', 'academic'),
    output: getArg('--output', 'assets/images/generated'),
    alt: getArg('--alt') || undefined,
  };
}

/**
 * Generate filename from prompt
 */
function generateFilename(prompt: string): string {
  // Convert to kebab-case
  return prompt
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, '')
    .trim()
    .replace(/\s+/g, '-')
    .substring(0, 60); // Limit length
}

/**
 * Insert image into QMD file
 */
async function insertImageIntoFile(
  filePath: string,
  imagePath: string,
  altText: string
): Promise<void> {
  if (!existsSync(filePath)) {
    console.error(`ERROR: File not found: ${filePath}`);
    return;
  }

  const content = await fs.readFile(filePath, 'utf-8');
  const { data: frontmatter, content: body } = matter(content);

  // Create relative path from file to image
  const fileDir = path.dirname(filePath);
  const projectRoot = process.cwd();
  const relativeImagePath = path.relative(fileDir, path.join(projectRoot, imagePath)).replace(/\\/g, '/');

  // Create markdown image reference
  const imageMarkdown = `![${altText}](${relativeImagePath})`;

  // Append to end of file (before any final newlines)
  const updatedBody = body.trimEnd() + '\n\n' + imageMarkdown + '\n';

  // Reconstruct file with frontmatter
  const updatedContent = matter.stringify(updatedBody, frontmatter);

  await fs.writeFile(filePath, updatedContent, 'utf-8');
  console.log(`✓ Image inserted into ${filePath}`);
}

/**
 * Main image generation function
 */
async function generateImage(options: GenerateImageOptions): Promise<void> {
  console.log('\n🎨 Generating Image');
  console.log('='.repeat(60));
  console.log(`Prompt: ${options.prompt}`);
  console.log(`Type: ${options.type}`);
  console.log(`Aspect: ${options.aspect}`);
  console.log(`Style: ${options.style}`);
  console.log('='.repeat(60) + '\n');

  // Check for API key
  if (!process.env.GOOGLE_GENERATIVE_AI_API_KEY) {
    console.error('ERROR: GOOGLE_GENERATIVE_AI_API_KEY environment variable is not set');
    console.error('Get your API key from: https://aistudio.google.com/app/apikey');
    process.exit(1);
  }

  // Build full prompt with style and type
  const imageTypeConfig = ImageTypes[options.type];
  const visualStyle = VisualStyles[options.style as keyof typeof VisualStyles] || VisualStyles.academic;

  const fullPrompt = `${imageTypeConfig.promptPrefix} ${options.prompt}

Style: ${visualStyle.style}

Requirements:
- Clear, professional academic visualization
- High contrast for readability
- Suitable for research publication
- No unnecessary decoration
- Focus on clarity and information density`;

  // Generate filename
  const filename = generateFilename(options.prompt);
  const filePrefix = `${filename}-${options.type}`;

  // Ensure output directory exists
  await fs.mkdir(options.output, { recursive: true });

  console.log(`Generating image...`);

  // Generate image
  const generatedFiles = await generateAndSaveImages({
    prompt: fullPrompt,
    aspectRatio: options.aspect,
    outputDir: options.output,
    filePrefix,
  });

  if (!generatedFiles || generatedFiles.length === 0) {
    console.error('\n❌ Image generation failed');
    process.exit(1);
  }

  const imagePath = generatedFiles[0];
  const relativeImagePath = path.relative(process.cwd(), imagePath).replace(/\\/g, '/');

  console.log(`\n✅ Image generated successfully!`);
  console.log(`📁 Path: ${relativeImagePath}`);

  // Auto-insert if file specified
  if (options.file) {
    const altText = options.alt || options.prompt;
    await insertImageIntoFile(options.file, relativeImagePath, altText);
  } else {
    // Print markdown for manual insertion
    const altText = options.alt || options.prompt;
    console.log(`\n📋 Markdown (copy to insert):`);
    console.log(`![${altText}](/${relativeImagePath})`);
  }

  console.log('\n' + '='.repeat(60));
}

/**
 * Main entry point
 */
async function main() {
  try {
    const options = parseArgs();
    await generateImage(options);
    process.exit(0);
  } catch (error) {
    console.error('\n❌ Error:', error);
    process.exit(1);
  }
}

main();
