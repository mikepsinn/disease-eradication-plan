# Cartoon Style Bible: "How to End War and Disease (for Busy People)"

This file goes with the scene script (`cartoon-script.md`). It sets the look, the characters, and the recurring gags. Use it to brief illustrators, animators, and image tools.

The audiobook MP3 is the voice track. Do not record new narration. All times in the script are times in that MP3.

---

## 1. Look

The episode uses two visual layers. Each layer has a different job.

### Layer A: Wishonia's office (the cosmic layer)

- Use this layer when Wishonia talks *to* the viewer: the opening, the jokes, the verdicts, and the ending.
- Match the podcast cover: 1970s retro sunburst rays (red, orange, yellow, periwinkle blue, cream), a half-sun on the horizon, and a neon cyan perspective grid floor.
- Use flat 2D shapes, thick dark outlines, and a slight paper-grain texture. Use gradients only on the sunburst.
- The office floats in space above Earth. It has a desk, a filing cabinet labeled **"EARTH: CASE #847"**, a coffee mug, and a large retro wall screen. The wall screen shows the Earth footage (Layer B).
- Wishonia's blue skin and orange dress already match the cover palette. Keep the sunburst behind Wishonia slightly darker, so that Wishonia stands out from it.

### Layer B: Earth evidence (the engraving layer)

- Use this layer when the audio describes what humans do: money, wars, the FDA, the treaty mechanics.
- Match the episode art: black-and-white engraved, cross-hatched, hand-drawn infographic style on cream paper. Use banners, pipes, funnels, factories, and labels with arrows.
- Use only **two** accent colors on top of the black and white:
  - **Murder-money red** (`#D7322B`) for weapons, war, and the money that funds them.
  - **Medicine teal** (`#1FA39A`) for clinical trials, cures, and the money that funds them.
- When the money moves from war to medicine, the paper changes from red to teal. This is the main visual idea of the whole episode.
- Wishonia can stay on screen in Layer B as a small talking head in a round corner frame ("PiP" in the script).

### Text on screen

- Big numbers use a heavy retro serif (like the cover title), in black with a cream outline.
- **Use the numbers the narrator says.** The audiobook edition has some different figures from the current website (for example 97 million war deaths, 13,000 warheads, 3,070 : 1). The script already uses the audio figures.
- Chapter title cards use Layer A: the sunburst, the grid floor, and the title in the cover font. The chapter list is at the top of the script.
- Keep on-screen text short. The narrator says the words; the screen shows the number or the label.

### Motion

- Use limited animation. Most shots are illustrated plates with slow push-ins and pans, plus a few looping actions (2–4 frames).
- Animate the paper money a lot. It is the main "actor" of Layer B: it walks, runs, flows through pipes, and changes color.
- **HOLD** on dark facts. When the audio states a death toll, stop all motion for 1–2 seconds. Do not add jokes on top of those lines.

---

## 2. Wishonia (use the existing sprites)

Wishonia already has a full sprite set. Use it. Do not redesign the character.

- **Where the sprites are:** the originals are in `mikepsinn/disease-eradication-plan` (branch `develop`) → `transmit/public/assets/sprites/alien/`, at full resolution (heads 1024×1024, bodies 1343×768). The 12 seed images that the sprites were made from are in `alien/sources/`. `mikepsinn/optimitron` has reduced copies in `apps/optimitron/public/sprites/wishonia/` (some are only 512 px). **Use the originals for video.** A contact sheet of all 59 sprites, with their file names, is next to this file: `wishonia-contact-sheet.png`.
- **Design:** blue skin, a black bob haircut with straight bangs, two thin antennae with ball tips, large eyes with dark lashes. An orange 1960s-style mod dress with a darker swirl pattern and a small white brooch at the neck. Blue arms.
- **Name on screen:** "WISHONIA." The full name is "World Integrated System for High-efficiency Optimization Networked Intelligence and Allocation" (the audio spells it out at 04:15).

### How the sprites fit together

