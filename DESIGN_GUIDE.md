# Design Guide

This guide defines the visual design standards for all charts, diagrams, and visualizations in the Decentralized Institutes of Health project.

## Quick Reference

- **Writing Style:** See [STYLE_GUIDE.md](STYLE_GUIDE.md) for tone, voice, and writing conventions
- **Content Guidelines:** See [CONTRIBUTING.md](CONTRIBUTING.md) for overall contribution workflow
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
3. **Save generated images** in the same `brain/figures/` directory
4. **Include proper labels** for cross-referencing

### File Naming

**Format:** `[topic]-[comparison/metric]-[visualization]-chart.qmd`

Always end filenames with `-chart` (or `-diagram`, `-counter` for non-charts).

**Examples:**
- ✅ `military-spending-vs-medical-research-bar-chart.qmd`
- ✅ `disease-deaths-by-type-2024-pie-chart.qmd`
- ✅ `money-flow-diagram.qmd` (diagrams don't need `-chart`)
- ✅ `death-counter-realtime.qmd` (counters don't need `-chart`)
- ❌ `military-spending-bar.qmd` (missing `-chart`)
- ❌ `data.qmd`, `figure1.qmd`, `comparison.qmd`

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
3. Name output file to match source: `chart-name.qmd` → `chart-name.png`
4. Use linear scales for disparity charts (never logarithmic)
5. Add line breaks to prevent text cutoff: `f'Label:\n${value}T'`
6. Don't use `plt.tight_layout()` (overrides margins)

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

For bold, impactful messaging inspired by atomic age propaganda posters:

**Recommended Font Hierarchy:**

- **Display/Headlines:** Impact, Arial Black (strong, commanding)
- **Body Text:** Helvetica, Arial (clean, readable)
- **Fallbacks:** System sans-serif fonts

**Python Implementation:**
```python
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Impact', 'Arial Black', 'Helvetica', 'Arial']
plt.rcParams['font.size'] = 12
plt.rcParams['font.weight'] = 'bold'
```

**Font Size Guidelines:**

- Chart titles: 16-18pt (bold)
- Axis labels: 11-12pt
- Data labels: 10-11pt
- Watermark: 8-9pt
- Presentation headlines: 48-72pt
- Presentation body: 24-36pt

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

## Minimalist Chart Design Rules

**What to Include:**
- Data bars (white fill with black outline, use solid black for emphasis)
- Y-axis with scale (ONLY when columns aren't all labeled with amounts)
- Key data values (large, bold, impossible to miss)
- Watermark (required)

**Chart Reusability Rule:**
- **NO titles in chart code** - Context provides the title (chapter heading, figure caption, etc.)
- **NO explanatory text in charts** - The surrounding document explains the chart
- **Charts must work in ANY context** - Book, website, presentation, social media
- This allows the same chart to be included with different captions and contexts

**Label Placement (Tufte-approved):**
- Put labels directly ON the data (on bars, lines, points)
- Format: `"$7T\nIndirect War Costs"` (value + description with line break)
- **Large bars (white fill):** Label inside (black text on white bars) OR label above
- **Large bars (solid black fill):** Label inside (white text on black bars)
- **Small bars:** Label above (black text, positioned just above the bar)
- Remove redundant x-axis labels when data is self-labeled
- Remove y-axis entirely on column charts when all columns show their amounts
- This eliminates matching numbers to separate axis labels

**Typography Size (Neobrutalist approach):**
- **Make text as large as reasonably possible** - Bold, commanding, impossible to miss
- Bar labels: 44-72pt (depending on available space)
- Numbers should dominate the visual hierarchy
- If text feels too small, it probably is - go bigger
- Think propaganda posters, not academic papers

**Text Width and Clipping:**
- **Test your text fits** - Long text on bars gets clipped at edges
- Use abbreviations when needed: "55M Deaths/Year" not "55 Million Deaths/Year"
- Multi-line text is better than long single lines
- If text is wider than the bar, make it smaller or split it up
- Check the generated PNG - if text is cut off, shorten or reduce font size

**What to Remove:**
- **Chart titles** - ALWAYS remove (context provides the title via captions/headings)
- **Gridlines** - Remove unless absolutely necessary for readability
- **Y-axis entirely** - Remove on column charts when all columns show numeric labels
- **X-axis labels** - Remove when labels are on the bars themselves
- **Legends** - Remove (use direct labels on data instead)
- **Explanatory text** - Remove (the surrounding document explains the chart)
- **Backgrounds/fills** - Remove (pure white only)
- **Borders, shadows, gradients, 3D effects** - Remove all decorative effects
- **Extra annotations, callouts, arrows** - Remove unless critical for understanding

**The Tufte Test:**
Ask: "If I remove this element, does the chart lose essential information?" If no, remove it.

## 1950s Atomic Age Aesthetic (for Images/Graphics)

When creating or sourcing images:

- **Bold, stark compositions** - High contrast, dramatic
- **Limited color palette** - Red, white, blue, black only
- **Strong typography** - Impact fonts, all caps for headlines
- **Urgent messaging** - "Act Now", "The Future Is At Stake"
- **Retro-futurism** - Atoms, rockets, bold geometric shapes
- **Propaganda poster style** - Direct, commanding, no subtlety

**Think:**
- "Duck and Cover" civil defense posters
- 1950s "Atoms for Peace" campaign
- WWII "We Can Do It" propaganda
- Cold War public information graphics

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

# Add labels (no title needed)
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
