## Project Overview

This is a Quarto-based book project: "How to End War and Disease" - a guide to getting nations to sign a 1% treaty, redirecting military spending to the Decentralized Institutes of Health and decentralized framework for drug assessment to automate ubiquitous clinical trials. 

**Key Navigation:**

- **`todo.md`**: Master task list and current priorities for book completion
- **`OUTLINE.md`**: Complete book outline (comprehensive writing checklist)
- **`index.qmd`**: Book introduction and overview (landing page)
- **`_book.yml`**: Book configuration, chapter order, and output formats
- **`package.json`**: Node.js dependencies and npm scripts

**Important:** Use `tsx` (not ts-node) to run TypeScript files. Example: `npx tsx scripts/review/review.ts`

### Applying Global Changes to All QMD Files

When the user requests a change that should be applied to all QMD chapter/appendix files (e.g., "replace all instances of X with Y", "fix all occurrences of...", "update formatting for..."), use the automated batch processing script:

```bash
npx tsx scripts/review/apply-instruction-all-files.ts "Your instruction here"
```

**Examples:**
```bash
# Style/formatting changes
npx tsx scripts/review/apply-instruction-all-files.ts "Replace all instances of 'utilise' with 'use'"

# Consistency fixes
npx tsx scripts/review/apply-instruction-all-files.ts "Ensure all section headers use sentence case, not title case"

# Content updates
npx tsx scripts/review/apply-instruction-all-files.ts "Replace references to 'FDA approval timeline' with 'regulatory approval timeline'"
```

**How it works:**
- Loops through all book QMD files (excludes references.qmd, vision.qmd, futures chapters)
- Sends each file to Gemini Pro with your instruction
- Shows 5-second preview with file list before processing
- Tracks statistics (modified/unchanged/errors)
- Continues processing if individual files fail

### Python Scripts on Windows

**CRITICAL: All Python scripts must handle Windows console encoding.**

