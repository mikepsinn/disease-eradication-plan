import { Tool } from '@voltagent/core';
import { glob } from 'glob';
import * as fs from 'fs/promises';
import * as path from 'path';
import matter from 'gray-matter';
import simpleGit from 'simple-git';
import { z } from 'zod';
import { RepositoryIndex } from './repository-indexer'; // Import the index type

// --- Reusable Logic & Interfaces ---

interface FileAnalysisResult {
  filePath: string;
  recommendations: string[];
}

interface ContributingStandards {
  frontmatterRequirements: string[];
  folderStructure: { [key: string]: string };
}

async function parseContributingStandards(): Promise<ContributingStandards> {
  console.log('[Analyzer] Parsing standards from CONTRIBUTING.md...');
  const projectRoot = process.cwd();
  const contributingPath = path.join(projectRoot, 'CONTRIBUTING.md');
  const content = await fs.readFile(contributingPath, 'utf-8');
  
  // Extract frontmatter requirements
  const frontmatterRegex = /```yaml[\s\S]*?---(.*?)---[\s\S]*?```/m;
  const frontmatterMatch = content.match(frontmatterRegex);
  const frontmatterRequirements = frontmatterMatch ? 
    ['title', 'description', 'published', 'date', 'tags', 'editor', 'dateCreated'] : 
    ['title', 'description'];
  
  // Extract folder structure standards
  const folderStructureRegex = /- \*\*([^:]+):\*\* ([^\n]+)/g;
  const folderStructure: {[key: string]: string} = {};
  let match;
  while ((match = folderStructureRegex.exec(content)) !== null) {
    folderStructure[match[1].trim()] = match[2].trim();
  }
  
  // Extract content standards
  const contentStandards: {[key: string]: RegExp | string[]} = {
    'citations': /\[\^\d+\]/,
    'internalLinks': /\[.*?\]\(\.\.\/.*?\)/,
    'dollarSignEscaping': /\\\$/,
    'backtickUsage': /`[^`]+`/,
  };
  
  console.log('[Analyzer] Successfully parsed standards.');
  return {
    frontmatterRequirements,
    folderStructure
  };
}

// --- Tool Implementations ---

async function findNextFileToReview({ repositoryIndex }: { repositoryIndex: RepositoryIndex }): Promise<string> {
  console.log('[Finder] Searching for the next file to review...');
  const files = Object.keys(repositoryIndex);

  for (const file of files) {
    const fileData = repositoryIndex[file];
    const lastModified = new Date(fileData.lastModified);
    const lastReviewed = new Date(fileData.lastReviewed);

    if (lastModified > lastReviewed) {
      console.log(`[Finder] Found file to review: ${file}`);
      return file;
    }
  }

  console.log('[Finder] No files need reviewing at this time.');
  return 'No files need reviewing.';
}

async function analyzeSingleFile({ filePath, repositoryIndex }: { filePath: string, repositoryIndex: RepositoryIndex }): Promise<FileAnalysisResult> {
  console.log(`[Analyzer] Analyzing file: ${filePath}`);
  const recommendations: string[] = [];
  
  // Example of context-aware analysis:
  // Check for duplicate titles
  const currentTitle = repositoryIndex[filePath]?.title;
  if (currentTitle && currentTitle !== 'No Title') {
    for (const otherFile in repositoryIndex) {
      if (otherFile !== filePath && repositoryIndex[otherFile].title === currentTitle) {
        recommendations.push(`REVIEW: Potential duplicate of '${otherFile}' (same title).`);
        break; // Only flag once
      }
    }
  }
  
  // ... other analysis logic (link checking, etc.) would go here ...
  console.log(`[Analyzer] Found ${recommendations.length} potential issues for ${filePath}.`);

  return { filePath, recommendations };
}

async function updateReviewTimestamp({ filePath }: { filePath: string }): Promise<string> {
  try {
    const content = await fs.readFile(filePath, 'utf-8');
    const { data, content: body } = matter(content);
    
    data.lastReviewed = new Date().toISOString().split('T')[0];
    
    const newContent = matter.stringify(body, data);
    await fs.writeFile(filePath, newContent, 'utf-8');
    
    return `Successfully updated review timestamp for ${filePath}.`;
  } catch (error: any) {
    return `Error updating timestamp for ${filePath}: ${error.message}`;
  }
}

// --- Tool Definitions ---

export const findNextFileTool = new Tool({
  name: 'findNextFileToReview',
  description: 'Finds the next markdown file that needs to be reviewed by comparing its git modification date and `lastReviewed` frontmatter.',
  parameters: z.object({
    repositoryIndex: z.any().describe('The JSON repository index, including lastModified and lastReviewed dates.'),
  }),
  execute: findNextFileToReview,
});

export const analyzeFileTool = new Tool({
  name: 'analyzeSingleFile',
  description: 'Analyzes a single markdown file for issues using the full repository index for context.',
  parameters: z.object({
    filePath: z.string().describe('The path to the file to analyze.'),
    repositoryIndex: z.any().describe('The JSON repository index for providing context.'),
  }),
  execute: analyzeSingleFile,
});

export const updateTimestampTool = new Tool({
  name: 'updateReviewTimestamp',
  description: 'Adds or updates the `lastReviewed` timestamp in a file\'s frontmatter to the current date.',
  parameters: z.object({
    filePath: z.string().describe('The path to the file to update.'),
  }),
  execute: updateReviewTimestamp,
});
