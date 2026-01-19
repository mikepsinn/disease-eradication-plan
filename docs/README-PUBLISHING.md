# Publishing Documentation

Complete documentation for publishing papers and the book from this repository.

## 📋 Quick Navigation

| Document | Purpose | Use When |
|----------|---------|----------|
| **[PUBLICATION-CHECKLIST.md](PUBLICATION-CHECKLIST.md)** | Quick reference checklist | Starting publication process |
| **[PUBLICATION-TRACKING-GUIDE.md](PUBLICATION-TRACKING-GUIDE.md)** | Complete implementation guide | Understanding the system |
| **[publication-tracking-schema.yml](publication-tracking-schema.yml)** | YAML schema reference | Adding fields to configs |
| **[PUBLICATION-TRACKER.md](PUBLICATION-TRACKER.md)** | Legacy publication tracker | Overview of all publications |
| **[zenodo-publishing.md](zenodo-publishing.md)** | Zenodo automation guide | Working with Zenodo uploads |
| **[DEPLOYMENT.md](../GUIDES/DEPLOYMENT.md)** | GitHub Actions deployment | Understanding CI/CD |

**Publication tracking is already integrated** in all `_quarto-*.yml` files under `metadata.publishing`.

## 📦 What We Publish

### 6 Publications from This Repository

1. **How to End War and Disease** (Book)
   - Main book, 81 chapters, ~900 pages
   - Site: https://manual.WarOnDisease.org
   - Config: `_quarto-book.yml`

2. **The 1% Treaty** (Economics Paper)
   - Economic impact analysis
   - Site: https://impact.warondisease.org
   - Config: `_quarto-economics.yml` ✓ Publishing added

3. **Incentive Alignment Bonds** (IAB Paper)
   - Mechanism design for political incentives
   - Site: https://iab.warondisease.org
   - Config: `_quarto-iab.yml` ✓ Publishing added

4. **Wishocracy** (RAPPA Paper)
   - Democratic resource allocation mechanism
   - Site: https://paper.wishocracy.org
   - Config: `_quarto-wishocracy.yml` ✓ Publishing added

5. **dFDA Spec** (Methodology Paper)
   - Two-stage real-world evidence validation
   - Site: https://spec.dfda.earth
   - Config: `_quarto-dfda-spec.yml` ✓ Publishing added

6. **dFDA Impact** (ROI Paper)
   - Cost-benefit analysis and ROI
   - Site: https://impact.dfda.earth
   - Config: `_quarto-dfda-impact.yml` ✓ Publishing added

## 🚀 Publication Workflow

### Current Status: Phase 1 Complete ✓

All sites deployed and live at their own domains via Netlify.

### Next Phases

```
Phase 1: Own Websites ✓ DONE
├─ All sites live on Netlify
└─ Automated deployment via GitHub Actions

Phase 2: Preprints (Week 1-2)
├─ Zenodo (automated uploads via CI)
├─ SSRN (manual upload)
├─ arXiv (manual, requires endorsement)
└─ medRxiv (health papers, manual)

Phase 3: Academic Networks (Week 2-3)
├─ ResearchGate
├─ Academia.edu
└─ Google Scholar (auto-indexed)

Phase 4: Journal Submissions (Week 3+)
├─ Economics → Health Affairs, Value in Health
├─ IAB → Public Choice, AER
├─ Wishocracy → Social Choice and Welfare
├─ dFDA-spec → Clinical Pharmacology & Therapeutics
└─ dFDA-impact → Value in Health, Health Affairs

Phase 5: Book Distribution (Month 2+)
├─ Amazon KDP (Kindle + paperback + hardcover)
├─ IngramSpark (bookstores)
├─ Draft2Digital (Apple, Kobo, B&N, libraries)
└─ Direct sales (Gumroad, Leanpub)

Phase 6: Marketing & Outreach (Ongoing)
├─ Social media announcements
├─ Podcast pitches
├─ Press releases
└─ Think tank engagement
```

## 📝 How to Use This System

### 1. Publishing Sections Already Added ✓

All `_quarto-*.yml` files now have `metadata.publishing` sections with:
- Own site URL and deployment status
- Top 3 journal targets
- Preprint server configurations (Zenodo, SSRN, arXiv/medRxiv)

### 2. Update Status as You Progress

Edit the YAML directly to track progress:

```yaml
# Before
preprints:
  - platform: ssrn
    status: pending
    url: ""

# After
preprints:
  - platform: ssrn
    status: published
    url: "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=12345"
    submission-date: "2025-01-20"
    publish-date: "2025-01-22"
```

## 🎯 Top Journal Targets

### Economics Paper
1. **Health Affairs** (IF: 7.5) - Premier health policy
2. **Value in Health** (IF: 5.9) - ISPOR health economics
3. **The Lancet** (IF: 202.7) - Commentary piece

### IAB Paper
1. **Public Choice** (IF: 1.3) - PERFECT FIT
2. **American Economic Review** (IF: 10.7) - Top tier
3. **Journal of Political Economy** (IF: 9.3)

### Wishocracy Paper
1. **Social Choice and Welfare** (IF: 0.9) - PERFECT FIT
2. **Public Choice** (IF: 1.3)
3. **APSR** (IF: 5.7) - Top political science

### dFDA Spec Paper
1. **Clinical Pharmacology & Therapeutics** (IF: 6.3) - EXCELLENT FIT
2. **Pharmacoepidemiology and Drug Safety** (IF: 3.4) - PERFECT FIT
3. **Drug Safety** (IF: 4.6)

### dFDA Impact Paper
1. **Value in Health** (IF: 5.9) - EXCELLENT FIT
2. **Health Affairs** (IF: 7.5)
3. **PharmacoEconomics** (IF: 4.4)

