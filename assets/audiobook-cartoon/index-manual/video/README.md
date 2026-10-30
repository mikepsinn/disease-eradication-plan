# Episode 1 cartoon: HyperFrames project

The cartoon video for audiobook episode 1, "How to End War and Disease (for Busy People)", built with [HyperFrames](https://github.com/heygen-com/hyperframes) (HTML + GSAP rendered to MP4). The voice is the audiobook MP3. There is no text-to-speech. The plan, the scene script and the style bible are in the folder above this one.

**Part 1, "Opening"** (`parts/part-01.json`, `compositions/scenes/part-01/`) is the first part built on the current audio, in the earlier office look, with synthesized sound effects. The other parts use the 1950s atomic-age film look (`../cartoon-style-bible.md`, section 1); Part 2 in that look (`parts/part-02-atomic.json`, `compositions/scenes/style-atomic/part-02/`) is the reference. The storyboards for every part are in `storyboards/`, one per part. The old pilot, Part 2 "Hello, human" (`parts/part-02.json`, `compositions/scenes/s*.html`), was built on the March 2026 audio, whose narration is no longer in the episode.

Every part renders twice: 16:9 (1920 × 1080) and the tall phone version, 9:16 (1080 × 1920).

| File | Purpose |
| --- | --- |
| `STORYBOARD.md` | Part 2, scene by scene: cue word, layer, what moves on which word |
| `parts/part-02.json` | The audio cut, and for each scene: cue word, composition file, Wishonia states |
| `storyboards/part-NN-*.md` | One storyboard per part, for review before anything is animated |
| `storyboards/part-NN-*.sketch.mjs` | The sketch of each scene's key moment, drawn with `kit.js` |
| `storyboards/part-NN-*.html` | Generated: the sketch sheet to review (`node tools/storyboard-sheet.mjs storyboards/part-NN-*.md`; add `--inline <file>` for a self-contained copy to publish) |
| `tools/word-timings.mjs` | Rebuilds `../word-timings.json` and the transcripts from the audiobook pipeline's alignment |
| `tools/build-part.mjs` | Cuts the MP3, mixes in the sound effects, copies the sprites and media, writes `data/part-NN.js` and `index.html` (`--aspect 9x16` for the tall version; `--data-only` writes just `data/part-NN.js`, for checking scenes while another part builds) |
| `tools/scene-check.mjs` | Loads one scene with its part's data in headless Chrome, in either shape, reports page errors and saves frames and a contact sheet to `snapshots/scene-check/` |
| `tools/props-sheet.mjs` | Draws the shared props library (`assets/js/props/*.js`) on review sheets in `snapshots/props/` |
| `tools/sfx.py` | Synthesizes the sound effects (thunk, stamp, slide whistle and so on) with numpy; nothing is downloaded |
| `data/part-NN.js` | Generated: scene times, words, mouth track, blinks, caption groups, sound times |
| `index.html` | Generated: the root composition (scenes, captions, voice) |
| `compositions/scenes/*.html` | One composition for each scene |
| `compositions/captions.html` | Captions from the word timings, with the spoken word highlighted |
| `assets/js/kit.js` | Shared code: cue times, the Wishonia rig, and all SVG art for both layers |
| `assets/js/film.js` | The film look (Parts 2 to 27): the period film, the host's studio set, the iris, and the camera that travels over a plate. Load it after `kit.js` |
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

## Adding the other parts

1. Copy `parts/part-02.json` to `parts/part-NN.json`. Set the audio cut and the scenes from `cartoon-script.md`.
2. Write one composition for each scene in `compositions/scenes/`, with `kit.js` for the art and `KIT.cue` for the timing. Load `data/part-NN.js` in each one.
3. Run the build, the check and the render for that part. Join the parts with ffmpeg.
