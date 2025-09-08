import { Tool } from '@voltagent/core';
import * as fs from 'node:fs/promises';
import * as path from 'node:path';
import { z } from 'zod';

export const listFiles = new Tool({
  id: 'list-files',
  name: 'List Files',
  description: 'Lists all files and directories within a specified directory.',
  // Define the input schema for the tool using Zod for validation.
  parameters: z.object({
    directory: z.string().describe(
      'The directory to list files from, relative to the project root.'
    ),
  }),
  // Define the output schema for the tool.
  output: z.array(z.string()),
  // The run function contains the actual logic of the tool.
  run: async ({ parameters }) => {
    const { directory } = parameters;
    // Resolve the absolute path to prevent directory traversal issues.
    const absolutePath = path.resolve(process.cwd(), directory);
    // Read the directory and return the list of files.
    const files = await fs.readdir(absolutePath);
    return files;
  },
});
