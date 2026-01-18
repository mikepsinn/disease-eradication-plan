# GitHub Copilot Instructions - Disease Eradication Plan

This is a Quarto-based book project: "How to End War and Disease" - a guide to getting nations to sign a 1% treaty, redirecting military spending to the Decentralized Institutes of Health.

## Tech Stack

- **Quarto**: Book rendering and publishing framework
- **Python 3.10+**: Data analysis, calculations, and parameter generation
- **TypeScript/Node.js**: Scripts, automation, and review tools
- **npm/pnpm**: Package management
- **Markdown/QMD**: Content files (Quarto Markdown)

## Key Files and Navigation

- **`todo.md`**: Master task list and current priorities
- **`OUTLINE.md`**: Complete book outline
- **`index.qmd`**: Book introduction and landing page
- **`_quarto-book.yml`**: Book configuration and chapter order
- **`package.json`**: Node.js dependencies and npm scripts
- **`dih_models/parameters.py`**: Single source of truth for all numeric values
- **`_variables.yml`**: Auto-generated variables from parameters.py

## Critical Rules

### Parameter and Variable System

**NEVER hardcode numeric values.** Always use the automated parameter/variable system:

1. Define parameters in `dih_models/parameters.py`
2. Run: `.venv/Scripts/python.exe scripts/generate-everything-parameters-variables-calculations-references.py`
3. Use in QMD files: `{{< var parameter_name >}}`

**Parameter Naming Convention:**
- Format: `[SCOPE]_[METRIC]_[MODIFIERS]_[UNIT_TYPE]`
- Examples: `TREATY_COMPLETE_ROI_EXPECTED_95TH_PERCENTILE`, `DFDA_ROI_RD_ONLY`
- Always include scope prefix (TREATY, DFDA, GLOBAL, etc.)
- Store raw values only (e.g., `519_000_000`, not `519` with unit "millions USD")

**Calculated Parameters:**
- Must use formulas, not hardcoded results
- Set `source_type="calculated"`
- Example: `Parameter(GLOBAL_WAR_COST * TREATY_REDUCTION_PCT, source_type="calculated", formula="...")`

### Cross-Format Linking

**ALWAYS use `.qmd` extensions** for internal links:
- ✅ Correct: `[Link](../path/to/file.qmd#section-id)`
- ❌ Wrong: `[Link](../path/to/file.html)` - breaks PDF/EPUB

### Python Scripts on Windows

**CRITICAL:** Add UTF-8 encoding header to all Python scripts:
```python
#!/usr/bin/env python3
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
```

Avoid Unicode characters in print statements. Use ASCII: `->`, `WARNING:`, `[OK]`.

### TypeScript Execution

- **Always use `tsx`** to run TypeScript files, not `ts-node`
- Example: `npx tsx scripts/review/review.ts`

### LaTeX Math Blocks

**Variables DO NOT work inside `$$` blocks.** Use pre-built LaTeX variables:
- Example: `{{< var peace_dividend_annual_societal_benefit_latex >}}`
- Never manually replace values inside LaTeX equations

## Code Quality Standards

### Before Any Commit

1. Review **every change** for errors
2. Validate all parameter names match `_variables.yml` (lowercase format)
3. Run validation checks with no regressions
4. Only commit when explicitly requested

### Testing and Validation

- Run existing linters, builds, and tests before changes
- Use `npm run lint:md` and `npm run lint:qmd` for markdown linting
- Use `npm run generate:everything` after parameter changes
- Test changes incrementally, not full test suite until complete

### Security

- Never commit secrets or credentials
- Use proper sanitization to prevent XSS vulnerabilities
- Run `codeql_checker` for security scanning
- Fix vulnerabilities in changed code

## Build and Development Commands

### Python Setup
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### Common npm Scripts
```bash
npm run generate:everything       # Generate parameters, variables, calculations
npm run lint:md                   # Lint markdown files
npm run lint:qmd                  # Lint Quarto markdown files
npm run preview:book              # Preview book in browser
npx tsx scripts/path/to/script.ts # Run TypeScript scripts
```

### Quarto Commands
```bash
quarto render                     # Render book to HTML
quarto preview index.qmd          # Live preview
```

## Content Standards

### Writing Style

- Follow CONTRIBUTING.md and GUIDES/STYLE_GUIDE.md
- Write for intelligent non-experts (explain jargon)
- Use "we" for inclusive voice
- Avoid marketing hyperbole, focus on facts

### File Organization

- Content lives in `knowledge/` directory
- All `.qmd` files use Quarto markdown format
- Update `_quarto-book.yml` when adding chapters
- Keep related files together in topic directories

### Documentation Changes

- Update relevant guides when changing structure
- Keep OUTLINE.md in sync with actual chapters
- Documentation changes don't need tests

## Minimal Changes Philosophy

- Make **smallest possible changes** to achieve goals
- Don't fix unrelated bugs or broken tests
- Don't remove/modify working code unless necessary
- Use ecosystem tools (scaffolding, package managers) to reduce mistakes
- Surgical, precise edits only

## Attribution and Licensing

- Project licensed under CC BY-NC 4.0
- Contributors get credit but not automatic co-authorship
- All contributions must respect the open-source license

## Getting Help

- Check `TODO.md` for current priorities
- Read `CONTRIBUTING.md` for full contribution workflow
- See `GUIDES/TECHNICAL_GUIDE.md` for detailed setup
- Review `dih_models/parameters.py` for parameter system details
