# Quarto Render Validation

## Overview

The project includes automated validation to catch common rendering issues:

1. **Unrendered inline Python expressions** - Variables that show as literal `{python} var_name` instead of their values
2. **Cell option leaks** - When "echo: false" appears in the output
3. **Python errors** - Runtime errors in code cells

## Usage

### Manual Validation

Run validation on already-rendered output:

```bash
npm run validate:render
```

Or directly:

```bash
python scripts/validate_render.py
```

### Automatic Validation

The validation runs automatically after every `quarto render` via the post-render hook configured in `_quarto.yml`.

### Build with Validation

```bash
npm run build:validated
```

This cleans, renders, and validates in one step.

## Known Issues

### Inline Python in Markdown Lists

**Issue:** Inline Python expressions inside markdown list items render as literal code instead of evaluating.

**Example - Doesn't Work:**
```markdown
- Return: `{python} victory_bond_annual_return_pct_formatted`
- Investment: `{python} victory_bond_investment_unit_usd_formatted`
```

**Workaround Options:**

1. **Use paragraphs instead:**
   ```markdown
   **Return:** `{python} victory_bond_annual_return_pct_formatted`

   **Investment:** `{python} victory_bond_investment_unit_usd_formatted`
   ```

2. **Generate lists in Python:**
   ```python
   from IPython.display import Markdown

   list_md = f"""
   - Return: {victory_bond_annual_return_pct_formatted}
   - Investment: {victory_bond_investment_unit_usd_formatted}
   """
   Markdown(list_md)
   ```

3. **Hardcode values** (not recommended - defeats purpose of variables)

### Echo: False Leaks

**Issue:** Cell option appears in output when not using `#|` prefix.

**Wrong:**
```python
```{python}
echo: false
import sys
```
```

**Correct:**
```python
```{python}
#| echo: false
import sys
```
```

## Clearing Cached Computations

Quarto uses `freeze: auto` which caches computation results in `_freeze` and `.quarto/_freeze` directories.

If inline expressions aren't evaluating:

```bash
# Clear both freeze directories
rm -rf _freeze .quarto/_freeze

# Then re-render
quarto render
```

Or render with fresh execution:

```bash
quarto render --execute-daemon restart
```

## Integration with CI/CD

The validation script exits with code 1 if errors are found, making it suitable for CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Build and validate
  run: npm run build:validated
```

## Validation Script Details

**Location:** `scripts/validate_render.py`

**Checks:**
- `UNRENDERED_PYTHON` - Finds `<code>{python} ...</code>` patterns
- `ECHO_FALSE_LEAK` - Finds "echo: false" in visible output
- `PYTHON_ERROR` - Finds Python exception messages

**Options:**
```bash
# Specify custom output directory
python scripts/validate_render.py --output-dir _book/custom

# Treat warnings as errors
python scripts/validate_render.py --fail-on-warnings
```

## Fixing Issues

### Fix Inline Python Script

The `fix_inline_python.py` script was created to extract complex inline expressions and replace them with pre-formatted variables:

```bash
# Dry run (shows what would change)
npm run fix:inline-python:dry-run

# Actually make changes
npm run fix:inline-python
```

This script:
1. Scans all `.qmd` files for inline Python with function calls
2. Creates pre-formatted variables in `economic_parameters.py`
3. Replaces complex expressions with simple variable references

**However**, this doesn't solve the list item issue - those inline expressions still won't evaluate even after simplification.

### Hardcode List Values Script

The `hardcode_list_values.py` script replaces all inline Python expressions with their hardcoded values:

```bash
python scripts/hardcode_list_values.py
```

This script:
1. Dynamically loads all 384 formatted variables and constants from `economic_parameters.py`
2. Scans all `.qmd` files (in `brain/book/` and root directory)
3. Replaces all `` `{python} variable_name` `` with the actual hardcoded value
4. Skips code blocks and frontmatter

**Why hardcode everything?**

While inline Python expressions *should* work in paragraphs, we hardcode all expressions to:
- Ensure consistent rendering (no cache or execution issues)
- Faster build times (no Python evaluation needed)
- Guaranteed reliability in all contexts

**When to run:**

Run this script after updating values in `economic_parameters.py`:

```bash
python scripts/hardcode_list_values.py
npm run build:validated
```

Or add to your CI/CD workflow to auto-run when `economic_parameters.py` changes.
