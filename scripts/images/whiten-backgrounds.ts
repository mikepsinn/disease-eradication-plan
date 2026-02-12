#!/usr/bin/env tsx
/**
 * Whiten Backgrounds - Make image backgrounds white using Gemini image editing
 *
 * Sends each image to Gemini with an edit prompt to make the background white,
 * preserving the foreground content. Skips images already on white backgrounds.
 *
 * Usage:
 *   npx tsx scripts/images/whiten-backgrounds.ts              # Fix all images
 *   npx tsx scripts/images/whiten-backgrounds.ts --dry-run    # Preview without fixing
 *   npx tsx scripts/images/whiten-backgrounds.ts --limit 5    # Fix only 5 images
 *   npx tsx scripts/images/whiten-backgrounds.ts --path assets/images/ch-01
 *   npx tsx scripts/images/whiten-backgrounds.ts --force      # Re-process already-whitened images
 */

import fs from 'fs/promises'
import path from 'path'
import { findImages, getMimeType } from '../lib/image-file-utils'
import { readImageMetadata, writeImageMetadata } from '../lib/exiftool-utils'
import { editImage, saveImage, GeneratedImage, ImageMetadata } from '../lib/gemini-images'
import { updateImageInIndex, processImage, loadIndex } from './generate-image-index'
import { isExiftoolAvailable } from '../lib/exiftool-utils'
import { parseCommonArgs, hasFlag, printHeader, printSummary } from '../lib/cli-utils'

const ASSETS_DIR = path.join(process.cwd(), 'assets', 'images')
const MAX_ATTEMPTS = 2

const WHITEN_PROMPT = `Change the background of this image to pure white (#FFFFFF). Keep all foreground content, text, illustrations, diagrams, and objects exactly the same. Only replace the background color/texture with solid white. Do not alter any non-background elements.`

/**
 * Check if an image has already been whitened (marked in metadata)
 */
async function isAlreadyWhitened(filepath: string): Promise<boolean> {
  const metadata = await readImageMetadata(filepath)
  if (!metadata) return false
  const prompt = metadata.generationPrompt || ''
  return prompt.includes('[WHITENED]')
}

/**
 * Find images that need whitening
 */
async function findImagesToWhiten(
  targetDir: string,
  limit?: number,
  force?: boolean
): Promise<string[]> {
  console.log('\nScanning for images to whiten...')

  const images = await findImages(targetDir)
  console.log(`Found ${images.length} images total`)

  if (force) {
    const result = limit ? images.slice(0, limit) : images
    console.log(`Force mode: will process ${result.length} images`)
    return result
  }

  const toProcess: string[] = []
  let scanned = 0

  for (const imagePath of images) {
    if (limit && toProcess.length >= limit) break
    scanned++

    if (await isAlreadyWhitened(imagePath)) continue
    toProcess.push(imagePath)

    if (scanned % 50 === 0) {
      process.stdout.write(`  Scanned ${scanned}/${images.length}...\r`)
    }
  }

  console.log(`\nFound ${toProcess.length} images to whiten (${images.length - toProcess.length} already done)`)
  return toProcess
}

/**
 * Whiten a single image's background
 */
async function whitenImage(
  filepath: string
): Promise<'success' | 'policy_blocked' | 'failed'> {
  const imageBuffer = await fs.readFile(filepath)
  const base64Image = imageBuffer.toString('base64')
  const mimeType = getMimeType(filepath)

  for (let attempt = 1; attempt <= MAX_ATTEMPTS; attempt++) {
    console.log(`  Attempt ${attempt}/${MAX_ATTEMPTS}...`)

    const result = await editImage(base64Image, mimeType, WHITEN_PROMPT)

    if (result.result === 'policy_blocked') {
      console.log(`  [BLOCKED] Content policy: ${result.error}`)
      return 'policy_blocked'
    }

    if (result.result !== 'success' || !result.imageBytes) {
      console.log(`  [ERROR] Gemini returned no image (${result.result})`)
      if (attempt < MAX_ATTEMPTS) continue
      return 'failed'
    }

    // Preserve existing metadata
    const originalMetadata = await readImageMetadata(filepath)
    const index = await loadIndex()
    const relativePath = path.relative(process.cwd(), filepath).replace(/\\/g, '/')
    const indexEntry = index?.images.find(img => img.path === relativePath)

    const metadata: ImageMetadata = {
      ...(indexEntry || {}),
      ...(originalMetadata || {}),
      title: originalMetadata?.title || indexEntry?.title || path.basename(filepath),
      description: originalMetadata?.description || indexEntry?.description || '',
      keywords: originalMetadata?.keywords || indexEntry?.keywords || [],
    }

    const generatedImage: GeneratedImage = {
      imageBytes: result.imageBytes,
    }

    await saveImage(
      generatedImage,
      filepath,
      metadata,
      `[WHITENED] ${originalMetadata?.generationPrompt || 'background made white'}`,
      { skipWatermark: false }
    )

    // Update image index
    const useExiftool = await isExiftoolAvailable()
    const fullMetadata = await processImage(filepath, useExiftool)
    await updateImageInIndex(filepath, fullMetadata)

    return 'success'
  }

  return 'failed'
}

async function main() {
  const args = process.argv.slice(2)
  const options = parseCommonArgs(args)

  printHeader('Whiten Image Backgrounds')
  console.log(`Mode: ${options.dryRun ? 'DRY RUN' : 'WHITEN'}`)
  if (options.limit) console.log(`Limit: ${options.limit}`)
  if (options.force) console.log(`Force: re-processing already-whitened images`)

  const targetDir = options.path ? path.resolve(options.path) : ASSETS_DIR

  const images = await findImagesToWhiten(targetDir, options.limit, options.force)

  if (images.length === 0) {
    console.log('\nNo images need whitening.')
    process.exit(0)
  }

  // Display what will be processed
  console.log('\n' + '='.repeat(60))
  console.log('IMAGES TO WHITEN')
  console.log('='.repeat(60))

  for (const img of images) {
    console.log(`  ${path.relative(process.cwd(), img)}`)
  }

  if (options.dryRun) {
    console.log('\n' + '='.repeat(60))
    console.log(`[DRY RUN] Would whiten ${images.length} images.`)
    process.exit(0)
  }

  // Process images
  console.log('\n' + '='.repeat(60))
  console.log('WHITENING')
  console.log('='.repeat(60))

  let success = 0
  let failed = 0
  let policyBlocked = 0

  for (let i = 0; i < images.length; i++) {
    const filepath = images[i]
    console.log(`\n[${i + 1}/${images.length}] ${path.relative(process.cwd(), filepath)}`)

    const result = await whitenImage(filepath)

    if (result === 'success') {
      console.log(`  [OK] Background whitened`)
      success++
    } else if (result === 'policy_blocked') {
      console.log(`  [BLOCKED] Content policy - manual fix needed`)
      policyBlocked++
    } else {
      console.log(`  [FAILED]`)
      failed++
    }

    // Rate limiting between images
    await new Promise(resolve => setTimeout(resolve, 2000))
  }

  printSummary({
    'Whitened': success,
    'Policy blocked': policyBlocked,
    'Failed': failed,
  })

  if (failed > 0 || policyBlocked > 0) {
    process.exit(1)
  }
}

main().catch(error => {
  console.error('Fatal error:', error)
  process.exit(1)
})
