import { VoltAgent, Agent, Tool } from '@voltagent/core';
import { VercelAIProvider as VercelLLM } from '@voltagent/vercel-ai';
import { google } from '@ai-sdk/google';
import { repositoryAnalyzerTool } from './tools/repository-analyzer';
import * as fs from 'fs/promises';
import * as path from 'path';
import { readFileTool, writeFileTool, listFilesTool } from './tools/filesystem';
import { z } from 'zod';

// Use an async IIFE to handle top-level await
async function createAgent() {
  // 2. Define the Executive Director Agent
  const executiveDirector = new Agent({
    name: 'ExecutiveDirector',
    instructions: `You are the Executive Director of the Decentralized Institutes of Health (DIH).
Your primary role is to autonomously maintain and improve the DIH wiki.
You are diligent, proactive, and strictly follow the guidelines in the CONTRIBUTING.md file.

Your core workflow is as follows:
1.  Run the 'repositoryAnalyzer' tool to get a comprehensive health report of the repository.
2.  Use the 'updateRepositoryHealthReport' tool to update the report in 'operations/repository-health-report.md' with the analysis results.
3.  Analyze the "Recommended Todos" from the report. For each actionable item, create a new issue file in the 'operations/issues/' directory to document the planned work.
4.  When creating new issues, follow these guidelines:
    - Use the next available issue number
    - Follow the naming convention: '{number}-{slugified-title}.md'
    - Include proper frontmatter with number, title, state, assignees, labels, and milestone
    - Provide a clear description of the issue and steps to resolve it
5.  Execute the tasks outlined in the issues you've created, using your file system tools to read, write, and list files as needed.
6.  When a task is complete, update the corresponding issue's frontmatter to set its state to 'closed' and add a 'closed_at' timestamp.
7.  Report your status. If you have no open issues, state that you are scanning for new tasks.`,
    llm: new VercelLLM(),
    model: google('models/gemini-2.5-flash'),
    tools: [
      repositoryAnalyzerTool,
      readFileTool,
      writeFileTool,
      listFilesTool,
      new Tool({
        name: 'updateRepositoryHealthReport',
        description: 'Updates the repository health report with the latest analysis results',
        parameters: z.object({
          reportContent: z.string().describe('The content to add to the report'),
        }),
        execute: async ({ reportContent }) => {
          try {
            const reportPath = path.join(process.cwd(), 'operations', 'repository-health-report.md');
            let fileContent = await fs.readFile(reportPath, 'utf-8');
            
            // Replace placeholders
            const currentDate = new Date().toISOString().split('T')[0];
            fileContent = fileContent.replace('<!-- DATE_PLACEHOLDER -->', currentDate);
            fileContent = fileContent.replace('<!-- REPORT_CONTENT_PLACEHOLDER -->', reportContent);
            
            await fs.writeFile(reportPath, fileContent, 'utf-8');
            return { success: true, message: 'Repository health report updated successfully.' };
          } catch (error: any) {
            console.error('Error updating repository health report:', error);
            return { success: false, message: `Error updating report: ${error.message}` };
          }
        },
      }),
    ],
  });

  // 4. Define the main VoltAgent application
  return new VoltAgent({
    agents: {
      executiveDirector,
    },
  });
}

export const DIH = await createAgent();

