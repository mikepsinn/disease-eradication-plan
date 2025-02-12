import * as fs from 'fs';
import * as path from 'path';
import { promisify } from 'util';

const writeFile = promisify(fs.writeFile);
const mkdir = promisify(fs.mkdir);
const rm = promisify(fs.rm);
const unlink = promisify(fs.unlink);

describe('Notion Sync', () => {
  const testDir = path.join(__dirname, 'test-files');
  const validMdPath = path.join(testDir, 'valid.md');
  const noFrontmatterPath = path.join(testDir, 'no-frontmatter.md');

  beforeAll(async () => {
    // Clean up any existing test directory
    try {
      await rm(testDir, { recursive: true, force: true });
    } catch (error) {
      // Ignore if directory doesn't exist
    }

    // Create test directory and files
    await mkdir(testDir, { recursive: true });

    // Create a valid markdown file with frontmatter
    const validContent = `---
title: Test Document
description: A test document
published: true
date: 2024-03-20
tags: test
editor: jest
dateCreated: 2024-03-20
---

# Test Content
This is a test document.`;

    // Create a markdown file without frontmatter
    const noFrontmatterContent = `# No Frontmatter
This document has no frontmatter.`;

    await writeFile(validMdPath, validContent);
    await writeFile(noFrontmatterPath, noFrontmatterContent);
  });

  afterAll(async () => {
    // Cleanup test directory and all its contents
    await rm(testDir, { recursive: true, force: true });
  });

  it('should find markdown files', async () => {
    const { getMarkdownFiles } = require('../scripts/notion-sync');
    const files = await getMarkdownFiles(testDir);
    expect(files).toHaveLength(2);
    expect(files.map(f => path.basename(f))).toContain('valid.md');
    expect(files.map(f => path.basename(f))).toContain('no-frontmatter.md');
  });

  it('should extract metadata from valid frontmatter', async () => {
    const { extractMetadataAndContent } = require('../scripts/notion-sync');
    const { metadata, content } = await extractMetadataAndContent(validMdPath);
    
    expect(metadata).toEqual({
      title: 'Test Document',
      description: 'A test document',
      published: true,
      date: '2024-03-20',
      tags: 'test',
      editor: 'jest',
      dateCreated: '2024-03-20'
    });

    expect(content).toContain('# Test Content');
  });

  it('should handle files without frontmatter', async () => {
    const { extractMetadataAndContent } = require('../scripts/notion-sync');
    const { metadata, content } = await extractMetadataAndContent(noFrontmatterPath);
    
    expect(metadata).toHaveProperty('title', 'No Frontmatter');
    expect(metadata).toHaveProperty('published', false);
    expect(metadata).toHaveProperty('description', '');
    expect(content).toContain('# No Frontmatter');
  });

  it('should respect .gitignore patterns', async () => {
    // Create a .gitignore file in test directory
    const gitignorePath = path.join(testDir, '.gitignore');
    await writeFile(gitignorePath, 'ignored.md\n');
    
    // Create an ignored file
    const ignoredPath = path.join(testDir, 'ignored.md');
    await writeFile(ignoredPath, '# Ignored file');

    const { getMarkdownFiles } = require('../scripts/notion-sync');
    const files = await getMarkdownFiles(testDir);
    
    expect(files.map(f => path.basename(f))).not.toContain('ignored.md');

    // Cleanup
    await unlink(gitignorePath);
    await unlink(ignoredPath);
  });
}); 