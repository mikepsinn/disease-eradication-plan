---
name: manage-publications
description: Manage academic paper publication workflows - track publication status across platforms (Zenodo, SSRN, arXiv, journals), generate PDFs, and update publication URLs in Quarto configs
---

# Publication Management Skill

This skill manages publication workflows for Quarto-based academic papers in this project.

## When to Use

Activate this skill when the user:
- Asks to check publication status ("what's the status of my papers?")
- Wants to generate PDFs ("generate PDFs for all papers")
- Needs to update publication URLs or status ("I just uploaded to SSRN")
- Requests a publication TODO list ("what publications are pending?")
- Mentions preprints, journals, or publication platforms

## Publications in This Project

This project contains 6 Quarto publications:
1. **Book**: "How to End War and Disease" (`_quarto-manual.yml`)
2. **Economics Paper**: "The 1% Treaty" (`_quarto-1-pct-treaty-impact.yml`)
3. **IAB Paper**: "Incentive Alignment Bonds" (`_quarto-iab.yml`)
4. **Wishocracy Paper**: "RAPPA for Democratic Resource Allocation" (`_quarto-wishocracy.yml`)
5. **dFDA Spec Paper**: "Two-Stage Real-World Evidence Validation" (`_quarto-dfda-spec.yml`)
6. **dFDA Impact Paper**: "Cost-Benefit Analysis & ROI" (`_quarto-dfda-impact.yml`)

## Configuration Location

Each publication has a `_quarto-*.yml` file in the project root containing:
- **Path**: `metadata.publishing` section
- **Structure**:
  - `own-site`: {url, status}
  - `preprints`: [{platform, status, url, doi}]
  - `journals`: [{name, tier, status, url}]

**Important**: Exclude files in `_build_temp/` - those are build artifacts.

## Core Workflows

### 1. Show Publication Status

**When requested**, display status for all papers:

```
Publication Status (6 papers)
─────────────────────────────────────────

Economics Paper (1% Treaty)
  Config: _quarto-1-pct-treaty-impact.yml
  ✓ Own Site: deployed (https://impact.warondisease.org)
  ✓ Zenodo: auto-uploaded (DOI: 10.5281/zenodo.18161561)
  ⏳ SSRN: pending
  ⏳ arXiv: pending
  📋 Journals: 3 targets (Health Affairs, Value in Health, PLOS Medicine)

IAB Paper
  Config: _quarto-iab.yml
  ✓ Own Site: deployed (https://iab.warondisease.org)
  ✓ Zenodo: auto-uploaded (DOI: 10.5281/zenodo.18203222)
  ⏳ SSRN: pending
  ⏳ arXiv: pending
  📋 Journals: 6 targets (AER, JPE, Public Choice, ...)

[... continue for all 6 papers]
```

**How to do it:**
1. Use Glob to find all `_quarto-*.yml` files in project root
2. Read each file and extract `metadata.publishing` section
3. Display status with clear visual indicators:
   - ✓ for deployed/auto-uploaded/published
   - ⏳ for pending/target
   - 📋 for lists

### 2. Generate Publication TODO List

**When requested**, show actionable checklist of pending items:

