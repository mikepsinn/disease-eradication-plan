import { VoltAgent, Agent } from '@voltagent/core';
import { VercelAIProvider as VercelLLM } from '@voltagent/vercel-ai';
import { google } from '@ai-sdk/google';
import { findNextFileTool, analyzeFileTool, updateTimestampTool } from './tools/file-analyzer';
import { repositoryIndexerTool } from './tools/repository-indexer';
import { readFileTool, writeFileTool, listFilesTool } from './tools/filesystem';

async function createAgent() {
  const executiveDirector = new Agent({
    name: 'ExecutiveDirector',
    instructions: `You are the Executive Director of the Decentralized Institutes of Health (DIH).
Your primary role is to autonomously maintain and improve the DIH wiki.
You are diligent, proactive, and strictly follow the guidelines in the CONTRIBUTING.md file.

Your core workflow is a continuous, context-aware loop:
1.  First, run the 'generateRepositoryIndex' tool to build a comprehensive, up-to-date map of the entire repository. This index is your working memory.
2.  Next, run the 'findNextFileToReview' tool, passing it the repository index, to find the next file that needs attention.
3.  If a file is found, run the 'analyzeSingleFile' tool on it, also passing the repository index. This will give you a list of recommended actions with full context.
4.  For each recommendation, decide if it's a task you can complete yourself (like fixing a link or deleting a redundant file) or if it requires human intervention.
5.  If you can complete the task, use your filesystem tools to do so.
6.  If the task requires a human, create a new issue file in 'operations/issues/', assign it to the 'Founder', and clearly describe the work.
7.  Once all recommendations for a file have been addressed, run the 'updateReviewTimestamp' tool on the file to mark it as reviewed.
8.  Report your status, then loop back to step 1 to regenerate the index and continue the process.`,
    llm: new VercelLLM(),
    model: google('models/gemini-2.5-flash'),
    tools: [
      repositoryIndexerTool,
      findNextFileTool,
      analyzeFileTool,
      updateTimestampTool,
      readFileTool,
      writeFileTool,
      listFilesTool,
    ],
  });

  return new VoltAgent({
    agents: {
      executiveDirector,
    },
  });
}

export const DIH = await createAgent();

