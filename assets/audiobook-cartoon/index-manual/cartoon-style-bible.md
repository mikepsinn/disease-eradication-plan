# Cartoon Style Bible: "How to End War and Disease (for Busy People)"

This file goes with the scene script (`cartoon-script.md`). It sets the look, the characters, and the recurring gags. Use it to brief illustrators, animators, and image tools.

The audiobook MP3 is the voice track. Do not record new narration. All times in the script are times in that MP3.

---

## 1. Look

The episode is a 1950s atomic-age instructional film. Wishonia hosts it from a lectern and talks to the viewer; between her shots, illustrated plates show what the humans do, and she is the voice. Period film runs over every shot. The drawing continues the theme song music video that opens the episode: mid-century flat illustration in its palette (measured from its keyframes): deep navy `#112845` and `#061D3E`, slate `#273049`, burnt orange `#E5903B`, cream `#F3ECD0`, rust `#904B2E`, tan `#B47E52`, with mustard `#E8B04A` stars. Flat shapes and thin navy outlines. No gradients.

**One idea per picture.** A diagram with many labeled parts on screen at once reads as an animated slide deck. Each phrase of narration gets one framing, held long enough to read.

Part 1 (the opening) was made before this look, in Wishonia's office with paper diagrams. It keeps that look until it is restyled.

### Layer A: the host

- Use it when Wishonia talks to the viewer: the line after a title card, her verdicts, the jokes she tells to the camera, and the ending.
- One set (`KIT.studio`): a mustard studio wall with a spotlight pool, and a navy lectern with the film's atom on its front.
- Wishonia stands large at the lectern, drawn from the real sprites (section 2). Her props sit on the lectern: the coffee mug, the case file "EARTH: CASE #847" and its rubber stamp.
- A **reaction cut** is a host shot of about a second after a big line: a side-eye, or a slow look at the camera.

### Layer B: the plates

- Use them when the audio describes what humans do: money, wars, the FDA, the treaty mechanics.
- A plate is one large illustration on a plain field, with no paper borders, labels or arrows. A scene draws it once (a looping road with its stops, a field of headstones) and the camera travels over it, one framing per phrase.
- Wishonia is not in the plates. She is the voice.
- Money is always **money green**, like a real bill, never red. Its dark green seal says what it buys: a little missile for war money, a cross for medicine money (`KIT.money("war" | "med" | "plain")`).
- When the money moves from war to medicine, the missile on its seal flips to a cross. This is the main visual idea of the whole episode. Where a storyboard says "red papers" it means war money, and "teal papers" means medicine money: both are green.

### Period film

Every shot, title cards included, runs under `KIT.film` (grain, flicker, gate weave, dust), outside the camera so camera moves never scale it.

### Text on screen

- Text that is part of the joke or the fact is fine: a sign, a stamp, a button, a big number ("EARTH: CASE #847", "I PREFER LIVING", 310,000,000 stamped into the sky over the headstones). Big numbers use Fraunces Black, navy on a light plate and cream on a dark one.
- No text that explains the picture: no labels on things, no arrows, and no narration written out. That is what turns a plate back into a slide.
- **Use the numbers the narrator says.** The audiobook edition has some different figures from the current website (for example 97 million war deaths, 13,000 warheads, 3,070 : 1). The script already uses the audio figures.
- Title cards are the period card (`KIT.titleScene`): the heading on plain navy under the film's emblem. Use one only where the narrator reads a heading; a part whose first line is not a heading starts without one. The chapter list is at the top of the script.

### Motion

- Use limited animation: camera moves over held plates, and a few actors that move on the words.
- The paper money is the main actor of the plates. It walks, marches, runs round loops and changes seals.
- **HOLD** on dark facts. When the audio states a death toll, let the number land, then hold the frame for 1–2 seconds: no motion, no joke and no sound.

### Both canvas shapes

