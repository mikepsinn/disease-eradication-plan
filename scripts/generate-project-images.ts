/**
 * Generate OG images for book chapters
 */

import dotenv from 'dotenv';
import path from 'path';
import fs from 'fs/promises';
import matter from 'gray-matter';
import { generateAndSaveImages } from './lib/genai-image.js';
import { getBookFilesForProcessing, stringifyWithFrontmatter } from './lib/file-utils.js';

// Load environment variables
dotenv.config();

/**
 * Generate OG image for a single file
 */
async function generateImageForFile(filePath: string): Promise<void> {
  console.log(`\n[*] Processing: ${filePath}`);

  const fileName = path.basename(filePath, '.qmd');

  // Read file with frontmatter
  const fileContent = await fs.readFile(filePath, 'utf-8');
  const { data: frontmatter, content: body } = matter(fileContent);

  // Skip if already has an image
  if (frontmatter.image) {
    console.log(`[SKIP] Already has image: ${frontmatter.image}`);
    return;
  }

  // Skip if no title or description
  if (!frontmatter.title && !frontmatter.description) {
    console.log(`[SKIP] No title or description for prompt generation`);
    return;
  }

  console.log(`  Title: ${frontmatter.title || '(no title)'}`);
  console.log(`  Description: ${frontmatter.description || '(no description)'}`);

  // Generate simple prompt with file content
  const prompt = `Please generate an infographic for the following content.
  Use a fun retro futuristic style with vibrant colors and bold shapes.
   Use a size typical for Open Graph (OG) images for social media sharing.

---
${fileContent}
---`;

  // Determine output directory and filename
  const relativePath = path.relative(process.cwd(), filePath);
  const outputDir = path.join(process.cwd(), 'assets', 'og-images', path.dirname(relativePath));
  const filePrefix = fileName;

  console.log(`  Generating OG image...`);

  // Generate the image
  const generatedFiles = await generateAndSaveImages({
    prompt,
    aspectRatio: '16:9',
    outputDir,
    filePrefix,
  });

  if (generatedFiles && generatedFiles.length > 0) {
    // Get the relative path for the image (relative to project root)
    const imagePath = path.relative(process.cwd(), generatedFiles[0]).replace(/\\/g, '/');

    console.log(`  [OK] Generated image: ${imagePath}`);

    // Update frontmatter with image path
    const updatedFrontmatter = {
      ...frontmatter,
      image: `/${imagePath}`
    };

    // Write updated file
    const updatedContent = stringifyWithFrontmatter(body, updatedFrontmatter);
    await fs.writeFile(filePath, updatedContent, 'utf-8');

    console.log(`  [OK] Updated frontmatter in ${filePath}`);
  } else {
    console.log(`  [WARN] No image files generated`);
    throw new Error('Image generation failed');
  }
}

/**
 * Generate OG images for book chapters
 */
async function generateBookChapterImages(fileFilter?: string): Promise<void> {
  console.log('\n' + '='.repeat(60));
  console.log('Generating OG images for book chapters');
  console.log('='.repeat(60) + '\n');

  // Get all book files
  console.log('[*] Loading book files...');
  const allBookFiles = await getBookFilesForProcessing();

  // Filter to specific file if provided
  let bookFiles: string[];
  if (fileFilter) {
    bookFiles = allBookFiles.filter(f => f.includes(fileFilter));
    if (bookFiles.length === 0) {
      console.error(`ERROR: No files found matching "${fileFilter}"`);
      console.error('\nAvailable files:');
      allBookFiles.slice(0, 10).forEach(f => console.error(`  - ${f}`));
      if (allBookFiles.length > 10) {
        console.error(`  ... and ${allBookFiles.length - 10} more`);
      }
      process.exit(1);
    }
    console.log(`[OK] Found ${bookFiles.length} file(s) matching "${fileFilter}"\n`);
  } else {
    bookFiles = allBookFiles;
    console.log(`[OK] Found ${bookFiles.length} book files\n`);
  }

  let filesProcessed = 0;
  let filesSkipped = 0;
  let filesGenerated = 0;
  let filesFailed = 0;

  for (const filePath of bookFiles) {
    try {
      filesProcessed++;
      await generateImageForFile(filePath);
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

  // Check for API key
  if (!process.env.GOOGLE_GENERATIVE_AI_API_KEY) {
    console.error('ERROR: GOOGLE_GENERATIVE_AI_API_KEY environment variable is not set');
    console.error('Please set your Google Gemini API key in .env file:');
    console.error('GOOGLE_GENERATIVE_AI_API_KEY=your_api_key_here');
    console.error('Get your API key from: https://aistudio.google.com/app/apikey');
    process.exit(1);
  }

  // Parse command line arguments
  const args = process.argv.slice(2);

  // Look for --file parameter
  const fileIndex = args.indexOf('--file');
  const fileFilter = fileIndex !== -1 && args[fileIndex + 1] ? args[fileIndex + 1] : undefined;

  if (fileFilter) {
    console.log(`\nGenerating image for file matching: "${fileFilter}"\n`);
  }

  await generateBookChapterImages(fileFilter);
}

// Run the script
main().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
