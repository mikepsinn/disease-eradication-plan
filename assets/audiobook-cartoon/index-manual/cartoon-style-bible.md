# Cartoon Style Bible: "How to End War and Disease (for Busy People)"

This file goes with the scene script (`cartoon-script.md`). It sets the look, the characters, and the recurring gags. Use it to brief illustrators, animators, and image tools.

The audiobook MP3 is the voice track. Do not record new narration. All times in the script are times in that MP3.

---

## 1. Look

The episode uses two visual layers. Each layer has a different job. Both match the theme song music video that opens the episode, so the cartoon continues its look: mid-century flat illustration in its palette (measured from its keyframes): deep navy `#112845` and `#061D3E`, slate `#273049`, burnt orange `#E5903B`, cream `#F3ECD0`, rust `#904B2E`, tan `#B47E52`, with mustard `#E8B04A` stars. Flat shapes, atomic stars and boomerangs, and a fine print grain over every drawn frame.

### Layer A: Wishonia's office (the cosmic layer)

- Use this layer when Wishonia talks *to* the viewer: the opening, the jokes, the verdicts, and the ending.
- A navy wall with slate and deep-navy geometric panels, mustard and cream atomic stars and orange boomerangs; a rising orange sun on the horizon; a tiled floor.
- Use flat 2D shapes and dark navy outlines. No gradients.
- The office floats in space above Earth. It has a desk, a filing cabinet labeled **"EARTH: CASE #847"**, a coffee mug, and a large retro wall screen. The wall screen shows the Earth footage (Layer B).
- Wishonia's blue skin and orange dress already match the palette. A mustard disc behind Wishonia's head makes Wishonia stand out from the navy wall.

### Layer B: Earth evidence (the diagram layer)

- Use this layer when the audio describes what humans do: money, wars, the FDA, the treaty mechanics.
- Flat cream paper diagrams in the music video's printed style: navy lines, halftone-dot fills (in place of cross-hatching), a few orange and mustard stars. Use banners, pipes, funnels, factories, and labels with arrows.
- Money is always **money green** (`KIT.C.money`), like a real bill, so nobody has to learn what a red rectangle means.
- Two accent colors say what the money buys:
  - **Murder-money red** (`#C8452E`) for weapons and war: war money carries a red seal with a little missile.
  - **Medicine teal** (`#2F8F86`) for clinical trials and cures: medicine money carries a teal seal with a white cross.
- When the money moves from war to medicine, the bill's seal flips from the red missile to the teal cross. This is the main visual idea of the whole episode. Where a storyboard says "red papers" it means war money (green, red seal), and "teal papers" means medicine money (green, teal seal).
- Wishonia can stay on screen in Layer B ("PiP" in the script). In 16:9 she stands in the bottom right corner, cut off at the thighs by the frame's bottom edge; in 9:16, where the captions and the apps' buttons fill the bottom, she rides a small 1950s flying saucer at the top right. Both show her whole gesture body (pointing, shrugging, arms crossed), mirrored so she points into the frame at what she is talking about, with a cream-and-navy cut-out edge.

### Text on screen

- Big numbers use a heavy retro serif (like the cover title), in black with a cream outline.
- **Use the numbers the narrator says.** The audiobook edition has some different figures from the current website (for example 97 million war deaths, 13,000 warheads, 3,070 : 1). The script already uses the audio figures.
- Chapter title cards use Layer A: the navy wall, the rising sun and the stars, and the title in the cover font. Use one only where the script says "title card" (where the narrator reads the heading). Parts whose first line is not a heading, such as Part 2 "Hello, human", start without a card, so the narration is not interrupted. The chapter list is at the top of the script.
- Keep on-screen text short. The narrator says the words; the screen shows the number or the label.

### Motion

- Use limited animation. Most shots are illustrated plates with slow push-ins and pans, plus a few looping actions (2–4 frames).
- Animate the paper money a lot. It is the main "actor" of Layer B: it walks, runs, flows through pipes, and changes color.
- **HOLD** on dark facts. When the audio states a death toll, stop all motion for 1–2 seconds. Do not add jokes on top of those lines.

### Comedy

The narration already tells its joke. The picture's job is a second joke that the words do not say.

