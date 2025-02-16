const path = require('path');
const fs = require('fs').promises;
const matter = require('gray-matter');
const { FrontmatterGenerator, validateMarkdownFiles, findMarkdownFiles } = require('./fix_frontmatter_metadata');
const LLMClient = require('./llm-client');

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

describe('FrontmatterGenerator', () => {
  it('should generate tags when frontmatter has empty tags field', async () => {
    // Create test file content
    const testContent = `---
title: 05. 🏨 Organization 
description: The DAO will utilize Laboratory working groups which use a scientific experimentation-based approach to effectively carrying out the will of its Citizen Scientist voting members.
published: true
date: 2022-08-25T17:02:39.027Z
tags: 
editor: markdown
dateCreated: 2022-07-27T21:26:27.705Z
---

# Organization

The DAO will utilize Laboratory working groups which use a scientific experimentation-based approach.`;

    const testFilePath = path.join(__dirname, 'test-organization.md');
    
    try {
      // Write test file
      await fs.writeFile(testFilePath, testContent);
      
      // Process the file
      const llmClient = new LLMClient();
      const generator = new FrontmatterGenerator(llmClient);
      const result = await generator.processFile(testFilePath);
      
      // Read the processed file
      const processedContent = await fs.readFile(testFilePath, 'utf8');
      const { data: processedFrontmatter } = matter(processedContent);
      
      // Verify tags were generated
      expect(result.updated).toBe(true);
      expect(processedFrontmatter.tags).toBeTruthy();
      expect(processedFrontmatter.tags).not.toBe('');
      expect(processedFrontmatter.tags.length).toBeGreaterThan(0);
      
      console.log('Generated tags:', processedFrontmatter.tags);
    } finally {
      // Cleanup
      try {
        await fs.unlink(testFilePath);
      } catch (error) {
        // Ignore cleanup errors
      }
    }
  });
}); 