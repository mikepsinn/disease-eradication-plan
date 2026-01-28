#!/usr/bin/env tsx
/**
 * Fix Image Issues - Automatically fix prompt leakage and figure numbers
 *
 * Finds images with prompt leakage (style words, "Figure 1", database text, etc.)
 * and sends them to Gemini for repair. Verifies fix worked, retries if needed.
 *
 * Usage:
 *   npx tsx scripts/images/fix-image-issues.ts              # Fix all issues
 *   npx tsx scripts/images/fix-image-issues.ts --dry-run    # Preview without fixing
 *   npx tsx scripts/images/fix-image-issues.ts --limit 5    # Fix only 5 images
 *   npx tsx scripts/images/fix-image-issues.ts --no-verify  # Skip post-fix verification
 */

import fs from 'fs/promises'
import path from 'path'
import { genAI, GEMINI_IMAGE_MODEL_ID } from '../lib/llm'
import { findImages, getMimeType } from '../lib/image-file-utils'
import { readImageMetadata, writeImageMetadata } from '../lib/exiftool-utils'
import { saveImage, generateImages, GeneratedImage, ImageMetadata } from '../lib/gemini-images'
import { generateCompleteMetadata } from '../lib/image-analysis'
import { updateImageInIndex, processImage, loadIndex } from './generate-image-index'
import { isExiftoolAvailable } from '../lib/exiftool-utils'
import { parseCommonArgs, hasFlag, printHeader, printSummary } from '../lib/cli-utils'

const ASSETS_DIR = path.join(process.cwd(), 'assets', 'images')
const MAX_FIX_ATTEMPTS = 2

interface ImageIssue {
  filepath: string
  relativePath: string
  imageProblems: string[]  // Problems to fix (leakage, figure numbers)
  repairPrompt: string
}

/**
 * Keywords that indicate prompt leakage or meta-artifacts (case-insensitive)
 */
const LEAKAGE_KEYWORDS = [
  'prompt leakage',
  'scientific illustration',
  'scientific diagram',
  'scientific database',
  'retro',
  'vintage',
  'academic',
  'visualization',
  'infographic',
  'high contrast',
  'minimalist',
  'aspect ratio',
  'circa',
  'confidential',
  'draft',
  'sample',
  'database',
  'volume',
  'figure 1',
  'figure 2',
  'fig. 1',
  'fig. 2',
  'fig 1',
  'fig 2',
]

/**
 * Check if a problem description indicates prompt leakage or figure numbers
 */
function isLeakageOrFigureProblem(problem: string): boolean {
  const lowerProblem = problem.toLowerCase()
  return LEAKAGE_KEYWORDS.some(keyword => lowerProblem.includes(keyword))
}

/**
 * Find images with prompt leakage or figure numbers (NOT typos or quality issues)
 */
async function findImagesWithIssues(
  targetDir: string,
  limit?: number
): Promise<ImageIssue[]> {
  console.log('\nScanning for prompt leakage and figure numbers...')

  const images = await findImages(targetDir)
  console.log(`Found ${images.length} images to scan`)

  const issues: ImageIssue[] = []
  let scanned = 0

  for (const imagePath of images) {
    if (limit && issues.length >= limit) break
    scanned++

    const metadata = await readImageMetadata(imagePath)
    if (!metadata) continue

    // Only fix images with detected problems (leakage, figure numbers)
    if (metadata.imageProblemsDetected && metadata.imageProblems?.length && metadata.imageProblemsRepairPrompt) {
      // Filter to only leakage/figure problems (ignore typos from old metadata)
      const relevantProblems = metadata.imageProblems.filter(isLeakageOrFigureProblem)

      if (relevantProblems.length > 0) {
        issues.push({
          filepath: imagePath,
          relativePath: path.relative(process.cwd(), imagePath),
          imageProblems: relevantProblems,
          repairPrompt: metadata.imageProblemsRepairPrompt,
        })
      }
    }

    if (scanned % 50 === 0) {
      process.stdout.write(`  Scanned ${scanned}/${images.length}...\r`)
    }
  }

  console.log(`\nFound ${issues.length} images with problems`)
  return issues
}

