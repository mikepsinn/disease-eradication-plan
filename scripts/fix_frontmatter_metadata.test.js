const fs = require('fs').promises;
const path = require('path');
const { validateMarkdownFiles, findMarkdownFiles } = require('./fix_frontmatter_metadata');

describe('validateMarkdownFiles', () => {
  it('should not include causal-inference-analysis.md in invalid files', async () => {
    // Get actual files from repo
    const repoRoot = path.resolve(__dirname, '..');
    const markdownFiles = await findMarkdownFiles(repoRoot);
    
    // Run validation on actual files
    const invalidFiles = await validateMarkdownFiles(markdownFiles);
    
    // Get paths relative to repo root for easier debugging
    const relativeInvalidPaths = invalidFiles.map(f => path.relative(repoRoot, f.path));
    
    // Verify causal-inference-analysis.md is not in invalid files
    expect(relativeInvalidPaths).not.toContain('analytics/causal-inference-analysis.md');
    
    // Log invalid files for visibility
    console.log('\nInvalid files found:', relativeInvalidPaths);
  });
}); 