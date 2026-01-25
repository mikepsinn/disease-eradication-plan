/**
 * Extract text from images using Gemini Vision API (OCR)
 *
 * Loops through all images, sends them to Gemini for text extraction,
 * and saves the transcript to image metadata.
 *
 * Usage:
 *   npx tsx scripts/images/extract-image-text.ts [image.jpg]     # Single image
 *   npx tsx scripts/images/extract-image-text.ts [options]       # Batch mode
 *
 * Single image mode:
 *   npx tsx scripts/images/extract-image-text.ts path/to/image.jpg
 *
 * Batch options:
 *   --all              Process all images (default: only those without transcript)
 *   --dry-run          Show what would be extracted without saving
 *   --limit N          Process only N images (for testing)
 *   --path <dir>       Process only images in specific directory
 */

import { existsSync } from 'fs'
import path from 'path'

// Shared utilities
import { findImages, isSupportedImage } from '../lib/image-file-utils'
import { hasTranscript, writeImageMetadata } from '../lib/exiftool-utils'
import { extractImageText } from '../lib/image-analysis'
import { parseCommonArgs, getArgValue, printHeader, printSummary } from '../lib/cli-utils'

const ASSETS_DIR = path.join(process.cwd(), 'assets', 'images')

interface ExtractionResult {
  path: string
  transcript: string
  hasText: boolean
  error?: string
}

/**
 * Process a single image and print/save the transcript
 */
async function processSingleImage(imagePath: string, dryRun: boolean): Promise<void> {
  const resolvedPath = path.resolve(imagePath)

  if (!existsSync(resolvedPath)) {
    console.error(`ERROR: File not found: ${resolvedPath}`)
    process.exit(1)
  }

  if (!isSupportedImage(resolvedPath)) {
    const ext = path.extname(resolvedPath).toLowerCase()
    console.error(`ERROR: Not a supported image format: ${ext}`)
    process.exit(1)
  }

  printHeader('Image Text Extractor (OCR) - Single Image Mode')
  console.log(`File: ${resolvedPath}`)
  console.log(`Dry run: ${dryRun}`)
  console.log('')

  console.log('Extracting text...')
  const transcript = await extractImageText(resolvedPath)
  const hasText = transcript !== '[NO TEXT]'

  console.log('\n--- EXTRACTED TEXT ---')
  console.log(transcript)
  console.log('--- END ---\n')

  if (!dryRun && hasText) {
    await writeImageMetadata(resolvedPath, {
      transcript,
      transcriptExtractedAt: new Date().toISOString(),
    })
    console.log('[OK] Transcript saved to image metadata')
  } else if (dryRun) {
    console.log('[DRY RUN] Transcript not saved')
  } else {
    console.log('[INFO] No text found in image')
  }
}

async function main() {
  const args = process.argv.slice(2)
  const options = parseCommonArgs(args)

  // Check for single image mode: first non-flag argument that looks like a file
  const firstArg = args.find(a => !a.startsWith('--'))
  if (firstArg && isSupportedImage(firstArg)) {
    await processSingleImage(firstArg, options.dryRun)
    return
  }

  // Batch mode
  const targetDir = options.path ? path.resolve(options.path) : ASSETS_DIR

  printHeader('Image Text Extractor (OCR) - Batch Mode')
  console.log(`Target directory: ${targetDir}`)
  console.log(`Process all: ${options.all}`)
  console.log(`Dry run: ${options.dryRun}`)
  if (options.limit) console.log(`Limit: ${options.limit}`)
  console.log('')

  if (!existsSync(targetDir)) {
    console.error(`ERROR: Directory not found: ${targetDir}`)
    process.exit(1)
  }

  // Find all images
  console.log('[1/3] Finding images...')
  let images = await findImages(targetDir)
  console.log(`  Found ${images.length} images`)

  // Filter to only those without transcript (unless --all)
  if (!options.all) {
    console.log('\n[2/3] Checking for existing transcripts...')
    const toProcess: string[] = []
    for (const img of images) {
      const has = await hasTranscript(img)
      if (!has) {
        toProcess.push(img)
      }
    }
    console.log(`  ${images.length - toProcess.length} already have transcripts`)
    console.log(`  ${toProcess.length} need processing`)
    images = toProcess
  }

  // Apply limit
  if (options.limit && images.length > options.limit) {
    images = images.slice(0, options.limit)
    console.log(`  Limited to ${options.limit} images`)
  }

  if (images.length === 0) {
    console.log('\nNo images to process.')
    process.exit(0)
  }

  // Process images
  console.log(`\n[3/3] Extracting text from ${images.length} images...`)
  const results: ExtractionResult[] = []
  let processed = 0
  let withText = 0

  for (const imagePath of images) {
    const relativePath = path.relative(process.cwd(), imagePath)
    processed++

    process.stdout.write(`\n[${processed}/${images.length}] ${relativePath}\n`)

    try {
      const transcript = await extractImageText(imagePath)
      const hasText = transcript !== '[NO TEXT]'

      if (hasText) withText++

      results.push({
        path: relativePath,
        transcript,
        hasText,
      })

      // Preview transcript
      const preview =
        transcript.length > 200 ? transcript.substring(0, 200) + '...' : transcript
      console.log(`  Text: ${preview.replace(/\n/g, ' | ')}`)

      // Save to metadata
      if (!options.dryRun && hasText) {
        await writeImageMetadata(imagePath, {
          transcript,
          transcriptExtractedAt: new Date().toISOString(),
        })
        console.log(`  [OK] Transcript saved to metadata`)
      }

      // Rate limiting
      await new Promise(resolve => setTimeout(resolve, 500))
    } catch (error) {
      console.error(`  [ERROR] ${error}`)
      results.push({
        path: relativePath,
        transcript: '',
        hasText: false,
        error: String(error),
      })
    }
  }

  // Summary
  printSummary({
    'Images processed': processed,
    'With text': withText,
    'Without text': processed - withText,
    Errors: results.filter(r => r.error).length,
  })

  if (options.dryRun) {
    console.log('\n[DRY RUN] No metadata was saved. Run without --dry-run to save.')
  } else {
    // Regenerate image search index to include new transcripts
    console.log('\n[4/4] Regenerating image search index...')
    const { execSync } = await import('child_process')
    execSync('npx tsx scripts/images/generate-image-index.ts', {
      cwd: process.cwd(),
      stdio: 'inherit',
    })
  }
}

main().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
