#!/usr/bin/env tsx
/**
 * Fix Image Text - Search and edit images with text issues
 *
 * Searches through image transcripts for a given string and optionally
 * edits the images using Gemini to fix the text, or regenerates from scratch.
 *
 * Usage:
 *   npx tsx scripts/images/fix-image-text.ts --search "wrong text"
 *   npx tsx scripts/images/fix-image-text.ts --search "typo" --replace "correct" --edit
 *   npx tsx scripts/images/fix-image-text.ts --search "old.com" --remove --edit
 *   npx tsx scripts/images/fix-image-text.ts --search "badtext" --regenerate
 *
 * Options:
 *   --search <text>     Text to search for in transcripts (required)
 *   --replace <text>    Replace found text with this
 *   --remove            Remove the found text (same as --replace "")
 *   --edit              Edit existing images using Gemini (preserves style)
 *   --regenerate        Regenerate images from scratch (uses original prompt)
 *   --path <dir>        Only search images in specific directory
 *   --limit N           Process only N images
 */

import fs from 'fs/promises'
import { existsSync } from 'fs'
import path from 'path'
import {
  generateAndSaveImages,
  ImageMetadata,
  saveImage,
  GeneratedImage,
} from '../lib/gemini-images'
import { genAI, GEMINI_IMAGE_MODEL_ID } from '../lib/llm'

// Shared utilities
import { findImages, getMimeType } from '../lib/image-file-utils'
import { readImageMetadata, writeImageMetadata } from '../lib/exiftool-utils'
import { ImageSearchMatch } from '../lib/image-metadata'
import { parseCommonArgs, getArgValue, hasFlag, printHeader, printSummary } from '../lib/cli-utils'

const ASSETS_DIR = path.join(process.cwd(), 'assets', 'images')

/**
 * Get context around a match (for display)
 */
function getMatchContext(text: string, searchText: string, contextChars: number = 50): string {
  const index = text.toLowerCase().indexOf(searchText.toLowerCase())
  if (index === -1) return ''

  const start = Math.max(0, index - contextChars)
  const end = Math.min(text.length, index + searchText.length + contextChars)

  let context = text.substring(start, end)
  if (start > 0) context = '...' + context
  if (end < text.length) context = context + '...'

  return context
}

/**
 * Search images for text in transcripts
 */
async function searchImages(
  searchText: string,
  targetDir: string,
  limit?: number
): Promise<ImageSearchMatch[]> {
  console.log(`\nSearching for "${searchText}" in image transcripts...`)

  const images = await findImages(targetDir)
  console.log(`Found ${images.length} images to search`)

  const matches: ImageSearchMatch[] = []
  let searched = 0

  for (const imagePath of images) {
    if (limit && searched >= limit) break
    searched++

    const metadata = await readImageMetadata(imagePath)
    if (!metadata) continue

    const transcript = metadata.transcript
    if (!transcript) continue

    if (transcript.toLowerCase().includes(searchText.toLowerCase())) {
      matches.push({
        filepath: imagePath,
        relativePath: path.relative(process.cwd(), imagePath),
        transcript,
        generationPrompt: metadata.generationPrompt,
        matchedText: searchText,
        matchContext: getMatchContext(transcript, searchText),
      })
    }

    // Progress indicator
    if (searched % 50 === 0) {
      process.stdout.write(`  Searched ${searched}/${images.length}...\r`)
    }
  }

  console.log(`\nFound ${matches.length} images with "${searchText}" in transcript`)
  return matches
}

/**
 * Edit an image using Gemini to fix text
 * This preserves the overall style while fixing specific text
 */
