---
name: require-citation-urls
enabled: true
event: file
conditions:
  - field: file_path
    operator: ends_with
    pattern: references.bib
  - field: new_text
    operator: regex_match
    pattern: "@(article|misc|techreport|online|webpage|inproceedings)"
---

⚠️ **Citation URL Requirement**

You're adding a citation to references.bib. **Every citation should have a verifiable URL.**

## Required Steps

### 1. Add URL Field
Ensure your BibTeX entry includes:
```bibtex
url = {https://...},
urldate = {2026-01-26},
```

Or a DOI (which is even better):
```bibtex
doi = {10.xxxx/...},
```

### 2. Verify URL Contains Claimed Content
Before finalizing, use WebFetch to verify the URL actually supports the claims:

```
Use WebFetch to check: [URL]
Prompt: "Does this source support the claim that [CLAIM FROM ABSTRACT]?"
```

### 3. URL Priority by Source Type

| Source Type | Best URL | Fallback |
|-------------|----------|----------|
| Journal article | DOI link | Publisher page |
| Book | Publisher page | WorldCat/Amazon |
| Report | Official PDF | Archive.org |
| News article | Original URL | Archive.org |
| Dataset | Repository URL | Documentation |

### 4. Handle Paywalled Sources
If source is paywalled:
- Still include the DOI/publisher URL
- Note in `abstract` field: "Full text requires subscription"
- Consider linking to preprint (arXiv, SSRN) if available

## Example Complete Entry

```bibtex
@article{smith2024,
  title = {Example Study Title},
  author = {Smith, John and Doe, Jane},
  year = {2024},
  journal = {Journal Name},
  volume = {10},
  pages = {1-15},
  doi = {10.1234/example.2024},
  url = {https://doi.org/10.1234/example.2024},
  urldate = {2026-01-26},
  abstract = {Summary of key findings relevant to our use of this source.},
}
```

**Remember:** A citation without a verifiable URL reduces credibility. Take 30 seconds to add and verify the link.
