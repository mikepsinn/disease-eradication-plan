#!/usr/bin/env tsx
/**
 * Generate full head sprites (expression + mouth together) by editing
 * a single clean reference head. No separate mouth overlays needed.
 *
 * Usage:
 *   npx tsx transmit/scripts/generate-full-heads.ts              # all
 *   npx tsx transmit/scripts/generate-full-heads.ts neutral-smile # specific
 */

import fs from 'fs/promises'
import path from 'path'
import sharp from 'sharp'
import { editImage } from '../../scripts/lib/gemini-images'
import { getMimeType } from '../../scripts/lib/image-file-utils'

const HEAD_SOURCE = path.resolve('transmit/public/assets/sprites/alien/sources/head-neutral-seed.png')
const OUTPUT_DIR = path.resolve('transmit/public/assets/sprites/alien')
// Don't force dimensions - just scale down proportionally
const MAX_WIDTH = 400

const ANTI_DUPE = 'Generate exactly one single head image. Do not generate multiple versions.'

interface HeadCombo {
  name: string
  instruction: string
}

// Expression descriptions
const EYES = {
  neutral: 'relaxed neutral eyes looking forward, normal eyebrows',
  happy: 'slightly squinted happy/smiling eyes, raised cheeks',
  blink: 'eyes CLOSED as thin curved happy lines (blinking), relaxed eyebrows',
  surprised: 'extra wide open eyes, raised eyebrows high',
  eyeroll: 'eyes rolled up looking away, exasperated eyebrows, slight head tilt',
  skeptical: 'one eyebrow raised higher than the other, narrowed suspicious eyes',
  annoyed: 'flat narrowed eyes, furrowed brows, drooping eyelids showing impatience',
  smirk: 'sly knowing eyes, one side slightly more narrowed, raised eyebrow',
  sad: 'downcast eyes looking slightly down, worried upward-angled eyebrows',
  thinking: 'eyes looking up and to the side as if pondering',
  sideeye: 'eyes looking hard to one side while head faces forward, suspicious',
  lookRight: 'eyes looking to the right (viewer\'s left), head still forward',
  excited: 'extra wide sparkling eyes with highlight dots, raised eyebrows, joyful',
}

const MOUTHS = {
  smile: 'a friendly closed smile, lips curved upward',
  open: 'mouth wide open like saying "AH!", showing dark interior and teeth',
  oh: 'mouth in a round O shape, lips pursed like saying "ooh"',
  ee: 'a wide grin showing white teeth, like saying "cheese"',
  closed: 'lips pressed gently together, neutral',
  frown: 'lips curved downward in a frown/displeasure',
  small: 'mouth slightly open with a small gap between lips, like "uh"',
}

const BASE_INSTRUCTION = `Change ONLY the facial expression on this head. CRITICAL: Keep the EXACT same size, position, and framing as the input - do NOT zoom in, do NOT crop differently, do NOT resize. The head must stay in the EXACT same position and scale. The antennae, hair outline, and overall silhouette must remain identical. Only change the eyes, eyebrows, and mouth. Same character, same art style, same magenta #FF00FF background. No neck. ${ANTI_DUPE}`

