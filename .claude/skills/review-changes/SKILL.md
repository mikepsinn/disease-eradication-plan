---
name: review-changes
description: Reviews uncommitted git changes for errors, inconsistencies, and problems. Use before committing to catch issues.
allowed-tools: all
---

# Review Uncommitted Changes

Reviews all uncommitted git changes (staged + unstaged + untracked) for errors and inconsistencies before committing.

**This is a review-only skill. Do NOT auto-fix anything.** Present findings and let the user decide what to fix.

## Process

### 1. Gather all changes

```bash
cd E:\code\obsidian\websites\disease-eradication-plan

# Staged changes
git diff --cached --name-status

# Unstaged changes
git diff --name-status

# Untracked files
git status --porcelain
```

Also run `git diff` and `git diff --cached` (without `--name-status`) to see the actual line-level changes for review.

### 2. Categorize changed files

Group every changed file into one of these categories:

| Category | File Patterns |
|----------|--------------|
| Parameters | `dih_models/parameters.py` |
| Variables YAML | `_variables.yml` |
| QMD content | `knowledge/**/*.qmd`, `index.qmd` |
| Quarto config | `_quarto*.yml`, `_book.yml` |
| Project config | `CLAUDE.md`, `OUTLINE.md`, `todo.md` |
| Python scripts | `scripts/**/*.py` |
| TypeScript scripts | `scripts/**/*.ts` |
| Generated figures | `knowledge/figures/*.qmd` |
| Generated analysis | `_analysis/*`, `dih_models/parameters-calculations-citations.ts`, `dih_models/reference_ids.py` |
| Assets | `assets/**/*` |
| Other | Everything else |

### 3. Review each category

#### Parameters (`dih_models/parameters.py`)

- Read the diff. For each added/modified parameter check:
  - Name follows `SCOPE_METRIC_MODIFIERS` convention (all caps, underscores)
  - Has required fields: value, `unit`, `description`
  - `unit` reads naturally in prose (not `"count"`)
  - Calculated parameters use formulas, not hardcoded values
  - `source_type` is set correctly: `"external"`, `"calculated"`, or `"definition"`
  - Constitutional constants use `distribution="fixed"`
  - Raw values stored (not pre-scaled like `519` for millions)
  - No duplicate names (grep for the parameter name)

#### Variables YAML (`_variables.yml`)

- If `parameters.py` was also changed, check: were variables regenerated?
  - Look for corresponding new entries in `_variables.yml` for new parameters
  - If parameters changed but `_variables.yml` didn't, flag as **error**: "Variables not regenerated after parameter changes"

#### QMD content files

