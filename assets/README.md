# Assets Folder

This folder contains all image assets for the book "The Complete Idiot's Guide to Ending War and Disease."

## Contents

- **132+ images** including charts, infographics, diagrams, logos, and photos
- Images from [ThinkByNumbers.org](https://thinkbynumbers.org)
- Custom-generated charts and visualizations
- Platform architecture diagrams
- Branding assets (dFDA logos, icons)

## Image Guide

See **[IMAGE-GUIDE.md](IMAGE-GUIDE.md)** for a comprehensive catalog of all images with:

- AI-generated descriptions
- Recommended chapters for each image
- File sizes, formats, and dimensions
- Source attribution
- Keywords and categories

## Adding New Images

When you add a new image to this folder:

1. **Analyze and catalog it:**

   ```bash
   pnpm images:analyze
   ```

   This will:
   - Use Gemini Vision API to analyze the image
   - Generate detailed description and metadata
   - Suggest which chapters should use it
   - Update the IMAGE-GUIDE.md automatically

2. **Or regenerate guide from existing images:**

   ```bash
   pnpm images:guide
   ```

   Quickly regenerates IMAGE-GUIDE.md without re-analyzing images

## Available Scripts

### `pnpm images:analyze`

Analyzes only NEW (unprocessed) images and updates the guide.

- Skips images that have already been analyzed
- Adds AI-generated metadata to image files
- Updates IMAGE-GUIDE.md with new entries

### `pnpm images:analyze:all`

Re-analyzes ALL images, even if previously processed.

- Useful if you want to regenerate all descriptions
- Takes longer (1-2 minutes for 100+ images)
- Uses Gemini API credits

### `pnpm images:guide`

Regenerates IMAGE-GUIDE.md from existing metadata.

- Fastest option (no API calls)
- Reads metadata already stored in images
- Good for quick guide updates after manual edits

## Advanced Options

You can run the script directly with more control:

```bash
# Process only PNG files
pnpm tsx scripts/generate-image-metadata.ts --pattern="*.png"

# Process just 5 images (for testing)
pnpm tsx scripts/generate-image-metadata.ts --limit=5

# Skip updating metadata, just generate guide
pnpm tsx scripts/generate-image-metadata.ts --skip-metadata

# Force re-analyze everything
pnpm tsx scripts/generate-image-metadata.ts --all
```

## Image Metadata

The script stores metadata in images using:

- **PNG files**: Text chunks (via exiftool)
- **JPEG files**: EXIF Comment and UserComment fields
- **Other formats**: Metadata stored in guide only

Metadata includes:

- `description`: AI-generated description of image content
- `keywords`: Relevant search terms
- `chapters`: Recommended chapters for usage
- `source`: Original source URL (if applicable)
- `ai-analyzed`: Marker indicating image has been processed

## Requirements

To use the image analysis script, you need:

1. **Node.js packages** (already installed):
   - `@google/genai` - Gemini Vision API
   - `sharp` - Image processing
   - `glob` - File pattern matching

2. **exiftool** (optional, for metadata writing):

   ```bash
   # Windows (via Chocolatey)
   choco install exiftool

   # macOS
   brew install exiftool

   # Linux
   sudo apt-get install libimage-exiftool-perl
   ```

3. **API Key** in `.env`:

   ```
   GOOGLE_GENERATIVE_AI_API_KEY=your_key_here
   ```

## File Organization

Images are loosely organized by category:

- **Charts & Data**: `*-chart.png`, `*-graph.png`
- **FDA/Health**: `fda-*`, `drug-*`, `health-*`, `life-expectancy-*`
- **Military/War**: `military-*`, `war-*`, `nuclear-*`
- **Democracy**: `voter-*`, `democracy-*`
- **Platform**: `dfda-*`, `dao-*`, `platform-*`
- **Branding**: `dfda-logo*`, `dfda-icon*`
- **ThinkByNumbers**: Images from thinkbynumbers.org articles

## Usage in Book

Reference images in Quarto (`.qmd`) files using relative paths:

```markdown
![Image caption](../../../assets/image-name.png)
```

From different locations:

```markdown
# From brain/book/problem/
![Caption](../../../assets/image-name.png)

# From brain/book/appendix/
![Caption](../../../assets/image-name.png)

# From brain/figures/
![Caption](../../assets/image-name.png)
```

## Best Practices

1. **Use descriptive filenames**: `voter-support-vs-law-passage.png` not `image1.png`
2. **Optimize file sizes**: Run images through compression before adding
3. **Check dimensions**: Most images should be 800-2000px wide
4. **Add attribution**: For external sources, note in filename or metadata
5. **Update guide**: Run `pnpm images:analyze` after adding new images

## Contributing Images

When contributing new images:

1. Add image to `assets/` folder
2. Use descriptive kebab-case filename
3. Run `pnpm images:analyze` to catalog it
4. Commit both the image and updated IMAGE-GUIDE.md

## Troubleshooting

**"exiftool not found"**

- Metadata writing will be skipped
- Guide generation still works
- Install exiftool for full functionality

**"API key not set"**

- Add `GOOGLE_GENERATIVE_AI_API_KEY` to `.env` file
- Get key from [Google AI Studio](https://makersuite.google.com/app/apikey)

**"Rate limit exceeded"**

- Script waits 1 second between API calls
- Process fewer images with `--limit=N`
- Use `--guide-only` to regenerate without API calls

## See Also

- [IMAGE-GUIDE.md](IMAGE-GUIDE.md) - Full image catalog
- [thinkbynumbers-images-guide.md](thinkbynumbers-images-guide.md) - Manual guide for ThinkByNumbers.org images
- [DESIGN_GUIDE.md](../GUIDES/DESIGN_GUIDE.md) - Visual design standards
