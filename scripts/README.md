# 📁 Scripts Directory

Repository management automation scripts with AI-powered file organization.

## Key Scripts

### [`reorganize.js`](reorganize.js)
- Creates standardized directory structure
- Generates foundational READMEs
- Enforces consistent taxonomy across docs

### [`migrate-content.js`](migrate-content.js) 
- AI-powered content migration engine
- Analyzes file locations using GPT-4
- Validates moves against directory structure
- Batch processes entire repository

### [`file-path-analyzer.js`](file-path-analyzer.js)
- AI classification module
- Returns JSON analysis with:
  - Target directory suggestions
  - Confidence scoring
  - Priority levels
  - Recommended actions (move/delete/flag)

### [`smart-repo-importer.js`](smart-repo-importer.js)
- Repository ingestion system
- Automatic directory tree generation
- AI-assisted file placement
- Legacy content integration

### [`process-images.js`](process-images.js)
- Automated image pipeline:
  1. S3 bucket synchronization
  2. Markdown URL rewriting
  3. Image catalog generation
  4. Local ↔ cloud validation
