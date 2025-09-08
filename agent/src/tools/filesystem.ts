import { Tool } from '@voltagent/core';
import * as fs from 'fs/promises';
import { z } from 'zod';

export const readFileTool = new Tool({
  name: 'readFile',
  description: 'Reads the content of a file.',
  parameters: z.object({
    path: z.string().describe('The path to the file to read.'),
  }),
  execute: async ({ path }) => {
    try {
      const content = await fs.readFile(path, 'utf-8');
      return content;
    } catch (error) {
      return `Error reading file: ${error.message}`;
    }
  },
});

export const writeFileTool = new Tool({
  name: 'writeFile',
  description: 'Writes content to a file.',
  parameters: z.object({
    path: z.string().describe('The path to the file to write.'),
    content: z.string().describe('The content to write to the file.'),
  }),
  execute: async ({ path, content }) => {
    try {
      await fs.writeFile(path, content, 'utf-8');
      return `File written successfully to ${path}.`;
    } catch (error) {
      return `Error writing file: ${error.message}`;
    }
  },
});

export const listFilesTool = new Tool({
  name: 'listFiles',
  description: 'Lists all files in a directory.',
  parameters: z.object({
    path: z.string().describe('The path to the directory to list.'),
  }),
  execute: async ({ path }) => {
    try {
      const files = await fs.readdir(path);
      return files.join('\n');
    } catch (error) {
      return `Error listing files: ${error.message}`;
    }
  },
});
