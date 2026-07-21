# Scripts Directory

This directory contains automation scripts for the disease eradication book project.

## Quick Reference

| Task | Command | Description |
|------|---------|-------------|
| **Parameter audit** | `npm run param:audit -- PARAM_NAME` | Find usages of a specific parameter |
| **Find unused params** | `npm run param:unused` | List all unused parameters |
| **Run review checks** | `npm run review:run -- file.qmd --checks fact,link` | Run specific checks on a file |
| **Run all reviews** | `npm run review:all -- --checks fact` | Run checks on all stale files |
| **Audit hardcoded values** | `npm run audit-hardcoded` | Find hardcoded numbers in QMD files |
| **Generate images** | `npm run images:sections -- file.qmd` | Generate section images for a file |
| **Validate pre-render** | `npm run validate:pre-render` | Run pre-render validation |
| **Generate and validate** | `npm run validate:full` | Regenerate artifacts, then run validation |
| **Generate everything** | `npm run generate:everything` | Regenerate variables, calculations, references |

## Directory Structure

```
scripts/
├── images/                      # Image generation and processing
├── lib/                         # Shared utilities and constants
├── review/                      # Content review and validation
├── agents/                      # AI agent implementations
├── prompts/                     # LLM prompt templates
└── *.ts, *.py                   # Top-level utility scripts
```

## Core Systems

### 1. Parameter System

The book uses a centralized parameter system where all numeric values are defined in `dih_models/parameters.py` and exposed as Quarto variables.

**Key Scripts:**
- `parameter-audit.ts` - Find parameter usages, list all params, find unused params
- `generate-everything-parameters-variables-calculations-references.py` - Regenerate `_variables.yml`

**Usage:**
```bash
# Find usages of a specific parameter
npx tsx scripts/parameter-audit.ts DFDA_LIVES_SAVED_ANNUAL

# List all parameters
npx tsx scripts/parameter-audit.ts --all

# Find unused parameters
npx tsx scripts/parameter-audit.ts --unused
```

### 2. Review System

Unified review framework for content validation.

**Key Scripts:**
- `review/run-checks.ts` - Single entry point for all review checks
- Individual check scripts in `review/` (for backwards compatibility)

**Available Checks:**
| Check | Description | Hash Field |
|-------|-------------|------------|
| `fact` | Verify claims and statistics | `lastFactCheckHash` |
| `link` | Verify internal/external links | `lastLinkCheckHash` |
| `figure` | Check figure references | `lastFigureCheckHash` |
| `structure` | Document structure validation | `lastStructureCheckHash` |
| `param` | Find hardcoded values | `lastParamCheckHash` |
| `latex` | Verify LaTeX equations | `lastLatexCheckHash` |
| `format` | Content formatting | `lastFormattedHash` |
| `nonprofit` | Nonprofit compliance | `lastNonprofitComplianceHash` |

**Usage:**
```bash
# Run multiple checks on a single file
npx tsx scripts/review/run-checks.ts knowledge/file.qmd --checks fact,link

# Run checks on all stale files
npx tsx scripts/review/run-checks.ts --all --checks fact

# Force recheck (ignore hash tracking)
npx tsx scripts/review/run-checks.ts --all --checks link --force

# Dry run - see what would be processed
npx tsx scripts/review/run-checks.ts --all --checks structure --dry-run
```

### 3. Hash Tracking System

Files are tracked using content hashes to avoid reprocessing unchanged files.

**Key Files:**
- `lib/constants.ts` - Hash field definitions
- `lib/hash_store.py` - Python wrapper for hash tracking
- `.file-hashes.json` - Stored hashes (root directory)

**Hash Fields:**
All hash fields are defined in `lib/constants.ts` under `HASH_FIELDS`. Each review operation updates the corresponding hash field in the file's frontmatter.

### 4. Image System

Scripts for generating and processing images.

**Key Scripts:**
- `images/generate-section-images.ts` - Generate images for QMD sections
- `images/fix-image-issues.ts` - Fix common image problems
- `images/enrich-image-metadata.ts` - Add metadata to images
- `images/generate-image-index.ts` - Build searchable image index

**Usage:**
```bash
# Generate images for a specific file
npm run images:sections -- knowledge/file.qmd

# Generate for all files
npm run images:sections:all

# Force regeneration
npm run images:sections:force
```

## Library Modules (`lib/`)

| Module | Purpose |
|--------|---------|
| `constants.ts` | Hash fields, directories, file patterns |
| `file-utils.ts` | File reading, writing, hash management |
| `llm.ts` | Gemini/Claude API integrations |
| `hash_store.py` | Python hash tracking wrapper |
| `image-analysis.ts` | AI image analysis prompts |
| `image-metadata.ts` | Image metadata types |
| `image-file-utils.ts` | Image file operations |
| `image-prompts.ts` | Image generation prompts |

## Claude Code Integration

### Hooks

Located in `.claude/hooks/`:

| Hook | Trigger | Purpose |
|------|---------|---------|
| `quick-validate.py` | PostToolUse (Edit\|Write) | Fast validation after edits |
| `check-pending-work.py` | SessionStart | Show pending tasks |
| `check-pdf-validation-errors.py` | Pre-commit | Validate PDFs |

### Skills

Located in `.claude/skills/`:
- Various specialized skills for book maintenance

## Adding New Scripts

1. **TypeScript preferred** for new utility scripts
2. Use `lib/constants.ts` for hash fields and patterns
3. Add npm scripts to `package.json` for common operations
4. Follow existing patterns in similar scripts
5. Add UTF-8 header to Python scripts for Windows compatibility

## Development

```bash
# Run any TypeScript script
npx tsx scripts/script-name.ts [args]

# Run Python scripts
.venv/Scripts/python.exe -u scripts/script-name.py [args]
```
