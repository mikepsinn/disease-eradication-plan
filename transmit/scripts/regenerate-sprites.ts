#!/usr/bin/env tsx
/**
 * Regenerate problem sprites using clean outputs as source images.
 * Key principle: edit good results instead of extracting from complex scenes.
 *
 * Usage:
 *   npx tsx transmit/scripts/regenerate-sprites.ts              # all
 *   npx tsx transmit/scripts/regenerate-sprites.ts mouths       # just mouths
 *   npx tsx transmit/scripts/regenerate-sprites.ts bodies       # just bodies
 *   npx tsx transmit/scripts/regenerate-sprites.ts heads        # just heads
 *   npx tsx transmit/scripts/regenerate-sprites.ts mouth-closed # specific sprite
 */

import fs from 'fs/promises'
import path from 'path'
import sharp from 'sharp'
import { editImage } from '../../scripts/lib/gemini-images'
import { getMimeType } from '../../scripts/lib/image-file-utils'

const SPRITE_DIR = path.resolve('transmit/public/assets/sprites/alien')

// Clean source images to edit FROM
const SOURCES = {
  mouthRef: path.join(SPRITE_DIR, 'mouth-small-raw.png'),     // good mouth to modify
  mouthRef2: path.join(SPRITE_DIR, 'mouth-ee-raw.png'),       // another good mouth
  headNeutral: path.join(SPRITE_DIR, 'head-base-neutral-raw.png'),
  headSurprised: path.join(SPRITE_DIR, 'head-base-surprised-raw.png'),
  bodyIdle: path.join(SPRITE_DIR, 'body-idle-raw.png'),
  headIdleFull: path.join(SPRITE_DIR, 'raw-archive/head-idle-raw.png'), // full head with mouth
}

interface RegenTask {
  name: string
  category: 'mouths' | 'heads' | 'bodies'
  source: string  // key into SOURCES
  instruction: string
  size: { w: number, h: number }
}

const ANTI_DUPE = 'Generate exactly one single image, not multiple versions.'

