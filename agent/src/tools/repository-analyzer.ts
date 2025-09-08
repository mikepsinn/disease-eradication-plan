import { Tool } from '@voltagent/core';
import { glob } from 'glob';
import * as fs from 'fs/promises';
import * as path from 'path';
import matter from 'gray-matter';
import simpleGit from 'simple-git';
import { z } from 'zod';
import * as yaml from 'js-yaml';

interface FileAnalysis {
  filePath: string;
  title: string;
  description: string;
  lastModified: string;
  lastReviewed: string;
  recommendedTodos: string[];
  tags?: string[];
  published?: boolean;
  date?: string;
  dateCreated?: string;
}

interface ContributingStandards {
  frontmatterRequirements: string[];
  contentStandards: {
    [key: string]: RegExp | string[];
  };
  folderStructure: {
    [key: string]: string;
  };
}

async function parseContributingStandards(): Promise<ContributingStandards> {
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
  
  return {
    frontmatterRequirements,
    contentStandards,
    folderStructure
  };
}

export async function analyzeRepository(): Promise<string> {
  const git = simpleGit();
  const projectRoot = process.cwd();
  const files = await glob('**/*.md', {
    ignore: ['node_modules/**', '**/README.md'],
    cwd: projectRoot,
  });
  
  // Parse contributing standards
  const standards = await parseContributingStandards();
  
  // Load milestones for reference
  let milestones: any[] = [];
  try {
    const milestonesPath = path.join(projectRoot, 'operations', 'milestones.yml');
    const milestonesContent = await fs.readFile(milestonesPath, 'utf-8');
    milestones = yaml.load(milestonesContent) as any[] || [];
  } catch (error) {
    console.warn('Could not load milestones:', error);
  }

  const analysisPromises = files.map(async (file): Promise<FileAnalysis | null> => {
    try {
      const filePath = path.join(projectRoot, file);
      const content = await fs.readFile(filePath, 'utf-8');
      const { data, content: bodyContent } = matter(content);

      const log = await git.log({ file: filePath, maxCount: 1 });
      const lastModified = log.latest?.date ? new Date(log.latest.date).toISOString().split('T')[0] : 'N/A';
      
      // Find last review date from git history (if commented with "REVIEW:")
      let lastReviewed = 'N/A';
      try {
        const logs = await git.log({ file: filePath });
        const reviewCommit = logs.all.find(commit => 
          commit.message.includes('REVIEW:') || 
          commit.message.toLowerCase().includes('review'));
        if (reviewCommit) {
          lastReviewed = new Date(reviewCommit.date).toISOString().split('T')[0];
        }
      } catch (error) {
        console.warn(`Could not get review history for ${file}:`, error);
      }

      // Advanced recommendation engine based on CONTRIBUTING.md standards
      const recommendedTodos: string[] = [];

      // Check frontmatter requirements
      standards.frontmatterRequirements.forEach(field => {
        if (!data[field]) {
          recommendedTodos.push(`UPDATE: Missing ${field} in frontmatter`);
        }
      });
      
      // Check content standards
      if (!bodyContent.includes('## Source Quotes') && bodyContent.match(/\d+%|\$\d+|\d+ million|\d+ billion/)) {
        recommendedTodos.push('UPDATE: Contains statistics but missing Source Quotes section');
      }
      
      if (bodyContent.includes('TODO') || bodyContent.includes('FIXME')) {
        recommendedTodos.push('UPDATE: Contains TODO or FIXME markers');
      }
      
      // Check folder structure compliance
      const fileDir = path.dirname(file);
      const topLevelDir = fileDir.split(path.sep)[0];
      
      if (topLevelDir in standards.folderStructure) {
        const expectedContent = standards.folderStructure[topLevelDir];
        if (!bodyContent.includes(expectedContent.toLowerCase())) {
          recommendedTodos.push(`REVIEW: File may be in wrong directory (${topLevelDir})`);
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
          recommendedTodos.push(`FIX: Broken internal link to ${linkPath}`);
        }
      }
      
      // Check for files that haven't been updated in a long time
      const sixMonthsAgo = new Date();
      sixMonthsAgo.setMonth(sixMonthsAgo.getMonth() - 6);
      if (lastModified !== 'N/A' && new Date(lastModified) < sixMonthsAgo) {
        recommendedTodos.push(`REVIEW: File not updated in over 6 months`);
      }
      
      return {
        filePath: file,
        title: data.title || 'No Title',
        description: data.description || 'No Description',
        lastModified,
        lastReviewed,
        recommendedTodos,
        tags: data.tags,
        published: data.published,
        date: data.date,
        dateCreated: data.dateCreated
      };
    } catch (error) {
      console.error(`Error analyzing file ${file}:`, error);
      return null;
    }
  });

  const results = (await Promise.all(analysisPromises)).filter(Boolean) as FileAnalysis[];

  // Sort results by number of recommendations (most issues first)
  results.sort((a, b) => b.recommendedTodos.length - a.recommendedTodos.length);
  
  // Format as a Markdown table
  let table = '| File Path | Title | Description | Last Modified | Last Reviewed | Recommended Todos |\n';
  table += '| --- | --- | --- | --- | --- | --- |\n';
  results.forEach(res => {
    // Truncate description if too long
    const description = res.description.length > 50 ? 
      res.description.substring(0, 47) + '...' : 
      res.description;
      
    table += `| ${res.filePath} | ${res.title} | ${description} | ${res.lastModified} | ${res.lastReviewed} | ${res.recommendedTodos.join('<br/>')} |\n`;
  });
  
  // Add summary statistics
  const totalFiles = results.length;
  const filesWithIssues = results.filter(r => r.recommendedTodos.length > 0).length;
  const totalIssues = results.reduce((sum, r) => sum + r.recommendedTodos.length, 0);
  
  const summary = `
## Repository Health Summary

- **Total Files Analyzed:** ${totalFiles}
- **Files with Issues:** ${filesWithIssues} (${Math.round(filesWithIssues/totalFiles*100)}%)
- **Total Issues Found:** ${totalIssues}
- **Analysis Date:** ${new Date().toISOString().split('T')[0]}

`;
  
  return summary + table;
}

export const repositoryAnalyzerTool = new Tool({
  name: 'repositoryAnalyzer',
  description: 'Analyzes all markdown files in the repository and generates a health report with recommended actions.',
  parameters: z.object({}),
  execute: analyzeRepository,
});
