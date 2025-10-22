# Design Guide

## Quick Reference

- **Writing Style:** See [STYLE_GUIDE.md](STYLE_GUIDE.md) for tone, voice, and writing conventions
- **Content Guidelines:** See [CONTRIBUTING.md](../CONTRIBUTING.md) for overall contribution workflow
- **Technical Implementation:** See [brain/figures/_chart_style.py](brain/figures/_chart_style.py) for all code constants and functions

## Design Philosophy

**Minimalism Above All**

Charts should be as simple and powerful as possible. Every element must earn its place.

- Strip away everything that doesn't directly convey data
- Use black and white only (no color)
- Use patterns to distinguish categories when needed
- Make numbers impossible to miss
- Remove decorative elements, gradients, shadows, 3D effects

**Visual Inspiration:**

- **Charts:** Edward Tufte's minimalism - maximize data-ink ratio
- **Images/Graphics:** 1950s atomic age propaganda posters - bold, stark, urgent

## Chart Library

All reusable charts are located in [brain/figures/](brain/figures/) as **Quarto Markdown (.qmd) files**. These files contain executable Python code that generates visualizations. See that directory for the complete list of available visualizations.

## Chart File Format

**IMPORTANT:** Charts must be created as `.qmd` files, NOT Python scripts. This ensures they can be:

- Included directly in book chapters and presentations
- Rendered independently for testing
- Reused across multiple documents
- Version controlled with their output

## Usage

Include charts in any `.qmd` file using Quarto's include directive:

```markdown
{{< include brain/figures/disease-vs-war-annual-deaths-pie-chart.qmd >}}
```

## Chart Creation Guidelines

### File Format Requirements

1. **Must be `.qmd` files** with Python code blocks
2. **Use descriptive filenames** following the naming convention below
3. **MUST generate PNG files** - Every chart must save a PNG output
4. **Save generated images** in the same `brain/figures/` directory
5. **Include proper labels** for cross-referencing

### PNG Generation is MANDATORY

**Every QMD chart file MUST generate a corresponding PNG file.** This is required for:

- Presentations and slide decks
- Shared on social media (Twitter, LinkedIn, etc.)
- Embedded in external reports and documents
- Backup visualization if Quarto rendering fails
- Version control tracking of visual output changes
- Quick preview without running code

**Implementation:**

```python
# This code MUST be at the end of every chart file:

output_dir = project_root / 'brain' / 'figures'
output_dir.mkdir(parents=True, exist_ok=True)
plt.savefig(output_dir / 'same-name-as-qmd-file.png',
            dpi=200, bbox_inches=None, facecolor=COLOR_WHITE)
plt.show()  # For Quarto display
```

### File Naming

**Format:** `[topic]-[comparison/metric]-[type]-chart.qmd`

**Rules:**

- Always end with `[type]-chart` for charts (e.g., `column-chart`, `pie-chart`, `line-chart`)
- **Prefer `column-chart` over `bar-chart`** for better mobile readability
- Use `-diagram`, `-counter` etc. for non-charts
- Don't add redundant context (if "victory-bonds" is clear, don't add "medical-")
- Use hyphens between all words

**Examples:**

- ✅ `military-spending-vs-medical-research-column-chart.qmd`
- ✅ `disease-deaths-by-type-2024-pie-chart.qmd`
- ✅ `victory-bonds-roi-projection-line-chart.qmd` (not `medical-victory-bonds...`)
- ✅ `money-flow-diagram.qmd`
- ✅ `death-counter-realtime.qmd`
- ❌ `military-spending-bar.qmd` (missing `-chart`)
- ❌ `data.qmd`, `figure1.qmd`

### Labels - Plain Language Only

**The "mom test":** Would your mom understand this label at a glance?

- ✅ "Curing Diseases" (not "Medical R&D")
- ✅ "Cost of Disease" (not "Disease Burden")
- ✅ "War's Hidden Costs" (not "Indirect Costs")

### Technical Checklist

1. Import from [_chart_style.py](_chart_style.py): `setup_chart_style()`, color constants, helper functions
2. **Save images using dynamic project root** (works regardless of where quarto runs from):

   ```python
   # At top of file - find project root dynamically
   project_root = Path.cwd()
   if project_root.name != 'decentralized-institutes-of-health':
       while project_root.name != 'decentralized-institutes-of-health' and project_root.parent != project_root:
           project_root = project_root.parent

   # At bottom - save to brain/figures/ using dynamic path
   output_dir = project_root / 'brain' / 'figures'
   output_dir.mkdir(parents=True, exist_ok=True)
   plt.savefig(output_dir / 'chart-name.png', dpi=200, bbox_inches=None, facecolor=COLOR_WHITE)
   ```

3. **MANDATORY: Generate PNG output** - Every chart MUST save a PNG:

   ```python
   plt.savefig(output_dir / 'exact-same-name-as-qmd.png',
               dpi=200, bbox_inches=None, facecolor=COLOR_WHITE)
   ```

