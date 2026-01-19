# Publication Tracking in Quarto Configs

This guide explains how to use the YAML-based publication tracking system embedded in Quarto config files.

## Overview

Instead of maintaining a separate tracking document, we embed publication status directly in each `_quarto-*.yml` file under `metadata.publishing`. This keeps publication targets and status alongside the paper's metadata.

## Benefits

1. **Single Source of Truth**: Paper metadata and publication status in one place
2. **Version Control**: Track publication history in Git
3. **Automation Ready**: Scripts can read/update status programmatically
4. **Self-Documenting**: Each paper carries its own publication roadmap

## Quick Start

### 1. Add Publishing Section to Quarto Config

In your `_quarto-*.yml` file, add a `publishing` section under `metadata`:

```yaml
metadata:
  # ... existing metadata ...

  publishing:
    own-site:
      url: "https://impact.warondisease.org"
      status: deployed

    preprints:
      - platform: zenodo
        status: auto-uploaded
        url: ""
        doi: ""

    journals:
      - name: "Health Affairs"
        status: target
        url: ""
```

### 2. Update Status as You Progress

Edit the YAML directly to track progress:

```yaml
preprints:
  - platform: ssrn
    status: published  # Changed from 'pending'
    url: "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=12345"
    submission-date: "2025-01-20"
    publish-date: "2025-01-22"
```

### 3. Extract Status with Scripts

Python example:

```python
import yaml

with open('_quarto-economics.yml') as f:
    config = yaml.safe_load(f)

publishing = config['metadata']['publishing']

# Check what's been published
for preprint in publishing['preprints']:
    if preprint['status'] == 'published':
        print(f"{preprint['platform']}: {preprint['url']}")
```

## Status Values

### Preprints and Archives

| Status | Meaning |
|--------|---------|
| `pending` | Not yet uploaded |
| `in-progress` | Preparing upload |
| `auto-uploaded` | CI auto-uploaded as draft |
| `published` | Live and accessible |
| `skipped` | Intentionally not pursuing this platform |

### Journals

| Status | Meaning |
|--------|---------|
| `target` | Identified as submission target |
| `preparing` | Formatting for submission |
| `submitted` | Submitted, awaiting response |
| `under-review` | Peer review in progress |
| `revision-requested` | Revisions requested |
| `revised-submitted` | Revisions submitted |
| `accepted` | Accepted for publication |
| `published` | Published and live |
| `rejected` | Rejected by journal |
| `withdrawn` | Withdrawn by author |

### Own Site

| Status | Meaning |
|--------|---------|
| `building` | Site being built |
| `deployed` | Live on web |
| `pending` | Not yet deployed |

## Publication Workflow

### Phase 1: Own Website (Immediate)

```yaml
own-site:
  url: "https://impact.warondisease.org"
  status: deployed
  deploy-trigger: push-to-main
```

**Action**: Already automated via GitHub Actions

### Phase 2: Preprint Servers (Week 1-2)

```yaml
preprints:
  - platform: zenodo
    status: auto-uploaded
    notes: "Check https://zenodo.org/me/uploads for draft"

  - platform: ssrn
    status: pending
    target-date: "2025-01-25"
```

**Actions**:
1. Review Zenodo draft, click "Publish" to get DOI
2. Manually upload to SSRN
3. Upload to OSF Preprints (can automate)
4. Update URLs and DOIs in YAML

### Phase 3: Academic Networks (Week 2-3)

```yaml
academic-networks:
  - platform: researchgate
    status: pending
  - platform: academia-edu
    status: pending
```

**Actions**: Upload PDF to ResearchGate and Academia.edu

### Phase 4: Journal Submissions (Week 3+)

```yaml
journals:
  - name: "Health Affairs"
    status: submitted
    submission-date: "2025-02-01"
    decision-date: ""
```

**Actions**:
1. Submit to top-choice journal
2. Update status as review progresses
3. If rejected, submit to next journal in priority order

### Phase 5: Social Media & Outreach (Ongoing)

```yaml
social-media:
  - platform: twitter
    account: "@warondisease"
    status: published
    post-url: "https://twitter.com/warondisease/status/123"
    post-date: "2025-02-05"
```

## Examples by Publication Type

### Economics Paper

See: `docs/publication-tracking-economics-example.yml`

**Key platforms:**
- SSRN (economics preprints)
- NBER Working Papers
- Health Affairs (journal)
- Value in Health (journal)

### Political Science Paper (Wishocracy)

**Key platforms:**
- SSRN (political science)
- arXiv (cs.GT - game theory)
- Public Choice (journal)
- Social Choice and Welfare (journal)

### Medical/Methodology Paper (dFDA)

**Key platforms:**
- medRxiv (health sciences preprints)
- arXiv (stat.ME - methodology)
- Clinical Pharmacology & Therapeutics
- Pharmacoepidemiology & Drug Safety

### Book (How to End War and Disease)

**Key platforms:**
- Amazon KDP (Kindle + paperback)
- Apple Books (ePub)
- IngramSpark (bookstores)
- Google Play Books

## Automated Updates

### Zenodo CI Integration

The GitHub Actions workflow auto-uploads drafts to Zenodo. To track this:

```yaml
preprints:
  - platform: zenodo
    status: auto-uploaded
    url: ""  # Manually add after publishing draft
    doi: ""  # Manually add after publishing draft
    last-ci-upload: "2025-01-19"  # Updated by CI
    notes: "Draft auto-uploaded on every push; manually publish at zenodo.org/me/uploads"
```

### Future: Status Update Script

Proposed: `scripts/update-publication-status.py`

```bash
# Update status for a specific publication
python scripts/update-publication-status.py \
  --config _quarto-economics.yml \
  --platform ssrn \
  --status published \
  --url "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=12345"

# List all publication targets
python scripts/update-publication-status.py \
  --config _quarto-economics.yml \
  --list
```