```
Publication TODO List
═════════════════════════════════════════

PREPRINTS (High Priority - Week 1-2)
─────────────────────────────────────────

Economics Paper:
  [ ] Upload to SSRN (Social Science Research Network)
      Category: econ.GN (General Economics)
  [ ] Upload to arXiv (econ.GN category)

IAB Paper:
  [ ] Upload to SSRN (Political Economy category)
  [ ] Upload to arXiv (econ.GN or cs.GT - Game Theory)

Wishocracy Paper:
  [ ] Upload to SSRN (Political Science / Public Choice)
  [ ] Upload to arXiv (cs.GT - Game Theory)

dFDA Spec Paper:
  [ ] Upload to medRxiv (Health sciences preprint)
  [ ] Upload to arXiv (stat.ME - Methodology)

dFDA Impact Paper:
  [ ] Upload to medRxiv (Health sciences)
  [ ] Upload to SSRN (Health Economics)
  [ ] Upload to arXiv (econ.GN)

─────────────────────────────────────────
JOURNALS (Medium Priority - Week 4+)
─────────────────────────────────────────

Economics Paper:
  [ ] Submit to Health Affairs (Tier 1)
  [ ] Submit to Value in Health (Tier 2)
  [ ] Submit to PLOS Medicine (open access)

IAB Paper:
  [ ] Submit to Public Choice (Tier 2)
  [ ] Submit to American Economic Review (Tier 1)
  [ ] Submit to Journal of Political Economy (Tier 1)

[... continue for all papers]

═════════════════════════════════════════
Summary: 15 pending preprints, 18 journal targets
```

**How to generate:**
1. Read `metadata.publishing` from all configs
2. Filter for `status: pending` (preprints) or `status: target` (journals)
3. Group by priority:
   - **High**: Preprints (SSRN, arXiv, medRxiv, OSF)
   - **Medium**: Journal submissions
4. Include relevant metadata (categories, tier levels)

### 3. Generate PDFs with Review

**IMPORTANT: PDFs for publication should include quality review!**

#### Review Levels

Users can choose thoroughness:

**A. Basic Review** (~2-5 min/paper - fast):
```
User: Generate PDFs (basic review)
→ 1. Pre-render validation + auto-fixes
→ 2. PDF generation
→ 3. Post-render validation
→ 4. Brief report
```

**B. Standard Review** (~5-10 min/paper - recommended):
```
User: Generate PDFs for publication
→ 1. Pre-render validation + auto-fixes
→ 2. Citation verification
→ 3. PDF generation
→ 4. Post-render validation
→ 5. Review report
```

**C. Comprehensive Review** (~15-30 min/paper - pre-submission):
```
User: Generate PDFs with full review
→ 1. Pre-render validation + auto-fixes
→ 2. AI content quality review
→ 3. Parameter methodology critique
→ 4. Citation verification
→ 5. PDF generation
→ 6. Post-render validation
→ 7. Detailed review report
```

#### Standard Review Workflow (Default)

When user requests PDF generation, run **Standard Review**:

**Step 1: Pre-Render Validation + Auto-Fixes**
```bash
python scripts/pre-render-validation.py
```
- Detects: LaTeX errors, broken links, missing citations, unknown variables
- If errors found: Use `/pre-render-validate` skill to auto-fix
- Auto-fixable issues:
  ✅ LaTeX syntax errors
  ✅ Missing image references
  ✅ Broken cross-reference links
  ✅ Unknown variables
  ✅ Hardcoded numbers
  ✅ Missing citations
  ✅ GIF file wrapping
  ✅ Python syntax errors

**Step 2: Citation Verification**
- Use `/verify-and-add-sources` skill
- Ensures all claims properly cited
- Searches for missing sources
- Adds references to bibliography

**Step 3: PDF Generation**
```bash
python scripts/render-quarto.py <project> --to pdf
```
- Includes built-in Python code leakage validation

**Step 4: Post-Render Validation**
```bash
python scripts/post-render-validation.py
```
- Checks rendered HTML for issues
- Validates: broken links, unrendered expressions, formatting

**Step 5: Review Report**
Display publication readiness report with findings from all stages.

#### Comprehensive Review (Optional Steps)

For comprehensive review, add between Step 1 and Step 2:

**Content Quality Review:**
- Use `/review-qmd` skill on main paper file
- Checks: clarity, engagement, rigor, structure, tone
- Generates improvement suggestions
- Optional: apply improvements

**Parameter Methodology Critique:**
- Use `/critique-calculation` skill for key parameters
- Validates formulas, empirical backing, uncertainty
- Identifies weaknesses and improvements

#### Example Output

