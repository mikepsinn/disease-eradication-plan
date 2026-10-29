# Episode cartoon: how a part gets made

The cartoon of audiobook episode 1 is drawn in code and rendered with HyperFrames, one part at a time, in two shapes: 16:9 (1920 × 1080) and the tall phone version, 9:16 (1080 × 1920).

Read these first:
- `cartoon-style-bible.md`: the look, Wishonia, the humans, the recurring gags, the drawing kit.
- `video/README.md`: the files and the commands.
- `video/storyboards/README.md`: every part, the shorts and the props (generated).
- `video/storyboards/part-01-opening.md` and `video/compositions/scenes/part-01/`: the first finished part. Copy their form.

## The process

1. **Audio first.** The voice is the published episode MP3. Scene times come from `word-timings.json` (`video/tools/word-timings.mjs`). If the narration changes, re-voice the episode and rebuild the timings first; the scenes follow their cue words.
2. **Storyboard** (`video/storyboards/part-NN-*.md`). One scene per beat, with a name, not a number (feedback says "loved-ones: make the form smaller"). Each scene has transition_in, key, cue, layer, scene, voiceover, wishonia, props and status, then **Moves** (each on a quoted spoken word), **Sound**, **On screen**, **No** and **Why**. `tools/storyboard-times.mjs` fills in the times and voiceover from the cue words; `tools/storyboard-index.mjs` rewrites the README.
3. **Sketches** (`part-NN-*.sketch.mjs`): each scene's key frame, drawn with the kit. `tools/storyboard-sheet.mjs` builds the review sheet. Mike reviews the sheet, by scene name, before anything is animated.
4. **Comedy pass.** The moves are the jokes. Every Layer B scene has an actor that moves on the words; reactions land a beat after the line (`KIT.after`). No slideshow (a new text card every scene) and no screensaver (motion that says nothing).
5. **Part file** (`video/parts/part-NN.json`): the audio cut; each scene's id, file, cue word, approximate time, layer and Wishonia states; `noCaptions` for title cards; `media` (other footage); `sounds`, placed on spoken words, from the effects `tools/sfx.py` synthesizes (nothing is downloaded).
6. **Scenes** (`video/compositions/scenes/part-NN/<scene-id>.html`), one per scene, each with its own layout for each shape.
7. **Check.** Build 16:9, `npx hyperframes lint`, snapshot every key moment, read the contact sheets, fix. Then build 9:16 and do the same.
8. **Render** 16:9, then build and render 9:16. Rebuild 16:9 before committing.

## Rules that are easy to get wrong

**Builds**
- Build and render one shape at a time. The build rewrites `index.html`, `data/part.js`, `data/aspect.js` and every scene's canvas size, so never build while someone else is snapshotting, and commit after a 16:9 build.
- In a worktree the build reads big git-ignored media (the theme song music video) from the main checkout.

**Both shapes.** Keep-out zones:

| | Captions | Wishonia's corner frame (Layer B) | Countdown board |
| --- | --- | --- | --- |
| 16:9 | nothing important below y 900 | circle at (1760, 740), r 128 | top left, x < 440 and y < 190 |
| 9:16 | y 1470 to 1700 (keep above 1450) | circle at (902, 300), r 122 | top left, x < 400 and y < 200 |

**GSAP on SVG**
- Never tween x, y, scale or rotation on an SVG element that has a `transform` attribute: GSAP reads it as its start and the element jumps. Position an outer group; tween an inner one.
- `svgOrigin`: set it once (`gsap.set`) or put it in both halves of a `fromTo`. Passing it to a later tween on an element that has already moved shifts the element.
- `fromTo` renders its from-state at once, so use it for things that appear later. No CSS `transform` on an element you tween.

**Scenes**
- Determinism: no `Math.random` (use `KIT.rng`), no `Date`, no timers, finite repeats.
- A scene id that starts with a digit (`604-papers`) is not a valid CSS selector. Get its elements with `getElementById`.

**Offices and zooms**
- Office scenes use the `KIT.OFFICE` positions. A scene that moves its wall screen (earth-means-dirt in 16:9) makes the next zoom-in scene pass that screen box to `KIT.enter`.
- Wall-screen zooms go through `KIT.zoomView` and `KIT.enter`. An office scene that zooms out draws the previous Earth frame inside its screen with `KIT.zoomView(screen).mini`, so the zoom starts on that frame.
- In scenes that zoom, keep the countdown board and the grain outside the camera wrapper, so they stay put.

**Continuity**
- A scene that continues the last one ("same form (no seam)", a cut between two office scenes, a zoom-out) starts on the last scene's final frame.
- That drawing code is copied between the two files (nuclear-winters and eligible, eligible and meet-wishonia, fire-on-fire and earth-means-dirt). Change both.

**Sound**
- A sound placed after its scene ends plays under the next scene. Keep each sound inside its scene, or put its visual in the next scene (the YES tick at the start of eligible).

**Word timings**
- The forced alignment sometimes squeezes words to zero length. Measure them with Whisper (faster-whisper small.en, starting the clip in a pause) and `ffmpeg -af silencedetect`.
- Add the fix to `timing-fixes.json`, then rerun `video/tools/word-timings.mjs`.

**Snapshots**
- Always pass `--describe false`.
- Write to your own `-o` folder.
- A frame taken on a cue word catches the move just starting. To judge where things end up, snapshot a moment after the move settles.
- To check one scene in isolation (for example a camera transform), load its template in headless Chrome with `puppeteer-core` from `video/node_modules`, seek with `window.__timelines[id].seek(t, false)` (without `false` the `KIT.onTime` callbacks can stay silent) and read the computed styles. Set `window.HF_ASPECT = "9x16"` before `kit.js` loads to see the tall version without a build.

**Art**
- All art is drawn in code. The only AI-made footage is the theme song music video in Part 1.

## Working with several agents

Give each agent about two scenes. Each agent's brief:
- this file
- its scenes' storyboard sections, sketches and sounds
- the scene times

Agents write only their own scene files. One lead makes kit changes, runs the builds, checks 9:16 and renders.