1. **Every scene has a visual joke of its own:** a background gag, a detail that contradicts the line, an escalation, or a callback to an earlier gag. A scene that only shows what the narrator says gets one, or gets merged into its neighbor.
2. **Land the payoff a beat after the line.** Setups go up before or on the words; the visual punchline comes about 0.4 s after the spoken punchline ends, then holds. In a storyboard's Moves, `"word" →` starts on the word, `after "word" →` a beat after it ends, and `before "word" →` half a second before it starts.
3. **Someone reacts to the big lines.** Wishonia changes expression or gesture in her corner, or looks slowly at the camera in the office; a human turns its head slowly. The reaction is often the laugh.
4. **Do not repeat the captions.** The captions already show the words, so a label or counter goes on screen only when the number is itself the joke.
5. **Threes with a twist, and callbacks.** Two of a kind, then a wrong third. Bring earlier gags back changed.
6. **Go all the way, like the theme song.** A threat always pays off on screen. The bomb goes off: a white flash, a mushroom cloud, then the humans standing there charred black and smoking, hair straight up, only their eyes blinking. The spark spreads until the whole person is on fire and running in circles. The dying turn into skeletons, and the skeletons keep smiling. The button is the humans doing it again. This is Looney Tunes violence: nobody bleeds; everybody is charred, flattened, frozen or a skeleton. The kit draws these (`KIT.person` with `skeleton` or `charred`, `KIT.flames`, `KIT.nuke`, `KIT.xray`). The cheerful voice against the horror is the joke, so the horror has to be seen.
7. **Sound.** Each scene gets one or two cartoon sound effects on its gags (a rubber-stamp thunk, a cash-register ding, a boing, a slide whistle, a record scratch, a toaster pop), listed on its storyboard's Sound line. No music under the narration except the theme. A HOLD is silent.

---

## 2. Wishonia (use the existing sprites)

Wishonia already has a full sprite set. Use it. Do not redesign the character.

- **Where the sprites are:** the originals are in `mikepsinn/disease-eradication-plan` (branch `develop`; the 59 files used here are as of commit `5d6cad7`) → `transmit/public/assets/sprites/alien/`, at full resolution (heads 1024×1024, bodies 1343×768). The 12 seed images that the sprites were made from are in `alien/sources/`. `mikepsinn/optimitron` has reduced copies in `apps/optimitron/public/sprites/wishonia/` (some are only 512 px). **Use the originals for video.** A contact sheet of all 59 sprites, with their file names, is next to this file: `wishonia-contact-sheet.png`.
- **Design:** blue skin, a black bob haircut with straight bangs, two thin antennae with ball tips, large eyes with dark lashes. An orange 1960s-style mod dress with a darker swirl pattern and a small white brooch at the neck. Blue arms.
- **Name on screen:** "WISHONIA." The full name is "World Integrated System for High-efficiency Optimization Networked Intelligence and Allocation" (the theme song sings it out).

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

- **Stereotypes you read from the silhouette,** as the theme song draws them (its keyframes are the reference: the fat cat, the woman with the megaphone, the masked crook, the politician at the podium, the scientist with the magnifying glass). Each body is one big clothing shape: the fat cat an egg on stub legs, the politician a padded inverted triangle, the businessman a refrigerator box, the crook a hunched trench coat, the worker a barrel, the beanpole a plank, a woman an hourglass or a pear.
- **A small head with a big nose:** 3/4 view, the nose breaking the outline, almond eyes with heavy lids like Wishonia's, thin angled brows, a jowly, lantern-jawed or long sly face.
- **One stereotype tell each:** a top hat and cigar, a domino mask and fedora, a toothy grin, a bubbling flask. **Greedy** puts dollar signs in the eyes.
- **Sharp and angular, never rounded:** polygons with hard corners, thin navy lines, tapered limbs with sharp elbows and knees, narrow hands, pointed shoes. Rounded heads, thick outlines, stubby limbs and mitten hands read as toy people. Print shading: orange edges on navy suits, halftone dots on light cloth.
- Each human has a small round **"check engine" light** on the chest, over the clothes. It blinks red when a disease starts.
- Four skin tones and four clothing colors. An everyday human gets a body type and proportions of its own from its outfit, skin tone and color, so a crowd is a cast of 1950s types, and the same human looks the same in every scene.
- They act with posture and timing: a slow head turn, an arm thrown up, a slump, a hunch.

### The Papers (money)

- Small paper rectangles with stick legs and a tiny oval portrait of a generic, unnamed old man in a wig. Do not copy any real banknote.
- Always money green. A red missile seal = murder money; a teal cross seal = medicine money; no seal = plain money (`KIT.money("war" | "med" | "plain")`).
- They run toward whoever calls them. They form lines, crowds, and rivers. They jump into funnels.

