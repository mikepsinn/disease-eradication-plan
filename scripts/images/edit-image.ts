#!/usr/bin/env tsx
/**
 * Edit Image - AI-powered image editing using Gemini
 *
 * Edit images using natural language instructions. Preserves the original
 * style while making requested changes.
 *
 * Usage:
 *   npx tsx scripts/images/edit-image.ts <image-path> "<edit instructions>"
 *   npx tsx scripts/images/edit-image.ts image.jpg "Change the title to 'New Title'"
 *   npx tsx scripts/images/edit-image.ts chart.png "Make the background white"
 *   npx tsx scripts/images/edit-image.ts poster.jpg "Remove the watermark"
 *
 * Options:
 *   --output <path>     Save edited image to different path (default: overwrites original)
 *   --no-backup         Don't create a backup of the original
 */

import fs from 'fs/promises'
import path from 'path'
import { editImage, saveImage, ImageMetadata, GeneratedImage } from '../lib/gemini-images'
import { getMimeType, validateImageFile } from '../lib/image-file-utils'
import { readImageMetadata } from '../lib/exiftool-utils'
import { getArgValue, hasFlag, getPositionalArgs, printHeader } from '../lib/cli-utils'

/**
 * Edit an image file using the shared editImage function
 */
async function editImageFile(
  imagePath: string,
  editInstructions: string,
  outputPath: string,
  createBackup: boolean = true
): Promise<{ success: boolean; error?: string }> {
  console.log(`\nEditing: ${imagePath}`)
  console.log(`Instructions: ${editInstructions}`)

  // Read the existing image
  const imageBuffer = await fs.readFile(imagePath)
  const base64Image = imageBuffer.toString('base64')
  const mimeType = getMimeType(imagePath)

  // Create backup if requested and overwriting original
  if (createBackup && imagePath === outputPath) {
    const backupPath = imagePath + '.backup'
    await fs.copyFile(imagePath, backupPath)
    console.log(`Backup saved: ${backupPath}`)
  }

  // Get original metadata
  const originalMetadata = await readImageMetadata(imagePath)
  console.log(`Original metadata: ${originalMetadata ? 'Found' : 'None'}`)

  // Use shared editImage function
  const result = await editImage(base64Image, mimeType, editInstructions)

  if (result.result === 'policy_blocked') {
    return { success: false, error: `Content policy blocked: ${result.error}` }
  }

  if (result.result !== 'success' || !result.imageBytes) {
    return { success: false, error: result.error || 'No edited image returned' }
  }

  // Build metadata for the edited image
  const metadata: ImageMetadata = {
    title: originalMetadata?.title || path.basename(imagePath),
    description: originalMetadata?.description || '',
    keywords: originalMetadata?.keywords || [],
  }

  // Build the edit description for the prompt field
  const originalPrompt = originalMetadata?.generationPrompt
  const editDescription = originalPrompt
    ? `[EDITED] Original: ${originalPrompt}. Edit: ${editInstructions}`
    : `[EDITED] ${editInstructions}`

  // Save the edited image
  const generatedImage: GeneratedImage = {
    imageBytes: result.imageBytes,
  }

  await saveImage(generatedImage, outputPath, metadata, editDescription, { skipWatermark: true })

  console.log(`\n[OK] Edited image saved: ${outputPath}`)
  return { success: true }
}

async function main() {
  const args = process.argv.slice(2)

  // Parse arguments
  const outputPath = getArgValue(args, 'output', ['o'])
  const noBackup = hasFlag(args, 'no-backup')
  const positionalArgs = getPositionalArgs(args)

  if (positionalArgs.length < 2) {
    console.log(`
Edit Image - AI-powered image editing using Gemini

Usage:
  npx tsx scripts/images/edit-image.ts <image-path> "<edit instructions>"

Examples:
  npx tsx scripts/images/edit-image.ts chart.png "Change the title to 'Updated Chart'"
  npx tsx scripts/images/edit-image.ts poster.jpg "Make the background darker"
  npx tsx scripts/images/edit-image.ts diagram.png "Remove the red circle"
  npx tsx scripts/images/edit-image.ts logo.png "Change 'oldsite.com' to 'newsite.com'"

Options:
  --output <path>     Save edited image to different path (default: overwrites original)
  --no-backup         Don't create a backup of the original
`)
    process.exit(1)
  }

  const imagePath = path.resolve(positionalArgs[0])
  const editInstructions = positionalArgs.slice(1).join(' ')
  const finalOutputPath = outputPath ? path.resolve(outputPath) : imagePath

  // Validate image file
  const validation = validateImageFile(imagePath)
  if (!validation.valid) {
    console.error(`ERROR: ${validation.error}`)
    process.exit(1)
  }

  printHeader('Edit Image')
  console.log(`Image: ${imagePath}`)
  console.log(`Output: ${finalOutputPath}`)
  console.log(`Instructions: ${editInstructions}`)
  console.log(`Backup: ${!noBackup}`)

  const result = await editImageFile(imagePath, editInstructions, finalOutputPath, !noBackup)

  if (!result.success) {
    console.error(`\n[ERROR] ${result.error}`)
    process.exit(1)
  }

  console.log('\nDone!')
}

main().catch(error => {
  console.error('Fatal error:', error)
  process.exit(1)
})
