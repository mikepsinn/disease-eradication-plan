import { Tool } from '@voltagent/core';
import { glob } from 'glob';
import * as fs from 'fs/promises';
import * as path from 'path';
import matter from 'gray-matter';
import simpleGit from 'simple-git';
import { z } from 'zod';
import * as yaml from 'js-yaml';

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

// --- New Tool Implementations ---

async function findNextFileToReview(): Promise<string> {
  const git = simpleGit();
  const files = await glob('**/*.md', { ignore: 'node_modules/**' });

  for (const file of files) {
    try {
      const content = await fs.readFile(file, 'utf-8');
      const { data } = matter(content);
      const log = await git.log({ file, maxCount: 1 });
      
      const lastModified = log.latest?.date ? new Date(log.latest.date) : new Date(0);
      const lastReviewed = data.lastReviewed ? new Date(data.lastReviewed) : new Date(0);

      if (lastModified > lastReviewed) {
        return `File to review: ${file}`;
      }
    } catch (error) {
      continue;
    }
  }
  return 'No files need reviewing.';
}

async function analyzeSingleFile({ filePath }: { filePath: string }): Promise<FileAnalysisResult> {
  const recommendations: string[] = [];
  const standards = await parseContributingStandards();
  const projectRoot = process.cwd();

  try {
    const content = await fs.readFile(filePath, 'utf-8');
    const { data, content: bodyContent } = matter(content);

    const log = await simpleGit().log({ file: filePath, maxCount: 1 });
    const lastModified = log.latest?.date ? new Date(log.latest.date).toISOString().split('T')[0] : 'N/A';
    
    // Find last review date from git history (if commented with "REVIEW:")
    let lastReviewed = 'N/A';
    try {
      const logs = await simpleGit().log({ file: filePath });
      const reviewCommit = logs.all.find(commit => 
        commit.message.includes('REVIEW:') || 
        commit.message.toLowerCase().includes('review'));
      if (reviewCommit) {
        lastReviewed = new Date(reviewCommit.date).toISOString().split('T')[0];
      }
    } catch (error) {
      console.warn(`Could not get review history for ${filePath}:`, error);
    }

    // Advanced recommendation engine based on CONTRIBUTING.md standards
    standards.frontmatterRequirements.forEach(field => {
      if (!data[field]) {
        recommendations.push(`UPDATE: Missing ${field} in frontmatter`);
      }
    });
    
    if (!bodyContent.includes('## Source Quotes') && bodyContent.match(/\d+%|\$\d+|\d+ million|\d+ billion/)) {
      recommendations.push('UPDATE: Contains statistics but missing Source Quotes section');
    }
    
    if (bodyContent.includes('TODO') || bodyContent.includes('FIXME')) {
      recommendations.push('UPDATE: Contains TODO or FIXME markers');
    }
    
    // Check folder structure compliance
    const fileDir = path.dirname(filePath);
    const topLevelDir = fileDir.split(path.sep)[0];
    
    if (topLevelDir in standards.folderStructure) {
      const expectedContent = standards.folderStructure[topLevelDir];
      if (!bodyContent.includes(expectedContent.toLowerCase())) {
        recommendations.push(`REVIEW: File may be in wrong directory (${topLevelDir})`);
      }
    }
    
    // Check for broken internal links
    const internalLinkRegex = /\[.*?\]\((\.\.\/.*?)\)/g;
    let linkMatch;
    while ((linkMatch = internalLinkRegex.exec(bodyContent)) !== null) {
      const linkPath = linkMatch[1];
      const absoluteLinkPath = path.resolve(path.dirname(filePath), linkPath);
      try {
        await fs.access(absoluteLinkPath);
      } catch (error) {
        recommendations.push(`FIX: Broken internal link to ${linkPath}`);
      }
    }
    
    // Check for files that haven't been updated in a long time
    const sixMonthsAgo = new Date();
    sixMonthsAgo.setMonth(sixMonthsAgo.getMonth() - 6);
    if (lastModified !== 'N/A' && new Date(lastModified) < sixMonthsAgo) {
      recommendations.push(`REVIEW: File not updated in over 6 months`);
    }
    
    return { filePath, recommendations };
  } catch (error: any) {
    console.error(`[Analyzer] Error analyzing file ${filePath}:`, error.message);
    return { filePath, recommendations: [`Error analyzing file: ${error.message}`] };
  }
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
  description: 'Finds the next markdown file that needs to be reviewed based on its git modification date and `lastReviewed` frontmatter.',
  parameters: z.object({}),
  execute: findNextFileToReview,
});

export const analyzeFileTool = new Tool({
  name: 'analyzeSingleFile',
  description: 'Analyzes a single markdown file for issues based on CONTRIBUTING.md and returns a list of recommendations.',
  parameters: z.object({
    filePath: z.string().describe('The path to the file to analyze.'),
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
