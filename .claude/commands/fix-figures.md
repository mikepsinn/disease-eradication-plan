---
description: Fix figure and chart compliance issues
---

Review and fix all figures in the current chapter to comply with the design guide.

## Check For

1. **Python chart files** in `brain/figures/`:
   - Must call `setup_chart_style()` from `scripts/lib/chart_style.py`
   - Must call `add_watermark()`
   - Must NOT use `plt.tight_layout()` (discouraged)

2. **Static images**:
   - Should be in `assets/` directory
   - If not, move them and update references

3. **Figure includes**:
   - Use `{{< include brain/figures/filename.qmd >}}` syntax
   - Verify included file exists

## Design Guide Location

Full design guide: `GUIDES/DESIGN_GUIDE.md`

## Actions

1. Find all figure references in the current file
2. Check compliance with design guide
3. Fix issues automatically where possible
4. For complex issues, add clear TODO comments
5. Update `lastFigureCheckHash` in frontmatter when done
