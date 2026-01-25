#!/usr/bin/env tsx
/**
 * Compress Images - Optimize existing images to reduce file size
 *
 * Compresses images using optimal quality settings that are visually
 * indistinguishable from the original while significantly reducing file size.
 *
 * Typical savings:
 * - JPEG: 30-50% smaller at quality 85 (vs unoptimized)
 * - PNG: 20-60% smaller with compression level 9
 * - WebP: Best compression, 40-60% smaller than JPEG
 *
 * Usage:
 *   npx tsx scripts/images/compress-images.ts              # Compress all images
 *   npx tsx scripts/images/compress-images.ts --dry-run    # Preview savings
 *   npx tsx scripts/images/compress-images.ts --limit 10   # Process 10 images
 *   npx tsx scripts/images/compress-images.ts --path <dir> # Specific directory
 *   npx tsx scripts/images/compress-images.ts --min-size 100  # Only files > 100KB
 *   npx tsx scripts/images/compress-images.ts --to-webp    # Convert to WebP (best compression)
 *
 * Options:
 *   --dry-run      Preview compression savings without modifying files
 *   --limit N      Process only N images
 *   --path <dir>   Process only images in specific directory
 *   --min-size N   Only compress files larger than N KB (default: 50)
 *   --to-webp      Convert JPEG/PNG to WebP for maximum compression
 *   --backup       Keep original files with .backup extension
 */

import { existsSync } from 'fs'
import fs from 'fs/promises'
import path from 'path'
import sharp from 'sharp'

// Shared utilities
import { findImages, formatBytes } from '../lib/image-file-utils'
import { compressImageIfNeeded, CompressionResult as BaseCompressionResult } from '../lib/gemini-images'
import { parseCommonArgs, getArgValue, hasFlag, printHeader, printSummary } from '../lib/cli-utils'

const ASSETS_DIR = path.join(process.cwd(), 'assets', 'images')

interface CompressionResult {
  path: string
  originalSize: number
  compressedSize: number
  savings: number
  savingsPercent: number
  format: string
  error?: string
}

/**
 * Compress a single image (with optional WebP conversion)
 */
async function compressImage(
  imagePath: string,
  options: { toWebp?: boolean; backup?: boolean; dryRun?: boolean }
): Promise<CompressionResult> {
  const stats = await fs.stat(imagePath)
  const originalSize = stats.size
  const ext = path.extname(imagePath).toLowerCase()

  // WebP conversion is a special case - needs separate handling
  if (options.toWebp && (ext === '.jpg' || ext === '.jpeg' || ext === '.png')) {
    const outputPath = imagePath.replace(/\.(jpg|jpeg|png)$/i, '.webp')

    if (!options.dryRun) {
      // Backup original if requested
      if (options.backup) {
        await fs.copyFile(imagePath, imagePath + '.backup')
      }

      // Convert to WebP
      await sharp(imagePath)
        .webp({ quality: 85, effort: 6 })
        .toFile(outputPath)

      const newStats = await fs.stat(outputPath)
      const savings = originalSize - newStats.size
      const savingsPercent = (savings / originalSize) * 100

      // Delete original after successful conversion
      await fs.unlink(imagePath)

      return {
        path: outputPath,
        originalSize,
        compressedSize: newStats.size,
        savings,
        savingsPercent,
        format: '.webp',
      }
    } else {
      // Dry run for WebP - estimate savings
      const outputBuffer = await sharp(imagePath)
        .webp({ quality: 85, effort: 6 })
        .toBuffer()

      return {
        path: outputPath,
        originalSize,
        compressedSize: outputBuffer.length,
        savings: originalSize - outputBuffer.length,
        savingsPercent: ((originalSize - outputBuffer.length) / originalSize) * 100,
        format: '.webp',
      }
    }
  }

  // Backup original if requested (before compression)
  if (!options.dryRun && options.backup) {
    await fs.copyFile(imagePath, imagePath + '.backup')
  }

  // Standard compression using shared utility
  const result = await compressImageIfNeeded(imagePath, {
    force: true, // Always try to compress since user explicitly requested
    minSizeBytes: 0, // No threshold for explicit compression
    dryRun: options.dryRun,
  })

  return {
    path: imagePath,
    originalSize: result.originalSize,
    compressedSize: result.finalSize,
    savings: result.savings,
    savingsPercent: result.savingsPercent,
    format: ext,
    error: result.skipReason,
  }
}

