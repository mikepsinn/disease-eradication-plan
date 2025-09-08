import { Tool } from '@voltagent/core';
import * as fs from 'node:fs/promises';
import * as path from 'node:path';
import { z } from 'zod';
import * as yaml from 'js-yaml';

export const writeYaml = new Tool({
  id: 'write-yaml',
  name: 'Write YAML',
  description: 'Writes a JSON object to a specified YAML file.',
  parameters: z.object({
    filePath: z.string().describe('The path to the YAML file to write, relative to the project root.'),
    data: z.any().describe('The JSON object to write to the file.'),
  }),
  output: z.string(),
  run: async ({ parameters }) => {
    const { filePath, data } = parameters;
    const absolutePath = path.resolve(process.cwd(), filePath);
    const yamlString = yaml.dump(data);
    await fs.writeFile(absolutePath, yamlString, 'utf-8');
    return `Successfully wrote YAML to ${filePath}.`;
  },
});
