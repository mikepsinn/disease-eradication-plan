# PDF and EPUB Deployment Strategy

## Overview

The book's PDF and EPUB files are now served directly from the website (Netlify) instead of being stored as GitHub Actions artifacts. This approach:

- ✅ **Zero cost** - No GitHub artifact storage fees
- ✅ **Better UX** - Users don't need GitHub account to download
- ✅ **Persistent** - Files don't expire after 30 days
- ✅ **Faster** - Direct download from Netlify CDN
- ✅ **Simpler** - One deployment pipeline for everything

## How It Works

### Build Process

The workflow uses an optimized 3-phase build strategy:

**Phase 1: HTML Sites (Parallel - ~25 min)**
- Main book HTML
- Economics site
- Wishocracy paper
- IAB paper

All build simultaneously using separate jobs for maximum speed.

**Phase 2: PDF + EPUB (Parallel - ~30-40 min)**
After HTML completes:
- PDF builds (reuses HTML's freeze cache)
- EPUB builds (reuses HTML's freeze cache)

Both formats build **in parallel**, not sequentially, saving ~20 minutes.

**Phase 3: Deployment**
- **Netlify** deploys entire `_book/warondisease/` directory
- Includes: HTML site + PDF + EPUB

**Total time: ~65 minutes** (vs 75 min if EPUB waited for PDF)

### Deployment

All files in `_book/warondisease/` are deployed to Netlify at:
- **Website**: https://manual.WarOnDisease.org/
- **PDF**: https://manual.WarOnDisease.org/How-to-End-War-and-Disease.pdf
- **EPUB**: https://manual.WarOnDisease.org/How-to-End-War-and-Disease.epub

### User Access

Download links are in the navbar under "Download Book" dropdown:
- PDF option
- EPUB option

## Configuration

### Quarto Config (`_quarto-book.yml`)

```yaml
format:
  pdf:
    output-file: "How-to-End-War-and-Disease.pdf"
    # ... other PDF settings
    
  epub:
    output-file: "How-to-End-War-and-Disease.epub"
    # ... other EPUB settings
```

### Navbar Links

```yaml
navbar:
  right:
    - icon: file-pdf
      text: "Download Book"
      menu:
        - text: "PDF"
          href: /How-to-End-War-and-Disease.pdf
        - text: "EPUB"
          href: /How-to-End-War-and-Disease.epub
```

## Comparison with Artifacts Approach

| Aspect | GitHub Artifacts (Old) | Website Deployment (New) |
|--------|------------------------|--------------------------|
| **Storage Cost** | ~$10/month | $0 (included in Netlify) |
| **Retention** | 30 days max | Permanent |
| **Access** | Requires GitHub login | Public URL |
| **CDN** | No | Yes (Netlify CDN) |
| **Maintenance** | Manual cleanup needed | Automatic |
| **Build Time** | Same | Same |
| **User Experience** | Complex (GitHub UI) | Simple (direct link) |

## Similar Implementations

This approach is used by other projects in the repository:

### Wishocracy Paper (`_quarto-wishocracy.yml`)
```yaml
format:
  pdf:
    output-file: "wishocracy-rappa-paper.pdf"

navbar:
  right:
    - icon: file-pdf
      text: "Download PDF"
      href: /wishocracy-rappa-paper.pdf
```

Deployed at: https://paper.wishocracy.org/wishocracy-rappa-paper.pdf

### IAB Paper (`_quarto-iab.yml`)
Similar setup for the Incentive Alignment Bonds paper.

## Troubleshooting

### PDFs not showing up?

1. **Check build logs**: Ensure PDF/EPUB generation succeeded
   ```bash
   # Look for these files in build output
   _book/warondisease/How-to-End-War-and-Disease.pdf
   _book/warondisease/How-to-End-War-and-Disease.epub
   ```

2. **Check Netlify deployment**: Verify files are included
   - Go to Netlify dashboard
   - Check "Deploys" → Latest deploy → "Deploy summary"
   - Files should be listed

3. **Check file paths**: URLs are case-sensitive
   - Correct: `/How-to-End-War-and-Disease.pdf`
   - Wrong: `/how-to-end-war-and-disease.pdf`

### Links not working?

1. **Relative vs absolute paths**:
   - In navbar: Use `/filename.pdf` (absolute from root)
   - In markdown: Use relative paths `../filename.pdf`

2. **Clear browser cache**: Hard refresh (Ctrl+Shift+R)

3. **Check Netlify redirects**: Ensure no redirect rules interfere

## Future Enhancements

### Add to Main Page

Consider adding prominent download buttons on `index.qmd`:

### Analytics

Track downloads using Netlify Analytics or custom event tracking:

```html
<a href="/How-to-End-War-and-Disease.pdf" 
   onclick="gtag('event', 'download', {'file_name': 'pdf'})">
   Download PDF
</a>
```

### Multiple Versions

If you need to keep older versions:

```
/How-to-End-War-and-Disease.pdf          # Latest
/archive/How-to-End-War-and-Disease-v1.0.pdf
/archive/How-to-End-War-and-Disease-v0.9.pdf
```

## Migration Complete ✅

- ✅ All artifact uploads removed from workflow
- ✅ 40.83 GB storage cleaned up
- ✅ PDF/EPUB output filenames specified
- ✅ Navbar download links added
- ✅ Files deploy automatically with website
- ✅ $10/month cost savings
- ✅ Better user experience

No further action needed! Files will be available on the website after the next successful build.

