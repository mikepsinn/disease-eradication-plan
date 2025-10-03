# Design Guide

This guide defines the visual design standards for all charts, diagrams, and visualizations in the Decentralized Institutes of Health project.

## Quick Reference

- **Writing Style:** See [STYLE_GUIDE.md](STYLE_GUIDE.md) for tone, voice, and writing conventions
- **Content Guidelines:** See [CONTRIBUTING.md](CONTRIBUTING.md) for overall contribution workflow
- **Technical Implementation:** See [brain/charts/_chart_style.py](brain/charts/_chart_style.py) for all code constants and functions

## Design Philosophy

**Minimalism Above All**

Charts should be as simple and powerful as possible. Every element must earn its place.

- Strip away everything that doesn't directly convey data
- Use color only when it adds meaning (problem vs solution)
- Default to black bars on white backgrounds
- Make numbers impossible to miss
- Remove decorative elements, gradients, shadows, 3D effects

**Visual Inspiration:**

- **Charts:** Edward Tufte's minimalism - maximize data-ink ratio
- **Images/Graphics:** 1950s atomic age propaganda posters - bold, stark, urgent

## Chart Library

All reusable charts are located in [brain/charts/](brain/charts/). See that directory for the complete list of available visualizations.

## Usage

Include charts in any `.qmd` file using:

```markdown
{{< include brain/charts/annual-deaths.qmd >}}
```

## Chart Creation Guidelines

### File Naming

Name charts starting with the leftmost/biggest column: `[primary-topic]-[secondary-topics]-[chart-type].qmd`

**Examples:**
- ✅ `war-vs-curing-diseases-column-chart.qmd`
- ✅ `disease-war-curing-costs-column-chart.qmd`
- ❌ `chart1.qmd` (not descriptive)

### Labels - Plain Language Only

**The "mom test":** Would your mom understand this label at a glance?

- ✅ "Curing Diseases" (not "Medical R&D")
- ✅ "Cost of Disease" (not "Disease Burden")
- ✅ "War's Hidden Costs" (not "Indirect Costs")

### Technical Checklist

1. Import from [_chart_style.py](_chart_style.py): `setup_chart_style()`, color constants, helper functions
2. Save generated images in `brain/charts/` directory (same location as `.qmd` source file)
3. Name output file to match source: `chart-name.qmd` → `chart-name.png`
4. Use linear scales for disparity charts (never logarithmic)
5. Add line breaks to prevent text cutoff: `f'Label:\n${value}T'`
6. Don't use `plt.tight_layout()` (overrides margins)

## Official Color Palette (American Flag Colors)

Simple, powerful colors inspired by 1950s atomic age propaganda:

```python
# The Four Colors - That's It
COLOR_BLACK = '#000000'      # Pure black - bars, primary text, emphasis
COLOR_RED = '#B22234'        # Flag red - danger, war, disease, problems
COLOR_WHITE = '#FFFFFF'      # Pure white - backgrounds, text on dark elements
COLOR_BLUE = '#3C3B6E'       # Flag blue - hope, solutions, cures, action
```

**When to Use Each Color:**

- **BLACK:** All chart bars (default), primary text, headlines, axis labels
- **RED:** Problems/threats (war deaths, disease, waste) - use sparingly for emphasis
- **WHITE:** Chart backgrounds, text overlaid on colored bars
- **BLUE:** Solutions (treaty, cures, VICTORY bonds) - use sparingly for emphasis

**Design Philosophy:**

- **Default to black** - Most charts should use solid black bars
- **Color = meaning** - Only use red/blue when the color adds semantic meaning (problem vs solution)
- **Maximum contrast** - Black on white, white on black, no grays
- **Less is more** - If you're not sure whether to add color, don't

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
- Data bars (solid black or red/blue when meaning is clear)
- Y-axis with scale (only when columns aren't all labeled with amounts)
- Key data values (large, bold, impossible to miss)
- Watermark (required)

**Label Placement (Tufte-approved):**
- Put labels directly ON the data (on bars, lines, points)
- Format: `"$7T\nIndirect War Costs"` (value + description with line break)
- **Large bars:** Label inside (white text on colored bars)
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
- Gridlines (unless absolutely necessary, then use sparingly)
- Chart titles (let the context provide the title)
- X-axis labels (when labels are on the bars themselves)
- Y-axis entirely (when all columns are labeled with amounts)
- Legends (use direct labels instead)
- Backgrounds/fills (pure white only)
- Borders, shadows, gradients, 3D effects
- Decorative elements
- Extra annotations, callouts, arrows (use only if critical)

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
from brain.charts._chart_style import setup_chart_style, add_watermark, clean_spines
from brain.charts._chart_style import COLOR_BLACK, COLOR_RED, COLOR_BLUE, COLOR_WHITE

setup_chart_style()  # Applies consistent styling with automatic margins

# --- 2. Create the Plot ---
x = np.linspace(0, 10, 100)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, y, color=COLOR_BLACK, linewidth=2.5)

# Add labels (no title needed)
ax.set_xlabel('X-Axis Label', fontsize=12, color=COLOR_BLACK)
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