const TASKS: RegenTask[] = [
  // ─── MOUTHS: Edit mouth-small-raw into other shapes ─────────
  { name: 'mouth-closed', category: 'mouths', source: 'mouthRef',
    size: { w: 80, h: 50 },
    instruction: `Change this mouth to have the lips pressed gently together, closed and neutral. Keep the same blue skin color and dark blue lip color and art style. Solid magenta #FF00FF background. ${ANTI_DUPE}` },
  { name: 'mouth-open', category: 'mouths', source: 'mouthRef',
    size: { w: 80, h: 50 },
    instruction: `Change this mouth to be WIDE OPEN like saying "AH!", showing dark interior, teeth at top, tongue visible. Keep same blue skin and dark blue lip style. Solid magenta #FF00FF background. ${ANTI_DUPE}` },
  { name: 'mouth-oh', category: 'mouths', source: 'mouthRef',
    size: { w: 80, h: 50 },
    instruction: `Change this mouth to a round O shape, lips pursed in a circle like saying "ooh". Keep same blue skin and dark blue lip style. Solid magenta #FF00FF background. ${ANTI_DUPE}` },
  { name: 'mouth-fv', category: 'mouths', source: 'mouthRef',
    size: { w: 80, h: 50 },
    instruction: `Change this mouth so the upper teeth are gently biting the lower lip, like saying "fff" or "vvv". Keep same blue skin and dark blue lip style. Solid magenta #FF00FF background. ${ANTI_DUPE}` },
  { name: 'mouth-small', category: 'mouths', source: 'mouthRef',
    size: { w: 80, h: 50 },
    instruction: `Change this mouth to be only very slightly open with a small gap between the lips, like a relaxed "uh". Keep same blue skin and dark blue lip style. Solid magenta #FF00FF background. ${ANTI_DUPE}` },

  // ─── HEADS: Edit clean heads into missing expressions ───────
  { name: 'head-base-excited', category: 'heads', source: 'headSurprised',
    size: { w: 200, h: 250 },
    instruction: `Make the eyes even wider with sparkle/star highlights in them. More excited and joyful expression. Raise the eyebrows higher. Keep the same art style, hair, antennae. No mouth. Solid magenta #FF00FF background. ${ANTI_DUPE}` },
  { name: 'head-base-look-left', category: 'heads', source: 'headNeutral',
    size: { w: 200, h: 250 },
    instruction: `Move the pupils/irises to look to the left (the character's left, viewer's right). Keep everything else exactly the same - same face, hair, antennae, no mouth, same style. ${ANTI_DUPE}` },

  // ─── BODIES: Edit body-idle into other poses ────────────────
  { name: 'body-arms-crossed', category: 'bodies', source: 'bodyIdle',
    size: { w: 300, h: 400 },
    instruction: `Change her arms to be crossed over her chest. Keep the same dress, skin color, art style, and magenta background. No head. ${ANTI_DUPE}` },
  { name: 'body-listening', category: 'bodies', source: 'bodyIdle',
    size: { w: 300, h: 400 },
    instruction: `Change her arms to be folded across her chest in an attentive listening pose. Keep the same dress, skin color, art style, and magenta background. No head. ${ANTI_DUPE}` },
  { name: 'body-thinking', category: 'bodies', source: 'bodyIdle',
    size: { w: 300, h: 400 },
    instruction: `Move her right hand up to her chin as if thinking deeply. Left arm supports the right elbow. Keep the same dress, skin color, art style, and magenta background. No head. ${ANTI_DUPE}` },
  { name: 'body-excited', category: 'bodies', source: 'bodyIdle',
    size: { w: 350, h: 400 },
    instruction: `Raise both her arms up high above her shoulders in celebration. Keep the same dress, skin color, art style, and magenta background. No head. ${ANTI_DUPE}` },
  { name: 'body-point-right', category: 'bodies', source: 'bodyIdle',
    size: { w: 350, h: 400 },
    instruction: `Extend her right arm fully to the right side, index finger pointing. Left arm relaxed at her side. Keep the same dress, skin color, art style, and magenta background. No head. ${ANTI_DUPE}` },
  { name: 'body-open-palms', category: 'bodies', source: 'bodyIdle',
    size: { w: 300, h: 400 },
    instruction: `Raise both hands to chest height with palms facing outward toward the viewer, fingers spread. Keep the same dress, skin color, art style, position, and magenta background. No head. ${ANTI_DUPE}` },
  { name: 'body-wide-gesture', category: 'bodies', source: 'bodyIdle',
    size: { w: 400, h: 400 },
    instruction: `Spread both arms wide to the sides, palms up. Big expansive gesture. Keep the same dress, skin color, art style, position, and magenta background. No head. ${ANTI_DUPE}` },
  { name: 'body-counting', category: 'bodies', source: 'bodyIdle',
    size: { w: 300, h: 400 },
    instruction: `Raise one hand with index finger pointing up, as if making a point. Other hand at side. Keep the same dress, skin color, art style, position, and magenta background. No head. ${ANTI_DUPE}` },
  { name: 'body-fist', category: 'bodies', source: 'bodyIdle',
    size: { w: 300, h: 400 },
    instruction: `Raise one fist to shoulder height showing determination. Other arm at side. Keep the same dress, skin color, art style, position, and magenta background. No head. ${ANTI_DUPE}` },
  { name: 'body-palms-down', category: 'bodies', source: 'bodyIdle',
    size: { w: 300, h: 400 },
    instruction: `Both hands in front at waist height, palms facing down, pressing downward. Calming gesture. Keep the same dress, skin color, art style, position, and magenta background. No head. ${ANTI_DUPE}` },
  { name: 'body-presenting', category: 'bodies', source: 'bodyIdle',
    size: { w: 350, h: 400 },
    instruction: `Both hands raised outward and up at chest height, palms up, in a welcoming gesture. Keep the same dress, skin color, art style, position, and magenta background. No head. ${ANTI_DUPE}` },
  { name: 'body-hand-chest', category: 'bodies', source: 'bodyIdle',
    size: { w: 300, h: 400 },
    instruction: `Place one hand on her chest/heart area, other arm relaxed. Sincere gesture. Keep the same dress, skin color, art style, position, and magenta background. No head. ${ANTI_DUPE}` },
  { name: 'body-hands-hips', category: 'bodies', source: 'bodyIdle',
    size: { w: 300, h: 400 },
    instruction: `Both hands on hips, elbows out. Assertive stance. Keep the same dress, skin color, art style, position, and magenta background. No head. ${ANTI_DUPE}` },
  { name: 'body-shrug', category: 'bodies', source: 'bodyIdle',
    size: { w: 350, h: 400 },
    instruction: `Both arms out to sides, palms up, shoulders raised in a classic shrug gesture. Keep the EXACT same position and size. Same dress, skin color, art style, and magenta background. No head. ${ANTI_DUPE}` },
  { name: 'body-typing', category: 'bodies', source: 'bodyIdle',
    size: { w: 400, h: 400 },
    instruction: `Change to a seated pose with hands on a desk/keyboard in front. Keep the same dress, skin color, art style, and magenta background. No head. ${ANTI_DUPE}` },
]

