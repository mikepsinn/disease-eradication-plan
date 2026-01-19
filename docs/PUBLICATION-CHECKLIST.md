# Publication Checklist - Quick Reference

Complete publication tracking system for all papers and the book.

## Files Created

| File | Purpose |
|------|---------|
| `publication-tracking-schema.yml` | Complete YAML schema reference |
| `PUBLICATION-TRACKING-GUIDE.md` | Comprehensive implementation guide |

**Publishing sections added to:**
- `_quarto-economics.yml` (Economics paper)
- `_quarto-iab.yml` (IAB paper)
- `_quarto-wishocracy.yml` (Wishocracy paper)
- `_quarto-dfda-spec.yml` (dFDA methodology)
- `_quarto-dfda-impact.yml` (dFDA ROI/impact)

## Quick Start

### 1. Publishing is Already in Quarto Configs ✓

Each `_quarto-*.yml` file now has a `publishing:` section under `metadata:` with:
- Own site URL and status
- Top 3 journal targets
- Preprint server configurations
- URL placeholders for when published

### 2. Top Journal Targets by Paper

#### Economics Paper (1% Treaty)
**Top 3 Targets:**
1. Health Affairs (impact factor: 7.5) - Premier health policy journal
2. Value in Health (IF: 5.9) - ISPOR health economics journal
3. The Lancet (IF: 202.7) - Commentary/viewpoint piece

**Preprints:** SSRN (Health Economics), arXiv (econ.GN), medRxiv

#### IAB Paper
**Top 3 Targets:**
1. American Economic Review (IF: 10.7) - Top economics, competitive
2. Public Choice (IF: 1.3) - PERFECT FIT for public choice theory
3. Journal of Political Economy (IF: 9.3) - Political economy

**Preprints:** SSRN (Political Economy), arXiv (econ.GN or cs.GT)

#### Wishocracy Paper
**Top 3 Targets:**
1. Social Choice and Welfare (IF: 0.9) - PERFECT FIT for voting theory
2. Public Choice (IF: 1.3) - Collective decision-making
3. American Political Science Review (IF: 5.7) - Top political science

**Preprints:** SSRN (Political Science), arXiv (cs.GT)

#### dFDA Spec Paper (Methodology)
**Top 3 Targets:**
1. Clinical Pharmacology & Therapeutics (IF: 6.3) - EXCELLENT FIT
2. Pharmacoepidemiology and Drug Safety (IF: 3.4) - PERFECT FIT
3. Drug Safety (IF: 4.6) - Pharmacovigilance methodology

**Preprints:** medRxiv, arXiv (stat.ME), SSRN (Health Economics)

#### dFDA Impact Paper (ROI)
**Top 3 Targets:**
1. Value in Health (IF: 5.9) - EXCELLENT FIT for ROI/cost-benefit
2. Health Affairs (IF: 7.5) - Health policy, broader reach
3. PharmacoEconomics (IF: 4.4) - Pharmaceutical economics

**Preprints:** SSRN (Health Economics), medRxiv, arXiv (econ.GN)

#### Main Book
**Top Platforms:**
1. Amazon KDP (Kindle + paperback) - Largest reach
2. IngramSpark (print-on-demand) - Bookstore distribution
3. Draft2Digital (aggregator) - Apple, Kobo, B&N, libraries
4. Own website (free HTML) - Maximum reach ✓ Already live

## Publication Workflow

### Phase 1: Own Website ✓ DONE
All sites deployed via GitHub Actions to Netlify.

### Phase 2: Preprints (Week 1-2)
```yaml
☐ Review Zenodo drafts at https://zenodo.org/me/uploads
☐ Publish Zenodo drafts to get DOIs
☐ Upload to SSRN (manual)
☐ Upload to arXiv (manual, requires endorsement)
☐ Upload to medRxiv (for health papers, manual)
☐ Update URLs and DOIs in YAML files
```

### Phase 3: Academic Networks (Week 2-3)
```yaml
☐ Upload PDFs to ResearchGate
☐ Upload PDFs to Academia.edu
☐ Wait for Google Scholar auto-indexing
☐ Update profile URLs in YAML
```

### Phase 4: Journal Submissions (Week 3+)
```yaml
☐ Submit economics paper to Health Affairs
☐ Submit IAB paper to Public Choice
☐ Submit Wishocracy to Social Choice and Welfare
☐ Submit dFDA-spec to Clinical Pharmacology & Therapeutics
☐ Submit dFDA-impact to Value in Health
☐ Track status in YAML (submitted → under-review → accepted → published)
```

### Phase 5: Book Distribution (Month 2+)
```yaml
☐ Register ISBNs (Bowker or use KDP ISBNs)
☐ Format for KDP (Kindle + paperback + hardcover)
☐ Upload to Amazon KDP
☐ Upload to IngramSpark (bookstores)
☐ Upload to Draft2Digital (Apple, Kobo, B&N, libraries)
☐ Setup Gumroad for direct sales
☐ Create Goodreads author page and book listing
```