## Tracking DOIs

### Zenodo (Concept DOI vs Version DOI)

Zenodo creates two DOIs:
- **Concept DOI**: Always resolves to latest version (use in citations)
- **Version DOI**: Specific to this version

```yaml
preprints:
  - platform: zenodo
    doi: "10.5281/zenodo.12344"  # Concept DOI (latest)
    version-doi: "10.5281/zenodo.12345"  # This version
```

### Journal DOI

Added when published:

```yaml
journals:
  - name: "Health Affairs"
    status: published
    doi: "10.1377/hlthaff.2025.00123"
    url: "https://www.healthaffairs.org/doi/10.1377/hlthaff.2025.00123"
    publication-date: "2025-03-15"
```

## Cross-Referencing Publications

When one paper references another (e.g., economics paper cites IAB paper):

```yaml
# In _quarto-economics.yml
metadata:
  related-publications:
    - title: "Incentive Alignment Bonds"
      url: "https://iab.warondisease.org"
      doi: "10.5281/zenodo.xxxxx"  # Once published
      relationship: "cites"
```

## Migration from PUBLICATION-TRACKER.md

The existing `docs/PUBLICATION-TRACKER.md` lists all platforms. To migrate:

1. **Keep PUBLICATION-TRACKER.md** as the master overview
2. **Add `publishing:` sections** to each `_quarto-*.yml` with specific targets
3. **Update both** when status changes

Or:

1. **Deprecate PUBLICATION-TRACKER.md**
2. **Move all tracking** into Quarto configs
3. **Generate overview** from configs: `scripts/generate-publication-overview.py`

## Generating Publication Reports

### Markdown Summary

```bash
# Generate summary from all configs
python scripts/generate-publication-summary.py

# Output: docs/PUBLICATION-STATUS.md
```

### CSV Export

```bash
# Export to CSV for spreadsheet tracking
python scripts/export-publication-status.py --format csv > publications.csv
```

### Dashboard

```bash
# Generate HTML dashboard
python scripts/generate-publication-dashboard.py
# Opens: _site/publication-dashboard.html
```

## Best Practices

### 1. Update Immediately

Update the YAML as soon as status changes:
- Paper submitted → Change `status: target` to `status: submitted`
- DOI received → Add `doi: "10.xxxx/xxxxx"`

### 2. Add Notes

Use `notes:` field for context:

```yaml
journals:
  - name: "Health Affairs"
    status: revision-requested
    revision-deadline: "2025-02-15"
    notes: "Reviewers requested more details on Monte Carlo methodology"
```

### 3. Track Dates

Always record dates:

```yaml
submission-date: "2025-01-20"
decision-date: "2025-02-10"
revision-deadline: "2025-03-01"
publication-date: "2025-04-15"
```

### 4. Version Control

Commit updates with clear messages:

```bash
git add _quarto-economics.yml
git commit -m "publishing: economics paper accepted by Health Affairs"
```

## Platform-Specific Notes

### SSRN
- **Category**: Select appropriate field (economics, political science, health)
- **Abstract**: 300-word limit
- **Keywords**: Up to 10
- **Related Papers**: Link to Zenodo DOI

### arXiv
- **Endorsement**: Required for first submission in a category
- **Category Codes**: `econ.GN`, `stat.ME`, `cs.GT`, etc.
- **Submission Window**: Daily deadline (20:00 UTC)

### Zenodo
- **Resource Type**: `publication-workingpaper`, `publication-article`, etc.
- **Communities**: Can add to topic-based communities
- **Versioning**: Each publish creates new version DOI

### ResearchGate
- **Auto-Index**: Often auto-indexes from arXiv/Zenodo
- **Stats**: Tracks reads, citations, recommendations

## Templates

### New Paper Publishing Section

```yaml
metadata:
  publishing:
    own-site:
      url: "https://your-paper.domain.org"
      status: deployed

    preprints:
      - platform: zenodo
        status: auto-uploaded
        url: ""
        doi: ""

    journals:
      - name: "Target Journal Name"
        tier: 1
        status: target
        url: ""
        impact-factor: 0.0
```

### Zenodo-Only (Minimal)

```yaml
metadata:
  publishing:
    own-site:
      url: "https://your-paper.domain.org"
      status: deployed

    preprints:
      - platform: zenodo
        status: auto-uploaded
        doi: ""
        notes: "See https://zenodo.org/me/uploads"
```

## FAQ

**Q: Should I track every possible journal?**
A: No. List your top 3-5 targets. Add more only if top choices reject.

**Q: What if I don't want to submit to journals?**
A: Fine. Just track preprints and own site.

**Q: Can I automate status updates?**
A: Partially. CI can update Zenodo status. Journal updates require manual tracking.

**Q: Do I need to update PUBLICATION-TRACKER.md too?**
A: Your choice. Either keep both in sync or deprecate the markdown file.

**Q: What about confidential submission info?**
A: Omit sensitive details. Just track status and public URLs.

## Related Files

- `docs/publication-tracking-schema.yml` - Full schema definition
- `docs/publication-tracking-economics-example.yml` - Economics paper example
- `docs/PUBLICATION-TRACKER.md` - Original tracking document
- `docs/zenodo-publishing.md` - Zenodo automation guide
- `.github/workflows/publish.yml` - CI workflow that uploads to Zenodo

## Next Steps

1. **Add `publishing:` section** to each `_quarto-*.yml` file
2. **Review Zenodo drafts** at https://zenodo.org/me/uploads
3. **Publish Zenodo drafts** to get DOIs
4. **Upload to SSRN** (manual)
5. **Upload to ResearchGate** and Academia.edu
6. **Submit to journals** starting with top choice
