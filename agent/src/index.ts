import { Agent } from '@voltagent/core';
import { listFiles } from './tools/list-files';
import { readFile } from './tools/read-file';
import { writeFile } from './tools/write-file';

// Define the persona and capabilities of our agent
const executiveDirectorPrompt = `You are the Executive Director of the Decentralized Institutes of Health (DIH).
Your role is to manage the DIH wiki, oversee project management, and coordinate human efforts.
You are diligent, autonomous, and focused on maintaining the integrity and progress of the DIH initiative.
You operate by interacting with the file system and a defined set of tools.`;

// Define the main agent
export const agent = new Agent({
  id: 'dih-executive-director',
  name: 'DIH Executive Director',
  // The system prompt sets the agent's persona and high-level instructions.
  system: executiveDirectorPrompt,
  // The prompt function is the entry point for the agent's work cycle.
  // It will receive context and is expected to return a response.
  prompt: async function* (context) {
    // Find the last message from the user in the conversation history.
    const userMessage = context.messages.findLast((m) => m.role === 'user');

    // If there's no user message, we can't proceed.
    if (!userMessage) {
      yield 'I am ready to receive tasks, but I did not receive a user message.';
      return;
    }

    // 1. Read the planning document.
    const readmeContent = await readFile({
      filePath: 'agent/README.md',
    });

    // 2. Identify the next task and create the updated content.
    // This is a simple string replacement for demonstration purposes.
    // Future iterations will use more robust parsing logic.
    const updatedReadmeContent = readmeContent.replace(
      '-   [ ] Implement `readFile` and `editFile` tools.',
      '-   [x] Implement `readFile` and `editFile` tools.'
    );

    // 3. Autonomously update the planning document.
    await writeFile({
      filePath: 'agent/README.md',
      content: updatedReadmeContent,
    });

    // 4. Respond with a confirmation of the autonomous action.
    yield `I have received the task: "${userMessage.content}". I have read my planning document, identified that my next task was to implement file system tools, and have now autonomously updated the roadmap to mark this task as complete.`;
  },
  server: {
    port: 8181,
    providers: {
      mcp: true,
    },
  },
  tools: [listFiles, readFile, writeFile],
});
