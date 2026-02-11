# Implementation Plan: Consolidate and Verify Build Scripts

## Phase 1: Audit and Baseline
- [ ] Task: Audit existing render scripts in `package.json` for consistency.
- [ ] Task: Run `npm run validate:all` and document any existing baseline errors.
- [ ] Task: Verify `npm run generate:everything` runs successfully.
- [ ] Task: Conductor - User Manual Verification 'Audit and Baseline' (Protocol in workflow.md)

## Phase 2: Verification of Primary Renders
- [ ] Task: Verify Manual render (`npm run render:manual`) and check PDF/HTML output.
- [ ] Task: Verify Treaty Impact render (`npm run render:1-pct-treaty-impact`) and check output.
- [ ] Task: Verify Audit render (`npm run render:us-efficiency-audit`) and check output.
- [ ] Task: Conductor - User Manual Verification 'Verification of Primary Renders' (Protocol in workflow.md)

## Phase 3: Validation Consolidation
- [ ] Task: Ensure `validate:all` includes MD/QMD linting.
- [ ] Task: Verify LaTeX validation script coverage for all academic papers.
- [ ] Task: Update documentation (README or a new BUILD.md) with the verified build sequence.
- [ ] Task: Conductor - User Manual Verification 'Validation Consolidation' (Protocol in workflow.md)
