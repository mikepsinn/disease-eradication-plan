#!/usr/bin/env tsx
/**
 * Whiten Backgrounds (Sharp) - Programmatically whiten off-white/parchment backgrounds
 *
 * Uses a levels/curves approach: samples the background color from corners,
 * then applies per-channel linear scaling so the background maps to pure white.
 * This preserves anti-aliasing and text crispness because all pixels scale
 * proportionally (like adjusting the white point in Photoshop Levels).
 *
 * Skips images that already have white backgrounds.
 *
 * Usage:
 *   npx tsx scripts/images/whiten-backgrounds-sharp.ts                    # Fix all images
 *   npx tsx scripts/images/whiten-backgrounds-sharp.ts --dry-run          # Preview without fixing
 *   npx tsx scripts/images/whiten-backgrounds-sharp.ts --limit 5          # Fix only 5 images
 *   npx tsx scripts/images/whiten-backgrounds-sharp.ts --path assets/images/ch-01
 *   npx tsx scripts/images/whiten-backgrounds-sharp.ts --path assets/images/file.jpg  # Single file
 *   npx tsx scripts/images/whiten-backgrounds-sharp.ts --force            # Re-process all images
 */

import fs from 'fs/promises'
import path from 'path'
import sharp from 'sharp'
import { findImages } from '../lib/image-file-utils'
import { readImageMetadata, writeImageMetadata, isExiftoolAvailable } from '../lib/exiftool-utils'
import { updateImageInIndex, processImage } from './generate-image-index'
import { parseCommonArgs, printHeader, printSummary } from '../lib/cli-utils'

const ASSETS_DIR = path.join(process.cwd(), 'assets', 'images')
const CORNER_SAMPLE_SIZE = 20 // Pixels per side for corner sampling
const ALREADY_WHITE_THRESHOLD = 248 // Corner average above this = already white
const MIN_SCALE = 1.02 // Minimum scale factor to bother processing (avoids near-white no-ops)

interface WhitenResult {
  status: 'whitened' | 'already_white' | 'skipped' | 'error'
  bgColor?: { r: number; g: number; b: number }
  scale?: { r: number; g: number; b: number }
  error?: string
}

/**
 * Sample corner regions and return average RGB background color
 */
function sampleBackground(
  pixels: Buffer,
  width: number,
  height: number,
  channels: number
): { r: number; g: number; b: number } {
  const size = Math.min(CORNER_SAMPLE_SIZE, Math.floor(width / 4), Math.floor(height / 4))

  let totalR = 0, totalG = 0, totalB = 0, count = 0

  // Four corners
  const corners = [
    { x0: 0, y0: 0 },
    { x0: width - size, y0: 0 },
    { x0: 0, y0: height - size },
    { x0: width - size, y0: height - size },
  ]

  for (const { x0, y0 } of corners) {
    for (let y = y0; y < y0 + size; y++) {
      for (let x = x0; x < x0 + size; x++) {
        const idx = (y * width + x) * channels
        totalR += pixels[idx]
        totalG += pixels[idx + 1]
        totalB += pixels[idx + 2]
        count++
      }
    }
  }

  return {
    r: totalR / count,
    g: totalG / count,
    b: totalB / count,
  }
}

/**
 * Process a single image using per-channel linear scaling (levels adjustment).
 *
 * For each channel: output = input * (255 / bg_value), clamped to 255.
 * This maps the background color to white while preserving relative contrast
 * and anti-aliasing on text/illustration edges.
 */
async function whitenImage(filepath: string): Promise<WhitenResult> {
  const image = sharp(filepath)
  const metadata = await image.metadata()
  const { width, height, channels } = metadata

  if (!width || !height || !channels || channels < 3) {
    return { status: 'skipped', error: 'unsupported format or channels' }
  }

  // Read raw pixels to sample background
  const hasAlpha = channels === 4
  const rawBuffer = await image.ensureAlpha().raw().toBuffer()
  const rawChannels = 4

  // Detect background color from corners
  const bg = sampleBackground(rawBuffer, width, height, rawChannels)

  // Already white?
  if (
    bg.r >= ALREADY_WHITE_THRESHOLD &&
    bg.g >= ALREADY_WHITE_THRESHOLD &&
    bg.b >= ALREADY_WHITE_THRESHOLD
  ) {
    return { status: 'already_white', bgColor: bg }
  }

  // Compute per-channel scale factors
  const scale = {
    r: 255 / Math.max(bg.r, 1),
    g: 255 / Math.max(bg.g, 1),
    b: 255 / Math.max(bg.b, 1),
  }

  // If scale is negligible, skip
  if (scale.r < MIN_SCALE && scale.g < MIN_SCALE && scale.b < MIN_SCALE) {
    return { status: 'already_white', bgColor: bg, scale }
  }

  // Apply linear scaling using sharp
  // sharp.linear(a, b) does: output = input * a + b
  // For RGB with alpha: provide arrays [r, g, b, alpha]
  // Alpha channel: scale=1, offset=0 (preserve as-is)
  let output = sharp(filepath)

  if (hasAlpha) {
    output = output.linear([scale.r, scale.g, scale.b, 1], [0, 0, 0, 0])
  } else {
    output = output.linear([scale.r, scale.g, scale.b], [0, 0, 0])
  }

  // Determine output format from extension
  const ext = path.extname(filepath).toLowerCase()
  if (ext === '.jpg' || ext === '.jpeg') {
    output = output.jpeg({ quality: 95 })
  } else if (ext === '.webp') {
    output = output.webp({ quality: 95 })
  } else {
    output = output.png({ compressionLevel: 9 })
  }

  // Write to temp then rename
  const tempPath = filepath + '.tmp'
  await output.toFile(tempPath)
  await fs.rename(tempPath, filepath)

  return { status: 'whitened', bgColor: bg, scale }
}