### Recurring Earth characters

| Character | Design | Used in |
|---|---|---|
| The Rich Human | A fat cat: a navy egg on stub legs, jowls, top hat, monocle, walrus mustache, cigar and gold watch chain, hugging a stack of cash, smug. Sits on a hill of papers. Later wears a button: "I PREFER LIVING." (`KIT.cast("richHuman")`) | Quiz, Paper Distribution, bonds |
| The Loud Human | A human with a megaphone instead of a head. (`KIT.cast("loudHuman")`) | Step 2 (marketing) |
| The Lobbyist | A masked crook: fedora pulled low, domino mask, popped-collar trench coat, gloves, tiptoeing with a fistful of cash and a briefcase leaking money. (`KIT.cast("lobbyist")`) | Paper Distribution, Bribe the Bribers |
| The Politician | A lantern jaw, a grin full of teeth, slick hair, a flag pin and a very wide tie, waving a bill. The tie flips between red and blue (the "red team / blue team" gag). (`KIT.cast("politician")`) | Leaders, Purchase Democracy |
| The Weapons Maker | A barrel-chested worker with a tiny head under a hard hat, Popeye forearms and a cigar, cradling a smiling missile like a baby. Factory chimneys are shaped like missiles. (`KIT.cast("weaponsMaker")`) | Leaders loop, Enjoy |
| The Orderly | A beanpole in scrubs with a long neck and long arms, holding out a medicine cup (and sliding it through a door slot). (`KIT.cast("orderly")`) | Institutionalize scene |
| Grandma | Hunched, pear-shaped, in curlers, cat-eye glasses and an apron, waving her 1940s war-bond poster overhead. (`KIT.cast("grandma")`) | What Grandma got |
| The Scientist | A lab coat, a hair bun and big glasses, holding up a bubbling flask, with a clipboard. (`KIT.cast("scientist")`) | The trials, the dFDA |
| The Democracy Dog | A round dog chasing its own tail. The tail is made of papers; later it is made of teal pills. | Leaders loop |
| The Optimitron | A 1970s countertop appliance (a toaster–microwave hybrid) with two big dials: **HEALTH** and **WEALTH**. Policy cards pop out of it like toast. | Optimitron, Step 1 |
| The Calculator | A desk calculator with eyes. It shows "ERROR," screams, and walks off the desk. | The Math |

### Real people, brands and weapons

- Never draw real, identifiable politicians, executives, companies, or brand logos. Use the generic humans and plain signs. Real names (Eisenhower, Erica Chenoweth) appear as text only.
- Weapons are silly objects (missiles with price tags, a submarine in a field).

---

## 4. Recurring gags and devices

1. **The 604 bar.** A tall stack of war money (red seals) next to one small medicine bill (teal seal). It returns every time the audio says "604."
2. **The seal flip.** War money goes into a funnel and comes out medicine money: the red missile seal flips to the teal cross. Use it every time money is "redirected."
3. **Wishonia's mug sip.** Before a big punchline, Wishonia sips coffee. After the punchline, Wishonia puts the mug down slowly.
4. **The case file.** Wishonia stamps the Earth case file: "SUBOPTIMAL" (after the FDA part) and finally "ELIGIBLE FOR OPTIMIZATION" (the ending).
5. **Chapter cards.** A 2-second title card in the office colors (navy wall, rising sun, stars), where the script says "title card" (see section 1).

---

## 5. Drawing the art in code

All art is drawn in code (SVG and CSS). Do not use AI images. The shared drawing functions are in `video/assets/js/kit.js`. Use them, so that all parts look the same.

One exception: the first 1:40 of episode 1 (the theme song) is the existing music video, `assets/music-video/wishonia-theme-song-music-video.mp4`, which was made from AI keyframes. The drawn style starts at the title card. See `video/storyboards/part-01-opening.md`, scene theme-music-video.