### Phase 6: Marketing & Outreach (Ongoing)
```yaml
☐ Announce on Twitter (@warondisease, @thinkbynumbers)
☐ Post on LinkedIn
☐ Write Medium blog posts
☐ Pitch to podcasts (80,000 Hours, Lex Fridman, Tim Ferriss)
☐ Press release for book launch
☐ Share with think tanks (Brookings, RAND)
☐ Share with practitioner networks (Participatory Budgeting Project)
```

## Status Update Commands

### Manual Update
Edit `_quarto-*.yml` directly:

```yaml
preprints:
  - platform: ssrn
    status: published  # Changed from 'pending'
    url: "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=12345"
    submission-date: "2025-01-20"
    publish-date: "2025-01-22"
```

### Programmatic Update (Future)
```bash
# Update status
python scripts/update-publication-status.py \
  --config _quarto-economics.yml \
  --platform ssrn \
  --status published \
  --url "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=12345"

# Generate overview report
python scripts/generate-publication-summary.py > docs/PUBLICATION-STATUS.md
```

## Priority Order

### Immediate (This Week)
1. ✓ Quarto configs with publishing metadata
2. Review Zenodo drafts, publish to get DOIs
3. Upload to SSRN (all applicable papers)

### Week 2-3
4. Upload to academic networks (ResearchGate, Academia.edu)
5. Prepare journal submissions (format, cover letters)

### Week 3-4
6. Submit to top-choice journals
7. Start book formatting for KDP

### Month 2+
8. Book distribution to all platforms
9. Marketing and podcast pitches
10. Think tank engagement

## DOI Tracking

### Zenodo DOIs (Concept vs Version)
- **Concept DOI**: 10.5281/zenodo.XXXXX (always latest)
- **Version DOI**: 10.5281/zenodo.XXXXX+1 (this version)

Use **Concept DOI** in citations to always point to latest version.

### Where to Add DOIs

```yaml
# In _quarto-*.yml metadata
preprints:
  - platform: zenodo
    doi: "10.5281/zenodo.12344"        # Concept DOI
    version-doi: "10.5281/zenodo.12345" # Version DOI
    url: "https://zenodo.org/records/12345"

journals:
  - name: "Health Affairs"
    doi: "10.1377/hlthaff.2025.00123"
    url: "https://www.healthaffairs.org/doi/10.1377/hlthaff.2025.00123"
```

## Key Contacts & Links

### Zenodo
- Production: https://zenodo.org/me/uploads
- Sandbox: https://sandbox.zenodo.org/me/uploads
- Token: Set in GitHub Secrets as `ZENODO_TOKEN`

### SSRN
- Upload: https://www.ssrn.com/index.cfm/en/janda/job-openings/
- Profile: Create author profile

### arXiv
- Submit: https://arxiv.org/submit
- Endorsement: Required for first submission (request from established researcher)

### medRxiv
- Submit: https://www.medrxiv.org/submit-a-manuscript
- Manual upload only (no API)

### ResearchGate
- Profile: https://www.researchgate.net/profile/Mike-Sinn
- Upload: Manual PDF upload

### Amazon KDP
- Dashboard: https://kdp.amazon.com
- ISBN: Register via Bowker or use free KDP ISBN

## ISBNs Needed for Book

```yaml
☐ Paperback ISBN-13: _______________
☐ Hardcover ISBN-13: _______________
☐ eBook ISBN-13 (optional): _______________
```

Register at: https://www.myidentifiers.com (Bowker - official US ISBN agency)
Or use free KDP ISBNs (but then Amazon is listed as publisher)

## BISAC Categories for Book

Primary: **POL024000** - POLITICAL SCIENCE / Public Policy / Social Policy
Secondary: **MED036000** - MEDICAL / Public Health
Tertiary: **POL034000** - POLITICAL SCIENCE / Peace

## Marketing Taglines

### Economics Paper
"How a 1% Military Budget Shift Could Generate $30 Quadrillion in Value"

### IAB Paper
"Making Public Goods Profitable: How to Align Political and Societal Incentives"

### Wishocracy Paper
"Fixing Democracy with Randomized Pairwise Comparisons"

### dFDA Spec Paper
"Bradford Hill Criteria Meet Machine Learning: The Predictor Impact Score"

### dFDA Impact Paper
"How to Cut Drug Development Costs by 95% and Generate Trillion-Dollar Returns"

### Book
"How to End War and Disease: Get 500 Years of Medical Progress in 20, Make Humanity Filthy Rich, and Avoid the Apocalypse"

## Next Actions

### Today
- [ ] Copy publishing sections from example YML files to actual `_quarto-*.yml` files
- [ ] Go to https://zenodo.org/me/uploads and review auto-uploaded drafts
- [ ] Publish Zenodo drafts to get DOIs

### This Week
- [ ] Create SSRN author profile
- [ ] Upload all papers to SSRN
- [ ] Request arXiv endorsement (if submitting to arXiv)

### Next Week
- [ ] Upload PDFs to ResearchGate and Academia.edu
- [ ] Prepare journal submission packages (cover letters, formatted manuscripts)

### Month 2
- [ ] Submit to top-choice journals
- [ ] Start book formatting and ISBN registration
- [ ] Begin podcast pitch campaign

## Questions?

See `PUBLICATION-TRACKING-GUIDE.md` for detailed implementation instructions.
