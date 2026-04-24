---
name: pre-render-validate
description: Runs pre-render-validation.py and systematically fixes all detected errors. Use before rendering or committing to catch LaTeX, link, variable, citation, and import issues.
allowed-tools:
  - Read
  - Bash
  - Write
  - Edit
  - Grep
  - Glob
---

# Pre-Render Validation & Fix

## When to Use

Use this skill when you:
- Are about to render the Quarto book (HTML, PDF, or EPUB)
- Want to catch errors before committing changes
- See validation errors during Quarto render
- Need to fix multiple file issues systematically

## What It Validates

The pre-render-validation.py script checks for:

1. **LaTeX Syntax Errors**
   - Triple dollar signs ($$$)
   - Escaped double dollar signs (\\$$)
   - Unbalanced braces in \\underbrace{}
   - Malformed equation endings
   - Quarto variables inside math blocks (don't work)

2. **Missing/Broken References**
   - Image files not found
   - Broken cross-reference links to .qmd files
   - Broken anchor IDs (#section-id not in target)
   - Broken include directives
   - Unknown Quarto variables not in _variables.yml
   - Missing citations not in references.bib

3. **Python Code Block Issues**
   - Missing imports (numpy_financial, get_figure_output_path, etc.)
   - Parameter usage without importing from dih_models.parameters
   - Quarto variables in Graphviz code (don't work)
   - Hardcoded figure paths

4. **Format Compatibility Issues**
   - GIF files not wrapped in HTML-only blocks (breaks PDF)
   - Em-dashes (should use commas, periods, or semicolons)
   - Unclosed code blocks (``` without closing ```)
   - Figure files with YAML frontmatter

5. **Redundancy Detection**
   - Duplicate `_latex` variables (same equation used multiple times indicates redundancy)

## Process

### 1. Run validation script

```bash
cd E:\code\obsidian\websites\disease-eradication-plan
.venv/Scripts/python.exe scripts/pre-render-validation.py 2>&1
```

### 2. Parse and categorize errors

Errors are grouped by file and type. Common error patterns:

- `Em-dash (—) found` - Replace with appropriate punctuation
- `Unknown Quarto variable` - Add to parameters.py or fix typo
- `Missing citation` - Add to references.bib or fix citation key
- `Broken cross-reference link` - Fix path or create target file
- `Broken anchor link` - Fix anchor ID or add anchor to target
- `GIF file not wrapped` - Wrap in HTML-only block
- `Unclosed code block` - Add missing closing ```
- `Parameter 'X' used but not imported` - Add import statement
- `Quarto variable inside link text` - Remove link brackets (variables have built-in links)

### 3. Fix each error type

#### Em-dashes (—)
Read the context and replace with appropriate punctuation:
- Use comma and space (", ") for parenthetical phrases
- Use period for separate sentences
- Use semicolon for related independent clauses
- Use parentheses for clarifications

#### Unknown variables
1. Search _variables.yml for similar names (typo?)
2. If typo, fix the variable reference
3. If new value needed, add parameter to dih_models/parameters.py
4. Regenerate variables: `.venv/Scripts/python.exe scripts/generate-everything-parameters-variables-calculations-references.py`

#### Missing citations
1. Search references.bib for similar citation keys
2. If typo, fix the citation key
3. If new source needed, add BibTeX entry to references.bib

#### Broken links
1. Check if target file exists with different path
2. Fix the path if file exists elsewhere
3. If file should exist but doesn't, note for creation

#### Missing imports
Add the missing import to the Python code block:
```python
from dih_models.parameters import PARAMETER_NAME
```
or
```python
import numpy_financial as npf
```

#### GIF not in HTML block
Wrap GIF reference:
```markdown
::: {.content-visible when-format="html"}
<img src="path/to/file.gif" alt="Description" />
:::
```

#### Unclosed code blocks
Find the code block opening and add closing ```:
```markdown
```{python}
# code here
```  <-- Add this
```

#### Duplicate _latex variables
Having the same `_latex` variable multiple times indicates redundant LaTeX equations:
1. Read both occurrences in context
2. If truly redundant (same calculation shown twice), remove the duplicate
3. Keep the instance with better surrounding explanation
4. If both serve different purposes, they're likely not redundant (validation is a hint, not a rule)

#### Quarto variable inside link text
Variables have built-in links to their source, so wrapping them in additional links breaks rendering.

**Wrong:**
```markdown
[{{< var treaty_campaign_total_cost >}}](../economics/victory-bonds.qmd)
```

**Right** (variable alone, it has its own link):
```markdown
{{< var treaty_campaign_total_cost >}}
```

**Right** (if descriptive link text needed):
```markdown
{{< var treaty_campaign_total_cost >}} via [Victory Incentive Alignment Bonds](../economics/victory-bonds.qmd)
```

### 4. Re-run validation

After fixes, run validation again to confirm all errors resolved:

```bash
.venv/Scripts/python.exe scripts/pre-render-validation.py 2>&1
```

### 5. Report results

- Total errors found initially
- Errors fixed by type
- Any remaining errors requiring manual attention
- Recommendation to render book

## Error Priority

Fix in this order (highest impact first):

1. **Unclosed code blocks** - Breaks entire render
2. **Missing imports** - Causes Python execution failures
3. **Broken links** - Causes navigation failures
4. **Unknown variables** - Shows raw {{< var >}} in output
5. **Missing citations** - Shows [?] in output
6. **GIF wrapping** - Breaks PDF build only
7. **Duplicate _latex vars** - Redundancy hint, review needed
8. **Em-dashes** - Style issue, lowest priority

## Expected Outcome

After running this skill:
- Pre-render validation passes with no errors
- Book is ready to render: `quarto render`
- All cross-references resolve correctly
- All variables expand to values
- All citations link to sources

## Quick Commands

```bash
# Run validation only (see errors)
.venv/Scripts/python.exe scripts/pre-render-validation.py 2>&1

# Regenerate variables (fixes unknown variable errors if params exist)
.venv/Scripts/python.exe scripts/generate-everything-parameters-variables-calculations-references.py

# Render book after validation passes
quarto render
```
