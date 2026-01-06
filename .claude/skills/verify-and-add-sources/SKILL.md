---
name: verify-and-add-sources
description: Verifies claims have proper citations, searches for sources if needed, and adds them to references.qmd. Use when making factual claims or adding statistics.
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
cd knowledge
grep -i "keyword" references.qmd
```

Check if the source already exists in `knowledge/references.qmd`.

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

### 5. Add to references.qmd

Add new source to `knowledge/references.qmd`:

```markdown
## Military Spending and Economics

### sipri-2024-military-spending
- **Title**: World Military Expenditure 2024
- **Author**: SIPRI (Stockholm International Peace Research Institute)
- **Date**: 2024
- **URL**: https://www.sipri.org/...
- **Summary**: Global military spending reached $2.2 trillion in 2024...
```

### 6. Cite in Text

Add citation to the claim:
```markdown
Global military spending is $2.2T [@sipri-2024-military-spending].
```

## Reference Format

Use this structure for `references.qmd`:

```markdown
### reference-id-kebab-case
- **Title**: Full title of source
- **Author**: Author(s) or organization
- **Date**: Publication date
- **URL**: Direct link to source
- **DOI**: (if available)
- **Summary**: Brief 1-2 sentence summary of key finding
- **Confidence**: high/medium/low (based on source quality)
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
1. Search references.qmd: `grep -i "clinical trial cost" knowledge/references.qmd`
2. Not found
3. WebSearch: "clinical trial cost average 2024 academic study"
4. Find: DiMasi et al. (2016) study on drug development costs
5. Add to references.qmd:
   ```markdown
   ### dimasi-2016-clinical-trial-costs
   - **Title**: Innovation in the pharmaceutical industry: New estimates of R&D costs
   - **Author**: DiMasi JA, Grabowski HG, Hansen RW
   - **Date**: 2016
   - **Journal**: Journal of Health Economics, 47:20-33
   - **DOI**: 10.1016/j.jhealeco.2016.01.012
   - **Summary**: Estimated average cost of bringing a new drug to market at $2.6B (2013 dollars), including clinical trial costs
   - **Confidence**: high
   ```
6. Update text: `Clinical trials cost approximately $1B on average [@dimasi-2016-clinical-trial-costs].`

## Notes

- Always verify facts before adding them
- When in doubt, search for a source
- Prefer citing parameters (which have sources) over making new claims
- Keep references.qmd organized by topic
- Use consistent reference ID format: `author-year-topic-kebab-case`