- **Palette (`KIT.C`):** the theme song colors (section 1). Take every color from `KIT.C`, so that a palette change stays one edit.
- **Layer A (`KIT.office`):** the navy wall with geometric panels, atomic stars (`KIT.star`) and boomerangs (`KIT.boomerang`), the rising orange sun, the tiled floor, and a mustard disc behind Wishonia's head. Props: `KIT.desk` (in front of Wishonia), `KIT.mug`, `KIT.cabinet` ("EARTH: CASE #847") and `KIT.wallScreen`. `KIT.OFFICE` gives the standard positions for each canvas shape (wall screen, Wishonia, desk, the disc), so that the office stays the same from scene to scene.
- **Both canvas shapes:** every scene is drawn for 16:9 (1920 × 1080) and for the tall phone version, 9:16 (1080 × 1920); `KIT.V` is true for 9:16. Each scene has its own layout for each shape, not a scaled copy. In 9:16, Wishonia's saucer is top right and the captions sit at y 1470 to 1700.
- **Transitions (`KIT.enter`):** "slide left" (Earth to Earth), "zoom into the wall screen" (office to Earth) and "zoom out of the wall screen" (Earth to office, with a small copy of the last Earth picture on the screen).
- **The eligibility form (`KIT.form`, `KIT.FORM_Q`, `KIT.FORM_AT`):** the 1950s mail-in form of loved-ones, nuclear-winters and eligible, with its YES/NO boxes and the fine print.
- **Layer B (`KIT.paper`):** cream paper with a navy and orange double rule border and a few stars. `KIT.paperDefs` gives the halftone-dot fills (the ids keep their old names: hatch, cross, fine, hred, hteal). Use navy lines. Money is money green with a red seal (war) or a teal seal (medicine) (section 1, Layer B). For teal text on cream, use the darker `#1F6E68`, so that the text is easy to read.
- **Print grain (`KIT.grain`):** a fine speckle pattern laid over the whole frame, last. Do not use full-frame SVG filters for it: in the render they paint through from scenes that are not on screen and wash out the colors.
- **Characters (original designs):** `KIT.person(o)` (a stereotype human, with a chest light; `KIT.cast(name)` gives the recurring characters above, with their props and pose unless the scene poses the arms; `KIT.rig(o)` gives a person's pivots and hands; the old name `KIT.bean` now draws a person too, and `tools/cast-sheet.mjs` draws the cast sheet), `KIT.money` (a paper bill with stick legs and a generic oval portrait), `KIT.tophat`, and the quiz parts (`KIT.checkbox`, `KIT.tick`, `KIT.pencil`).
- **Wishonia:** the real sprite PNGs only (section 2). `KIT.mountWishonia` puts the head on the body as in `characters.js`, swaps the mouth from `word-timings.json`, shows `blink-smile` in pauses, and rocks the head ±2° on the 7-second loop. Layer A shows Wishonia large. Layer B shows her in the corner (`KIT.cornerOpts`: standing in 16:9, in her saucer in 9:16).
- **Text:** big numbers use Fraunces Black (soft), labels use Oswald SemiBold, captions use Inter. The font files and their licenses (SIL Open Font License) are in `video/assets/fonts/`. Draw check marks and arrows as SVG, because the fonts do not have all symbols.

---

## 6. Building it with HyperFrames

The video is a HyperFrames project (HTML + GSAP, rendered to MP4) in `video/`. It follows `mikepsinn/optimitron/videos/care-integrated-clinical-trials`, but it uses the audiobook MP3 as the voice, so there is no text-to-speech step. `video/README.md` gives the commands.

- **One part at a time.** `video/parts/part-NN.json` gives the audio cut and, for each scene, its cue word, its composition file, and the Wishonia states (`expression`, resting mouth, body pose, large or PiP).
- **The build step** (`node tools/build-part.mjs parts/part-NN.json`, add `--aspect 9x16` for the tall version) cuts the MP3, mixes in the part's sound effects (`tools/sfx.py` makes them; nothing is downloaded), copies the sprites and other media, and writes `data/part-NN.js` and `index.html`. The data file has the scene start times (found from the cue words), the words, the mouth track (`CHAR_TO_VISEME`, closed in pauses), the blinks, the caption groups and the sound times. Build and render one shape at a time: the build rewrites files that both shapes use.
- **One composition for each scene** (`compositions/scenes/part-NN/<scene-id>.html`). Each scene starts its animations on the spoken words with `KIT.cue(scene, "word")`, `KIT.after` (a beat after the word) or `KIT.before`, so the motion stays in sync with the voice.
- **SVG and GSAP:** never tween x, y, scale or rotation on an SVG element that has a `transform` attribute (GSAP reads it as the start and the element jumps). Position an outer group and tween an inner one.
- **Captions** (`compositions/captions.html`) come from the same word timings. The spoken word is highlighted.
- **Check, then render:** `npx hyperframes check`, look at frames with `npx hyperframes snapshot --describe false`, then `npx hyperframes render`. Render each part on its own, then join the parts with ffmpeg.
- Keep the renders, the MP3 and the audio cuts out of git.