4. Name output file to match source: `chart-name.qmd` → `chart-name.png`
5. Use linear scales for disparity charts (avoid logarithmic scales - they hide the dramatic differences we're trying to highlight)
6. Add line breaks to prevent text cutoff: `f'Label:\n${value}T'`
7. Don't use `plt.tight_layout()` (overrides margins)

## Official Color Palette

**Black and white only** for maximum authority, timelessness, and accessibility:

```python
COLOR_BLACK = '#000000'      # Pure black - bars, text, lines
COLOR_WHITE = '#FFFFFF'      # Pure white - backgrounds
```

**Pattern Palette for Multi-Category Charts:**

When you need to distinguish between categories, use fill patterns instead of color:

```python
# Default: White fill with black outline (most elegant)
PATTERN_SOLID = None         # No hatch pattern (white fill)
PATTERN_DIAGONAL = '///'     # Diagonal lines
PATTERN_HORIZONTAL = '---'   # Horizontal lines
PATTERN_CROSS = 'xxx'        # Crosshatch
PATTERN_DOTS = '...'         # Dots/stippling
```

**Bar Fill Guidelines:**

- **Default: White with black outline** - Clean, elegant, maximizes data-ink ratio
- **For emphasis: Solid black fill** - Use sparingly for critical data that needs maximum visual weight
- **Patterns on white** - Use hatching patterns on white fills to distinguish categories

**Design Philosophy:**

- **Default to white fills** - Lighter, more sophisticated, easier to read
- **Solid black for emphasis** - Reserve for the most important data point
- **Patterns = distinction** - Use hatching to differentiate categories
- **Maximum contrast** - Black lines on white fills, no grays, no color
- **Academic authority** - Tufte-approved minimalism conveys seriousness and credibility

## Typography Guidelines

For authoritative, journalistic typography inspired by newspaper editorial pages and typewriter documents:

**Recommended Font Hierarchy:**

- **Display/Headlines:** Georgia, 'Times New Roman', serif (authoritative, editorial)
- **Body Text/Data:** 'Courier New', 'Courier', monospace (typewriter precision)
- **Fallbacks:** System serif and monospace fonts

**Design Inspiration:**

- 1940s-60s newspaper front pages (serious, factual, authoritative)
- Typewriter documents (direct, unvarnished truth)
- Government reports and white papers (credible, institutional)

**Python Implementation:**

```python
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Georgia', 'Times New Roman', 'Liberation Serif']
plt.rcParams['font.monospace'] = ['Courier New', 'Courier', 'Liberation Mono']
plt.rcParams['font.size'] = 11
plt.rcParams['font.weight'] = 'normal'  # Let serif do the heavy lifting
```

**Font Sizing - Adaptive to Chart Density:**

Mobile-first (320-428px). Scale fonts based on element count:

- **Sparse (≤5 elements):** Max sizes | **Dense (>10):** Min sizes to prevent overlap
- **Hierarchy:** Data values (24-44pt) > Title (28-36pt) ≥ Axis labels (20-36pt) > Annotations (11-24pt) > Callouts (11-22pt) > Notes (9-16pt) > Watermark (11pt fixed)

**Anti-overlap:** Start with full descriptive text at smaller sizes. Only shorten if essential. Stagger vertically when crowded (5pt min spacing). Better: 11pt readable text than 28pt overlapping mess.

**Common Mistakes:**

- ❌ 18pt title with 44pt data - title disappears
- ❌ Fonts that look "fine" on desktop but illegible on mobile
- ✅ 36pt+ for everything - instantly readable anywhere

## Chart Margins and Padding

All charts must have adequate padding to avoid overlap with the watermark and maintain visual balance:

- **Bottom margin:** 12% (for watermark clearance)
- **Top margin:** 8%
- **Left margin:** 10%
- **Right margin:** 5%

These margins are automatically set by `setup_chart_style()` but can be adjusted per chart if needed.

## Watermark Specifications

- **Font size:** 11pt (bold)
- **Color:** Black (`COLOR_BLACK = #000000`)
- **Position:** Bottom-right with 3% padding from edges
- **Opacity:** 100% (fully opaque)

## Mobile-First Chart Orientation

**Prefer Column Charts (Vertical) Over Bar Charts (Horizontal):**

Mobile devices are held vertically - column charts use this natural orientation better:

- **Column charts:** Full width for data, natural scrolling if needed
- **Horizontal bar charts:** Cramped, text gets squeezed, hard to read labels

**When to Use Each:**

- **Column charts (default):** Comparisons, rankings, time series - anything under 10 categories with comparable value ranges (within 100× of each other)
- **Horizontal bars:** Use when you have 5+ categories
- **Pie charts:** Only for showing parts of a whole (max 3-4 slices). **Default to white fill with black outline** for slices

## Minimalist Chart Design Rules

**What to Include:**

- **Chart title (MANDATORY)** - Clear, concise, properly sized (28-36pt bold). **Every chart MUST have a title for standalone readability**
- Data bars/columns (white fill with black outline, use solid black for emphasis)
- Y-axis with scale (ONLY when columns aren't all labeled with amounts)
- Key data values (large, bold, impossible to miss)
- Watermark (required)

**Label Placement (Tufte-approved):**

- Put labels directly ON the data (on bars, lines, points)
- Format: `"$7T\nIndirect War Costs"` (value + description with line break)
- **Large bars (white fill):** Label inside (black text on white bars) OR label above
- **Large bars (solid black fill):** Label inside (white text on black bars)
- **Small bars:** Label above (black text, positioned just above the bar)
- Remove redundant x-axis labels when data is self-labeled
- Remove y-axis entirely on column charts when all columns show their amounts
- This eliminates matching numbers to separate axis labels

**White Background Boxes for Labels:**

- **Use white boxes ONLY for labels placed ON bars/columns** - Makes text readable over patterns
- **Do NOT use boxes for labels positioned above/outside bars** - They're already on white background
- Add boxes using: `bbox=dict(boxstyle='round,pad=0.4', facecolor=COLOR_WHITE, edgecolor=COLOR_BLACK, linewidth=1)`
- Essential for text over hatched/patterned areas (e.g., labels on diagonal stripe patterns)
- Keep padding minimal (0.4) to avoid visual clutter

**Typography Approach:**

- **Make text as large as reasonably possible**
- Numbers should dominate the visual hierarchy
- If text feels too small, it probably is - go bigger

**Text Width and Clipping:**

- **Test your text fits** - Long text on bars gets clipped at edges
- Use abbreviations when needed: "55M Deaths/Year" not "55 Million Deaths/Year"
- Multi-line text is better than long single lines
- If text is wider than the bar, make it smaller or split it up
- Check the generated PNG - if text is cut off, shorten or reduce font size

**What to Remove:**

- **Gridlines** - Remove unless absolutely necessary for readability
- **Y-axis entirely** - Remove on column charts when all columns show numeric labels
- **X-axis labels** - Remove when labels are on the bars themselves
- **Legends** - Remove (use direct labels on data instead)
- **Backgrounds/fills** - Remove (pure white only)
- **Borders, shadows, gradients, 3D effects** - Remove all decorative effects
- **Extra annotations, callouts, arrows** - Remove unless critical for understanding

**The Tufte Test:**

Ask: "If I remove this element, does the chart lose essential information?" If no, remove it.

## Newspaper/Typewriter Aesthetic (for Images/Graphics)

When creating or sourcing images:

- **High-contrast compositions** - Stark black and white, newspaper clarity
- **Limited color palette** - Black and white only (newspaper ink)
- **Serif typography** - Georgia, Times New Roman for headlines
- **Monospace for data** - Courier New for numbers and statistics
- **Editorial authority** - Serious, factual, institutional credibility
- **Typewriter precision** - Aligned, structured, document-like

**Design Inspiration:**

- 1940s-60s newspaper front pages (The New York Times, Washington Post editorial style)
- Typewriter documents and government memos
- Pentagon Papers aesthetic (authoritative classified documents)
- Congressional Budget Office reports (serious economic analysis)

## Implementation Example

To ensure consistency, use the centralized style module at `_chart_style.py`:

```python
import matplotlib.pyplot as plt
import numpy as np

# --- 1. Import centralized style ---
from brain.figures._chart_style import setup_chart_style, add_watermark, clean_spines
from brain.figures._chart_style import COLOR_BLACK, COLOR_WHITE, PATTERN_DIAGONAL

setup_chart_style()  # Applies consistent styling with automatic margins

# --- 2. Create the Plot ---
categories = ['Category A', 'Category B', 'Category C']
values = [100, 75, 50]

fig, ax = plt.subplots(figsize=(8, 5))

# Default: white fill with black outline, use patterns to distinguish
bar1 = ax.bar(0, values[0], color=COLOR_WHITE, edgecolor=COLOR_BLACK, linewidth=2, hatch=None)
bar2 = ax.bar(1, values[1], color=COLOR_WHITE, edgecolor=COLOR_BLACK, linewidth=2, hatch=PATTERN_DIAGONAL)
bar3 = ax.bar(2, values[2], color=COLOR_BLACK, edgecolor=COLOR_BLACK, linewidth=2)  # Solid black for emphasis

# Add title and labels
ax.set_title('Chart Title Here', fontsize=16, color=COLOR_BLACK, weight='bold', pad=20)
ax.set_ylabel('Y-Axis Label', fontsize=12, color=COLOR_BLACK)

# --- 3. Add the Watermark ---
add_watermark(fig)  # Black, bold, 11pt, positioned with padding

# Remove unnecessary spines for a cleaner look
clean_spines(ax)  # Removes top and right spines by default

# DON'T use plt.tight_layout() - overrides margins!
plt.show()
```

**Important Notes:**

- **DO NOT use plt.tight_layout()** - it overrides margin settings and makes charts touch edges
- Use `bbox_inches=None` when saving (not `bbox_inches='tight'`)
- Margins are set globally by `setup_chart_style()` to ensure the watermark never overlaps chart content
