# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Quarto-based book project: "The Complete Idiot's Guide to Ending War and Disease" - a guide to getting nations to sign the 1% Treaty redirecting military spending to medical research. The project uses a hybrid Node.js/Python setup with TypeScript utility scripts for content management.

## Essential Commands

### Book Building and Preview
```bash
# Preview the book (live reload)
npm run quarto:preview

# Build HTML version
npm run build:html

# Build PDF version
npm run build:pdf

# Build both formats
npm run build

# Clean build artifacts
npm run quarto:clean
```

### Content Management
```bash
# Generate project file index
npm run generate:index

# Lint markdown files
npm run lint:md

# Fix markdown linting issues
npm run lint:md:fix

# Validate frontmatter in all markdown files
npm run validate:frontmatter

# Fix frontmatter issues automatically
npm run fix:frontmatter

# Remove empty directories
npm run delete-empty-folders
```

### Python Environment
```bash
# Setup Python virtual environment (if not already created)
python -m venv .venv

# Activate environment (Windows)
.venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

## Project Architecture

### Content Structure
- **`brain/book/`**: Main book chapters organized by topic
  - `problem/`: Chapter 1 - The $119 trillion problem analysis
  - `solution/`: Chapter 2 - The 1% Treaty and DIH/dFDA solutions
  - `economics/`: Chapter 3 - VICTORY Bonds and economic analysis
  - `strategy/`: Chapter 4 - Implementation strategy
  - `proof/`: Chapter 5 - Historical precedents and evidence
  - `futures/`: Chapter 6 - Dystopia vs utopia scenarios
- **`brain/reference/`**: Supporting research and citations
- **`scripts/`**: TypeScript utilities for content management
- **`assets/`**: Images, charts, and static resources

### Build System
- **Quarto**: Primary build system for book rendering (HTML/PDF/presentations)
- **Node.js**: Content management scripts and linting
- **Python**: Data analysis and visualization (Jupyter integration)
- **TypeScript**: Utility scripts with strict type checking

### Key Configuration Files
- **`_quarto.yml`**: Book configuration, chapter order, and output formats
- **`package.json`**: Node.js dependencies and npm scripts
- **`pyproject.toml`**: Python dependencies and project metadata
- **`.markdownlint.json`**: Markdown linting rules (relaxed for creative writing)

## Content Standards

### Writing Style
Follow the guidelines in `CONTRIBUTING.md`:
- **Dark humor with practical hope** (Kurt Vonnegut style)
- **Plain language**: Write for "smart drunk friend" not academics
- **Quantify everything**: All claims need data and citations
- **Public choice theory framing**: Assume rational self-interest, not idealism

### Citation Format
Use placeholder markers during writing:
- `[TODO: source - claim about X]` for facts needing citations
- `[STAT NEEDED: specific number about Y]` for statistics
- `[CITATION: existing reference ID]` for known references

### Frontmatter Requirements
All markdown files need:
```yaml
---
title: "Chapter Title"
description: "Brief description"
published: true
date: "YYYY-MM-DDTHH:mm:ss.000Z"
tags: [relevant, tags]
dateCreated: "YYYY-MM-DDTHH:mm:ss.000Z"
---
```

## Quality Control

### Automated Validation
- **Frontmatter validation**: `npm run validate:frontmatter --fix`
- **Markdown linting**: Custom rules in `.markdownlint.json`
- **Link checking**: Scripts validate internal links and references
- **Image optimization**: Automated resizing and cleanup scripts

### Manual Review
- All content follows the "4 Core Checks": Clarity, Credibility, Concision, Directness
- Voice test: "Would this make someone laugh AND think?"
- Avoid corporate buzzwords and academic pomposity

## Development Workflow

1. **Content Creation**: Write in `brain/book/` following chapter structure
2. **Validation**: Run `npm run validate:frontmatter --fix` and `npm run lint:md:fix`
3. **Preview**: Use `npm run quarto:preview` for live development
4. **Build**: Run `npm run build` before major commits
5. **Index Update**: Run `npm run generate:index` to update file inventory

## Technical Notes

- **Jupyter Integration**: Configured for `dih-project-kernel` Python environment
- **Figure Management**: All generated charts go to `assets/charts/` with prefixed names
- **Cross-platform**: Scripts handle Windows/Unix path differences
- **Caching**: Quarto cache disabled for fresh renders each time
- **Git Integration**: Configured to ignore build artifacts and cache directories

## Testing

Currently no automated tests. Quality assurance relies on:
- Markdown linting
- Frontmatter validation
- Manual content review
- Build success verification