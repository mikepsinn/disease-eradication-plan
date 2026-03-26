#!/usr/bin/env tsx
/**
 * Generate complete head sprites for the alien character.
 * Instead of isolating individual elements (unreliable), generate full head variants:
 *   - idle: eyes open, mouth smiling
 *   - blink: eyes closed, mouth smiling
 *   - speaking: eyes open, mouth wide open
 *   - listening: eyes open, mouth slightly open
 *
 * Usage: npx tsx transmit/scripts/generate-head-sprites.ts [variant...]
 */

import fs from 'fs/promises'
import path from 'path'
import sharp from 'sharp'
import { editImage } from '../../scripts/lib/gemini-images'
import { getMimeType } from '../../scripts/lib/image-file-utils'

const REFERENCE_IMAGE = path.resolve('assets/music-video/keyframes/scene-09.jpg')
const BODY_REFERENCE = path.resolve('assets/images/wishonia/wishonia-body-clean.png')
const OUTPUT_DIR = path.resolve('transmit/public/assets/sprites/alien')

interface HeadVariant {
  name: string
  instruction: string
}

const CHARACTER_DESC = 'the cute blue-skinned alien girl with black bob haircut and antennae from this illustration. IMPORTANT: Her black bob hair MUST show the pointed tips that curl inward at chin level on both sides - this is a key feature of her 60s bob hairstyle'

const VARIANTS: HeadVariant[] = [
  {
    name: 'head-idle',
    instruction: `Extract just the head of ${CHARACTER_DESC}. Show her head, hair, antennae, eyebrows, eyes (open, looking forward), nose, and mouth (closed friendly smile). Place the isolated head centered on a solid bright magenta #FF00FF background. Remove her body, the computer, monitor, background patterns, spirals, and everything else. ONLY the head from the neck up.`
  },
  {
    name: 'head-blink',
    instruction: `Extract just the head of ${CHARACTER_DESC}. Show her head, hair, antennae, eyebrows, nose, and mouth (closed friendly smile), but make her eyes CLOSED (thin curved lines as if blinking). Place the isolated head centered on a solid bright magenta #FF00FF background. Remove her body, the computer, monitor, background patterns, spirals, and everything else. ONLY the head from the neck up.`
  },
  {
    name: 'head-speaking',
    instruction: `Extract just the head of ${CHARACTER_DESC}. Show her head, hair, antennae, eyebrows, eyes (open, looking forward), nose, and mouth WIDE OPEN as if speaking excitedly (showing teeth). Place the isolated head centered on a solid bright magenta #FF00FF background. Remove her body, the computer, monitor, background patterns, spirals, and everything else. ONLY the head from the neck up.`
  },
  {
    name: 'head-listening',
    instruction: `Extract just the head of ${CHARACTER_DESC}. Show her head, hair, antennae, eyebrows, eyes (open, looking forward), nose, and mouth SLIGHTLY OPEN in a small 'O' shape as if listening attentively. Place the isolated head centered on a solid bright magenta #FF00FF background. Remove her body, the computer, monitor, background patterns, spirals, and everything else. ONLY the head from the neck up.`
  },
  {
    name: 'body',
    instruction: `Take the alien girl from this image and redraw ONLY her body from the neck down, standing upright facing forward (NOT seated at desk). Show her neck, shoulders, torso, arms relaxed at sides, and her orange/blue patterned sleeveless dress going to about mid-thigh. NO head, NO desk, NO computer. Place the standing body centered on a solid filled bright magenta #FF00FF background with NO transparency or checkerboard.`
  },
]

async function removeMagentaBackground(inputPath: string, outputPath: string): Promise<void> {
  const image = sharp(inputPath)
  const { data, info } = await image.raw().toBuffer({ resolveWithObject: true })
  const outputData = Buffer.alloc(info.width * info.height * 4)

  for (let i = 0; i < info.width * info.height; i++) {
    const srcIdx = i * info.channels
    const dstIdx = i * 4
    const r = data[srcIdx], g = data[srcIdx + 1], b = data[srcIdx + 2]
    const isMagenta = r > 180 && g < 100 && b > 180
    outputData[dstIdx] = r
    outputData[dstIdx + 1] = g
    outputData[dstIdx + 2] = b
    outputData[dstIdx + 3] = isMagenta ? 0 : 255
  }

  // Save full-size transparent PNG
  const tempPath = outputPath + '.tmp.png'
  await sharp(outputData, { raw: { width: info.width, height: info.height, channels: 4 } })
    .png()
    .toFile(tempPath)

  // Trim, pad, and resize in a clean pipeline using the PNG (not raw buffer)
  const temp2 = outputPath + '.tmp2.png'
  await sharp(tempPath).trim().png().toFile(temp2)

  await sharp(temp2)
    .extend({ top: 10, bottom: 10, left: 10, right: 10, background: { r: 0, g: 0, b: 0, alpha: 0 } })
    .resize(200, 250, { fit: 'contain', background: { r: 0, g: 0, b: 0, alpha: 0 } })
    .png()
    .toFile(outputPath)

  await fs.unlink(tempPath)
  await fs.unlink(temp2)
}

async function generateVariant(variant: HeadVariant, imageBase64: string, mimeType: string, altBase64?: string, altMime?: string): Promise<boolean> {
  // Body uses main reference (full scene) for better context
  // Alt image had transparency issues
  const rawPath = path.join(OUTPUT_DIR, `${variant.name}-raw.png`)
  const finalPath = path.join(OUTPUT_DIR, `${variant.name}.png`)

  console.log(`\n--- Generating: ${variant.name} ---`)

  const result = await editImage(imageBase64, mimeType, variant.instruction)

  if (result.result !== 'success' || !result.imageBytes) {
    console.error(`  FAILED: ${result.error || result.result}`)
    return false
  }

  const rawBuffer = Buffer.from(result.imageBytes, 'base64')
  await fs.writeFile(rawPath, rawBuffer)
  console.log(`  Raw: ${rawPath}`)

  await removeMagentaBackground(rawPath, finalPath)
  console.log(`  Final: ${finalPath}`)

  return true
}

async function main() {
  const args = process.argv.slice(2)
  const onlyVariants = args.length > 0 ? args : null

  console.log('=== Head Sprite Generation ===')
  console.log(`Reference: ${REFERENCE_IMAGE}`)

  const imageBuffer = await fs.readFile(REFERENCE_IMAGE)
  const imageBase64 = imageBuffer.toString('base64')
  const mimeType = getMimeType(REFERENCE_IMAGE)

  // Load body reference if available
  let bodyBase64 = imageBase64
  let bodyMime = mimeType
  try {
    const bodyBuf = await fs.readFile(BODY_REFERENCE)
    bodyBase64 = bodyBuf.toString('base64')
    bodyMime = getMimeType(BODY_REFERENCE)
    console.log(`Body reference: ${BODY_REFERENCE}`)
  } catch { console.log('Body reference not found, using main reference') }

  await fs.mkdir(OUTPUT_DIR, { recursive: true })

  const toGenerate = onlyVariants
    ? VARIANTS.filter(v => onlyVariants.includes(v.name))
    : VARIANTS

  let ok = 0, fail = 0
  for (const variant of toGenerate) {
    (await generateVariant(variant, imageBase64, mimeType, bodyBase64, bodyMime)) ? ok++ : fail++
  }

  console.log(`\n=== Done: ${ok} ok, ${fail} failed ===`)
}

main().catch(e => { console.error('Fatal:', e); process.exit(1) })
