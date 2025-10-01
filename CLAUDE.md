# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Quarto-based book project: "The Complete Idiot's Guide to Ending War and Disease" - a guide to getting nations to sign the 1% Treaty redirecting military spending to medical research. The project uses a hybrid Node.js/Python setup with TypeScript utility scripts for content management.

**Key Navigation:**

- **`todo.md`**: Master task list and current priorities for book completion
- **`OUTLINE.md`**: Complete book outline (comprehensive writing checklist)
- **`index.qmd`**: Book introduction and overview (landing page)
- **`_quarto.yml`**: Chapter ordering and build configuration

**Current Focus**: Writing and enhancing book chapters with data visualizations, charts, and interactive elements. Track progress in `todo.md`.

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

**See `CONTRIBUTING.md` for complete writing guidelines, style requirements, and content standards.**

### Core Message & Focus

- **Primary Focus:** The unnecessary suffering and death from war (14M deaths/year) and disease (55M deaths/year). Every year we lose 69 million lives that could be saved.
- **The Problem:** We spend $119 trillion annually on war and disease while investing just 0.06% of that on finding cures. Children die of rare diseases while we build nuclear submarines.
- **The Solution:** Redirect just 1% of military spending to medical research through systems that are 80X more efficient than current approaches.
- **The Mission:** Save millions of lives by making curing people more profitable than killing them

### Writing Tone & Style

- **Dark Humor Meets Practical Hope:** Think Kurt Vonnegut explaining economics to drunk people at a funeral
- **The 4 Core Checks:** Clarity (would mom understand?), Credibility (can I stake my reputation on this?), Concision (can I cut words?), Directness (does it sound like Vonnegut?)
- **Voice Test:** "Would this make someone laugh AND think?"
- **Avoid:** Corporate buzzwords, academic pomposity, euphemisms for death

### Framing Central Planning

- **Use History Wisely:** Central planning has killed millions (Soviet famines, Great Leap Forward). Present as historical evidence that committee-based systems fail in complex domains
- **Walk Readers Logically:** From "committees failed at agriculture" to "committees are failing at medical research"
- **Keep It Bipartisan:** Both Democrats and Republicans lose loved ones to disease. Both parties have created successful market-based programs (Medicare Part D, etc.)
- **Not Ideological:** This is about what saves lives, not winning political debates

### Key Writing Guidelines

- Follow the "Write first, research later" approach from `todo.md`
- Use placeholder citations during writing phase: `[TODO: source - claim]`
- Lead with human stories and suffering, not economic theory
- Present decentralization as practical, not ideological

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

**Current Priority: Book Writing & Enhancement (see `todo.md` for detailed task tracking)**

1. **Content Creation**: Write chapters in `brain/book/` following structure in `_quarto.yml`
2. **Data Visualization**: Add Python/Jupyter charts and interactive elements using Quarto
3. **Sourcing**: Add proper citations after writing phase is complete
4. **Validation**: Run `npm run validate:frontmatter --fix` and `npm run lint:md:fix`
5. **Preview**: Use `npm run quarto:preview` for live development with charts/diagrams

## Python/Jupyter Integration for Data Visualization

- **Environment**: Use `dih-project-kernel` Jupyter kernel (configured in `_quarto.yml`)
- **Charts & Diagrams**: All generated figures saved to `assets/charts/` with doc-title prefixes
- **Available Libraries**: pandas, numpy, matplotlib, seaborn, plotly (see `requirements.txt`)
- **Interactive Elements**: Quarto supports interactive plotly charts, widgets, and calculations
- **Code Execution**: Use Python code blocks in `.qmd` files for dynamic content generation

## Testing

Currently no automated tests. Quality assurance relies on:

- Markdown linting
- Frontmatter validation
- Manual content review
- Build success verification