- **Heads (44 files):** `{expression}-{mouth}.png`. The expression sets the eyes and brows. The mouth shape changes for lip-sync.
- **Bodies (15 files):** `body-{pose}.png`, without a head. Put the head on top of the body at the neck.
- **Expressions and their mouth shapes** (the same table as `packages/wishonia-widget/src/core/viseme-map.ts`):

| Expression | Mouth shapes available | Use it for |
|---|---|---|
| `neutral` | smile, open, oh, ee, closed, small, frown | default narration |
| `happy` | smile, open, oh, ee, closed, small | good news, warm lines |
| `excited` | open, ee, oh, closed | big reveals, "money volcano" |
| `smirk` | smile, ee, closed | the dry jokes (most punchlines) |
| `skeptical` | smile, closed | "I can see your expression…" |
| `eyeroll` | closed, frown, smile | human foolishness |
| `sideeye` | closed | "This is why aliens don't visit." |
| `annoyed` | closed, frown, small | "I cannot believe I have to explain this" |
| `thinking` | oh, closed, small | explaining mechanisms |
| `surprised` | open, oh, ee | "You can imagine my surprise…" |
| `sad` | closed, frown, oh, small | death tolls (when Wishonia is on screen) |
| `lookright` | smile, closed, open, oh | looking at the wall screen |
| `blink` | smile | idle blinks, the last "Love you. Bye." |

- **Body poses:** `idle`, `presenting`, `point-right`, `open-palms`, `palms-down`, `arms-crossed`, `counting`, `excited`, `fist`, `hand-chest`, `hands-hips`, `listening`, `shrug`, `thinking`, `wide-gesture`.
- **Layout (from `transmit/public/assets/js/characters.js`):** make the head 95% of the character's width, centered. Put the body under it at the full character width. Move the body up so that it overlaps the head by about 9% of the character's width (−12 px at 140 px wide). The head goes in front of the body.
- **Idle motion (same file):** the head rocks slowly from −2° to +2° and up 2 px, on a 7-second loop. Every few seconds, show `blink-smile` for one short moment, then return to the resting head.
- **In the script:** each Wishonia line gives `expression-mouth` + `body-pose`, for example `smirk-smile` + `body-hands-hips`. The given mouth is the resting mouth. While Wishonia talks, swap the mouth by lip-sync (below), and go back to the resting mouth in pauses.

### Lip-sync

The narration is the audiobook, so the mouth must follow that audio. Two ways, both already in the Optimitron code:

1. **From the audio level** (simplest): measure the loudness of the MP3 about 24 times a second and pick the mouth with `amplitudeToViseme`: quiet → `closed`, then `small`, `oh`, `open`, and loudest → `ee`.
2. **From the words** (more exact): `word-timings.json` gives the start and end of every word. Spread each word's letters across its duration and map each letter with `CHAR_TO_VISEME` (vowels → open/ee/oh; b, m, p, f, v → closed; most other letters → small).

If an expression does not have the chosen mouth, use `getHeadName` from the same file. It falls back to an available mouth.

---

## 3. Other characters

All of these are original designs for this project. Do not base them on characters from other cartoons.

### The Humans ("meat robots")

- Simple, rounded bean-shaped bodies, short arms and legs, dot eyes. Small rivets at the elbows and knees (the "meat robot" joke).
- Each human has a small round **"check engine" light** on the chest. It blinks red when a disease starts. Use this gentle sign in place of any image of sickness.
- Use many skin tones and hair shapes.

### The Papers (money)

- Small paper rectangles with stick legs and a tiny oval portrait of a generic, unnamed old man in a wig. Do not copy any real banknote.
- Red papers = murder money. Teal papers = medicine money.
- They run toward whoever calls them. They form lines, crowds, and rivers. They jump into funnels.

### Recurring Earth characters