Add this header to every Python script:
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
```

**Avoid Unicode characters in print statements** that may fail on Windows console (arrows →, emojis ⚠️, checkmarks ✅). Use ASCII alternatives: `->`, `WARNING:`, `[OK]`.

## Code Quality and Verification Standards

**CRITICAL: These rules exist to prevent careless errors that have caused significant problems in the past.**

### Commit Rules

**NEVER commit changes unless:**
1. The user has **explicitly requested** a commit
2. You have **reviewed EVERY SINGLE CHANGE** for errors
3. You have **verified all parameter names** match `_variables.yml` (lowercase format)
4. You have **run validation checks** to ensure no regressions



## Parameter and Variable System

**CRITICAL: Use the automated parameter/variable system for all numeric values.**

**Before hardcoding ANY value in QMD files, check `_variables.yml` first.** All available variables are listed there in lowercase format (e.g., `global_military_spending_annual_2024`, `treaty_annual_funding`).

### When Editing QMD Files

**ALWAYS check for hardcoded numbers that should be variables:**
- When you edit a QMD file, scan for hardcoded numbers like `$14M`, `$929`, `15,076`, etc.
- Search `_variables.yml` for existing variables: `grep "keyword" _variables.yml`
- If a variable exists, use `{{< var variable_name >}}` instead of the hardcoded value
- If no variable exists but should, create it in `dih_models/parameters.py` first

**Common hardcoded values to replace:**
- Trial costs: Use `{{< var adaptable_trial_cost_per_patient >}}`, `{{< var recovery_trial_cost_per_patient >}}`
- Patient counts: Use `{{< var adaptable_trial_patients >}}`, `{{< var recovery_trial_patients >}}`
- Cost reductions: Use `{{< var dfda_trial_cost_reduction_factor >}}`

### How It Works

1. **Define parameters** in `dih_models/parameters.py`:
   ```python
   FOUNDATION_FUNDING_REALISTIC = Parameter(
       519_000_000,  # Use underscores for readability
       unit="USD",   # Formatter auto-scales to "$519M"
       source_ref="/knowledge/appendix/fundraising-strategy.qmd#...",
       description="Nonprofit foundation funding in realistic scenario",
       confidence="high"
   )
   ```

2. **Generate variables** by running:
   ```bash
   .venv/Scripts/python.exe scripts/generate-everything-parameters-variables-calculations-references.py
   ```

3. **Use in QMD files** (formatter handles all formatting):
   ```markdown
   Foundation funding: {{< var foundation_funding_realistic >}}
   ```
   Output: "Foundation funding: $519M" (with HTML tooltip and source link)

### Quick Parameter Lookup

**Use `_analysis/parameter-summary.md` to quickly get calculated values** (auto-generated, one parameter per line):

```bash
grep "TREATY_ANNUAL_FUNDING" _analysis/parameter-summary.md
# → TREATY_ANNUAL_FUNDING: $27.2B (95% CI: $27.2B-$27.2B)
```

### Parameter Naming Rules

**CRITICAL: Parameter names must be SELF-DOCUMENTING. A reader should know EXACTLY what is being measured without looking at the description.**

**Naming Structure: `[SCOPE]_[METRIC]_[MODIFIERS]_[UNIT_TYPE]`**

- **SCOPE**: What entity? (DFDA, TREATY, GLOBAL, PERSONAL, VICTORY_BOND, etc.)
- **METRIC**: What's being measured? (ROI, COST, BENEFIT, DEATHS, DALYS, etc.)
- **MODIFIERS**: Scenario, timeframe, calculation method
- **UNIT_TYPE**: Optional for clarity (ANNUAL, PCT, RATIO, etc.)

**Examples:**

✅ **Good (self-documenting):**
```python
TREATY_COMPLETE_ROI_EXPECTED_95TH_PERCENTILE  # Clear: Treaty, complete benefits, expected value, 95th percentile
DFDA_ROI_RD_ONLY                              # Clear: dFDA, R&D savings only
PERSONAL_LIFE_EXTENSION_YEARS_AGE_30          # Clear: Personal benefit, life extension, for age 30
VICTORY_BOND_ANNUAL_RETURN_PCT                # Clear: VICTORY Incentive Alignment Bonds, annual return, percentage
```

❌ **Bad (ambiguous):**
```python
PROBABILISTIC_ROI_EXPECTED_UPPER_BOUND        # ROI of WHAT? dFDA? Treaty? R&D only?
ANNUAL_BENEFIT                                # Benefit of WHAT? Which scenario?
TOTAL_COST                                    # Total cost of WHAT?
ROI_MEDIAN                                    # Median ROI for WHAT intervention?
```

**Specific Rules:**

- **Parameter name**: `FOUNDATION_FUNDING_REALISTIC` (uppercase, semantic name)
- **Variable name**: `foundation_funding_realistic` (lowercase, auto-generated)
- **Unit**: Specify unit type, formatter handles scaling
- **DO NOT** include scale in parameter name:
  - ❌ `FOUNDATION_FUNDING_REALISTIC_MILLIONS`
  - ❌ `REGULATORY_DELAY_DEATHS_MILLIONS`
  - ❌ `ECONOMIC_LOSS_TRILLIONS`
- **DO NOT** manually format in QMD:
  - ❌ `${{< var foundation_funding_realistic >}}M`
  - ❌ `{{< var regulatory_delay_deaths >}}M deaths`
- **DO** include scope prefix for ROI/cost/benefit parameters:
  - ✅ `TREATY_COMPLETE_ROI_CONSERVATIVE` (not just `CONSERVATIVE_ROI`)
  - ✅ `DFDA_ANNUAL_COST` (not just `ANNUAL_COST`)
  - ✅ `PERSONAL_LIFETIME_BENEFIT_AGE_30` (not just `LIFETIME_BENEFIT`)

**Examples:**

✅ **Correct:**
```python
# Currency
FOUNDATION_FUNDING = Parameter(519_000_000, unit="USD")  # Displays as "$519M"

# Deaths
REGULATORY_DELAY_DEATHS = Parameter(184_600_000, unit="deaths")  # Displays as "184.6M"

# DALYs
TOTAL_DALYS = Parameter(4_830_000_000, unit="DALYs")  # Displays as "4.83B"
```

❌ **Wrong:**
```python
# DO NOT include scale in parameter name
FOUNDATION_FUNDING_MILLIONS = Parameter(519_000_000, unit="USD")

