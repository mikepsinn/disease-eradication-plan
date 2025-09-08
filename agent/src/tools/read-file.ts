import { Tool } from '@voltagent/core';
import * as fs from 'node:fs/promises';
import * as path from 'node:path';
import { z } from 'zod';

export const readFile = new Tool({
  id: 'read-file',
  name: 'Read File',
  description: 'Reads the content of a specified file.',
  parameters: z.object({
    filePath: z.string().describe('The path to the file to read, relative to the project root.'),
  }),
  output: z.string(),
  run: async ({ parameters }) => {
    const { filePath } = parameters;
    const absolutePath = path.resolve(process.cwd(), filePath);
    const content = await fs.readFile(absolutePath, 'utf-8');
    return content;
  },
});
