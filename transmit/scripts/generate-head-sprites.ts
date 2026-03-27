#!/usr/bin/env tsx
/**
 * Generate Wishonia character sprite set.
 * Layered system: head bases (no mouth) + mouth shapes + body poses
 *
 * Usage:
 *   npx tsx transmit/scripts/generate-head-sprites.ts              # all sprites
 *   npx tsx transmit/scripts/generate-head-sprites.ts heads        # just head bases
 *   npx tsx transmit/scripts/generate-head-sprites.ts mouths       # just mouth shapes
 *   npx tsx transmit/scripts/generate-head-sprites.ts bodies       # just body poses
 *   npx tsx transmit/scripts/generate-head-sprites.ts head-base-neutral mouth-smile  # specific sprites
 */

import fs from 'fs/promises'
import path from 'path'
import sharp from 'sharp'
import { editImage } from '../../scripts/lib/gemini-images'
import { getMimeType } from '../../scripts/lib/image-file-utils'

const REFERENCE_IMAGE = path.resolve('assets/music-video/keyframes/scene-09.jpg')
const OUTPUT_DIR = path.resolve('transmit/public/assets/sprites/alien')

const CHARACTER = 'the cute blue-skinned alien girl named Wishonia with black 60s bob haircut (with pointed inward-curling tips at chin level) and blue antennae with ball tips, from this illustration'
const HEAD_COMMON = `on a solid bright magenta #FF00FF background. Remove body, computer, monitor, desk, and all background elements. ONLY the head from neck up, centered. The black bob hair MUST show pointed tips curling inward at chin level on both sides.`
const MOUTH_COMMON = `Draw ONLY the mouth/lips area of ${CHARACTER} on a solid bright magenta #FF00FF background. The mouth should be a small isolated element, roughly 80x40 pixels in the center of the image. Nothing else - no face, no chin, no nose. Just the lips/mouth shape in the same blue skin and art style.`
const BODY_COMMON = `of ${CHARACTER} from neck down, standing upright facing forward. Show her neck, shoulders, torso, and her orange/blue patterned sleeveless dress to mid-thigh. NO head. Place centered on solid bright magenta #FF00FF background. Same illustrated art style.`

interface SpriteDefinition {
  name: string
  category: 'heads' | 'mouths' | 'bodies'
  instruction: string
  size: { w: number, h: number }  // output size after trim
}