Both shapes use the same plates, each with its own camera views. 16:9 keeps everything important above y 900 (YouTube's captions and controls); 9:16 frames tighter, above the burned-in captions at y 1470.

### Comedy

The narration already tells its joke. The picture's job is a second joke that the words do not say.

1. **Every scene has a visual joke of its own:** a background gag, a detail that contradicts the line, an escalation, or a callback to an earlier gag. A scene that only shows what the narrator says gets one, or gets merged into its neighbor.
2. **Land the payoff a beat after the line.** Setups go up before or on the words; the visual punchline comes about 0.4 s after the spoken punchline ends, then holds. In a storyboard's Moves, `"word" →` starts on the word, `after "word" →` a beat after it ends, and `before "word" →` half a second before it starts.
3. **Someone reacts to the big lines.** A human in the plate turns its head slowly, or the film cuts to Wishonia at her lectern for a beat. The reaction is often the laugh.
4. **Threes with a twist, and callbacks.** Two of a kind, then a wrong third. Bring earlier gags back changed.
5. **Go all the way, like the theme song.** A threat always pays off on screen. The bomb goes off: a white flash, a mushroom cloud, then the humans standing there charred black and smoking, hair straight up, only their eyes blinking. The spark spreads until the whole person is on fire and running in circles. The dying turn into skeletons, and the skeletons keep smiling. The button is the humans doing it again. This is Looney Tunes violence: nobody bleeds; everybody is charred, flattened, frozen or a skeleton. The kit draws these (`KIT.person` with `skeleton` or `charred`, `KIT.burn`, `KIT.flames`, `KIT.nuke`, `KIT.xray`). The cheerful voice against the horror is the joke, so the horror has to be seen.
6. **Sound.** Each scene gets one or two cartoon sound effects on its gags (a rubber-stamp thunk, a cash-register ding, a boing, a slide whistle, a record scratch, a toaster pop), listed on its storyboard's Sound line. No music under the narration except the theme. A HOLD is silent.

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
- Always money green, never red. A missile seal = murder money; a cross seal = medicine money; no seal = plain money (`KIT.money("war" | "med" | "plain")`).
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

1. **The 604 bar.** A tall stack of war money (missile seals) next to one small medicine bill (cross seal). It returns every time the audio says "604."
2. **The seal flip.** War money goes into a funnel and comes out medicine money: the missile on its seal flips to a cross. Use it every time money is "redirected."
3. **Wishonia's mug sip.** Before a big punchline, Wishonia sips coffee at her lectern. After the punchline, she puts the mug down slowly.
4. **The case file.** Wishonia stamps the Earth case file on her lectern: "SUBOPTIMAL" (after the FDA part) and finally "ELIGIBLE FOR OPTIMIZATION" (the ending).
5. **Chapter cards.** The period title card, where the script says "title card" (see section 1).
6. **The iris.** The film opens on Wishonia's face and closes on it.

---

## 5. Drawing the art in code

Art is drawn in code (SVG and CSS), except a few generated cut-out characters such as the Grim Reaper, where code turns cloth and faces into blobs (`AGENTS.md`, Generated art). The shared drawing functions are in `video/assets/js/kit.js`. Use them, so that all parts look the same.

One exception: the first 1:40 of episode 1 (the theme song) is the existing music video, `assets/music-video/wishonia-theme-song-music-video.mp4`, which was made from AI keyframes. The drawn style starts at the title card. See `video/storyboards/part-01-opening.md`, scene theme-music-video.

- **Palette (`KIT.C`):** the theme song colors (section 1). Take every color from `KIT.C`, so that a palette change stays one edit.
- **The film look (`video/assets/js/film.js`, loaded after `kit.js`):** `KIT.film` (the period film), `KIT.studio` (a whole host shot: the set, Wishonia, the lectern and the push; `KIT.STUDIO` gives the set's positions for each canvas shape), `KIT.iris` (in or out on a point), `KIT.camera` (a camera over a plate: named views and timed keys, eased from key to key), and the helpers `KIT.mix` (a color between two), `KIT.burn` (a drawing charred) and `KIT.smooth`. Part 2's scenes in `video/compositions/scenes/part-02/` are the reference for each kind of shot.
- **Both canvas shapes:** every scene is drawn for 16:9 (1920 × 1080) and for the tall phone version, 9:16 (1080 × 1920); `KIT.V` is true for 9:16. In 9:16 the captions sit at y 1470 to 1700.
- **The eligibility form (`KIT.form`, `KIT.FORM_Q`, `KIT.FORM_AT`):** the 1950s mail-in form of loved-ones, nuclear-winters and eligible, with its YES/NO boxes and the fine print.
- **Part 1's office look:** `KIT.office` and its props (`KIT.desk`, `KIT.mug`, `KIT.cabinet`, `KIT.wallScreen`, positions in `KIT.OFFICE`), the wall-screen zooms (`KIT.enter`, `KIT.zoomView`), the cream diagram paper (`KIT.paper`, `KIT.paperDefs`), the print grain (`KIT.grain`) and Wishonia's corner (`KIT.cornerOpts`) drew Part 1. Do not use them in the other parts. Do not use full-frame SVG filters for grain: in the render they paint through from scenes that are not on screen and wash out the colors.
- **Characters (original designs):** `KIT.person(o)` (a stereotype human, with a chest light; `KIT.cast(name)` gives the recurring characters above, with their props and pose unless the scene poses the arms; `KIT.rig(o)` gives a person's pivots and hands; the old name `KIT.bean` now draws a person too, and `tools/cast-sheet.mjs` draws the cast sheet), `KIT.money` (a paper bill with stick legs and a generic oval portrait), `KIT.tophat`, and the quiz parts (`KIT.checkbox`, `KIT.tick`, `KIT.pencil`).
- **Wishonia:** the real sprite PNGs only (section 2). `KIT.mountWishonia` puts the head on the body as in `characters.js`, swaps the mouth from `word-timings.json`, shows `blink-smile` in pauses, and rocks the head ±2° on the 7-second loop. Layer A shows her large at the lectern (`KIT.studio`). The plates do not show her.
- **Text:** big numbers use Fraunces Black (soft), labels use Oswald SemiBold, captions use Inter. The font files and their licenses (SIL Open Font License) are in `video/assets/fonts/`. Draw check marks and arrows as SVG, because the fonts do not have all symbols.

---

## 6. Building it with HyperFrames

The video is a HyperFrames project (HTML + GSAP, rendered to MP4) in `video/`, voiced by the audiobook MP3, so there is no text-to-speech step. `AGENTS.md` gives the process and the rules that are easy to get wrong; `video/README.md` gives the files and the commands.