/**
 * Edit an image using Gemini to fix all issues in one pass
 */
async function editImageWithGemini(
  filepath: string,
  editPrompt: string
): Promise<boolean> {
  const imageBuffer = await fs.readFile(filepath)
  const base64Image = imageBuffer.toString('base64')
  const mimeType = getMimeType(filepath)

  // Wrap repair prompt with context (same format as edit-image.ts)
  const fullPrompt = `Edit this image according to these instructions: ${editPrompt}

Keep everything else exactly the same - preserve the overall style, colors, layout, and any elements not mentioned in the instructions. Make ONLY the changes requested.`

  const response = await genAI.models.generateContent({
    model: GEMINI_IMAGE_MODEL_ID,
    contents: [
      {
        parts: [
          { text: fullPrompt },
          {
            inlineData: {
              mimeType,
              data: base64Image,
            },
          },
        ],
      },
    ],
  })

  if (response.candidates && response.candidates.length > 0) {
    const candidate = response.candidates[0]
    const parts = candidate.content?.parts || []

    for (const part of parts) {
      if (part.inlineData?.data) {
        // IMPORTANT: Preserve ALL existing metadata, not just title/description/keywords
        // This includes enriched fields like qualityScore, socialCaption, speakerNotes, etc.
        const originalMetadata = await readImageMetadata(filepath)

        // Also get existing metadata from image-index.json as backup
        // (in case EXIF doesn't have all fields)
        const index = await loadIndex()
        const relativePath = path.relative(process.cwd(), filepath).replace(/\\/g, '/')
        const indexEntry = index?.images.find(img => img.path === relativePath)

        // Merge: index entry (most complete) + EXIF metadata + minimal defaults
        const metadata: ImageMetadata = {
          ...(indexEntry || {}),           // Preserve all fields from index
          ...(originalMetadata || {}),     // Overlay with EXIF (may have newer values)
          title: originalMetadata?.title || indexEntry?.title || path.basename(filepath),
          description: originalMetadata?.description || indexEntry?.description || '',
          keywords: originalMetadata?.keywords || indexEntry?.keywords || [],
        }

        const generatedImage: GeneratedImage = {
          imageBytes: part.inlineData.data,
        }

        await saveImage(generatedImage, filepath, metadata, `[FIXED] ${editPrompt}`, { skipWatermark: false })
        return true
      }
    }
  }

  return false
}

/**
 * Regenerate an image from scratch using the original prompt
 * Used as fallback when editing fails
 */
