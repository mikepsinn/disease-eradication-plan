# Cartoon Style Bible: "How to End War and Disease (for Busy People)"

This file goes with the storyboards (`video/storyboards/`): the look, Wishonia, the cast, the recurring gags and the drawing kit. The audiobook MP3 is the voice track, and all times are times in that MP3. `AGENTS.md` has the process and Mike's calls.

---

## 1. Look

The episode is a 1950s atomic-age instructional film. Wishonia hosts it from her control console, as in the theme song, and talks to the viewer; between her shots, illustrated plates show what the humans do, and she is the voice. Period film (grain, flicker, gate weave, dust) runs over every shot. The host shots continue the theme song music video that opens the episode: mid-century flat illustration in its palette, deep navy `#112845` and `#061D3E`, slate `#273049`, burnt orange `#E5903B`, cream `#F3ECD0`, rust `#904B2E`, tan `#B47E52`, with mustard `#E8B04A` stars; flat shapes and thin navy outlines.

- **Host shots (layer A):** Wishonia large at her control console on her observation deck (`KIT.studio`): a glass wall onto deep space painted after the book cover, with Earth hanging in it (`KIT.STUDIO.earth`, for gags that happen on Earth; art in `video/assets/art/deck/`). The console is generated art copied from the theme song (`video/assets/art/console/`), with a cream ledge, keys, two dials, a readout and a big red button (`KIT.STUDIO.button`). Her coffee mug and the case file "EARTH: CASE #847" sit on the ledge only when a gag uses them. A **reaction cut** is a host shot of about a second after a big line: a side-eye, a slow look at the camera. Host shots stay as they are.
- **Plates (layer B):** cut-out collage on aged paper (`KIT.collage`): hand-tinted engraving cut-outs from `video/assets/art/collage/` with paper margins and a paper shadow, moving stiffly on twos (12 drawings a second): they slide in rigidly, hinge, pop, squash and swap. Words are on cream cards, tags and red rubber stamps. The pilot is `video/parts/pilot-collage.json`.
- **Money** is a green bill with stick legs and a generic oval portrait. Its dark green seal says what it buys: a missile for war money, a cross for medicine money (`KIT.money("war" | "med" | "plain")`). When money moves from war to medicine, the missile on its seal flips to a cross: the main visual idea of the episode. In older storyboards "red papers" means war money and "teal papers" medicine money; both are green.
- **Title cards** are the period card (`KIT.titleScene`): the heading on plain navy under the film's emblem, where the narrator reads a heading. The chapter list is at the top of the script.
- **Storyboard notation:** in a scene's Moves, `"word" →` starts on the word, `after "word" →` about 0.4 s after it ends, and `before "word" →` half a second before it starts.

---

## 2. Wishonia (the existing sprites)

- **Where the sprites are:** the originals are in `mikepsinn/disease-eradication-plan` (branch `develop`; the 59 files used here are as of commit `5d6cad7`) → `transmit/public/assets/sprites/alien/`, at full resolution (heads 1024×1024, bodies 1343×768). The 12 seed images they were made from are in `alien/sources/`. `mikepsinn/optimitron` has reduced copies in `apps/optimitron/public/sprites/wishonia/` (some only 512 px), so use the originals for video. A contact sheet of all 59, with their file names, is next to this file: `wishonia-contact-sheet.png`.
- **Design:** blue skin, a black bob haircut with straight bangs, two thin antennae with ball tips, large eyes with dark lashes. An orange 1960s-style mod dress with a darker swirl pattern and a small white brooch at the neck. Blue arms.
- **Name on screen:** "WISHONIA." The full name is "World Integrated System for High-efficiency Optimization Networked Intelligence and Allocation" (the theme song sings it out).

### How the sprites fit together

- **Heads (44 files):** `{expression}-{mouth}.png`. The expression sets the eyes and brows; the mouth shape changes for lip-sync.
- **Bodies (15 files):** `body-{pose}.png`, without a head. The head goes on top of the body at the neck.
- **Expressions and their mouth shapes** (the same table as `packages/wishonia-widget/src/core/viseme-map.ts`):