async function main() {
  const args = process.argv.slice(2)
  const options = parseCommonArgs(args)

  const targetDir = options.path ? path.resolve(options.path) : ASSETS_DIR
  const minSizeKB = parseInt(getArgValue(args, 'min-size') || '50', 10)
  const toWebp = hasFlag(args, 'to-webp')
  const backup = hasFlag(args, 'backup')

  printHeader('Image Compression')
  console.log(`Target directory: ${targetDir}`)
  console.log(`Minimum size: ${minSizeKB}KB`)
  console.log(`Convert to WebP: ${toWebp}`)
  console.log(`Keep backups: ${backup}`)
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

  // Filter by minimum size
  console.log('\n[2/3] Filtering by size...')
  const minSizeBytes = minSizeKB * 1024
  const largeImages: { path: string; size: number }[] = []

  for (const img of images) {
    const stats = await fs.stat(img)
    if (stats.size >= minSizeBytes) {
      largeImages.push({ path: img, size: stats.size })
    }
  }

  console.log(`  ${images.length - largeImages.length} images below ${minSizeKB}KB (skipped)`)
  console.log(`  ${largeImages.length} images to compress`)

  // Sort by size (largest first)
  largeImages.sort((a, b) => b.size - a.size)

  // Apply limit
  let toProcess = largeImages.map(i => i.path)
  if (options.limit && toProcess.length > options.limit) {
    toProcess = toProcess.slice(0, options.limit)
    console.log(`  Limited to ${options.limit} images`)
  }

  if (toProcess.length === 0) {
    console.log('\nNo images to compress.')
    process.exit(0)
  }

  // Process images
  console.log(`\n[3/3] Compressing ${toProcess.length} images...`)
  const results: CompressionResult[] = []
  let processed = 0
  let totalOriginal = 0
  let totalCompressed = 0
  let errors = 0

  for (const imagePath of toProcess) {
    const relativePath = path.relative(process.cwd(), imagePath)
    processed++

    try {
      const result = await compressImage(imagePath, { toWebp, backup, dryRun: options.dryRun })
      results.push(result)

      totalOriginal += result.originalSize
      totalCompressed += result.compressedSize

      // Only show if significant savings
      if (result.savingsPercent > 5) {
        const status = options.dryRun ? '[DRY RUN]' : '[OK]'
        console.log(
          `[${processed}/${toProcess.length}] ${relativePath}: ` +
          `${formatBytes(result.originalSize)} -> ${formatBytes(result.compressedSize)} ` +
          `(-${result.savingsPercent.toFixed(1)}%) ${status}`
        )
      } else {
        console.log(`[${processed}/${toProcess.length}] ${relativePath}: Already optimal`)
      }
    } catch (error) {
      console.error(`[${processed}/${toProcess.length}] ${relativePath}: ERROR - ${error}`)
      results.push({
        path: imagePath,
        originalSize: 0,
        compressedSize: 0,
        savings: 0,
        savingsPercent: 0,
        format: '',
        error: String(error),
      })
      errors++
    }
  }

  // Summary
  const totalSavings = totalOriginal - totalCompressed
  const totalSavingsPercent = totalOriginal > 0 ? (totalSavings / totalOriginal) * 100 : 0

  printSummary({
    'Images processed': processed,
    'Errors': errors,
  })

  console.log(`\nCompression Results:`)
  console.log(`  Original total: ${formatBytes(totalOriginal)}`)
  console.log(`  Compressed total: ${formatBytes(totalCompressed)}`)
  console.log(`  Total savings: ${formatBytes(totalSavings)} (${totalSavingsPercent.toFixed(1)}%)`)

  // Top savings
  const topSavers = results
    .filter(r => r.savings > 0)
    .sort((a, b) => b.savings - a.savings)
    .slice(0, 5)

  if (topSavers.length > 0) {
    console.log(`\nTop savings:`)
    for (const r of topSavers) {
      const relativePath = path.relative(process.cwd(), r.path)
      console.log(`  ${formatBytes(r.savings)} saved: ${relativePath}`)
    }
  }

  if (options.dryRun) {
    console.log('\n[DRY RUN] No files were modified. Run without --dry-run to compress.')
  }
}

main().catch(error => {
  console.error('Fatal error:', error)
  process.exit(1)
})