async function regenerateImage(
  filepath: string,
  problems: string[]
): Promise<boolean> {
  // Get original metadata to find the generation prompt
  const originalMetadata = await readImageMetadata(filepath)
  const index = await loadIndex()
  const relativePath = path.relative(process.cwd(), filepath).replace(/\\/g, '/')
  const indexEntry = index?.images.find(img => img.path === relativePath)

  // Find a prompt to use for regeneration
  const originalPrompt = originalMetadata?.generationPrompt || indexEntry?.generationPrompt
  const inferredPrompt = originalMetadata?.inferredPrompt || indexEntry?.inferredPrompt

  if (!originalPrompt && !inferredPrompt) {
    console.log(`  [REGEN] No original or inferred prompt found - cannot regenerate`)
    return false
  }

  // Use original prompt if available, otherwise use inferred
  let basePrompt = originalPrompt || inferredPrompt || ''

  // Remove [FIXED] or [EDITED] prefixes from previous fix attempts
  basePrompt = basePrompt.replace(/^\[(FIXED|EDITED)\]\s*/i, '')

  // Build a negative prompt based on the problems
  const negativeTerms: string[] = []
  for (const problem of problems) {
    const lower = problem.toLowerCase()
    if (lower.includes('figure 1') || lower.includes('fig. 1') || lower.includes('fig 1')) {
      negativeTerms.push('figure numbers', 'Figure 1', 'Fig. 1')
    }
    if (lower.includes('scientific illustration')) {
      negativeTerms.push('scientific illustration text', 'SCIENTIFIC ILLUSTRATION label')
    }
    if (lower.includes('scientific diagram')) {
      negativeTerms.push('scientific diagram text', 'SCIENTIFIC DIAGRAM label')
    }
    if (lower.includes('circa')) {
      negativeTerms.push('circa dates', 'Circa 2024')
    }
    if (lower.includes('database') || lower.includes('volume')) {
      negativeTerms.push('database labels', 'volume numbers')
    }
    if (lower.includes('confidential')) {
      negativeTerms.push('confidential labels', 'CONFIDENTIAL text')
    }
  }

  const negativePrompt = negativeTerms.length > 0
    ? negativeTerms.join(', ')
    : 'figure numbers, scientific illustration labels, database text, meta-labels'

  // Add explicit instruction to avoid the problematic elements
  const cleanPrompt = `${basePrompt}

IMPORTANT: Do NOT include any of the following in the image:
- Figure numbers (Figure 1, Fig. 1, etc.)
- Labels like "SCIENTIFIC ILLUSTRATION" or "SCIENTIFIC DIAGRAM"
- Meta-text like "CIRCA 2024", "DATABASE", "VOLUME"
- Any text that describes what the image IS rather than what it SHOWS`

  console.log(`  [REGEN] Regenerating with original prompt...`)

  try {
    const result = await generateImages({
      prompt: cleanPrompt,
      count: 1,
      aspectRatio: '1:1',
      negativePrompt,
    })

    if (result.images.length === 0 || !result.images[0].imageBytes) {
      console.log(`  [REGEN] No image generated`)
      return false
    }

    // Preserve existing metadata
    const metadata: ImageMetadata = {
      ...(indexEntry || {}),
      ...(originalMetadata || {}),
      title: originalMetadata?.title || indexEntry?.title || path.basename(filepath),
      description: originalMetadata?.description || indexEntry?.description || '',
      keywords: originalMetadata?.keywords || indexEntry?.keywords || [],
    }

    await saveImage(
      result.images[0],
      filepath,
      metadata,
      `[REGENERATED] ${basePrompt.substring(0, 200)}...`,
      { skipWatermark: false }
    )

    return true
  } catch (error: any) {
    console.log(`  [REGEN] Error: ${error.message}`)
    return false
  }
}

/**
 * Fix an image and verify the fix worked
 */
async function fixImage(issue: ImageIssue, verify: boolean): Promise<'fixed' | 'failed' | 'still_broken' | 'regenerated'> {
  console.log(`  Problems: ${issue.imageProblems.join(', ')}`)
  console.log(`  Repair: ${issue.repairPrompt}`)

  // Attempt fix
  for (let attempt = 1; attempt <= MAX_FIX_ATTEMPTS; attempt++) {
    console.log(`  Attempt ${attempt}/${MAX_FIX_ATTEMPTS}...`)

    const edited = await editImageWithGemini(issue.filepath, issue.repairPrompt)
    if (!edited) {
      console.log(`  [ERROR] Gemini returned no image`)
      continue
    }

    // Skip verification if disabled
    if (!verify) {
      const clearedMetadata = {
        imageProblemsDetected: false,
        imageProblems: [],
        imageProblemsRepairPrompt: '',
      }
      await writeImageMetadata(issue.filepath, clearedMetadata)

      // Update image index with fresh file stats + EXIF metadata
      const useExiftool = await isExiftoolAvailable()
      const fullMetadata = await processImage(issue.filepath, useExiftool)
      await updateImageInIndex(issue.filepath, fullMetadata)
      return 'fixed'
    }

    // Verify fix by re-analyzing
    console.log(`  Verifying fix...`)
    await new Promise(resolve => setTimeout(resolve, 1000)) // Rate limit

    const newMetadata = await generateCompleteMetadata(issue.filepath)

    // Check if problems are fixed
    if (newMetadata.imageProblemsDetected && newMetadata.imageProblems?.length) {
      console.log(`  [!] Still has problems: ${newMetadata.imageProblems.join(', ')}`)
      if (attempt < MAX_FIX_ATTEMPTS) {
        console.log(`  Retrying...`)
        continue
      }
      return 'still_broken'
    }

    // Update metadata with new analysis
    const clearedMetadata = {
      ...newMetadata,
      imageProblemsDetected: false,
      imageProblems: [],
      imageProblemsRepairPrompt: '',
    }
    await writeImageMetadata(issue.filepath, clearedMetadata)

    // Update image index with fresh file stats + EXIF metadata
    const useExiftool = await isExiftoolAvailable()
    const fullMetadata = await processImage(issue.filepath, useExiftool)
    await updateImageInIndex(issue.filepath, fullMetadata)

    return 'fixed'
  }

  // Editing failed - try regeneration as fallback
  console.log(`  [FALLBACK] Editing failed, attempting regeneration...`)
  const regenerated = await regenerateImage(issue.filepath, issue.imageProblems)

  if (regenerated) {
    // Clear problem flags and update index
    const clearedMetadata = {
      imageProblemsDetected: false,
      imageProblems: [],
      imageProblemsRepairPrompt: '',
    }
    await writeImageMetadata(issue.filepath, clearedMetadata)

    const useExiftool = await isExiftoolAvailable()
    const fullMetadata = await processImage(issue.filepath, useExiftool)
    await updateImageInIndex(issue.filepath, fullMetadata)

    return 'regenerated'
  }

  return 'failed'
}

