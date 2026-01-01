# Book Chapter OG Image Generator

Automatically generates Open Graph (OG) images for book chapters that don't already have them.

## What It Does

The `book-chapters` command:

1. **Scans all book QMD files** using `getBookFilesForProcessing()` from file-utils
2. **Checks frontmatter** for existing `image` field
3. **Skips files** that already have images (won't regenerate)
4. **Generates OG images** using Google Gemini's image generation API
5. **Updates frontmatter** with the image path automatically

## Usage

### Generate images for all chapters without images:

```bash
npm run images:generate:chapters
```

Or directly:

```bash
npx tsx scripts/generate-project-images.ts book-chapters
```

### Prerequisites

Set your Google Gemini API key in `.env`:

```bash
GOOGLE_GENERATIVE_AI_API_KEY=your_api_key_here
```

Get your API key from: https://aistudio.google.com/app/apikey

## How It Works

### 1. File Discovery

Uses `getBookFilesForProcessing()` which:
- Finds all `.qmd` files in `knowledge/**`
- Includes `index*.qmd` files from root
- Excludes:
  - `knowledge/references.qmd`
  - `knowledge/includes/` folder
  - `knowledge/figures/` folder
  - `knowledge/appendix/parameters-and-calculations.qmd` (auto-generated)
  - Files in `_freeze/` or `_book/` directories

### 2. Frontmatter Check

For each file, reads frontmatter using `gray-matter`:

```yaml
---
title: "Chapter Title"
description: "Chapter description"
tags: [tag1, tag2]
image: /assets/og-images/knowledge/chapter.png  # If exists, SKIP
---
```

### 3. Prompt Generation

Creates a professional infographic prompt based on:
- **Title**: From frontmatter or filename
- **Description**: From frontmatter
- **Tags**: From frontmatter
- **Style guide**: Neobrutalist + 90s computer aesthetic

Example generated prompt:
```
Create a professional, data-driven infographic for "Economic Analysis".
Style: Modern neobrutalist design blended with 90s computer program aesthetic

Content:
- Main title: "Economic Analysis" in large, bold typography
- Subtitle/description: "ROI calculations and cost-benefit analysis"
- Related topics: economics, roi, healthcare
- Visual elements appropriate to the topic
- Color scheme: Professional, trust-inspiring colors (blues, greens, golds)
- Data visualization elements if relevant (charts, graphs, icons)
Layout: Professional report/infographic style, landscape orientation
Size: Social media OG format (1200x630, 16:9)
Mood: Authoritative, informative, professional, engaging
```

### 4. Image Generation

- **Output directory**: `assets/og-images/{relative-path-to-qmd}/`
- **Filename**: `{qmd-filename}.png`
- **Aspect ratio**: 16:9 (1200x630 for OG images)
- **API**: Google Gemini Imagen

Example:
- QMD file: `knowledge/economics/economics.qmd`
- Image saved: `assets/og-images/knowledge/economics/economics.png`

### 5. Frontmatter Update

Automatically adds image path to frontmatter:

```yaml
---
title: "Economic Analysis"
description: "ROI calculations and cost-benefit analysis"
tags: [economics, roi, healthcare]
image: /assets/og-images/knowledge/economics/economics.png  # ADDED
---
```

## Output Format

The script provides detailed progress:

```
🎨 Project Image Generator
============================================================

============================================================
Generating OG images for book chapters
============================================================

[*] Loading book files...
[OK] Found 84 book files

[1/84] Processing: knowledge/problem.qmd
  Title: Problem Overview
  Description: Humanity's spectacular failure at prioritizing not dying
  Generating OG image...
  [OK] Generated image: assets/og-images/knowledge/problem.png
  [OK] Updated frontmatter in knowledge/problem.qmd

[2/84] Processing: knowledge/economics/economics.qmd
  [SKIP] knowledge/economics/economics.qmd - already has image: /assets/economics/economics-og.jpg

...

============================================================
Book Chapter Image Generation Summary:
  Total files processed: 84
  Images generated: 72
  Files skipped (already have images): 10
  Files failed: 2
============================================================
```

## Features

### ✅ Smart Skipping
- Files with existing `image` field → **skipped**
- Files without title/description → **skipped**
- Only generates for files that need images

### ✅ Error Handling
- Continues if individual files fail
- Shows summary of successes/failures
- Doesn't crash on errors

### ✅ Automatic Frontmatter Updates
- Uses `stringifyWithFrontmatter()` from file-utils
- Preserves formatting and structure
- Adds image path as absolute URL (`/assets/...`)

### ✅ Consistent File Organization
- All OG images in `assets/og-images/`
- Mirrors directory structure of QMD files
- Easy to find corresponding images

## Example Output

For `knowledge/problem/cost-of-war.qmd`:

**Before:**
```yaml
---
title: "The Cost of War"
description: "Global military spending and its opportunity cost"
tags: [war, economics, military-spending]
---
```

**After:**
```yaml
---
title: "The Cost of War"
description: "Global military spending and its opportunity cost"
tags: [war, economics, military-spending]
image: /assets/og-images/knowledge/problem/cost-of-war.png
---
```

**Generated image location:**
```
assets/og-images/knowledge/problem/cost-of-war.png
```

## Integration with Quarto

The `image` field in frontmatter is automatically used by Quarto for:
- Open Graph meta tags (`og:image`)
- Twitter card images (`twitter:image`)
- Social media previews

Example HTML output:
```html
<meta property="og:image" content="https://manual.WarOnDisease.org/assets/og-images/knowledge/problem/cost-of-war.png">
<meta name="twitter:image" content="https://manual.WarOnDisease.org/assets/og-images/knowledge/problem/cost-of-war.png">
```

## Cost Considerations

Google Gemini Imagen pricing (as of 2024):
- Image generation: ~$0.02 per image
- For 84 chapters: ~$1.68 total
- Re-runs are free (skips existing images)

## Troubleshooting

### "No images generated"
- Check API key is set correctly
- Verify API quota/billing enabled
- Check internet connection

### "Files skipped (no title or description)"
- Add frontmatter to QMD files:
  ```yaml
  ---
  title: "Chapter Title"
  description: "Brief description"
  ---
  ```

### "Import errors"
- Run from project root
- Ensure dependencies installed: `npm install`
- Use `tsx` not `ts-node`

## Other Commands

### Generate project-specific images:

```bash
# War on Disease branding
npm run images:generate:war

# Economics paper branding
npm run images:generate:economics

# All projects (war + economics)
npm run images:generate
```

These generate:
- OG images (1200x630)
- Twitter cards (1200x675)
- Square icons (512x512)

For project branding/marketing, not individual chapters.