async function main() {
  const args = process.argv.slice(2)
  const options = parseCommonArgs(args)

  printHeader('Whiten Backgrounds (Sharp - Levels)')
  console.log(`Mode: ${options.dryRun ? 'DRY RUN' : 'WHITEN'}`)
  if (options.limit) console.log(`Limit: ${options.limit}`)
  if (options.force) console.log(`Force: re-processing all images`)

  // Check if path is a single file
  let allImages: string[]
  if (options.path) {
    const resolved = path.resolve(options.path)
    const stat = await fs.stat(resolved)
    if (stat.isFile()) {
      console.log('\nProcessing single file:', resolved)
      allImages = [resolved]
    } else {
      console.log('\nScanning for images in:', resolved)
      allImages = await findImages(resolved)
      console.log(`Found ${allImages.length} images`)
    }
  } else {
    console.log('\nScanning for images...')
    allImages = await findImages(ASSETS_DIR)
    console.log(`Found ${allImages.length} images`)
  }

  // If not forcing, filter out already-marked images
  let images = allImages
  if (!options.force) {
    const filtered: string[] = []
    for (const img of allImages) {
      const meta = await readImageMetadata(img)
      const prompt = meta?.generationPrompt || ''
      if (!prompt.includes('[WHITENED-SHARP]')) {
        filtered.push(img)
      }
    }
    console.log(`${filtered.length} not yet processed (${allImages.length - filtered.length} already marked)`)
    images = filtered
  }

  if (options.limit) {
    images = images.slice(0, options.limit)
  }

  if (images.length === 0) {
    console.log('\nNo images to process.')
    process.exit(0)
  }

  if (options.dryRun) {
    console.log('\n' + '='.repeat(60))
    console.log('IMAGES TO PROCESS (DRY RUN)')
    console.log('='.repeat(60))
    for (const img of images) {
      console.log(`  ${path.relative(process.cwd(), img)}`)
    }
    console.log(`\n[DRY RUN] Would process ${images.length} images.`)
    process.exit(0)
  }

  // Process
  console.log('\n' + '='.repeat(60))
  console.log('WHITENING')
  console.log('='.repeat(60))

  let whitened = 0
  let alreadyWhite = 0
  let skipped = 0
  let errors = 0

  for (let i = 0; i < images.length; i++) {
    const filepath = images[i]
    const rel = path.relative(process.cwd(), filepath)
    process.stdout.write(`[${i + 1}/${images.length}] ${rel}`)

    try {
      const result = await whitenImage(filepath)

      if (result.status === 'whitened') {
        const bg = result.bgColor!
        const sc = result.scale!
        console.log(` -> whitened (bg: ${bg.r},${bg.g},${bg.b} scale: ${sc.r.toFixed(2)},${sc.g.toFixed(2)},${sc.b.toFixed(2)})`)
        whitened++

        // Mark as processed in metadata
        await writeImageMetadata(filepath, {
          generationPrompt: `[WHITENED-SHARP] levels adjusted (bg: ${bg.r},${bg.g},${bg.b})`,
        })

        // Update image index
        const useExiftool = await isExiftoolAvailable()
        const fullMetadata = await processImage(filepath, useExiftool)
        await updateImageInIndex(filepath, fullMetadata)
      } else if (result.status === 'already_white') {
        console.log(` -> already white, skipped`)
        alreadyWhite++
      } else {
        console.log(` -> skipped (${result.error})`)
        skipped++
      }
    } catch (err: any) {
      console.log(` -> ERROR: ${err.message}`)
      errors++
    }
  }

  printSummary({
    'Whitened': whitened,
    'Already white': alreadyWhite,
    'Skipped': skipped,
    'Errors': errors,
  })
}

main().catch(error => {
  console.error('Fatal error:', error)
  process.exit(1)
})