// All expression + mouth combos
const HEADS: HeadCombo[] = [
  // Neutral
  { name: 'neutral-smile', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.neutral}. Mouth: ${MOUTHS.smile}.` },
  { name: 'neutral-open', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.neutral}. Mouth: ${MOUTHS.open}.` },
  { name: 'neutral-oh', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.neutral}. Mouth: ${MOUTHS.oh}.` },
  { name: 'neutral-closed', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.neutral}. Mouth: ${MOUTHS.closed}.` },
  { name: 'neutral-small', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.neutral}. Mouth: ${MOUTHS.small}.` },
  // Happy
  { name: 'happy-smile', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.happy}. Mouth: ${MOUTHS.smile}.` },
  { name: 'happy-open', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.happy}. Mouth: ${MOUTHS.open}.` },
  { name: 'happy-oh', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.happy}. Mouth: ${MOUTHS.oh}.` },
  { name: 'happy-ee', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.happy}. Mouth: ${MOUTHS.ee}.` },
  // Blink
  { name: 'blink-smile', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.blink}. Mouth: ${MOUTHS.smile}.` },
  // Surprised
  { name: 'surprised-open', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.surprised}. Mouth: ${MOUTHS.open}.` },
  { name: 'surprised-oh', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.surprised}. Mouth: ${MOUTHS.oh}.` },
  // Eyeroll
  { name: 'eyeroll-closed', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.eyeroll}. Mouth: ${MOUTHS.closed}.` },
  { name: 'eyeroll-frown', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.eyeroll}. Mouth: ${MOUTHS.frown}.` },
  // Skeptical
  { name: 'skeptical-smile', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.skeptical}. Mouth: ${MOUTHS.smile}.` },
  { name: 'skeptical-closed', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.skeptical}. Mouth: ${MOUTHS.closed}.` },
  // Annoyed
  { name: 'annoyed-closed', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.annoyed}. Mouth: ${MOUTHS.closed}.` },
  { name: 'annoyed-frown', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.annoyed}. Mouth: ${MOUTHS.frown}.` },
  // Smirk
  { name: 'smirk-smile', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.smirk}. Mouth: ${MOUTHS.smile}.` },
  { name: 'smirk-ee', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.smirk}. Mouth: ${MOUTHS.ee}.` },
  // Sad
  { name: 'sad-closed', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.sad}. Mouth: ${MOUTHS.closed}.` },
  { name: 'sad-frown', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.sad}. Mouth: ${MOUTHS.frown}.` },
  // Thinking
  { name: 'thinking-oh', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.thinking}. Mouth: ${MOUTHS.oh}.` },
  { name: 'thinking-closed', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.thinking}. Mouth: ${MOUTHS.closed}.` },
  { name: 'thinking-small', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.thinking}. Mouth: ${MOUTHS.small}.` },
  // Sideeye
  { name: 'sideeye-closed', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.sideeye}. Mouth: ${MOUTHS.closed}.` },
  // Look right
  { name: 'lookright-smile', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.lookRight}. Mouth: ${MOUTHS.smile}.` },
  { name: 'lookright-closed', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.lookRight}. Mouth: ${MOUTHS.closed}.` },
  // Excited
  { name: 'excited-open', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.excited}. Mouth: ${MOUTHS.open}.` },
  { name: 'excited-ee', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.excited}. Mouth: ${MOUTHS.ee}.` },
  { name: 'excited-oh', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.excited}. Mouth: ${MOUTHS.oh}.` },
  // Extra speech combos (for smooth talk animation cycling)
  { name: 'neutral-ee', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.neutral}. Mouth: ${MOUTHS.ee}.` },
  { name: 'neutral-frown', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.neutral}. Mouth: ${MOUTHS.frown}.` },
  { name: 'happy-closed', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.happy}. Mouth: ${MOUTHS.closed}.` },
  { name: 'happy-small', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.happy}. Mouth: ${MOUTHS.small}.` },
  // Extra reactions
  { name: 'surprised-ee', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.surprised}. Mouth: ${MOUTHS.ee}.` },
  { name: 'eyeroll-smile', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.eyeroll}. Mouth: ${MOUTHS.smile}.` },
  { name: 'annoyed-small', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.annoyed}. Mouth: ${MOUTHS.small}.` },
  { name: 'sad-oh', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.sad}. Mouth: ${MOUTHS.oh}.` },
  { name: 'sad-small', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.sad}. Mouth: ${MOUTHS.small}.` },
  { name: 'smirk-closed', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.smirk}. Mouth: ${MOUTHS.closed}.` },
  // Extra gaze directions
  { name: 'lookright-open', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.lookRight}. Mouth: ${MOUTHS.open}.` },
  { name: 'lookright-oh', instruction: `${BASE_INSTRUCTION} Eyes: ${EYES.lookRight}. Mouth: ${MOUTHS.oh}.` },
]

async function removeMagentaAndProcess(inputPath: string, outputPath: string): Promise<void> {
  const image = sharp(inputPath)
  const { data, info } = await image.raw().toBuffer({ resolveWithObject: true })
  const buf = Buffer.alloc(info.width * info.height * 4)

  for (let i = 0; i < info.width * info.height; i++) {
    const s = i * info.channels, d = i * 4
    const r = data[s], g = data[s + 1], b = data[s + 2]
    buf[d] = r; buf[d + 1] = g; buf[d + 2] = b
    buf[d + 3] = (r > 180 && g < 100 && b > 180) ? 0 : 255
  }

  // No trim - preserve position and aspect ratio so all heads align when swapped
  await sharp(buf, { raw: { width: info.width, height: info.height, channels: 4 } })
    .resize(MAX_WIDTH, null, { fit: 'inside', withoutEnlargement: true })
    .png().toFile(outputPath)
}

async function generate(combo: HeadCombo, srcBase64: string, srcMime: string): Promise<boolean> {
  const rawPath = path.join(OUTPUT_DIR, `${combo.name}-raw.png`)
  const finalPath = path.join(OUTPUT_DIR, `${combo.name}.png`)

  console.log(`  ${combo.name}...`)
  const result = await editImage(srcBase64, srcMime, combo.instruction)

  if (result.result !== 'success' || !result.imageBytes) {
    console.error(`    FAILED: ${result.error || result.result}`)
    return false
  }

  await fs.writeFile(rawPath, Buffer.from(result.imageBytes, 'base64'))
  await removeMagentaAndProcess(rawPath, finalPath)
  console.log(`    OK`)
  return true
}

async function main() {
  const args = process.argv.slice(2)
  const toGen = args.length ? HEADS.filter(h => args.includes(h.name)) : HEADS

  console.log(`=== Generating ${toGen.length} full heads from ${path.basename(HEAD_SOURCE)} ===`)

  const srcBuf = await fs.readFile(HEAD_SOURCE)
  const srcBase64 = srcBuf.toString('base64')
  const srcMime = getMimeType(HEAD_SOURCE)

  let ok = 0, fail = 0
  for (const combo of toGen) {
    (await generate(combo, srcBase64, srcMime)) ? ok++ : fail++
  }

  console.log(`\n=== Done: ${ok} ok, ${fail} failed ===`)
}

main().catch(e => { console.error('Fatal:', e); process.exit(1) })