# DO NOT pre-scale the value - store raw numbers
REGULATORY_DELAY_DEATHS_MEAN = Parameter(184.6, unit="millions of deaths")

# DO NOT use both - always store raw value and let formatter auto-scale
PEACE_DIVIDEND_BILLIONS = Parameter(113.55, unit="billions USD")
```

**Why wrong**:
- Formatter automatically determines appropriate scale ($519M, 184.6M, $113.55B)
- Pre-scaled values (184.6 instead of 184_600_000) break the auto-scaling logic
- Scale suffixes in names (_MILLIONS, _BILLIONS) are redundant and confusing

### Formatter Capabilities

The `format_parameter_value()` function automatically:
- **Currency**: `unit="USD"` → auto-scales to $519M, $1.02B, $50K, $483T
- **Large numbers**: Auto-scales deaths/DALYs/years to M/B/K (≥100K)
  - `184_600_000` with `unit="deaths"` → `"184.6M"`
  - `4_830_000_000` with `unit="DALYs"` → `"4.83B"`
- **Percentages**: `unit="percentage"` → "51%"
- **Small numbers**: Uses commas (1,000-99,999) or raw values (<1,000)
- **3 significant figures** precision for all scaled values

### Calculated Parameters

**CRITICAL: Parameters marked as `source_type="calculated"` MUST use formulas, not hardcoded values.**

✅ **Correct** (calculated using inline formulas):
```python
PEACE_DIVIDEND_ANNUAL = Parameter(
    GLOBAL_ANNUAL_WAR_TOTAL_COST * TREATY_REDUCTION_PCT,
    source_type="calculated",
    description="Annual peace dividend from 1% treaty",
    unit="USD",  # Formatter auto-scales to $113.55B
    formula="GLOBAL_WAR_COST × 1%"
)

