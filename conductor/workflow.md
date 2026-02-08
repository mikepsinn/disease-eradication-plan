# Project Workflow

## Guiding Principles
1. **The Plan is the Source of Truth:** All work must be tracked in `plan.md`.
2. **Content First:** Focus on high-quality, evidence-based content in `.qmd` files.
3. **Verify Renders:** Always verify that changes render correctly to both PDF and HTML.
4. **Reproducibility:** Ensure all calculations and data sources are documented and reproducible.

## Task Workflow

1. **Select Task:** Choose the next task from `plan.md`.
2. **Mark In Progress:** Update `plan.md` to `[~]`.
3. **Edit Content/Code:** Modify `.qmd` files, scripts, or assets.
4. **Preview & Render:**
   - Use `npm run preview:<document>` to check changes interactively.
   - Use `npm run render:<document>` to build the final artifacts.
5. **Verify:**
   - Check generated PDF and HTML for formatting issues.
   - Ensure citations and cross-references resolve.
   - Run `npm run validate:all` to check for common errors.
6. **Commit:**
   - Stage changes.
   - Commit with a clear message (e.g., `content(chapter): Update introduction statistics` or `fix(build): Correct LaTeX error`).
7. **Update Plan:** Mark task as `[x]` in `plan.md`.

## Key Commands

### Rendering & Preview
- **Manual:** `npm run preview:manual` / `npm run render:manual`
- **Treaty Impact:** `npm run preview:1-pct-treaty-impact` / `npm run render:1-pct-treaty-impact`
- **Wishocracy:** `npm run preview:wishocracy` / `npm run render:wishocracy`

### Validation
- **Validate All:** `npm run validate:all` (Frontmatter, LaTeX, Render, Lint)
- **Fix Common Issues:** `npm run fix:all`

## Definition of Done
A task is complete when:
1. Content is written/updated.
2. Project renders successfully (PDF & HTML).
3. No validation errors (`npm run validate:all` passes).
4. Changes are committed.
5. `plan.md` is updated.