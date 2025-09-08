import { VoltAgent, Agent, Memories, MCPConfiguration } from '@voltagent/core';
import { VercelAIProvider as VercelLLM } from '@voltagent/vercel-ai';
import { google } from '@ai-sdk/google';

// 1. Configure the MCP Filesystem Server
// This will securely provide our agent with file system tools.
const fileTools = new MCPConfiguration({
  name: 'filesystem',
  command: 'npx',
  args: ['-y', '@modelcontextprotocol/server-filesystem', '.'], // Lock to the current directory
});

// Use an async IIFE to handle top-level await
async function createAgent() {
  // 2. Define the Executive Director Agent
  const executiveDirector = new Agent({
    name: 'ExecutiveDirector',
    instructions: `You are the Executive Director of the Decentralized Institutes of Health (DIH).
Your primary role is to manage the DIH wiki and its associated project management files.
You are diligent, autonomous, and strictly follow the guidelines in the CONTRIBUTING.md file.

Your core workflow is as follows:
1.  Identify the next open issue assigned to you in the 'operations/issues/' directory.
2.  Use your file system tools to read the issue file and understand the task.
3.  Execute the task, using your tools to read, write, and list files as needed.
4.  When the task is complete, update the issue's frontmatter to set its state to 'closed' and add a 'closed_at' timestamp.
5.  Report your status. If you have no open issues, state that you are standing by.`,
    llm: new VercelLLM(),
    model: google('models/gemini-1.5-flash'),
    // 3. Dynamically load the tools from the MCP server
    tools: await fileTools.getTools(),
  });

  // 4. Define the main VoltAgent application
  return new VoltAgent({
    name: 'DIH-Agent',
    agents: {
      executiveDirector,
    },
    memories: new Memories(),
  });
}

export const DIH = await createAgent();

