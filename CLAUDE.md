## Project Overview

This is a Quarto-based book project: "The Complete Idiot's Guide to Ending War and Disease" - a guide to getting nations to sign the 1% Treaty, redirecting military spending to the Decentralized Institutes of Health and Decentralized FDA to automate ubiquitous clinical trials. 

**Key Navigation:**

- **`todo.md`**: Master task list and current priorities for book completion
- **`OUTLINE.md`**: Complete book outline (comprehensive writing checklist)
- **`index.qmd`**: Book introduction and overview (landing page)
- **`_book.yml`**: Book configuration, chapter order, and output formats
- **`package.json`**: Node.js dependencies and npm scripts

**Important:** Use `tsx` (not ts-node) to run TypeScript files. Example: `npx tsx scripts/review/review.ts`

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
   .venv/Scripts/python.exe scripts/generate-variables-yml.py
   ```

3. **Use in QMD files** (formatter handles all formatting):
   ```markdown
   Foundation funding: {{< var foundation_funding_realistic >}}
   ```
   Output: "Foundation funding: $519M" (with HTML tooltip and source link)

### Parameter Naming Rules

**CRITICAL: These rules apply to ALL numeric parameters (currency, deaths, DALYs, etc.)**

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

### LaTeX Math Block Limitation

**CRITICAL: Quarto variables do NOT work inside LaTeX math blocks (`$$`).**

❌ **Wrong** (variables won't render in LaTeX):
```markdown
$$
\${{< var global_annual_war_total_cost >}} \times {{< var treaty_reduction_pct >}}
$$
```

✅ **Correct** (hardcode values in LaTeX):
```markdown
$$
\$11{,}355\text{B} \times 1\% = \$113.55\text{B}
$$
```

**Why**: LaTeX equations are processed separately from Quarto shortcodes. Variables must be hardcoded in math blocks. Document the source of hardcoded values in nearby text using variables.

### Why This Matters

- **Single source of truth**: All values come from parameters.py
- **Automatic tooltips**: Hover shows source, confidence, formula
- **Consistency**: Same value displayed identically everywhere
- **Zero maintenance**: Change parameter once, regenerates everywhere
- **Academic rigor**: Auto-generates parameters-and-calculations.qmd appendix

## Content Standards

**See `CONTRIBUTING.md` for complete writing guidelines, style requirements, and content standards.**

Please render and critically review output images of quarto files whenever you modify figure-generating files. 