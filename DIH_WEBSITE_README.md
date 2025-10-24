---
title: DIH Website
description: Source files and build instructions for the dih.earth website with neobrutalist design and Quarto configuration.
---

# DIH Website

This directory contains the source files for the Decentralized Institutes of Health (DIH) website at [dih.earth](https://dih.earth).

## Structure

- **[dih-index.qmd](dih-index.qmd)** - Main landing page for the DIH website
- **[_dih.yml](_dih.yml)** - Quarto configuration for the DIH website
- **[dih-styles.css](dih-styles.css)** - Neobrutalist CSS styling (black & white, bold, stark)
- **[styles.css](styles.css)** - Original styles for the main book

## Building the Website

### Quick Test (Recommended for Development)

```bash
quarto render dih-index.qmd --to html
```

Open `dih-index.html` in your browser to preview.

### Full Site Build

```bash
quarto render --profile dih
```

Output will be in `_book/dih/`

## Output

The rendered website will be generated in `_book/dih/`.

## Website Features

The DIH website includes:

### Landing Page Features

1. **Hero Banner** - Prominent call-to-action with key messaging
2. **Problem Overview** - Visual grid showing the core issues (deaths, costs, funding gap)
3. **How It Works Tabs** - Interactive explanation of DIH principles
4. **Results Cards** - Highlighting the 80X efficiency, 10X speed, and 100% transparency
5. **Funding Flow Diagram** - Mermaid diagram showing the treaty → treasury → patients flow
6. **dFDA Overview** - Split view for patients vs. researchers
7. **Governance Section** - Explanation of Wishocratic governance
8. **Get Involved CTAs** - Clear action items for different audiences

### Navigation Structure

- **Home** - Landing page (dih-index.qmd)
- **How It Works** (dropdown)
  - About the DIH
  - The dFDA
  - Wishocracy Governance
  - The 1% Treaty
- **Governance** - Detailed governance information
- **Resources** (dropdown)
  - FAQ
  - References
  - Full Book
- **Get Involved** - CTA button
- **GitHub** - Source code link

### Styling

The website uses a **pure neobrutalist design** following the project's GUIDES/DESIGN_GUIDE.md:

- **Pure black (#000) and white (#fff)** - No grays, no gradients, no compromise
- **Bold geometric shapes** - Thick borders (4-8px), offset drop shadows
- **Impact typography** - All caps headers, bold weights, commanding presence
- **Stark minimalism** - Strip away everything that doesn't convey information
- **1950s propaganda poster aesthetic** - Bold, urgent, direct
- **Responsive brutalism** - Mobile-first with aggressive spacing
- **Interactive elements** - Buttons and cards with strong hover states

**Design Philosophy:**

- Black and white ONLY (per GUIDES/DESIGN_GUIDE.md)
- Maximum contrast and readability
- Bold, geometric, no rounded corners
- Typography hierarchy through size and weight
- Generous spacing for impact
- Shadow offsets (not blurred) for depth

## Customization

### Adding New Pages

1. Create a new `.qmd` file in the project root or appropriate subdirectory
2. Add the page to the navbar in `_dih.yml`
3. Ensure all links use relative paths

### Modifying Styles

Edit [styles.css](styles.css) to customize:

- Colors and themes
- Button styles
- Card designs
- Typography
- Responsive breakpoints

### Updating Navigation

Edit the `navbar` section in [_dih.yml](_dih.yml) to:

- Add/remove menu items
- Organize dropdown menus
- Change page order
- Update links

## Content Sources

The website pulls from existing book content in `brain/book/`:

- `brain/book/solution/dih.qmd` - Full DIH chapter
- `brain/book/solution/dfda.qmd` - dFDA chapter
- `brain/book/solution/wishocracy.qmd` - Wishocracy governance
- `brain/book/solution/1-percent-treaty.qmd` - Treaty details
- `brain/book/appendix/governance.qmd` - Governance framework
- `brain/book/appendix/faq.qmd` - Frequently asked questions
- `brain/book/references.qmd` - Citations and sources

## Development Workflow

1. **Edit content** in `.qmd` files
2. **Preview changes** with `quarto preview dih-index.qmd`
3. **Build site** with render command above
4. **Test locally** by opening `_book/dih/dih-index.html` in a browser
5. **Deploy** by pushing to hosting service (GitHub Pages, Netlify, etc.)

## Quarto Features Used

- **Grid layout** for responsive design
- **Panel tabsets** for interactive content organization
- **Mermaid diagrams** for visual flow representation
- **Callout boxes** for warnings and important information
- **Custom CSS classes** for styling
- **Full-page layout** for landing page impact
- **Navbar with dropdowns** for organized navigation
- **Footer** with links and copyright

## Related Files

- Main book configuration: [_quarto.yml](_quarto.yml)
- Main book landing page: [index.qmd](index.qmd)
- Project instructions: [CLAUDE.md](CLAUDE.md)
- Contributing guidelines: [CONTRIBUTING.md](CONTRIBUTING.md)
- Design guide: [DESIGN_GUIDE.md](GUIDES/DESIGN_GUIDE.md)

## Questions or Issues?

See the main project documentation or create an issue in the GitHub repository.
