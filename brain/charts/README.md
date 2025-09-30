# Reusable Chart Modules

This directory contains modular, reusable chart visualizations that can be included in both the presentation and book chapters.

## Available Charts

### Core Data Visualizations

1. **[annual-deaths.qmd](annual-deaths.qmd)** - Pie chart showing 69M annual deaths (55M disease, 14M war)
2. **[budget-waste.qmd](budget-waste.qmd)** - Bar chart comparing $119T spending on problems vs $68B on solutions
3. **[treaty-impact.qmd](treaty-impact.qmd)** - Pie chart showing 1% treaty budget split (99% defense, 1% cures)
4. **[treaty-impact-metrics.qmd](treaty-impact-metrics.qmd)** - Bar chart showing what $27B buys (54K trials, 27M patients, 180K lives saved)

### Solution Components

5. **[dfda-comparison.qmd](dfda-comparison.qmd)** - Side-by-side comparison: dFDA vs FDA (82X more efficient)
6. **[victory-bonds-returns.qmd](victory-bonds-returns.qmd)** - Horizontal bar chart comparing investment returns (40% VICTORY Bonds)
7. **[money-flow-diagram.qmd](money-flow-diagram.qmd)** - Flow diagram showing how $27B moves from treaty to impact
8. **[coalition-wheel.qmd](coalition-wheel.qmd)** - Polar chart showing all stakeholders profit

### Evidence & Futures

9. **[oxford-recovery-proof.qmd](oxford-recovery-proof.qmd)** - Bar chart showing Oxford RECOVERY trial metrics
10. **[futures-comparison.qmd](futures-comparison.qmd)** - Side-by-side comparison: Gollumland vs Wishonia

## Usage

Include charts in any `.qmd` file using:

```markdown
{{< include brain/charts/annual-deaths.qmd >}}
```

## Design System

All charts follow the official style guide defined in:
- **Color Palette:** [CONTRIBUTING.md](../../CONTRIBUTING.md#official-color-palette-palette-c---modern-neutral)
- **Typography:** EB Garamond (serif) for elegant, prestigious aesthetic
- **Style Module:** [_chart_style.py](_chart_style.py) - Centralized styling functions

### Color Palette (Palette C - Modern Neutral)

```python
COLOR_DARK = '#1a1a1a'       # Primary text and emphasis
COLOR_MID = '#4a4a4a'        # Secondary elements
COLOR_LIGHT = '#e0e0e0'      # Subtle backgrounds
COLOR_ACCENT = '#2c5f7d'     # Key data points (use sparingly)
COLOR_BG = '#f8f8f8'         # Chart backgrounds
COLOR_WHITE = '#ffffff'      # High contrast
```

### Typography

- **Display/Headlines:** EB Garamond, Libre Baskerville (classic serif)
- **Body Text:** Georgia, Garamond
- **Data/Numbers:** Clear, bold rendering in serif fonts

## Chart Outputs

All charts are automatically saved to `assets/charts/` when rendered:

- `annual-deaths.png`
- `budget-waste.png`
- `treaty-impact.png`
- `treaty-impact-metrics.png`
- `dfda-comparison.png`
- `victory-bonds-returns.png`
- `money-flow-diagram.png`
- `coalition-wheel.png`
- `oxford-recovery-proof.png`
- `futures-comparison.png`

## Chart Specifications

### Margins and Padding

All charts automatically include proper margins to avoid watermark overlap and maintain visual balance:

- **Bottom margin:** 12% (for watermark clearance)
- **Top margin:** 8%
- **Left margin:** 10%
- **Right margin:** 5%

These are set automatically by `setup_chart_style()`.

### Watermark

All charts include the **WarOnDisease.org** watermark:

- **Font size:** 11pt (bold)
- **Color:** Black (#1a1a1a)
- **Position:** Bottom-right with 3% padding from edges
- **Opacity:** 100% (fully opaque)
- **Usage:** `add_watermark(fig)`

## Contributing

When creating new charts:

1. Use the centralized `_chart_style.py` module
2. Follow the official color palette (blacks, grays, single teal accent)
3. Add meaningful captions and insights
4. Save to `assets/charts/` with descriptive names
5. Include branding watermark: `add_watermark(fig)`
6. Use `clean_spines(ax)` for minimal design
7. **DO NOT use plt.tight_layout()** - it overrides the automatic margins
8. Ensure adequate padding - margins are automatic but verify no overlap
9. **Use LINEAR scales for disparity charts** - Never use logarithmic scales when showing budget disparities. The whole point is to make the absurdity VISIBLE. Tiny solution bars next to massive problem bars = effective communication.
