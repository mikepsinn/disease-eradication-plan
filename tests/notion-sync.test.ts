import * as fs from 'fs';
import * as path from 'path';
import { promisify } from 'util';
import { Client } from "@notionhq/client";
import { PageObjectResponse } from "@notionhq/client/build/src/api-endpoints";
import dotenv from 'dotenv';

dotenv.config();

const writeFile = promisify(fs.writeFile);
const readFile = promisify(fs.readFile);
const mkdir = promisify(fs.mkdir);
const rm = promisify(fs.rm);
const unlink = promisify(fs.unlink);

// Ensure we have the required environment variables
const NOTION_API_KEY = process.env.NOTION_API_KEY;
const NOTION_DATABASE_ID = process.env.NOTION_DATABASE_ID;

if (!NOTION_API_KEY || !NOTION_DATABASE_ID) {
  throw new Error('Missing required environment variables: NOTION_API_KEY and NOTION_DATABASE_ID');
}

describe('Notion Sync', () => {
  const testDir = path.join(__dirname, 'test-files');
  const validMdPath = path.join(testDir, 'valid.md');
  const noFrontmatterPath = path.join(testDir, 'no-frontmatter.md');
  const notion = new Client({ auth: NOTION_API_KEY });

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
title: Test Sync Document
description: A test document for syncing
published: true
date: 2024-03-20
tags: test, sync
editor: jest
dateCreated: 2024-03-20
---

# Test Content
This is a test document for syncing.`;

    // Create a markdown file without frontmatter
    const noFrontmatterContent = `# No Frontmatter
This document has no frontmatter.`;

    await writeFile(validMdPath, validContent);
    await writeFile(noFrontmatterPath, noFrontmatterContent);
  });

  afterAll(async () => {
    // Cleanup test directory and all its contents
    await rm(testDir, { recursive: true, force: true });

    // Clean up Notion test pages
    try {
      const response = await notion.databases.query({
        database_id: NOTION_DATABASE_ID,
        filter: {
          property: "title",
          rich_text: {
            contains: "Test Sync Document"
          }
        }
      });

      for (const page of response.results) {
        await notion.pages.update({
          page_id: page.id,
          archived: true
        });
      }
    } catch (error) {
      console.error('Error cleaning up Notion pages:', error);
    }
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
      title: 'Test Sync Document',
      description: 'A test document for syncing',
      published: true,
      date: '2024-03-20',
      tags: 'test, sync',
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

  describe('Bidirectional Sync', () => {
    beforeAll(async () => {
      // Ensure database has required properties
      const { ensureDatabaseProperties } = require('../scripts/notion-sync');
      await ensureDatabaseProperties();
    });

    it('should create a new page in Notion from markdown', async () => {
      const { createNotionPage, extractMetadataAndContent } = require('../scripts/notion-sync');
      
      // First extract the metadata and content
      const { metadata, content } = await extractMetadataAndContent(validMdPath);
      
      // Create the page in Notion
      await createNotionPage(metadata, content);
      
      // Verify the page was created
      const response = await notion.databases.query({
        database_id: NOTION_DATABASE_ID,
        filter: {
          property: "title",
          rich_text: {
            equals: metadata.title
          }
        }
      });
      
      expect(response.results).toHaveLength(1);
      const page = response.results[0] as PageObjectResponse;
      const titleProperty = page.properties.title as { title: Array<{ plain_text: string }> };
      const descriptionProperty = page.properties.description as { rich_text: Array<{ plain_text: string }> };
      const publishedProperty = page.properties.published as { checkbox: boolean };
      
      expect(titleProperty.title[0].plain_text).toBe(metadata.title);
      expect(descriptionProperty.rich_text[0].plain_text).toBe(metadata.description);
      expect(publishedProperty.checkbox).toBe(metadata.published);
    });

    it('should update markdown file from Notion changes', async () => {
      const { updateMarkdownFile, getNotionPageByTitle } = require('../scripts/notion-sync');
      
      // Get the test page from Notion
      const notionPage = await getNotionPageByTitle('Test Sync Document');
      expect(notionPage).not.toBeNull();

      // Update the page in Notion
      const updatedTitle = 'Updated Test Document';
      await notion.pages.update({
        page_id: notionPage.id,
        properties: {
          title: { 
            title: [{ text: { content: updatedTitle } }]
          },
          description: {
            rich_text: [{ text: { content: 'Updated description' } }]
          }
        }
      });

      // Create a new test file to update
      const testFilePath = path.join(testDir, 'to-update.md');
      await writeFile(testFilePath, 'Initial content');

      // Update the markdown file from Notion
      const updatedPage = await getNotionPageByTitle(updatedTitle);
      await updateMarkdownFile(testFilePath, updatedPage);

      // Read and verify the updated file
      const updatedContent = await readFile(testFilePath, 'utf-8');
      expect(updatedContent).toContain('title: Updated Test Document');
      expect(updatedContent).toContain('description: Updated description');

      // Cleanup
      await unlink(testFilePath);
    });
  });
}); 