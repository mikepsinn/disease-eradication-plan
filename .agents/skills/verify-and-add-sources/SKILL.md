---
name: verify-and-add-sources
description: Verifies claims have proper citations, searches for sources if needed, and adds them to references.bib. Use when making factual claims or adding statistics.
allowed-tools:
  - Read
  - Edit
  - Grep
  - WebSearch
  - WebFetch
---

# Source Verification & References Management

## When to Use

Use this skill when you:
- Add factual claims or statistics to QMD files
- Make assertions that need citations
- Reference external data or research
- Notice unsourced claims in existing text

## Process

### 1. Identify Claims Needing Sources

Common claims requiring citations:
- Statistics (e.g., "Global military spending is $2.2T")
- Scientific facts (e.g., "Clinical trials cost $1B on average")
- Historical events (e.g., "Costa Rica abolished its military in 1948")
- Research findings (e.g., "Bed nets cost $5/DALY")
- Policy statements (e.g., "FDA approval takes 8.2 years")

### 2. Search Existing References

```bash
grep -i "keyword" references.bib
```

Check if the source already exists in `references.bib` (project root).

### 3. Use Existing Source

If found, add citation to text:
```markdown
Global military spending is $2.2T [@sipri-2024-military-spending].
```

### 4. Search for New Source

If NOT found, use WebSearch:
- Search for authoritative sources (government data, academic papers, reputable organizations)
- Prefer primary sources over secondary
- Check publication date for currency

### 5. Add to references.bib

Add new BibTeX entry to `references.bib` (project root):

```bibtex
@misc{sipri-2024-military-spending,
  author = {{SIPRI}},
  title = {World Military Expenditure 2024},
  year = {2024},
  url = {https://www.sipri.org/...},
  note = {Global military spending reached \$2.2 trillion in 2024}
}
```

### 6. Cite in Text

Add citation to the claim:
```markdown
Global military spending is $2.2T [@sipri-2024-military-spending].
```

## BibTeX Entry Types

Use appropriate entry types:

| Type | Use For |
|------|---------|
| `@article` | Journal papers with DOI |
| `@book` | Books |
| `@misc` | Websites, reports, data sources |
| `@techreport` | Government/org reports |
| `@inproceedings` | Conference papers |

## BibTeX Format Examples

**Journal Article:**
```bibtex
@article{dimasi-2016-clinical-trial-costs,
  author = {DiMasi, Joseph A. and Grabowski, Henry G. and Hansen, Ronald W.},
  title = {Innovation in the pharmaceutical industry: New estimates of R\&D costs},
  journal = {Journal of Health Economics},
  volume = {47},
  pages = {20--33},
  year = {2016},
  doi = {10.1016/j.jhealeco.2016.01.012}
}
```

**Website/Report:**
```bibtex
@misc{who-2024-disease-burden,
  author = {{World Health Organization}},
  title = {Global Health Estimates 2024},
  year = {2024},
  url = {https://www.who.int/...},
  note = {Accessed January 2026}
}
```

**Government Report:**
```bibtex
@techreport{cbo-2024-defense-budget,
  author = {{Congressional Budget Office}},
  title = {The Outlook for Major Federal Trust Funds: 2024 to 2034},
  institution = {Congressional Budget Office},
  year = {2024},
  url = {https://www.cbo.gov/...}
}
```

## Source Quality Criteria

**High Confidence:**
- Government statistics (WHO, SIPRI, CDC, BLS)
- Peer-reviewed academic papers
- Systematic reviews and meta-analyses

**Medium Confidence:**
- Reputable think tanks (Brookings, RAND)
- Major foundations (Gates Foundation, Open Philanthropy)
- Industry reports from established organizations

**Low Confidence:**
- News articles
- Opinion pieces
- Blog posts
- Wikipedia (use as starting point, find primary source)

## Example Workflow

**User adds claim**: "Clinical trials cost $1B on average"

You:
1. Search references.bib: `grep -i "clinical trial cost" references.bib`
2. Not found
3. WebSearch: "clinical trial cost average 2024 academic study"
4. Find: DiMasi et al. (2016) study on drug development costs
5. Add to references.bib:
   ```bibtex
   @article{dimasi-2016-clinical-trial-costs,
     author = {DiMasi, Joseph A. and Grabowski, Henry G. and Hansen, Ronald W.},
     title = {Innovation in the pharmaceutical industry: New estimates of R\&D costs},
     journal = {Journal of Health Economics},
     volume = {47},
     pages = {20--33},
     year = {2016},
     doi = {10.1016/j.jhealeco.2016.01.012},
     note = {Estimated average cost of bringing a new drug to market at \$2.6B (2013 dollars)}
   }
   ```
6. Update text: `Clinical trials cost approximately $1B on average [@dimasi-2016-clinical-trial-costs].`

## Notes

- Always verify facts before adding them
- When in doubt, search for a source
- Prefer citing parameters (which have sources) over making new claims
- Use consistent citation key format: `author-year-topic-kebab-case`
- Escape special characters in BibTeX: `\$`, `\&`, `\%`
- The `note` field is good for storing key quotes/findings