For each changed QMD, read the diff and check:
- **Variable references**: Every `{{< var NAME >}}` must exist in `_variables.yml`. Grep to verify.
- **Cross-references**: Links like `[text](../path/to/file.qmd)` must point to existing files
- **Em-dashes**: Flag any `---` used as em-dashes (the project bans em-dashes)
- **LaTeX blocks**: No `{{< var >}}` inside `$$` blocks (Quarto variables don't work there)
- **Link extensions**: Internal links must use `.qmd` not `.html`
- **Variables inside links**: `[{{< var x >}}](url)` is wrong (variables have built-in links)
- **Citation keys**: Every `@citation_key` should exist in `references.bib`
- **Redundancy in changed sections**: Read the full changed file (not just the diff) and check for:
  - Repeated paragraphs or sentences that say the same thing in different words
  - The same statistic or claim stated multiple times in the file
  - Sections that substantially overlap and could be merged
  - Equations or LaTeX blocks that duplicate what a `_latex` variable already provides
  - Boilerplate or filler text that adds no information
  Flag redundancies as **warning** with the duplicated content locations and a suggestion for which instance to keep or how to merge

#### Quarto config (`_quarto*.yml`, `_book.yml`)

- Valid YAML syntax
- Chapter paths point to existing files
- No duplicate chapter entries

#### Project config (`CLAUDE.md`, `OUTLINE.md`)

- No contradictions with existing documented rules
- Formatting is consistent

#### Python scripts

- UTF-8 encoding header present (check for `sys.stdout.reconfigure(encoding='utf-8')` on Windows)
- Valid Python syntax: `python -c "import ast; ast.parse(open('FILE').read())"`
- No bare `try/except` blocks (project rule: let errors crash loudly)

#### TypeScript scripts

- Valid syntax (check for obvious issues in diff)

#### Generated files (figures/, _analysis/, parameters-calculations-citations.ts, reference_ids.py)

- **Do NOT review content** of auto-generated files
- Only check: if `parameters.py` changed, were these regenerated too?
- If generated files are in the diff but parameters.py is NOT, flag as **warning**: "Generated files appear to be manually edited"

### 4. Deletion review

For every deleted file (D in `git status`), check:

- **Was it replaced?** Look for a new file serving the same purpose (renamed, restructured). If a clear replacement exists, note it as info.
- **Dangling references?** Grep all QMD and YAML files for the deleted filename or its stem. Flag remaining references as **errors**.
- **Content loss?** For deleted content files (not auto-generated), read the deleted content with `git show HEAD:path/to/file` and assess whether the information was moved elsewhere or truly removed. Flag substantive content deletion without replacement as a **warning**.
- **Deleted parameters**: If parameters were removed from `parameters.py`, check whether the analysis they supported was also removed or restructured. Flag orphaned analysis sections that reference deleted parameters.

For large line removals within modified files (visible in `git diff`), check:
- Was removed content moved to another file, or was it genuinely cut?
- If a section was deleted, does the surrounding text still flow logically?
- Were removed citations/references still needed by other sections?

### 5. Duplicate detection

#### Duplicate parameters (`dih_models/parameters.py`)

Check the **full file** (not just the diff) for parameters that overlap or could be merged:

```bash
# Find all parameter names
grep -n "^[A-Z_]* = Parameter(" dih_models/parameters.py
```

Look for:
- **Identical names** (Python would silently overwrite the first)
- **Near-duplicate names** that likely measure the same thing (e.g., `GLOBAL_WAR_COST` vs `GLOBAL_ANNUAL_WAR_TOTAL_COST`)
- **Same value, different names** -- two parameters with the same numeric value and unit that could be consolidated
- **Overlapping scope** -- parameters whose descriptions suggest they cover the same concept from different angles

Flag duplicates as **warning** with both parameter names and their values.

#### Duplicate references (`references.bib`)

Check for duplicate or near-duplicate BibTeX entries:

```bash
# Find all citation keys
grep -n "^@" references.bib
```

Look for:
- **Identical citation keys** (BibTeX would use the last one silently)
- **Same URL in multiple entries** -- different keys pointing to the same source
- **Same title/author** with different keys (likely accidental duplicates)

Flag duplicates as **warning** with both entry keys and what they share.

### 6. Cross-file consistency checks

- **New parameters without variables**: Any new parameter in `parameters.py` should have a corresponding entry in `_variables.yml`
- **New QMD variable refs without parameters**: Any new `{{< var NAME >}}` in QMD diffs should reference an existing variable
- **Deleted parameters still referenced**: If a parameter was removed from `parameters.py`, grep all QMD files for its variable name
- **Citation additions**: New `@key` references in QMD should have matching entries in `references.bib`

### 7. Report findings and offer to fix

Present findings as a **numbered checklist** grouped by severity:

```
## Review of Uncommitted Changes

### Files Changed
- X modified, Y added, Z deleted

### Errors (must fix before commit)
1. [ ] description of error -- file:line
2. [ ] description of error -- file:line

### Warnings (should probably fix)
3. [ ] description of warning -- file:line
4. [ ] description of warning -- file:line

### Info (consider reviewing)
5. [ ] description -- file:line

### Auto-generated files
- Regenerated: yes/no (list which ones)

### Summary
X errors, Y warnings, Z info items
```

**After presenting the report**, use `AskUserQuestion` to ask:

> "Which items would you like me to fix? Select by number, or choose 'All errors', 'All errors + warnings', or 'None (just commit)'."

Options:
- "All errors" -- fix all error-severity items
- "All errors + warnings" -- fix errors and warnings
- "Pick specific items" -- user provides numbers
- "None" -- skip fixes

If the user selects items to fix, **enter plan mode** and create a fix plan covering only the selected items. Present the plan for approval before making any changes.

**Severity guide:**

| Severity | Criteria |
|----------|----------|
| Error | Will break render, wrong values, missing references, syntax errors, duplicates |
| Warning | Style violations, potential inconsistencies, missing regeneration, content loss |
| Info | Suggestions, minor style notes, things to double-check |

## Known Non-Issues (Do NOT Flag)

- **Hardcoded values in Quarto YAML config abstracts/descriptions** (`_quarto-*.yml`). These fields use hardcoded numbers instead of `{{< var >}}` references intentionally. Quarto variables don't render in YAML metadata consumed by search engines, social previews, and PDF front matter. The `yaml_sync_utils.py` script auto-syncs these values from `_variables.yml`, so they stay current without manual maintenance.
- **CRLF line ending warnings from git.** This is a Windows development environment. Git's `core.autocrlf` handles normalization. Ignore CRLF/LF warnings in git diff output.

## Important Rules

- **Read diffs, not full files** for most checks. Focus on what changed.
- **Full file scan for duplicates.** Duplicate detection (step 5) requires reading the full `parameters.py` and `references.bib`, not just diffs.
- **Skip auto-generated file content.** Only verify they were regenerated if parameters changed.
- **Do NOT fix anything during the review phase.** Report only. Fixes happen after user selects items.
- **Be specific.** Include file paths and line numbers for every finding.
- **Use parallel Task agents** for independent checks (e.g., checking multiple QMD files simultaneously).