TREATY_CAMPAIGN_TOTAL_COST = Parameter(
    TREATY_CAMPAIGN_REFERENDUM + TREATY_CAMPAIGN_LOBBYING + TREATY_CAMPAIGN_RESERVE,
    source_type="calculated",
    description="Total campaign cost",
    unit="USD",  # Store raw value, let formatter auto-scale to $1B
    formula="REFERENDUM + LOBBYING + RESERVE"
)
```

❌ **Wrong** (hardcoded value marked as calculated):
```python
PEACE_DIVIDEND_ANNUAL = Parameter(
    113_550_000_000,  # Hardcoded result
    source_type="calculated",  # Lie! Not actually calculated
    description="Annual peace dividend",
    unit="USD"
)
```

**When to use each source_type:**
- `source_type="external"`: Data from external sources (WHO, SIPRI, papers)
- `source_type="calculated"`: Derived using formulas from other parameters
- `source_type="definition"`: Fixed values, core assumptions, legacy compatibility values

### LaTeX Math Block Variables

**RECOMMENDED: Use LaTeX variables from `_variables.yml` instead of hardcoding.**

The `generate-variables-yml.py` script automatically exports LaTeX equations as `{param_name}_latex` variables that you can use directly in QMD files.

✅ **Best Practice** (use LaTeX variables):
```markdown
{{< var peace_dividend_annual_societal_benefit_latex >}}
```

This renders as:
```
$$
PD_{annual} = $11,355B \times 0.01 = $113.55B
$$
```

❌ **Avoid** (hardcoding LaTeX):
```markdown
$$
\$11{,}355\text{B} \times 1\% = \$113.55\text{B}
$$
```

❌ **Wrong** (variables don't work INSIDE LaTeX blocks):
```markdown
$$
\${{< var global_annual_war_total_cost >}} \times {{< var treaty_reduction_pct >}}
$$
```

**Why**:
- LaTeX equations defined in `parameters.py` get auto-exported as variables
- Single source of truth: change equation once in parameters.py, updates everywhere
- Maintains consistency between LaTeX formulas and their component parameters
- Quarto variables cannot be used INSIDE `$$` blocks, but LaTeX variables work OUTSIDE them

**IMPORTANT for hardcoded value audits:**
When auditing QMD files for hardcoded values to replace with variables:
1. **NEVER try to replace values inside LaTeX `$$` blocks** - Quarto variables don't render there
2. **Check `_variables.yml` for `_latex` suffixed variables** (e.g., `peace_dividend_annual_societal_benefit_latex`)
3. **Replace the entire LaTeX block** with the latex variable if one exists
4. **Leave LaTeX hardcoded values as-is** if no suitable `_latex` variable exists
5. **REMOVE hyperlinks from around variables** - Variables have built-in links to their source
   - Wrong: `[{{< var treaty_campaign_total_cost >}}](../economics/victory-bonds.qmd)`
   - Right: `{{< var treaty_campaign_total_cost >}}` (variable already links to source)
   - If link text is needed: `{{< var treaty_campaign_total_cost >}} via [VICTORY Bonds](../economics/victory-bonds.qmd)`

**Systematic LaTeX Equation Audit:**
Use `/latex-equation-audit` to systematically find calculated variables and add their `_latex` equations where contextually appropriate. The skill uses Ralph Loop to process all files iteratively.

### Why This Matters

- **Single source of truth**: All values come from parameters.py
- **Automatic tooltips**: Hover shows source, confidence, formula
- **Consistency**: Same value displayed identically everywhere
- **Zero maintenance**: Change parameter once, regenerates everywhere
- **Academic rigor**: Auto-generates parameters-and-calculations.qmd appendix

## Cross-Format Linking (HTML, PDF, EPUB)

**CRITICAL: Always use `.qmd` extensions for internal links in source files.**

Quarto automatically converts `.qmd` links to the appropriate format:
- **HTML output**: `.qmd` → `.html`
- **PDF/EPUB output**: `.qmd` → internal references

✅ **Correct** (cross-format compatible):
<!-- Example: [Link Text](../path/to/file.qmd) -->
<!-- Example: [Link with Anchor](../path/to/file.qmd#section-id) -->

❌ **Wrong** (breaks PDF/EPUB):
<!-- Example: [Link Text](../path/to/file.html) -->

**IMPORTANT**: Links only work if the target file is listed in `_quarto-book.yml` chapters. If post-validation reports `QMD_FILE_LINK` errors:

1. Check if target `.qmd` file exists
2. Add it to `_quarto-book.yml` in the appropriate section
3. Re-render - Quarto will handle format conversion

**External URLs** (outside the book) should use full URLs:
<!-- Example: [External Link](https://example.com/page.html) -->

## Foundation Grant Proposal System

The project includes a specialized version of the book formatted for foundation grant applications, with executive summary, budget breakdowns, and impact metrics suitable for philanthropic evaluation.

### Overview

The foundation grant proposal system extracts key content from the main book and reformats it for foundation program officers and philanthropic evaluators. It's a separate Quarto configuration that generates both a standalone website and a PDF suitable for grant portal uploads.

**Key Files:**
- **`_quarto-foundation.yml`**: Quarto configuration for the foundation grant proposal
- **`_variables-foundation-manual-DO-NOT-DELETE.yml`**: Foundation-specific variables (80+ simplified metrics, grant-ready text snippets)
- **`knowledge/grant-proposal/`**: Grant proposal content (8 QMD files)
- **Output**: HTML site at `_site/foundation-grant/` and PDF at `Foundation-Grant-Proposal.pdf`

### How to Render the Grant Proposal

**Render all formats (HTML + PDF):**
```bash
python scripts/render-quarto.py foundation
```

**Render only PDF:**
```bash
python scripts/render-quarto.py foundation --to pdf
```

**Render only HTML:**
```bash
python scripts/render-quarto.py foundation --to html
```

**Live preview with hot reload:**
```bash
python scripts/render-quarto.py foundation --preview
```

The render script automatically:
- Copies relevant files to `_build_temp/foundation/`
- Rewrites cross-site links (QMD links to main book chapters become absolute URLs)
- Validates the PDF for any code leakage
- Generates filtered `_variables-foundation.yml` (only variables used in grant proposal)

### Grant Proposal Structure

The proposal is organized for efficient evaluation by foundation program officers:

**Core Proposal** (~25 pages, essential reading):
1. **`index.qmd`**: Cover letter with overview and funding request
2. **`executive-summary.qmd`**: Comprehensive summary with key metrics
3. **`budget-breakdown.qmd`**: Detailed financial plan and ROI analysis
4. **`theory-of-change.qmd`**: Logic model and causal pathway diagram
5. **`evaluation-framework.qmd`**: KPIs and monitoring plan

**Supporting Documentation** (~20 pages):
6. **`organizational-capacity.qmd`**: Team, governance, partnerships
7. **`risk-analysis.qmd`**: Comprehensive risk assessment and mitigation
8. **`evidence-base.qmd`**: Historical precedents (Ottawa Treaty, RECOVERY trial) and academic validation

**Appendices** (reference materials):
- **`parameters-and-calculations.qmd`**: Complete methodology and source data
- **`references.qmd`**: 500+ peer-reviewed citations

### Customization for Specific Foundations

The grant proposal system is designed to be easily customized for specific foundation requirements.

**1. Edit Foundation Variables**

Edit `_variables-foundation-manual-DO-NOT-DELETE.yml` to customize:

```yaml
# Funding amounts (adjust based on foundation's grant size)
foundation_amount_requested_full: "$1.02B (full campaign budget)"
foundation_amount_requested_seed: "$250M-$400M (Phase 1 seed funding)"
foundation_amount_requested_anchor: "$50M-$100M (anchor donation)"

