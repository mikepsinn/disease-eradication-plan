# Audience-Specific Content Generation System

This system automatically generates audience-tailored versions of all content files from your source (funny) versions.

## Philosophy

**Source files are the entertaining versions.** They're funny, engaging, sarcastic, and designed to be memorable. These live in `knowledge/` without any suffix (e.g., `cost-of-war.qmd`).

**Generated files are audience-specific transformations.** They maintain all data, citations, and core arguments, but adjust tone for specific audiences. These have suffixes like `-foundations.qmd` or `-academic.qmd`.

## File Naming Convention

```
knowledge/problem/
├── cost-of-war.qmd                    # Source (funny, engaging)
├── cost-of-war-foundations.qmd        # Generated (professional)
├── cost-of-war-academic.qmd           # Generated (formal)
├── untapped-therapeutic-frontier.qmd  # Source
├── untapped-therapeutic-frontier-foundations.qmd
├── untapped-therapeutic-frontier-academic.qmd
...
```

## Audiences

### 1. **Foundations** (`-foundations.qmd`)
**Target**: Gates Foundation, Wellcome Trust, Open Philanthropy, etc.

**Tone**: Professional, evidence-based, non-inflammatory

**What changes**:
- Remove direct attacks on readers ("you")
- Soften sarcastic section titles
- Remove profanity and crude language
- Transform dismissive characterizations into systemic critiques
- Keep humor that isn't mean

**What stays**:
- ALL data, statistics, citations
- Core arguments and critiques
- Compelling examples
- Memorable metaphors (made less accusatory)
- Sense of urgency

### 2. **Academic** (`-academic.qmd`)
**Target**: Journal of Health Economics, Health Affairs, PLOS Medicine, etc.

**Tone**: Formal, neutral, third-person, evidence-only

**What changes**:
- Remove ALL humor and sarcasm
- Convert to third-person perspective
- Remove rhetorical questions
- Transform informal headings to academic style
- Remove emotional appeals

**What stays**:
- ALL data, statistics, citations, formulas
- Methodological details
- Critical analysis (made formal)
- Core research contribution

## Usage

### Initial Setup (First Time)

Create baseline copies to track changes in git:

```bash
# 1. Create exact copies (no transformations)
npm run generate:audience:baseline

# 2. Commit baseline
git add .
git commit -m "baseline: copy source files to audience versions"

# 3. Apply transformations
npm run generate:audience:all

# 4. Review changes
git diff

# 5. Commit transformations
git add .
git commit -m "feat: apply audience-specific transformations"
```

### Generate versions for a specific audience

```bash
# Generate foundation versions of all files
npm run generate:audience:foundations

# Generate academic versions of all files
npm run generate:audience:academic

# Generate both
npm run generate:audience:all
```

### Regular Workflow

1. **Edit source files** - Make changes to the entertaining versions (no suffix)
2. **Regenerate audience versions** - Run `npm run generate:audience:all`
3. **Review transformations** - Check git diff for changes
4. **Update Quarto configs** - Point `_quarto-*.yml` to appropriate versions

### What the script does

For each source file (e.g., `cost-of-war.qmd`):
1. **Copy** source → target (e.g., `cost-of-war-foundations.qmd`)
2. **Load** audience-specific transformation rules
3. **Transform** content using Gemini LLM with instructions
4. **Preserve** all frontmatter, citations, data, structure
5. **Track** with hash to avoid re-processing unchanged files

## Transformation Rules

### Foundations (`instructions-foundations-prompt.md`)
- Professional but engaging
- Remove attacks, keep critiques
- Soften sarcasm, keep facts
- Transform "you" → systemic observations

### Academic (`instructions-academic-prompt.md`)
- Formal third-person only
- No humor, no emotion
- Academic vocabulary
- Standard journal structure

## Quarto Configuration

Point different Quarto books at different audience versions:

### `_quarto-economics.yml` (for foundations)
```yaml
chapters:
  - text: "The Cost of War"
    href: knowledge/problem/cost-of-war-foundations.qmd
  - text: "NIH Inefficiency"
    href: knowledge/problem/nih-spent-1-trillion-eradicating-0-diseases-foundations.qmd
```

### `_quarto-academic.yml` (for journals)
```yaml
chapters:
  - text: "Economic Burden of Armed Conflict"
    href: knowledge/problem/cost-of-war-academic.qmd
  - text: "Resource Allocation in Biomedical Research"
    href: knowledge/problem/nih-spent-1-trillion-eradicating-0-diseases-academic.qmd
```

### `_quarto.yml` (default - original funny versions)
```yaml
chapters:
  - text: "The Cost of War"
    href: knowledge/problem/cost-of-war.qmd
```

## Benefits of This Approach

1. **Single source of truth** - Edit once, regenerate for all audiences
2. **Version control friendly** - All versions tracked, easy to diff
3. **Consistency** - Same data and arguments across all versions
4. **Flexibility** - Easy to add new audiences (investors, policy-makers, etc.)
5. **Automation** - Regenerate everything after any source edit

## Adding New Audiences

To add a new audience (e.g., "policy-makers"):

1. Create `scripts/review/instructions-policymakers-prompt.md` with concise transformation rules
2. Add to `AUDIENCES` object in `generate-audience-versions.ts`:
   ```typescript
   const AUDIENCES = {
     foundations: 'instructions-foundations-prompt.md',
     academic: 'instructions-academic-prompt.md',
     policymakers: 'instructions-policymakers-prompt.md', // NEW
   } as const;
   ```
3. Run: `npx tsx scripts/review/generate-audience-versions.ts policymakers`
4. Files generated with `-policymakers.qmd` suffix

## Important Notes

- **Never edit generated files directly** - They'll be overwritten on next generation
- **Source files should be entertaining** - That's the whole point
- **Citations are sacred** - Transformation never removes citations
- **Data is immutable** - Numbers, formulas, statistics stay exact
- **Review transformations** - LLM isn't perfect; check critical passages

## Example Transformations

### Source (cost-of-war.qmd)
> "You think you've explored medicine. In reality, you're standing in the parking lot of Disney World bragging about how fun the pavement is."

### Foundations (cost-of-war-foundations.qmd)
> "Despite significant investment in medical research, current efforts have explored less than 1% of potential therapeutic interventions. This is comparable to standing in a theme park's entrance area without accessing the attractions inside."

### Academic (cost-of-war-academic.qmd)
> "Despite substantial investment in pharmaceutical research, current therapeutic development has explored less than 1% of theoretically feasible drug-disease combinations, representing a significant gap between potential and realized therapeutic space."

---

**Last Updated**: 2025-12-21
