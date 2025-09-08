import { Agent } from '@voltagent/core';
import { VercelAIProvider } from '@voltagent/vercel-ai';
import { google } from '@ai-sdk/google';

// The 'Agent' class is the correct primitive for use in workflows.
export const executiveDirectorAgent = new Agent({
  id: 'executive-director-agent',
  llm: new VercelAIProvider(),
  model: google('models/gemini-1.5-flash'),
  systemPrompt: `
    You are the Executive Director of the Decentralized Institutes of Health.
    Your primary responsibility is to analyze repository files and provide a clear, actionable plan for maintenance.
    You will be given the content of a single file, its path, and a comprehensive index of the entire repository for context.
    Your analysis must be sharp and strategic, aligning with the project's core mission: establishing the DIH and funding it via the 1% Treaty.
    Based on your analysis, you must return a structured plan with a clear decision.
  `,
});
