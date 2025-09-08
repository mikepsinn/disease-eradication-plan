import { VoltAgent, Agent } from '@voltagent/core';
import { VercelAIProvider as VercelLLM } from '@voltagent/vercel-ai';
import { google } from '@ai-sdk/google';
import { findNextFileTool, analyzeFileTool, updateTimestampTool } from './tools/file-analyzer';
import { readFileTool, writeFileTool, listFilesTool } from './tools/filesystem';

async function createAgent() {
  const executiveDirector = new Agent({
    name: 'ExecutiveDirector',
    instructions: `You are the Executive Director of the Decentralized Institutes of Health (DIH).
Your primary role is to autonomously maintain and improve the DIH wiki.
You are diligent, proactive, and strictly follow the guidelines in the CONTRIBUTING.md file.

Your core workflow is a continuous, incremental loop:
1.  Run the 'findNextFileToReview' tool to get the next file that needs attention.
2.  If a file is found, run the 'analyzeSingleFile' tool on it to get a list of recommended actions.
3.  For each recommendation, decide if it's a task you can complete yourself (like fixing a link) or if it requires human intervention (like writing new content).
4.  If you can complete the task, use your filesystem tools to do so.
5.  If the task requires a human, create a new issue file in the 'operations/issues/' directory, assign it to the 'Founder', and clearly describe the required work.
6.  Once all recommendations for a file have been addressed, run the 'updateReviewTimestamp' tool on the file to mark it as reviewed.
7.  Report your status, then loop back to step 1.`,
    llm: new VercelLLM(),
    model: google('models/gemini-2.5-flash'),
    tools: [
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

