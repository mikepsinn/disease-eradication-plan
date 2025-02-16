import * as fs from 'fs';
import * as path from 'path';
import { promisify } from 'util';
import { Client } from "@notionhq/client";
import { PageObjectResponse } from "@notionhq/client/build/src/api-endpoints";
import dotenv from 'dotenv';
const { simpleGit } = require('simple-git');

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

console.log("NOTION_DATABASE_ID:", NOTION_DATABASE_ID);

describe('Notion Sync', () => {
  const testDir = path.join(__dirname, 'test-files');
  const notion = new Client({ auth: NOTION_API_KEY });

  beforeAll(async () => {
    // Clean up any existing test directory
    try {
      await rm(testDir, { recursive: true, force: true });
    } catch (error) {
      // Ignore if directory doesn't exist
    }

    // Create test directory
    await mkdir(testDir, { recursive: true });

    // Initialize Git repo
    const git = simpleGit();
    try {
      await git.cwd(testDir);
      await git.init();
      await git.addConfig('user.name', 'Test User');
      await git.addConfig('user.email', 'test@example.com');
    } catch (error) {
      console.warn('Error initializing Git repo:', error);
    }
  });

  afterAll(async () => {
    // Cleanup test directory
    await rm(testDir, { recursive: true, force: true });

    // Clean up Notion test pages
    try {
      const response = await notion.databases.query({
        database_id: NOTION_DATABASE_ID,
        filter: {
          property: "title",
          rich_text: {
            contains: "Problems We Can Solve with a Decentralized FDA"
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
  }, 30000); // 30 second timeout

  it('should properly sync 01-problem.md to Notion', async () => {
    const problemMdPath = path.join(testDir, '01-problem.md');
    const problemContent = `---
description: You and Everyone You Love Will Suffer and Die.
emoji: "💀"
title: Problems We Can Solve with a Decentralized FDA
number: 150k
textFollowingNumber: people die every day from possibly preventable degenerative diseases
tags: global-health, chronic-diseases, preventable-deaths, healthcare-spending
published: true
editor: markdown
date: 2025-02-11T13:38:21.578Z
dateCreated: 2025-02-11T13:38:21.578Z
---
# Problem: You and Everyone You Love Will Suffer and Die

There are over [2 billion](https://www.george-health.com/global-health-challenge/) people suffering from chronic diseases.

Additionally, [150,000](https://www.weforum.org/agenda/2020/05/how-many-people-die-each-day-covid-19-coronavirus/) people die every single day by possibly preventable degenerative diseases. For perspective, this is equivalent to:

* [**FIFTY-ONE**](https://en.wikipedia.org/wiki/Casualties_of_the_September_11_attacks) September 11th attacks every day
* [**NINE**](https://en.wikipedia.org/wiki/Casualties_of_the_September_11_attacks) Holocausts every year

![deaths from disease](https://static.crowdsourcingcures.org/img/deaths-from-disease-vs-deaths-from-terrorism-chart.png)`;

    await writeFile(problemMdPath, problemContent);

    const { createNotionPage, extractMetadataAndContent } = require('../scripts/notion-sync');
    
    // Extract metadata and content
    const { metadata, content } = await extractMetadataAndContent(problemMdPath);
    
    // Verify metadata extraction
    expect(metadata.title).toBe('Problems We Can Solve with a Decentralized FDA');
    expect(metadata.description).toBe('You and Everyone You Love Will Suffer and Die.');
    expect(metadata.published).toBe(true);
    expect(metadata.date).toBe('2025-02-11');
    expect(metadata.tags).toBe('global-health, chronic-diseases, preventable-deaths, healthcare-spending');
    expect(metadata.editor).toBe('markdown');
    expect(metadata.dateCreated).toBe('2025-02-11');
    
    // Create the page in Notion
    const page = await createNotionPage(metadata, content);
    expect(page).toBeDefined();
    
    // Get the blocks
    const blocks = await notion.blocks.children.list({ block_id: page.id });
    
    // Verify content structure
    const blockTypes = blocks.results.map((block: any) => block.type);
    
    // Should have: heading_1, paragraph (with link), paragraph (with link), paragraph (intro), bulleted_list_item (x2), paragraph (spacing), image
    expect(blockTypes).toEqual([
      'heading_1',
      'paragraph',
      'paragraph',
      'paragraph',
      'bulleted_list_item',
      'bulleted_list_item',
      'paragraph',
      'image'
    ]);

    // Verify heading content
    const heading = blocks.results[0] as any;
    expect(heading.heading_1.rich_text[0].plain_text).toBe('Problem: You and Everyone You Love Will Suffer and Die');

    // Verify bullet points
    const bulletPoint1 = blocks.results[4] as any;
    const bulletPoint2 = blocks.results[5] as any;
    expect(bulletPoint1.bulleted_list_item.rich_text[0].plain_text).toContain('FIFTY-ONE');
    expect(bulletPoint2.bulleted_list_item.rich_text[0].plain_text).toContain('NINE');

    // Verify image
    const image = blocks.results[7] as any;
    expect(image.type).toBe('image');
    expect(image.image.external.url).toBe('https://static.crowdsourcingcures.org/img/deaths-from-disease-vs-deaths-from-terrorism-chart.png');

    // Cleanup
    await unlink(problemMdPath);
  }, 30000); // 30 second timeout
}); 