| Character | Design | Used in |
|---|---|---|
| The Rich Human | Bean human in a top hat, sitting on a hill of papers. Later wears a button: "I PREFER LIVING." | Quiz, Paper Distribution, bonds |
| The Loud Human | Bean human with a megaphone instead of a head. | Step 2 (marketing) |
| The Lobbyist | Bean human with a briefcase that has a funnel on top. | Paper Distribution, Bribe the Bribers |
| The Politician | Bean human with a very wide tie. The tie flips between red and blue (the "red team / blue team" gag). | Leaders, Purchase Democracy |
| The Weapons Maker | Bean human in a hard hat. Factory chimneys are shaped like missiles. | Leaders loop, Enjoy |
| The Orderly | Very tall bean human in white scrubs, sliding a medicine cup through a door slot. | Institutionalize scene |
| Grandma | Bean human with hair curlers, holding a 1940s war-bond poster. | What Grandma got |
| The Democracy Dog | A round dog chasing its own tail. The tail is made of papers; later it is made of teal pills. | Leaders loop |
| The Optimitron | A 1970s countertop appliance (a toaster–microwave hybrid) with two big dials: **HEALTH** and **WEALTH**. Policy cards pop out of it like toast. | Optimitron, Step 1 |
| The Calculator | A desk calculator with eyes. It shows "ERROR," screams, and walks off the desk. | The Math |
| The Countdown Board | A retro flip-number board: "HUMANS TERMINATED BY CURABLE DISEASES SINCE THIS VIDEO STARTED." It counts about 1.7 per second (104 per minute). | Hello human, The Problem, Closing |

### Rules for sensitive content

- The audio mentions the Holocaust and Nazis, 9/11, a crucifixion, a mass shooting, a dying child, and war deaths. Show these as plain text cards or as empty, quiet scenes. Do not draw victims, Nazis, uniforms, weapons in use, religious figures, or a sick child.
- Never draw real, identifiable politicians, executives, companies, or brand logos. Use the generic bean humans and plain signs. Real names (Eisenhower, Erica Chenoweth) appear as text only.
- Weapons can be silly objects (missiles with price tags, a submarine in a field). Never show a weapon hitting a person.

---

## 4. Recurring gags and devices

1. **The 604 bar.** A tall red stack of papers next to one small teal paper. It returns every time the audio says "604."
2. **The color flip.** Red paper goes into a funnel and comes out teal. Use it every time money is "redirected."
3. **The countdown board.** It sits in a corner during the opening and the ending.
4. **Wishonia's mug sip.** Before a big punchline, Wishonia sips coffee. After the punchline, Wishonia puts the mug down slowly.
5. **The case file.** Wishonia stamps the Earth case file: "SUBOPTIMAL" (after the FDA part) and finally "ELIGIBLE FOR OPTIMIZATION" (the ending).
6. **Chapter cards.** Each part starts with a 2-second sunburst title card.

---

## 5. Image-generator prompts (starting points)

Add the scene details from the script to these base prompts. For Wishonia, put the real sprites into the scene. Do not generate a new Wishonia.

- **Layer A background:** "flat 2D cartoon background, 1970s retro poster style, sunburst rays in red orange yellow periwinkle and cream, neon cyan perspective grid floor, thick dark outlines, paper grain texture, floating space office above Earth with a desk and a large retro wall screen, no characters"
- **Layer B base:** "black and white engraved cross-hatched infographic illustration on cream paper, vintage hand-drawn diagram with labels, banners and arrows, single accent colors red (#D7322B) and teal (#1FA39A)"
- **Humans:** "simple rounded bean-shaped cartoon people, short limbs, dot eyes, small rivets at elbows and knees, small round light on the chest, engraved line style"
- **Papers:** "small walking paper money rectangles with stick legs and a tiny generic oval portrait, engraved line style, red paper and teal paper"

---

## 6. Building it with the existing video pipeline

`mikepsinn/optimitron/videos/care-integrated-clinical-trials` already renders narrated explainers with HyperFrames (HTML + GSAP → MP4). It supports a recorded voice with word timings in place of text-to-speech. For this episode:

- Use the audiobook MP3 as the voice, and `word-timings.json` for the word timings and captions.
- Build each scene from the script as one HyperFrames composition.
- Drive Wishonia's mouth with `amplitudeToViseme` or `CHAR_TO_VISEME` (section 2).
- A 62-minute render is long. Render each part (chapter) on its own, then join the parts with ffmpeg.