```
Generating PDFs with Standard Review...

[1/6] Economics Paper (1% Treaty)
═══════════════════════════════════════════

[Step 1/5] Pre-Render Validation
  Running: python scripts/pre-render-validation.py
  ✓ No LaTeX errors
  ✓ All images found
  ✓ All cross-references valid
  ⚠ 3 citations missing - Running auto-fix...
  ✓ Auto-fixed 3 missing citations

[Step 2/5] Citation Verification
  Running: /verify-and-add-sources skill
  ✓ All 47 claims properly cited
  ✓ Bibliography complete

[Step 3/5] PDF Generation
  Running: python scripts/render-quarto.py economics --to pdf
  ✓ Generated: _site/economics/economics-paper.pdf (1.3 MB)
  ✓ No Python code leakage detected

[Step 4/5] Post-Render Validation
  Running: python scripts/post-render-validation.py
  ✓ All internal links functional
  ✓ No unrendered expressions
  ✓ PDF navbar links valid

[Step 5/5] Review Report
─────────────────────────────────────────
PUBLICATION READINESS: ✓ READY
Minor warnings: None
Critical errors: None
PDF ready for upload to SSRN, arXiv, journals
─────────────────────────────────────────

[2/6] IAB Paper
═══════════════════════════════════════════
[... continues for all papers]
```

#### How to Implement

1. **Detect review level** from user request:
   - "basic review" → Basic
   - "full review" / "comprehensive" → Comprehensive
   - Default → Standard

2. **Run validation pipeline:**
   ```python
   # Step 1: Pre-render validation
   subprocess.run(['python', 'scripts/pre-render-validation.py'])
   # If errors: use /pre-render-validate skill

   # Step 2 (Standard+): Citation verification
   # Use /verify-and-add-sources skill

   # Steps for Comprehensive only:
   # Use /review-qmd skill
   # Use /critique-calculation skill

   # Step 3: Generate PDF
   subprocess.run(['python', 'scripts/render-quarto.py', project, '--to', 'pdf'])

   # Step 4: Post-render validation
   subprocess.run(['python', 'scripts/post-render-validation.py'])
   ```

3. **Compile review report** with findings from all stages

4. **Show review report** and ask user if they want to:
   - Proceed with upload (if clean)
   - Fix warnings manually (if warnings)
   - Fix critical errors (if errors found)

### 4. Update Publication Metadata (Interactive)

**When user reports uploading a paper**, guide them through updating the config:

**Example conversation:**
```
User: I just uploaded the economics paper to SSRN
Claude: Great! Let me update the config. What's the SSRN URL?
User: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1234567
Claude: Should I change the status from "pending" to "submitted"?
User: Yes
Claude: [Shows preview of changes]

Preview of changes to _quarto-1-pct-treaty-impact.yml:
───────────────────────────────────────────
  preprints:
    - platform: ssrn
-     status: pending
+     status: submitted
-     url: ""
+     url: "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1234567"

Apply these changes? (y/n)
User: y
Claude: ✓ Updated _quarto-1-pct-treaty-impact.yml
```

**How to update YAML:**

**CRITICAL SAFETY RULES:**
1. **Always preview changes** before writing
2. **Wait for user confirmation**
3. **Use ruamel.yaml** to preserve formatting (NOT PyYAML)
4. **Only modify `metadata.publishing` section**
5. **Verify the file parses after changes**

**Update workflow:**
1. Read the appropriate `_quarto-*.yml` file
2. Navigate to `metadata.publishing` section
3. Find the specific platform or journal entry
4. Update the relevant fields (status, url, doi)
5. Show diff preview
6. Get user confirmation
7. Write changes using Edit tool
8. Verify file still parses correctly

**Status values:**
- `deployed` - Own site is live
- `auto-uploaded` - Zenodo automated upload
- `pending` - Not yet uploaded
- `submitted` - Uploaded/submitted but not published
- `published` - Published and live
- `target` - Journal target (not yet submitted)
- `rejected` - Submission rejected