async function editImage(
  match: ImageSearchMatch,
  searchText: string,
  replaceText: string
): Promise<boolean> {
  console.log(`  Editing image to fix text...`)
  console.log(`    Change: "${searchText}" -> "${replaceText || '(remove)'}"`)

  try {
    // Read the existing image
    const imageBuffer = await fs.readFile(match.filepath)
    const base64Image = imageBuffer.toString('base64')
    const mimeType = getMimeType(match.filepath)

    // Create backup
    const backupPath = match.filepath + '.backup'
    await fs.copyFile(match.filepath, backupPath)
    console.log(`    Backup saved: ${path.basename(backupPath)}`)

    // Build the edit prompt
    let editPrompt: string
    if (replaceText) {
      editPrompt = `Edit this image: Find and replace all instances of "${searchText}" with "${replaceText}". Keep everything else exactly the same - same style, colors, layout, and other text. Only change the specific text mentioned.`
    } else {
      editPrompt = `Edit this image: Remove all instances of "${searchText}" from the image. Keep everything else exactly the same - same style, colors, layout, and other text. Fill in the removed area naturally to match the surrounding design.`
    }

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
          // Get original metadata to preserve
          const originalMetadata = await readImageMetadata(match.filepath)

          const metadata: ImageMetadata = {
            title: originalMetadata?.title || path.basename(match.filepath),
            description: originalMetadata?.description || '',
            keywords: originalMetadata?.keywords || [],
          }

          // Build the edit description for the prompt field
          const editDescription = `[EDITED] Original prompt: ${match.generationPrompt || 'unknown'}. Edit: replaced "${searchText}" with "${replaceText || '(removed)'}"`

          // Save the edited image
          const generatedImage: GeneratedImage = {
            imageBytes: part.inlineData.data,
          }

          await saveImage(generatedImage, match.filepath, metadata, editDescription, { skipWatermark: false })

          console.log(`    [OK] Edited: ${match.relativePath}`)
          return true
        }
      }
    }

    console.log(`    [ERROR] No edited image returned from Gemini`)
    return false
  } catch (error: any) {
    console.log(`    [ERROR] Failed to edit: ${error.message}`)
    return false
  }
}

/**
 * Regenerate an image with modified prompt
 */
async function regenerateImage(
  match: ImageSearchMatch,
  searchText: string,
  replaceText: string
): Promise<boolean> {
  if (!match.generationPrompt) {
    console.log(`  [SKIP] No generation prompt stored for ${match.relativePath}`)
    return false
  }

  // Modify the prompt
  const newPrompt = match.generationPrompt.replace(new RegExp(searchText, 'gi'), replaceText)

  if (newPrompt === match.generationPrompt) {
    console.log(`  [SKIP] Search text not found in prompt for ${match.relativePath}`)
    return false
  }

  console.log(`  Regenerating with modified prompt...`)
  console.log(`    Old: ${match.generationPrompt.substring(0, 100)}...`)
  console.log(`    New: ${newPrompt.substring(0, 100)}...`)

  try {
    // Parse the filepath to get output directory and filename
    const dir = path.dirname(match.filepath)
    const ext = path.extname(match.filepath)
    const basename = path.basename(match.filepath, ext)

    // Create backup of original
    const backupPath = match.filepath + '.backup'
    await fs.copyFile(match.filepath, backupPath)
    console.log(`    Backup saved: ${backupPath}`)

    // Regenerate the image
    // Note: We need the original metadata to preserve title, description, keywords, etc.
    const originalMetadata = await readImageMetadata(match.filepath)

    const metadata: ImageMetadata = {
      title: originalMetadata?.title || basename,
      description: originalMetadata?.description || '',
      keywords: originalMetadata?.keywords || [],
    }

    await generateAndSaveImages({
      prompt: newPrompt,
      outputDir: dir,
      filePrefix: basename,
      format: ext.slice(1) as 'png' | 'jpg',
      metadata,
    })

    console.log(`    [OK] Regenerated: ${match.relativePath}`)
    return true
  } catch (error: any) {
    console.log(`    [ERROR] Failed to regenerate: ${error.message}`)
    return false
  }
}