async function removeMagentaAndProcess(inputPath: string, outputPath: string, size: { w: number, h: number }): Promise<void> {
  const image = sharp(inputPath)
  const { data, info } = await image.raw().toBuffer({ resolveWithObject: true })
  const buf = Buffer.alloc(info.width * info.height * 4)

  for (let i = 0; i < info.width * info.height; i++) {
    const s = i * info.channels, d = i * 4
    const r = data[s], g = data[s + 1], b = data[s + 2]
    const isMagenta = r > 180 && g < 100 && b > 180
    buf[d] = r; buf[d + 1] = g; buf[d + 2] = b
    buf[d + 3] = isMagenta ? 0 : 255
  }

  // Full resolution, no trim, no resize - preserve exact position and dimensions
  await sharp(buf, { raw: { width: info.width, height: info.height, channels: 4 } })
    .png()
    .toFile(outputPath)
}

async function runTask(task: RegenTask): Promise<boolean> {
  const sourcePath = SOURCES[task.source as keyof typeof SOURCES]
  const rawPath = path.join(SPRITE_DIR, `${task.name}-raw.png`)
  const finalPath = path.join(SPRITE_DIR, `${task.name}.png`)

  console.log(`  [${task.category}] ${task.name} (from ${path.basename(sourcePath)})...`)

  const imageBuffer = await fs.readFile(sourcePath)
  const imageBase64 = imageBuffer.toString('base64')
  const mimeType = getMimeType(sourcePath)

  const result = await editImage(imageBase64, mimeType, task.instruction)

  if (result.result !== 'success' || !result.imageBytes) {
    console.error(`    FAILED: ${result.error || result.result}`)
    return false
  }

  await fs.writeFile(rawPath, Buffer.from(result.imageBytes, 'base64'))
  await removeMagentaAndProcess(rawPath, finalPath, task.size)
  console.log(`    OK -> ${task.name}.png`)
  return true
}

async function main() {
  const args = process.argv.slice(2)

  let tasks: RegenTask[]
  if (args.length === 0) {
    tasks = TASKS
  } else if (args.includes('mouths')) {
    tasks = TASKS.filter(t => t.category === 'mouths')
  } else if (args.includes('heads')) {
    tasks = TASKS.filter(t => t.category === 'heads')
  } else if (args.includes('bodies')) {
    tasks = TASKS.filter(t => t.category === 'bodies')
  } else {
    tasks = TASKS.filter(t => args.includes(t.name))
  }

  console.log(`=== Regenerating ${tasks.length} sprites ===`)

  let ok = 0, fail = 0
  for (const task of tasks) {
    (await runTask(task)) ? ok++ : fail++
  }

  console.log(`\n=== Done: ${ok} ok, ${fail} failed ===`)
}

main().catch(e => { console.error('Fatal:', e); process.exit(1) })
