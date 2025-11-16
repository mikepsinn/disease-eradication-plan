# Number Management Scripts

Automated tools for ensuring all numbers in documentation match calculations and are properly linked to sources.

## Quick Start

```bash
# Find unlinked numbers in your QMD files
python scripts/find-unlinked-numbers.py

# Check if hardcoded numbers match parameters.py
python scripts/validate-numbers.py

# Get suggestions for reference links
python scripts/suggest-links.py
```

## The Problem We Solve

**Before:** Numbers hardcoded in markdown, drift from calculations, break reader trust.

**After:** All numbers come from `dih_models/parameters.py` and auto-link to detailed sources.

## The Scripts

### `find-unlinked-numbers.py`

**Purpose:** Find numbers that aren't using inline Python or aren't linked to sources.

**Usage:**
```bash
# Scan all files
python scripts/find-unlinked-numbers.py

# Scan specific directory
python scripts/find-unlinked-numbers.py --path knowledge/economics

# JSON output
python scripts/find-unlinked-numbers.py --format json > unlinked.json
```

**Finds:**
- Money values: `$27.2B`, `$113.6 billion`
- Percentages: `1%`, `50.0%`
- Ratios: `463:1`, `1,239:1`
- Multipliers: `82x`, `115X`
- Large numbers: `1,000,000`

**Example output:**
```
📄 knowledge/economics/peace-dividend.qmd
   8 unlinked number(s)

   Line   23 | money        | $27.2B
              Context: The treaty redirects $27.2B annually

   Line   45 | ratio        | 463:1
              Context: This generates 463:1 returns
```

### `validate-numbers.py`

**Purpose:** Check that hardcoded numbers match calculated values in `parameters.py`.

**Usage:**
```bash
# Scan all files
python scripts/validate-numbers.py

# Scan specific directory
python scripts/validate-numbers.py --path knowledge/economics

# Generate JSON report
python scripts/validate-numbers.py --report mismatches.json
```

**Checks:**
- Does `$27.2B` match `TREATY_ANNUAL_FUNDING`?
- Does `463:1` match calculated ROI?
- Does `82x` match `TRIAL_COST_REDUCTION_FACTOR`?

**Example output:**
```
📄 knowledge/economics/economics.qmd
   15 number(s) that match parameters.py

   Line  142: $27.2B
              Matches: TREATY_ANNUAL_FUNDING
              Suggest: {python} treaty_annual_funding_linked
              Context: The treaty redirects $27.2B annually
```

### `suggest-links.py`

**Purpose:** Suggest appropriate reference links for numbers based on context.

**Usage:**
```bash
# Scan all files
python scripts/suggest-links.py

# Scan specific file
python scripts/suggest-links.py --file knowledge/economics/economics.qmd
```

**Suggests links based on:**
- Number value (matches known figures)
- Context keywords (military, trial, cost, etc.)
- Common sources (SIPRI, RECOVERY trial, GiveWell, etc.)

**Example output:**
```
📄 knowledge/economics/economics.qmd
   6 number(s) to link

   Line   67: $2.7T
              Reference: SIPRI 2024 Military Spending
              Replace with: [$2.7T](../references.qmd#sipri-2024-spending)
              Context: Global military spending totals $2.7T

   Line   89: 82x
              Reference: RECOVERY Trial Cost Reduction
              Replace with: [82x](../appendix/recovery-trial.qmd)
              Context: Trials cost 82x less using pragmatic methods
```

## The Solution: Auto-Linked Parameters

Instead of manually managing numbers and links, use the auto-linking system in `parameters.py`:

**Before (manual):**
```markdown
The treaty redirects [$27.2B annually](../appendix/peace-dividend-calculations.qmd).
```

**After (auto-linked):**
```markdown
The treaty redirects `{python} treaty_annual_funding_linked`.
```

**Benefits:**
- ✅ Number always matches calculation
- ✅ Link always points to correct source
- ✅ Single source of truth
- ✅ Zero maintenance

## How It Works

### 1. Parameters defined in `dih_models/parameters.py`

```python
# Raw calculation
TREATY_ANNUAL_FUNDING = 27.18e9

# Formatted for display
treaty_annual_funding_formatted = "$27.2B"

# Auto-linked (value + source)
treaty_annual_funding_linked = param_link('treaty_annual_funding', treaty_annual_funding_formatted)
# Returns: "[$27.2B](../appendix/peace-dividend-calculations.qmd)"
```

### 2. Link registry maps params to sources

```python
PARAMETER_LINKS = {
    'treaty_annual_funding': '../appendix/peace-dividend-calculations.qmd',
    'roi_conservative': '../appendix/dfda-cost-benefit-analysis.qmd',
    'global_military_spending': '../references.qmd#sipri-2024-spending',
}
```

### 3. Scripts validate everything stays in sync

```bash
python scripts/validate-numbers.py
# ✅ All numbers match calculations
```

## Workflow

### When Writing Content

1. **Use auto-linked parameters:**
   ```markdown
   The cost is `{python} parameter_name_linked`.
   ```