| Expression | Mouth shapes available | Good for |
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
| `sad` | closed, frown, oh, small | death tolls |
| `lookright` | smile, closed, open, oh | looking off to the side |
| `blink` | smile | idle blinks, the last "Love you. Bye." |

- **Body poses:** `idle`, `presenting`, `point-right`, `open-palms`, `palms-down`, `arms-crossed`, `counting`, `excited`, `fist`, `hand-chest`, `hands-hips`, `listening`, `shrug`, `thinking`, `wide-gesture`.
- **Layout (from `transmit/public/assets/js/characters.js`):** the head is 95% of the character's width, centered; the body goes under it at the full width, moved up to overlap the head by about 9% of the width; the head is in front.
- **Idle motion (same file):** the head rocks from −2° to +2° and up 2 px on a 7-second loop; every few seconds `blink-smile` shows for a moment.
- **In the part file:** each Wishonia state gives `expression-mouth` + `body-pose` (for example `smirk-smile` + `body-hands-hips`); the mouth is the resting mouth, swapped by lip-sync while she talks.

### Lip-sync

`word-timings.json` gives the start and end of every word; each word's letters are spread across its duration and mapped with `CHAR_TO_VISEME` (vowels → open/ee/oh; b, m, p, f, v → closed; most other letters → small). `getHeadName` falls back to an available mouth.

---

## 3. The cast

The cast are Victorian engraving cut-outs, hand-tinted, each drawn once under its name in `video/storyboards/ART.md` (which has every cut-out, its poses and states, and its parts). Each human has a small round "check engine" light on the chest that blinks red when a disease starts; greed puts dollar signs in the eyes. The recurring characters:

| Name | Look | Parts |
|---|---|---|
| `you` | YOU, the viewer: a busy clerk in a bowler with a pocket watch; later charred, bone-legged, a skeleton. | 1, 8, 10, 12 to 14, 17, 19 to 21, 23 to 27 |
| `fat-cat` | The Rich Human: a robber-baron fat cat, egg-shaped, top hat, monocle, walrus mustache, cigar, watch chain. | 1, 4, 5, 8 to 10, 13 to 17, 21 to 23, 25, 26 |
| `weapons-maker` | A barrel-chested foundry worker, tiny head under a hard hat, cigar, cradling his smiling `baby-missile`. | 1, 2, 4, 6, 7, 11 to 13, 15, 17 to 21, 23 to 26 |
| `politician` | Lantern jaw, a grin full of teeth, slick hair, a wide tie that tints red, blue or teal. | 2 to 7, 11 to 15, 17, 19 to 22, 26 |
| `lobbyist` | A masked crook: fedora, domino mask, trench coat, gloves, a briefcase with an empty BELIEFS slot. | 5, 15, 17, 19 to 24 |
| `scientist` | A lab coat, a bun, big glasses and a bubbling flask. | 1, 4 to 7, 9, 11 to 18, 21, 22, 24, 25, 27 |
| `reaper` | The Grim Reaper (generated art in `video/assets/art/reaper/`), with a clipboard of tallies; a deli cap at his counter. | 1, 5, 6, 8, 17, 18, 20, 21, 26, 27 |
| `grandma` | Hunched, in curlers, cat-eye glasses and an apron, with her war-bond poster; then her skeleton. | 17, 21, 27 |
| `loud-human` | A human with a megaphone for a head, in four builds. | 4, 5, 14, 18, 23, 25 |
| `super-pac` | A rust canvas backpack with a red cape, its SUPER PAC patch sewn over BRIBERY. | 5, 17, 20, 23 |
| `germ` | A microscope-plate microbe on little legs with a smug grin. | 1, 4, 6 to 10, 14 to 17, 21, 24 to 27 |
| `bill-war`, `bill-med`, `bill-plain` | Green banknotes on stick legs; the seal (missile, cross or none) is its own piece and flips. | most parts |
| `patient` | A Victorian invalid with a thermometer, in a gown or an iron bed; then a skeleton. | 1, 5, 11, 12, 14 to 16, 21, 22 |
| `citizen` | A sheet of everyday Victorians of every build: townsfolk, voters, strangers, crowds. | 1, 6, 14, 18, 20, 23, 24, 26 |
| `family` | The Victorian family of four on the sofa; charred, then skeletons. | 1, 2, 10, 12 |
| `fda-official` | Bald, glasses, an FDA badge and a magnifying glass. | 12, 14, 15 |
| `robot` | A clockwork tin robot: hunched over a laptop (cybercrime), or in an army helmet (the pro-war algorithm). | 10, 11, 25, 27 |
| `optimitron` | A 1970s countertop toaster-oven with a face and two dials, HEALTH and WEALTH; cards pop out like toast. | 14, 17, 22, 23 |
| `calculator` | A brass adding machine with eyes; it screams and walks off the ledge. | 16, 19, 22 |
| `democracy-dog` | A round dog chasing its tail of war bills, later of pills. | 1, 6 |

