# Episode 1 cartoon: HyperFrames project

The cartoon video for audiobook episode 1, "How to End War and Disease (for Busy People)", built with [HyperFrames](https://github.com/heygen-com/hyperframes) (HTML + GSAP rendered to MP4). The voice is the audiobook MP3. There is no text-to-speech. The plan, the scene script and the style bible are in the folder above this one.

Plates are cut-out collage (Victorian engravings on aged paper, `KIT.collage`); host shots are Wishonia at her console on the observation deck (`KIT.studio`). See `../cartoon-style-bible.md`. `parts/pilot-collage.json` (Part 1's atom sequence) and `parts/short-soviet-plan.json` are built in collage. Parts 1 to 14 have older scenes in the flat 1950s look, to be rebuilt in collage. The storyboards (one beat sheet per part) are in `storyboards/`.

Every part renders twice: 16:9 (1920 × 1080) and the tall phone version, 9:16 (1080 × 1920).

| File | Purpose |
| --- | --- |
| `parts/part-02.json` | The audio cut, and for each scene: cue word, composition file, Wishonia states |
| `storyboards/part-NN-*.md` | One storyboard per part, for review before anything is animated |
| `tools/word-timings.mjs` | Rebuilds `../word-timings.json` and the transcripts from the audiobook pipeline's alignment |
| `tools/build-part.mjs` | Cuts the MP3, mixes in the sound effects, copies the sprites and media, writes `data/part-NN.js` and `index.html` (`--aspect 9x16` for the tall version; `--data-only` writes just `data/part-NN.js`, for checking scenes while another part builds) |
| `tools/scene-check.mjs` | Loads one scene with its part's data in headless Chrome, in either shape, reports page errors and saves frames and a contact sheet to `snapshots/scene-check/` |
| `tools/props-sheet.mjs` | Draws the shared props library (`assets/js/props/*.js`) on review sheets in `snapshots/props/` |
| `tools/text-overflow.mjs` | Finds text that runs off its sign; `scene-check` prints what it finds |
| `tools/text-widths.mjs` | Measures the fonts into `kit.js`, for `KIT.textWidth` and `KIT.fitText` |
| `tools/art-gen.sh`, `tools/art-cutout.py` | Generate a cut-out art sheet with Codex, then cut it into WebP pieces (`../AGENTS.md`, Generated art) |
| `tools/sfx.py` | Synthesizes the sound effects (thunk, stamp, slide whistle and so on) with numpy; nothing is downloaded |
| `data/part-NN.js` | Generated: scene times, words, mouth track, blinks, caption groups, sound times |
| `index.html` | Generated: the root composition (scenes, captions, voice) |
| `compositions/scenes/*.html` | One composition for each scene |
| `compositions/captions.html` | Captions from the word timings, with the spoken word highlighted |
| `assets/js/kit.js` | Shared code: cue times, the Wishonia rig, and all SVG art for both layers |
| `assets/js/film.js` | The film look (Parts 2 to 27): the period film, the host's studio set, the iris, and the camera that travels over a plate. Load it after `kit.js` |
| `assets/js/collage.js` | `KIT.collage`: a cut-out collage scene from a short spec ("Writing a collage scene" below). Load it after `film.js` |
| `assets/art/<name>/` | Generated cut-out art (the Grim Reaper's poses and puppet pieces for `KIT.reaper`), with its source sheets in `sheets/` |
| `assets/fonts/` | Fraunces, Oswald and Inter (SIL Open Font License; license files next to them) |
| `assets/vendor/gsap.min.js` | GSAP 3.15.0, so that renders work offline ([license](https://gsap.com/standard-license)) |

Not in git (see `.gitignore`): `assets/audio/` (the audio cut), `assets/sprites/` (copies of `transmit/public/assets/sprites/alien/`), `renders/` and `snapshots/`. The episode MP3 downloads to `assets/audiobook/cartoon/` at the repository root, which is also ignored.

## Rebuilding

Requires Node 22+ and ffmpeg. HyperFrames needs a Chrome headless shell. In a Claude Code cloud session, use the pre-installed one:

```bash
export HYPERFRAMES_BROWSER_PATH=/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell
```

On another computer, run `npx hyperframes browser ensure` once.

```bash
npm install                                  # installs the pinned hyperframes CLI
node tools/build-part.mjs parts/part-01.json # audio cut with sound effects, sprites, data/part-01.js, index.html
npx hyperframes check                        # lint, runtime, layout, motion, contrast
npx hyperframes snapshot --at 5,20,40 --describe false   # look at frames
npx hyperframes render --quality high --output ../../../audiobook/cartoon/part-01-opening.mp4
node tools/build-part.mjs parts/part-01.json --aspect 9x16   # then the tall version
npx hyperframes render --quality high --output ../../../audiobook/cartoon/part-01-opening-9x16.mp4
```

Captions: the 9:16 version has them burned in (Shorts, Reels and TikTok scroll with the sound off). The 16:9 version has none on the picture; upload `data/part-NN.srt` (written by every build) to YouTube as its closed captions. `--captions` burns them into 16:9 anyway.

Build and render one shape at a time: the build rewrites `index.html`, `data/part.js` and the compositions' canvas size. Media too big for git (the theme song music video) is read from the main checkout when the build runs in a worktree.

Always pass `--describe false` to `snapshot`. Otherwise it sends the frames to Gemini when a Gemini key is set.

Rendering Part 2 (147 s, 30 fps) took about 8 minutes on 4 CPU cores with no GPU.

## How it works

- **Timing comes from the words.** `build-part.mjs` finds each scene's start from its cue word in `word-timings.json`. Each scene starts its animations with `KIT.cue("s07", "604")`, which gives that word's start in scene time. If the timings change, rebuild; the scenes follow.
- **Lip-sync.** Each word's letters are spread over its duration and mapped with `CHAR_TO_VISEME` (the same table as `packages/wishonia-widget/src/core/viseme-map.ts` in mikepsinn/optimitron). A pause of 0.18 s or more shows the resting mouth of the current state. `getHeadName` falls back to an available mouth.
- **Blinks and idle motion** follow `transmit/public/assets/js/characters.js`: `blink-smile` for 150 ms in pauses, and a head rock from -2° to +2° on a 7-second loop.
- **Determinism.** No `Math.random` and no clock: confetti uses a seeded generator, and everything that changes over time is a function of the seek time (`KIT.onTime`).

## Writing a collage scene

Each scene loads `assets/js/art-sizes.js` (every cut-out's size, written by `tools/art-sizes.py`, which `tools/art-cutout.py` runs) just before `assets/js/collage.js`. A collage scene is a spec for `KIT.collage` (`assets/js/collage.js`): cut-outs from `assets/art/collage/` on aged paper, moving on twos (12 drawings a second) under the period film. Copy `compositions/scenes/pilot-collage/split-the-atom.html`, replace every `split-the-atom` with the scene id, and write the spec. Check it with `--data-only` and `tools/scene-check.mjs`.

```js
KIT.collage({
  id: "pointing-at-each-other", seed: 312,          // seed: the film grain (any number)
  cast: { sam: { art: "uncle-sam", x: 150, y: 1000, anchor: [0, 697], scale: 1.1 } },
  beats: [{ on: "when", do: "slideIn", who: "sam", from: "left" }],
});
```

**Plate:** `plate: [x0, y0, x1, y1]` (canvas px) is the area the paper covers, and a `wash` or a flash with it; give it when the camera travels past the frame (default: the frame).

**Host shots** (layer A) are collage specs too: `host: true` (or `{ push: [1, 1.07], iris: ["in", 0.04, 0.7] }`) draws Wishonia at her console on the observation deck (`KIT.studio`) with no paper, and the cast stands in front of the console. Her expressions come from the part file's `wishonia` list, as in `parts/part-02.json`. `KIT.STUDIO` gives the set's points in canvas px: `top` (the console's ledge), `button`, `earth` ([x, y, r] of Earth in the window), `face`. Give the root a dark background (`#0B0805`).

**Cast** (z-order is the order written; a cut piece of `cut` sits in front of the whole cast). Positions are canvas px (1920 × 1080); points on a cut-out are art px (`KIT.collage.SIZES` has each art's size; add new art there).

| Field | Meaning |
| --- | --- |
| `art` | the file name in `assets/art/collage/` without `.webp` |
| `x`, `y`, `anchor` | the art point `anchor` (art px, or `"center"` (default), `"bottom"`, `"top"`, `"left"`, `"right"`, `"topleft"`) goes on canvas `x`, `y` |
| `scale` | size (default 1) |
| `pivot` | the point it turns, squashes and folds on (art px or a keyword; default its middle) |
| `clip` | show only part of the art: `"left"`, `"right"`, `"top"`, `"bottom"` or a polygon in art px |
| `pieces` | `{ name: { clip, pivot, pieces } }`: the art drawn as hinged pieces (nest them); a piece is `"actor.name"` in beats |
| `cut` | `"lr"` or `"tb"`: halves `actor.L`/`actor.R` (or `.T`/`.B`), hidden until `split` |
| `points` | named art points, `{ tip: [341, 208] }`, for `move` (`to: "sam.tip"`) |
| `eyes`, `smoke` | art points where white eyes and smoke appear when charred; `eyeSize` (30 px) |
| `faces` | `"left"` if the cut-out faces left (`nudge` pushes the way it faces) |
| `label` | words drawn on the art, moving with it: `{ text, at: [art x, art y], width (art px), size, tilt }` or a list of them |
| `hidden` | start hidden (otherwise a cut-out whose first move is an entrance starts hidden) |

**Beats** run in the order written, which is also the order their effects add up. Every beat has `do` and a time: `on` (a spoken word, as `KIT.cue` takes it; `n` for its n-th time in the scene) plus an optional `offset` in seconds, or `at` (scene seconds). `who` is a name or a list of names. One drawing is 1/12 s (0.083).

| `do` | What happens; options (defaults) |
| --- | --- |
| `slideIn` | slides in rigidly over 6 drawings, overshoots and settles; `from` (`"left"`), `dist` (just off the frame), `over` (22 px), `tilt` (0°; it rocks on its pivot as it stops) |
| `slideOut` | accelerates off and hides; `to` (`"left"`), `dist`, `dur` (0.42) |
| `hinge` | a piece swings on its pivot; `angle` (30°), `frames` (1), `hold` (s; then it swings back; leave out to stay open) |
| `bow` | a stiff bow from the waist piece and back up; `angle` (27°), `hold` (0.62) |
| `stamp` | `who` slams down from big with a jolt; `from` (2.3), `shake` (7). With `text`, a red rubber stamp: on the sign `who` (under its title), on the cut-out `who` at `spot` (art px), or free at `x`, `y` (its text fitted to `width`, 1000 px); `size` (56), `tilt` (-3°), `from` (1.9), `id` |
| `pop` | pops up from nothing with an overshoot; `squash: true` squashes and stretches as it pops, `swell` (grows by this much by the scene's end), `out: true` pops away and hides |
| `swap` | `who` hides and `to` (another cast name) appears in its place with a squash |
| `shiver` | shakes in place; `dur` (0.75), `amp` (8 px), `rot` (4°) |
| `bob` | an idle stiff bob; `y` (6 px), `r` (2°), `speed` (1), `phase`, `until` (a word or seconds), `fade` (0.4 s in and out) |
| `move` | goes to `to` (canvas `[x, y]`, a cast name, or `"name.point"`, which it then rides along with), plus `by` [dx, dy] (or `by` alone: a relative move), straightening to `turn` (0°); `dur` (4 drawings), `ease` (`"linear"` or `"smooth"`), `arc` (px it lifts on the way), `scale` (its scale on arrival). The middle of a `clip`/`cut` half is its cut edge |
| `nudge` | a jab: out by `by` ([40, 0], x the way it faces) in one drawing, back in three |
| `hop` | a little hop; `height` (34) |
| `drop` | falls off the bottom and hides; `dur` (0.6), `dist` (1250), `drift` (0), `spin` (30°) |
| `split` | a `cut` cut-out flies apart into its halves; `gap` (300 px), `spin` (14°), `shake` (9) |
| `char` | turns black; its `eyes` show white and its `smoke` puffs |
| `blink` | its eyes blink for two drawings (charred cut-outs) |
| `ash` | folds down into a little heap of ash on its pivot; the eyes stay round on top |
| `sunburst` | a turning sunburst with a glow pops up behind everything; `x`, `y` (the middle), `r` (1300), `glow` (true), `angle` (its turn at scene start, to continue the last scene), `enter: "none"` (already there), `id` (`"sunburst"`; `pop` with `out` shuts it) |
| `banner` | a card with the words slams in, the text fitted (`KIT.fitText`) to `width`; `text`, `x` (960), `y` (780, its middle), `size` (150, the largest font size), `width` (1080), `color` (`"red"` border or `"ink"`), `pad` (110), `lineHeight` (1.25), `spacing` (letter-spacing, 0 px), `tilt` (-2°), `id` (`"banner"`) |
| `tag` | a hang-tag on a string pops onto `who` and swings; `text` (fitted), `x`, `y` (its middle; default right of `who`), `w` (500), `h` (250), `knot` (art px on `who` where the string ties), `swing` (3°), `under` (a cast name to sit just behind), `id` (`"tag"`) |
| `glow` | a pulsing glow grows behind `who` and follows it; `dur` (0.9), `size` (220) |
| `sparks` | zigzag sparks between two cut-outs, `who: [a, b]`, new each drawing; `until` |
| `boom` | a white flash and a shake that dies away; `shake` (16), `flash` (0.25 s) |
| `shake` | the frame jolts for `frames` (4); `x` or `y` (px) |
| `show`, `hide` | at once |
| `flatten` | squashes flat on its pivot in two drawings (give it `pivot: "bottom"`) |
| `chart` | draws axes on the paper behind the cast: `chart` is `KIT.collage.axes({ box: [left, top, right, bottom], x: [min, max, tick], y: [min, max, tick], xLabels, yLabels, unit, title, subtitle, size })`, whose `pt(x, y)` gives the canvas px of a data point for the other beats; `enter` (a direction to slide in from; otherwise it is just there), `id` (`"chart"`) |
| `rule` | a dashed line across the chart at value `y` that draws itself left to right; `chart`, `text` (its label, at the right end; `labelAt: "left"`, `below: true`), `from`, `to` (x values; the whole chart), `color` (`"red"` or `"ink"`), `size` (32), `dur` (0.5), `id` (`"rule"`) |
| `chain` | copies of a cut-out appear one at a time, faster and faster, each popping out of the one before and hopping to its place, with an ink line through their feet: a line chart made of cut-outs. Places: `points` (canvas px), or `chart`, `f` (y of x) and `x: [from, to]` every `step` (0.5). `art` (a name or a list to cycle), `pose(i, n)` (the art for copy i), `scale`, or `height` (canvas px, every art the same height) with `sizes` (`{ tank: 0.6 }`, per-art multipliers), `anchor` (`"bottom"`), `until` (when the last appears; or `dur`, 2), `accel` (0.6; 1 is even), `jiggle` (2 px), `line: false`, `lineColor` (`"red"` or a colour), `lineWidth` (5), `join` (another chain: start from its last copy), `id` (`"chain"`; copies are `id.0`, `id.1`, ...) |
| `bar` | a hatched bar on a chart at `x` (data) that grows from its last height to `to` over `dur` (0.6); the same `id` again grows or shrinks it; `chart`, `width` (80 px), `text` (a label riding its top), `size` (30), `fill` |
| `wash` | a flat colour over the plate fading to `opacity` (1) over `dur` (0.8): `blend: "saturation"` (default) drains the colour out of what is under it, `"normal"` tints; `color` (`"#888"`), `above` (a cast name: it sits just above that one, so the cast written after it keeps its colour; default behind the cast); the same `id` again changes it |
| `camera` | moves the camera to `view` over `dur` (0.6), with `views: { wide: [960, 540, 1], close: [x, y, scale] }` in the spec (and `view`, the first) |

## Adding the other parts

1. Copy `parts/part-02.json` to `parts/part-NN.json`. Set the audio cut and the scenes from its storyboard (`storyboards/part-NN-*.md`).
2. Write one composition for each scene in `compositions/scenes/`, with `kit.js` for the art and `KIT.cue` for the timing. Load `data/part-NN.js` in each one.
3. Run the build, the check and the render for that part. Join the parts with ffmpeg.
