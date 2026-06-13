# Project Workflow

## Guiding Principles
1. **The Plan is the Source of Truth:** All work must be tracked in `plan.md`.
2. **Content First:** Focus on high-quality, evidence-based content in `.qmd` files.
3. **Verify Renders:** Always verify that changes render correctly to both PDF and HTML.
4. **Reproducibility:** Ensure all calculations and data sources are documented and reproducible.
5. **No Em-Dashes:** Replace with parenthesis, comma and space (", "), period, or semicolon.

## Task Workflow

1. **Select Task:** Choose the next task from `plan.md`.
2. **Mark In Progress:** Update `plan.md` to `[~]`.
3. **Execute:**
   - Modify `.qmd` files, scripts, or assets.
   - Use `{{< var param_name >}}` for all numeric values.
   - Use `[@citation_key]` for all claims.
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
   - **NEVER commit unless validation checks pass.**
7. **Update Plan:** Mark task as `[x]` in `plan.md`.

## Key Commands

### Rendering & Preview
The project uses `scripts/render-quarto.py` for all builds.

- **Manual:** `npm run preview:manual` / `npm run render:manual`
- **Treaty Impact:** `npm run preview:1-pct-treaty-impact` / `npm run render:1-pct-treaty-impact`
- **Wishocracy:** `npm run preview:wishocracy` / `npm run render:wishocracy`
- **Custom Config:** `python scripts/render-quarto.py <config_name> --to html --preview`

### Validation & Review
The project employs a multi-stage validation pipeline:

- **Pre-Render (Static Analysis):** `npm run validate:pre-render`
  *Checks for LaTeX errors, broken links, missing images.*
- **Post-Render (HTML Inspection):** `npm run validate:post-render`
  *Checks for unrendered code, broken internal links.*
- **Review Content:** `npx tsx scripts/review/run-checks.ts knowledge/file.qmd --checks fact,link`
- **Apply Global Fixes:** `npx tsx scripts/review/apply-instruction-all-files.ts "Instruction"`
- **Validate All:** `npm run validate:all` (Frontmatter, LaTeX, Render, Lint)

### Autonomous PDF Perfection + Upload
- **Single pass uploader:** `python scripts/upload-all-zenodo-and-save-dois.py --llm-pages 0`
- **Autonomous fix loop:** `python scripts/autonomous-perfect-and-upload.py --llm-pages 0 --max-cycles 20`
- **Paper-scoped run:** `python scripts/upload-all-zenodo-and-save-dois.py <paper-key> --force-reprocess --force-revalidate --llm-pages 0`

Operational notes:
- LLM validation is required before upload.
- The uploader is fail-fast: first blocking paper stops the run.
- Report output is written to `zenodo-upload-report.md` with a fix checklist.
- Autonomous progress is appended to `AUTONOMOUS-PIPELINE-STATUS.md`.
- Live command output is appended to `AUTONOMOUS-PIPELINE-PROGRESS.log`.
- Per-command cycle logs are written to `AUTONOMOUS-PIPELINE-LOGS/`.
- Do not commit inside autonomous loops.

### Data Pipeline
To regenerate all derived artifacts (variables, citations, charts):
- **Command:** `npm run generate:everything`
- **Script:** `scripts/generate-everything-parameters-variables-calculations-references.py`
- **Audit Params:** `npx tsx scripts/parameter-audit.ts PARAM_NAME`

## Parameter Workflow

1. **Check Existing:** `grep "keyword" _variables.yml`
2. **Define:** Add to `dih_models/parameters.py` using `Parameter()` class.
   ```python
   FOUNDATION_FUNDING_REALISTIC = Parameter(
       519_000_000, unit="USD",
       source_ref="/knowledge/appendix/campaign-financing-roadmap.qmd#...",
       description="Nonprofit foundation funding in realistic scenario"
   )
   ```
3. **Generate:** Run `npm run generate:everything`.
4. **Use:** Insert `{{< var foundation_funding_realistic >}}` in `.qmd` files.

## Citation Workflow

1. **WebSearch:** Find authoritative source URL.
2. **WebFetch:** Verify content matches claim.
3. **Edit BibTeX:** Add entry to `references.bib` with `url` and `urldate`.
4. **Quote:** Include relevant text in the `abstract` field of the BibTeX entry.
5. **Cite:** Use `[@key]` in content.

## Definition of Done
A task is complete when:
1. Content is written/updated.
2. Project renders successfully (PDF & HTML).
3. No validation errors (`npm run validate:all` passes).
4. Changes are committed.
5. `plan.md` is updated.
