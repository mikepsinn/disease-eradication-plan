import { Tool } from '@voltagent/core';
import { glob } from 'glob';
import * as fs from 'fs/promises';
import * as path from 'path';
import matter from 'gray-matter';
import { z } from 'zod';
import simpleGit from 'simple-git';

export interface RepositoryIndex {
  [filePath: string]: {
    title: string;
    description: string;
    tags: string[];
    lastModified: string;
    lastReviewed: string;
  };
}

const CACHE_PATH = path.join(process.cwd(), '.voltagent', 'repository-index-cache.json');

async function generateRepositoryIndex(): Promise<RepositoryIndex> {
  console.log('[Indexer] Generating repository index...');
  
  await fs.mkdir(path.dirname(CACHE_PATH), { recursive: true });
  const git = simpleGit();
  const files = await glob('**/*.md', { ignore: 'node_modules/**' });
  const index: RepositoryIndex = {};

  const indexPromises = files.map(async (file) => {
    try {
      const content = await fs.readFile(file, 'utf-8');
      const { data } = matter(content);
      const log = await git.log({ file, maxCount: 1 });
      
      const lastModified = log.latest?.date || new Date(0).toISOString();
      const lastReviewed = data.lastReviewed || new Date(0).toISOString();
      
      index[file] = {
        title: data.title || 'No Title',
        description: data.description || 'No Description',
        tags: data.tags || [],
        lastModified,
        lastReviewed,
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
  description: 'Scans all markdown files and creates a JSON index of their metadata, including last modification and review dates.',
  parameters: z.object({}),
  execute: generateRepositoryIndex,
});
