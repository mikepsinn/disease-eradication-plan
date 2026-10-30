# Episode cartoon: how a part gets made

The cartoon of audiobook episode 1 is drawn in code and rendered with HyperFrames, one part at a time, in two shapes: 16:9 (1920 × 1080) and the tall phone version, 9:16 (1080 × 1920).

Read these first:
- `cartoon-style-bible.md`: the look, Wishonia, the humans, the recurring gags, the drawing kit.
- `video/README.md`: the files and the commands.
- `video/assets/js/film.js`: the film look's shared code (`KIT.film`, `KIT.studio`, `KIT.iris`, `KIT.camera`). Every scene of Parts 2 to 27 loads it after `kit.js`.
- `video/assets/js/props/*.js`: the shared props library (`KIT.props.<name>`, documented at each function; `node video/tools/props-sheet.mjs [file]` draws them) and `KIT.titleScene` (title.js; copy `video/compositions/scenes/_templates/title-card.html` for a part's title card). Use these and the cast instead of drawing your own versions.
- `video/storyboards/README.md`: every part, the shorts and the props (generated).
- `video/compositions/scenes/part-02/` (`video/parts/part-02.json`): Part 2 in the film look, the reference for every kind of shot: the title card, a host shot that irises in (host-opens), a plate the camera travels round (money-loop), a death toll (the-toll) and a host shot with a guest that irises out (host-closes). Copy their form.
- `video/storyboards/part-01-opening.md`: the storyboard form.

## The process

1. **Audio first.** The voice is the published episode MP3. Scene times come from `word-timings.json` (`video/tools/word-timings.mjs`). If the narration changes, re-voice the episode and rebuild the timings first; the scenes follow their cue words.
2. **Storyboard** (`video/storyboards/part-NN-*.md`). One scene per beat, with a name, not a number (feedback says "loved-ones: make the form smaller"). Each scene has transition_in, key, cue, layer (A, the host at her lectern, or B, a plate), scene, voiceover, wishonia (host shots only), props and status, then **Moves** (each on a quoted spoken word: what the camera frames for each phrase, and what the actors do), **Sound**, **On screen**, **No** and **Why**. `tools/storyboard-times.mjs` fills in the times and voiceover from the cue words; `tools/storyboard-index.mjs` rewrites the README.
3. **Sketches** (`part-NN-*.sketch.mjs`): each scene's key frame, drawn with the kit. `tools/storyboard-sheet.mjs` builds the review sheet. Mike reviews the sheet, by scene name, before anything is animated.
4. **Comedy pass.** The moves are the jokes. Every plate has an actor that moves on the words; reactions land a beat after the line (`KIT.after`). No slideshow (a new text card every scene), no screensaver (motion that says nothing) and no busy diagram (labels, arrows, a dozen small things at once).
5. **Part file** (`video/parts/part-NN.json`): the audio cut; each scene's id, file, cue word, approximate time, layer and Wishonia states; `noCaptions` for title cards; `media` (other footage); `sounds`, placed on spoken words, from the effects `tools/sfx.py` synthesizes (nothing is downloaded).
6. **Scenes** (`video/compositions/scenes/part-NN/<scene-id>.html`), one per scene. A host shot uses `KIT.studio`; a plate is drawn once and has its own camera views for each shape.
7. **Check.** While writing, check each scene on its own in both shapes without a build: `node tools/build-part.mjs parts/part-NN.json --data-only` once, then `node tools/scene-check.mjs part-NN <scene-id> [--aspect 9x16] [--at t1,t2]` and read its contact sheet. Then build 16:9, `npx hyperframes lint`, snapshot every key moment, read the contact sheets, fix. Then build 9:16 and do the same.
8. **Render** 16:9, then build and render 9:16. Rebuild 16:9 before committing.

## Rules that are easy to get wrong

**Builds**
- Build and render one shape at a time. The build rewrites `index.html`, `data/part.js`, `data/aspect.js` and every scene's canvas size, so never build while someone else is snapshotting, and commit after a 16:9 build.
- In a worktree the build reads big git-ignored media (the theme song music video) from the main checkout.

**Both shapes.** Keep-out zones:

| | Captions |
| --- | --- |
| 16:9 | none burned in (YouTube's captions and controls sit there), so nothing important below y 900 |
| 9:16 | y 1470 to 1700 (keep above 1450) |

**The film look**
- Every scene has the same layers: `#<id>-weave` holds everything that moves (the camera, a flash, the iris), and `#<id>-film` sits outside it, last. `KIT.film(tl, ID, weave, film, seed)` puts the gate weave on the first and the grain on the second, so the camera never scales the grain. Use a different seed in each scene.
- A plate is drawn once, in plate units, inside one camera group (`<g id="<id>-cam">`). Every station of the scene lives on it, so a framing is a view (plate x, plate y, scale), and both shapes share the drawing with their own `VIEW` tables.
- Move the camera with `KIT.camera(VIEW, KEYS)` and set it in a `KIT.onTime` callback (`camera.place(cam, camera.at(t))`), not with a GSAP tween (the group has a transform attribute). To chase something (a missile), bend `camera.at(t)` before placing it.
- Wishonia's states go only on Layer A (host) scenes in the part file; the plates do not mount her.
- Money is green, never red. Its seal (a missile for war, a cross for medicine) says what it buys.

**GSAP on SVG**
- Never tween x, y, scale or rotation on an SVG element that has a `transform` attribute: GSAP reads it as its start and the element jumps. Position an outer group; tween an inner one.
- `svgOrigin`: set it once (`gsap.set`) or put it in both halves of a `fromTo`. Passing it to a later tween on an element that has already moved shifts the element.
- `fromTo` renders its from-state at once, so use it for things that appear later. No CSS `transform` on an element you tween.

**Scenes**
- Determinism: no `Math.random` (use `KIT.rng`), no `Date`, no timers, finite repeats.
- A scene id that starts with a digit (`604-papers`) is not a valid CSS selector. Get its elements with `getElementById`.
- Text fits its sign with room at each end: size the sign to the words (`KIT.textWidth`) or the words to the sign (`KIT.fitText`). `tools/scene-check.mjs` and `tools/sheet-shot.mjs` print a TEXT OVERFLOW line for each text that runs off its sign; fix every one.

**People**
- People come in many shapes, so never hard-code a pivot or a hand. `KIT.rig(o)` (with the same options you drew the person with; `KIT.castOpts(name, extra)` for a cast member) gives the shoulders and hips (svgOrigin for arms and legs), the neck (for the head), the hands, mouth and eyes.
- `plain: true` gives the standard build (shoulders at (±17, -26)) when a gag needs a predictable body; otherwise each human's build comes from its outfit, skin tone and color.
- `<!--head-end-->` (person units) and `<!--face-end-->` (the face's own units, facing +x) are where to add things to a head. The eyes are `.eye` groups with a `.pupil`.

**Continuity**
- A scene that continues the last one ("same plate (no seam)" or "same shot (no seam)") starts on the last scene's final frame.
- That drawing code is copied between the two files (eligible and meet-wishonia, for one). Change both.

**Sound**
- A sound placed after its scene ends plays under the next scene. Keep each sound inside its scene, or put its visual in the next scene (the YES tick at the start of eligible).

**Word timings**
- The forced alignment sometimes squeezes words to zero length. Measure them with Whisper (faster-whisper small.en, starting the clip in a pause) and `ffmpeg -af silencedetect`.
- Add the fix to `timing-fixes.json`, then rerun `video/tools/word-timings.mjs`.

**Snapshots**
- Always pass `--describe false`.
- Write to your own `-o` folder.
- A frame taken on a cue word catches the move just starting. To judge where things end up, snapshot a moment after the move settles.
- `tools/scene-check.mjs` checks one scene in isolation (both shapes, page errors, a contact sheet) and is safe to run while another part builds or renders. For lower-level checks (for example a camera transform), load its template in headless Chrome with `puppeteer-core` from `video/node_modules`, seek with `window.__timelines[id].seek(t, false)` (without `false` the `KIT.onTime` callbacks can stay silent) and read the computed styles. Set `window.HF_ASPECT = "9x16"` before `kit.js` loads to see the tall version without a build.

**Art.** Art is drawn in code, with two exceptions: the theme song music video in Part 1, and generated cut-outs (`video/assets/art/<name>/`) for the few things code draws badly.

**Generated art**
- Generate a thing only when all of these hold: its shape is organic (cloth, faces, hands, fur, tattered edges); it is seen big and long (about a sixth of the frame or more, for a couple of seconds); it moves as a whole or in a few parts (swapping poses, turning an arm, changing a face); it comes back across parts; and it carries no words or numbers. If the code version looks like a placeholder at its real size and screen time, compare the two in a real frame; Codex is free, so the test takes a minute.
- Generated so far: the Grim Reaper (`KIT.reaper`). Candidates when their scenes are made: the disease blob, the Democracy Dog, the screaming Calculator, the robot and the Optimitron, and the grumpy missile where it is shown big. People, money, papers, signs, buildings, maps, charts and labels stay in code.
- `video/tools/art-gen.sh` makes a sheet and `video/tools/art-cutout.py` cuts it into WebP pieces. Make two sheets per character from the same references: whole poses side by side at one size, and a puppet (the body without arms or head, each arm alone, the faces). Keep the sheets in `assets/art/<name>/sheets/` as the references for new poses. A kit function places the pieces in its own units from the boxes art-cutout prints, as `KIT.reaper` does. Words and numbers on the art go on top, in code.

## Working with several agents

Give each agent about two scenes. Each agent's brief:
- this file
- its scenes' storyboard sections, sketches and sounds
- the scene times

Agents write only their own scene files. One lead makes kit changes, runs the builds, checks 9:16 and renders.