async function main() {
  const args = process.argv.slice(2)
  const options = parseCommonArgs(args)

  // Parse specific arguments
  const searchText = getArgValue(args, 'search', ['s'])
  const replaceText = getArgValue(args, 'replace', ['r'])
  const removeFlag = hasFlag(args, 'remove')
  const editFlag = hasFlag(args, 'edit', ['e'])
  const regenerateFlag = hasFlag(args, 'regenerate')

  if (!searchText) {
    console.log(`
Fix Image Text - Search and edit images with text issues

Usage:
  npx tsx scripts/images/fix-image-text.ts --search "wrong text"
  npx tsx scripts/images/fix-image-text.ts --search "typo" --replace "correct" --edit
  npx tsx scripts/images/fix-image-text.ts --search "old.com" --remove --edit
  npx tsx scripts/images/fix-image-text.ts --search "badtext" --regenerate

Options:
  --search <text>     Text to search for in transcripts (required)
  --replace <text>    Replace found text with this
  --remove            Remove the found text (same as --replace "")
  --edit              Edit existing images using Gemini (preserves style)
  --regenerate        Regenerate images from scratch (uses original prompt)
  --path <dir>        Only search images in specific directory
  --limit N           Process only N images

Examples:
  # Find all images with "oldsite.com" in the text
  npx tsx scripts/images/fix-image-text.ts --search "oldsite.com"

  # Edit images to replace "oldsite.com" with "newsite.com" (preserves image style)
  npx tsx scripts/images/fix-image-text.ts --search "oldsite.com" --replace "newsite.com" --edit

  # Remove "DRAFT" watermark from images
  npx tsx scripts/images/fix-image-text.ts --search "DRAFT" --remove --edit

  # Regenerate images that have a typo (uses original prompt with fix)
  npx tsx scripts/images/fix-image-text.ts --search "teh" --replace "the" --regenerate
`)
    process.exit(1)
  }

  const finalReplaceText = replaceText !== undefined ? replaceText : removeFlag ? '' : null
  const targetDir = options.path ? path.resolve(options.path) : ASSETS_DIR
  const mode = editFlag ? 'edit' : regenerateFlag ? 'regenerate' : 'search'

  printHeader('Fix Image Text')
  console.log(`Search text: "${searchText}"`)
  console.log(`Replace with: ${finalReplaceText === null ? '(search only)' : `"${finalReplaceText}"`}`)
  console.log(`Mode: ${mode}`)
  console.log(`Target directory: ${targetDir}`)
  if (options.limit) console.log(`Limit: ${options.limit}`)

  if (!existsSync(targetDir)) {
    console.error(`ERROR: Directory not found: ${targetDir}`)
    process.exit(1)
  }

  // Search for matches
  const matches = await searchImages(searchText, targetDir, options.limit)

  if (matches.length === 0) {
    console.log('\nNo matches found.')
    process.exit(0)
  }

  // Display matches
  console.log('\n' + '='.repeat(60))
  console.log('MATCHES')
  console.log('='.repeat(60))

  for (let i = 0; i < matches.length; i++) {
    const match = matches[i]
    console.log(`\n[${i + 1}] ${match.relativePath}`)
    console.log(`    Context: ${match.matchContext}`)
    console.log(`    Has prompt: ${match.generationPrompt ? 'Yes' : 'No'}`)
  }

  // If only searching, we're done
  if (mode === 'search' || finalReplaceText === null) {
    console.log('\n' + '='.repeat(60))
    console.log(`Found ${matches.length} images with "${searchText}" in transcript.`)
    console.log('\nTo fix these images:')
    console.log('  --edit        Edit images using AI (preserves style, just fixes text)')
    console.log('  --regenerate  Regenerate from scratch (requires stored prompt)')
    process.exit(0)
  }

  // Show what will be processed
  console.log('\n' + '='.repeat(60))
  console.log(`${mode.toUpperCase()} MODE - Processing ${matches.length} images`)
  console.log('='.repeat(60))

  if (mode === 'regenerate') {
    // Check which images can be regenerated
    let canRegenerate = 0
    for (const match of matches) {
      if (match.generationPrompt) {
        const hasSearchInPrompt = match.generationPrompt.toLowerCase().includes(searchText.toLowerCase())
        console.log(`  ${hasSearchInPrompt ? '[CAN FIX]' : '[EDIT ONLY]'} ${match.relativePath}`)
        if (hasSearchInPrompt) canRegenerate++
      } else {
        console.log(`  [EDIT ONLY - NO PROMPT] ${match.relativePath}`)
      }
    }
    console.log(`\n${canRegenerate}/${matches.length} can be regenerated (have prompt with search text).`)
    console.log('Images without stored prompt or without search text in prompt can use --edit instead.')
  }

  // Process images
  console.log('\n' + '='.repeat(60))
  console.log(`PROCESSING (${mode})`)
  console.log('='.repeat(60))

  let success = 0
  let failed = 0
  let skipped = 0

  for (let i = 0; i < matches.length; i++) {
    const match = matches[i]
    console.log(`\n[${i + 1}/${matches.length}] ${match.relativePath}`)

    let result: boolean
    if (mode === 'edit') {
      result = await editImage(match, searchText, finalReplaceText)
    } else {
      result = await regenerateImage(match, searchText, finalReplaceText)
    }

    if (result) {
      success++
    } else {
      if (mode === 'regenerate' && !match.generationPrompt) {
        skipped++
      } else {
        failed++
      }
    }

    // Rate limiting
    if (result) {
      await new Promise(resolve => setTimeout(resolve, 2000))
    }
  }

  // Summary
  printSummary({
    Mode: mode,
    Processed: success,
    Skipped: skipped,
    Failed: failed,
  })
  console.log(`\nBackups saved with .backup extension`)
}

main().catch(error => {
  console.error('Fatal error:', error)
  process.exit(1)
})
