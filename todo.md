# Pre-Publication Cleanup Checklist

**Goal:** Prepare "The Complete Idiot's Guide to Ending War and Disease" for public release

## Critical Issues (Must Fix First)

- [ ] Resolve git merge conflicts in files with MM status
  - [ ] brain/book/appendix/1-percent-treaty-roi-tiers.qmd
  - [ ] brain/book/appendix/economic_parameters.py
- [ ] Handle untracked files (commit or delete)
  - [ ] scripts/review/fix-missing-pct-rename.ts
  - [ ] scripts/review/rename-ambiguous-variables-phase-4.ts

## Automated Fixes

- [ ] Run frontmatter fixes: `npm run fix:frontmatter:issues`
- [ ] Run markdown linting fixes: `npm run lint:md:fix && npm run lint:qmd:fix`
- [ ] Fix spacing issues: `npm run format:spacing`
- [ ] Apply programmatic formatting to all files: `npm run format:programmatic:all`
- [ ] Apply auto-standards to all files: `npm run standards:apply:all`

##  Validation & Quality Checks

- [ ] Validate frontmatter: `npm run validate:frontmatter`
- [ ] Check all internal/external links: `npm run link-check:all`
- [ ] Verify figure references: `npm run figure-check:all`
- [ ] Check economic parameter consistency: `npm run param-check:all`
- [ ] Structure check all files: `npm run structure-check:all`
- [ ] Style guide compliance: `npm run style:all`
- [ ] Fact-check claims: `npm run fact-check:all`

## <� Build Testing

- [ ] Clean build environment: `npm run clean`
- [ ] Test HTML build: `npm run build:html`
- [ ] Test PDF build: `npm run build:pdf`
- [ ] Test presentation build: `npm run build:presentation`
- [ ] Preview book locally: `npm run preview:book`

## Content Review

- [ ] Compare OUTLINE.md against actual files for missing sections
- [ ] Find and replace TODO markers in content
- [ ] Replace [FIGURE: ...] placeholders with actual figures
- [ ] Verify all economic values reference economic_parameters.py
- [ ] Check references.qmd for completeness
- [ ] Verify all citations resolve correctly

## Visual Assets

- [ ] Test render all figure files in brain/figures/
- [ ] Verify all PNG files are committed and accessible
- [ ] Check figure captions for clarity
- [ ] Verify Mermaid diagrams render properly
- [ ] Add alt text for accessibility

## Style Guide Compliance

- [ ] Remove corporate buzzwords (synergy, paradigm shift, stakeholder, utilize)
- [ ] Remove selling language (we're going to, our solution will, join us)
- [ ] Remove cliches (let that sink in, think about that)
- [ ] Convert passive to active voice
- [ ] Ensure instructional framing (Here's how you...)

## � Legal & Disclaimers

- [ ] Add investment disclaimer for VICTORY Bonds section
- [ ] Add medical disclaimer (not medical advice)
- [ ] Add forward-looking statements disclaimer
- [ ] Verify attribution for third-party data/images

## Metadata & SEO

- [ ] Check frontmatter in all key files
- [ ] Verify titles, descriptions, tags
- [ ] Set publication dates
- [ ] Configure social media preview images

## Final Pre-Publication

- [ ] Manual proofread of introduction
- [ ] Test call-to-action links
- [ ] Check navigation between chapters
- [ ] Test mobile/responsive rendering
- [ ] Have fresh eyes read key sections
- [ ] Create git tag: `v1.0-prepublish`

## Status

**Started:** TBD
**Target Completion:** TBD
**Current Phase:** Critical Issues

---

*This checklist is auto-generated. Update as tasks are completed.*
