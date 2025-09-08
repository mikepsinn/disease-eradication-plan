import { Agent } from '@voltagent/core';
import { listFiles } from './tools/list-files';
import { readFile } from './tools/read-file';
import { writeFile } from './tools/write-file';
import { webSearch } from './tools/web-search';
import { parseYaml } from './tools/parse-yaml';
import { writeYaml } from './tools/write-yaml';
import { generateProjectStatusReport } from './tools/generate-project-status-report';
import * as yaml from 'js-yaml';
import * as matter from 'gray-matter';
import slugify from 'slugify';

// Define the main agent
export const agent = new Agent({
  id: 'dih-executive-director',
  name: 'DIH Executive Director',
  // The system prompt is defined by the initial messages in the context.
  // We will add the persona as the first system message.
  prompt: async function* (context: any) {
    // Standard agent startup logic
    const userMessage = context.messages.findLast((m: any) => m.role === 'user');
    if (!userMessage) {
      yield 'I am ready to receive tasks, but I did not receive a user message.';
      return;
    }

    // 1. Find the next available task
    const issueFiles = await listFiles({ directory: 'operations/issues' });
    let nextTask: { number: number; title: string; [key: string]: any } | null = null;

    for (const fileName of issueFiles.sort()) {
      const fileContent = await readFile({
        filePath: `operations/issues/${fileName}`,
      });
      const { data: frontmatter } = matter(fileContent);

      if (
        frontmatter.state === 'open' &&
        frontmatter.assignees?.includes('agent')
      ) {
        // Extract number from filename, e.g., "45-..." -> 45
        const issueNumber = parseInt(fileName.split('-')[0], 10);
        nextTask = { number: issueNumber, title: frontmatter.title, ...frontmatter };
        break; // Found our task
      }
    }

    // 2. Report on the next task
    if (nextTask) {
      yield `I have received your message. My next assigned task is #${nextTask.number}: "${nextTask.title}". I will begin working on it.`;
    } else {
      yield `I have received your message. I have no open tasks assigned to me.`;
    }
  },
  server: {
    port: 8181,
    providers: {
      mcp: true,
    },
  },
  tools: [
    listFiles,
    readFile,
    writeFile,
    webSearch,
    parseYaml,
    writeYaml,
    generateProjectStatusReport,
  ],
});