const SPRITES: SpriteDefinition[] = [
  // ─── HEAD BASES (no mouth) ──────────────────────────────────────
  // Tier 1 - Essential
  { name: 'head-base-neutral', category: 'heads', size: { w: 200, h: 250 },
    instruction: `Extract just the head of ${CHARACTER}. Show her with a NEUTRAL resting expression - eyes forward, relaxed eyebrows, NO MOUTH (leave the mouth area as plain blue skin). ${HEAD_COMMON}` },
  { name: 'head-base-happy', category: 'heads', size: { w: 200, h: 250 },
    instruction: `Extract just the head of ${CHARACTER}. Show her with a HAPPY expression - eyes slightly squinted/smiling, raised cheeks, NO MOUTH (leave the mouth area as plain blue skin). ${HEAD_COMMON}` },
  { name: 'head-base-blink', category: 'heads', size: { w: 200, h: 250 },
    instruction: `Extract just the head of ${CHARACTER}. Show her with eyes CLOSED (thin curved happy lines as if blinking contentedly), relaxed eyebrows, NO MOUTH (leave the mouth area as plain blue skin). ${HEAD_COMMON}` },
  { name: 'head-base-surprised', category: 'heads', size: { w: 200, h: 250 },
    instruction: `Extract just the head of ${CHARACTER}. Show her with a SURPRISED expression - extra wide open eyes, raised eyebrows high, NO MOUTH (leave the mouth area as plain blue skin). ${HEAD_COMMON}` },
  // Tier 2 - Comedy/Personality
  { name: 'head-base-eyeroll', category: 'heads', size: { w: 200, h: 250 },
    instruction: `Extract just the head of ${CHARACTER}. Show her ROLLING HER EYES - pupils looking up/away, slight head tilt, exasperated eyebrows, NO MOUTH (leave the mouth area as plain blue skin). Classic "humans are ridiculous" expression. ${HEAD_COMMON}` },
  { name: 'head-base-skeptical', category: 'heads', size: { w: 200, h: 250 },
    instruction: `Extract just the head of ${CHARACTER}. Show her with a SKEPTICAL expression - one eyebrow raised higher than the other, eyes slightly narrowed with suspicion, NO MOUTH (leave the mouth area as plain blue skin). ${HEAD_COMMON}` },
  { name: 'head-base-annoyed', category: 'heads', size: { w: 200, h: 250 },
    instruction: `Extract just the head of ${CHARACTER}. Show her ANNOYED/FED UP - flat narrowed eyes, furrowed brows, drooping eyelids showing impatience, NO MOUTH (leave the mouth area as plain blue skin). ${HEAD_COMMON}` },
  { name: 'head-base-smirk', category: 'heads', size: { w: 200, h: 250 },
    instruction: `Extract just the head of ${CHARACTER}. Show her with a SLY SMIRK expression - knowing eyes, one side slightly more narrowed than the other, raised eyebrow, NO MOUTH (leave the mouth area as plain blue skin). "I told you so" face. ${HEAD_COMMON}` },
  // Tier 3 - Video/Extended
  { name: 'head-base-sad', category: 'heads', size: { w: 200, h: 250 },
    instruction: `Extract just the head of ${CHARACTER}. Show her with a SAD/CONCERNED expression - downcast eyes looking slightly down, worried upward-angled eyebrows, NO MOUTH (leave the mouth area as plain blue skin). ${HEAD_COMMON}` },
  { name: 'head-base-thinking', category: 'heads', size: { w: 200, h: 250 },
    instruction: `Extract just the head of ${CHARACTER}. Show her THINKING - eyes looking up and to the side as if pondering something, slightly raised eyebrows, NO MOUTH (leave the mouth area as plain blue skin). ${HEAD_COMMON}` },
  { name: 'head-base-excited', category: 'heads', size: { w: 200, h: 250 },
    instruction: `Extract just the head of ${CHARACTER}. Show her EXCITED/EUREKA - extra wide sparkling eyes with highlight dots, raised eyebrows, energetic expression, NO MOUTH (leave the mouth area as plain blue skin). ${HEAD_COMMON}` },
  { name: 'head-base-sideeye', category: 'heads', size: { w: 200, h: 250 },
    instruction: `Extract just the head of ${CHARACTER}. Show her giving SIDE-EYE - eyes looking hard to one side while head faces forward, one eyebrow slightly raised, suspicious/judging, NO MOUTH (leave the mouth area as plain blue skin). ${HEAD_COMMON}` },
  { name: 'head-base-look-left', category: 'heads', size: { w: 200, h: 250 },
    instruction: `Extract just the head of ${CHARACTER}. Eyes looking to the LEFT (her left, viewer's right), head still facing mostly forward, neutral eyebrows, NO MOUTH (leave the mouth area as plain blue skin). ${HEAD_COMMON}` },
  { name: 'head-base-look-right', category: 'heads', size: { w: 200, h: 250 },
    instruction: `Extract just the head of ${CHARACTER}. Eyes looking to the RIGHT (her right, viewer's left), head still facing mostly forward, neutral eyebrows, NO MOUTH (leave the mouth area as plain blue skin). ${HEAD_COMMON}` },

  // ─── MOUTH SHAPES ───────────────────────────────────────────────
  { name: 'mouth-closed', category: 'mouths', size: { w: 80, h: 50 },
    instruction: `${MOUTH_COMMON} The mouth should be CLOSED - lips pressed gently together in a neutral position. Dark blue-tinted lips on blue skin.` },
  { name: 'mouth-small', category: 'mouths', size: { w: 80, h: 50 },
    instruction: `${MOUTH_COMMON} The mouth should be SLIGHTLY OPEN - small opening between the lips, like saying "uh" or "eh". Dark blue-tinted lips on blue skin.` },
  { name: 'mouth-open', category: 'mouths', size: { w: 80, h: 50 },
    instruction: `${MOUTH_COMMON} The mouth should be WIDE OPEN - big open mouth like saying "AH!", showing the dark interior. Dark blue-tinted lips on blue skin, teeth visible at top.` },
  { name: 'mouth-oh', category: 'mouths', size: { w: 80, h: 50 },
    instruction: `${MOUTH_COMMON} The mouth should be in a round O SHAPE - lips pursed in a circle, like saying "ooh" or "oh". Dark blue-tinted lips on blue skin.` },
  { name: 'mouth-ee', category: 'mouths', size: { w: 80, h: 50 },
    instruction: `${MOUTH_COMMON} The mouth should be in a wide EE/SMILE shape - wide grin showing teeth, like saying "cheese" or "ee". Dark blue-tinted lips on blue skin, white teeth visible.` },
  { name: 'mouth-fv', category: 'mouths', size: { w: 80, h: 50 },
    instruction: `${MOUTH_COMMON} The mouth should show an F/V shape - top teeth biting gently on the lower lip, like saying "fff" or "vvv". Dark blue-tinted lips on blue skin.` },
  { name: 'mouth-smile', category: 'mouths', size: { w: 80, h: 50 },
    instruction: `${MOUTH_COMMON} The mouth should be a friendly CLOSED SMILE - lips curved upward in a warm smile, no teeth showing. Dark blue-tinted lips on blue skin.` },

  // ─── BODY POSES ─────────────────────────────────────────────────
  // Conversational
  { name: 'body-idle', category: 'bodies', size: { w: 300, h: 400 },
    instruction: `Draw the body ${BODY_COMMON} Arms relaxed, hands clasped gently in front of her body. Natural, comfortable standing pose.` },
  { name: 'body-listening', category: 'bodies', size: { w: 300, h: 400 },
    instruction: `Draw the body ${BODY_COMMON} Arms folded across her chest in an attentive listening pose. Looks engaged and thoughtful.` },
  { name: 'body-typing', category: 'bodies', size: { w: 400, h: 400 },
    instruction: `Draw ${CHARACTER} from neck down, SEATED at a desk/workstation. Hands on keyboard/controls, leaning slightly forward. Show her orange/blue dress, the desk surface, and her arms typing. Place on solid bright magenta #FF00FF background. NO head.` },
  // TED Talk
  { name: 'body-open-palms', category: 'bodies', size: { w: 300, h: 400 },
    instruction: `Draw the body ${BODY_COMMON} Both hands raised to chest height with PALMS FACING OUTWARD toward the viewer, fingers spread. Trust/transparency gesture like saying "here's the truth".` },
  { name: 'body-point-right', category: 'bodies', size: { w: 350, h: 400 },
    instruction: `Draw the body ${BODY_COMMON} RIGHT arm fully extended pointing to the right side, index finger pointing. Left arm relaxed at side. Directing attention to something off-screen.` },
  { name: 'body-wide-gesture', category: 'bodies', size: { w: 400, h: 400 },
    instruction: `Draw the body ${BODY_COMMON} Both arms spread WIDE to the sides, palms up, like presenting something huge or saying "imagine this!" Big expansive gesture.` },
  { name: 'body-counting', category: 'bodies', size: { w: 300, h: 400 },
    instruction: `Draw the body ${BODY_COMMON} One hand raised with index finger pointing up, as if making a first point or counting "number one". Other hand at side. Listing/counting gesture.` },
  { name: 'body-fist', category: 'bodies', size: { w: 300, h: 400 },
    instruction: `Draw the body ${BODY_COMMON} One fist raised to shoulder height, showing determination and resolve. "We must act!" power gesture. Other arm at side.` },
  { name: 'body-palms-down', category: 'bodies', size: { w: 300, h: 400 },
    instruction: `Draw the body ${BODY_COMMON} Both hands in front at waist height, palms facing DOWN, pressing downward. Calming "let me explain" gesture.` },
  { name: 'body-presenting', category: 'bodies', size: { w: 350, h: 400 },
    instruction: `Draw the body ${BODY_COMMON} Both hands raised outward and up at chest height, palms up, in an inviting welcoming gesture. Like saying "join us" or presenting something wonderful.` },
  // Emotional/Character
  { name: 'body-hand-chest', category: 'bodies', size: { w: 300, h: 400 },
    instruction: `Draw the body ${BODY_COMMON} One hand placed on her chest/heart area, other arm relaxed. Heartfelt, personal, sincere gesture.` },
  { name: 'body-shrug', category: 'bodies', size: { w: 350, h: 400 },
    instruction: `Draw the body ${BODY_COMMON} Classic SHRUG pose - both arms out to sides, palms up, shoulders raised. "I don't understand you humans" gesture.` },
  { name: 'body-hands-hips', category: 'bodies', size: { w: 300, h: 400 },
    instruction: `Draw the body ${BODY_COMMON} Both hands on hips, elbows out. Assertive, confident "well?" stance.` },
  { name: 'body-arms-crossed', category: 'bodies', size: { w: 300, h: 400 },
    instruction: `Draw the body ${BODY_COMMON} Arms CROSSED tightly across chest. Skeptical, challenging, "prove it to me" posture.` },
  { name: 'body-thinking', category: 'bodies', size: { w: 300, h: 400 },
    instruction: `Draw the body ${BODY_COMMON} One hand raised to chin/face area as if thinking deeply, other arm supporting the thinking elbow. Contemplative pose.` },
  { name: 'body-excited', category: 'bodies', size: { w: 350, h: 400 },
    instruction: `Draw the body ${BODY_COMMON} Both arms raised UP high in celebration/excitement! Eureka moment, victory pose.` },
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

  const tmp1 = outputPath + '.t1.png'
  const tmp2 = outputPath + '.t2.png'

  await sharp(buf, { raw: { width: info.width, height: info.height, channels: 4 } }).png().toFile(tmp1)
  await sharp(tmp1).trim().png().toFile(tmp2)
  await sharp(tmp2)
    .extend({ top: 10, bottom: 10, left: 10, right: 10, background: { r: 0, g: 0, b: 0, alpha: 0 } })
    .resize(size.w, size.h, { fit: 'contain', background: { r: 0, g: 0, b: 0, alpha: 0 } })
    .png()
    .toFile(outputPath)

  await fs.unlink(tmp1)
  await fs.unlink(tmp2)
}