## Implementation Notes

### Discovery Pattern

```python
# Find all Quarto config files (exclude build artifacts)
import glob
configs = [
    f for f in glob.glob('_quarto-*.yml')
    if '_build_temp' not in f
]
```

### YAML Parsing (If Helper Script Needed)

**Use ruamel.yaml to preserve formatting:**

```python
from ruamel.yaml import YAML

yaml = YAML()
yaml.preserve_quotes = True
yaml.default_flow_style = False

# Read
with open(config_file, 'r', encoding='utf-8') as f:
    config = yaml.load(f)

# Access publishing metadata
publishing = config['metadata']['publishing']

# Modify
for preprint in publishing['preprints']:
    if preprint['platform'] == 'ssrn':
        preprint['status'] = 'submitted'
        preprint['url'] = new_url

# Write (preserves original formatting)
with open(config_file, 'w', encoding='utf-8') as f:
    yaml.dump(config, f)
```

### PDF Output Paths

Each project has its PDF specified in the config under `dih-render.pdf-output-file`:
- Book: `How-to-End-War-and-Disease.pdf`
- Economics: `economics-paper.pdf`
- IAB: `incentive-alignment-bonds-paper.pdf`
- Wishocracy: `wishocracy-rappa-paper.pdf`
- dFDA Spec: `dfda-paper.pdf`
- dFDA Impact: `dfda-impact-paper.pdf`

All PDFs are output to `_site/<project-name>/` directory.

## Publication Platforms Reference

### Preprint Servers
- **Zenodo**: Auto-uploaded via GitHub Actions, assigns DOI
- **SSRN**: Social Science Research Network (economics, political science)
- **arXiv**: Physics, math, CS, econ (requires category)
- **medRxiv**: Health sciences preprints
- **OSF Preprints**: Open Science Framework

### Journal Categories by Paper
- **Economics**: Health Affairs, Value in Health, The Lancet, BMJ, PLOS Medicine
- **IAB**: AER, JPE, Public Choice, Games & Economic Behavior, J. Public Econ
- **Wishocracy**: APSR, J. Politics, Social Choice & Welfare, Public Choice
- **dFDA Spec**: Clinical Pharm & Therapeutics, Pharmacoepidemiology, Drug Safety
- **dFDA Impact**: Health Affairs, Value in Health, PharmacoEconomics

## Examples

### Example 1: Check Status
```
User: What's the publication status?
→ Skill displays status table for all 6 papers
```

### Example 2: Generate PDFs
```
User: Generate PDFs for all papers
→ Skill runs render-quarto.py for each project
→ Reports success and file locations
```

### Example 3: Update After Upload
```
User: I uploaded dFDA spec to medRxiv: https://medrxiv.org/content/10.1101/2025.01.15.12345678
→ Skill identifies dFDA spec paper
→ Updates medRxiv preprint entry
→ Changes status to "submitted"
→ Adds URL
→ Previews changes
→ Updates _quarto-dfda-spec.yml after confirmation
```

### Example 4: TODO List
```
User: What do I need to publish next?
→ Skill generates TODO list
→ Prioritizes preprints first
→ Shows 15 pending preprints, 18 journal targets
→ Includes submission categories and tiers
```

## Tips for Success

1. **Always show before changing**: Preview YAML diffs before writing
2. **Be specific**: When updating, confirm which paper and platform
3. **Context matters**: Reference paper titles and DOIs for clarity
4. **File safety**: Only modify `metadata.publishing`, never other sections
5. **Verify**: After updates, confirm file still parses correctly
6. **Batch operations**: When generating PDFs, do all at once for efficiency

## Future Enhancements

- Automated peer review before submission
- Bulk status updates via CSV import
- Integration with Zenodo API to auto-fetch DOIs
- Journal submission checklist generator
- Citation count tracking from Google Scholar
