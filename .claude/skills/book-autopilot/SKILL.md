---
name: book-autopilot
description: Automated book maintenance. Runs health checks, prioritizes work, and systematically fixes issues. Use when you want Claude to autonomously improve the book.
allowed-tools:
  - Read
  - Edit
  - Write
  - Bash
  - Grep
  - Glob
  - Task
---

# /book-autopilot [mode]

Autonomous book maintenance system. Modes:
- `check` - Run health check, generate report (default)
- `fix` - Fix all issues systematically (CRITICAL → LOW)
- `chapter <name>` - Focus on single chapter
- `images` - Generate missing section images
- `params` - Audit and fix parameter issues
- `citations` - Find and add missing citations

---

## Mode: check (default)

Run comprehensive health check:

```bash
python scripts/book-health-check.py
```

Read the report and summarize top priorities:
```bash
cat _build_temp/book-health-report.md | head -100
```

---

## Mode: fix

### Step 1: Run Health Check

```bash
python scripts/book-health-check.py --json > _build_temp/health-issues.json
```

### Step 2: Process Issues by Priority

Read the JSON output and process issues in order:

1. **CRITICAL** - Must fix immediately
   - Missing variables → Add to parameters.py, regenerate
   - Broken critical links → Fix or remove

2. **HIGH** - Fix before next render
   - Missing citations → Use `/verify-and-add-sources`
   - Broken links → Update paths
   - Missing images → Use `/generate-section-images`

3. **MEDIUM** - Batch fix
   - Hardcoded values → Use `/replace-hardcoded-values`

4. **LOW** - Opportunistic
   - Stale content → Flag for manual review
   - Readability → Use `/peer-review`

### Step 3: Verify Fixes

```bash
python scripts/book-health-check.py --quick
```

---

## Mode: chapter <name>

Focus on a single chapter:

```bash
python scripts/book-health-check.py --chapter <name>
```

Then apply all relevant fixes to that chapter:
1. Read the chapter fully
2. Run `/replace-hardcoded-values` on it
3. Run `/peer-review` on it
4. Verify links and citations

---

## Mode: images

Generate missing section images:

```bash
npx tsx scripts/images/generate-section-images.ts --limit 5
```

Review generated images and regenerate any that need improvement.

---

## Mode: params

Parameter audit and fix:

1. Check for unused parameters:
```bash
python scripts/find-unused-parameters.py
```

2. Check for hardcoded values across all files:
```bash
npx tsx scripts/audit-hardcoded-all.ts
```

3. Regenerate variables:
```bash
python scripts/generate-everything-parameters-variables-calculations-references.py
```

---

## Mode: citations

Find claims without citations:

1. Search for statistical claims:
```bash
grep -rn "studies show\|research indicates\|according to" knowledge/ --include="*.qmd" | head -20
```

2. For each uncited claim, use `/verify-and-add-sources` to find and add proper citations.

---

## Continuous Maintenance Loop

For ongoing maintenance, run this sequence periodically:

1. `python scripts/book-health-check.py` - Find issues
2. Fix CRITICAL/HIGH issues immediately
3. Batch process MEDIUM issues
4. Track LOW issues in todo.md
5. Commit fixes with descriptive messages

---

## Progress Tracking

After each fix session, update progress:

```bash
# Count remaining issues
python scripts/book-health-check.py --json | python -c "import json,sys; d=json.load(sys.stdin); print(f'Remaining: {d[\"total_issues\"]} issues')"
```