## 🔄 Automated Processes

### What's Automated (via GitHub Actions)

✓ **Website Deployment**
- All sites auto-deploy to Netlify on push to master
- See: `.github/workflows/publish.yml`

✓ **Zenodo Draft Uploads**
- PDFs auto-uploaded as drafts on every push
- Review at: https://zenodo.org/me/uploads
- See: `scripts/publish-zenodo.py`

### What's Manual

❌ **Preprint Servers**
- SSRN, arXiv, medRxiv require manual upload

❌ **Journal Submissions**
- All journal submissions manual

❌ **Academic Networks**
- ResearchGate, Academia.edu manual uploads

❌ **Book Platforms**
- Amazon KDP, IngramSpark, etc. manual

## 📊 Tracking & Reporting

### Current System

**Embedded in Quarto Configs**
- Each `_quarto-*.yml` has `metadata.publishing` section
- Version controlled with Git
- Single source of truth

### Future Automation (Planned)

```bash
# Update publication status
python scripts/update-publication-status.py \
  --config _quarto-economics.yml \
  --platform ssrn \
  --status published \
  --url "https://papers.ssrn.com/..."

# Generate status report
python scripts/generate-publication-summary.py > docs/STATUS.md

# Export to CSV
python scripts/export-publication-status.py --format csv > pubs.csv

# Generate dashboard
python scripts/generate-publication-dashboard.py
```

## 🔗 Important Links

### Zenodo
- **Production**: https://zenodo.org/me/uploads
- **Sandbox**: https://sandbox.zenodo.org/me/uploads
- **API Docs**: https://developers.zenodo.org/

### Preprint Servers
- **SSRN**: https://www.ssrn.com
- **arXiv**: https://arxiv.org/submit
- **medRxiv**: https://www.medrxiv.org/submit-a-manuscript
- **OSF Preprints**: https://osf.io/preprints/

### Academic Networks
- **ResearchGate**: https://www.researchgate.net
- **Academia.edu**: https://www.academia.edu
- **Google Scholar**: (auto-indexes)

### Book Platforms
- **Amazon KDP**: https://kdp.amazon.com
- **IngramSpark**: https://www.ingramspark.com
- **Draft2Digital**: https://www.draft2digital.com
- **Bowker (ISBNs)**: https://www.myidentifiers.com

## 📖 Documentation Hierarchy

```
docs/
├── README-PUBLISHING.md (this file)     ← Start here
├── PUBLICATION-CHECKLIST.md             ← Quick reference
├── PUBLICATION-TRACKING-GUIDE.md        ← Complete guide
├── publication-tracking-schema.yml      ← Schema reference
├── PUBLICATION-TRACKER.md               ← Legacy tracker
└── zenodo-publishing.md                 ← Zenodo automation

Publishing is integrated in Quarto configs:
├── _quarto-economics.yml     ✓ metadata.publishing added
├── _quarto-iab.yml           ✓ metadata.publishing added
├── _quarto-wishocracy.yml    ✓ metadata.publishing added
├── _quarto-dfda-spec.yml     ✓ metadata.publishing added
└── _quarto-dfda-impact.yml   ✓ metadata.publishing added
```

## 🎬 Getting Started

### Today (10 minutes)
1. Read [PUBLICATION-CHECKLIST.md](PUBLICATION-CHECKLIST.md)
2. Go to https://zenodo.org/me/uploads
3. Review auto-uploaded drafts
4. Publish drafts to get DOIs
5. Update DOI URLs in `_quarto-*.yml` files

### This Week (2-3 hours)
1. Create SSRN account and profile
2. Upload papers to SSRN
3. Update URLs in `_quarto-*.yml` publishing sections

### Next Week (4-5 hours)
1. Upload to ResearchGate and Academia.edu
2. Prepare journal submission packages
3. Write cover letters for top-choice journals

### Month 2 (Ongoing)
1. Submit to journals
2. Track review status in YAML
3. Start book formatting
4. Begin marketing campaign

## ❓ Common Questions

**Q: Do I need to update both the YAML and PUBLICATION-TRACKER.md?**
A: Your choice. Either keep both in sync or deprecate the markdown file and rely solely on YAML.

**Q: Can I automate more of this?**
A: Partially. Zenodo is automated. We could add OSF Preprints automation. Journals require manual submission.

**Q: What if a journal rejects my paper?**
A: Update status to `rejected`, submit to next journal in priority order, track new submission.

**Q: How do I get an arXiv endorsement?**
A: Ask an established researcher in the category to endorse you. One-time requirement per category.

**Q: Should I submit to all the journals listed?**
A: No. Start with top 1-2 choices. Only try others if rejected.

## 📞 Need Help?

- **Zenodo issues**: Check [zenodo-publishing.md](zenodo-publishing.md)
- **Deployment issues**: Check [DEPLOYMENT.md](../GUIDES/DEPLOYMENT.md)
- **Schema questions**: Check [publication-tracking-schema.yml](publication-tracking-schema.yml)
- **General questions**: Check [PUBLICATION-TRACKING-GUIDE.md](PUBLICATION-TRACKING-GUIDE.md)

## 🎉 Success Metrics

Track these in your YAML:

```yaml
success-metrics:
  zenodo-doi: "✓ 10.5281/zenodo.12345"
  ssrn-url: "✓ https://papers.ssrn.com/..."
  journal-acceptance: "[ ] Pending"
  citations: "0 (track via Google Scholar)"
  downloads: "Track via Zenodo, SSRN, ResearchGate"
```

---

**Last Updated**: 2025-01-19

**Maintainer**: Mike P. Sinn (mike@warondisease.org)

**Repository**: https://github.com/mikepsinn/disease-eradication-plan
