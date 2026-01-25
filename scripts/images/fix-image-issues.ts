#!/usr/bin/env tsx
/**
 * Fix Prompt Leakage - Automatically fix all images with detected issues
 *
 * Finds images with prompt leakage, figure numbers, quality issues (blurry text, etc.)
 * and sends them to Gemini for repair. Verifies fix worked, fails if issues remain.
 *
 * Usage:
 *   npx tsx scripts/images/fix-prompt-leakage.ts              # Fix all issues
 *   npx tsx scripts/images/fix-prompt-leakage.ts --dry-run    # Preview without fixing
 *   npx tsx scripts/images/fix-prompt-leakage.ts --limit 5    # Fix only 5 images
 *   npx tsx scripts/images/fix-prompt-leakage.ts --no-verify  # Skip post-fix verification
 */

import fs from 'fs/promises'
import path from 'path'
import { genAI, GEMINI_IMAGE_MODEL_ID } from '../lib/llm'
import { findImages, getMimeType } from '../lib/image-file-utils'
import { readImageMetadata, writeImageMetadata } from '../lib/exiftool-utils'
import { saveImage, GeneratedImage, ImageMetadata } from '../lib/gemini-images'
import { generateCompleteMetadata } from '../lib/image-analysis'
import { parseCommonArgs, hasFlag, printHeader, printSummary } from '../lib/cli-utils'

const ASSETS_DIR = path.join(process.cwd(), 'assets', 'images')
const MAX_FIX_ATTEMPTS = 2

interface ImageIssue {
  filepath: string
  relativePath: string
  allIssues: string[]  // Combined list of all issues to fix
  imageProblems?: string[]
  qualityIssues?: string[]
  qualityScore?: number
}

/**
 * Find all images with issues (leakage, figure numbers, quality problems)
 * Combines all issues for each image into a single repair task
 */
