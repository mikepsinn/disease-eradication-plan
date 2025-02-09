const fs = require('fs').promises;
const path = require('path');
const os = require('os');
const {
  FrontmatterSchema,
  processFile,
  generateFrontmatterObject,
} = require('../fix_frontmatter_metadata');

// Mock LLMClient
class MockLLMClient {
  async analyzeLocation(_, prompt) {
    return {
      number: '41k',
      textFollowingNumber: 'cost per participant in traditional clinical trials',
      description: 'Analysis of the high costs in traditional clinical trials',
      emoji: '💰',
      title: 'Clinical Trial Costs Analysis',
      tags: ['clinical-trials', 'costs', 'research'],
      source: 'https://example.com/clinical-trials-cost'
    };
  }
}

describe('Frontmatter Metadata Tests', () => {
  let tempDir;
  let mockLLMClient;

  beforeEach(async () => {
    // Create temp directory for test files
    tempDir = await fs.mkdtemp(path.join(os.tmpdir(), 'frontmatter-test-'));
    mockLLMClient = new MockLLMClient();
  });

  afterEach(async () => {
    // Cleanup temp directory
    await fs.rm(tempDir, { recursive: true, force: true });
  });

  test('FrontmatterSchema validates correct data', () => {
    const validData = {
      number: '41k',
      textFollowingNumber: 'cost per participant in traditional clinical trials',
      description: 'Test description',
      emoji: '📊',
      title: 'Test Title',
      published: true,
      date: new Date().toISOString(),
      tags: ['test', 'validation'],
      editor: 'markdown',
      dateCreated: new Date().toISOString()
    };

    const result = FrontmatterSchema.safeParse(validData);
    expect(result.success).toBe(true);
  });

  test('FrontmatterSchema catches invalid data', () => {
    const invalidData = {
      // Missing required fields
      title: 'Test Title',
      published: 'not-a-boolean', // Wrong type
      date: 'not-a-date', // Invalid date format
    };

    const result = FrontmatterSchema.safeParse(invalidData);
    expect(result.success).toBe(false);
    expect(result.error).toBeDefined();
  });

  test('generateFrontmatterObject returns valid metadata', async () => {
    const content = `# Test Content
    This is a test markdown file discussing the cost of $41k per participant
    in clinical trials. [Source](https://example.com/clinical-trials-cost)
    `;

    const result = await generateFrontmatterObject(content, mockLLMClient);
    expect(result).toMatchObject({
      number: expect.any(String),
      textFollowingNumber: expect.any(String),
      description: expect.any(String),
      emoji: expect.any(String),
      title: expect.any(String),
      tags: expect.any(Array)
    });
  });

  test('processFile handles valid markdown file', async () => {
    const testFile = path.join(tempDir, 'test.md');
    const validContent = `---
title: Test Title
description: Test description
emoji: 📊
published: true
date: ${new Date().toISOString()}
dateCreated: ${new Date().toISOString()}
---
# Test Content
    `;

    await fs.writeFile(testFile, validContent);
    await processFile(testFile, mockLLMClient);

    const processedContent = await fs.readFile(testFile, 'utf8');
    expect(processedContent).toContain('title: Test Title');
  });

  test('processFile fixes invalid markdown file', async () => {
    const testFile = path.join(tempDir, 'invalid.md');
    const invalidContent = `---
title: Test Title
# Missing required fields
---
# Test Content about clinical trials
The cost per participant is $41k in traditional trials.
    `;

    await fs.writeFile(testFile, invalidContent);
    await processFile(testFile, mockLLMClient);

    const processedContent = await fs.readFile(testFile, 'utf8');
    expect(processedContent).toContain('description:');
    expect(processedContent).toContain('emoji:');
  });

  test('processFile handles files without frontmatter', async () => {
    const testFile = path.join(tempDir, 'no-frontmatter.md');
    const content = `# Test Content
This is a markdown file without any frontmatter.
    `;

    await fs.writeFile(testFile, content);
    await processFile(testFile, mockLLMClient);

    const processedContent = await fs.readFile(testFile, 'utf8');
    expect(processedContent).toContain('---');
    expect(processedContent).toContain('title:');
    expect(processedContent).toContain('description:');
  });
}); 