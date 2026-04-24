---
name: generate-section-images
description: Analyze a QMD file and generate images for sections that would benefit from visual aids (diagrams, charts, infographics, flowcharts).
allowed-tools:
  - Bash
  - Read
  - Glob
  - AskUserQuestion
---

# /generate-section-images [file.qmd]

Analyze a QMD file with Gemini and automatically generate images for sections that would benefit from visual aids.

## Usage
```
/generate-section-images knowledge/economics/1-pct-treaty-impact.qmd
/generate-section-images @knowledge/appendix/invisible-graveyard.qmd
/generate-section-images  (uses current context or recent git changes)
```

---

## How It Works

1. **Analyzes** the entire QMD file with Gemini Flash
2. **Identifies** sections that would benefit from diagrams, charts, infographics, or flowcharts
3. **Generates** detailed visualization prompts with composition instructions
4. **Creates** images using Gemini image generation
5. **Inserts** images at optimal locations in the QMD file

---

## Step 1: Determine Target File

**Priority order:**
1. Explicit file argument (e.g., `knowledge/economics/1-pct-treaty-impact.qmd`)
2. File reference in conversation (e.g., `@knowledge/appendix/file.qmd`)
3. Recent git changes: `git diff --name-only HEAD~3 | grep "\.qmd$" | head -1`

If no file found, ask user to specify.

---

## Step 2: Ask User for Options

Use AskUserQuestion to confirm settings:

**Style:**
- `bw-academic` (Recommended) - Clean black and white scientific illustration
- `retro-futuristic` - Fun retro style with large text

**Aspect Ratio:**
- `1:1` (Recommended) - Square, consistent with manual generations
- `3:4` - Portrait, book-friendly
- `16:9` - Landscape, presentation-friendly

**Mode:**
- `Generate` (Recommended) - Analyze and generate images
- `Dry run` - Show recommendations without generating
- `Force regenerate` - Delete existing section images and regenerate all

---

## Step 3: Run Generation

```bash
npx tsx scripts/images/generate-section-images.ts <file.qmd> [options]
```

**Options:**
- `--retro-futuristic` - Use retro style instead of bw-academic
- `--aspect <ratio>` - Aspect ratio: 1:1, 3:4, 9:16, 16:9
- `--dry-run` - Show recommendations without generating
- `--force` - Delete existing and regenerate all

**Examples:**
```bash
# Default: bw-academic style, 1:1 aspect
npx tsx scripts/images/generate-section-images.ts knowledge/economics/1-pct-treaty-impact.qmd

# With options
npx tsx scripts/images/generate-section-images.ts knowledge/economics/1-pct-treaty-impact.qmd --aspect 3:4

# Dry run first
npx tsx scripts/images/generate-section-images.ts knowledge/economics/1-pct-treaty-impact.qmd --dry-run

# Force regenerate
npx tsx scripts/images/generate-section-images.ts knowledge/economics/1-pct-treaty-impact.qmd --force
```

---

## Step 4: Review Log File

After generation, check the prompt log:
```bash
cat image-prompts.log
```

This shows for each image:
- Section heading and image type
- Visualization goal (composition instructions)
- Content excerpt (data to include)
- Final prompt sent to Gemini

---

## Step 5: Report Results

Report:
- Number of images generated
- Where they were inserted (line numbers)
- Output directory: `assets/images/<qmd-basename>/`
- Remind user to preview the QMD file and review generated images

---

## Output Location

Images are saved to: `assets/images/<qmd-basename>/`

Example:
- `knowledge/economics/1-pct-treaty-impact.qmd`
- Images go to: `assets/images/1-pct-treaty-impact/`

---

## Environment

Requires `GOOGLE_GENERATIVE_AI_API_KEY` environment variable.

---

## Troubleshooting

**Images not inserted:**
- Check if anchor text was found (see console output for `[SKIP]` messages)
- The analysis may have suggested placement locations that don't exist in the file

**Images look wrong:**
- Check `image-prompts.log` to see what prompts were sent
- The visualization goal should contain detailed composition instructions
- If prompts are too vague, the analysis may need improvement

**To regenerate specific images:**
- Delete the image file from `assets/images/<qmd-basename>/`
- Remove the `![...]()` reference from the QMD file
- Run the script again (it will only generate missing images)