# Contact information
foundation_contact_name: "Mike P. Sinn"
foundation_contact_email: "mike@warondisease.org"
foundation_org_legal_name: "Decentralized Institutes of Health Foundation"

# Pitch customization (50/100/250-word versions available)
foundation_summary_50_words: "..."
foundation_summary_100_words: "..."
foundation_summary_250_words: "..."
```

**Common Customization Scenarios:**

- **Different funding tiers**: Edit `foundation_amount_requested_*` variables
- **Foundation-specific requirements**: Add new variables for required fields
- **Different emphasis**: Edit `foundation_pitch`, `foundation_primary_impact` for specific foundation priorities
- **Geographic scope**: Adjust `foundation_geographic_scope` if targeting regional foundations
- **Beneficiary focus**: Customize `foundation_beneficiaries` for specific populations

**2. Add Foundation-Specific Content**

For foundations with unique requirements, edit the QMD files in `knowledge/grant-proposal/`:

```bash
# Edit any grant proposal file
code knowledge/grant-proposal/executive-summary.qmd
```

**3. Regenerate Variables**

After editing parameters in `dih_models/parameters.py`, regenerate all variables including foundation-specific ones:

```bash
python scripts/generate-everything-parameters-variables-calculations-references.py
```

This automatically:
- Updates `_variables.yml` (main book variables)
- Updates `_variables-foundation.yml` (filtered subset used in grant proposal)
- Keeps `_variables-foundation-manual-DO-NOT-DELETE.yml` unchanged (manual customizations preserved)
- Regenerates `parameters-and-calculations.qmd` appendix

### Relationship to Main Book Content

The foundation grant proposal is a **targeted subset** of the main book, reformatted for philanthropic evaluation:

**Content Reuse:**
- **Parameters**: Grant proposal uses the same parameter system as main book (`_variables.yml`)
- **Calculations**: `parameters-and-calculations.qmd` appendix is identical to main book
- **References**: `references.qmd` uses the same bibliography
- **Evidence**: Grant proposal cites specific sections from main book for deeper exploration

**Key Differences:**
- **Tone**: Grant proposal uses more conservative, academically rigorous language suitable for foundation review
- **Length**: Core proposal is ~45 pages (vs. 300+ page main book)
- **Structure**: Organized around standard grant proposal sections (executive summary, budget, theory of change, evaluation framework)
- **Metrics**: Emphasizes cost-effectiveness comparisons to GiveWell top charities (bed nets, deworming, cash transfers)
- **PDF Format**: Optimized for grant portal uploads (US Letter, 1-inch margins, embedded fonts, numbered sections)

**Cross-Links:**
- Grant proposal HTML site includes links back to main book for detailed exploration
- Main book doesn't link to grant proposal (grant proposal is standalone for foundation distribution)
- Links in PDF are maintained as absolute URLs for accessibility

### Foundation-Specific Variables

The `_variables-foundation-manual-DO-NOT-DELETE.yml` file provides 80+ pre-formatted variables designed for grant proposals:

**Quick Reference Snippets:**
- `foundation_summary_50_words`: Elevator pitch for grant forms
- `foundation_summary_100_words`: Brief executive summary
- `foundation_summary_250_words`: Extended summary with problem/solution/impact

**Cost-Effectiveness Metrics:**
- `foundation_cost_per_daly_headline`: "$0.84 per DALY averted"
- `foundation_campaign_leverage`: "2,659× annual leverage"
- `foundation_campaign_roi_simple`: "542× return on investment"
- `foundation_lives_per_dollar`: "1 life saved per $97"

**Comparison Benchmarks:**
- `foundation_comparison_bed_nets`: "Bed nets: $89/DALY | 105× less efficient"
- `foundation_comparison_deworming`: "Deworming: $100-300/DALY | 119-357× less efficient"
- `foundation_comparison_vitamin_a`: "Vitamin A: $15-25/DALY | 18-30× less efficient"

**Theory of Change:**
- `foundation_toc_inputs`: Campaign funding, staff, partnerships, technology
- `foundation_toc_activities`: Lobbying, referendums, public education
- `foundation_toc_outputs`: Voter commitments, policy support, treaty ratification
- `foundation_toc_outcomes`: Funding stream, trials launched, cost reduction
- `foundation_toc_impact`: Lives saved, DALYs averted, economic value

**Risk Summaries:**
- `foundation_risk_political`: Political risk assessment and mitigation
- `foundation_risk_implementation`: Implementation risk and proven model
- `foundation_risk_financial`: Financial risk and VICTORY Bond structure
- `foundation_risk_timeline`: Timeline risk and multi-path strategy

**Evidence Base:**
- `foundation_evidence_ottawa`: Ottawa Treaty precedent (133 nations, <$50M budget)
- `foundation_evidence_recovery`: RECOVERY trial (15K patients, $500/patient, 1M lives saved)
- `foundation_evidence_smallpox`: Smallpox eradication precedent
- `foundation_evidence_academic`: 500+ peer-reviewed citations

**Use in QMD files:**
```markdown
{{< var foundation_pitch >}}
{{< var foundation_cost_per_daly_headline >}}
{{< var foundation_evidence_recovery >}}
```

### PDF Output Optimization

The foundation grant proposal PDF is optimized for grant portal uploads:

**Format Settings:**
- **Paper**: US Letter (8.5" × 11")
- **Margins**: 1 inch all sides (standard for grant portals)
- **Font**: 11pt with embedded fonts (ensures consistent rendering)
- **Spacing**: 1.5 line spacing (professional formatting)
- **Sections**: Numbered sections (typical for grant proposals)
- **TOC**: 3-level table of contents
- **Headers/Footers**: Organization name, page numbers

**Validation:**
The render script automatically validates the PDF:
- Checks for Python code leakage (ensures no implementation details exposed)
- Verifies all fonts are embedded
- Confirms proper section numbering
- Validates internal cross-references

### NPM Scripts for Foundation Proposal

While not currently in `package.json`, you can add these for convenience:

```json
{
  "scripts": {
    "render:foundation": "python scripts/render-quarto.py foundation",
    "render:foundation:pdf": "python scripts/render-quarto.py foundation --to pdf --verify",
    "preview:foundation": "python scripts/render-quarto.py foundation --preview"
  }
}
```

### Troubleshooting

**Issue**: Variables not updating in grant proposal
- **Solution**: Run `python scripts/generate-everything-parameters-variables-calculations-references.py` to regenerate all variables

**Issue**: Cross-links broken in PDF
- **Solution**: Ensure target files are listed in `_quarto-foundation.yml` chapters, use `.qmd` extensions for internal links

**Issue**: PDF render fails
- **Solution**: Check `build-foundation.log` for LaTeX errors, ensure Python virtual environment is activated

**Issue**: Grant proposal includes outdated metrics
- **Solution**: Verify `_variables-foundation.yml` is up-to-date, regenerate with generate script

**Issue**: Need foundation-specific version
- **Solution**: Edit `_variables-foundation-manual-DO-NOT-DELETE.yml`, add foundation name to filename for tracking (e.g., `_variables-gates-foundation.yml`)

## Content Standards

**See `CONTRIBUTING.md` for complete writing guidelines, style requirements, and content standards.**

Please render and critically review output images of quarto files whenever you modify figure-generating files. 