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
 *   --no-transcript     Skip extracting transcript after edit
 */

import fs from 'fs/promises'
import path from 'path'
import { genAI, GEMINI_IMAGE_MODEL_ID } from '../lib/llm'
import { saveImage, ImageMetadata, GeneratedImage } from '../lib/gemini-images'

// Shared utilities
import { getMimeType, isSupportedImage, validateImageFile } from '../lib/image-file-utils'
import { readImageMetadata } from '../lib/exiftool-utils'
import { getArgValue, hasFlag, getPositionalArgs, printHeader } from '../lib/cli-utils'

/**
 * Edit an image using Gemini
 */
async function editImage(
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

  // Build the edit prompt
  const editPrompt = `Edit this image according to these instructions: ${editInstructions}

Keep everything else exactly the same - preserve the overall style, colors, layout, and any elements not mentioned in the instructions. Make ONLY the changes requested.`

  console.log(`\nSending to Gemini (${GEMINI_IMAGE_MODEL_ID})...`)

  try {
    // Call Gemini with the image and edit request
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

    // Extract the edited image from response
    if (response.candidates && response.candidates.length > 0) {
      const candidate = response.candidates[0]
      const parts = candidate.content?.parts || []

      for (const part of parts) {
        if (part.inlineData?.data) {
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
            : `[EDITED] Edit: ${editInstructions}`

          // Save the edited image
          const generatedImage: GeneratedImage = {
            imageBytes: part.inlineData.data,
          }

          await saveImage(generatedImage, outputPath, metadata, editDescription, { skipWatermark: true })

          console.log(`\n[OK] Edited image saved: ${outputPath}`)
          return { success: true }
        }
      }

      // Check if there's a text response (might be an error or explanation)
      for (const part of parts) {
        if (part.text) {
          console.log(`\nModel response: ${part.text}`)
        }
      }
    }

    return { success: false, error: 'No edited image returned from Gemini' }
  } catch (error: any) {
    return { success: false, error: error.message }
  }
}

async function main() {
  const args = process.argv.slice(2)

  // Parse arguments
  const outputPath = getArgValue(args, 'output', ['o'])
  const noBackup = hasFlag(args, 'no-backup')
  const noTranscript = hasFlag(args, 'no-transcript')
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
  --no-transcript     Skip extracting transcript after edit
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

  const result = await editImage(imagePath, editInstructions, finalOutputPath, !noBackup)

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
