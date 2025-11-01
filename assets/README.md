---
title: Assets Folder
description: Image assets, charts, infographics, and branding materials for the book with automated AI-powered cataloging and metadata.
---

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


---
title: ThinkByNumbers.org Images Guide
description: Catalog of images from ThinkByNumbers.org with source URLs and chapter mappings for FDA, military spending, and health data.
---

# ThinkByNumbers.org Images - Usage Guide

This document catalogs all images downloaded from thinkbynumbers.org and maps them to relevant chapters in "The Complete Idiot's Guide to Ending War and Disease."

## FDA and Medical Research Images

### Life Expectancy and Health Explosion

**life-span-explosion.png** (14 KB)

- **Source:** [How many NET lives are saved by efficacy trials?](https://thinkbynumbers.org/health/how-many-net-lives-does-the-fda-save/)
- **Description:** Shows dramatic increase in human life expectancy from ~25 years (ancient times) to ~80 years (modern era), with acceleration beginning around 1800
- **Use in chapters:**
  - `brain/book/proof/historical-precedents.qmd` - Shows historical progress
  - `brain/book/problem/fda-is-unsafe-and-ineffective.qmd` - Context for FDA's impact
  - `brain/book/appendix/impact-of-innovative-medicines-on-life-expectancy.qmd`

**events-leading-to-health-explosion.png** (42 KB)

- **Source:** [How many NET lives are saved by efficacy trials?](https://thinkbynumbers.org/health/how-many-net-lives-does-the-fda-save/)
- **Description:** Timeline showing structural changes (research improvements, incentive improvements) that led to health explosion
- **Use in chapters:**
  - `brain/book/proof/historical-precedents.qmd`
  - `brain/book/problem/fda-is-unsafe-and-ineffective.qmd`

### FDA Regulation Impact

**new-treatments-per-year-2.png** (52 KB) - ALREADY IN ASSETS

- **Description:** Shows 70% reduction in new drug treatments per year following 1962 FDA regulatory changes
- **Use in chapters:**
  - `brain/book/problem/fda-is-unsafe-and-ineffective.qmd` - PRIMARY USE
  - `brain/book/problem/nih-spent-1-trillion-eradicating-0-diseases.qmd`

**lifespan-increase-before-after-1962.png** (85 KB)

- **Source:** [How many NET lives are saved by efficacy trials?](https://thinkbynumbers.org/health/how-many-net-lives-does-the-fda-save/)
- **Description:** Contrasts lifespan increases before 1962 (4 years per decade) vs. after 1962 (2 years per decade)
- **Use in chapters:**
  - `brain/book/problem/fda-is-unsafe-and-ineffective.qmd` - CRITICAL EVIDENCE
  - `brain/book/appendix/impact-of-innovative-medicines-on-life-expectancy.qmd`

**us-swiss-life-expectancy-5.png** (75 KB) - ALREADY IN ASSETS

- **Description:** Compares life expectancy trends between US and Switzerland (different regulatory approaches), showing divergence post-1962
- **Use in chapters:**
  - `brain/book/problem/fda-is-unsafe-and-ineffective.qmd`

**us-swiss-life-expectancy-drug-approvals.png** (184 KB) - ALREADY IN ASSETS

- **Description:** Overlays drug approval rates with comparative life expectancy data
- **Use in chapters:**
  - `brain/book/problem/fda-is-unsafe-and-ineffective.qmd`
  - `brain/book/appendix/dfda-cost-benefit-analysis.qmd`

**cost-to-develop-a-new-drug.png** (24 KB) - ALREADY IN ASSETS

- **Description:** Shows escalating costs from $74M to over $1B (inflation-adjusted)
- **Use in chapters:**
  - `brain/book/problem/fda-is-unsafe-and-ineffective.qmd`
  - `brain/book/problem/nih-spent-1-trillion-eradicating-0-diseases.qmd`
  - `brain/book/appendix/pharmaceutical-industry-randd-analysis.qmd`

**drug-cost-vs-lifespan.png** (51 KB)

- **Source:** [How many NET lives are saved by efficacy trials?](https://thinkbynumbers.org/health/how-many-net-lives-does-the-fda-save/)
- **Description:** Demonstrates correlation between rising development costs and stagnating lifespan improvements
- **Use in chapters:**
  - `brain/book/problem/fda-is-unsafe-and-ineffective.qmd` - POWERFUL VISUALIZATION
  - `brain/book/appendix/dfda-cost-benefit-analysis.qmd`

**diminishing-returns.png** (135 KB) - ALREADY IN ASSETS

- **Description:** Visual representation comparing linear decline vs. exponential decay patterns
- **Use in chapters:**
  - `brain/book/problem/fda-is-unsafe-and-ineffective.qmd`

**thalidomide.jpg** (15 KB) - ALREADY IN ASSETS

- **Description:** Historical newspaper headline about thalidomide tragedy that influenced FDA expansion
- **Use in chapters:**
  - `brain/book/problem/fda-is-unsafe-and-ineffective.qmd` - Historical context

### Research Coverage Gap

**how-much-we-know-numbers.png** (67 KB) - ALREADY IN ASSETS

- **Source:** [Only 0.000000002% of Potential Treatments Have Been Studied](https://thinkbynumbers.org/health/only-0-000000002-of-potential-treatments-have-been-studied/)
- **Description:** Infographic showing vast gap between studied and potential treatments (0.000000002%)
- **Use in chapters:**
  - `brain/book/problem/nih-spent-1-trillion-eradicating-0-diseases.qmd` - PRIMARY USE
  - `brain/book/solution/dfda.qmd`

**rare-diseases.jpg** (66 KB) - ALREADY IN ASSETS

- **Source:** [Only 0.000000002% of Potential Treatments Have Been Studied](https://thinkbynumbers.org/health/only-0-000000002-of-potential-treatments-have-been-studied/)
- **Description:** Chart showing prevalence and distribution of over 7,000 known rare diseases
- **Use in chapters:**
  - `brain/book/problem/nih-spent-1-trillion-eradicating-0-diseases.qmd`
  - `brain/book/problem/the-daily-massacre.qmd`

**number-of-molecules-with-drug-like-properties.png** (124 KB) - ALREADY IN ASSETS

- **Source:** [Only 0.000000002% of Potential Treatments Have Been Studied](https://thinkbynumbers.org/health/only-0-000000002-of-potential-treatments-have-been-studied/)
- **Description:** Shows 166 billion untested compounds with drug-like properties
- **Use in chapters:**
  - `brain/book/problem/nih-spent-1-trillion-eradicating-0-diseases.qmd`
  - `brain/book/solution/dfda.qmd`

## Risk Perception and Spending Priorities

**death-and-dollars-terrorism-comparison.jpg** (102 KB)

- **Source:** [Anti-Terrorism Spending 50,000 Times More Than on Any Other Threat](https://thinkbynumbers.org/government-spending/false-sense-of-insecurity/)
- **Description:** Infographic comparing deaths from terrorism (~300/year) vs. lightning strikes (~1,000/year), heart disease (652,486/year), cancer (553,888/year) alongside prevention spending. Shows terrorism gets $150B while causing far fewer deaths.
- **Use in chapters:**
  - `brain/book/problem/the-119-trillion-death-toilet.qmd` - PERFECT for spending priorities
  - `brain/book/problem/cost-of-war.qmd` - Shows military spending irrationality
  - `brain/book/problem/cost-of-disease.qmd` - Spending comparison
  - `brain/book/economics/best-idea-in-the-world.qmd` - ROI comparison

**deaths-vs-funding-bar-chart.jpg** (64 KB)

- **Source:** [Anti-Terrorism Spending 50,000 Times More Than on Any Other Threat](https://thinkbynumbers.org/government-spending/false-sense-of-insecurity/)
- **Description:** Bar graph version showing deaths from various causes vs. government prevention funding. Terrorism: $500M per victim; Strokes: $2,000 per victim (250,000x disparity)
- **Use in chapters:**
  - `brain/book/problem/the-119-trillion-death-toilet.qmd` - PRIMARY USE
  - `brain/book/appendix/humanity-budget-overview.qmd`
  - `brain/book/solution/1-percent-treaty.qmd` - Shows where money should go

**social-amplification-of-risks.jpg** (35 KB)

- **Source:** [Anti-Terrorism Spending 50,000 Times More Than on Any Other Threat](https://thinkbynumbers.org/government-spending/false-sense-of-insecurity/)
- **Description:** Flowchart illustrating how society amplifies perception of involuntary risks (terrorism, nuclear) versus voluntary risks (smoking, driving), explaining irrational spending patterns
- **Use in chapters:**
  - `brain/book/problem/unrepresentative-democracy.qmd` - Why bad policy happens
  - `brain/book/problem/regulatory-capture.qmd` - Media/fear manipulation
  - `brain/book/appendix/faq.qmd` - Addresses fear objections

**cancer-vs-terrorism-deaths-spending.jpg** (127 KB)

- **Source:** [Anti-Terrorism Spending 50,000 Times More Than on Any Other Threat](https://thinkbynumbers.org/government-spending/false-sense-of-insecurity/)
- **Description:** Graph comparing cancer deaths (553,888/year) and spending vs. terrorism deaths (~300/year) and spending. Shows massive spending disparity despite cancer killing 1,800x more people.
- **Use in chapters:**
  - `brain/book/problem/the-119-trillion-death-toilet.qmd` - PRIMARY USE
  - `brain/book/problem/the-daily-massacre.qmd` - Scale of disease deaths
  - `brain/book/solution/1-percent-treaty.qmd` - Justification for reallocation

## Military Spending Images

**2018-military-expenditures-by-country.png** (46 KB)

- **Source:** [How much does the US spend on the military compared to the rest of the world?](https://thinkbynumbers.org/government-spending/how-much-does-the-us-spend-on-the-military-compared-to-the-rest-of-the-world/)
- **Description:** Pie chart showing US = 37% of global military spending while being 4.4% of world population
- **Use in chapters:**
  - `brain/book/problem/cost-of-war.qmd` - PRIMARY USE
  - `brain/book/solution/1-percent-treaty.qmd`
  - `brain/book/appendix/peace-dividend-analysis.qmd`

**world-without-war.png** (1.7 MB)

- **Source:** [War Costs the Average Person $74,259 Over Their Lifetime](https://thinkbynumbers.org/military/war/the-economic-case-for-peace-a-comprehensive-financial-analysis/)
- **Description:** Hero image representing peace dividend concept
- **Use in chapters:**
  - `brain/book/problem/cost-of-war.qmd` - Hero/header image
  - `brain/book/solution/1-percent-treaty.qmd`

**nuclear-bombs.jpg** (62 KB)

- **Source:** [We Have Enough Nuclear Bombs to Kill EVERYONE 130 Times](https://thinkbynumbers.org/military/we-have-enough-nuclear-bombs-to-kill-everyone-on-the-planet-2-6-times/)
- **Description:** Nuclear weapons visual for global stockpile discussion
- **Use in chapters:**
  - `brain/book/appendix/nuclear-weapon-cost-and-casualties.qmd` - PRIMARY USE
  - `brain/book/problem/cost-of-war.qmd`

## Democracy and Governance Images

**voter-support-vs-law-passage.png** (211 KB)

- **Source:** [Voter Support for a Bill Has Near Zero Influence on Whether It Will Become Law](https://thinkbynumbers.org/democracy/voter-support-for-a-bill-has-near-zero-influence-on-whether-it-will-become-law/)
- **Description:** Graph showing flat ~30% passage rate regardless of public support level (0-100%)
- **Use in chapters:**
  - `brain/book/problem/unrepresentative-democracy.qmd` - CRITICAL PRIMARY USE
  - `brain/book/solution/wishocracy.qmd` - Shows problem Wishocracy solves

**expected-vs-actual-democracy.png** (104 KB)

- **Source:** [Voter Support for a Bill Has Near Zero Influence on Whether It Will Become Law](https://thinkbynumbers.org/democracy/voter-support-for-a-bill-has-near-zero-influence-on-whether-it-will-become-law/)
- **Description:** Comparative visualization: expected (higher support = higher passage) vs. actual (flat line)
- **Use in chapters:**
  - `brain/book/problem/unrepresentative-democracy.qmd` - POWERFUL CONTRAST
  - `brain/book/solution/wishocracy.qmd`

**change-the-world-35-percent.webp** (214 KB)

- **Source:** [It Takes 3.5% of the Population to Change the World](https://thinkbynumbers.org/democracy/it-takes-3-5-of-the-population-to-change-the-world/)
- **Description:** Hero image about social movements engaging just 3.5% of population rarely failing
- **Use in chapters:**
  - `brain/book/strategy/global-referendum.qmd` - PRIMARY USE
  - `brain/book/strategy/grassroots-mobilization.qmd`
  - `brain/book/call-to-action/three-actions.qmd`

## Image Files Already in Assets (from previous downloads)

These images from thinkbynumbers.org were already in your assets folder:

- `cost-to-develop-a-new-drug.png` - Drug development cost escalation
- `new-treatments-per-year-2.png` - 70% drop in treatments after 1962
- `us-swiss-life-expectancy-5.png` - US vs Switzerland comparison
- `us-swiss-life-expectancy-drug-approvals.png` - With drug approval overlay
- `how-much-we-know-numbers.png` - 0.000000002% treatments studied
- `rare-diseases.jpg` - 7,000+ rare diseases chart
- `number-of-molecules-with-drug-like-properties.png` - 166B untested compounds
- `diminishing-returns.png` - Linear vs exponential decay
- `thalidomide.jpg` - Historical FDA catalyst
- `bill-public-support-vs-chance-of-adoption-true-democracy.png` - What should happen
- `bill-public-support-vs-chance-of-adoption-what-actually-happens.png` - What actually happens

## Quick Reference: Images by Chapter

### brain/book/problem/the-119-trillion-death-toilet.qmd

- **death-and-dollars-terrorism-comparison.jpg** ⭐⭐ (PERFECT - shows spending irrationality)
- **deaths-vs-funding-bar-chart.jpg** ⭐⭐ (PRIMARY USE)
- **cancer-vs-terrorism-deaths-spending.jpg** ⭐⭐ (PRIMARY USE)

### brain/book/problem/the-daily-massacre.qmd

- cancer-vs-terrorism-deaths-spending.jpg
- rare-diseases.jpg

### brain/book/problem/fda-is-unsafe-and-ineffective.qmd

- life-span-explosion.png
- events-leading-to-health-explosion.png
- **new-treatments-per-year-2.png** ⭐ (70% drop)
- **lifespan-increase-before-after-1962.png** ⭐ (critical)
- us-swiss-life-expectancy-5.png
- us-swiss-life-expectancy-drug-approvals.png
- cost-to-develop-a-new-drug.png
- **drug-cost-vs-lifespan.png** ⭐ (powerful)
- diminishing-returns.png
- thalidomide.jpg

### brain/book/problem/nih-spent-1-trillion-eradicating-0-diseases.qmd

- **how-much-we-know-numbers.png** ⭐ (0.000000002%)
- rare-diseases.jpg
- number-of-molecules-with-drug-like-properties.png
- cost-to-develop-a-new-drug.png

### brain/book/problem/cost-of-war.qmd

- **2018-military-expenditures-by-country.png** ⭐ (37% US spending)
- **world-without-war.png** (hero image)
- **death-and-dollars-terrorism-comparison.jpg** ⭐ (military spending irrationality)
- nuclear-bombs.jpg

### brain/book/problem/cost-of-disease.qmd

- death-and-dollars-terrorism-comparison.jpg
- cancer-vs-terrorism-deaths-spending.jpg

### brain/book/problem/unrepresentative-democracy.qmd

- **voter-support-vs-law-passage.png** ⭐⭐ (CRITICAL)
- **expected-vs-actual-democracy.png** ⭐⭐ (CRITICAL)
- social-amplification-of-risks.jpg (why bad policy happens)

### brain/book/problem/regulatory-capture.qmd

- social-amplification-of-risks.jpg (media/fear manipulation)

### brain/book/solution/1-percent-treaty.qmd

- 2018-military-expenditures-by-country.png
- deaths-vs-funding-bar-chart.jpg (shows where money should go)
- cancer-vs-terrorism-deaths-spending.jpg (reallocation justification)

### brain/book/strategy/global-referendum.qmd

- **change-the-world-35-percent.webp** ⭐ (3.5% rule)

### brain/book/appendix/nuclear-weapon-cost-and-casualties.qmd

- **nuclear-bombs.jpg** (primary use)

## Citation Information

All images sourced from ThinkByNumbers.org. When using in the book, consider adding attribution:

```
Source: ThinkByNumbers.org (Mike P. Sinn)
```

Since these are from your own site, you have full rights to use them in this book project.

## Next Steps

1. Review each chapter and insert relevant images using:

   ```markdown
   ![Caption text](../../../assets/image-name.png)
   ```

2. Verify image quality in rendered output (especially the smaller file sizes like life-span-explosion.png at 14KB)

3. Consider creating higher-resolution versions of key charts if needed for print

4. Add citations/attribution where appropriate

5. Test all images render correctly when building the book with Quarto
