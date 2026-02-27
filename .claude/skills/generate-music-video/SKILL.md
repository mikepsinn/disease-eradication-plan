---
name: generate-music-video
description: Generate and iterate on AI music videos using Gemini keyframes + Veo 3.1 animation. Covers prompt writing, scene structure, regeneration, and assembly.
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Glob
  - Grep
  - AskUserQuestion
---

# Music Video Generation

Script: `scripts/generate_music_video.py`
Output: `assets/music-video/` (keyframes/, clips/, final .mp4)

## Commands

```bash
python scripts/generate_music_video.py                  # Full pipeline
python scripts/generate_music_video.py --scene 3        # Single scene
python scripts/generate_music_video.py --scene 3 --force # Regenerate scene
python scripts/generate_music_video.py --force           # Regenerate everything
python scripts/generate_music_video.py --list            # Show scene status
python scripts/generate_music_video.py --skip-keyframes --skip-animate  # Reassemble only
```

When regenerating specific scenes, run them in parallel (separate background commands). Reassemble after all finish.

## Architecture

1. **Keyframe** (Gemini `gemini-3-pro-image-preview`): Static image, first frame of the clip
2. **Veo 3.1** (`veo-3.1-generate-preview`): 8-second video clip animated from the keyframe
3. **ffmpeg**: Speed-adjusts each 8s clip to match lyric timestamps, then concatenates + overlays audio

## The Golden Rule: Keyframe Sets Up, Veo Animates

This is the most important lesson. Split every scene into:

| | Purpose | Example (scene 5) |
|-|---------|-------------------|
| **Keyframe** | Static setup: characters, props, positions | Tiny dollar on plate. Sad scientist with magnifying glass. |
| **Veo** | The action, comedy, punchline | Military contractor steals the dollar bill. |

**Never describe the same action in both.** The keyframe is a still photo. Veo makes it move.

## Prompt Writing Rules

### Keep prompts minimal BUT keep the concept
Only include details that serve the concept or the joke. Every extra detail constrains the model's creativity. But be careful not to cut too deep - before removing anything, ask: "Does this detail convey the concept, add comedy, or describe a key action?"

**The test for every detail: Does it tell the model WHAT to show or HOW things relate?**
- If yes, keep it (even if it seems wordy)
- If it's just decoration/atmosphere, cut it

| DELETE (decorative) | KEEP (conceptual/comedic) |
|--------------------|---------------------------|
| "sitting at desks" | "shoveling money from treasury to bomb factory" |
| "in a cape with a wand" | "a towering grim reaper skeleton in a dark hooded robe creeps up" |
| "in a suit" | "money near the input funnel" (tells model where money goes) |
| "stretching into the distance" | "bounces through gears, dominoes, catapults, and tubes" (the Rube Goldberg details ARE the comedy) |
| "in large retro typography" | "dancing skeletons" (dancing is the joke, not just skeletons) |
| "Navy background, warm orange glow" | "comedy of accidental good deeds" (the concept) |
| "Stars twinkle" | character-defining traits (hooded robe, scythe, trench coat) |

**Key distinction:** Character-defining visual traits (hooded robe, scythe, trench coat, top hat) are NOT the same as generic costume details (cape, wand, suit). The former tell the model what kind of character; the latter are obvious from the character type.

### Don't repeat VISUAL_STYLE
`VISUAL_STYLE` is prepended to every keyframe prompt. Don't add "Navy and orange", "warm orange glow", "navy background" at the end. For veo prompts, a brief "1950s style." or "1950s animation." is enough reinforcement.

### Text in images
- Most scenes use `NO_TEXT` to prevent random text artifacts
- Remove `NO_TEXT` only for scenes that need specific text (book titles, signs, treaty names)
- Put desired text in double quotes: `'A parchment scroll reads "1% Treaty"'`

### Character consistency
Extract recurring characters to variables (e.g., `WISHONIA_PLANET`, `WISHONIA_CHARACTER`) and reference them across scenes.

## Renumbering Scenes

When adding/removing scenes:
1. Update indices in the SCENES list
2. Rename cached files (keyframes + clips) from highest to lowest to avoid collisions:
   ```bash
   for i in 14 13 12 ...; do
     new=$(printf "%02d" $((10#$i + 1)))
     mv "keyframes/scene-${i}.jpg" "keyframes/scene-${new}.jpg"
     mv "clips/scene-${i}.mp4" "clips/scene-${new}.mp4"
   done
   ```
3. New scene number will have no cached files and generate fresh

## Technical Notes

| Topic | Detail |
|-------|--------|
| Image model | `gemini-3-pro-image-preview` (NOT `gemini-3.1-pro-preview`, which returns NO_IMAGE) |
| Veo durations | Exactly 4, 6, or 8 seconds. We always use 8 and speed-adjust with ffmpeg. |
| Veo limitation | Cannot combine `image` (first frame) and `reference_images` in same request |
| Python on Windows | Script needs `sys.stdout.reconfigure(encoding='utf-8')` |
| Rate limits | Gemini image: ~8 req/min. Veo: 4 parallel workers. |
| Retries | Veo has built-in 3-retry logic with backoff for 503s and empty results |
| Safety settings | Set to `BLOCK_NONE` for all categories (content is darkly comedic) |

## Common Pitfalls

- **TS subprocess fails on Windows**: Long prompts cause "Input file is missing" errors via `npx tsx`. Use the Python direct API instead.
- **Style divergence**: Words like "horrific", "ominous", "dark" can push away from the retro 1950s aesthetic. Keep tone light even for dark concepts.
- **"Broadway stage" text appearing**: Avoid words that render as literal text (Broadway, theater, etc.) unless you want text.
- **Coins vs dollar bills**: The project uses dollar bills throughout, not coins.
- **Over-trimming prompts**: When simplifying prompts, NEVER remove: (1) key actions that define the scene concept (shoveling money, creeping closer), (2) specific mechanisms that ARE the comedy (Rube Goldberg gears/tubes/catapults), (3) character-defining visual traits (skeleton, hooded robe, towering), (4) spatial relationships that set up the animation (money near input funnel, characters in a relay line). Only remove: color/background (covered by VISUAL_STYLE), generic costume details (cape, suit, wand), filler adjectives (gleaming, stretching into distance).
- **Gemini safety filters**: "Politicians" in prompts may trigger refusals. Use "marionette figures in suits" or similar abstractions for political satire scenes. The keyframe generator has 3-retry logic but repeated failures indicate the prompt itself needs rewording.
