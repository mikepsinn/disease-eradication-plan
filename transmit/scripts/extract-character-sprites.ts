#!/usr/bin/env tsx
/**
 * Extract character sprites from reference image using Gemini image editing.
 *
 * Asks Gemini to isolate each facial element onto a magenta background,
 * then uses sharp to convert magenta to transparency.
 *
 * Usage: npx tsx transmit/scripts/extract-character-sprites.ts
 */

import fs from 'fs/promises'
import path from 'path'
import sharp from 'sharp'
import { editImage } from '../../scripts/lib/gemini-images'
import { getMimeType } from '../../scripts/lib/image-file-utils'

const REFERENCE_IMAGE = path.resolve('assets/music-video/keyframes/scene-09.jpg')
const OUTPUT_DIR = path.resolve('transmit/public/assets/sprites/alien')

interface SpriteDefinition {
  name: string
  instruction: string
}

// Each sprite we need to extract
const SPRITES: SpriteDefinition[] = [
  {
    name: 'face',
    instruction: 'Isolate ONLY the blue-skinned alien girl\'s face/head shape (the blue skin area including chin) on a solid bright magenta #FF00FF background. Remove the hair, eyes, mouth, eyebrows, nose, antennae, and everything else. Just the blue face silhouette shape.'
  },
  {
    name: 'hair',
    instruction: 'Isolate ONLY the alien girl\'s black bob haircut (including the bangs/fringe) on a solid bright magenta #FF00FF background. Remove the face, eyes, mouth, body, and everything else. Just the black hair.'
  },
  {
    name: 'antennae',
    instruction: 'Isolate ONLY the alien girl\'s two antennae (thin stalks with round blue balls on top) on a solid bright magenta #FF00FF background. Remove everything else.'
  },
  {
    name: 'eyebrows',
    instruction: 'Isolate ONLY the alien girl\'s two eyebrows on a solid bright magenta #FF00FF background. Remove everything else. Keep them positioned where they would be on the face.'
  },
  {
    name: 'eyes-open',
    instruction: 'Isolate ONLY the alien girl\'s two eyes (open, with white sclera and dark irises visible) on a solid bright magenta #FF00FF background. Remove everything else. Keep them positioned where they would be on the face.'
  },
  {
    name: 'eyes-closed',
    instruction: 'Take the alien girl\'s face and draw ONLY two closed eyes (thin curved lines as if blinking) on a solid bright magenta #FF00FF background. Position them where the open eyes would be. Remove everything else.'
  },
  {
    name: 'nose',
    instruction: 'Isolate ONLY the alien girl\'s small nose on a solid bright magenta #FF00FF background. Remove everything else. Keep it positioned where it would be on the face.'
  },
  {
    name: 'mouth-idle',
    instruction: 'Isolate ONLY the alien girl\'s smiling mouth (closed smile) on a solid bright magenta #FF00FF background. Remove everything else. Keep it positioned where it would be on the face.'
  },
  {
    name: 'mouth-speaking',
    instruction: 'Take the alien girl\'s mouth and redraw it wide open (as if speaking/talking, showing teeth) on a solid bright magenta #FF00FF background. Remove everything else. Keep it positioned where it would be on the face.'
  },
  {
    name: 'mouth-listening',
    instruction: 'Take the alien girl\'s mouth and redraw it slightly open (as if listening, small O shape) on a solid bright magenta #FF00FF background. Remove everything else. Keep it positioned where it would be on the face.'
  },
]

async function removeMagentaBackground(inputPath: string, outputPath: string): Promise<void> {
  const image = sharp(inputPath)
  const { data, info } = await image.raw().toBuffer({ resolveWithObject: true })

  const outputData = Buffer.alloc(info.width * info.height * 4)

  for (let i = 0; i < info.width * info.height; i++) {
    const srcIdx = i * info.channels
    const dstIdx = i * 4

    const r = data[srcIdx]
    const g = data[srcIdx + 1]
    const b = data[srcIdx + 2]

    // Check if pixel is magenta (high red, low green, high blue)
    const isMagenta = r > 180 && g < 100 && b > 180

    outputData[dstIdx] = r
    outputData[dstIdx + 1] = g
    outputData[dstIdx + 2] = b
    outputData[dstIdx + 3] = isMagenta ? 0 : 255
  }

  await sharp(outputData, {
    raw: { width: info.width, height: info.height, channels: 4 },
  })
    .png()
    .toFile(outputPath)
}

async function extractSprite(sprite: SpriteDefinition, imageBase64: string, mimeType: string): Promise<boolean> {
  const rawPath = path.join(OUTPUT_DIR, `${sprite.name}-raw.png`)
  const finalPath = path.join(OUTPUT_DIR, `${sprite.name}.png`)

  console.log(`\n--- Extracting: ${sprite.name} ---`)
  console.log(`Instruction: ${sprite.instruction.substring(0, 80)}...`)

  const result = await editImage(imageBase64, mimeType, sprite.instruction)

  if (result.result !== 'success' || !result.imageBytes) {
    console.error(`  FAILED: ${result.error || result.result}`)
    return false
  }

  // Save raw result
  const rawBuffer = Buffer.from(result.imageBytes, 'base64')
  await fs.writeFile(rawPath, rawBuffer)
  console.log(`  Raw saved: ${rawPath}`)

  // Remove magenta background
  await removeMagentaBackground(rawPath, finalPath)
  console.log(`  Transparent PNG: ${finalPath}`)

  return true
}

async function main() {
  // Parse args - allow extracting specific sprites
  const args = process.argv.slice(2)
  const onlySprites = args.length > 0 ? args : null

  console.log('=== Character Sprite Extraction ===')
  console.log(`Reference: ${REFERENCE_IMAGE}`)
  console.log(`Output: ${OUTPUT_DIR}`)

  // Read reference image
  const imageBuffer = await fs.readFile(REFERENCE_IMAGE)
  const imageBase64 = imageBuffer.toString('base64')
  const mimeType = getMimeType(REFERENCE_IMAGE)

  await fs.mkdir(OUTPUT_DIR, { recursive: true })

  const spritesToExtract = onlySprites
    ? SPRITES.filter(s => onlySprites.includes(s.name))
    : SPRITES

  console.log(`\nExtracting ${spritesToExtract.length} sprites...`)

  let succeeded = 0
  let failed = 0

  for (const sprite of spritesToExtract) {
    const ok = await extractSprite(sprite, imageBase64, mimeType)
    if (ok) succeeded++
    else failed++
  }

  console.log(`\n=== Done: ${succeeded} succeeded, ${failed} failed ===`)
}

main().catch(error => {
  console.error('Fatal error:', error)
  process.exit(1)
})