async function generateSprite(sprite: SpriteDefinition, imageBase64: string, mimeType: string): Promise<boolean> {
  const rawPath = path.join(OUTPUT_DIR, `${sprite.name}-raw.png`)
  const finalPath = path.join(OUTPUT_DIR, `${sprite.name}.png`)

  console.log(`  [${sprite.category}] ${sprite.name}...`)

  const result = await editImage(imageBase64, mimeType, sprite.instruction)

  if (result.result !== 'success' || !result.imageBytes) {
    console.error(`    FAILED: ${result.error || result.result}`)
    return false
  }

  await fs.writeFile(rawPath, Buffer.from(result.imageBytes, 'base64'))
  await removeMagentaAndProcess(rawPath, finalPath, sprite.size)
  console.log(`    OK -> ${sprite.name}.png`)
  return true
}

async function main() {
  const args = process.argv.slice(2)

  // Determine which sprites to generate
  let toGenerate: SpriteDefinition[]
  if (args.length === 0) {
    toGenerate = SPRITES
  } else if (args.includes('heads')) {
    toGenerate = SPRITES.filter(s => s.category === 'heads')
  } else if (args.includes('mouths')) {
    toGenerate = SPRITES.filter(s => s.category === 'mouths')
  } else if (args.includes('bodies')) {
    toGenerate = SPRITES.filter(s => s.category === 'bodies')
  } else {
    toGenerate = SPRITES.filter(s => args.includes(s.name))
  }

  console.log(`=== Wishonia Sprite Generation (${toGenerate.length} sprites) ===`)

  const imageBuffer = await fs.readFile(REFERENCE_IMAGE)
  const imageBase64 = imageBuffer.toString('base64')
  const mimeType = getMimeType(REFERENCE_IMAGE)

  await fs.mkdir(OUTPUT_DIR, { recursive: true })

  let ok = 0, fail = 0
  for (const sprite of toGenerate) {
    (await generateSprite(sprite, imageBase64, mimeType)) ? ok++ : fail++
  }

  console.log(`\n=== Done: ${ok} ok, ${fail} failed ===`)
}

main().catch(e => { console.error('Fatal:', e); process.exit(1) })