async function findImagesWithIssues(
  targetDir: string,
  limit?: number
): Promise<ImageIssue[]> {
  console.log('\nScanning images for issues...')

  const images = await findImages(targetDir)
  console.log(`Found ${images.length} images to scan`)

  const issues: ImageIssue[] = []
  let scanned = 0

  for (const imagePath of images) {
    if (limit && issues.length >= limit) break
    scanned++

    const metadata = await readImageMetadata(imagePath)
    if (!metadata) continue

    const relativePath = path.relative(process.cwd(), imagePath)
    const allIssues: string[] = []

    // Collect image problems (leakage, figure numbers, etc.)
    if (metadata.imageProblemsDetected && metadata.imageProblems?.length) {
      for (const problem of metadata.imageProblems) {
        allIssues.push(`Fix: ${problem}`)
      }
    }

    // Collect quality issues (blurry text, low contrast, etc.)
    if (metadata.qualityIssues?.length && metadata.qualityScore && metadata.qualityScore < 4) {
      for (const issue of metadata.qualityIssues) {
        allIssues.push(`Fix: ${issue}`)
      }
    }

    // If any issues found, add to list
    if (allIssues.length > 0) {
      issues.push({
        filepath: imagePath,
        relativePath,
        allIssues,
        imageProblems: metadata.imageProblems,
        qualityIssues: metadata.qualityIssues,
        qualityScore: metadata.qualityScore,
      })
    }

    if (scanned % 50 === 0) {
      process.stdout.write(`  Scanned ${scanned}/${images.length}...\r`)
    }
  }

  console.log(`\nFound ${issues.length} images with issues`)
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

  const response = await genAI.models.generateContent({
    model: GEMINI_IMAGE_MODEL_ID,
    contents: [
      {
        parts: [
          { text: editPrompt },
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
        const originalMetadata = await readImageMetadata(filepath)

        const metadata: ImageMetadata = {
          title: originalMetadata?.title || path.basename(filepath),
          description: originalMetadata?.description || '',
          keywords: originalMetadata?.keywords || [],
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
 * Fix an image and verify the fix worked
 */
async function fixImage(issue: ImageIssue, verify: boolean): Promise<'fixed' | 'failed' | 'still_broken'> {
  // Create backup (only once)
  const backupPath = issue.filepath + '.backup'
  const backupExists = await fs.access(backupPath).then(() => true).catch(() => false)
  if (!backupExists) {
    await fs.copyFile(issue.filepath, backupPath)
    console.log(`  Backup: ${path.basename(backupPath)}`)
  }

  // Build combined repair prompt
  const editPrompt = `Fix ALL of these issues in this image while preserving the overall style, colors, and layout:\n\n${issue.allIssues.map((i, idx) => `${idx + 1}. ${i}`).join('\n')}\n\nKeep everything else exactly the same.`

  console.log(`  Repair prompt: ${issue.allIssues.length} issues`)
  for (const iss of issue.allIssues) {
    console.log(`    - ${iss}`)
  }

  // Attempt fix
  for (let attempt = 1; attempt <= MAX_FIX_ATTEMPTS; attempt++) {
    console.log(`  Attempt ${attempt}/${MAX_FIX_ATTEMPTS}...`)

    const edited = await editImageWithGemini(issue.filepath, editPrompt)
    if (!edited) {
      console.log(`  [ERROR] Gemini returned no image`)
      continue
    }

    // Skip verification if disabled
    if (!verify) {
      // Clear metadata flags
      await writeImageMetadata(issue.filepath, {
        imageProblemsDetected: false,
        imageProblems: [],
        imageProblemsRepairPrompt: '',
        qualityIssues: [],
      })
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

    // Check if quality improved
    if (newMetadata.qualityScore && issue.qualityScore && newMetadata.qualityScore < issue.qualityScore) {
      console.log(`  [!] Quality got worse: ${issue.qualityScore} -> ${newMetadata.qualityScore}`)
      // Restore backup
      await fs.copyFile(backupPath, issue.filepath)
      if (attempt < MAX_FIX_ATTEMPTS) {
        console.log(`  Restored backup, retrying...`)
        continue
      }
      return 'still_broken'
    }

    // Update metadata with new analysis
    await writeImageMetadata(issue.filepath, {
      ...newMetadata,
      imageProblemsDetected: false,
      imageProblems: [],
      imageProblemsRepairPrompt: '',
    })

    return 'fixed'
  }

  return 'failed'
}

async function main() {
  const args = process.argv.slice(2)
  const options = parseCommonArgs(args)
  const skipVerify = hasFlag(args, 'no-verify')

  printHeader('Fix Image Issues (Leakage + Quality)')
  console.log(`Mode: ${options.dryRun ? 'DRY RUN' : 'FIX'}`)
  console.log(`Verify fixes: ${!skipVerify}`)
  if (options.limit) console.log(`Limit: ${options.limit}`)

  const targetDir = options.path ? path.resolve(options.path) : ASSETS_DIR

  // Find images with issues
  const issues = await findImagesWithIssues(targetDir, options.limit)

  if (issues.length === 0) {
    console.log('\nNo images with issues found.')
    console.log('Run "npm run images:enrich" first to detect issues.')
    process.exit(0)
  }

  // Display issues
  console.log('\n' + '='.repeat(60))
  console.log('IMAGES WITH ISSUES')
  console.log('='.repeat(60))

  for (const issue of issues) {
    console.log(`\n${issue.relativePath}`)
    if (issue.imageProblems?.length) {
      console.log(`  Problems: ${issue.imageProblems.join(', ')}`)
    }
    if (issue.qualityScore && issue.qualityScore < 4) {
      console.log(`  Quality: ${issue.qualityScore}/5 - ${issue.qualityIssues?.join(', ')}`)
    }
    console.log(`  Total issues: ${issue.allIssues.length}`)
  }

  if (options.dryRun) {
    console.log('\n' + '='.repeat(60))
    console.log('[DRY RUN] No images were modified.')
    console.log(`Would fix ${issues.length} images with ${issues.reduce((sum, i) => sum + i.allIssues.length, 0)} total issues.`)
    process.exit(0)
  }

  // Process images
  console.log('\n' + '='.repeat(60))
  console.log('FIXING IMAGES')
  console.log('='.repeat(60))

  let fixed = 0
  let failed = 0
  let stillBroken = 0

  for (let i = 0; i < issues.length; i++) {
    const issue = issues[i]
    console.log(`\n[${i + 1}/${issues.length}] ${issue.relativePath}`)

    const result = await fixImage(issue, !skipVerify)

    if (result === 'fixed') {
      console.log(`  [OK] Fixed and verified`)
      fixed++
    } else if (result === 'still_broken') {
      console.log(`  [STILL BROKEN] Issues remain after ${MAX_FIX_ATTEMPTS} attempts`)
      stillBroken++
    } else {
      console.log(`  [FAILED] Could not generate fix`)
      failed++
    }

    // Rate limiting between images
    await new Promise(resolve => setTimeout(resolve, 2000))
  }

  printSummary({
    'Total images': issues.length,
    'Fixed & verified': fixed,
    'Still broken': stillBroken,
    'Failed': failed,
  })

  if (stillBroken > 0) {
    console.log(`\n[!] ${stillBroken} images still have issues after fixing.`)
    console.log('These may need manual regeneration or different prompts.')
    process.exit(1)
  }

  console.log('\nBackups saved with .backup extension')
}

main().catch(error => {
  console.error('Fatal error:', error)
  process.exit(1)
})
