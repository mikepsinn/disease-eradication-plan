import { Tool } from '@voltagent/core';
import { glob } from 'glob';
import * as fs from 'fs/promises';
import * as path from 'path';
import matter from 'gray-matter';
import { z } from 'zod';

export interface RepositoryIndex {
  [filePath: string]: {
    title: string;
    description: string;
    tags: string[];
  };
}

const CACHE_PATH = path.join(process.cwd(), '.voltagent', 'repository-index-cache.json');

async function generateRepositoryIndex(): Promise<RepositoryIndex> {
  console.log('[Indexer] Generating repository index...');
  
  // Ensure cache directory exists
  await fs.mkdir(path.dirname(CACHE_PATH), { recursive: true });

  const files = await glob('**/*.md', { ignore: 'node_modules/**' });
  const index: RepositoryIndex = {};

  const indexPromises = files.map(async (file) => {
    try {
      const content = await fs.readFile(file, 'utf-8');
      const { data } = matter(content);
      
      index[file] = {
        title: data.title || 'No Title',
        description: data.description || 'No Description',
        tags: data.tags || [],
      };
    } catch (error) {
      // Ignore files that can't be read
    }
  });

  await Promise.all(indexPromises);
  
  await fs.writeFile(CACHE_PATH, JSON.stringify(index, null, 2), 'utf-8');
  console.log(`[Indexer] Successfully generated and cached index for ${Object.keys(index).length} files.`);
  
  return index;
}

export const repositoryIndexerTool = new Tool({
  name: 'generateRepositoryIndex',
  description: 'Scans all markdown files and creates a JSON index of their metadata. The index is cached for performance.',
  parameters: z.object({}),
  execute: generateRepositoryIndex,
});
