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
1. **Book**: "How to End War and Disease" (`_quarto-book.yml`)
2. **Economics Paper**: "The 1% Treaty" (`_quarto-economics.yml`)
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
  Config: _quarto-economics.yml
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

### 3. Generate PDFs

**When requested**, generate PDFs for all papers using existing render script:

```
Generating PDFs for all publications...

[1/6] Book: How to End War and Disease
  Command: python scripts/render-quarto.py book --to pdf
  Status: Generating... (this may take a few minutes)
  ✓ Generated: _site/book/How-to-End-War-and-Disease.pdf (15.2 MB)

[2/6] Economics Paper (1% Treaty)
  Command: python scripts/render-quarto.py economics --to pdf
  ✓ Generated: _site/economics/economics-paper.pdf (1.3 MB)

[3/6] IAB Paper
  Command: python scripts/render-quarto.py iab --to pdf
  ✓ Generated: _site/iab/incentive-alignment-bonds-paper.pdf (920 KB)

[4/6] Wishocracy Paper
  Command: python scripts/render-quarto.py wishocracy --to pdf
  ✓ Generated: _site/wishocracy/wishocracy-rappa-paper.pdf (850 KB)

[5/6] dFDA Spec Paper
  Command: python scripts/render-quarto.py dfda-spec --to pdf
  ✓ Generated: _site/dfda-spec/dfda-paper.pdf (1.1 MB)

[6/6] dFDA Impact Paper
  Command: python scripts/render-quarto.py dfda-impact --to pdf
  ✓ Generated: _site/dfda-impact/dfda-impact-paper.pdf (980 KB)

All PDFs generated successfully!
Output directory: E:\code\obsidian\websites\disease-eradication-plan\_site\
```

**How to do it:**
1. For each publication, determine the project name:
   - book → `book`
   - _quarto-economics.yml → `economics`
   - _quarto-iab.yml → `iab`
   - _quarto-wishocracy.yml → `wishocracy`
   - _quarto-dfda-spec.yml → `dfda-spec`
   - _quarto-dfda-impact.yml → `dfda-impact`

2. Run: `python scripts/render-quarto.py <project> --to pdf`

3. Check for PDF in `_site/<project>/` directory

4. Report file size and location

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

Preview of changes to _quarto-economics.yml:
───────────────────────────────────────────
  preprints:
    - platform: ssrn
-     status: pending
+     status: submitted
-     url: ""
+     url: "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1234567"

Apply these changes? (y/n)
User: y
Claude: ✓ Updated _quarto-economics.yml
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