async function main() {
  const args = process.argv.slice(2)
  const options = parseCommonArgs(args)
  const skipVerify = hasFlag(args, 'no-verify')

  printHeader('Fix Image Issues (Leakage & Figure Numbers)')
  console.log(`Mode: ${options.dryRun ? 'DRY RUN' : 'FIX'}`)
  console.log(`Verify fixes: ${!skipVerify}`)
  if (options.limit) console.log(`Limit: ${options.limit}`)

  const targetDir = options.path ? path.resolve(options.path) : ASSETS_DIR

  // Find images with issues
  const issues = await findImagesWithIssues(targetDir, options.limit)

  if (issues.length === 0) {
    console.log('\nNo images with prompt leakage or figure numbers found.')
    console.log('Run "npm run images:enrich" first to detect issues.')
    process.exit(0)
  }

  // Display issues
  console.log('\n' + '='.repeat(60))
  console.log('IMAGES TO FIX')
  console.log('='.repeat(60))

  for (const issue of issues) {
    console.log(`\n${issue.relativePath}`)
    console.log(`  ${issue.imageProblems.join(', ')}`)
  }

  if (options.dryRun) {
    console.log('\n' + '='.repeat(60))
    console.log(`[DRY RUN] Would fix ${issues.length} images.`)
    process.exit(0)
  }

  // Process images
  console.log('\n' + '='.repeat(60))
  console.log('FIXING')
  console.log('='.repeat(60))

  let fixed = 0
  let regenerated = 0
  let failed = 0
  let stillBroken = 0

  for (let i = 0; i < issues.length; i++) {
    const issue = issues[i]
    console.log(`\n[${i + 1}/${issues.length}] ${issue.relativePath}`)

    const result = await fixImage(issue, !skipVerify)

    if (result === 'fixed') {
      console.log(`  [OK] Fixed (edited)`)
      fixed++
    } else if (result === 'regenerated') {
      console.log(`  [OK] Fixed (regenerated)`)
      regenerated++
    } else if (result === 'still_broken') {
      console.log(`  [STILL BROKEN] Manual intervention needed`)
      stillBroken++
    } else {
      console.log(`  [FAILED]`)
      failed++
    }

    // Rate limiting between images
    await new Promise(resolve => setTimeout(resolve, 2000))
  }

  printSummary({
    'Fixed (edited)': fixed,
    'Fixed (regenerated)': regenerated,
    'Still broken': stillBroken,
    'Failed': failed,
  })

  if (stillBroken > 0) {
    process.exit(1)
  }
}

main().catch(error => {
  console.error('Fatal error:', error)
  process.exit(1)
})
