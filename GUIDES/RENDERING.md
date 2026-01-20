# Rendering Options

This project supports multiple rendering configurations to publish different views of the content.

## Available Render Configurations

### 1. Full Book (Default)
**Config**: `_quarto-book.yml`
**Output**: `_book/warondisease/`
**Site**: https://manual.WarOnDisease.org

Renders the complete book with all chapters, appendices, and references.

```bash
# Copy config and render
cp _quarto-book.yml _quarto.yml
quarto render

# Or use the script
python scripts/render-book-website.py
```

### 2. Economics Analysis
**Config**: `_quarto-1-pct-treaty-impact.yml`
**Output**: `_site/economics/`
**Site**: https://impact.warondisease.org

Renders just the economic analysis and cost-benefit calculations.

```bash
# Copy config and render
cp _quarto-1-pct-treaty-impact.yml _quarto.yml
quarto render
```

### 3. Wishocracy Paper
**Config**: `_quarto-wishocracy.yml`
**Output**: `_site/wishocracy/`
**Site**: https://paper.wishocracy.org

Renders the Wishocracy academic paper as a standalone document with the paper as the landing page.

```bash
# Use the dedicated script (recommended)
python scripts/render-wishocracy.py

# Manual process (for reference):
# 1. Copy paper to root: cp knowledge/appendix/wishocracy-paper.qmd index.qmd
# 2. Update paths in index.qmd: ../ -> knowledge/
# 3. Copy config: cp _quarto-wishocracy.yml _quarto.yml
# 4. Render: quarto render
```

**How it works**:
- The render script copies `wishocracy-paper.qmd` to `index.qmd` at root (creating the landing page)
- Relative paths are automatically updated (e.g., `../figures/` becomes `knowledge/figures/`)
- Renders to `index.html` (landing page) and `index.pdf` (download)
- Paper is the first thing visitors see at https://paper.wishocracy.org

**Features**:
- Paper serves as the site landing page
- Standalone HTML and PDF versions
- **PDF download button** in navbar pointing to `/index.pdf`
- Automatically copies output to `../wishocracy/public/paper/` for deployment
- Includes all 7 RAPPA diagrams
- Full bibliography with proper references

### 4. Incentive Alignment Bonds Paper
**Config**: `_quarto-iab.yml`
**Output**: `_site/iab/`
**Site**: https://iab.warondisease.org

Renders the IAB academic paper as a standalone document with the paper as the landing page.

```bash
# Use the dedicated script (recommended)
python scripts/render-iab.py

# Manual process (for reference):
# 1. Copy paper to root: cp knowledge/appendix/incentive-alignment-bonds-paper.qmd index.qmd
# 2. Update paths in index.qmd: ../ -> knowledge/
# 3. Copy config: cp _quarto-iab.yml _quarto.yml
# 4. Render: quarto render
```

**How it works**:
- The render script copies `incentive-alignment-bonds-paper.qmd` to `index.qmd` at root (creating the landing page)
- Relative paths are automatically updated (e.g., `../figures/` becomes `knowledge/figures/`)
- Renders to `index.html` (landing page) and `index.pdf` (download)
- Paper is the first thing visitors see at https://iab.warondisease.org

**Features**:
- Paper serves as the site landing page
- Standalone HTML and PDF versions
- **PDF download button** in navbar pointing to `/index.pdf`
- Includes all IAB diagrams (spending scatter, Olsonian quadrants, utility function diagrams, architecture)
- Full bibliography with proper references

## Quick Reference

| What to Render | Command | Output Location |
|---------------|---------|-----------------|
| Full book | `python scripts/render-book-website.py` | `_book/warondisease/` |
| Economics | `cp _quarto-1-pct-treaty-impact.yml _quarto.yml && quarto render` | `_site/economics/` |
| Wishocracy paper | `python scripts/render-wishocracy.py` | `_site/wishocracy/` + `../wishocracy/public/paper/` |
| IAB paper | `python scripts/render-iab.py` | `_site/iab/` |

## Configuration Files

- `_quarto-book.yml` - Full book configuration (85 files)
- `_quarto-1-pct-treaty-impact.yml` - Economics website (71 files)
- `_quarto-wishocracy.yml` - Wishocracy paper only (1 file)
- `_quarto-iab.yml` - IAB paper only (1 file)
- `_quarto.yml` - **Active config** (copy one of the above here before rendering)

## Deployment

After rendering:

1. **Full Book**: Deploy `_book/warondisease/` to WarOnDisease.org via GitHub Pages
2. **Economics**: Deploy `_site/economics/` to impact.warondisease.org
3. **Wishocracy**:
   - Automatically copied to `../wishocracy/public/paper/`
   - Commit and push the wishocracy submodule
   - Deploy wishocracy repo to wishocracy.org
4. **IAB**: Deploy `_site/iab/` to iab.warondisease.org

## Notes

- All configs use the same source files but render different subsets
- Python scripts handle config copying automatically
- The book config is the default in `_quarto.yml`
- All outputs include proper metadata, citations, and styling
