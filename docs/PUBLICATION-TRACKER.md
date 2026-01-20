# Publication Tracker

This document tracks all papers and publications from this project and their publication destinations.

## Publication Status Tracking

**Status is tracked directly in each paper's Quarto config file** under `metadata.publishing`:
- Each `_quarto-*.yml` file contains its own publishing section
- Tracks own site deployment status
- Lists preprint servers (Zenodo, SSRN, arXiv/medRxiv) with URL placeholders
- Tracks top journal targets with submission status
- Update URLs and status directly in the YAML as you publish

**Schema reference:** See `publication-tracking-schema.yml` for all available fields and examples.

---

## Publications Summary

| # | Title | Type | Own Website | PDF | Status |
|---|-------|------|-------------|-----|--------|
| 1 | How to End War and Disease | Book | [manual.WarOnDisease.org](https://manual.WarOnDisease.org) | How-to-End-War-and-Disease.pdf | Draft |
| 2 | The 1% Treaty (Economics) | Paper | [impact.warondisease.org](https://impact.warondisease.org) | 1-percent-treaty-impact.pdf | Draft |
| 3 | Incentive Alignment Bonds | Paper | [iab.warondisease.org](https://iab.warondisease.org) | incentive-alignment-bonds-paper.pdf | Draft |
| 4 | Wishocracy (RAPPA) | Paper | [paper.wishocracy.org](https://paper.wishocracy.org) | wishocracy-rappa-paper.pdf | Draft |
| 5 | dFDA Spec (Methodology) | Paper | [spec.dfda.earth](https://spec.dfda.earth) | dfda-spec-paper.pdf | Draft |
| 6 | dFDA Impact (ROI Analysis) | Paper | [impact.dfda.earth](https://impact.dfda.earth) | dfda-impact-paper.pdf | Draft |

---

## 1. How to End War and Disease (Book)

**Source:** `_quarto-manual.yml`
**QMD:** `index-manual.qmd` + 81 chapters
**Website:** https://manual.WarOnDisease.org
**Formats:** HTML, PDF, EPUB

### Publication Destinations

| Platform | Status | URL/Notes |
|----------|--------|-----------|
| **Own Website** | Deployed | https://manual.WarOnDisease.org |
| **Amazon KDP** | TODO | Kindle Direct Publishing (ebook + paperback) |
| **Apple Books** | TODO | Via EPUB upload |
| **Google Play Books** | TODO | Via EPUB or PDF |
| **Barnes & Noble Press** | TODO | Nook ebook + print |
| **Kobo Writing Life** | TODO | International ebook distribution |
| **Smashwords** | TODO | Wide distribution to libraries |
| **Draft2Digital** | TODO | Aggregator for multiple platforms |
| **IngramSpark** | TODO | Print-on-demand for bookstores |
| **Leanpub** | TODO | For in-progress books with updates |
| **Gumroad** | TODO | Direct sales with pay-what-you-want |

---

## 2. The 1% Treaty: Health and Economic Impact (Economics Paper)

**Source:** `_quarto-1-pct-treaty-impact.yml`
**QMD:** `knowledge/economics/1-pct-treaty-impact.qmd`
**Website:** https://impact.warondisease.org
**Formats:** HTML, PDF

### Abstract
Quantitative analysis showing how redirecting 1% of global military spending ($27.2B/year) to pragmatic clinical trials could advance treatment access by 207 years, save 10.5 billion life-years, and generate $30 quadrillion in long-run economic value.

### Publication Destinations

| Platform | Status | Category | Notes |
|----------|--------|----------|-------|
| **Own Website** | Deployed | Self-hosted | https://impact.warondisease.org |
| **SSRN** | TODO | Preprint | Social Science Research Network |
| **NBER** | TODO | Working Paper | National Bureau of Economic Research |
| **arXiv** | TODO | Preprint | econ.GN (General Economics) |
| **ResearchGate** | TODO | Academic Social | Upload PDF + claim authorship |
| **Academia.edu** | TODO | Academic Social | Upload PDF + profile |
| **OSF Preprints** | TODO | Preprint | Open Science Framework |
| **Zenodo** | **AUTO** | Archive | DOI via CI (review drafts at zenodo.org/me/uploads) |
| **Google Scholar** | TODO | Indexing | Auto-indexed from above |
| **EconPapers/RePEc** | TODO | Economics DB | Working paper series |
| **Health Affairs** | TODO | Journal | Health policy journal |
| **The Lancet** | TODO | Journal | Commentary/Viewpoint |
| **BMJ** | TODO | Journal | Analysis piece |
| **PLOS Medicine** | TODO | Journal | Open access |
| **Value in Health** | TODO | Journal | ISPOR journal |

---

## 3. Incentive Alignment Bonds (IAB Paper)

**Source:** `_quarto-iab.yml`
**QMD:** `knowledge/appendix/incentive-alignment-bonds-paper.qmd`
**Website:** https://iab.warondisease.org
**Formats:** HTML, PDF

### Abstract
A mechanism design approach that makes supporting welfare-improving policies incentive-compatible for rational politicians through securitized returns on public good production.

### Publication Destinations

| Platform | Status | Category | Notes |
|----------|--------|----------|-------|
| **Own Website** | Deployed | Self-hosted | https://iab.warondisease.org |
| **SSRN** | TODO | Preprint | Political Economy category |
| **arXiv** | TODO | Preprint | econ.GN or cs.GT (Game Theory) |
| **NBER** | TODO | Working Paper | Political Economy program |
| **ResearchGate** | TODO | Academic Social | |
| **Academia.edu** | TODO | Academic Social | |
| **OSF Preprints** | TODO | Preprint | |
| **Zenodo** | **AUTO** | Archive | DOI via CI |
| **American Economic Review** | TODO | Journal | Top economics journal |
| **Journal of Political Economy** | TODO | Journal | Top economics journal |
| **Public Choice** | TODO | Journal | Public choice theory |
| **Games and Economic Behavior** | TODO | Journal | Mechanism design |
| **Journal of Public Economics** | TODO | Journal | Public economics |
| **Constitutional Political Economy** | TODO | Journal | Political economy |

---

## 4. Wishocracy: RAPPA for Democratic Resource Allocation

**Source:** `_quarto-wishocracy.yml`
**QMD:** `knowledge/appendix/wishocracy-paper.qmd`
**Website:** https://paper.wishocracy.org
**Formats:** HTML, PDF

### Abstract
A governance mechanism that employs Randomized Aggregated Pairwise Preference Allocation (RAPPA) to elicit and synthesize collective preferences for public resource allocation.

### Publication Destinations

| Platform | Status | Category | Notes |
|----------|--------|----------|-------|
| **Own Website** | Deployed | Self-hosted | https://paper.wishocracy.org |
| **SSRN** | TODO | Preprint | Political Science / Public Choice |
| **arXiv** | TODO | Preprint | cs.GT (Game Theory) |
| **ResearchGate** | TODO | Academic Social | |
| **Academia.edu** | TODO | Academic Social | |
| **OSF Preprints** | TODO | Preprint | |
| **Zenodo** | **AUTO** | Archive | DOI via CI |
| **American Political Science Review** | TODO | Journal | Top political science |
| **Journal of Politics** | TODO | Journal | Political science |
| **Social Choice and Welfare** | TODO | Journal | Voting theory |
| **Public Choice** | TODO | Journal | Collective decision-making |
| **Journal of Theoretical Politics** | TODO | Journal | Formal political theory |
| **Democracy & Nature** | TODO | Journal | Democratic theory |
| **Participatory Budgeting Project** | TODO | Practitioner | Blog/resource sharing |

---

## 5. dFDA: Two-Stage Real-World Evidence Validation (Spec Paper)

**Source:** `_quarto-dfda-spec.yml`
**QMD:** `knowledge/appendix/dfda-spec-paper.qmd`
**Website:** https://spec.dfda.earth
**Formats:** HTML, PDF

### Abstract
We present the Predictor Impact Score (PIS), a novel composite metric operationalizing Bradford Hill causality criteria for automated signal detection from aggregated N-of-1 observational studies. Combined with pragmatic trial confirmation following the RECOVERY model, this two-stage framework generates validated outcome labels at 100x lower cost than traditional Phase III trials.

### Publication Destinations

| Platform | Status | Category | Notes |
|----------|--------|----------|-------|
| **Own Website** | Deployed | Self-hosted | https://spec.dfda.earth |
| **medRxiv** | TODO | Preprint | Health sciences preprint |
| **arXiv** | TODO | Preprint | stat.ME (Methodology) |
| **SSRN** | TODO | Preprint | Health Economics |
| **ResearchGate** | TODO | Academic Social | |
| **Academia.edu** | TODO | Academic Social | |
| **OSF Preprints** | TODO | Preprint | |
| **Zenodo** | **AUTO** | Archive | DOI via CI |
| **Clinical Pharmacology & Therapeutics** | TODO | Journal | Pharmacology methodology |
| **Pharmacoepidemiology & Drug Safety** | TODO | Journal | Pharmacoepidemiology |
| **Drug Safety** | TODO | Journal | Pharmacovigilance |
| **JAMA Network Open** | TODO | Journal | Open access medical |
| **BMJ Open** | TODO | Journal | Open access medical |
| **PLOS Medicine** | TODO | Journal | Open access |
| **Nature Medicine** | TODO | Journal | High-impact |
| **Contemporary Clinical Trials** | TODO | Journal | Trial methodology |
| **Journal of Clinical Epidemiology** | TODO | Journal | Epidemiology methods |
| **Statistics in Medicine** | TODO | Journal | Statistical methods |

---

## 6. dFDA Cost-Benefit Analysis & ROI (Impact Paper)

**Source:** `_quarto-dfda-impact.yml`
**QMD:** `knowledge/appendix/dfda-impact-paper.qmd`
**Website:** https://impact.dfda.earth
**Formats:** HTML, PDF

### Abstract
Analysis and Return on Investment - How to slash per-patient trial costs by up to 95%, generate billions in annual gross R&D savings, and deliver exceptional ROI through a decentralized framework for drug assessment.

### Publication Destinations

| Platform | Status | Category | Notes |
|----------|--------|----------|-------|
| **Own Website** | Deployed | Self-hosted | https://impact.dfda.earth |
| **medRxiv** | TODO | Preprint | Health sciences |
| **SSRN** | TODO | Preprint | Health Economics |
| **arXiv** | TODO | Preprint | econ.GN |
| **ResearchGate** | TODO | Academic Social | |
| **Academia.edu** | TODO | Academic Social | |
| **OSF Preprints** | TODO | Preprint | |
| **Zenodo** | **AUTO** | Archive | DOI via CI |
| **Health Affairs** | TODO | Journal | Health policy |
| **Value in Health** | TODO | Journal | Health economics |
| **PharmacoEconomics** | TODO | Journal | Drug economics |
| **Journal of Health Economics** | TODO | Journal | Health economics |
| **JAMA Health Forum** | TODO | Journal | Health policy |
| **Nature Reviews Drug Discovery** | TODO | Journal | Industry perspective |
| **Drug Discovery Today** | TODO | Journal | Industry |
| **Expert Review of Pharmacoeconomics** | TODO | Journal | Pharma economics |

---

## Cross-Platform Publication Strategy

### Tier 1: Immediate (Self-Hosted)
All publications deployed to own domains via Quarto + GitHub Pages/Netlify.

### Tier 2: Preprint Servers (Week 1-2)
1. **SSRN** - All papers (economics, political science, health)
2. **arXiv** - Methodology papers (dFDA Spec)
3. **medRxiv** - Health-related papers (dFDA papers)
4. **OSF Preprints** - All papers (DOI, versioning)

### Tier 3: Academic Social Networks (Week 2-3)
1. **ResearchGate** - All papers
2. **Academia.edu** - All papers
3. **Google Scholar** - Auto-indexed

### Tier 4: Archive & DOI (Week 2-3)
1. **Zenodo** - All papers (DOI assignment, long-term archive)

### Tier 5: Journal Submissions (Week 4+)
Target journals by paper type:
- **Economics/1% Treaty**: Health Affairs, Value in Health, Lancet commentary
- **IAB**: Public Choice, Journal of Political Economy
- **Wishocracy**: Social Choice and Welfare, Public Choice
- **dFDA Spec**: Clinical Pharmacology & Therapeutics, Pharmacoepidemiology
- **dFDA Impact**: Health Affairs, PharmacoEconomics

### Tier 6: Book Distribution (Month 2+)
- **Amazon KDP**: Kindle + paperback
- **IngramSpark**: Bookstore distribution
- **Apple Books, Kobo, Google Play**: Ebook platforms
- **Smashwords/Draft2Digital**: Wide distribution

---

## DOI Tracking

**Strategy:** Get DOIs from Zenodo first, then reference them on all other platforms.

| Paper | Zenodo DOI | Concept DOI | Status |
|-------|------------|-------------|--------|
| Economics (1% Treaty) | `TBD` | `TBD` | Draft uploaded via CI |
| IAB | `TBD` | `TBD` | Draft uploaded via CI |
| Wishocracy | `TBD` | `TBD` | Draft uploaded via CI |
| dFDA Spec | `TBD` | `TBD` | Draft uploaded via CI |
| dFDA Impact | `TBD` | `TBD` | Draft uploaded via CI |

**After publishing on Zenodo**, use the DOI when submitting to:
- SSRN (has "link to existing version" field)
- arXiv (related DOI field)
- Journal submissions (prior preprint DOI)
- ResearchGate/Academia.edu profiles

---

## Platform API Comparison

| Platform | Upload API | Automation | Auth Method | Notes |
|----------|-----------|------------|-------------|-------|
| **Zenodo** | REST API | **Automated** (CI) | Token | Best for DOIs, versioning |
| **OSF Preprints** | REST API | Can automate | Token | Similar to Zenodo, good API |
| **Figshare** | REST API | Can automate | Token | Alternative to Zenodo |
| **arXiv** | SWORD | Possible | Institutional | Requires endorsement |
| **SSRN** | Partner API | Limited | Partner only | Manual upload easier |
| **medRxiv** | None | Manual | Web form | No API |
| **ResearchGate** | None | Manual | Web login | No upload API |
| **Academia.edu** | None | Manual | Web login | No upload API |

### Currently Automated (GitHub Actions)

```yaml
# .github/workflows/publish.yml
- Zenodo draft upload for all papers (economics, iab, wishocracy, dfda-spec, dfda-impact)
- Netlify deployment for all sites
```

### Potential to Automate

1. **OSF Preprints** - Good REST API, similar to Zenodo
2. **Figshare** - Good REST API, alternative archive

### Manual Upload Required

- SSRN, arXiv, medRxiv, ResearchGate, Academia.edu, Journals

---

## Zenodo Commands

```bash
# Upload all papers as drafts (review at zenodo.org/me/uploads)
python scripts/publish-zenodo.py --draft

# Upload specific paper
python scripts/publish-zenodo.py --draft --paper iab

# Dry run (show what would happen)
python scripts/publish-zenodo.py --dry-run

# Test with sandbox
python scripts/publish-zenodo.py --sandbox --draft

# List discovered papers
python scripts/publish-zenodo.py --list
```

**Environment Variables:**
- `ZENODO_TOKEN` - Production token from https://zenodo.org/account/settings/applications/
- `ZENODO_SANDBOX_TOKEN` - Sandbox token for testing

---

## Notes

- All publications licensed CC BY-NC 4.0
- Author: Mike P. Sinn, Decentralized Institutes of Health
- ORCID: [0009-0006-0212-1094](https://orcid.org/0009-0006-0212-1094)
- Contact: mike@warondisease.org
- GitHub: https://github.com/mikepsinn/disease-eradication-plan

---

## Render Commands

```bash
# Render all publications
python scripts/render-quarto.py all

# Render individual publications
python scripts/render-quarto.py book       # War on Disease book
python scripts/render-quarto.py economics  # 1% Treaty paper
python scripts/render-quarto.py iab        # Incentive Alignment Bonds
python scripts/render-quarto.py wishocracy # Wishocracy paper
python scripts/render-quarto.py dfda-spec  # dFDA methodology
python scripts/render-quarto.py dfda-impact # dFDA ROI analysis
```