---

## 4. Recurring gags and devices

1. **The 604 bar.** A tall stack of war money (missile seals) next to one small medicine bill (cross seal). It returns every time the audio says "604."
2. **The seal flip.** War money goes into a funnel and comes out medicine money: the missile on its seal flips to a cross, every time money is "redirected."
3. **Wishonia's mug sip.** Before a big punchline she sips coffee at her console; after it, she puts the mug down slowly.
4. **The case file.** Wishonia presses the big button and the Earth case file is stamped (`KIT.props.caseFile`): "MAY BE ELIGIBLE FOR OPTIMIZATION" (Part 1), "SUBOPTIMAL" (after the FDA part) and finally "ELIGIBLE FOR OPTIMIZATION" (the ending).
5. **Chapter cards.** The period title card, where the script says "title card".
6. **The iris.** The film opens on Wishonia's face and closes on it.

---

## 5. The drawing kit

The shared drawing code is in `video/assets/js/kit.js`, `film.js` and `props/*.js`; generated art is in `video/assets/art/`. The first 1:40 of the episode is the existing theme song music video (`assets/music-video/wishonia-theme-song-music-video.mp4`).

- **Palette:** `KIT.C` (the colors above).
- **The film look (`film.js`):** `KIT.film` (the period film), `KIT.studio` (a whole host shot: the set, Wishonia, the console and the push; `KIT.STUDIO` gives the set's positions for each shape), `KIT.iris`, `KIT.camera` (named views over a plate and timed keys), and `KIT.mix`, `KIT.burn` and `KIT.smooth`. Part 2's scenes in `video/compositions/scenes/part-02/` show each kind of shot.
- **Collage plates (`collage.js`, after `film.js`):** `KIT.collage(spec)` builds a whole plate scene from a cast of cut-outs and a list of beats on spoken words (the moves are in `video/README.md`, "Writing a collage scene"); `KIT.collage.SIZES` holds each cut-out's size.
- **Both shapes:** every scene is drawn for 16:9 (1920 × 1080) and 9:16 (1080 × 1920); `KIT.V` is true for 9:16.
- **People:** `KIT.person(o)` (a stereotype human with a chest light, `skeleton` and `charred` options, hats including `uncleSam` and `ushanka`), `KIT.cast(name)` (the recurring characters), `KIT.rig(o)` (a person's pivots and hands); `tools/cast-sheet.mjs` draws the cast.
- **Effects:** `KIT.flames`, `KIT.nuke`, `KIT.boom`, `KIT.xray`.
- **Props:** `KIT.props.<name>` (documented at each function; `tools/props-sheet.mjs` draws them), `KIT.money`, `KIT.reaper`, the eligibility form (`KIT.form`), `KIT.titleScene`.
- **Text:** `KIT.textWidth` and `KIT.fitText` measure it. Big numbers use Fraunces Black (soft), labels Oswald SemiBold, captions Inter (the fonts and their licenses are in `video/assets/fonts/`). Draw check marks and arrows as SVG; the fonts lack some symbols.
- **Wishonia:** `KIT.mountWishonia` puts the real sprites together, lip-syncs them from the word timings, blinks and rocks the head.
- **Part 1's old office look** (`KIT.office`, `KIT.desk`, `KIT.mug`, `KIT.wallScreen`, `KIT.enter`, `KIT.zoomView`, `KIT.paper`) drew the earlier version of Part 1.
