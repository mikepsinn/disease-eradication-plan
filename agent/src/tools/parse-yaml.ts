import { Tool } from '@voltagent/core';
import * as fs from 'node:fs/promises';
import * as path from 'node:path';
import { z } from 'zod';
import * as yaml from 'js-yaml';

export const parseYaml = new Tool({
  id: 'parse-yaml',
  name: 'Parse YAML',
  description: 'Reads a YAML file and parses it into a JSON object.',
  parameters: z.object({
    filePath: z.string().describe('The path to the YAML file to parse, relative to the project root.'),
  }),
  output: z.any().describe('The JSON object parsed from the YAML file.'),
  run: async ({ parameters }) => {
    const { filePath } = parameters;
    const absolutePath = path.resolve(process.cwd(), filePath);
    const fileContent = await fs.readFile(absolutePath, 'utf-8');
    const parsedYaml = yaml.load(fileContent);
    return parsedYaml;
  },
});
