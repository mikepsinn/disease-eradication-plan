# Episode cartoon: how a part gets made

The cartoon of audiobook episode 1 is rendered with HyperFrames, one part at a time, in two shapes: 16:9 (1920 × 1080) and the tall phone version, 9:16 (1080 × 1920). `video/README.md` lists the files and the commands; `cartoon-style-bible.md` describes the look, Wishonia, the cast and the drawing kit.

## Mike's calls

- Real people, brands and logos are fair game: caricature them.
- Gags go all the way, as in the theme song: the bomb goes off, people are charred and blink, the dead become grinning skeletons.
- Keep each framing minimal: one idea on a plain field, nothing the viewer has to work out.
- Money is green, never red; its seal (a missile or a cross) says what it buys.
- Use the numbers the narrator says (the audiobook's figures), not the website's.

## The process

1. **Audio first.** The voice is the published episode MP3. Scene times come from its word timings (`video/tools/word-timings.mjs`); if the narration changes, rebuild the timings and the scenes follow their cue words.
2. **Storyboard, as a beat sheet** (`video/storyboards/part-NN-*.md`, format in `video/storyboards/FORMAT.md`): written from the chapter text and its numbers. For each spoken line, the claim, the visual that shows it and the gag. Mike approves it before any art or animation. `tools/storyboard-times.mjs` fills in the times.
3. **Art and scene specs:** Codex makes the cut-outs the storyboard lists (`video/tools/art-gen.sh`), and each scene is a collage spec (`video/README.md`, "Writing a collage scene").
4. **Part file** (`video/parts/part-NN.json`): the audio cut; each scene's file, cue word, layer and Wishonia states (host scenes only); `media` (other footage); `sounds` placed on spoken words (`tools/sfx.py` synthesizes them).
5. **Scenes** (`video/compositions/scenes/part-NN/<scene-id>.html`). Check each on its own, in both shapes, without a build: `node tools/build-part.mjs parts/part-NN.json --data-only` once, then `node tools/scene-check.mjs part-NN <scene-id> [--aspect 9x16] [--at t1,t2]`.
6. **Build, check, render**, one shape at a time: build, `npx hyperframes check`, snapshot, fix, render. Rebuild 16:9 before committing.

## What breaks if you get it wrong

**Builds and snapshots**
- The build rewrites `index.html`, `data/part.js`, `data/aspect.js` and every scene's canvas size: build and render one shape at a time, and never while someone else snapshots. In a worktree it reads big media (the theme song music video) from the main checkout.
- Pass `--describe false` to `snapshot` (otherwise the frames go to Gemini) and write to your own `-o` folder. A frame taken on a cue word catches the move just starting; snapshot after it settles.

**Keep-out zones.** 16:9: nothing important below y 900 (YouTube's captions and controls). 9:16: nothing in y 1470 to 1700 (the burned-in captions).

**GSAP on SVG**
- Never tween x, y, scale or rotation on an SVG element that has a `transform` attribute: GSAP reads it as its start and the element jumps. Position an outer group; tween an inner one.
- `svgOrigin`: set it once (`gsap.set`) or put it in both halves of a `fromTo`. Passing it to a later tween on an element that has already moved shifts the element.
- `fromTo` renders its from-state at once, so use it for things that appear later. No CSS `transform` on an element you tween.

**Scenes**
- Determinism: no `Math.random` (use `KIT.rng`), no `Date`, no timers, finite repeats.
- A scene id that starts with a digit (`604-papers`) is not a valid CSS selector: get its elements with `getElementById`.
- Text fits its sign: size the sign to the words (`KIT.textWidth`) or the words to the sign (`KIT.fitText`). `scene-check` prints a TEXT OVERFLOW line for each text that runs off its sign.
- To show a hidden element again, set `visibility: "inherit"`, never `"visible"`: a visible child shows through when the runtime hides its scene, so it ghosts over other scenes in the render.
- No full-frame SVG filters for grain: in the render they paint through from scenes that are not on screen. Use `KIT.film`.
- A sound placed after its scene ends plays under the next scene: keep each sound inside its scene.
- A scene that continues the last one ("(no seam)") starts on its final frame, and drawing code shared between the two files changes in both.

**The film look** (`video/assets/js/film.js`, loaded after `kit.js`)
- Every scene has the same layers: `#<id>-weave` holds everything that moves (the camera, a flash, the iris), and `#<id>-film` sits outside it, last. `KIT.film(tl, ID, weave, film, seed)` puts the gate weave on the first and the grain on the second, so the camera never scales the grain.
- A plate is drawn once, in plate units, inside one camera group (`<g id="<id>-cam">`); a framing is a view (plate x, plate y, scale), and each shape has its own `VIEW` table.
- Move the camera with `KIT.camera(VIEW, KEYS)` set in a `KIT.onTime` callback (`camera.place(cam, camera.at(t))`), not with a GSAP tween (the group has a transform attribute).

**People**
- People come in many shapes, so never hard-code a pivot or a hand: `KIT.rig(o)` (the same options you drew the person with; `KIT.castOpts(name, extra)` for a cast member) gives the shoulders and hips (svgOrigin for arms and legs), the neck, the hands, mouth and eyes. `plain: true` gives the standard build.
- `<!--head-end-->` (person units) and `<!--face-end-->` (the face's own units, facing +x) are where to add things to a head. The eyes are `.eye` groups with a `.pupil`.

**Word timings.** The forced alignment sometimes squeezes words to zero length. Measure them with Whisper (faster-whisper small.en, starting the clip in a pause) and `ffmpeg -af silencedetect`, add the fix to `timing-fixes.json` and rerun `video/tools/word-timings.mjs`.

**Generated art.** Every character, prop and backdrop is generated: `video/tools/art-gen.sh` makes a sheet with Codex (free; `ART_PLATE=1` for a full-frame backdrop), and `video/tools/art-cutout.py` cuts it into WebP pieces in `video/assets/art/<name>/`. Pass an existing sheet as the reference so the look matches, keep the sheets as references, use the names in `video/storyboards/ART.md`, and put words on the art in code.

**Several agents.** Agents write only their own scene files; one lead changes the kit, builds and renders.
