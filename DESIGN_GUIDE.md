# Design Guide

This guide defines the visual design standards for all charts, diagrams, and visualizations in the Decentralized Institutes of Health project.

## Quick Reference

- **Writing Style:** See [STYLE_GUIDE.md](STYLE_GUIDE.md) for tone, voice, and writing conventions
- **Content Guidelines:** See [CONTRIBUTING.md](CONTRIBUTING.md) for overall contribution workflow
- **Technical Implementation:** See [brain/charts/_chart_style.py](brain/charts/_chart_style.py) for all code constants and functions

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
2. Save to `brain/charts/` directory (stay next to source code)
3. Use linear scales for disparity charts (never logarithmic)
4. Add line breaks to prevent text cutoff: `f'Label:\n${value}T'`
5. Don't use `plt.tight_layout()` (overrides margins)

## Official Color Palette (WWII Propaganda Style)

Bold red and blue inspired by WWII propaganda posters:

```python
# Primary Colors
COLOR_DARK = '#1a1a1a'       # Almost black - use for primary text and emphasis
COLOR_MID = '#4a4a4a'        # Charcoal - use for secondary elements
COLOR_LIGHT = '#e0e0e0'      # Light gray - use for backgrounds and subtle elements
COLOR_RED = '#c1272d'        # Bold propaganda red - danger, urgency, problems (war, disease, waste)
COLOR_BLUE = '#0051a5'       # Bold propaganda blue - hope, solutions, action (treaty, cures, bonds)
COLOR_BG = '#f8f8f8'         # Off-white - use for chart backgrounds
COLOR_WHITE = '#ffffff'      # Pure white - use for high contrast elements
```

**When to Use Each Color:**

- **COLOR_RED:** Bad things - war deaths, disease deaths, wasted spending, problems
- **COLOR_BLUE:** Good things - treaty solution, cures, VICTORY bonds, hope
- **COLOR_DARK:** Primary text, headlines, key numbers
- **COLOR_MID:** Secondary text, axis labels, annotations
- **COLOR_LIGHT:** Subtle gridlines, dividers, less important elements
- **COLOR_BG:** Chart backgrounds, slide backgrounds
- **COLOR_WHITE:** Text on dark backgrounds, high contrast needs

## Typography Guidelines

For bold, impactful messaging inspired by WWII propaganda posters:

**Recommended Font Hierarchy:**

- **Display/Headlines:** Cooper Black (bold, rounded, commanding presence)
- **Body Text:** Impact or Arial Black (strong, authoritative)
- **Fallbacks:** Helvetica Bold, Arial Bold

**Python Implementation:**
```python
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Cooper Black', 'Impact', 'Arial Black', 'Helvetica']
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
- **Color:** Black (`COLOR_DARK = #1a1a1a`)
- **Position:** Bottom-right with 3% padding from edges
- **Opacity:** 100% (fully opaque)

## Implementation Example

To ensure consistency, use the centralized style module at `_chart_style.py`:

```python
import matplotlib.pyplot as plt
import numpy as np

# --- 1. Import centralized style ---
from brain.charts._chart_style import setup_chart_style, add_watermark, clean_spines
from brain.charts._chart_style import COLOR_DARK, COLOR_MID, COLOR_BLUE, COLOR_LIGHT

setup_chart_style()  # Applies consistent styling with automatic margins

# --- 2. Create the Plot ---
x = np.linspace(0, 10, 100)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, y, color=COLOR_BLUE, linewidth=2.5)

# Add titles and labels
ax.set_title('Example Chart', fontsize=16, weight='bold', color=COLOR_DARK)
ax.set_xlabel('X-Axis Label', fontsize=12, color=COLOR_MID)
ax.set_ylabel('Y-Axis Label', fontsize=12, color=COLOR_MID)

# --- 3. Add the Watermark ---
add_watermark(fig)  # Black, bold, 11pt, positioned with padding

# Remove unnecessary spines for a cleaner look
clean_spines(ax)  # Removes top and right spines by default
ax.spines['left'].set_color(COLOR_LIGHT)
ax.spines['bottom'].set_color(COLOR_LIGHT)

# DON'T use plt.tight_layout() - overrides margins!
plt.show()
```

**Important Notes:**

- **DO NOT use plt.tight_layout()** - it overrides margin settings and makes charts touch edges
- Use `bbox_inches=None` when saving (not `bbox_inches='tight'`)
- Margins are set globally by `setup_chart_style()` to ensure the watermark never overlaps chart content