2. **Check what's available:**
   ```python
   from dih_models.parameters import PARAMETER_LINKS
   print(PARAMETER_LINKS.keys())
   ```

3. **Add new parameters as needed:**
   See [NUMBER_MANAGEMENT.md](../docs/NUMBER_MANAGEMENT.md#how-to-add-new-auto-linked-parameters)

### Before Committing

1. **Find unlinked numbers:**
   ```bash
   python scripts/find-unlinked-numbers.py
   ```

2. **Validate against calculations:**
   ```bash
   python scripts/validate-numbers.py
   ```

3. **Fix any issues** (replace hardcoded numbers with `{python}` references)

### Automated (CI/CD)

```yaml
# In .github/workflows/validate.yml
- name: Validate numbers
  run: |
    python scripts/validate-numbers.py --strict
    # Fails build if discrepancies found
```

## Common Use Cases

### Finding Mistakes

**Q: Did I hardcode a number that should come from parameters.py?**
```bash
python scripts/validate-numbers.py
```

**Q: Which numbers need links to sources?**
```bash
python scripts/find-unlinked-numbers.py
```

**Q: What source should I link this number to?**
```bash
python scripts/suggest-links.py
```

### Migration

**Q: I have 50 files with hardcoded numbers. How do I migrate?**

1. Run `find-unlinked-numbers.py` to see scope
2. Run `validate-numbers.py` to find parameters.py matches
3. Replace hardcoded with `{python} parameter_linked`
4. For non-calculated numbers, use `suggest-links.py`

**Q: How do I know if I'm done?**
```bash
python scripts/find-unlinked-numbers.py
python scripts/validate-numbers.py
# Should show minimal/zero issues
```

## Documentation

- **[NUMBER_SYSTEM_OVERVIEW.md](../docs/NUMBER_SYSTEM_OVERVIEW.md)** - Complete system documentation
- **[NUMBER_MANAGEMENT.md](../docs/NUMBER_MANAGEMENT.md)** - Best practices guide
- **[NUMBER_LINKING_QUICKSTART.md](../docs/NUMBER_LINKING_QUICKSTART.md)** - Quick reference

## Examples

### Example 1: Finding Unlinked Money Values

```bash
$ python scripts/find-unlinked-numbers.py --path knowledge/economics

📄 knowledge/economics/peace-dividend.qmd
   3 unlinked number(s)

   Line   23 | money | $27.2B
              Context: DIH gets $27.2B/year

   Line   24 | money | $113.6B
              Context: World saves $113.6B/year

   Line   67 | money | $2.7T
              Context: Governments spend $2.7T yearly
```

**Fix:**
```markdown
- DIH gets `{python} treaty_annual_funding_linked`
- World saves `{python} peace_dividend_annual_linked`
- Governments spend `{python} global_military_spending_linked`
```

### Example 2: Validating ROI Numbers

```bash
$ python scripts/validate-numbers.py

📄 knowledge/economics/economics.qmd
   2 number(s) that match parameters.py

   Line   89: 463:1
              Matches: ROI_CONSERVATIVE
              Suggest: {python} roi_conservative_linked

   Line  237: 1,239:1
              Matches: ROI_COMPLETE
              Suggest: {python} roi_complete_linked
```

**Fix:**
```markdown
- Conservative returns: `{python} roi_conservative_linked`
- Complete returns: `{python} roi_complete_linked`
```

### Example 3: Getting Source Suggestions

```bash
$ python scripts/suggest-links.py --file knowledge/economics/economics.qmd

📄 knowledge/economics/economics.qmd
   4 number(s) to link

   Line  116: $2.7T
              Reference: SIPRI 2024 Military Spending
              Replace with: [$2.7T](../references.qmd#sipri-2024-spending)

   Line  194: 82x
              Reference: RECOVERY Trial Cost Reduction
              Replace with: [82x](../appendix/recovery-trial.qmd)
```

## Troubleshooting

### "No module named 'dih_models'"

**Fix:** Run from project root:
```bash
cd /path/to/decentralized-institutes-of-health
python scripts/validate-numbers.py
```

### "Couldn't match number to parameter"

Numbers might be:
1. Not in parameters.py yet (add it)
2. From external source (use manual link)
3. Illustrative/example (leave unlinked)

### "Too many false positives"

The scripts are sensitive by design. Review each finding:
- Real issue → Fix it
- False positive → Add to script's skip patterns

## Contributing

### Adding New Detection Patterns

Edit the regex patterns in each script:
- `MONEY_PATTERN` for currency values
- `RATIO_PATTERN` for X:1 ratios
- `MULTIPLIER_PATTERN` for Xx values

### Adding New Reference Sources

Edit `REFERENCE_SOURCES` in `suggest-links.py`:
```python
ReferenceSource(
    name="New Source",
    anchor="new-source-anchor",
    typical_values=[123, 456],
    keywords=['keyword1', 'keyword2'],
    units='money'
)
```

## License

Same as main project (CC BY 4.0)
