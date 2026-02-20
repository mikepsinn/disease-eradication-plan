# Zenodo Upload Report

**Date:** 2026-02-19 17:37:36
**Duration:** 628.2 seconds
**Papers Processed:** 15

## Summary

- **Successful:** 0
- **Failed:** 1
- **Skipped (already perfected/uploaded):** 0
- **Validation Skipped:** `False`

## Build Results

| Paper | Status | Duration | QMD Files | Pages | PDF Size |
|-------|--------|----------|-----------|-------|----------|
| opg | OK | 325.1s | 1 | 108 | 12.16 MB |
| political-dysfunction-tax | FAILED | 252.7s | 1 | 58 | 8.56 MB |

## Validation Results

| Paper | Status | Source | Notes | Error Count | Warning Count | AI Fix Log |
|-------|--------|--------|-------|-------------|---------------|------------|
| opg | OK | cache | cache hit | 0 | 0 | - |

## Upload Results

| Paper | Status | DOI | Deposit ID | URL | Notes |
|-------|--------|-----|------------|-----|-------|
| opg | OK | 10.5281/zenodo.18603834 | 18705718 | https://zenodo.org/record/18603834 | - |

## Errors and Warnings

### political-dysfunction-tax

- [17:48:05] [ERROR] Found 10 validation error(s):
- [ERROR] Post-validation failed
- Build failed with return code 1

## Autonomous Fix Checklist

### political-dysfunction-tax

- [ ] Resolve all issues listed below for this paper.
- [ ] [17:48:05] [ERROR] Found 10 validation error(s):
- [ ] [ERROR] Post-validation failed
- [ ] Build failed with return code 1
- [ ] Re-run this paper: `python scripts/upload-all-zenodo-and-save-dois.py political-dysfunction-tax`

### Agent Prompt

Use the checklist above as the source of truth.
After each fix, rerun only the failing paper command.
Continue until this report shows zero failed papers and no checklist items.

## Action Log

- [17:37:36] Selected 15 paper(s): opg, political-dysfunction-tax, cost-of-change, dfda-spec, iab, invisible-graveyard, obg, optimocracy, right-to-trial, us-efficiency-audit, wishocracy, dfda-impact, drug-development-cost, 1-pct-treaty-impact, manual-paperback
- [17:37:37] Configured with skip_validation=False, draft=False
- [17:43:05] Validated opg: passed (cache hit)
- [17:43:05] Uploading opg
- [17:43:51] Upload verified for opg: DOI 10.5281/zenodo.18603834
- [17:48:05] Build failed for political-dysfunction-tax

## Next Steps

1. Review the results above
2. Check drafts on Zenodo: https://zenodo.org/me/uploads
3. Review config changes: `git diff _quarto-*.yml`
4. Commit updates: `git add _quarto-*.yml && git commit -m 'update: Zenodo DOIs'`
